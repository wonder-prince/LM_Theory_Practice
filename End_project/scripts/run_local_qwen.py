"""在本机 GPU 上运行 Qwen3 4bit Agent；不使用外部 API、不训练。"""
import argparse
from datetime import datetime
import hashlib
import json
import logging
import os
from pathlib import Path
import sys
import time
from dataclasses import asdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_cli import load_tasks, summarize
from agent_runtime import Budget, run_agent
from business_tools import ToolSession
from local_model_backend import LocalQwenBackend
from trace_readable import render_trace
from evaluation import (add_evaluation_arguments, evaluate_results, pricing_from_args,
                        write_evaluation_report)


def write_json(path, value):
    temporary = path.with_name(path.name + '.tmp')
    payload = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    for attempt in range(10):
        try:
            temporary.write_text(payload, encoding='utf-8')
            temporary.replace(path)
            return
        except PermissionError:
            # Windows readers/scanners can briefly deny FILE_SHARE_DELETE.
            if attempt == 9:
                raise
            time.sleep(min(.05 * 2 ** attempt, 1.0))


def load_resume(directory, tasks, args, budget, rules):
    manifest = json.loads((directory / 'run_manifest.json').read_text(encoding='utf-8'))
    previous_args = manifest['arguments']
    keys = ('split', 'max_context', 'max_new_tokens', 'max_decisions', 'timeout',
            'input_price_per_million', 'output_price_per_million',
            'compute_price_per_hour', 'cost_currency')
    if any(previous_args.get(key) != getattr(args, key) for key in keys):
        raise ValueError('续跑必须保持原切分、推理预算与费用配置')
    if Path(previous_args['model_dir']).resolve() != args.model_dir.resolve():
        raise ValueError('续跑必须使用原模型目录')
    if manifest['budget'] != asdict(budget) or manifest['task_ids'] != [t['task_id'] for t in tasks]:
        raise ValueError('续跑任务列表或调用预算与原批次不一致')
    results = json.loads((directory / 'traces.json').read_text(encoding='utf-8'))
    if not isinstance(results, list) or [r['task_id'] for r in results] != manifest['task_ids'][:len(results)]:
        raise ValueError('已有轨迹必须是原任务列表的有序前缀')
    if len(results) >= len(tasks):
        raise ValueError('原批次已经处理全部任务，无需续跑')
    for result, task in zip(results, tasks):
        if result['input'].get('scope') != task['query'] or result['input'].get('rules') != rules:
            raise ValueError('已有轨迹的任务范围或规则与当前数据不一致')
    provenance = directory / 'source_provenance.json'
    if provenance.exists():
        for name, expected in json.loads(provenance.read_text(encoding='utf-8'))['sha256'].items():
            # Only the batch runner may change to add checkpoint recovery.
            if name == 'scripts/run_local_qwen.py':
                continue
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError('续跑所用源码/数据已变化：' + name)
    return results


