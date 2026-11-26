"""Independent grading and cost regressions; no model calls or held-out tasks."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluation import (evaluate_results, extract_submission, measure_cost, score_plan,
                        summarize_evaluations, tool_metrics, validate_pricing)


def reference():
    return {'rule_version': 'brl-reconciliation-v1', 'unallocated_transaction_ids': [], 'orders': [{
        'order_id': 'o1', 'expected_cents': 1000, 'received_cents': 1000, 'refunded_cents': 200,
        'pending_refund_cents': 50, 'net_cents': 800, 'collection_gap_cents': 0,
        'net_vs_original_cents': 200, 'receipt_ids': ['p1', 'p2'], 'refund_ids': ['r1'],
        'pending_refund_ids': ['r2'], 'review': False}]}


def plan():
    row = copy.deepcopy(reference()['orders'][0])
    return {'orders': [{'order_id': 'o1', 'receipt_ids': ['p2', 'p1'], 'refund_ids': ['r1'],
                        'review': False, 'review_reason': '', 'missing_fields': [], 'balance': row}],
            'unallocated_transaction_ids': []}


def validation_call(value):
    return {'event': 'tool_result', 'executed': True, 'tool': 'validate_reconciliation',
            'arguments': json.dumps({'plan': value}), 'result': {'ok': True, 'data': {'valid': True}}}


def actual_task_result():
    # A saved-output fixture using one train task, without running a model.
    task = json.loads((ROOT / 'datasets/prepared/agent_visible/train/tasks.jsonl').read_text(encoding='utf-8').splitlines()[0])
    gold = json.loads((ROOT / 'datasets/prepared/hidden/train/ground_truth.jsonl').read_text(encoding='utf-8').splitlines()[0])
    submission = {'orders': gold['reference']['orders'], 'unallocated_transaction_ids': []}
    return {'task_id': task['task_id'], 'kind': 'local_transformers', 'model_connected': True,
            'stop_reason': 'completed', 'decisions': 1, 'tool_calls': 0, 'elapsed_seconds': 10,
            'token_usage': {'prompt_tokens': 100, 'completion_tokens': 20, 'total_tokens': 120},
            'token_usage_complete': True, 'trace': [], 'messages': [],
            'input': {'scope': task['query'], 'rules': {'version': 'brl-reconciliation-v1'}},
            'final_text': '<reconciliation_result>' + json.dumps(submission) + '</reconciliation_result>'}


class PlanTests(unittest.TestCase):
    def test_correct_nested_plan_ignores_id_order(self):
        score = score_plan(plan(), reference())
        self.assertTrue(score['plan_exact_match'])
        self.assertEqual(score['field_accuracy'], 1)

    def test_money_pending_and_review_are_independently_checked(self):
        for field, wrong in [('net_cents', 1000), ('pending_refund_cents', 0), ('review', True),
                             ('collection_gap_cents', False), ('refund_ids', ['wrong']),
                             ('receipt_ids', ['p1', 'p1', 'p2'])]:
            with self.subTest(field=field):
                candidate = plan()
                candidate['orders'][0]['balance'][field] = wrong
                score = score_plan(candidate, reference())
                self.assertFalse(score['plan_exact_match'])
                self.assertIn(field, [d['field'] for d in score['orders'][0]['mismatches']])

    def test_missing_and_extra_orders_and_unallocated_cannot_pass(self):
        variants = [None, {'orders': [], 'unallocated_transaction_ids': []}]
        extra = plan()
        extra['orders'].append({'order_id': 'extra'})
        variants.append(extra)
        duplicate = plan()
        duplicate['orders'] *= 2
        variants.append(duplicate)
        missing = plan()
        del missing['orders'][0]['balance']['pending_refund_ids']
        variants.append(missing)
        unallocated = plan()
        unallocated['unallocated_transaction_ids'] = ['extra_payment']
        variants.append(unallocated)
        for candidate in variants:
            with self.subTest(candidate=candidate):
                self.assertFalse(score_plan(candidate, reference())['plan_exact_match'])

    def test_tool_observations_are_not_synthesized_into_an_answer(self):
        row = {'final_text': '所有金额正确。', 'trace': [
            {'event': 'tool_result', 'tool': 'calculate_reconciliation', 'executed': True,
             'result': {'ok': True, 'data': reference()['orders'][0]}}]}
        self.assertEqual(extract_submission(row)[2], 'MISSING_STRUCTURED_SUBMISSION')

    def test_last_submission_wins_and_bad_final_json_cannot_fall_back(self):
        correct = plan()
        wrong = plan()
        wrong['orders'][0]['balance']['received_cents'] = 0
        row = {'trace': [validation_call(correct), validation_call(wrong)]}
        self.assertFalse(score_plan(extract_submission(row)[0], reference())['plan_exact_match'])
        row['final_text'] = '<reconciliation_result>{bad</reconciliation_result>'
        self.assertEqual(extract_submission(row)[2], 'INVALID_SUBMISSION_JSON')


class EvaluationTests(unittest.TestCase):
    visible = ROOT / 'datasets/prepared/agent_visible'

    def test_real_tool_plan_shape_matches_independent_reference(self):
        from business_tools import ToolSession
        from tool_demo import run_demo
        tasks = [json.loads(line) for line in (self.visible / 'train/tasks.jsonl').read_text(encoding='utf-8').splitlines()[:2]]
        gold = {r['task_id']: r['reference'] for r in
                map(json.loads, (ROOT / 'datasets/prepared/hidden/train/ground_truth.jsonl').read_text(encoding='utf-8').splitlines())}
        for task in tasks:
            session = ToolSession.from_visible(self.visible, 'train', task['environment_file'], task['query'])
            submitted = run_demo(session)['plan']
            self.assertTrue(score_plan(submitted, gold[task['task_id']])['plan_exact_match'])

    def test_perfect_fixture_is_scored_without_changing_model_messages(self):
        raw = actual_task_result()
        original = copy.deepcopy(raw)
        result = evaluate_results([raw], self.visible, 'train')[0]
        self.assertEqual(result['accuracy'], 1)
        self.assertEqual(raw, original)
        self.assertEqual(result['input'], original['input'])
        self.assertEqual(result['trace'], original['trace'])
        self.assertEqual(result['messages'], original['messages'])
        self.assertTrue(result['evaluation']['post_run_only'])

    def test_missing_answer_failure_and_mocks_are_not_successes(self):
        raw = actual_task_result()
        raw['final_text'] = '金额全部正确。'
        result = evaluate_results([raw], self.visible, 'train')[0]
        self.assertEqual(result['accuracy'], 0)
        self.assertIn('MISSING_STRUCTURED_SUBMISSION', result['evaluation']['failure_reasons'])
        self.assertEqual(result['evaluation']['scores']['field_accuracy'], 0)
        raw['kind'] = 'scripted_mock'
        scripted = evaluate_results([raw], self.visible, 'train')[0]
        self.assertIsNone(scripted['accuracy'])
        summary = summarize_evaluations([result, scripted])
        self.assertEqual(summary['accuracy'], 0)
        self.assertEqual(summary['evaluation']['tasks_scored'], 1)
        self.assertEqual(summary['evaluation']['tasks_excluded'], 1)

    def test_exact_plan_on_timeout_does_not_count_as_task_success(self):
        raw = actual_task_result()
        raw['stop_reason'] = 'timeout'
        result = evaluate_results([raw], self.visible, 'train')[0]
        self.assertTrue(result['evaluation']['scores']['plan_exact_match'])
        self.assertEqual(result['accuracy'], 0)

    def test_wrong_dataset_scope_rule_and_heldout_split_are_rejected(self):
        for change in ('scope', 'rule', 'id'):
            raw = actual_task_result()
            if change == 'scope':
                raw['input']['scope']['cutoff'] = 'wrong'
            elif change == 'rule':
                raw['input']['rules']['version'] = 'wrong'
            else:
                raw['task_id'] = 'not-a-task'
            with self.subTest(change=change), self.assertRaises(ValueError):
                evaluate_results([raw], self.visible, 'train')
        with patch.object(Path, 'read_bytes') as reader, self.assertRaises(ValueError):
            evaluate_results([actual_task_result()], self.visible, 'test')
        reader.assert_not_called()

    def test_offline_cli_does_not_connect_to_a_model(self):
        from agent_cli import main
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'source.json', Path(directory) / 'evaluated'
            source.write_text(json.dumps([actual_task_result()]), encoding='utf-8')
            with patch('agent_cli.OpenAIBackend.from_env') as api, patch('agent_cli.run_agent') as runner:
                self.assertEqual(main(['--evaluate-trace', str(source), '--output-dir', str(output)]), 0)
                api.assert_not_called()
                runner.assert_not_called()
            summary = json.loads((output / 'summary.json').read_text(encoding='utf-8'))
            self.assertEqual(summary['accuracy'], 1)
            self.assertTrue((output / 'evaluation.md').is_file())


class CostTests(unittest.TestCase):
    def test_local_fee_and_explicit_compute_estimate_are_distinct(self):
        raw = actual_task_result()
        cost = measure_cost(raw)
        self.assertEqual(cost['api_fee'], 0)
        self.assertIsNone(cost['compute_fee_estimate'])
        self.assertEqual(cost['reported_output_tokens_per_second'], 2)
        self.assertEqual(measure_cost(raw, {'compute_price_per_hour': 3.6})['compute_fee_estimate'], .01)

    def test_api_rates_are_required_and_partial_usage_remains_labeled(self):
        raw = actual_task_result()
        raw['kind'] = 'real_api'
        self.assertEqual(measure_cost(raw)['api_fee_status'], 'missing_pricing')
        pricing = {'input_price_per_million': 2, 'output_price_per_million': 8}
        self.assertEqual(measure_cost(raw, pricing)['api_fee'], .00036)
        raw['token_usage_complete'] = False
        self.assertEqual(measure_cost(raw, pricing)['api_fee_status'], 'partial_usage_estimate')

    def test_invalid_rates_are_rejected(self):
        for pricing in ({'compute_price_per_hour': -1}, {'compute_price_per_hour': float('nan')},
                        {'input_price_per_million': 1}, {'cost_currency': '???'}):
            with self.subTest(pricing=pricing), self.assertRaises(ValueError):
                validate_pricing(pricing)

    def test_failed_validation_is_not_hidden_by_an_earlier_success(self):
        good = validation_call(plan())
        bad = copy.deepcopy(good)
        bad['result'] = {'ok': False, 'error': {'code': 'INVALID_ARGUMENT'}}
        metrics = tool_metrics({'trace': [good, bad]})
        self.assertFalse(metrics['validation_passed'])
        self.assertEqual(metrics['validation_calls'], 2)
        self.assertEqual(metrics['tool_success_rate'], .5)


if __name__ == '__main__':
    unittest.main()
