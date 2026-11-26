"""无凭证真实图测试；不读取留出test/hidden/raw。"""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent_runtime import Budget, run_agent
from evaluation import extract_submission
from agent_cli import load_tasks, run_batch, summarize, main
from business_tools import ToolSession, TOOL_NAMES
from model_backends import OpenAIBackend, ScriptedBackend, SmokeBackend, tool_message

HAS_GRAPH = importlib.util.find_spec('langgraph') is not None
T = '2020-01-10T12:00:00-03:00'
SCOPE = {'mode': 'single_order', 'order_id': 'o1', 'cutoff': T}
ENV = {'orders': [{'order_id': 'o1', 'expected_cents': 1000, 'currency': 'BRL',
                   'merchant_reference': 'mo1', 'created_at': '2020-01-01T00:00:00-03:00'}],
       'events': [{'event_id': 'ep1', 'transaction_id': 'p1', 'amount_cents': 1000, 'currency': 'BRL',
                   'kind': 'receipt', 'status': 'success', 'order_id': 'o1', 'merchant_reference': 'mo1',
                   'original_transaction_id': None, 'effective_at': T, 'observed_at': T}]}
FINAL = {'role': 'assistant', 'content': '脚本测试结束；不是模型推理结果。'}


def paired(messages):
    pending = []
    for message in messages:
        if message['role'] == 'tool':
            if not pending or message['tool_call_id'] != pending.pop(0):
                return False
        else:
            if pending:
                return False
            pending = [call['id'] for call in message.get('tool_calls', [])]
    return not pending


class EightToolScript(ScriptedBackend):
    """根据前一回执填测试参数，仅适用此固定夹具；不用于真实任务决策。"""
    def __init__(self, ambiguous=False):
        self.stage, self.ambiguous = 0, ambiguous

    def complete(self, messages, schemas, deadline):
        self.stage += 1
        if self.stage == 1:
            output = tool_message(('query_orders', {}), ('search_receipts', {}))
        elif self.stage == 2:
            output = tool_message(('find_match_candidates', {'transaction_id': 'p1'}),
                                  ('get_transaction_evidence', {'transaction_id': 'p1'}),
                                  ('check_duplicate_events', {'transaction_ids': ['p1']}),
                                  ('query_refunds', {'order_id': 'o1'}))
        elif self.stage == 3:
            output = tool_message(('calculate_reconciliation', {'order_id': 'o1',
                                  'receipt_ids': [] if self.ambiguous else ['p1'], 'refund_ids': []}))
        elif self.stage == 4:
            balance = json.loads(messages[-1]['content'])['data']
            plan = {'orders': [{'order_id': 'o1', 'receipt_ids': [] if self.ambiguous else ['p1'],
                               'refund_ids': [], 'balance': balance, 'review': self.ambiguous,
                               'review_reason': '同额无强引用，需补证' if self.ambiguous else '',
                               'missing_fields': ['order_id', 'merchant_reference'] if self.ambiguous else []}],
                    'unallocated_transaction_ids': ['p1'] if self.ambiguous else []}
            output = tool_message(('validate_reconciliation', {'plan': plan}))
        else:
            output = {'role': 'assistant', 'content': '脚本夹具：待复核，补订单或商户引用。' if self.ambiguous else FINAL['content']}
        return {'message': output, 'usage': None, 'attempts': 1}


def run_fixture(backend, budget=None, environment=None):
    return run_agent(ToolSession(environment or ENV, SCOPE), '测试订单', SCOPE, {}, backend, budget)


