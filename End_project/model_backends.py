"""OpenAI兼容HTTP适配；scripted仅用于控制图烟测。"""
import copy
import json
import os
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

from agent_runtime import ModelError


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # 防止Authorization被重定向到其他地址。
        return None


class OpenAIBackend:
    kind = 'real_api'
    temperature = 0
    request_timeout = 30.0
    retries = 1

    def __init__(self, key, base_url, model, profile='base'):
        parsed = urllib.parse.urlsplit(base_url)
        if (parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or parsed.query or parsed.fragment):
            raise ValueError('OPENAI_BASE_URL必须是无用户密码、query和fragment的HTTP(S)地址')
        if parsed.scheme == 'http' and parsed.hostname not in ('127.0.0.1', 'localhost', '::1'):
            raise ValueError('远程API必须使用HTTPS；HTTP仅允许本机mock服务')
        if not key.strip() or not model.strip():
            raise ValueError('API密钥与模型名称不能为空')
        self._key, self.base_url, self.model, self.profile = key, base_url.rstrip('/'), model, profile

    @classmethod
    def from_env(cls, profile='base'):
        if profile not in ('base', 'sft'):
            raise ValueError('profile仅支持base/sft')
        names = ('OPENAI_API_KEY', 'OPENAI_BASE_URL', 'MODEL_NAME')
        prefix = 'SFT_' if profile == 'sft' else ''
        values = {name: os.environ.get(prefix + name, '').strip() for name in names}
        missing = [prefix + name for name, value in values.items() if not value]
        if missing:
            raise ValueError('缺少配置：' + ', '.join(missing) + '；未发送请求')
        return cls(values[names[0]], values[names[1]], values[names[2]], profile)

    def metadata(self):
        return {'model': self.model, 'profile': self.profile, 'base_url': self.base_url,
                'temperature': self.temperature, 'request_timeout_seconds': self.request_timeout,
                'retries': self.retries, 'trained_weights_verified': False,
                'thinking': 'disabled' if urllib.parse.urlsplit(self.base_url).hostname == 'api.deepseek.com' else 'provider_default'}

    def sanitize(self, value):
        # 整个输出递归去除当前密钥；不记录响应头/错误正文/环境变量全集。
        if isinstance(value, str):
            return value.replace(self._key, '[REDACTED]')
        if isinstance(value, list):
            return [self.sanitize(item) for item in value]
        if isinstance(value, dict):
            return {self.sanitize(key): self.sanitize(item) for key, item in value.items()}
        return value

    def complete(self, messages, schemas, deadline):
        body = {'model': self.model, 'messages': messages, 'tools': schemas,
                'tool_choice': 'auto', 'temperature': self.temperature, 'stream': False}
        if urllib.parse.urlsplit(self.base_url).hostname == 'api.deepseek.com':
            body['thinking'] = {'type': 'disabled'}
        payload = json.dumps(body).encode()
        opener = urllib.request.build_opener(NoRedirect())
        for attempt in range(self.retries + 1):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ModelError('DEADLINE_EXCEEDED')
            request = urllib.request.Request(self.base_url + '/chat/completions', data=payload,
                                            headers={'Content-Type': 'application/json',
                                                     'Authorization': 'Bearer ' + self._key}, method='POST')
            try:
                with opener.open(request, timeout=min(remaining, self.request_timeout)) as response:
                    # read1每次只读取当前可取得的数据，逐块检查绝对期限，避免滴流响应无限续期。
                    chunks, size = [], 0
                    while True:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise ModelError('DEADLINE_EXCEEDED')
                        response.fp.raw._sock.settimeout(min(remaining, self.request_timeout))
                        chunk = response.read1(min(65536, 8 * 1024 * 1024 + 1 - size))
                        if time.monotonic() >= deadline:
                            raise ModelError('DEADLINE_EXCEEDED')
                        if not chunk:
                            break
                        chunks.append(chunk)
                        size += len(chunk)
                        if size > 8 * 1024 * 1024:
                            raise ModelError('RESPONSE_TOO_LARGE')
                        if response.isclosed():
                            break
                    raw = b''.join(chunks)
                data = json.loads(raw)
                message = data['choices'][0]['message']
                return {'message': message, 'usage': data.get('usage'), 'attempts': attempt + 1}
            except urllib.error.HTTPError as exc:
                code = 'HTTP_' + str(exc.code)
                retryable = exc.code == 429 or 500 <= exc.code < 600
                exc.close()
            except (urllib.error.URLError, TimeoutError, socket.timeout, OSError):
                code, retryable = 'TRANSPORT_ERROR', True
            except (ValueError, KeyError, IndexError, TypeError, RecursionError):
                raise ModelError('INVALID_MODEL_RESPONSE') from None
            if not retryable or attempt == self.retries:
                raise ModelError(code, attempts=attempt + 1) from None
        raise ModelError('RETRY_EXHAUSTED')


class ScriptedBackend:
    """显式脚本消息队列；每题新建实例，不能用作模型能力或SFT轨迹。"""
    kind = 'scripted_mock'

    def __init__(self, messages):
        self._messages = iter(copy.deepcopy(messages))

    def metadata(self):
        return {'model': None, 'purpose': '仅测试控制图；不是训练轨迹', 'temperature': None,
                'request_timeout_seconds': None, 'retries': 0}

    def sanitize(self, value):
        return value

    def complete(self, messages, schemas, deadline):
        try:
            value = next(self._messages)
        except StopIteration:
            raise ModelError('SCRIPT_EXHAUSTED') from None
        if isinstance(value, str):
            raise ModelError(value)
        return {'message': value, 'usage': None, 'attempts': 1}


def tool_message(*calls):
    return {'role': 'assistant', 'content': None, 'tool_calls': [
        {'id': 'call_' + str(i), 'type': 'function', 'function': {
            'name': name, 'arguments': args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)}}
        for i, (name, args) in enumerate(calls)]}


class SmokeBackend(ScriptedBackend):
    """仅检查已加载任务的查询回路，不宣称完成该任务对账。"""
    def __init__(self):
        super().__init__([
            tool_message(('query_orders', {})),
            tool_message(('search_receipts', {})),
            {'role': 'assistant', 'content': '脚本烟测已读取订单和收款回执；未进行模型推理或业务正确性评分。'},
        ])
