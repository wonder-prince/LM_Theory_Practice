"""Trusted post-run scoring. Hidden train/val references never enter model messages."""
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import re

REAL_KINDS = {'real_api', 'local_transformers'}
MONEY_FIELDS = ('expected_cents', 'received_cents', 'refunded_cents', 'pending_refund_cents',
                'net_cents', 'collection_gap_cents', 'net_vs_original_cents')
ID_FIELDS = ('receipt_ids', 'refund_ids', 'pending_refund_ids')
FIELDS = MONEY_FIELDS + ID_FIELDS + ('review',)
DEFINITION = ('结构化对账方案整题精确匹配率：订单覆盖、7项金额、收款/退款/待退款交易归属、'
              '复核标记和未分配交易全部正确，且正常返回最终文本；缺失提交计失败。'
              '不自动评分中文叙述、证据引用、复核理由及缺失字段说明。')


def add_evaluation_arguments(parser):
    parser.add_argument('--input-price-per-million', type=float, help='API每百万输入token单价；需同时给出输出单价')
    parser.add_argument('--output-price-per-million', type=float, help='API每百万输出token单价')
    parser.add_argument('--compute-price-per-hour', type=float, help='可选本地算力每小时估价；不是实测电费')
    parser.add_argument('--cost-currency', default='USD', help='用户提供单价的币种，默认USD')


def pricing_from_args(args):
    pricing = {key: getattr(args, key) for key in (
        'input_price_per_million', 'output_price_per_million', 'compute_price_per_hour', 'cost_currency')}
    validate_pricing(pricing)
    return pricing


def validate_pricing(pricing):
    for key in ('input_price_per_million', 'output_price_per_million', 'compute_price_per_hour'):
        value = pricing.get(key)
        if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
            raise ValueError('费用单价必须是有限的非负数')
    if (pricing.get('input_price_per_million') is None) != (pricing.get('output_price_per_million') is None):
        raise ValueError('API输入和输出单价必须同时提供')
    if not re.fullmatch('[A-Z]{3}', pricing.get('cost_currency', 'USD')):
        raise ValueError('cost-currency使用3位大写币种代码')


def measure_cost(result, pricing=None):
    pricing = pricing or {}
    validate_pricing(pricing)
    kind = result.get('kind')
    elapsed = result.get('elapsed_seconds', 0)
    usage = result.get('token_usage') or {}
    complete = result.get('token_usage_complete') is True
    cost = {'mode': kind, 'currency': pricing.get('cost_currency', 'USD'),
            'elapsed_seconds': elapsed, 'reported_token_usage': usage,
            'token_usage_complete': complete,
            'reported_output_tokens_per_second': round(usage.get('completion_tokens', 0) / elapsed, 4)
            if elapsed > 0 and type(usage.get('completion_tokens')) is int else None,
            'api_fee': None, 'compute_fee_estimate': None,
            'compute_fee_status': 'not_configured',
            'scope': 'elapsed含预填充、生成、工具执行与图调度，不含模型加载和评分；速度为端到端输出吞吐。'
                     '本地API费用为0不代表硬件和电费为0；未测量实际电费。'}
    if kind == 'local_transformers':
        cost.update(api_fee=0.0, api_fee_status='local_no_api')
        hourly = pricing.get('compute_price_per_hour')
        if hourly is not None:
            cost.update(compute_fee_estimate=round(elapsed / 3600 * hourly, 8),
                        compute_fee_status='user_hourly_rate_estimate', compute_price_per_hour=hourly)
    elif kind == 'real_api':
        valid_usage = all(type(usage.get(k)) is int and usage[k] >= 0
                          for k in ('prompt_tokens', 'completion_tokens'))
        if pricing.get('input_price_per_million') is not None and valid_usage:
            fee = (usage['prompt_tokens'] * pricing['input_price_per_million'] +
                   usage['completion_tokens'] * pricing['output_price_per_million']) / 1_000_000
            cost.update(api_fee=round(fee, 8),
                        api_fee_status='user_rate_estimate' if complete else 'partial_usage_estimate',
                        input_price_per_million=pricing['input_price_per_million'],
                        output_price_per_million=pricing['output_price_per_million'])
        else:
            cost['api_fee_status'] = 'missing_usage' if not valid_usage else 'missing_pricing'
    else:
        cost.update(api_fee=0.0, api_fee_status='simulation_not_billable',
                    reported_output_tokens_per_second=None)
    return cost