@unittest.skipUnless(HAS_GRAPH, '项目.venv安装LangGraph后执行图测试')
class GraphTests(unittest.TestCase):
    def test_normal_all_eight_and_real_receipts(self):
        result = run_fixture(EightToolScript())
        tools = [e for e in result['trace'] if e['event'] == 'tool_result']
        self.assertEqual({e['tool'] for e in tools}, set(TOOL_NAMES))
        self.assertTrue(all(e['executed'] and e['result']['ok'] for e in tools))
        self.assertTrue(tools[-1]['result']['data']['valid'])
        self.assertEqual(result['decisions'], 5)
        self.assertEqual(result['tool_calls'], 8)
        self.assertEqual(result['stop_reason'], 'completed')
        self.assertTrue(paired(result['messages']))
        self.assertFalse(result['model_connected'])
        self.assertIsNone(result['token_usage'])

    def test_ambiguity_actual_tool_evidence(self):
        env = copy.deepcopy(ENV)
        env['events'][0].update(order_id=None, merchant_reference=None)
        result = run_fixture(EightToolScript(True), environment=env)
        tools = [e for e in result['trace'] if e['event'] == 'tool_result']
        self.assertFalse(tools[2]['result']['data']['candidates'][0]['strong'])
        self.assertTrue(tools[-1]['result']['data']['valid'])
        self.assertIn('待复核', result['final_text'])

    def test_final_json_is_checked_and_repaired_from_feedback(self):
        plan = {'orders': [{'order_id': 'o1', 'receipt_ids': ['ep1'], 'refund_ids': [],
                            'review': False, 'review_reason': '', 'missing_fields': []}],
                'unallocated_transaction_ids': []}

        def final_message():
            return {'role': 'assistant', 'content': f'对账报告\n<reconciliation_result>{json.dumps(plan)}</reconciliation_result>'}

        invalid = final_message()
        plan['orders'][0]['receipt_ids'] = ['p1']
        result = run_fixture(ScriptedBackend([invalid, final_message()]))
        checks = [e for e in result['trace'] if e['event'] == 'submission_check']
        self.assertEqual([c['result']['data']['valid'] for c in checks], [False, True])
        retry = next(e for e in result['trace'] if e['event'] == 'model_input' and e['decision'] == 2)
        self.assertIn('TRANSACTION_UNAVAILABLE', retry['messages'][-1]['content'])
        self.assertEqual(result['stop_reason'], 'completed')
        accepted, source, error = extract_submission(result)
        self.assertEqual((source, error), ('final_json', None))
        self.assertEqual(accepted['orders'][0]['balance']['received_cents'], 1000)
        self.assertEqual(accepted['orders'][0]['balance']['evidence_event_ids'], ['ep1'])
        self.assertEqual(extract_submission({'final_text': result['final_text']})[0], accepted)

    def test_validate_call_computes_balance_before_final_report(self):
        plan = {'orders': [{'order_id': 'o1', 'receipt_ids': ['p1'], 'refund_ids': ['r1'],
                            'review': False, 'review_reason': '', 'missing_fields': []}],
                'unallocated_transaction_ids': []}
        env = copy.deepcopy(ENV)
        env['events'].append({**env['events'][0], 'event_id': 'er1', 'transaction_id': 'r1',
                              'kind': 'refund', 'status': 'pending', 'original_transaction_id': 'p1',
                              'amount_cents': 200})
        result = run_fixture(ScriptedBackend([tool_message(('validate_reconciliation', {'plan': plan})), FINAL]),
                             environment=env)
        self.assertEqual(result['stop_reason'], 'completed')
        self.assertTrue(paired(result['messages']))
        receipt = next(e['result'] for e in result['trace'] if e['event'] == 'tool_result')
        balance = receipt['data']['balances'][0]
        self.assertEqual((balance['net_cents'], balance['pending_refund_cents']), (1000, 200))
        self.assertEqual(extract_submission(result)[0]['orders'][0]['balance']['pending_refund_ids'], ['r1'])

    def test_invalid_final_cannot_fall_back_to_earlier_valid_tool_submission(self):
        valid = {'orders': [{'order_id': 'o1', 'receipt_ids': ['p1'], 'refund_ids': [],
                             'review': False, 'review_reason': '', 'missing_fields': []}],
                 'unallocated_transaction_ids': []}
        malformed = {'role': 'assistant', 'content': '报告<reconciliation_result>{</reconciliation_result>'}
        result = run_fixture(ScriptedBackend([tool_message(('validate_reconciliation', {'plan': valid})),
                                              malformed, FINAL, FINAL]))
        self.assertEqual(result['stop_reason'], 'submission_rejected')
        self.assertEqual(result['final_text'], '')
        self.assertIsNone(result['validated_submission'])
        self.assertEqual(extract_submission(result)[2], 'INVALID_SUBMISSION_JSON')

    def test_real_backend_requires_submission_and_respects_decision_budget(self):
        backend = ScriptedBackend([FINAL])
        backend.kind = 'local_transformers'
        result = run_fixture(backend, Budget(max_decisions=1))
        self.assertEqual(result['stop_reason'], 'decision_budget')
        self.assertEqual(result['final_text'], '')
        self.assertEqual(extract_submission(result)[2], 'MISSING_STRUCTURED_SUBMISSION')

    def test_unsupported_invalid_json_and_arguments_visible(self):
        backend = ScriptedBackend([tool_message(('not_a_tool', {}), ('query_orders', '{'),
                                               ('query_refunds', {}), ('query_orders', [])), FINAL])
        result = run_fixture(backend)
        errors = [e['result']['error']['code'] for e in result['trace'] if e['event'] == 'tool_result']
        self.assertEqual(errors, ['UNKNOWN_TOOL', 'INVALID_JSON', 'INVALID_ARGUMENT', 'INVALID_ARGUMENT'])
        self.assertTrue(paired(result['messages']))

    def test_multi_call_budget_pairs_unexecuted_errors(self):
        result = run_fixture(ScriptedBackend([tool_message(('query_orders', {}), ('search_receipts', {}),
                                                          ('query_refunds', {'order_id': 'o1'}))]), Budget(max_tools=1))
        tools = [e for e in result['trace'] if e['event'] == 'tool_result']
        self.assertEqual(result['stop_reason'], 'tool_budget')
        self.assertEqual(result['tool_calls'], 1)
        self.assertEqual([e['executed'] for e in tools], [True, False, False])
        self.assertTrue(all(e['result']['error']['code'] == 'RUN_STOPPED' for e in tools[1:]))
        self.assertTrue(paired(result['messages']))

    def test_decision_and_total_step_limits(self):
        for budget, reason, calls in [(Budget(max_decisions=1), 'decision_budget', 1),
                                      (Budget(max_steps=1), 'step_budget', 0)]:
            with self.subTest(reason=reason):
                result = run_fixture(ScriptedBackend([tool_message(('query_orders', {}))]), budget)
                self.assertEqual(result['stop_reason'], reason)
                self.assertEqual(result['tool_calls'], calls)
                self.assertTrue(paired(result['messages']))

    def test_empty_final_and_api_error(self):
        self.assertEqual(run_fixture(ScriptedBackend([{'role': 'assistant', 'content': '  '}]))['stop_reason'], 'empty_final')
        result = run_fixture(ScriptedBackend(['HTTP_503']))
        self.assertEqual(result['stop_reason'], 'api_error:HTTP_503')
        self.assertFalse(any(e['event'] == 'tool_result' for e in result['trace']))

    def test_invalid_model_protocol_is_not_replayed(self):
        message = tool_message(('query_orders', {}), ('search_receipts', {}))
        message['tool_calls'][1]['id'] = message['tool_calls'][0]['id']
        result = run_fixture(ScriptedBackend([message]))
        self.assertEqual(result['stop_reason'], 'api_error:INVALID_TOOL_CALL_PROTOCOL')
        self.assertEqual(len(result['messages']), 2)

    def test_timeout_pairs_all_requested_calls(self):
        # 仅控制运行时模块的时钟，无sleep、不影响LangGraph内部时钟。
        clock = SimpleNamespace(monotonic=Mock(side_effect=[0, 0, 121, 121]))
        with patch('agent_runtime.time', clock):
            result = run_fixture(SmokeBackend())
        self.assertEqual(result['stop_reason'], 'timeout')
        self.assertEqual(result['tool_calls'], 0)
        self.assertTrue(paired(result['messages']))

    def test_actual_train_and_val_reset_no_environment_exposure(self):
        root = ROOT / 'datasets/prepared/agent_visible'
        for split in ('train', 'val'):
            tasks, rules = load_tasks(root, split, limit=2)
            results = run_batch(tasks, root, split, rules, SmokeBackend, Budget())
            self.assertEqual(len(results), 2)
            self.assertTrue(all(r['decisions'] == 3 and r['tool_calls'] == 2 for r in results))
            first_input = results[0]['trace'][0]['messages']
            self.assertNotIn('environment_file', json.dumps(first_input))
            self.assertNotIn('events', json.dumps(first_input))
            self.assertNotEqual(results[0]['task_id'], results[1]['task_id'])
            self.assertIsNone(summarize(results)['accuracy'])


