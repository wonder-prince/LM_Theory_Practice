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
            'config': {}, 'input': {'scope': task(index)['query'], 'rules': {}},
            'trace': [], 'messages': [], 'final_text': 'fixture',
            'stop_reason': 'completed', 'decisions': 1, 'tool_calls': 0, 'steps': 1,
            'elapsed_seconds': .01, 'token_usage': None, 'token_usage_complete': False}


class RunnerLifecycleTests(unittest.TestCase):
    def test_checkpoint_retries_a_temporary_windows_file_lock(self):
        original_replace = Path.replace
        attempts = []

        def replace(source, target):
            attempts.append(source)
            if len(attempts) == 1:
                self.assertEqual(json.loads(target.read_text(encoding='utf-8')), {'old': True})
                raise PermissionError('temporary Windows file lock')
            return original_replace(source, target)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'status.json'
            path.write_text('{"old": true}', encoding='utf-8')
            with patch.object(Path, 'replace', replace), patch.object(runner.time, 'sleep') as sleep:
                runner.write_json(path, {'new': True})
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), {'new': True})
            self.assertFalse(path.with_name(path.name + '.tmp').exists())
            sleep.assert_called_once_with(.05)

    def test_checkpoint_permanent_permission_failure_has_bounded_retries(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'status.json'
            path.write_text('{"old": true}', encoding='utf-8')
            with patch.object(Path, 'replace', side_effect=PermissionError('locked')) as replace, \
                 patch.object(runner.time, 'sleep') as sleep, self.assertRaises(PermissionError):
                runner.write_json(path, {'new': True})
            self.assertEqual(replace.call_count, 10)
            self.assertEqual(sleep.call_count, 9)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), {'old': True})

    def test_resume_keeps_saved_rows_and_runs_only_remaining_tasks(self):
        backend = Mock(kind='scripted_mock')
        backend.metadata.return_value = {'model': 'mock-only'}
        backend.close.return_value = {'status': 'closed'}
        with tempfile.TemporaryDirectory() as directory:
            previous, output = Path(directory) / 'previous', Path(directory) / 'continued'
            argv = ['run_local_qwen.py', '--limit', '5', '--output-dir', str(previous)]
            with patch.object(sys, 'argv', argv), patch.object(runner, 'LocalQwenBackend', return_value=backend), \
                 patch.object(runner, 'load_tasks', return_value=([task(i) for i in range(5)], {})), \
                 patch.object(runner, 'run_task', side_effect=[row(0), row(1), ValueError('interrupted')]), \
                 contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
                runner.main()
            saved = (previous / 'traces.json').read_bytes()
            argv = ['run_local_qwen.py', '--limit', '5', '--resume-from', str(previous), '--output-dir', str(output)]
            with patch.object(sys, 'argv', argv), patch.object(runner, 'LocalQwenBackend', return_value=backend), \
                 patch.object(runner, 'load_tasks', return_value=([task(i) for i in range(5)], {})), \
                 patch.object(runner, 'run_task', side_effect=[row(2), row(3), row(4)]) as execute, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(), 0)
            self.assertEqual([call.args[0]['task_id'] for call in execute.call_args_list], ['2', '3', '4'])
            self.assertEqual((previous / 'traces.json').read_bytes(), saved)
            self.assertEqual(json.loads((output / 'traces.json').read_text(encoding='utf-8'))[:2], json.loads(saved))
            state = json.loads((output / 'run_status.json').read_text(encoding='utf-8'))
            self.assertEqual((state['phase'], state['processed_tasks'], state['resumed_tasks']), ('finished', 5, 2))
            changed = Path(directory) / 'changed'
            argv = argv[:-1] + [str(changed), '--max-decisions', '13']
            with patch.object(sys, 'argv', argv), patch.object(runner, 'LocalQwenBackend') as load, \
                 patch.object(runner, 'load_tasks', return_value=([task(i) for i in range(5)], {})), \
                 contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                runner.main()
            load.assert_not_called()
            self.assertFalse(changed.exists())

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