def extract_submission(result):
    """Score model-authored allocations with runtime-computed balances when available."""
    validated = result.get('validated_submission')
    if validated is not None:
        return validated['plan'], validated['source'], None
    check = next((e for e in reversed(result.get('trace', [])) if e.get('event') == 'submission_check'), None)
    if check is not None:
        return check['plan'], check['source'], check['submission_error']
    text = result.get('final_text') or ''
    if '<reconciliation_result>' in text or '</reconciliation_result>' in text:
        blocks = re.findall(r'<reconciliation_result>\s*(.*?)\s*</reconciliation_result>', text, re.S)
        if len(blocks) != 1 or text.count('<reconciliation_result>') != 1 or text.count('</reconciliation_result>') != 1:
            return None, 'final_json', 'INVALID_SUBMISSION_JSON'
        try:
            plan = json.loads(blocks[0])
        except (ValueError, TypeError, RecursionError):
            return None, 'final_json', 'INVALID_SUBMISSION_JSON'
        return plan, 'final_json', None
    # A validate call is itself a structured answer authored by the model.
    calls = [e for e in result.get('trace', []) if e.get('event') == 'tool_result'
             and e.get('tool') == 'validate_reconciliation']
    if calls:
        try:
            args = calls[-1].get('arguments')
            args = json.loads(args) if isinstance(args, str) else args
            return args['plan'], 'last_validation_call', None
        except (ValueError, TypeError, KeyError):
            return None, 'last_validation_call', 'INVALID_SUBMISSION_JSON'
    return None, None, 'MISSING_STRUCTURED_SUBMISSION'


def _ids_match(actual, expected):
    return (isinstance(actual, list) and all(isinstance(x, str) for x in actual)
            and len(actual) == len(set(actual)) and sorted(actual) == sorted(expected))


def _field_matches(field, actual, expected):
    if field in MONEY_FIELDS:
        return type(actual) is int and actual == expected
    if field in ID_FIELDS:
        return _ids_match(actual, expected)
    return type(actual) is bool and actual == expected


def score_plan(plan, reference):
    """Independent comparison against the precomputed facts-based reference."""
    valid = isinstance(plan, dict) and isinstance(plan.get('orders'), list)
    actual_rows = plan['orders'] if valid else []
    actual_ids = [r.get('order_id') if isinstance(r, dict) else None for r in actual_rows]
    expected_ids = [r['order_id'] for r in reference['orders']]
    coverage = _ids_match(actual_ids, expected_ids)
    rows, matched = [], 0
    for expected in reference['orders']:
        candidates = [r for r in actual_rows if isinstance(r, dict) and r.get('order_id') == expected['order_id']]
        actual = candidates[0] if len(candidates) == 1 else {}
        balance = actual.get('balance', actual)
        balance = balance if isinstance(balance, dict) else {}
        mismatches = []
        for field in FIELDS:
            observed = actual.get(field, balance.get(field)) if field in ID_FIELDS + ('review',) else balance.get(field)
            wanted = expected[field]
            same = _field_matches(field, observed, wanted)
            # Conflicting copies of a field/order ID must not pass through normalization.
            if field in actual and field in balance:
                same = same and _field_matches(field, actual[field], wanted) and _field_matches(field, balance[field], wanted)
            if 'order_id' in balance and balance['order_id'] != expected['order_id']:
                same = False
            if same:
                matched += 1
            else:
                mismatches.append({'field': field, 'expected': wanted, 'actual': observed})
        rows.append({'order_id': expected['order_id'], 'submitted': len(candidates) == 1,
                     'exact_match': not mismatches, 'matched_fields': len(FIELDS) - len(mismatches),
                     'total_fields': len(FIELDS), 'mismatches': mismatches})
    unallocated = plan.get('unallocated_transaction_ids') if isinstance(plan, dict) else None
    unallocated_match = _ids_match(unallocated, reference['unallocated_transaction_ids'])
    total = len(reference['orders']) * len(FIELDS) + 2
    matched += int(coverage) + int(unallocated_match)
    return {'plan_exact_match': valid and coverage and unallocated_match and all(r['exact_match'] for r in rows),
            'field_accuracy': round(matched / total, 6), 'matched_fields': matched, 'total_fields': total,
            'order_coverage_exact': coverage, 'expected_order_ids': expected_ids,
            'submitted_order_ids': actual_ids, 'orders': rows,
            'unallocated_exact': unallocated_match,
            'expected_unallocated_transaction_ids': reference['unallocated_transaction_ids'],
            'submitted_unallocated_transaction_ids': unallocated}


