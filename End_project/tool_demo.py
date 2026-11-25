"""确定性规则脚本演示；不是Agent轨迹或SFT数据。预算由未来调度器控制。"""
import argparse
import json
from pathlib import Path
from business_tools import ToolSession, tool_schemas


def run_demo(session):
    log = []
    def call(name, **arguments):
        result = session.call(name, arguments)
        log.append({'tool': name, 'arguments': arguments, 'result': result})
        if not result['ok']:
            raise ValueError(result['error'])
        return result['data']
    orders = call('query_orders')['orders']
    events = call('search_receipts')['events']
    transactions = sorted({e['transaction_id'] for e in events})
    call('check_duplicate_events', transaction_ids=transactions)
    allocations = {o['order_id']: [] for o in orders}
    unallocated, missing = [], set()
    for tx in transactions:
        candidates = call('find_match_candidates', transaction_id=tx)
        evidence = call('get_transaction_evidence', transaction_id=tx)
        if evidence['transaction'] is not None and evidence['transaction']['status'] != 'success':
            continue
        strong = [c for c in candidates['candidates'] if c['strong']]
        if len(strong) == 1 and strong[0]['order_id'] in allocations:
            allocations[strong[0]['order_id']].append(tx)
        elif not strong:
            unallocated.append(tx)
            missing.update(evidence['missing_fields'])
    plan = {'orders': [], 'unallocated_transaction_ids': unallocated}
    for order in orders:
        oid = order['order_id']
        refunds = call('query_refunds', order_id=oid)['events']
        refund_ids = sorted({e['transaction_id'] for e in refunds})
        balance = call('calculate_reconciliation', order_id=oid, receipt_ids=allocations[oid], refund_ids=refund_ids)
        review = any(c['order_id'] == oid for tx in unallocated
                     for c in call('find_match_candidates', transaction_id=tx)['candidates'])
        plan['orders'].append({'order_id': oid, 'receipt_ids': allocations[oid], 'refund_ids': refund_ids,
                               'balance': balance, 'review': review, 'review_reason': '缺少强归属引用，同额不能确认' if review else '',
                               'missing_fields': sorted(missing) if review else []})
    validation = call('validate_reconciliation', plan=plan)
    return {'kind': 'deterministic_rule_script_demo', 'model_connected': False, 'calls': log,
            'plan': plan, 'validation': validation}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--visible-root', default='datasets/prepared/agent_visible')
    parser.add_argument('--split', choices=['train', 'val'], default='train')
    parser.add_argument('--environment')
    parser.add_argument('--scope', help='任务query对象的JSON')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--schemas', action='store_true')
    args = parser.parse_args()
    if args.schemas:
        print(json.dumps(tool_schemas(), ensure_ascii=False, indent=2))
        return
    if not args.environment or not args.scope:
        parser.error('演示必须显式指定environment和scope')
    session = ToolSession.from_visible(args.visible_root, args.split, args.environment, json.loads(args.scope))
    result = run_demo(session)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'kind': result['kind'], 'calls': len(result['calls']), 'validation': result['validation'],
                      'orders': len(result['plan']['orders']), 'unallocated': result['plan']['unallocated_transaction_ids']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
