"""固定金额边界和错误输入测试，不依赖 Olist 下载或生成器的答案。"""
import copy
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_data import reconcile, validate_allocations
from prepare_data import SCENARIOS, cents, make_task
from reference import build_reference

T = '2020-01-10T12:00:00-03:00'


def order(oid='o1', amount=1000):
    return {'order_id': oid, 'expected_cents': amount, 'merchant_reference': 'm' + oid, 'created_at': '2020-01-01T00:00:00-03:00'}


def event(tx='p1', amount=1000, **kwargs):
    result = {'event_id': 'e' + tx, 'transaction_id': tx, 'kind': 'receipt', 'amount_cents': amount,
              'currency': 'BRL', 'status': 'success', 'effective_at': T, 'observed_at': T,
              'order_id': 'o1', 'merchant_reference': 'mo1', 'original_transaction_id': None}
    result.update(kwargs)
    return result


class ReconciliationTests(unittest.TestCase):
    def run_case(self, events, orders=None, query=None):
        return reconcile({'orders': orders or [order()], 'events': events},
                         query or {'mode': 'single_order', 'order_id': 'o1', 'cutoff': T})

    def test_normal_exact_cents(self):
        result = self.run_case([event()])
        self.assertEqual(result['totals']['net_cents'], 1000)
        self.assertEqual(result['orders'][0]['status'], 'balanced')
        self.assertEqual(cents('12.34'), 1234)
        with self.assertRaises(ValueError):
            cents('0.001')

    def test_split_receipts(self):
        result = self.run_case([event('a', 333), event('b', 667)])
        self.assertEqual(result['totals']['received_cents'], 1000)

    def test_partial_success_refund(self):
        refund = event('r', 300, kind='refund', order_id=None, merchant_reference=None, original_transaction_id='p1')
        result = self.run_case([event(), refund])
        self.assertEqual(result['totals']['net_cents'], 700)
        self.assertEqual(result['totals']['collection_gap_cents'], 0)
        self.assertEqual(result['orders'][0]['status'], 'balanced')

    def test_pending_refund_not_deducted(self):
        refund = event('r', 300, kind='refund', status='pending', order_id=None, merchant_reference=None, original_transaction_id='p1')
        result = self.run_case([event(), refund])
        self.assertEqual(result['totals']['net_cents'], 1000)
        self.assertEqual(result['totals']['refunded_cents'], 0)
        self.assertEqual(result['totals']['pending_refund_cents'], 300)
        self.assertEqual(result['orders'][0]['pending_refund_ids'], ['r'])

    def test_duplicates_count_once(self):
        result = self.run_case([event(), event(event_id='replay')])
        self.assertEqual(result['totals']['received_cents'], 1000)
        self.assertEqual(len(result['duplicate_event_ids']), 1)

    def test_recover_missing_reference(self):
        result = self.run_case([event(order_id=None)])
        self.assertEqual(result['totals']['received_cents'], 1000)

    def test_equal_amount_ambiguity_suspends(self):
        result = self.run_case([event(order_id=None, merchant_reference=None)], [order(), order('o2')])
        self.assertTrue(result['orders'][0]['review'])
        self.assertEqual(result['totals']['received_cents'], 0)
        self.assertEqual(result['unallocated_transaction_ids'], ['p1'])

    def test_amount_alone_even_unique_not_strong(self):
        result = self.run_case([event(order_id=None, merchant_reference=None)])
        self.assertEqual(result['unallocated_transaction_ids'], ['p1'])

    def test_cutoff_inclusive_and_one_second_later(self):
        after = (datetime.fromisoformat(T) + timedelta(seconds=1)).isoformat()
        result = self.run_case([event('a', 400), event('b', 600, effective_at=after, observed_at=after)])
        self.assertEqual(result['totals']['received_cents'], 400)
        self.assertEqual(result['excluded_after_cutoff_event_ids'], ['eb'])

    def test_observed_after_cutoff(self):
        after = (datetime.fromisoformat(T) + timedelta(seconds=1)).isoformat()
        result = self.run_case([event(observed_at=after)])
        self.assertEqual(result['totals']['received_cents'], 0)

    def test_refund_cutoff(self):
        after = (datetime.fromisoformat(T) + timedelta(seconds=1)).isoformat()
        refunds = [event('r1', 200, kind='refund', order_id=None, merchant_reference=None, original_transaction_id='p1'),
                   event('r2', 300, kind='refund', order_id=None, merchant_reference=None, original_transaction_id='p1', effective_at=after, observed_at=after)]
        self.assertEqual(self.run_case([event()] + refunds)['totals']['net_cents'], 800)

    def test_allocation_reuse_rejected(self):
        with self.assertRaisesRegex(ValueError, '重复分配'):
            validate_allocations([{'transaction_id': 'p1', 'order_id': 'o1'}, {'transaction_id': 'p1', 'order_id': 'o2'}])

    def test_batch_totals_and_period_exclusion(self):
        orders = [order(), order('o2', 2000), dict(order('outside'), created_at='2020-02-01T00:00:00-03:00')]
        query = {'mode': 'period_batch', 'period_start': '2020-01-01T00:00:00-03:00', 'period_end': '2020-02-01T00:00:00-03:00', 'cutoff': T}
        result = self.run_case([event(), event('p2', 2000, order_id='o2', merchant_reference='mo2')], orders, query)
        self.assertEqual(len(result['orders']), 2)
        self.assertEqual(result['totals']['expected_cents'], 3000)
        self.assertEqual(result['totals']['net_cents'], 3000)

    def test_over_refund_rejected(self):
        with self.assertRaisesRegex(ValueError, '超过'):
            self.run_case([event(), event('r', 1001, kind='refund', order_id=None, merchant_reference=None, original_transaction_id='p1')])

    def test_conflicting_notification_rejected(self):
        with self.assertRaisesRegex(ValueError, '冲突通知'):
            self.run_case([event(), event(event_id='replay', amount=900)])

    def test_reference_conflict_rejected(self):
        with self.assertRaisesRegex(ValueError, '引用冲突'):
            self.run_case([event(merchant_reference='wrong')])

    def test_empty_results(self):
        result = self.run_case([])
        self.assertEqual(result['totals']['received_cents'], 0)
        self.assertEqual(result['orders'][0]['status'], 'shortfall')

    def test_unknown_order_rejected(self):
        with self.assertRaisesRegex(ValueError, '不存在'):
            self.run_case([], query={'mode': 'single_order', 'order_id': 'missing', 'cutoff': T})

    def test_invalid_money_rejected(self):
        for amount in (1.5, True, -100):
            with self.assertRaisesRegex(ValueError, '金额'):
                self.run_case([event(amount=amount)])

    def test_currency_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, '币种'):
            self.run_case([event(currency='CNY')])

    def test_orphan_refund_rejected(self):
        with self.assertRaisesRegex(ValueError, '缺少'):
            self.run_case([event('r', 300, kind='refund', original_transaction_id='missing')])

    def test_multiple_refunds_and_cumulative_limit(self):
        refunds = [event('r1', 300, kind='refund', order_id=None, merchant_reference=None, original_transaction_id='p1'),
                   event('r2', 200, kind='refund', order_id=None, merchant_reference=None, original_transaction_id='p1')]
        result = self.run_case([event()] + refunds)
        self.assertEqual(result['totals']['net_cents'], 500)
        self.assertEqual(result['orders'][0]['refund_ids'], ['r1', 'r2'])
        refunds[1]['amount_cents'] = 701
        with self.assertRaisesRegex(ValueError, '超过'):
            self.run_case([event()] + refunds)

    def test_refund_before_receipt_rejected(self):
        before = (datetime.fromisoformat(T) - timedelta(seconds=1)).isoformat()
        with self.assertRaisesRegex(ValueError, '早于'):
            self.run_case([event(), event('r', 100, kind='refund', order_id=None,
                          merchant_reference=None, original_transaction_id='p1', effective_at=before)])

    def test_refund_observed_after_cutoff_not_deducted(self):
        after = (datetime.fromisoformat(T) + timedelta(seconds=1)).isoformat()
        result = self.run_case([event(), event('r', 300, kind='refund', order_id=None,
                               merchant_reference=None, original_transaction_id='p1', observed_at=after)])
        self.assertEqual(result['totals']['net_cents'], 1000)
        self.assertEqual(result['excluded_after_cutoff_event_ids'], ['er'])

    def test_refund_merchant_conflict_rejected(self):
        with self.assertRaisesRegex(ValueError, '退款归属冲突'):
            self.run_case([event(), event('r', 100, kind='refund', order_id=None,
                          merchant_reference='wrong', original_transaction_id='p1')])

    def test_pending_receipt_not_collected(self):
        self.assertEqual(self.run_case([event(status='pending')])['totals']['received_cents'], 0)

    def test_invalid_order_amount_and_currency(self):
        for amount in (True, 1.5, -100, 0):
            with self.assertRaisesRegex(ValueError, '订单金额'):
                self.run_case([], [order(amount=amount)])
        with self.assertRaisesRegex(ValueError, '订单币种'):
            self.run_case([], [dict(order(), currency='CNY')])

    def test_events_input_not_mutated(self):
        events = [event(), event(event_id='replay')]
        before = copy.deepcopy(events)
        self.run_case(events)
        self.assertEqual(events, before)


