"""框架无关、单环境只读业务工具；不导入参考答案或环境求解器。"""
import copy
from datetime import datetime
import inspect
import json
from pathlib import Path


class BusinessError(ValueError):
    def __init__(self, code, message, **details):
        super().__init__(message)
        self.code, self.details = code, details


def require(condition, code, message, **details):
    if not condition:
        raise BusinessError(code, message, **details)


def stamp(value):
    require(isinstance(value, str), 'INVALID_TIME', '时间必须为带时区的ISO字符串')
    try:
        result = datetime.fromisoformat(value)
    except ValueError:
        raise BusinessError('INVALID_TIME', '时间格式非法')
    require(result.tzinfo is not None, 'INVALID_TIME', '时间必须包含时区')
    return result


def ids(value):
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value),
            'INVALID_ARGUMENT', '标识集合必须为非空字符串数组')
    require(len(value) == len(set(value)), 'DUPLICATE_ALLOCATION', '标识集合存在重复')
    return value


class ToolSession:
    """构造时复制快照；公开调用仅接受业务参数，不接受路径。"""
    def __init__(self, environment, scope):
        self._env = copy.deepcopy(environment)
        self._scope = copy.deepcopy(scope)
        self._orders = {o['order_id']: o for o in self._env['orders']}
        require(len(self._orders) == len(self._env['orders']), 'INVALID_ENV', '订单标识重复')
        self._cutoff = stamp(scope['cutoff'])
        if scope['mode'] == 'single_order':
            require(scope['order_id'] in self._orders, 'INVALID_SCOPE', '范围订单不存在')
            self._targets = {scope['order_id']}
        elif scope['mode'] == 'period_batch':
            start, end = stamp(scope['period_start']), stamp(scope['period_end'])
            require(start < end, 'INVALID_SCOPE', '账期起点必须早于终点')
            self._targets = {k for k, o in self._orders.items() if start <= stamp(o['created_at']) < end}
        else:
            raise BusinessError('INVALID_SCOPE', '未知范围模式')
        for o in self._orders.values():
            require(type(o['expected_cents']) is int and o['expected_cents'] > 0 and o.get('currency') == 'BRL',
                    'INVALID_ENV', '订单必须使用正整数BRL分')
        self._events = self._env['events']
        require(len({e['event_id'] for e in self._events}) == len(self._events), 'INVALID_ENV', '事件标识重复')
        for e in self._events:
            require(type(e['amount_cents']) is int and e['amount_cents'] > 0 and e['currency'] == 'BRL',
                    'INVALID_ENV', '交易必须使用正整数BRL分')
            require(e['kind'] in ('receipt', 'refund') and e['status'] in ('success', 'pending'),
                    'INVALID_ENV', '交易类型或状态非法')
            stamp(e['effective_at'])
            stamp(e['observed_at'])

    @classmethod
    def from_visible(cls, visible_root, split, environment_file, scope):
        root = Path(visible_root).absolute()
        require(root.name == 'agent_visible' and root.resolve() == root and root.is_dir(),
                'PATH_DENIED', '必须指定真实agent_visible目录')
        require(split in ('train', 'val'), 'PATH_DENIED', '运行时仅允许train或val')
        relative = Path(environment_file)
        require(not relative.is_absolute() and len(relative.parts) == 2 and relative.parts[0] == 'environments'
                and relative.suffix == '.json' and '..' not in relative.parts,
                'PATH_DENIED', '仅允许当前切分environments中的单个JSON')
        path = root / split / relative
        require(path.resolve() == path and path.is_file(), 'PATH_DENIED', '拒绝符号链接、逃逸或不存在的环境')
        return cls(json.loads(path.read_text()), scope)

    def call(self, name, arguments):
        try:
            require(name in TOOL_NAMES, 'UNKNOWN_TOOL', '工具不存在')
            require(isinstance(arguments, dict), 'INVALID_ARGUMENT', '参数必须为JSON对象')
            method = getattr(self, name)
            try:
                inspect.signature(method).bind(**arguments)
            except TypeError as exc:
                raise BusinessError('INVALID_ARGUMENT', str(exc))
            result = method(**arguments)
            return json.loads(json.dumps({'ok': True, 'data': result, 'error': None}, ensure_ascii=False))
        except BusinessError as exc:
            return {'ok': False, 'data': None, 'error': {'code': exc.code, 'message': str(exc), 'details': exc.details}}
        except (TypeError, KeyError, ValueError) as exc:
            return {'ok': False, 'data': None, 'error': {'code': 'INVALID_ARGUMENT', 'message': str(exc), 'details': {}}}

    def _order(self, oid, target=False):
        require(isinstance(oid, str) and oid in self._orders, 'UNKNOWN_ORDER', '当前环境无此订单')
        require(not target or oid in self._targets, 'OUT_OF_SCOPE', '订单不在任务范围')
        return self._orders[oid]

    def _eligible(self, e):
        return stamp(e['effective_at']) <= self._cutoff and stamp(e['observed_at']) <= self._cutoff

    def _notifications(self, tx):
        require(isinstance(tx, str) and bool(tx), 'INVALID_ARGUMENT', '交易标识必须为非空字符串')
        return [e for e in self._events if e['transaction_id'] == tx and self._eligible(e)]

    def _transaction(self, tx):
        rows = self._notifications(tx)
        require(rows, 'TRANSACTION_UNAVAILABLE', '当前范围无截止前已观察且生效的交易', transaction_id=tx)
        fields = ('kind', 'amount_cents', 'currency', 'status', 'effective_at', 'order_id', 'merchant_reference', 'original_transaction_id')
        require(len({tuple(e.get(k) for k in fields) for e in rows}) == 1,
                'CONFLICTING_EVENTS', '同一交易通知冲突，需核查事件', transaction_id=tx)
        return min(rows, key=lambda e: (stamp(e['observed_at']), e['event_id']))

    def _owner(self, e):
        oid, merchant = e.get('order_id'), e.get('merchant_reference')
        if oid:
            require(oid in self._orders and (not merchant or self._orders[oid]['merchant_reference'] == merchant),
                    'REFERENCE_CONFLICT', '订单引用与商户引用冲突')
            return oid
        if merchant:
            matches = [o['order_id'] for o in self._orders.values() if o.get('merchant_reference') == merchant]
            require(len(matches) == 1, 'REFERENCE_AMBIGUITY', '商户引用不存在或不唯一')
            return matches[0]
        return None

    def query_orders(self, order_id=None, period_start=None, period_end=None):
        require(not (order_id is not None and (period_start is not None or period_end is not None)),
                'INVALID_ARGUMENT', '订单号与账期不能同时指定')
        rows = [self._orders[k] for k in sorted(self._targets)]
        if order_id is not None:
            require(isinstance(order_id, str) and bool(order_id), 'INVALID_ARGUMENT', '订单号必须为非空字符串')
            rows = [o for o in rows if o['order_id'] == order_id]
        if period_start is not None or period_end is not None:
            start, end = stamp(period_start), stamp(period_end)
            require(start < end, 'INVALID_ARGUMENT', '账期起点必须早于终点')
            rows = [o for o in rows if start <= stamp(o['created_at']) < end]
        return {'orders': copy.deepcopy(rows), 'scope': self._scope}

    def search_receipts(self, order_id=None, merchant_reference=None, transaction_id=None,
                        effective_start=None, effective_end=None, status=None, unassigned_only=False):
        require(type(unassigned_only) is bool, 'INVALID_ARGUMENT', 'unassigned_only必须为布尔值')
        require(status is None or status in ('success', 'pending'), 'INVALID_ARGUMENT', '状态非法')
        for value in (order_id, merchant_reference, transaction_id):
            require(value is None or isinstance(value, str) and bool(value), 'INVALID_ARGUMENT', '引用必须为非空字符串')
        start = stamp(effective_start) if effective_start is not None else None
        end = stamp(effective_end) if effective_end is not None else None
        require(not (start and end) or start < end, 'INVALID_ARGUMENT', '时间范围非法')
        rows = []
        for e in self._events:
            if e['kind'] != 'receipt' or not self._eligible(e):
                continue
            if any(value is not None and e.get(key) != value for key, value in
                   (('order_id', order_id), ('merchant_reference', merchant_reference), ('transaction_id', transaction_id), ('status', status))):
                continue
            if unassigned_only and e.get('order_id'):
                continue
            if start and stamp(e['effective_at']) < start or end and stamp(e['effective_at']) >= end:
                continue
            rows.append(copy.deepcopy(e))
        return {'events': rows, 'cutoff': self._scope['cutoff']}

    def find_match_candidates(self, transaction_id):
        e = self._transaction(transaction_id)
        require(e['kind'] == 'receipt', 'INVALID_KIND', '候选检索需要收款交易')
        candidates, conflicts = [], []
        try:
            owner = self._owner(e)
        except BusinessError as exc:
            owner = None
            conflicts.append({'code': exc.code, 'message': str(exc)})
        for o in self._orders.values():
            evidence = []
            if e.get('order_id') == o['order_id']:
                evidence.append('order_id')
            if e.get('merchant_reference') and e['merchant_reference'] == o.get('merchant_reference'):
                evidence.append('merchant_reference')
            same_amount = e['amount_cents'] == o['expected_cents']
            if evidence or same_amount:
                candidates.append({'order_id': o['order_id'], 'evidence_fields': evidence,
                                   'amount_equal': same_amount, 'strong': owner == o['order_id'] and not conflicts,
                                   'in_scope': o['order_id'] in self._targets})
        return {'transaction_id': transaction_id, 'candidates': candidates, 'conflicts': conflicts,
                'amount_is_strong_evidence': False}

    def get_transaction_evidence(self, transaction_id):
        rows = self._notifications(transaction_id)
        require(rows, 'TRANSACTION_UNAVAILABLE', '当前范围无截止前已观察且生效的交易', transaction_id=transaction_id)
        try:
            e = self._transaction(transaction_id)
        except BusinessError as exc:
            if exc.code != 'CONFLICTING_EVENTS':
                raise
            fields = ('kind', 'amount_cents', 'currency', 'status', 'effective_at', 'order_id', 'merchant_reference', 'original_transaction_id')
            conflicts = [k for k in fields if len({r.get(k) for r in rows}) > 1]
            return {'transaction': None, 'events': copy.deepcopy(rows), 'status': 'conflict',
                    'conflicting_fields': conflicts, 'missing_fields': [],
                    'supplement_request': {'transaction_id': transaction_id, 'requested_fields': conflicts,
                                           'instruction': '请核实冲突事件并提供上述字段的渠道权威凭证。'}}
        required = ['event_id', 'transaction_id', 'effective_at', 'observed_at']
        if e['kind'] == 'refund':
            required.append('original_transaction_id')
        elif not e.get('order_id') and not e.get('merchant_reference'):
            required.extend(['order_id', 'merchant_reference'])
        missing = [k for k in required if not e.get(k)]
        return {'transaction': copy.deepcopy(e), 'events': copy.deepcopy(self._notifications(transaction_id)),
                'missing_fields': missing,
                'supplement_request': {'transaction_id': transaction_id, 'requested_fields': missing,
                    'instruction': '请提供支付渠道可核验的原始引用；收款需订单号或唯一商户引用，退款需原支付交易号。' if missing else ''}}

    def check_duplicate_events(self, transaction_ids):
        groups = []
        for tx in ids(transaction_ids):
            rows = self._notifications(tx)
            if not rows:
                groups.append({'transaction_id': tx, 'status': 'empty', 'duplicate_event_ids': []})
                continue
            try:
                kept = self._transaction(tx)
                groups.append({'transaction_id': tx, 'status': 'consistent', 'kept_event_id': kept['event_id'],
                               'duplicate_event_ids': sorted(e['event_id'] for e in rows if e != kept)})
            except BusinessError:
                groups.append({'transaction_id': tx, 'status': 'conflict', 'event_ids': [e['event_id'] for e in rows]})
        return {'groups': groups}

    def query_refunds(self, order_id=None, original_transaction_id=None):
        require((order_id is None) != (original_transaction_id is None), 'INVALID_ARGUMENT', '提供订单号或原交易号之一')
        parents = set()
        if order_id is not None:
            self._order(order_id)
            merchant = self._orders[order_id]['merchant_reference']
            relevant = {e['transaction_id'] for e in self._events if e['kind'] == 'receipt' and self._eligible(e)
                        and (e.get('order_id') == order_id or e.get('merchant_reference') == merchant)}
            for tx in relevant:
                e = self._transaction(tx)
                if self._owner(e) == order_id:
                    parents.add(tx)
        else:
            require(isinstance(original_transaction_id, str) and bool(original_transaction_id), 'INVALID_ARGUMENT', '原交易号非法')
            parents.add(original_transaction_id)
        return {'events': [copy.deepcopy(e) for e in self._events if e['kind'] == 'refund'
                           and e.get('original_transaction_id') in parents and self._eligible(e)]}

    def calculate_reconciliation(self, order_id, receipt_ids, refund_ids):
        order = self._order(order_id, target=True)
        ids(receipt_ids)
        ids(refund_ids)
        require(not set(receipt_ids) & set(refund_ids), 'DUPLICATE_ALLOCATION', '交易重复占用')
        received = refunded = pending = 0
        receipts, refunded_by_parent, evidence = {}, {}, []
        for tx in receipt_ids:
            e = self._transaction(tx)
            require(e['kind'] == 'receipt' and e['status'] == 'success', 'INVALID_RECEIPT', '仅可计入成功收款')
            require(self._owner(e) == order_id, 'INSUFFICIENT_EVIDENCE', '收款缺少目标订单强归属证据', transaction_id=tx)
            receipts[tx] = e
            received += e['amount_cents']
            evidence.append(e['event_id'])
        pending_ids, success_ids = [], []
        for tx in refund_ids:
            e = self._transaction(tx)
            parent = e.get('original_transaction_id')
            require(e['kind'] == 'refund' and parent in receipts, 'INVALID_REFUND_PARENT', '退款须关联本次指定的成功收款', transaction_id=tx)
            require((not e.get('order_id') or e['order_id'] == order_id) and
                    (not e.get('merchant_reference') or e['merchant_reference'] == order['merchant_reference']),
                    'REFERENCE_CONFLICT', '退款归属引用冲突')
            require(stamp(e['effective_at']) >= stamp(receipts[parent]['effective_at']), 'INVALID_REFUND_TIME', '退款早于收款')
            if e['status'] == 'pending':
                pending += e['amount_cents']
                pending_ids.append(tx)
            else:
                refunded_by_parent[parent] = refunded_by_parent.get(parent, 0) + e['amount_cents']
                require(refunded_by_parent[parent] <= receipts[parent]['amount_cents'], 'OVER_REFUND', '累计成功退款超过原收款')
                refunded += e['amount_cents']
                success_ids.append(tx)
            evidence.append(e['event_id'])
        expected = order['expected_cents']
        return {'order_id': order_id, 'expected_cents': expected, 'received_cents': received,
                'refunded_cents': refunded, 'pending_refund_cents': pending, 'net_cents': received - refunded,
                'collection_gap_cents': expected - received, 'net_vs_original_cents': expected - received + refunded,
                'receipt_ids': sorted(receipt_ids), 'refund_ids': sorted(success_ids), 'pending_refund_ids': sorted(pending_ids),
                'evidence_event_ids': sorted(evidence)}

    def validate_reconciliation(self, plan):
        require(isinstance(plan, dict) and set(plan) == {'orders', 'unallocated_transaction_ids'}, 'INVALID_PLAN',
                '方案必须包含orders与unallocated_transaction_ids')
        require(isinstance(plan['orders'], list), 'INVALID_PLAN', 'orders必须为数组')
        unallocated = ids(plan['unallocated_transaction_ids'])
        errors, used, seen, justified_reviews = [], {}, set(), set()
        def issue(code, message, **details):
            errors.append({'code': code, 'message': message, **details})
        for index, row in enumerate(plan['orders']):
            require(isinstance(row, dict), 'INVALID_PLAN', '逐单方案必须为对象')
            required = {'order_id', 'receipt_ids', 'refund_ids', 'review', 'review_reason', 'missing_fields', 'balance'}
            if set(row) != required:
                issue('PLAN_FIELDS', '补齐逐单方案字段并移除未知字段', index=index, required_fields=sorted(required))
                continue
            oid = row['order_id']
            require(isinstance(oid, str), 'INVALID_PLAN', '订单号必须为字符串')
            if oid in seen:
                issue('DUPLICATE_ORDER', '同一订单只能提交一次', order_id=oid)
            seen.add(oid)
            for tx in ids(row['receipt_ids']) + ids(row['refund_ids']):
                if tx in used:
                    issue('DUPLICATE_ALLOCATION', '交易跨行重复占用，请移除重复分配', transaction_id=tx)
                used[tx] = oid
            receipt_ids = row['receipt_ids']
            refund_ids = row['refund_ids']
            result = self.call('calculate_reconciliation', {'order_id': oid, 'receipt_ids': receipt_ids, 'refund_ids': refund_ids})
            if not result['ok']:
                issue(result['error']['code'], result['error']['message'], order_id=oid, **result['error']['details'])
            elif (row['balance'] != result['data'] or not isinstance(row['balance'], dict)
                  or any(type(row['balance'].get(k)) is not int for k in result['data'] if k.endswith('_cents'))):
                issue('BALANCE_MISMATCH', '按指定交易重新调用calculate_reconciliation并提交完整整数分balance', order_id=oid)
            require(type(row['review']) is bool and isinstance(row['review_reason'], str), 'INVALID_PLAN', 'review或理由类型非法')
            ids(row['missing_fields'])
            if row['review'] and (not row['review_reason'].strip() or not row['missing_fields']):
                issue('REVIEW_DETAILS', '待复核必须说明原因及具体待补字段', order_id=oid)
            if not row['review'] and (row['review_reason'] or row['missing_fields']):
                issue('REVIEW_DETAILS', '非待复核订单不应携带待补原因或字段', order_id=oid)
        if seen != self._targets:
            issue('ORDER_COVERAGE', '按query_orders覆盖全部且仅范围内订单', missing_order_ids=sorted(self._targets - seen), extra_order_ids=sorted(seen - self._targets))
        for tx in unallocated:
            if tx in used:
                issue('ALLOCATION_CONFLICT', '已分配交易不能同时列为未分配', transaction_id=tx)
            try:
                self._transaction(tx)
            except BusinessError as exc:
                issue(exc.code, str(exc), transaction_id=tx)
        target_merchants = {self._orders[oid]['merchant_reference'] for oid in self._targets}
        def may_target(event):
            oid, merchant = event.get('order_id'), event.get('merchant_reference')
            return (oid in self._targets or merchant in target_merchants or
                    not oid and not merchant or oid is not None and oid not in self._orders)
        for tx in sorted({e['transaction_id'] for e in self._events if self._eligible(e)}):
            raw = self._notifications(tx)
            related_raw = [e for e in raw if e['kind'] == 'receipt']
            for refund in (e for e in raw if e['kind'] == 'refund'):
                parents = [p for p in self._events if p['transaction_id'] == refund.get('original_transaction_id')
                           and p['kind'] == 'receipt' and self._eligible(p)]
                related_raw.extend(parents or [refund])
            if not any(may_target(e) for e in related_raw):
                if tx in unallocated:
                    issue('OUT_OF_SCOPE', '未分配清单包含无关订单交易，请移除', transaction_id=tx)
                continue
            try:
                e = self._transaction(tx)
                if e['kind'] == 'receipt':
                    owner = self._owner(e)
                    related = owner in self._targets or owner is None
                else:
                    parent = self._transaction(e.get('original_transaction_id'))
                    owner = self._owner(parent)
                    related = owner in self._targets or owner is None
                if not related:
                    if tx in unallocated:
                        issue('OUT_OF_SCOPE', '未分配清单包含无关订单交易，请移除', transaction_id=tx)
                    continue
                if e['kind'] == 'receipt' and e['status'] == 'pending':
                    continue
                if tx not in used and tx not in unallocated:
                    issue('TRANSACTION_OMITTED', '补查交易并在分配或未分配中明确处置', transaction_id=tx)
                if tx in unallocated and owner is not None:
                    issue('UNALLOCATED_WITH_EVIDENCE', '交易有强引用，需核对归属后处理', transaction_id=tx)
                if owner is None:
                    affected = [o for o in plan['orders'] if o.get('order_id') in self._targets and
                                self._orders[o['order_id']]['expected_cents'] == e['amount_cents']]
                    for row in affected:
                        justified_reviews.add(row['order_id'])
                        if not row.get('review'):
                            issue('REVIEW_REQUIRED', '同额仅为弱候选，需挂起并请求订单或商户引用', order_id=row['order_id'])
                        elif not set(row.get('missing_fields', [])) & {'order_id', 'merchant_reference'}:
                            issue('REVIEW_FIELDS', '缺失归属须请求order_id或merchant_reference', order_id=row['order_id'])
            except BusinessError as exc:
                issue(exc.code, str(exc), transaction_id=tx)
        for row in plan['orders']:
            if row.get('review') and row.get('order_id') not in justified_reviews:
                issue('UNJUSTIFIED_REVIEW', '当前可见证据不支持所报归属缺失；核对引用并纠正待复核结论', order_id=row.get('order_id'))
        return {'valid': not errors, 'errors': errors}