def tool_metrics(result):
    events = [e for e in result.get('trace', []) if e.get('event') == 'tool_result' and e.get('executed')]
    failed = [e for e in events if (e.get('result') or {}).get('ok') is not True]
    checks = [e for e in events if e.get('tool') == 'validate_reconciliation']
    last = (checks[-1].get('result') or {}) if checks else {}
    return {'executed_calls': len(events), 'successful_calls': len(events) - len(failed),
            'tool_errors': len(failed),
            'tool_success_rate': round((len(events) - len(failed)) / len(events), 6) if events else None,
            'tool_error_codes': dict(Counter((e.get('result', {}).get('error') or {}).get('code', 'UNKNOWN')
                                             for e in failed)),
            'validation_calls': len(checks),
            'last_validation_valid': (last.get('data') or {}).get('valid'),
            'validation_passed': bool(last.get('ok') and (last.get('data') or {}).get('valid') is True)}


def evaluate_results(results, visible_root, split, pricing=None):
    """Called by the trusted runner only after generation. No feedback is sent to the model."""
    root = Path(visible_root).absolute()
    if split not in ('train', 'val') or root.name != 'agent_visible' or root.resolve() != root:
        raise ValueError('评测仅开放真实agent_visible目录的train/val')
    output = copy.deepcopy(results)
    targets = {r['task_id'] for r in results if r.get('kind') in REAL_KINDS}
    references, tasks, source_hash = {}, {}, None
    if targets:
        task_path = root / split / 'tasks.jsonl'
        gold_path = root.parent / 'hidden' / split / 'ground_truth.jsonl'
        if task_path.resolve() != task_path or gold_path.resolve() != gold_path:
            raise ValueError('拒绝评测任务或参考答案符号链接')
        for line in task_path.read_text(encoding='utf-8').splitlines():
            row = json.loads(line)
            if row['task_id'] in targets:
                if row['task_id'] in tasks:
                    raise ValueError('任务ID重复')
                tasks[row['task_id']] = row
        raw = gold_path.read_bytes()
        source_hash = hashlib.sha256(raw).hexdigest()
        for line in raw.decode('utf-8').splitlines():
            row = json.loads(line)
            if row['task_id'] in targets:
                if row['task_id'] in references:
                    raise ValueError('参考答案任务ID重复')
                references[row['task_id']] = row
        if references.keys() != targets or tasks.keys() != targets:
            raise ValueError('任务ID未在指定数据集/切分中找到；拒绝静默漏评')
    for result in output:
        result['cost'] = measure_cost(result, pricing)
        metrics = tool_metrics(result)
        if result.get('kind') not in REAL_KINDS:
            result.update(accuracy=None, evaluation={'status': 'not_applicable',
                          'reason': '脚本/规则演示不计入模型准确率', 'tool_metrics': metrics})
            continue
        task_id = result['task_id']
        if result.get('input', {}).get('scope') != tasks[task_id]['query']:
            raise ValueError('轨迹scope与所选数据集任务不一致')
        reference = references[task_id]['reference']
        if reference['rule_version'] != result.get('input', {}).get('rules', {}).get('version'):
            raise ValueError('轨迹与参考答案规则版本不一致')
        plan, source, error = extract_submission(result)
        scores = score_plan(plan, reference)
        successful = bool(scores['plan_exact_match'] and result.get('stop_reason') == 'completed'
                          and result.get('model_connected') is True and not error)
        reasons = []
        if error:
            reasons.append(error)
        elif not scores['plan_exact_match']:
            reasons.append('REFERENCE_MISMATCH')
        if result.get('stop_reason') != 'completed':
            reasons.append('RUN_NOT_COMPLETED')
        if not result.get('model_connected'):
            reasons.append('NO_MODEL_RESPONSE')
        result.update(accuracy=float(successful), evaluation={
            'status': 'scored', 'grading_version': 'structured-plan-exact-v1', 'accuracy_definition': DEFINITION,
            'submission_source': source, 'submission_present': source is not None,
            'submission_validated': (result['validated_submission'] is not None
                                     if 'validated_submission' in result else metrics['validation_passed']),
            'failure_reasons': reasons, 'scores': scores, 'tool_metrics': metrics,
            'reference': {'split': split, 'category': references[task_id]['category'],
                          'rule_version': reference['rule_version'], 'sha256': source_hash},
            'submission_contract_requested': any(
                '最终必须提交可评测的结构化对账方案' in (m.get('content') or '')
                for e in result.get('trace', []) if e.get('event') == 'model_input'
                for m in e.get('messages', []) if m.get('role') == 'system'),
            'post_run_only': True, 'natural_language_report_scored': False})
    return output


