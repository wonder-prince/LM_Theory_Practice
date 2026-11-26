"""选择已有 train/val 任务运行八工具规则演示；无需模型 API。"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_cli import load_tasks, save_results
from business_tools import ToolSession
from tool_demo import run_demo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--split', choices=['train', 'val'], default='train')
    parser.add_argument('--task-id', help='默认运行当前切分的第一条任务')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'artifacts' /
                        ('local_case_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f')))
    args = parser.parse_args()
    try:
        if args.output_dir.exists():
            raise ValueError('输出目录已存在，请指定新目录')
        visible = ROOT / 'datasets/prepared/agent_visible'
        tasks, _ = load_tasks(visible, args.split, args.task_id, limit=1)
        task = tasks[0]
        session = ToolSession.from_visible(visible, args.split, task['environment_file'], task['query'])
        result = run_demo(session)
        result.update(task_id=task['task_id'], request=task['request'], query=task['query'])
        summary = {
            'kind': result['kind'],
            'model_connected': False,
            'task_id': task['task_id'],
            'split': args.split,
            'tool_calls': len(result['calls']),
            'distinct_tools': sorted({call['tool'] for call in result['calls']}),
            'validation': result['validation'],
            'orders': len(result['plan']['orders']),
            'unallocated_transaction_ids': result['plan']['unallocated_transaction_ids'],
            'balances': [row['balance'] for row in result['plan']['orders']],
            'evaluation': '确定性业务工具自检；不代表模型能力或独立评测正确率',
        }
        save_results(args.output_dir, [result], summary)
    except (ValueError, RuntimeError, OSError) as exc:
        print('运行失败：' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('完整结果：' + str(args.output_dir.resolve()))
    return 0 if summary['validation']['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())