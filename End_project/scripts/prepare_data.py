"""以 Olist 金额和订单为底座生成隔离的模拟对账任务；不生成模型轨迹。"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import random
import sys

from reference import RULE_VERSION, build_reference

VERSION = 'olist-sim-v2'
ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = {'basic': ('normal', 'split_receipts'),
             'cross_tool': ('partial_refund', 'pending_refund', 'recoverable_reference', 'multiple_refunds'),
             'boundary': ('duplicate_event', 'ambiguous_amount', 'cutoff', 'refund_cutoff', 'refund_observed_cutoff')}
RULES = {
    'version': RULE_VERSION, 'currency': 'BRL', 'money_unit': 'integer_cent',
    'time_policy': '模拟事件统一使用固定UTC-03:00；原订单无时区，按该偏移解释，不声称原始时区已知。',
    'cutoff_policy': 'effective_at和observed_at均不晚于cutoff，包含等于边界。',
    'matching_policy': '先用order_id；缺失时用唯一merchant_reference；退款用original_transaction_id。同额仅产生候选，不能单独确认归属。',
    'dedup_policy': '按transaction_id计一笔，同一交易通知金额、状态、归属和生效时间必须一致；保留截止前最早observed_at通知，同时间按event_id。',
    'refund_policy': '仅success退款减少净收；pending不扣款。退款成功累计不能超过原交易成功金额。',
    'balance_policy': 'received=成功收款；refunded=成功退款；net=received-refunded；collection_gap=expected-received；net_vs_original=expected-net。正常部分退款不视作少收。',
    'allocation_policy': '每笔交易最多归属一个订单；歧义挂起，资金列为unallocated；目标外订单只作候选上下文。',
    'period_policy': 'period_batch以[start,end)选订单created_at，按cutoff核验交易；可见orders即该环境全量订单。',
    'source_policy': 'Olist没有实际到账时间、退款或通知；所有事件均为模拟，installments不是到账分笔。',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def write_lines(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n' for r in rows))


def cents(value):
    d = Decimal(value) * 100
    if not d.is_finite() or d != d.to_integral_value():
        raise ValueError('非整数分金额')
    return int(d)


def load_sources(raw, seed):
    manifest = json.loads((raw / 'source_manifest.json').read_text())
    tables = {}
    for role, entry in manifest['files'].items():
        path = raw / entry['filename']
        if digest(path) != entry['sha256']:
            raise ValueError(f'源文件校验失败: {path}')
        with path.open(newline='', encoding='utf-8-sig') as stream:
            tables[role] = list(csv.DictReader(stream))
    if set(tables) != {'orders', 'items', 'payments', 'customers'}:
        raise ValueError('必须提供orders/items/payments/customers四表')
    customers = {r['customer_id']: r['customer_unique_id'] for r in tables['customers']}
    items, payments = defaultdict(list), defaultdict(list)
    for r in tables['items']:
        items[r['order_id']].append(r)
    for r in tables['payments']:
        payments[r['order_id']].append(r)
    pools, excluded = defaultdict(list), Counter()
    seen = set()
    for order in tables['orders']:
        oid = order['order_id']
        if oid in seen:
            raise ValueError('源orders主键重复')
        seen.add(oid)
        if order['order_status'] != 'delivered':
            excluded['not_delivered'] += 1
            continue
        if not items[oid] or not payments[oid] or order['customer_id'] not in customers:
            excluded['missing_join'] += 1
            continue
        try:
            total = sum(cents(r['price']) + cents(r['freight_value']) for r in items[oid])
            paid = sum(cents(r['payment_value']) for r in payments[oid])
            valid = total >= 4 and total == paid
            valid &= all(cents(r['price']) > 0 and cents(r['freight_value']) >= 0 for r in items[oid])
            valid &= all(cents(r['payment_value']) > 0 and int(r['payment_installments']) >= 0 for r in payments[oid])
            valid &= len({r['payment_sequential'] for r in payments[oid]}) == len(payments[oid])
            valid &= len({r['order_item_id'] for r in items[oid]}) == len(items[oid])
            datetime.fromisoformat(order['order_purchase_timestamp'])
            if not valid:
                raise ValueError('金额或序号不一致')
        except (ValueError, InvalidOperation):
            excluded['inconsistent_amount_or_fields'] += 1
            continue
        customer = customers[order['customer_id']]
        bucket = int(hashlib.sha256(f'{seed}:{customer}'.encode()).hexdigest()[:8], 16) % 100
        split = 'train' if bucket < 70 else ('val' if bucket < 80 else 'test')
        pools[split].append({'source_order': order, 'source_items': items[oid], 'source_payments': payments[oid],
                             'source_customer_unique_id': customer, 'amount_cents': total})
    for split in ('train', 'val', 'test'):
        random.Random(f'{seed}:{split}').shuffle(pools[split])
    return pools, dict(excluded), manifest


def new_id(rng):
    return f'{rng.getrandbits(128):032x}'


def stamp(date):
    return date.isoformat(timespec='seconds')


def make_task(sources, scenario, mode, rng):
    task_id = new_id(rng)
    public_orders, hidden_orders = [], []
    for index, source in enumerate(sources):
        oid = new_id(rng)
        original = source['source_order']
        created = datetime.fromisoformat(original['order_purchase_timestamp']).replace(tzinfo=timezone(timedelta(hours=-3)))
        amount = sources[0]['amount_cents'] if scenario == 'ambiguous_amount' and index == 1 else source['amount_cents']
        order = {'order_id': oid, 'customer_reference': new_id(rng), 'merchant_reference': new_id(rng),
                 'expected_cents': amount, 'currency': 'BRL', 'created_at': stamp(created),
                 'source_payment_attributes': [{'payment_type': p['payment_type'], 'payment_installments': int(p['payment_installments'])} for p in source['source_payments']],
                 'provenance': {'order_id': 'synthetic', 'customer_reference': 'synthetic', 'merchant_reference': 'synthetic',
                     'expected_cents': 'modified' if amount != source['amount_cents'] else 'derived',
                     'currency': 'derived', 'created_at': 'derived', 'source_payment_attributes': 'original'}}
        field_provenance = order.pop('provenance')
        public_orders.append(order)
        hidden_orders.append({'id': oid, 'expected_cents': amount, 'source': source, 'field_provenance': field_provenance,
                              'lineage': {'created_at': 'source_order.order_purchase_timestamp + assumed UTC-03:00',
                                          'expected_cents': 'sum(source_items.price + freight_value), except explicitly modified equal-amount distractor'}})
    cutoff_date = max(datetime.fromisoformat(o['created_at']) for o in public_orders) + timedelta(days=10)
    cutoff = stamp(cutoff_date)
    events, transfers = [], []

    def add(kind, amount, owner, when, status='success', reference=None, missing=False, ambiguous=False, duplicate=False):
        transaction = new_id(rng)
        order = public_orders[owner]
        first = {'event_id': new_id(rng), 'transaction_id': transaction, 'kind': kind, 'amount_cents': amount,
                 'currency': 'BRL', 'status': status, 'effective_at': stamp(when), 'observed_at': stamp(when),
                 'order_id': None if missing or ambiguous or kind == 'refund' else order['order_id'],
                 'merchant_reference': None if ambiguous or kind == 'refund' else order['merchant_reference'],
                 'original_transaction_id': reference,
                 'provenance': {'entity': 'synthetic', 'amount_cents': 'derived', 'currency': 'derived',
                                'all_other_fields': 'synthetic'}}
        field_provenance = first.pop('provenance')
        notifications = [{'id': first['event_id'], 'observed_at': first['observed_at']}]
        events.append(first)
        if duplicate:
            replay = dict(first, event_id=new_id(rng), observed_at=stamp(when + timedelta(seconds=1)))
            events.append(replay)
            notifications.append({'id': replay['event_id'], 'observed_at': replay['observed_at']})
        transfers.append({'id': transaction, 'field_provenance': field_provenance, 'kind': kind, 'amount_cents': amount, 'status': status,
                          'effective_at': first['effective_at'], 'notifications': notifications,
                          'latent_owner_id': order['order_id'], 'resolvable_order_id': None if ambiguous else order['order_id'],
                          'candidate_ids': [o['order_id'] for o in public_orders if o['expected_cents'] == amount] if ambiguous else [order['order_id']]})
        return transaction

    for index, order in enumerate(public_orders):
        amount = order['expected_cents']
        early = cutoff_date - timedelta(days=2)
        primary = index == 0
        if scenario == 'ambiguous_amount' and index < 2:
            add('receipt', amount, index, early, ambiguous=True)
            continue
        if primary and scenario in ('split_receipts', 'cutoff'):
            half = amount // 2
            add('receipt', half, index, cutoff_date if scenario == 'cutoff' else early)
            add('receipt', amount - half, index, cutoff_date + timedelta(seconds=1) if scenario == 'cutoff' else early + timedelta(hours=1))
        else:
            tx = add('receipt', amount, index, early, missing=primary and scenario == 'recoverable_reference',
                     duplicate=primary and scenario == 'duplicate_event')
            if primary and scenario in ('partial_refund', 'pending_refund', 'multiple_refunds', 'refund_cutoff', 'refund_observed_cutoff'):
                add('refund', amount // 3, index,
                    cutoff_date if scenario in ('refund_cutoff', 'refund_observed_cutoff') else early + timedelta(days=1),
                    status='pending' if scenario == 'pending_refund' else 'success', reference=tx)
                if scenario == 'multiple_refunds':
                    add('refund', amount // 4, index, early + timedelta(days=1, hours=1), reference=tx)
                elif scenario == 'refund_cutoff':
                    add('refund', amount // 4, index, cutoff_date + timedelta(seconds=1), reference=tx)
                elif scenario == 'refund_observed_cutoff':
                    # 业务已生效但通知在截止后才到，不能使用未来证据。
                    late = stamp(cutoff_date + timedelta(seconds=1))
                    events[-1]['observed_at'] = late
                    transfers[-1]['notifications'][0]['observed_at'] = late
    target = [o['order_id'] for o in public_orders] if mode == 'period_batch' else [public_orders[0]['order_id']]
    start = min(o['created_at'] for o in public_orders)
    end = stamp(max(datetime.fromisoformat(o['created_at']) for o in public_orders) + timedelta(seconds=1))
    query = {'mode': mode, 'cutoff': cutoff}
    if mode == 'single_order':
        query['order_id'] = target[0]
        request = f'核查订单 {target[0]}，截至 {cutoff} 的收款、退款、差额和待复核项，并列出证据。'
    else:
        query.update({'period_start': start, 'period_end': end})
        request = f'批量核查账期 [{start}, {end}) 内全部订单，截至 {cutoff}，逐单列出证据及差额并汇总。'
    rng.shuffle(events)
    rng.shuffle(public_orders)
    env = {'schema_version': VERSION, 'orders': public_orders, 'events': events}
    task = {'task_id': task_id, 'request': request, 'query': query, 'environment_file': f'environments/{task_id}.json', 'rules_file': '../rules.json'}
    facts = {'task_id': task_id, 'scenario': scenario, 'cutoff': cutoff, 'target_order_ids': target,
             'orders': hidden_orders, 'transfers': transfers}
    return task, env, facts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw', type=Path, default=ROOT / 'datasets/raw')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20261124)
    parser.add_argument('--counts', type=int, nargs=3, default=[200, 50, 360], metavar=('TRAIN', 'VAL', 'TEST'))
    args = parser.parse_args()
    if min(args.counts) < 1:
        parser.error('每个切分任务数必须为正数')
    if args.output.exists() and any(args.output.iterdir()):
        parser.error('输出目录非空；为保护已有数据，请指定新目录')
    pools, excluded, source_manifest = load_sources(args.raw, args.seed)
    rng = random.Random(args.seed)
    dump(args.output / 'agent_visible/rules.json', RULES)
    stats = {'version': VERSION, 'rule_version': RULE_VERSION, 'seed': args.seed,
             'python': sys.version.split()[0], 'source': source_manifest, 'source_exclusions': excluded,
             'eligible_pool_counts': {s: len(p) for s, p in pools.items()}, 'splits': {},
             'split_policy': 'SHA256(seed:customer_unique_id)%100: train<70,val<80,test otherwise; source order consumed once',
             'code_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sorted(list((ROOT / 'scripts').glob('*.py')) + list((ROOT / 'tests').glob('*.py')))}}
    for split, count in zip(('train', 'val', 'test'), args.counts):
        tasks, facts_rows, answers, selected = [], [], [], []
        categories, scenarios, modes = Counter(), Counter(), Counter()
        cursor = 0
        for i in range(count):
            category = tuple(SCENARIOS)[i % 3]
            choices = SCENARIOS[category]
            scenario = choices[(i // 3) % len(choices)]
            mode = 'period_batch' if (i // 9 + i) % 2 else 'single_order'
            size = 3 if mode == 'period_batch' else (2 if scenario == 'ambiguous_amount' else 1)
            sources = pools[split][cursor:cursor + size]
            cursor += size
            if len(sources) != size:
                raise ValueError(f'{split}源订单不足')
            task, env, facts = make_task(sources, scenario, mode, rng)
            dump(args.output / 'agent_visible' / split / task['environment_file'], env)
            tasks.append(task)
            facts_rows.append(facts)
            answers.append({'task_id': task['task_id'], 'category': category, 'reference': build_reference(facts)})
            selected.extend({'task_id': task['task_id'], 'source_order_id': s['source_order']['order_id'],
                             'source_customer_unique_id': s['source_customer_unique_id']} for s in sources)
            categories[category] += 1
            scenarios[scenario] += 1
            modes[mode] += 1
        write_lines(args.output / 'agent_visible' / split / 'tasks.jsonl', tasks)
        write_lines(args.output / 'hidden' / split / 'facts.jsonl', facts_rows)
        write_lines(args.output / 'hidden' / split / 'ground_truth.jsonl', answers)
        write_lines(args.output / 'hidden' / split / 'source_assignments.jsonl', selected)
        stats['splits'][split] = {'tasks': count, 'source_orders': cursor, 'categories': dict(categories),
                                  'scenarios': dict(scenarios), 'modes': dict(modes)}
    stats['output_sha256'] = {str(p.relative_to(args.output)): digest(p) for p in sorted(args.output.rglob('*')) if p.is_file()}
    dump(args.output / 'statistics.json', stats)
    print(json.dumps({'output': str(args.output), 'splits': stats['splits'], 'excluded': excluded}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
