"""从 Agent 可见证据重算并验证隐藏参考答案；不消费场景类型或潜在归属。"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path

from reference import RULE_VERSION


def read_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def validate_allocations(plan):
    used = set()
    for row in plan:
        tx = row['transaction_id']
        if tx in used:
            raise ValueError('交易重复分配')
        used.add(tx)


def reconcile(env, query):
    orders = {o['order_id']: o for o in env['orders']}
    if len(orders) != len(env['orders']):
        raise ValueError('订单ID重复')
    for order in orders.values():
        if type(order['expected_cents']) is not int or order['expected_cents'] <= 0:
            raise ValueError('订单金额非法')
        if order.get('currency', 'BRL') != 'BRL':
            raise ValueError('订单币种非法')
    cutoff = datetime.fromisoformat(query['cutoff'])
    if query['mode'] == 'single_order':
        targets = {query['order_id']}
        if not targets <= orders.keys():
            raise ValueError('目标订单不存在')
    elif query['mode'] == 'period_batch':
        start, end = map(datetime.fromisoformat, (query['period_start'], query['period_end']))
        targets = {oid for oid, o in orders.items() if start <= datetime.fromisoformat(o['created_at']) < end}
    else:
        raise ValueError('未知任务类型')
    rows = {oid: {'order_id': oid, 'expected_cents': orders[oid]['expected_cents'], 'received_cents': 0,
                  'refunded_cents': 0, 'pending_refund_cents': 0, 'receipt_ids': [], 'refund_ids': [],
                  'pending_refund_ids': [], 'review': False} for oid in targets}
    signatures, eligible, future, event_ids = {}, {}, [], set()
    for event in env['events']:
        if event['event_id'] in event_ids:
            raise ValueError('事件ID重复')
        event_ids.add(event['event_id'])
        if type(event['amount_cents']) is not int or event['amount_cents'] <= 0 or event['currency'] != 'BRL':
            raise ValueError('交易金额或币种非法')
        if event['status'] not in ('success', 'pending') or event['kind'] not in ('receipt', 'refund'):
            raise ValueError('交易类型或状态非法')
        signature = tuple(event[k] for k in ('kind', 'amount_cents', 'currency', 'status', 'effective_at', 'order_id', 'merchant_reference', 'original_transaction_id'))
        tx = event['transaction_id']
        if tx in signatures and signatures[tx] != signature:
            raise ValueError('同一交易存在冲突通知')
        signatures[tx] = signature
        if max(datetime.fromisoformat(event['effective_at']), datetime.fromisoformat(event['observed_at'])) > cutoff:
            future.append(event['event_id'])
        else:
            eligible.setdefault(tx, []).append(event)
    dedup, duplicates = {}, []
    for tx, notifications in eligible.items():
        notifications.sort(key=lambda e: (e['observed_at'], e['event_id']))
        dedup[tx] = notifications[0]
        duplicates.extend(e['event_id'] for e in notifications[1:])
    resolved, unresolved, plan = {}, [], []
    for tx, event in dedup.items():
        if event['kind'] != 'receipt' or event['status'] != 'success':
            continue
        oid = event['order_id']
        merchant = event['merchant_reference']
        if oid is not None:
            if oid not in orders or (merchant is not None and orders[oid]['merchant_reference'] != merchant):
                raise ValueError('强引用冲突')
        elif merchant is not None:
            candidates = [key for key, o in orders.items() if o['merchant_reference'] == merchant]
            if len(candidates) != 1:
                raise ValueError('商户引用不唯一或不存在')
            oid = candidates[0]
        if oid is None:
            unresolved.append(tx)
            for key, order in orders.items():
                if order['expected_cents'] == event['amount_cents'] and key in rows:
                    rows[key]['review'] = True
            continue
        resolved[tx] = oid
        plan.append({'transaction_id': tx, 'order_id': oid})
        if oid in rows:
            rows[oid]['received_cents'] += event['amount_cents']
            rows[oid]['receipt_ids'].append(tx)
    refund_totals = Counter()
    for tx, event in dedup.items():
        if event['kind'] != 'refund':
            continue
        parent = event['original_transaction_id']
        if parent not in resolved:
            raise ValueError('退款缺少截止前可确认的成功收款')
        oid = resolved[parent]
        if ((event['order_id'] is not None and event['order_id'] != oid)
                or (event['merchant_reference'] is not None
                    and event['merchant_reference'] != orders[oid]['merchant_reference'])):
            raise ValueError('退款归属冲突')
        if datetime.fromisoformat(event['effective_at']) < datetime.fromisoformat(dedup[parent]['effective_at']):
            raise ValueError('退款早于收款')
        if event['status'] == 'pending':
            if oid in rows:
                rows[oid]['pending_refund_cents'] += event['amount_cents']
                rows[oid]['pending_refund_ids'].append(tx)
            continue
        refund_totals[parent] += event['amount_cents']
        if refund_totals[parent] > dedup[parent]['amount_cents']:
            raise ValueError('退款超过原收款')
        plan.append({'transaction_id': tx, 'order_id': oid})
        if oid in rows:
            rows[oid]['refunded_cents'] += event['amount_cents']
            rows[oid]['refund_ids'].append(tx)
    validate_allocations(plan)
    for row in rows.values():
        row['net_cents'] = row['received_cents'] - row['refunded_cents']
        row['collection_gap_cents'] = row['expected_cents'] - row['received_cents']
        row['net_vs_original_cents'] = row['expected_cents'] - row['net_cents']
        row['status'] = 'review' if row['review'] else ('balanced' if row['collection_gap_cents'] == 0 else 'shortfall')
        row['receipt_ids'].sort()
        row['refund_ids'].sort()
        row['pending_refund_ids'].sort()
    result = sorted(rows.values(), key=lambda r: r['order_id'])
    keys = ('expected_cents', 'received_cents', 'refunded_cents', 'pending_refund_cents', 'net_cents', 'collection_gap_cents', 'net_vs_original_cents')
    return {'rule_version': RULE_VERSION, 'orders': result, 'totals': {k: sum(row[k] for row in result) for k in keys},
            'unallocated_transaction_ids': sorted(unresolved), 'duplicate_event_ids': sorted(duplicates),
            'excluded_after_cutoff_event_ids': sorted(future)}


def validate_dataset(root):
    stats = json.loads((root / 'statistics.json').read_text())
    project = Path(__file__).resolve().parents[1]
    for name, expected in stats['code_sha256'].items():
        if hashlib.sha256((project / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'代码版本与数据生成时不同: {name}')
    for name, expected in stats['output_sha256'].items():
        actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
        if expected != actual:
            raise ValueError(f'产物hash不一致: {name}')
    source_sets, customer_sets, task_ids, counts = {}, {}, set(), {}
    business_ids = set()
    for split in ('train', 'val', 'test'):
        hidden = root / 'hidden' / split
        assignments = read_lines(hidden / 'source_assignments.jsonl')
        source_sets[split] = {a['source_order_id'] for a in assignments}
        customer_sets[split] = {a['source_customer_unique_id'] for a in assignments}
        if len(source_sets[split]) != len(assignments):
            raise ValueError('同一源订单重复用于多个任务')
        tasks = read_lines(root / 'agent_visible' / split / 'tasks.jsonl')
        answer_rows = read_lines(hidden / 'ground_truth.jsonl')
        facts_rows = read_lines(hidden / 'facts.jsonl')
        answers = {r['task_id']: r['reference'] for r in answer_rows}
        facts = {r['task_id']: r for r in facts_rows}
        recorded = stats['splits'][split]
        if (len(tasks) != recorded['tasks'] or len(assignments) != recorded['source_orders']
                or Counter(r['category'] for r in answer_rows) != recorded['categories']
                or Counter(r['scenario'] for r in facts_rows) != recorded['scenarios']
                or Counter(t['query']['mode'] for t in tasks) != recorded['modes']):
            raise ValueError('统计与实际任务不一致')
        ids = {t['task_id'] for t in tasks}
        if len(ids) != len(tasks) or ids != set(answers) or ids != set(facts) or len(answer_rows) != len(tasks) or len(facts_rows) != len(tasks):
            raise ValueError('任务/事实/答案索引不一致')
        if task_ids & ids:
            raise ValueError('任务ID跨切分重复')
        task_ids |= ids
        assignment_tasks = {a['task_id'] for a in assignments}
        if assignment_tasks != ids:
            raise ValueError('切分清单任务不完整')
        checked, batches, reviews = 0, 0, 0
        coverage = Counter()
        source_tokens = source_sets[split] | customer_sets[split]
        for task in tasks:
            path = root / 'agent_visible' / split / task['environment_file']
            env = json.loads(path.read_text())
            env_ids = ({o['order_id'] for o in env['orders']}
                       | {e['transaction_id'] for e in env['events']}
                       | {e['event_id'] for e in env['events']})
            if business_ids & env_ids:
                raise ValueError('业务标识跨任务复用')
            business_ids |= env_ids
            coverage['visible_orders'] += len(env['orders'])
            coverage['visible_events'] += len(env['events'])
            coverage['unique_transactions'] += len({e['transaction_id'] for e in env['events']})
            coverage['refund_events'] += sum(e['kind'] == 'refund' for e in env['events'])
            serialized = json.dumps({'task': task, 'env': env})
            if any(token in serialized for token in source_tokens):
                raise ValueError('可见环境泄漏源标识')
            if any(key in serialized for key in ('latent_owner_id', 'resolvable_order_id', 'scenario', 'ground_truth', 'source_order_id')):
                raise ValueError('可见环境泄漏隐藏标签字段')
            actual = reconcile(env, task['query'])
            if actual != answers[task['task_id']]:
                raise ValueError(f'可见证据与独立参考答案不同: {task["task_id"]}')
            fact = facts[task['task_id']]
            for original in fact['orders']:
                generated_receipts = sum(t['amount_cents'] for t in fact['transfers']
                                         if t['kind'] == 'receipt' and t['latent_owner_id'] == original['id'])
                if generated_receipts != original['expected_cents']:
                    raise ValueError('模拟收款拆分未守恒（含截止后金额）')
                source_amount = original['source']['amount_cents']
                provenance = original['field_provenance']['expected_cents']
                if original['expected_cents'] != source_amount and provenance != 'modified':
                    raise ValueError('源金额变更缺少modified来源记录')
            linked_sources = {o['source']['source_order']['order_id'] for o in fact['orders']}
            listed_sources = {a['source_order_id'] for a in assignments if a['task_id'] == task['task_id']}
            if linked_sources != listed_sources or not linked_sources <= source_sets[split]:
                raise ValueError('环境含清单之外或跨切分源订单')
            if set(actual['totals']) and actual['totals']['net_cents'] != actual['totals']['received_cents'] - actual['totals']['refunded_cents']:
                raise ValueError('金额不守恒')
            if task['query']['mode'] == 'period_batch':
                if len(actual['orders']) < 2:
                    raise ValueError('批量任务没有多个订单')
                batches += 1
            reviews += sum(r['review'] for r in actual['orders'])
            checked += 1
        counts[split] = {'tasks_verified': checked, 'multi_order_batches_verified': batches,
                         'review_orders': reviews, 'coverage': dict(coverage)}
    for left, right in (('train', 'val'), ('train', 'test'), ('val', 'test')):
        if source_sets[left] & source_sets[right] or customer_sets[left] & customer_sets[right]:
            raise ValueError('源订单或客户跨切分')
    return {'status': 'passed', 'splits': counts, 'cross_split_source_order_overlap': 0,
            'cross_split_customer_overlap': 0, 'output_files_hash_verified': len(stats['output_sha256'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset', type=Path)
    parser.add_argument('--record', action='store_true', help='将实际验证结果写入statistics.json')
    args = parser.parse_args()
    result = validate_dataset(args.dataset)
    if args.record:
        path = args.dataset / 'statistics.json'
        stats = json.loads(path.read_text())
        stats['verification'] = result
        path.write_text(json.dumps(stats, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
