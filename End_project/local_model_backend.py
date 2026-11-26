"""用官方 Transformers 模板在单张 CUDA GPU 上执行 Qwen3 4bit 推理。"""
import json
import logging
from pathlib import Path
import re
import time
import uuid

from agent_runtime import ModelError

LOGGER = logging.getLogger(__name__)


def parse_tool_output(text):
    blocks = re.findall(r'<tool_call>\s*(.*?)\s*</tool_call>', text, flags=re.DOTALL)
    if text.count('<tool_call>') != len(blocks) or text.count('</tool_call>') != len(blocks):
        raise ModelError('INCOMPLETE_LOCAL_TOOL_CALL')
    calls = []
    for block in blocks:
        try:
            item = json.loads(block)
            if not isinstance(item, dict) or not isinstance(item.get('name'), str) or not item['name']:
                raise ValueError('invalid name')
            args = item['arguments']
            if isinstance(args, str):
                args = json.loads(args)
            if not isinstance(args, dict):
                raise ValueError('invalid arguments')
        except (ValueError, TypeError, KeyError):
            raise ModelError('INVALID_LOCAL_TOOL_CALL') from None
        calls.append({'id': 'local_' + uuid.uuid4().hex, 'type': 'function',
                      'function': {'name': item['name'], 'arguments': json.dumps(args, ensure_ascii=False)}})
    content = re.sub(r'<tool_call>.*?</tool_call>', '', text, flags=re.DOTALL).strip()
    message = {'role': 'assistant', 'content': content or None}
    if calls:
        message['tool_calls'] = calls
    return message


class LocalQwenBackend:
    kind = 'local_transformers'

    def __init__(self, model_dir, max_context=8192, max_new_tokens=1024):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        self.model_dir = Path(model_dir).resolve()
        self.max_context, self.max_new_tokens = max_context, max_new_tokens
        if not torch.cuda.is_available():
            raise RuntimeError('CUDA 不可用，请先验证 GPU 环境')
        if not torch.cuda.is_bf16_supported():
            raise RuntimeError('当前 GPU 不支持本入口使用的 BF16 计算')
        # 推理计算在 GPU 上，限制 CPU 线程占用。
        torch.set_num_threads(4)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir, local_files_only=True)
        config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                                   bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_dir, local_files_only=True, quantization_config=config,
            torch_dtype=torch.bfloat16, device_map={'': 0}, attn_implementation='sdpa')
        self.model.eval()
        # 本入口使用贪心解码，清除权重附带的采样参数以避免逐轮警告。
        for key in ('temperature', 'top_p', 'top_k'):
            setattr(self.model.generation_config, key, None)
        torch.cuda.reset_peak_memory_stats()

    def metadata(self):
        import torch
        return {'model': 'Qwen/Qwen3-4B-Instruct-2507', 'model_dir': str(self.model_dir),
                'quantization': 'NF4 double quantization', 'compute_dtype': 'bfloat16',
                'gpu': torch.cuda.get_device_name(0), 'temperature': 0,
                'torch_version': torch.__version__, 'cuda_version': torch.version.cuda,
                'cpu_threads': torch.get_num_threads(),
                'max_context': self.max_context, 'max_new_tokens': self.max_new_tokens,
                'peak_allocated_mib': round(torch.cuda.max_memory_allocated() / 1024**2, 2),
                'trained_weights_verified': False}

    def sanitize(self, value):
        return value

    def close(self):
        """Release this worker's model; exiting the worker also destroys its CUDA context."""
        import gc
        import torch

        self.model = None
        self.tokenizer = None
        gc.collect()
        torch.cuda.empty_cache()
        return {'status': 'closed', 'allocated_after_close_mib':
                round(torch.cuda.memory_allocated() / 1024**2, 2)}

    def complete(self, messages, schemas, deadline):
        import torch
        from transformers import StoppingCriteria, StoppingCriteriaList

        if time.monotonic() >= deadline:
            raise ModelError('DEADLINE_EXCEEDED')
        text = self.tokenizer.apply_chat_template(messages, tools=schemas, tokenize=False,
                                                 add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors='pt').to('cuda')
        prompt_tokens = inputs.input_ids.shape[1]
        available = self.max_context - prompt_tokens
        if available <= 0:
            raise ModelError('LOCAL_CONTEXT_LIMIT')
        started = time.monotonic()
        LOGGER.info('开始生成：输入 %s tokens，输出预算 %s tokens',
                    prompt_tokens, min(available, self.max_new_tokens))

        class Deadline(StoppingCriteria):
            def __call__(self, input_ids, scores, **kwargs):
                return time.monotonic() >= deadline

        try:
            with torch.inference_mode():
                generated = self.model.generate(
                    **inputs, max_new_tokens=min(available, self.max_new_tokens), do_sample=False,
                    pad_token_id=self.tokenizer.pad_token_id,
                    stopping_criteria=StoppingCriteriaList([Deadline()]))
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            raise ModelError('CUDA_OUT_OF_MEMORY') from None
        if time.monotonic() >= deadline:
            raise ModelError('DEADLINE_EXCEEDED')
        output = generated[0, prompt_tokens:]
        eos_ids = self.model.generation_config.eos_token_id
        eos_ids = eos_ids if isinstance(eos_ids, list) else [eos_ids]
        if len(output) >= min(available, self.max_new_tokens) and int(output[-1]) not in eos_ids:
            raise ModelError('LOCAL_OUTPUT_LIMIT')
        decoded = self.tokenizer.decode(output, skip_special_tokens=True)
        message = parse_tool_output(decoded)
        LOGGER.info('生成完成：输出 %s tokens，%.2f 秒，%s 个工具调用',
                    len(output), time.monotonic() - started, len(message.get('tool_calls', [])))
        return {'message': message, 'usage': {'prompt_tokens': prompt_tokens,
                'completion_tokens': len(output), 'total_tokens': prompt_tokens + len(output)}, 'attempts': 1}
