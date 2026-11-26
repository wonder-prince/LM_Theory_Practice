"""train/val单任务与小批量基线入口；正式test不开放。"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import sys

from agent_runtime import Budget, run_agent
from business_tools import ToolSession
from model_backends import OpenAIBackend, SmokeBackend
from evaluation import (add_evaluation_arguments, evaluate_results, pricing_from_args,
                        summarize_evaluations, tool_metrics, write_evaluation_report)

ROOT = Path(__file__).resolve().parent


def load_tasks(visible_root, split, task_id=None, limit=1):
    root = Path(visible_root).absolute()
    if root.name != 'agent_visible' or root.resolve() != root or split not in ('train', 'val'):
        raise ValueError('仅允许真实agent_visible目录的train/val')
    path = root / split / 'tasks.jsonl'
    rules_path = root / 'rules.json'
    if path.resolve() != path or rules_path.resolve() != rules_path:
        raise ValueError('拒绝任务或规则符号链接')
    with path.open() as stream:
        rows = (json.loads(line) for line in stream if line.strip())
        if task_id:
            tasks = list(itertools.islice((row for row in rows if row['task_id'] == task_id), 1))
        else:
            tasks = list(itertools.islice(rows, limit))
    if not tasks:
        raise ValueError('当前切分未找到任务')
    return tasks, json.loads(rules_path.read_text())


def run_batch(tasks, visible_root, split, rules, backend_factory, budget):
    results = []
    for task in tasks:
        # trusted runner读取单任务快照；不将快照、路径或隐藏文件传给模型。
        session = ToolSession.from_visible(visible_root, split, task['environment_file'], task['query'])
        results.append(run_agent(session, task['request'], task['query'], rules, backend_factory(), budget, task['task_id']))
    return results


def summarize(results):
    kinds = sorted({row['kind'] for row in results})
    summary = {'tasks': len(results), 'kinds': kinds, 'stop_reasons': dict(Counter(row['stop_reason'] for row in results)),
            'decisions': sum(row['decisions'] for row in results),
            'tool_calls': sum(row['tool_calls'] for row in results), 'cost': None,
            'accuracy': None, 'evaluation': '未接入独立评分；completed只代表返回了非空文本',
            'model_effect_verified': False}
    summary.update(summarize_evaluations(results))
    if any(isinstance(row.get('evaluation'), dict) for row in results):
        summary['task_results'] = [{
            **{key: row.get(key) for key in ('task_id', 'kind', 'stop_reason', 'model_connected',
               'decisions', 'tool_calls', 'elapsed_seconds', 'token_usage', 'accuracy', 'cost', 'evaluation',
               'recorded_trace_incomplete')},
            **tool_metrics(row)} for row in results]
        summary['tool_validated_tasks'] = sum(r['validation_passed'] for r in summary['task_results']
                                               if r['kind'] in ('real_api', 'local_transformers'))
    return summary


def save_results(output_dir, results, summary):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    with (output_dir / 'traces.json').open('x', encoding='utf-8') as stream:
        json.dump(results, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with (output_dir / 'summary.json').open('x', encoding='utf-8') as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--visible-root', type=Path, default=ROOT / 'datasets/prepared/agent_visible')
    parser.add_argument('--split', choices=['train', 'val'], default='train')
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument('--task-id')
    choice.add_argument('--limit', type=int, default=1, help='小批量任务数，1到20')
    offline = parser.add_mutually_exclusive_group()
    offline.add_argument('--render-trace', type=Path, help='离线格式化已有JSON或旧JSONL完整轨迹，不调用模型或工具')
    offline.add_argument('--evaluate-trace', type=Path, help='离线评测已有轨迹；只读取指定train/val参考答案，不调用模型')
    parser.add_argument('--backend', choices=['api', 'scripted'], default='api')
    parser.add_argument('--profile', choices=['base', 'sft'], default='base')
    parser.add_argument('--max-decisions', type=int, default=12)
    parser.add_argument('--max-tools', type=int, default=48)
    parser.add_argument('--max-steps', type=int, default=60)
    parser.add_argument('--timeout', type=float, default=120.0)
    parser.add_argument('--output-dir', type=Path, required=True, help='必须是不存在的新目录，避免覆盖历史轨迹')
    add_evaluation_arguments(parser)
    args = parser.parse_args(argv)
    try:
        pricing = pricing_from_args(args)
        if not 1 <= args.limit <= 20:
            raise ValueError('limit仅支持1到20')
        if args.output_dir.exists():
            raise ValueError('输出目录已存在，请指定新目录')
        if args.render_trace or args.evaluate_trace:
            # 直接转换已经脱敏的运行结果，不接触.env，不修改原日志。
            text = (args.render_trace or args.evaluate_trace).read_text(encoding='utf-8')
            try:
                parsed = json.loads(text)
                results = parsed if isinstance(parsed, list) else [parsed]
            except json.JSONDecodeError:
                results = [json.loads(line) for line in text.splitlines() if line.strip()]
            if not results or not all(isinstance(r, dict) and isinstance(r.get('trace'), list) for r in results):
                raise ValueError('输入必须为非空运行结果JSON/JSONL，每个任务包含trace数组')
            if args.evaluate_trace:
                results = evaluate_results(results, args.visible_root, args.split, pricing)
            summary = summarize(results)
            save_results(args.output_dir, results, summary)
            if args.evaluate_trace:
                write_evaluation_report(args.output_dir, results, summary)
            print(('已离线评测：' + str(args.output_dir / 'evaluation.md')) if args.evaluate_trace
                  else ('已离线转换轨迹：' + str(args.output_dir / 'traces.json')))
            return 0
        budget = Budget(args.max_decisions, args.max_tools, args.max_steps, args.timeout)
        if args.backend == 'api':
            # 在读环境、运行图或发请求前校验必填配置。
            configured = OpenAIBackend.from_env(args.profile)
            factory = lambda: OpenAIBackend(configured._key, configured.base_url, configured.model, configured.profile)
        else:
            factory = SmokeBackend
        tasks, rules = load_tasks(args.visible_root, args.split, args.task_id, args.limit)
        results = run_batch(tasks, args.visible_root, args.split, rules, factory, budget)
        results = evaluate_results(results, args.visible_root, args.split, pricing)
        summary = summarize(results)
        save_results(args.output_dir, results, summary)
        write_evaluation_report(args.output_dir, results, summary)
    except (ValueError, RuntimeError, OSError) as exc:
        # 本层异常仅来自本地配置/路径/框架；HTTP错误已在适配层归一化。
        print('运行失败：' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all(row['stop_reason'] == 'completed' for row in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
