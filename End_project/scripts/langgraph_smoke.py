"""无凭证烟测产物；显式复用测试夹具，不是模型训练轨迹。"""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from agent_cli import load_tasks, run_batch, summarize, save_results
from agent_runtime import Budget
from model_backends import ScriptedBackend, SmokeBackend, tool_message
from test_langgraph import EightToolScript, HTTPTests, ENV, run_fixture, paired


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'artifacts/langgraph_smoke')
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error('输出目录已存在，请使用--output-dir指定新目录')
    root = ROOT / 'datasets/prepared/agent_visible'
    records = []
    for split in ('train', 'val'):
        tasks, rules = load_tasks(root, split, limit=2)
        for row in run_batch(tasks, root, split, rules, SmokeBackend, Budget()):
            row['smoke_case'] = 'actual_' + split + '_query_loop'
            records.append(row)
    records.append({**run_fixture(EightToolScript()), 'smoke_case': 'fixture_all_eight_normal'})
    import copy
    ambiguous = copy.deepcopy(ENV)
    ambiguous['events'][0].update(order_id=None, merchant_reference=None)
    records.append({**run_fixture(EightToolScript(True), environment=ambiguous), 'smoke_case': 'fixture_ambiguity'})
    for label, backend, budget in [
        ('unknown_invalid_args', ScriptedBackend([
            tool_message(('unknown_tool', {}), ('query_orders', '{'), ('query_refunds', {})),
            {'role': 'assistant', 'content': '脚本异常演示：已收到未知工具、非法JSON和缺参回执。'}]), Budget()),
        ('budget_exhaustion', ScriptedBackend([tool_message(('query_orders', {}), ('search_receipts', {}))]), Budget(max_tools=1)),
        ('empty_final', ScriptedBackend([{'role': 'assistant', 'content': ''}]), Budget()),
    ]:
        records.append({**run_fixture(backend, budget), 'smoke_case': label})
    # 本机HTTP服务仅返回脚本响应，绝不把适配器运行说成真实模型效果。
    server_fixture = HTTPTests('test_http_retry_and_nonretryable_error')
    try:
        backend, requests = server_fixture.serve([(503, {'error': 'mock service unavailable'})])
        backend.kind = 'http_mock'
        records.append({**run_fixture(backend), 'smoke_case': 'http_mock_503', 'mock_http_requests': len(requests)})
    finally:
        server_fixture.doCleanups()
    if not all(paired(row['messages']) for row in records):
        raise RuntimeError('工具消息未配对')
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful() or result.skipped:
        raise RuntimeError('完整.venv测试必须全部通过且无skip')
    summary = summarize(records)
    summary.update({'python': platform.python_version(), 'langgraph': version('langgraph'),
                    'structural_smoke_passed': True, 'tests_run': result.testsRun,
                    'tests_failures': len(result.failures), 'tests_errors': len(result.errors),
                    'tests_skipped': len(result.skipped), 'all_tool_messages_paired': True,
                    'external_model_requests': 0, 'heldout_test_tasks_accessed': False,
                    'notes': 'test目录指代码单测；未读取agent_visible/test。http_mock tokens若有也不是实际模型计费。'})
    hashes = {}
    for name in ('business_tools.py', 'tool_demo.py', 'agent_runtime.py', 'model_backends.py', 'agent_cli.py',
                 'requirements.txt', 'requirements.lock.txt', 'tests/test_langgraph.py', 'scripts/langgraph_smoke.py'):
        hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    summary['code_sha256'] = hashes
    save_results(args.output_dir, records, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
