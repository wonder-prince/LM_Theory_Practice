"""独立参考答案：仅消费隐藏的场景事实账本，不读取可见环境或调用匹配器。"""
RULE_VERSION = 'brl-reconciliation-v1'


def build_reference(facts):
    cutoff = facts['cutoff']
    target = set(facts['target_order_ids'])
    balances = {o['id']: {'order_id': o['id'], 'expected_cents': o['expected_cents'],
                          'received_cents': 0, 'refunded_cents': 0,
                          'receipt_ids': [], 'refund_ids': [], 'pending_refund_ids': [],
                          'pending_refund_cents': 0, 'review': False}
                for o in facts['orders'] if o['id'] in target}
    unallocated, future, duplicates = [], [], []
    for transfer in facts['transfers']:
        notifications = sorted(transfer['notifications'], key=lambda e: (e['observed_at'], e['id']))
        eligible = [e for e in notifications if e['observed_at'] <= cutoff and transfer['effective_at'] <= cutoff]
        if not eligible:
            future.extend(e['id'] for e in notifications)
            continue
        duplicates.extend(e['id'] for e in eligible[1:])
        future.extend(e['id'] for e in notifications if e['observed_at'] > cutoff)
        if transfer['status'] != 'success':
            oid = transfer['resolvable_order_id']
            if transfer['kind'] == 'refund' and transfer['status'] == 'pending' and oid in balances:
                balances[oid]['pending_refund_cents'] += transfer['amount_cents']
                balances[oid]['pending_refund_ids'].append(transfer['id'])
            continue
        if transfer['resolvable_order_id'] is None:
            unallocated.append(transfer['id'])
            for oid in transfer['candidate_ids']:
                if oid in balances:
                    balances[oid]['review'] = True
            continue
        oid = transfer['resolvable_order_id']
        if oid not in target:
            continue
        row = balances[oid]
        if transfer['kind'] == 'receipt':
            row['received_cents'] += transfer['amount_cents']
            row['receipt_ids'].append(transfer['id'])
        else:
            row['refunded_cents'] += transfer['amount_cents']
            row['refund_ids'].append(transfer['id'])
    for row in balances.values():
        row['net_cents'] = row['received_cents'] - row['refunded_cents']
        row['collection_gap_cents'] = row['expected_cents'] - row['received_cents']
        row['net_vs_original_cents'] = row['expected_cents'] - row['net_cents']
        row['status'] = 'review' if row['review'] else ('balanced' if row['collection_gap_cents'] == 0 else 'shortfall')
        row['receipt_ids'].sort()
        row['refund_ids'].sort()
        row['pending_refund_ids'].sort()
    rows = sorted(balances.values(), key=lambda r: r['order_id'])
    totals = {key: sum(row[key] for row in rows) for key in
              ('expected_cents', 'received_cents', 'refunded_cents', 'pending_refund_cents', 'net_cents', 'collection_gap_cents', 'net_vs_original_cents')}
    return {'rule_version': RULE_VERSION, 'orders': rows, 'totals': totals,
            'unallocated_transaction_ids': sorted(unallocated), 'duplicate_event_ids': sorted(duplicates),
            'excluded_after_cutoff_event_ids': sorted(future)}
