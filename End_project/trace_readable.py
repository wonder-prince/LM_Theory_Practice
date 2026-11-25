"""人工审阅视图；只转换已保存结果，不调用模型或重新执行业务工具。"""
import json
import re


def json_block(value):
    text = json.dumps(value, ensure_ascii=False, indent=2)
    return fenced(text, 'json')


def fenced(text, language=''):
    # 参数或回执含反引号时，仍完整留在代码块内。
    runs = re.findall(r'`+', str(text))
    fence = '`' * max(3, 1 + max(map(len, runs), default=0))
    return f'{fence}{language}\n{text}\n{fence}\n'


def arguments_value(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (ValueError, RecursionError):
            return value
    return value


def tool_status(event):
    result = event.get('result') or {}
    if not event.get('executed', False):
        return '未执行'
    if result.get('ok') is not True:
        return '工具报错'
    data = result.get('data')
    if isinstance(data, dict) and data.get('valid') is False:
        return '调用成功，方案未通过'
    if isinstance(data, dict) and data.get('valid') is True:
        return '方案核验通过'
    return '调用成功'


def table_cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')


def render_trace(results):
    out = ['# Agent 运行轨迹（人工审阅版）',
           '此文件由真实保存记录转换；未重新调用模型或工具。完整原始字段见 traces.pretty.json，程序处理使用 traces.jsonl。',
           '“正常结束”只表示返回最终文本；工具调用成功、方案核验通过与独立评测正确是不同状态。',
           '## 任务导航']
    navigation = ['| 序号 | 任务 | 停止原因 | 工具调用 | 工具报错 | 未通过的方案核验 |',
                  '| --- | --- | --- | ---: | ---: | ---: |']
    for index, row in enumerate(results, 1):
        events = [e for e in row.get('trace', []) if e.get('event') == 'tool_result']
        failed = sum(e.get('executed', False) and (e.get('result') or {}).get('ok') is False for e in events)
        rejected = sum(tool_status(e) == '调用成功，方案未通过' for e in events)
        navigation.append(f'| [{index}](#task-{index}) | {table_cell(row.get("task_id"))} | '
                          f'{table_cell(row.get("stop_reason"))} | {row.get("tool_calls", 0)} | {failed} | {rejected} |')
    out.append('\n'.join(navigation))
    for index, row in enumerate(results, 1):
        out.extend([f'<a id="task-{index}"></a>', f'## 任务 {index}', '### 运行概览'])
        config = row.get('config') or {}
        backend = config.get('backend') or {}
        meta = {key: row.get(key) for key in ('task_id', 'kind', 'model_connected', 'stop_reason',
                'decisions', 'tool_calls', 'steps', 'elapsed_seconds', 'token_usage', 'token_usage_complete', 'cost')}
        meta['model'] = backend.get('model')
        meta['evaluation'] = row.get('evaluation')
        out.append(json_block(meta))
        out.extend(['### 用户请求', str((row.get('input') or {}).get('request', '（未记录）')),
                    '### 任务范围', json_block((row.get('input') or {}).get('scope', {})),
                    '<details><summary>展开业务规则、运行预算和工具定义</summary>\n',
                    json_block({'rules': (row.get('input') or {}).get('rules'), 'config': config}), '</details>\n',
                    '### 逐轮执行过程'])
        decision = None
        for event in row.get('trace', []):
            kind = event.get('event')
            if kind in ('model_input', 'model_output', 'model_error'):
                number = event.get('decision')
                if number != decision:
                    decision = number
                    out.append(f'#### 第 {decision} 轮')
            if kind == 'model_input':
                messages = event.get('messages') or []
                out.append(f'模型输入：当前累计 {len(messages)} 条消息。历史正文不在此重复，完整快照保留在 JSON 中。')
            elif kind == 'model_output':
                message = event.get('message') or {}
                if not isinstance(message, dict):
                    out.extend(['模型返回了异常消息结构：', json_block(message)])
                    continue
                if message.get('content'):
                    out.extend(['模型可见输出：', fenced(message['content'], 'text')])
                calls = message.get('tool_calls') or []
                out.append(f'本轮提出 {len(calls)} 个工具调用（由执行器依次处理）。' if calls else '本轮未提出工具调用。')
                for call in calls:
                    function = call.get('function') or {}
                    out.extend([f'待调用：`{table_cell(function.get("name"))}`；调用 ID：`{table_cell(call.get("id"))}`',
                                json_block(arguments_value(function.get('arguments')))])
                out.append('本轮 API 用量与尝试次数：')
                out.append(json_block({'usage': event.get('usage'), 'attempts': event.get('attempts')}))
            elif kind == 'tool_result':
                out.extend([f'##### 工具回执：{table_cell(event.get("tool"))} · {tool_status(event)}',
                            f'对应调用 ID：`{table_cell(event.get("tool_call_id"))}`；实际执行：{event.get("executed", False)}。',
                            '实际参数：', json_block(arguments_value(event.get('arguments'))),
                            '完整回执（不截断金额、证据或错误）：', json_block(event.get('result'))])
            elif kind == 'model_error':
                out.extend(['**模型调用失败**', json_block(event)])
            else:
                out.extend(['其他事件：', json_block(event)])
        out.extend(['### 最终回答', str(row.get('final_text') or '（未产生最终回答，请检查停止原因及最后一轮错误。）'),
                    '---'])
    return '\n\n'.join(out) + '\n'


def save_readable(output_dir, results):
    with (output_dir / 'traces.pretty.json').open('x', encoding='utf-8') as stream:
        json.dump(results, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with (output_dir / 'traces.md').open('x', encoding='utf-8') as stream:
        stream.write(render_trace(results))