def run_task(task, visible, split, rules, backend, budget):
    session = ToolSession.from_visible(visible, split, task['environment_file'], task['query'])
    started = time.monotonic()
    try:
        return run_agent(session, task['request'], task['query'], rules, backend, budget, task['task_id'])
    except RuntimeError as exc:
        # Normal model errors/OOM are handled inside the graph. Retain an explicit
        # failed row if an unexpected CUDA/runtime error escapes, then try the next task.
        logging.exception('任务运行异常：%s', task['task_id'])
        return {'task_id': task['task_id'], 'kind': backend.kind, 'model_connected': False,
                'config': {'backend': backend.metadata(), 'budget': asdict(budget)},
                'input': {'request': task['request'], 'scope': task['query'], 'rules': rules},
                'trace': [{'event': 'runner_error', 'code': type(exc).__name__}],
                'messages': [], 'final_text': '', 'stop_reason': 'runner_error:' + type(exc).__name__,
                'decisions': 0, 'tool_calls': 0, 'steps': 0, 'recorded_trace_incomplete': True,
                'token_usage': None, 'token_usage_complete': False,
                'elapsed_seconds': round(time.monotonic() - started, 6)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model-dir', type=Path, default=ROOT / 'models/Qwen3-4B-Instruct-2507')
    parser.add_argument('--split', choices=['train', 'val'], default='train')
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument('--task-id')
    choice.add_argument('--limit', type=int, default=1, help='任务数，1到50；只加载一次模型，结束后自动释放')
    parser.add_argument('--max-context', type=int, default=16384)
    parser.add_argument('--max-new-tokens', type=int, default=2048)
    parser.add_argument('--max-decisions', type=int, default=12)
    parser.add_argument('--timeout', type=float, default=1000, help='单题超时秒数（默认 %(default)s）')
    parser.add_argument('--resume-from', type=Path, help='读取原批次已保存前缀，仅执行剩余题；写入新的输出目录')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'artifacts' /
                        ('local_qwen_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f')))
    add_evaluation_arguments(parser)
    args = parser.parse_args()
    pricing = pricing_from_args(args)
    if args.max_context < 1 or args.max_new_tokens < 1:
        parser.error('token 预算必须为正整数')
    if not 1 <= args.limit <= 50:
        parser.error('limit 仅支持 1 到 50')
    if args.output_dir.exists():
        parser.error('输出目录已存在，请指定新目录')
    visible = ROOT / 'datasets/prepared/agent_visible'
    tasks, rules = load_tasks(visible, args.split, args.task_id, limit=args.limit)
    budget = Budget(max_decisions=args.max_decisions, timeout_seconds=args.timeout)
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING)
    logging.getLogger('local_model_backend').setLevel(logging.INFO)
    try:
        results = load_resume(args.resume_from, tasks, args, budget, rules) if args.resume_from else []
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error('无法续跑：' + str(exc))
    resumed_tasks = len(results)
    backend = None
    args.output_dir.mkdir(parents=True, exist_ok=False)
    status = {'pid': os.getpid(), 'phase': 'loading_model', 'split': args.split,
              'requested_tasks': len(tasks), 'processed_tasks': resumed_tasks,
              'resumed_tasks': resumed_tasks,
              'started_at': datetime.now().astimezone().isoformat(), 'current_task_id': None,
              'model_cleanup': {'status': 'pending'}}
    write_json(args.output_dir / 'run_status.json', status)
    write_json(args.output_dir / 'run_manifest.json', {
        'task_ids': [task['task_id'] for task in tasks], 'arguments': {k: str(v) if isinstance(v, Path) else v
        for k, v in vars(args).items()}, 'budget': asdict(budget), 'pid': os.getpid()})

    def save():
        summary = summarize(results)
        summary.update(local_model=backend.metadata(), split=args.split, requested_tasks=len(tasks))
        summary['run_progress'] = {k: status[k] for k in ('phase', 'requested_tasks', 'processed_tasks')}
        summary['model_cleanup'] = status['model_cleanup']
        for filename, value in (('traces.json', results), ('summary.json', summary)):
            write_json(args.output_dir / filename, value)
        (args.output_dir / 'traces.md').write_text(render_trace(results), encoding='utf-8')
        write_evaluation_report(args.output_dir, results, summary)
        return summary

    try:
        print(f'加载本地模型：{args.model_dir.resolve()}', flush=True)
        backend = LocalQwenBackend(args.model_dir, args.max_context, args.max_new_tokens)
        status['phase'] = 'running'
        save()
        for index, task in enumerate(tasks[resumed_tasks:], resumed_tasks + 1):
            status['current_task_id'] = task['task_id']
            status['processed_tasks'] = len(results)
            write_json(args.output_dir / 'run_status.json', status)
            print(f'[{index}/{len(tasks)}] {task["task_id"]} ({task["query"]["mode"]})', flush=True)
            row = run_task(task, visible, args.split, rules, backend, budget)
            results.extend(evaluate_results([row], visible, args.split, pricing))
            status['processed_tasks'] = len(results)
            summary = save()
            write_json(args.output_dir / 'run_status.json', status)
            print(json.dumps({k: summary['task_results'][-1].get(k) for k in
                             ('task_id', 'stop_reason', 'accuracy', 'elapsed_seconds', 'tool_errors')},
                             ensure_ascii=False), flush=True)
        status.update(phase='finished', current_task_id=None)
    except BaseException as exc:
        status.update(phase='failed', error_type=type(exc).__name__)
        raise
    finally:
        if backend is not None:
            try:
                status['model_cleanup'] = backend.close()
            except Exception as exc:
                logging.exception('模型释放失败，进程退出时仍会销毁CUDA上下文')
                status['model_cleanup'] = {'status': 'close_error', 'error_type': type(exc).__name__}
        else:
            status['model_cleanup'] = {'status': 'constructor_not_completed_process_exit_releases_cuda'}
        status['finished_at'] = datetime.now().astimezone().isoformat()
        status['processed_tasks'] = len(results)
        write_json(args.output_dir / 'run_status.json', status)
        if backend is not None:
            summary = save()
        print('模型清理：' + json.dumps(status['model_cleanup'], ensure_ascii=False), flush=True)
    print(json.dumps({k: summary.get(k) for k in ('tasks', 'accuracy', 'cost', 'stop_reasons')},
                     ensure_ascii=False, indent=2))
    print('完整结果：' + str(args.output_dir.resolve()))
    return 0 if all(row['stop_reason'] == 'completed' for row in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