TOOL_NAMES = ('query_orders', 'search_receipts', 'find_match_candidates', 'get_transaction_evidence',
              'check_duplicate_events', 'query_refunds', 'calculate_reconciliation', 'validate_reconciliation')


def tool_schemas():
    """标准function schema；运行时call同时执行参数绑定与业务校验。"""
    text = {'type': 'string', 'minLength': 1}
    array = {'type': 'array', 'items': text, 'uniqueItems': True}
    balance_properties = {'order_id': text,
        **{key: {'type': 'integer'} for key in ('expected_cents', 'received_cents', 'refunded_cents',
            'pending_refund_cents', 'net_cents', 'collection_gap_cents', 'net_vs_original_cents')},
        **{key: array for key in ('receipt_ids', 'refund_ids', 'pending_refund_ids', 'evidence_event_ids')}}
    balance_schema = {'type': 'object', 'additionalProperties': False,
        'description': '原样复制calculate_reconciliation返回的完整data对象，包含order_id、全部金额、交易列表及evidence_event_ids；不能只传金额字段。',
        'required': list(balance_properties), 'properties': balance_properties}
    specs = {
        'query_orders': ('查询任务范围内订单；账期左闭右开', {'order_id': text, 'period_start': text, 'period_end': text}, []),
        'search_receipts': ('在当前环境截止前精确检索收款，支持未归属补查',
            {**{k: text for k in ('order_id', 'merchant_reference', 'transaction_id', 'effective_start', 'effective_end')},
             'status': {'type': 'string', 'enum': ['success', 'pending']}, 'unassigned_only': {'type': 'boolean'}}, []),
        'find_match_candidates': ('仅返回可见候选、证据与冲突；同额不是强证据', {'transaction_id': text}, ['transaction_id']),
        'get_transaction_evidence': ('补查现有事件凭证并返回具体缺失字段', {'transaction_id': text}, ['transaction_id']),
        'check_duplicate_events': ('仅对同一交易的通知查重并检测冲突', {'transaction_ids': array}, ['transaction_ids']),
        'query_refunds': ('按订单或原支付交易号查询退款，保留pending', {'order_id': text, 'original_transaction_id': text}, []),
        'calculate_reconciliation': ('仅计算显式分配交易，使用整数BRL分并分别报告收款差额与净收',
            {'order_id': text, 'receipt_ids': array, 'refund_ids': array}, ['order_id', 'receipt_ids', 'refund_ids']),
        'validate_reconciliation': ('核验整批方案的覆盖、证据、重复占用、金额与待复核字段；不生成分配答案',
            {'plan': {'type': 'object', 'required': ['orders', 'unallocated_transaction_ids'], 'additionalProperties': False,
                      'properties': {'unallocated_transaction_ids': array, 'orders': {'type': 'array', 'items': {
                          'type': 'object', 'additionalProperties': False,
                          'required': ['order_id', 'receipt_ids', 'refund_ids', 'review', 'review_reason', 'missing_fields', 'balance'],
                          'properties': {'order_id': text, 'receipt_ids': array, 'refund_ids': array,
                              'review': {'type': 'boolean'}, 'review_reason': {'type': 'string'},
                              'missing_fields': array, 'balance': balance_schema}}}}}}, ['plan']),
    }
    return [{'type': 'function', 'function': {'name': name, 'description': specs[name][0],
            'parameters': {'type': 'object', 'properties': specs[name][1], 'required': specs[name][2],
                           'additionalProperties': False}}} for name in TOOL_NAMES]


def register_tools(session):
    return {name: (lambda _name=name, **arguments: session.call(_name, arguments)) for name in TOOL_NAMES}