class ConfigTests(unittest.TestCase):
    def test_missing_configuration_before_request(self):
        with patch.dict('os.environ', {}, clear=True), patch('urllib.request.OpenerDirector.open') as opener:
            with self.assertRaisesRegex(ValueError, '缺少配置.*未发送请求'):
                OpenAIBackend.from_env()
            opener.assert_not_called()

    def test_deepseek_disables_thinking_without_changing_other_providers(self):
        for url in ('https://api.deepseek.com', 'https://example.invalid/v1'):
            with self.subTest(url=url), patch('urllib.request.build_opener') as build:
                backend = OpenAIBackend('fake-secret', url, 'mock-model')
                response = Mock()
                response.__enter__ = Mock(return_value=response)
                response.__exit__ = Mock(return_value=False)
                response.read1.return_value = json.dumps({'choices': [{'message': FINAL}]}).encode()
                response.isclosed.return_value = True
                build.return_value.open.return_value = response
                backend.complete([], [], time.monotonic() + 10)
                request = build.return_value.open.call_args.args[0]
                body = json.loads(request.data)
                if 'api.deepseek.com' in url:
                    self.assertEqual(request.full_url, 'https://api.deepseek.com/chat/completions')
                    self.assertEqual(body['thinking'], {'type': 'disabled'})
                else:
                    self.assertNotIn('thinking', body)

    def test_no_unsafe_base_urls(self):
        for url in ('https://user:pass@example.invalid/v1', 'https://example.invalid/v1?key=secret',
                    'https://example.invalid/v1#secret', 'http://example.invalid/v1'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                OpenAIBackend('mock-key', url, 'mock')

    def test_profile_and_redaction(self):
        with patch.dict('os.environ', {'SFT_OPENAI_API_KEY': 'local-secret',
                        'SFT_OPENAI_BASE_URL': 'http://127.0.0.1:9999/v1', 'SFT_MODEL_NAME': 'unverified-adapter'}, clear=True):
            backend = OpenAIBackend.from_env('sft')
        self.assertEqual(backend.profile, 'sft')
        self.assertNotIn('local-secret', json.dumps(backend.sanitize({'output': ['local-secret']})))
        self.assertFalse(backend.metadata()['trained_weights_verified'])

    def test_redaction_in_dictionary_keys(self):
        backend = OpenAIBackend('fake-secret', 'https://example.invalid/v1', 'mock')
        self.assertNotIn('fake-secret', json.dumps(backend.sanitize({'usage': {'fake-secret': 1}})))

    def test_nested_response_is_normalized_without_graph(self):
        from agent_runtime import ModelError
        backend = OpenAIBackend('fake-secret', 'https://example.invalid/v1', 'mock')
        response = Mock()
        response.fp.raw._sock = Mock()
        response.read1.return_value = b'[' * 2000 + b'0' + b']' * 2000
        response.isclosed.return_value = True
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        with patch('urllib.request.build_opener') as build:
            build.return_value.open.return_value = response
            with self.assertRaisesRegex(ModelError, 'INVALID_MODEL_RESPONSE'):
                backend.complete([], [], time.monotonic() + 10)

    def test_deadline_checked_between_response_chunks(self):
        from agent_runtime import ModelError
        backend = OpenAIBackend('fake-secret', 'https://example.invalid/v1', 'mock')
        response = Mock()
        response.fp.raw._sock = Mock()
        response.read1.return_value = b'partial'
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        clock = SimpleNamespace(monotonic=Mock(side_effect=[0, 0, 2]))
        with patch('urllib.request.build_opener') as build, patch('model_backends.time', clock):
            build.return_value.open.return_value = response
            with self.assertRaisesRegex(ModelError, 'DEADLINE_EXCEEDED'):
                backend.complete([], [], 1)
        response.fp.raw._sock.settimeout.assert_called_once_with(1)

    def test_no_test_split_or_symlink(self):
        with self.assertRaises(ValueError):
            load_tasks(ROOT / 'datasets/prepared/agent_visible', 'test')
        with tempfile.TemporaryDirectory() as directory:
            link = Path(directory) / 'agent_visible'
            link.symlink_to(ROOT / 'datasets/prepared/agent_visible', target_is_directory=True)
            with self.assertRaises(ValueError):
                load_tasks(link, 'train')


@unittest.skipUnless(HAS_GRAPH, '项目.venv安装LangGraph后执行HTTP图测试')
class HTTPTests(unittest.TestCase):
    def serve(self, replies):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                requests.append({'path': self.path, 'body': json.loads(self.rfile.read(int(self.headers['Content-Length'])))})
                status, response = replies[min(len(requests) - 1, len(replies) - 1)]
                body = json.dumps(response).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.01}, daemon=True)
        worker.start()
        self.addCleanup(server.server_close)
        self.addCleanup(worker.join, 2)
        self.addCleanup(server.shutdown)
        return OpenAIBackend('local-mock-secret', f'http://127.0.0.1:{server.server_port}/v1', 'local-mock'), requests

    def test_http_graph_and_usage(self):
        backend, requests = self.serve([
            (200, {'choices': [{'message': tool_message(('query_orders', {}))}],
                   'usage': {'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12}}),
            (200, {'choices': [{'message': FINAL}], 'usage': {'prompt_tokens': 20, 'completion_tokens': 3, 'total_tokens': 23}}),
        ])
        # HTTP协议路径是真实适配器，响应由本机mock产生，必须显式改标日志来源。
        backend.kind = 'http_mock'
        result = run_fixture(backend)
        self.assertEqual(result['stop_reason'], 'completed')
        self.assertEqual(result['kind'], 'http_mock')
        self.assertFalse(result['model_connected'])
        self.assertEqual(result['token_usage']['total_tokens'], 35)
        self.assertEqual(requests[0]['path'], '/v1/chat/completions')
        self.assertEqual(len(requests[0]['body']['tools']), 8)
        self.assertEqual(requests[0]['body']['temperature'], 0)
        self.assertTrue(paired(requests[1]['body']['messages']))
        self.assertNotIn('local-mock-secret', json.dumps(result))

    def test_http_retry_and_nonretryable_error(self):
        for status, expected_calls in ((503, 2), (401, 1)):
            with self.subTest(status=status):
                backend, requests = self.serve([(status, {'error': 'local-mock-secret; never log response'})])
                backend.kind = 'http_mock'
                result = run_fixture(backend)
                self.assertEqual(len(requests), expected_calls)
                self.assertEqual(result['stop_reason'], 'api_error:HTTP_' + str(status))
                self.assertNotIn('never log response', json.dumps(result))

    def test_transport_timeout(self):
        backend = OpenAIBackend('local-mock-secret', 'http://127.0.0.1:9999/v1', 'mock')
        backend.kind = 'http_mock'
        with patch('urllib.request.OpenerDirector.open', side_effect=TimeoutError), patch('urllib.request.build_opener') as build:
            build.return_value.open.side_effect = TimeoutError
            result = run_fixture(backend)
            self.assertEqual(build.return_value.open.call_count, 2)
        self.assertEqual(result['stop_reason'], 'api_error:TRANSPORT_ERROR')


if __name__ == '__main__':
    unittest.main()
