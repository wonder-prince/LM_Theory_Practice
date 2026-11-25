"""Readable exports preserve error evidence and work without API/model execution."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent_cli import main, save_results, summarize
from trace_readable import fenced, render_trace, tool_status


def fixture():
    return {'task_id': 'sample', 'kind': 'scripted_mock', 'stop_reason': 'completed',
            'decisions': 2, 'tool_calls': 1, 'final_text': '示例最终回答',
            'input': {'request': '核查订单', 'scope': {}}, 'config': {},
            'trace': [
                {'event': 'model_input', 'decision': 1, 'messages': [{'role': 'user', 'content': '历史正文哨兵'}]},
                {'event': 'model_output', 'decision': 1, 'message': {'role': 'assistant', 'content': '尝试计算',
                 'tool_calls': [{'id': 'c1', 'function': {'name': 'calculate_reconciliation', 'arguments': '{"receipt_ids":["wrong"]}'}}]}},
                {'event': 'tool_result', 'tool_call_id': 'c1', 'tool': 'calculate_reconciliation',
                 'arguments': '{"receipt_ids":["wrong"]}', 'executed': True,
                 'result': {'ok': False, 'data': None, 'error': {'code': 'TRANSACTION_UNAVAILABLE'}}},
                {'event': 'model_input', 'decision': 2, 'messages': []},
                {'event': 'model_output', 'decision': 2, 'message': {'role': 'assistant', 'content': '示例最终回答'}}]}


class ReadableTests(unittest.TestCase):
    def test_rounds_parameters_and_errors_are_visible_without_history_duplicates(self):
        row = fixture()
        text = render_trace([row])
        self.assertIn('第 1 轮', text)
        self.assertIn('第 2 轮', text)
        self.assertIn('TRANSACTION_UNAVAILABLE', text)
        self.assertIn('"wrong"', text)
        self.assertIn('c1', text)
        self.assertIn('示例最终回答', text)
        self.assertNotIn('历史正文哨兵', text)
        self.assertIn('| --- | --- | --- | ---: | ---: | ---: |\n| [1]', text)

    def test_call_success_is_distinct_from_plan_failure_and_not_executed(self):
        event = {'executed': True, 'result': {'ok': True, 'data': {'valid': False}}}
        self.assertEqual(tool_status(event), '调用成功，方案未通过')
        event['executed'] = False
        self.assertEqual(tool_status(event), '未执行')

    def test_save_preserves_raw_payload_and_refuses_overwrite(self):
        row = fixture()
        original = copy.deepcopy(row)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            save_results(output, [row], summarize([row]))
            self.assertEqual(json.loads((output / 'traces.json').read_text()), [row])
            self.assertIn('\n  {\n', (output / 'traces.json').read_text())
            self.assertEqual({p.name for p in output.iterdir()}, {'traces.json', 'summary.json'})
            self.assertEqual(row, original)
            with self.assertRaises(FileExistsError):
                save_results(output, [row], {})

    def test_offline_conversion_does_not_create_backend_or_run_agent(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'old.jsonl'
            source.write_text(json.dumps(fixture(), ensure_ascii=False) + '\n', encoding='utf-8')
            output = Path(directory) / 'readable'
            with patch('agent_cli.OpenAIBackend.from_env') as backend, patch('agent_cli.run_agent') as runner:
                self.assertEqual(main(['--render-trace', str(source), '--output-dir', str(output)]), 0)
                backend.assert_not_called()
                runner.assert_not_called()
            self.assertTrue((output / 'traces.json').exists())
            second = Path(directory) / 'second'
            self.assertEqual(main(['--render-trace', str(output / 'traces.json'), '--output-dir', str(second)]), 0)
            self.assertEqual(json.loads((second / 'traces.json').read_text()), [fixture()])

    def test_invalid_arguments_and_embedded_fences_are_preserved(self):
        row = fixture()
        row['trace'][2]['arguments'] = '{bad ``` json'
        self.assertIn('"{bad ``` json"', render_trace([row]))
        self.assertTrue(fenced('```').startswith('````\n'))

    def test_multiple_tasks_and_model_error_remain_separate(self):
        first, second = fixture(), fixture()
        second.update(task_id='second', final_text='', stop_reason='api_error:HTTP_401')
        second['trace'] = [{'event': 'model_error', 'decision': 1, 'code': 'HTTP_401'}]
        text = render_trace([first, second])
        self.assertIn('id="task-2"', text)
        self.assertIn('HTTP_401', text)
        self.assertIn('未产生最终回答', text)


if __name__ == '__main__':
    unittest.main()
