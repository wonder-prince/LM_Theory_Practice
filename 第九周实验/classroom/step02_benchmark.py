# 教学说明：本文件用于Step 02：在严格相同设置下测量速度、显存和回答区困惑度。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 02：在严格相同设置下测量速度、显存和回答区困惑度。"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
from pathlib import Path

import torch
import bitsandbytes as bnb

from quant_utils import (
    OUTPUT_DIR,
    MIXED_FP16_MODULES,
    VAL_PATH,
    cuda_memory,
    load_tokenizer,
    load_tuned_model,
    model_footprint_mib,
    reset_cuda_peak,
    result_name,
    set_seed,
    synchronize,
    write_json,
)

PROMPTS = [
    "### 指令\n用通俗语言解释过拟合，并给出一个缓解方法。\n### 回答\n",
    "### 指令\n学生说：训练损失下降但验证损失上升。请诊断原因。\n### 回答\n",
    "### 指令\n比较学习率过大和过小时训练曲线的典型表现。\n### 回答\n",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="受控评测 FP16/NF4/FP4/混合精度模型")
    parser.add_argument("--mode", choices=["fp16", "nf4", "fp4", "mixed"], required=True)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--validation-limit", type=int, default=50)
    parser.add_argument("--max-length", type=int, default=192)
    return parser.parse_args()


def load_validation(limit: int) -> list[dict]:
    """按顺序读取指定数量的验证样本。"""
    items = []
    with VAL_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                items.append(json.loads(line))
            if len(items) >= limit:
                break
    return items


def format_prompt(item: dict) -> str:
    """把 JSON 样本转换成与微调阶段一致的指令模板。"""
    text = f"### 指令\n{item['instruction']}\n"
    if item.get("input"):
        text += f"### 输入\n{item['input']}\n"
    return text + "### 回答\n"


def answer_only_loss(model, tokenizer, items: list[dict], max_length: int) -> tuple[float, float, int]:
    """只累计参考回答 token 的负对数似然，并计算困惑度。"""
    total_nll = 0.0
    total_tokens = 0
    device = next(model.parameters()).device
    with torch.inference_mode():
        for item in items:
            prompt = format_prompt(item)
            full = prompt + item["output"]
            encoded = tokenizer(full, truncation=True, max_length=max_length, return_tensors="pt").to(device)
            prompt_len = len(tokenizer(prompt, truncation=True, max_length=max_length).input_ids)
            labels = encoded.input_ids.clone()
            # -100 表示提示词区域不参与 loss，只评价参考回答区域。
            labels[:, : min(prompt_len, labels.shape[1])] = -100
            outputs = model(**encoded, labels=labels)
            count = int((labels[:, 1:] != -100).sum().item())
            total_nll += outputs.loss.item() * count
            total_tokens += count
    average = total_nll / max(total_tokens, 1)
    return average, math.exp(min(average, 30)), total_tokens


def generate_once(model, tokenizer, prompt: str, max_new_tokens: int) -> tuple[str, int, float]:
    """完成一次受控生成，返回回答、生成 token 数和耗时。"""
    encoded = tokenizer(prompt, return_tensors="pt").to("cuda")
    synchronize()
    started = time.perf_counter()
    with torch.inference_mode():
        output = model.generate(
            **encoded, max_new_tokens=max_new_tokens, do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    synchronize()
    elapsed = time.perf_counter() - started
    new_ids = output[0, encoded.input_ids.shape[1]:]
    text = tokenizer.decode(new_ids, skip_special_tokens=True).strip()
    return text, int(new_ids.numel()), elapsed


def main() -> int:
    args = parse_args()
    set_seed(args.seed)
    tokenizer = load_tokenizer()
    model, load_seconds = load_tuned_model(args.mode)
    # 正式计时前先核验 4-bit 层、LoRA 和 mixed 保留的 FP16 模块数量。
    linear4 = sum(isinstance(module, bnb.nn.Linear4bit) for module in model.modules())
    lora_modules = sum("lora_A" in name for name, _ in model.named_modules())
    module_map = dict(model.named_modules())
    mixed_fp16_modules = []
    for expected_name in MIXED_FP16_MODULES:
        matches = [
            module for name, module in module_map.items()
            if name.endswith(expected_name)
        ]
        if matches and all(not isinstance(module, bnb.nn.Linear4bit) for module in matches):
            mixed_fp16_modules.append(expected_name)

    for _ in range(args.warmup):
        # 预热结果不计入统计，避免首次 CUDA 初始化影响速度。
        generate_once(model, tokenizer, PROMPTS[0], args.max_new_tokens)
    reset_cuda_peak()

    runs = []
    final_answers = {}
    for prompt_index, prompt in enumerate(PROMPTS):
        for repeat in range(args.repeats):
            text, tokens, elapsed = generate_once(model, tokenizer, prompt, args.max_new_tokens)
            runs.append({
                "prompt_index": prompt_index,
                "repeat": repeat + 1,
                "generated_tokens": tokens,
                "seconds": elapsed,
                "tokens_per_second": tokens / elapsed,
            })
            final_answers[str(prompt_index)] = text

    memory_after_generation = cuda_memory()
    items = load_validation(args.validation_limit)
    loss, ppl, answer_tokens = answer_only_loss(model, tokenizer, items, args.max_length)
    seconds = [r["seconds"] for r in runs]
    speeds = [r["tokens_per_second"] for r in runs]
    report = {
        "checkpoint": "PASS",
        "mode": args.mode,
        "verification": {
            "linear4bit_modules": linear4,
            "lora_A_modules": lora_modules,
            "mixed_fp16_modules": mixed_fp16_modules,
        },
        "control": {
            "same_adapter": True,
            "seed": args.seed,
            "max_new_tokens": args.max_new_tokens,
            "warmup": args.warmup,
            "repeats_per_prompt": args.repeats,
            "prompt_count": len(PROMPTS),
            "do_sample": False,
            "cuda_synchronize": True,
            "validation_samples": len(items),
            "max_length": args.max_length,
        },
        "load_seconds": round(load_seconds, 4),
        "model_footprint_mib": model_footprint_mib(model),
        "cuda_memory_after_generation": memory_after_generation,
        "generation": {
            "median_latency_seconds": round(statistics.median(seconds), 5),
            "median_tokens_per_second": round(statistics.median(speeds), 3),
            "runs": runs,
            "answers": final_answers,
        },
        "validation": {
            "answer_only_loss": round(loss, 6),
            "answer_only_perplexity": round(ppl, 4),
            "answer_tokens": answer_tokens,
        },
    }
    name = result_name(args.mode)
    out = OUTPUT_DIR / f"step02_benchmark_{name}.json"
    write_json(out, report)
    print(f"核验：4-bit 线性层={linear4}；LoRA A 模块={lora_modules}；混合精度保留FP16={len(mixed_fp16_modules)}")
    print(f"模式：{name}；模型占用：{report['model_footprint_mib']:.2f} MiB")
    print(f"中位延迟：{report['generation']['median_latency_seconds']:.5f} s")
    print(f"中位速度：{report['generation']['median_tokens_per_second']:.3f} token/s")
    print(f"回答区 loss={loss:.6f}，perplexity={ppl:.4f}")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