class GeneratorTests(unittest.TestCase):
    def sources(self):
        return [{'source_order': {'order_id': f'private_source_{i}', 'order_purchase_timestamp': '2017-01-01 12:00:00'},
                 'source_customer_unique_id': f'private_customer_{i}', 'source_items': [],
                 'source_payments': [{'payment_type': 'credit_card', 'payment_installments': '12'}],
                 'amount_cents': 1000 + 777 * i} for i in range(3)]

    def test_every_scenario_and_request_mode(self):
        for scenarios in SCENARIOS.values():
            for scenario in scenarios:
                for mode in ('single_order', 'period_batch'):
                    with self.subTest(scenario=scenario, mode=mode):
                        task, env, facts = make_task(self.sources(), scenario, mode, random.Random(34))
                        self.assertEqual(reconcile(env, task['query']), build_reference(facts))
                        visible = json.dumps({'task': task, 'env': env})
                        for forbidden in ('private_source_', 'private_customer_', 'scenario', 'latent_owner', 'modified', 'ground_truth'):
                            self.assertNotIn(forbidden, visible)

    def test_generated_refund_boundaries_have_expected_amounts(self):
        for scenario, refunded, excluded in (('multiple_refunds', 583, 0),
                                               ('refund_cutoff', 333, 1),
                                               ('refund_observed_cutoff', 0, 1)):
            with self.subTest(scenario=scenario):
                task, env, facts = make_task(self.sources()[:1], scenario, 'single_order', random.Random(7))
                result = reconcile(env, task['query'])
                self.assertEqual(result['totals']['received_cents'], 1000)
                self.assertEqual(result['totals']['refunded_cents'], refunded)
                self.assertEqual(len(result['excluded_after_cutoff_event_ids']), excluded)

    def test_repeatable_generation(self):
        first = make_task(self.sources(), 'split_receipts', 'period_batch', random.Random(7))
        second = make_task(self.sources(), 'split_receipts', 'period_batch', random.Random(7))
        self.assertEqual(first, second)

    def test_installments_do_not_create_receipts(self):
        task, env, facts = make_task(self.sources()[:1], 'normal', 'single_order', random.Random(6))
        self.assertEqual(len(env['events']), 1)
        self.assertEqual(env['orders'][0]['source_payment_attributes'][0]['payment_installments'], 12)


if __name__ == '__main__':
    unittest.main()
