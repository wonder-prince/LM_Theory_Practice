"""Step 06：测量 Automatic Prefix Caching 对重复长前缀 TTFT 的影响。"""

from __future__ import annotations

import argparse
import json
import statistics
import time

import requests

from course_paths import API_BASE, LORA_MODEL_NAME, OUTPUT_DIR, write_json


# 这些内容在每个请求中完全相同，用来模拟课程助教、RAG 或智能体的长系统提示词。
# 问题放在共享前缀之后并保持不同，避免把实验退化为重复发送完全相同的请求。
PREFIX_UNIT = (
    "你是大模型课程的学习伴侣。回答时先说明核心概念，再给出一个简短例子，"
    "最后指出常见误区。不得编造实验结果；遇到不确定信息时应明确说明。"
    "课程内容包括注意力机制、量化、LoRA、数据清洗、模型评估和推理服务。"
)
# 重复13次后，实际聊天模板约为790个prompt token；既足够放大Prefill差异，
# 又能和16个输出token一起落在本实验的1024-token上下文限制内。
SHARED_SYSTEM_PROMPT = "\n".join(PREFIX_UNIT for _ in range(13))
QUESTIONS = [
    "什么是token？",
    "为什么需要验证集？",
    "LoRA为什么能减少可训练参数？",
    "4-bit量化主要节省什么资源？",
    "KV Cache保存了什么？",
    "TTFT表示什么？",
    "连续批处理为什么能提高吞吐量？",
    "PagedAttention解决了什么问题？",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vLLM Automatic Prefix Caching实验")
    parser.add_argument("--label", choices=("apc_off", "apc_on"))
    parser.add_argument(
        "--compare",
        action="store_true",
        help="读取apc_off与apc_on的JSON并输出对比，不发送新请求。",
    )
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=180)
    return parser.parse_args()


def stream_once(question: str, max_tokens: int, timeout: float) -> dict:
    """发送一个流式请求，记录首token时间；TTFT最能反映Prefill是否被复用。"""
    payload = {
        # APC 必须在同一模型入口下复用完全相同的 token 前缀。
        "model": LORA_MODEL_NAME,
        "messages": [
            {"role": "system", "content": SHARED_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        # 关闭随机采样，使两组实验的生成路径尽量一致。
        "temperature": 0.0,
        "seed": 42,
        # 输出保持很短，让测量重点落在 Prefill 和 TTFT。
        "max_tokens": max_tokens,
        "ignore_eos": True,
        # 流式返回用于准确记录首 token 到达时间。
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    started = time.perf_counter()
    first_token_at = None
    usage = None

    with requests.post(
        f"{API_BASE}/v1/chat/completions",
        json=payload,
        stream=True,
        timeout=timeout,
    ) as response:
        response.raise_for_status()
        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line or not raw_line.startswith("data: "):
                continue
            data = raw_line[6:]
            if data == "[DONE]":
                break
            event = json.loads(data)
            if event.get("usage"):
                usage = event["usage"]
            choices = event.get("choices") or []
            content = ((choices[0].get("delta") or {}).get("content") or "") if choices else ""
            if content and first_token_at is None:
                first_token_at = time.perf_counter()

    finished = time.perf_counter()
    if first_token_at is None or usage is None:
        raise RuntimeError("没有收到有效流式token或usage。")
    return {
        "question": question,
        "prompt_tokens": int(usage["prompt_tokens"]),
        "completion_tokens": int(usage["completion_tokens"]),
        "ttft_ms": round((first_token_at - started) * 1000, 3),
        "e2e_ms": round((finished - started) * 1000, 3),
    }


def run_measurement(label: str, max_tokens: int, timeout: float) -> int:
    # 使用不含共享长前缀的短请求完成CUDA预热，避免污染待测前缀缓存。
    warmup_payload = {
        "model": LORA_MODEL_NAME,
        "messages": [{"role": "user", "content": "只回答：预热完成"}],
        "temperature": 0.0,
        "max_tokens": 4,
    }
    warmup = requests.post(
        f"{API_BASE}/v1/chat/completions", json=warmup_payload, timeout=timeout
    )
    warmup.raise_for_status()

    # 顺序发送：首个请求建立前缀缓存，后七个请求测试重复前缀命中。
    results = [stream_once(q, max_tokens, timeout) for q in QUESTIONS]
    first = results[0]
    repeated = results[1:]
    summary = {
        "requests": len(results),
        "prompt_tokens": first["prompt_tokens"],
        "first_ttft_ms": first["ttft_ms"],
        "repeat_ttft_median_ms": round(
            statistics.median(item["ttft_ms"] for item in repeated), 3
        ),
        "repeat_e2e_median_ms": round(
            statistics.median(item["e2e_ms"] for item in repeated), 3
        ),
    }
    report = {
        "checkpoint": "PASS",
        "label": label,
        "api_base": API_BASE,
        "model": LORA_MODEL_NAME,
        "protocol": {
            "shared_system_prefix": True,
            "sequential_requests": True,
            "unrelated_warmup": True,
            "fixed_max_tokens": max_tokens,
        },
        "summary": summary,
        "raw_requests": results,
    }
    out = OUTPUT_DIR / f"step06_{label}.json"
    write_json(out, report)

    print(f"label: {label}")
    print(f"requests/prompt tokens: {len(results)}/{summary['prompt_tokens']}")
    print(f"first TTFT: {summary['first_ttft_ms']:.3f} ms")
    print(f"repeat TTFT median: {summary['repeat_ttft_median_ms']:.3f} ms")
    print(f"repeat E2E median: {summary['repeat_e2e_median_ms']:.3f} ms")
    print("PASS step06 prefix cache measurement")
    print(f"完整报告已写入：{out}")
    return 0


def compare_reports() -> int:
    # 汇总阶段只读取关闭组和开启组的 JSON，不再次调用模型。
    off = json.loads((OUTPUT_DIR / "step06_apc_off.json").read_text(encoding="utf-8"))
    on = json.loads((OUTPUT_DIR / "step06_apc_on.json").read_text(encoding="utf-8"))
    off_ttft = float(off["summary"]["repeat_ttft_median_ms"])
    on_ttft = float(on["summary"]["repeat_ttft_median_ms"])
    reduction = (off_ttft - on_ttft) / off_ttft * 100 if off_ttft else 0.0
    report = {
        "checkpoint": "PASS",
        "apc_off_repeat_ttft_median_ms": off_ttft,
        "apc_on_repeat_ttft_median_ms": on_ttft,
        "ttft_reduction_percent": round(reduction, 2),
    }
    out = OUTPUT_DIR / "step06_apc_comparison.json"
    write_json(out, report)
    print(f"APC off repeat TTFT median: {off_ttft:.3f} ms")
    print(f"APC on repeat TTFT median: {on_ttft:.3f} ms")
    print(f"TTFT reduction: {reduction:.2f}%")
    print("PASS step06 prefix cache comparison")
    return 0


def main() -> int:
    args = parse_args()
    if args.compare:
        return compare_reports()
    if args.label is None:
        raise ValueError("测量时必须指定--label apc_off或--label apc_on。")
    return run_measurement(args.label, args.max_tokens, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
