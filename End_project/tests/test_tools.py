"""业务工具独立测试，固定可见记录，不读取hidden或test任务。"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from business_tools import ToolSession, BusinessError, TOOL_NAMES, tool_schemas, register_tools
from tool_demo import run_demo

T = '2020-01-10T12:00:00-03:00'
LATE = '2020-01-10T12:00:01-03:00'
ROOT = Path(__file__).resolve().parents[1]


def order(oid='o1'):
    return {'order_id': oid, 'expected_cents': 1000, 'currency': 'BRL', 'merchant_reference': 'm' + oid,
            'created_at': '2020-01-01T00:00:00-03:00'}


def event(tx='p1', **changes):
    e = {'event_id': 'e' + tx, 'transaction_id': tx, 'amount_cents': 1000, 'currency': 'BRL',
         'kind': 'receipt', 'status': 'success', 'order_id': 'o1', 'merchant_reference': 'mo1',
         'original_transaction_id': None, 'effective_at': T, 'observed_at': T}
    e.update(changes)
    return e


def session(events=None, orders=None):
    return ToolSession({'orders': orders or [order()], 'events': [event()] if events is None else events},
                       {'mode': 'single_order', 'order_id': 'o1', 'cutoff': T})


class ToolsTests(unittest.TestCase):
    def call(self, name, **args):
        return self.s.call(name, args)

    def setUp(self):
        self.s = session()

    def test_all_eight_normal_and_error_or_empty(self):
        demo = run_demo(self.s)
        self.assertTrue(demo['validation']['valid'])
        normal = {c['tool'] for c in demo['calls']}
        self.assertEqual(normal, set(TOOL_NAMES))
        cases = [('query_orders', {'order_id': 'absent'}), ('search_receipts', {'transaction_id': 'absent'}),
                 ('find_match_candidates', {'transaction_id': 'absent'}), ('get_transaction_evidence', {'transaction_id': 'absent'}),
                 ('check_duplicate_events', {'transaction_ids': ['absent']}), ('query_refunds', {'order_id': 'o1'}),
                 ('calculate_reconciliation', {'order_id': 'absent', 'receipt_ids': [], 'refund_ids': []}),
                 ('validate_reconciliation', {'plan': {}})]
        for name, args in cases:
            with self.subTest(name=name):
                result = self.s.call(name, args)
                self.assertEqual(set(result), {'ok', 'data', 'error'})
                if name in ('query_orders', 'search_receipts', 'query_refunds'):
                    self.assertEqual(next(iter(result['data'].values())), [])
                elif name == 'check_duplicate_events':
                    self.assertEqual(result['data']['groups'][0]['status'], 'empty')
                else:
                    self.assertFalse(result['ok'])

    def test_duplicate_and_same_amount_distinct(self):
        self.s = session([event(), event(event_id='replay'), event('other')])
        data = self.call('check_duplicate_events', transaction_ids=['p1', 'other'])['data']['groups']
        self.assertEqual(data[0]['duplicate_event_ids'], ['replay'])
        self.assertEqual(data[1]['duplicate_event_ids'], [])
        self.assertEqual(self.calc(['p1', 'other'])['data']['received_cents'], 2000)

    def calc(self, receipts=None, refunds=None):
        return self.call('calculate_reconciliation', order_id='o1', receipt_ids=receipts or ['p1'], refund_ids=refunds or [])

    def test_conflict(self):
        self.s = session([event(), event(event_id='bad', amount_cents=900)])
        self.assertEqual(self.call('check_duplicate_events', transaction_ids=['p1'])['data']['groups'][0]['status'], 'conflict')
        self.assertFalse(self.calc()['ok'])
        evidence = self.call('get_transaction_evidence', transaction_id='p1')
        self.assertTrue(evidence['ok'])
        self.assertIsNone(evidence['data']['transaction'])
        self.assertEqual(len(evidence['data']['events']), 2)
        self.assertEqual(evidence['data']['conflicting_fields'], ['amount_cents'])
        self.s = session([event(), event('p2', order_id='o2', merchant_reference='mo2'),
                          event('p2', event_id='conflict', amount_cents=900, order_id='o2', merchant_reference='mo2')],
                         [order(), order('o2')])
        self.assertTrue(self.call('query_refunds', order_id='o1')['ok'])

    def test_pending_and_success_refunds(self):
        self.s = session([event(), event('r', kind='refund', amount_cents=300, order_id=None,
                          merchant_reference=None, original_transaction_id='p1'),
                          event('pending', kind='refund', amount_cents=200, status='pending', order_id=None,
                          merchant_reference=None, original_transaction_id='p1')])
        result = self.calc(refunds=['r', 'pending'])['data']
        self.assertEqual((result['net_cents'], result['collection_gap_cents'], result['pending_refund_cents']), (700, 0, 200))
        self.assertEqual(len(self.call('query_refunds', original_transaction_id='p1')['data']['events']), 2)

    def test_refund_cutoff_effective_and_observed(self):
        for field in ('effective_at', 'observed_at'):
            self.s = session([event(), event('r', kind='refund', amount_cents=100, original_transaction_id='p1', **{field: LATE})])
            self.assertEqual(self.call('query_refunds', original_transaction_id='p1')['data']['events'], [])
            self.assertFalse(self.calc(refunds=['r'])['ok'])

    def test_receipt_cutoff(self):
        self.s = session([event(observed_at=LATE)])
        self.assertFalse(self.calc()['ok'])
        self.assertEqual(self.call('search_receipts')['data']['events'], [])

    def test_refund_cumulative_limit(self):
        self.s = session([event()] + [event(tx, kind='refund', amount_cents=600, original_transaction_id='p1', order_id=None, merchant_reference=None) for tx in ('r1', 'r2')])
        self.assertEqual(self.calc(refunds=['r1', 'r2'])['error']['code'], 'OVER_REFUND')

    def test_orphan_and_refund_time_conflict(self):
        for changes in ({'original_transaction_id': 'missing'}, {'effective_at': '2020-01-09T12:00:00-03:00'}, {'merchant_reference': 'wrong'}):
            e = event('r', kind='refund', amount_cents=100, original_transaction_id='p1', order_id=None, merchant_reference=None)
            e.update(changes)
            self.s = session([event(), e])
            self.assertFalse(self.calc(refunds=['r'])['ok'])

    def test_missing_fields_and_weak_amount(self):
        self.s = session([event(order_id=None, merchant_reference=None)])
        evidence = self.call('get_transaction_evidence', transaction_id='p1')['data']
        self.assertEqual(evidence['missing_fields'], ['order_id', 'merchant_reference'])
        self.assertFalse(self.call('find_match_candidates', transaction_id='p1')['data']['candidates'][0]['strong'])
        self.assertFalse(self.calc()['ok'])
        demo = run_demo(self.s)
        self.assertTrue(demo['validation']['valid'])
        self.assertTrue(demo['plan']['orders'][0]['review'])

    def test_merchant_recovery_and_exact_search(self):
        self.s = session([event(order_id=None)])
        self.assertTrue(self.calc()['ok'])
        self.assertEqual(len(self.call('search_receipts', merchant_reference='mo1', unassigned_only=True)['data']['events']), 1)
        self.assertEqual(self.call('search_receipts', merchant_reference='mo')['data']['events'], [])

    def test_reference_conflict(self):
        self.s = session([event(merchant_reference='wrong')])
        self.assertFalse(self.calc()['ok'])
        self.assertTrue(self.call('find_match_candidates', transaction_id='p1')['data']['conflicts'])

    def test_plan_double_use_omission_amount_review(self):
        plan = run_demo(self.s)['plan']
        for mutate, code in (
            (lambda p: p['orders'].append({**copy.deepcopy(p['orders'][0]), 'order_id': 'o2'}), 'DUPLICATE_ALLOCATION'),
            (lambda p: p['orders'][0]['balance'].update(received_cents=1000.0), 'BALANCE_MISMATCH'),
            (lambda p: p['orders'].append(copy.deepcopy(p['orders'][0])), 'DUPLICATE_ALLOCATION'),
            (lambda p: p['orders'].clear(), 'ORDER_COVERAGE'),
            (lambda p: p['orders'][0]['balance'].update(net_cents=1), 'BALANCE_MISMATCH'),
            (lambda p: p['orders'][0].update(review=True), 'REVIEW_DETAILS'),
            (lambda p: p['orders'][0].update(review=True, review_reason='missing reference', missing_fields=['order_id']), 'UNJUSTIFIED_REVIEW'),
            (lambda p: p['orders'][0].update(receipt_ids=[]), 'TRANSACTION_OMITTED')):
            p = copy.deepcopy(plan)
            mutate(p)
            errors = self.call('validate_reconciliation', plan=p)['data']['errors']
            self.assertIn(code, [e['code'] for e in errors])

    def test_parameter_validation(self):
        for name, args in [('query_orders', {'typo': 1}), ('search_receipts', {'status': 'bad'}),
                           ('check_duplicate_events', {'transaction_ids': 'p1'}),
                           ('calculate_reconciliation', {'order_id': 'o1', 'receipt_ids': ['p1', 'p1'], 'refund_ids': []}),
                           ('query_refunds', {}), ('query_orders', {'period_start': T, 'period_end': T})]:
            self.assertFalse(self.s.call(name, args)['ok'])

    def test_schema_registry_serialization(self):
        self.assertEqual(len(tool_schemas()), 8)
        json.dumps(tool_schemas())
        validator = next(s['function'] for s in tool_schemas() if s['function']['name'] == 'validate_reconciliation')
        balance_schema = validator['parameters']['properties']['plan']['properties']['orders']['items']['properties']['balance']
        actual = self.s.call('calculate_reconciliation', {'order_id': 'o1', 'receipt_ids': ['p1'], 'refund_ids': []})
        self.assertTrue(actual['ok'])
        self.assertEqual(set(balance_schema['required']), set(actual['data']))
        self.assertIn('evidence_event_ids', balance_schema['required'])
        self.assertTrue(register_tools(self.s)['query_orders']()['ok'])

    def test_snapshot_and_session_isolation(self):
        env = {'orders': [order()], 'events': [event()]}
        s = ToolSession(env, {'mode': 'single_order', 'order_id': 'o1', 'cutoff': T})
        env['events'].clear()
        a = run_demo(s)
        a['plan']['orders'].clear()
        self.assertTrue(run_demo(s)['validation']['valid'])
        self.assertEqual(run_demo(session([]))['plan']['orders'][0]['balance']['received_cents'], 0)

    def test_path_escape_symlink_and_forbidden_split(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'agent_visible'
            (root / 'train' / 'environments').mkdir(parents=True)
            outside = Path(d) / 'private.json'
            outside.write_text('{}')
            (root / 'train' / 'environments' / 'link.json').symlink_to(outside)
            for split, name in [('test', 'environments/x.json'), ('train', '../../hidden/x.json'),
                                ('train', str(outside)), ('train', 'environments/link.json'), ('raw', 'environments/x.json')]:
                with self.assertRaises(BusinessError):
                    ToolSession.from_visible(root, split, name, {})

    def test_actual_train_three_order_flow(self):
        path = ROOT / 'datasets/prepared/agent_visible/train/tasks.jsonl'
        task = json.loads(path.read_text().splitlines()[1])
        s = ToolSession.from_visible(path.parent.parent, 'train', task['environment_file'], task['query'])
        demo = run_demo(s)
        self.assertEqual(len(demo['plan']['orders']), 3)
        self.assertTrue(demo['validation']['valid'])


if __name__ == '__main__':
    unittest.main()
