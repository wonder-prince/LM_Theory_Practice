"""Batch checkpoint and shutdown lifecycle checks without loading a GPU model."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_local_qwen as runner
from agent_runtime import Budget


def task(index):
    return {'task_id': str(index), 'environment_file': 'unused.json', 'request': 'fixture',
            'query': {'mode': 'single_order'}}


def row(index):
    return {'task_id': str(index), 'kind': 'scripted_mock', 'model_connected': False,
            'config': {}, 'input': {}, 'trace': [], 'messages': [], 'final_text': 'fixture',
            'stop_reason': 'completed', 'decisions': 1, 'tool_calls': 0, 'steps': 1,
            'elapsed_seconds': .01, 'token_usage': None, 'token_usage_complete': False}


class RunnerLifecycleTests(unittest.TestCase):
    def test_all_50_are_checkpointed_and_model_is_closed(self):
        backend = Mock(kind='scripted_mock')
        backend.metadata.return_value = {'model': 'mock-only'}
        backend.close.return_value = {'status': 'closed'}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            argv = ['run_local_qwen.py', '--split', 'val', '--limit', '50', '--output-dir', str(output)]
            with patch.object(sys, 'argv', argv), patch.object(runner, 'LocalQwenBackend', return_value=backend), \
                 patch.object(runner, 'load_tasks', return_value=([task(i) for i in range(50)], {})), \
                 patch.object(runner, 'run_task', side_effect=[row(i) for i in range(50)]) as execute, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(), 0)
            backend.close.assert_called_once()
            self.assertEqual(execute.call_count, 50)
            state = json.loads((output / 'run_status.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'finished')
            self.assertEqual(state['processed_tasks'], 50)
            self.assertEqual(state['model_cleanup']['status'], 'closed')
            self.assertEqual(len(json.loads((output / 'traces.json').read_text(encoding='utf-8'))), 50)

    def test_fatal_error_keeps_previous_task_and_still_closes_model(self):
        backend = Mock(kind='scripted_mock')
        backend.metadata.return_value = {}
        backend.close.return_value = {'status': 'closed'}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            argv = ['run_local_qwen.py', '--limit', '2', '--output-dir', str(output)]
            with patch.object(sys, 'argv', argv), patch.object(runner, 'LocalQwenBackend', return_value=backend), \
                 patch.object(runner, 'load_tasks', return_value=([task(0), task(1)], {})), \
                 patch.object(runner, 'run_task', side_effect=[row(0), ValueError('fatal fixture')]), \
                 contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
                runner.main()
            backend.close.assert_called_once()
            state = json.loads((output / 'run_status.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'failed')
            self.assertEqual(state['processed_tasks'], 1)
            self.assertEqual(len(json.loads((output / 'traces.json').read_text(encoding='utf-8'))), 1)

    def test_unexpected_runtime_error_is_an_explicit_incomplete_record(self):
        backend = Mock(kind='local_transformers')
        backend.metadata.return_value = {}
        with patch.object(runner.ToolSession, 'from_visible'), \
             patch.object(runner, 'run_agent', side_effect=RuntimeError('runtime fixture')), \
             self.assertLogs(level='ERROR'):
            result = runner.run_task(task(0), ROOT, 'val', {}, backend, Budget())
        self.assertTrue(result['recorded_trace_incomplete'])
        self.assertFalse(result['token_usage_complete'])
        self.assertEqual(result['stop_reason'], 'runner_error:RuntimeError')


if __name__ == '__main__':
    unittest.main()