def summarize_evaluations(results):
    scored = [r for r in results if isinstance(r.get('evaluation'), dict)
              and r['evaluation'].get('status') == 'scored']
    if not scored:
        if any(isinstance(r.get('evaluation'), dict) for r in results):
            return {'accuracy': None, 'cost': {'api_fee': 0.0, 'api_fee_status': 'simulation_not_billable'},
                    'evaluation': {'status': 'not_applicable', 'tasks_scored': 0,
                                   'tasks_excluded': len(results), 'reason': '脚本/规则演示不计入模型准确率'}}
        return {}
    count = len(scored)
    correct = sum(r['accuracy'] == 1 for r in scored)
    costs = [r['cost'] for r in scored]
    currencies = {c['currency'] for c in costs}
    fee_known = all(c['api_fee'] is not None for c in costs) and len(currencies) == 1
    compute_known = all(c['compute_fee_estimate'] is not None for c in costs) and len(currencies) == 1
    tokens = {k: sum(c['reported_token_usage'].get(k, 0) for c in costs)
              for k in ('prompt_tokens', 'completion_tokens', 'total_tokens')}
    field_matched = sum(r['evaluation']['scores']['matched_fields'] for r in scored)
    field_total = sum(r['evaluation']['scores']['total_fields'] for r in scored)
    return {'accuracy': correct / count,
            'cost': {'currency': next(iter(currencies)) if len(currencies) == 1 else 'MIXED',
                     'api_fee': round(sum(c['api_fee'] for c in costs), 8) if fee_known else None,
                     'api_fee_status': 'see_task_costs' if fee_known else 'pricing_or_usage_missing_see_task_costs',
                     'compute_fee_estimate': round(sum(c['compute_fee_estimate'] for c in costs), 8)
                     if compute_known else None, 'compute_fee_status': 'estimated' if compute_known else 'not_configured_for_all_tasks',
                     'elapsed_seconds': round(sum(c['elapsed_seconds'] for c in costs), 6),
                     'reported_token_usage': tokens, 'token_usage_complete': all(c['token_usage_complete'] for c in costs)},
            'evaluation': {'status': 'scored', 'accuracy_definition': DEFINITION,
                           'tasks_scored': count, 'correct_tasks': correct,
                           'tasks_excluded': len(results) - count,
                           'legacy_prompt_tasks': sum(not r['evaluation']['submission_contract_requested'] for r in scored),
                           'submission_rate': sum(r['evaluation']['submission_present'] for r in scored) / count,
                           'field_accuracy': field_matched / field_total if field_total else 0,
                           'tool_validated_tasks': sum(r['evaluation']['tool_metrics']['validation_passed'] for r in scored),
                           'submission_validated_tasks': sum(
                               r['evaluation'].get('submission_validated', r['evaluation']['tool_metrics']['validation_passed'])
                               for r in scored),
                           'failure_reasons': dict(Counter(reason for r in scored
                                                          for reason in r['evaluation']['failure_reasons'])),
                           'natural_language_report_scored': False}}


def write_evaluation_report(output_dir, results, summary):
    from trace_readable import json_block
    lines = ['# Agent 实际效果评测', '', DEFINITION, '',
             '参考答案只在模型运行结束后读取。缺失结构化提交按失败计；纯文字回答未做自动语义评分。', '',
             '历史提示词没有强制结构化输出的任务，记录 submission_contract_requested=false；'
             '其0分表示未满足当前交付规范，不能解释成自然语言中的所有事实都错。', '',
             '| 任务 | 整题准确率 | 字段匹配率 | 工具成功率 | 耗时/秒 | 输出 tokens/秒 | API费用 | 结论 |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    def pct(value):
        return f'{value:.1%}' if isinstance(value, (int, float)) else '不适用'
    for row in results:
        ev = row.get('evaluation') or {}
        if not isinstance(ev, dict):
            continue
        cost = row.get('cost') or {}
        metrics = ev.get('tool_metrics', {})
        reasons = ', '.join(ev.get('failure_reasons', [])) or ev.get('status')
        fee = cost.get('api_fee')
        fee_text = f'{fee} {cost.get("currency")}' if fee is not None else str(cost.get('api_fee_status'))
        lines.append(f'| {row["task_id"]} | {pct(row.get("accuracy"))} | '
                     f'{pct(ev.get("scores", {}).get("field_accuracy"))} | '
                     f'{pct(metrics.get("tool_success_rate"))} | {row.get("elapsed_seconds")} | '
                     f'{cost.get("reported_output_tokens_per_second")} | {fee_text} | {reasons} |')
    lines.extend(['', '本地 API 费用为 0；硬件及电费未实测。算力估价仅在用户配置每小时单价时计算。', '',
                  '## 汇总', '', json_block(summary)])
    for row in results:
        ev = row.get('evaluation') or {}
        if isinstance(ev, dict) and ev.get('status') == 'scored':
            lines.extend(['', f'## {row["task_id"]} 差异明细', '', json_block(ev)])
    (Path(output_dir) / 'evaluation.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
