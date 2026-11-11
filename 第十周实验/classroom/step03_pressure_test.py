# 教学说明：本文件用于Step 03：对真实 vLLM 服务执行单个并发级别的流式压力测试。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 03：对真实 vLLM 服务执行单个并发级别的流式压力测试。"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from course_paths import API_BASE, LORA_MODEL_NAME, OUTPUT_DIR, write_json

PROMPTS = [
    "解释过拟合并给出一种缓解方法。",
    "说明 LoRA 为什么能够减少可训练参数。",
    "比较 FP16 与 4-bit 量化的主要取舍。",
    "什么是验证集，它为什么不能替代测试集？",
    "解释学习率过大时训练曲线可能出现的现象。",
    "说明连续批处理可能提高吞吐量的原因。",
    "区分推理服务的延迟与吞吐量。",
    "解释 KV cache 在自回归推理中的作用。",
]


def percentile(values: list[float], q: float) -> float:
    """使用线性插值计算分位数，q=0.95 即 p95。"""
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vLLM 单级并发压力测试")
    parser.add_argument("--concurrency", type=int, required=True)
    parser.add_argument("--requests", type=int, default=16)
    parser.add_argument("--max-tokens", type=int, default=32)
    parser.add_argument("--label", required=True, help="例如 baseline_c1 或 tuned_c8")
    parser.add_argument("--timeout", type=float, default=180)
    return parser.parse_args()


def send_one(prompt: str, max_tokens: int, timeout: float) -> dict:
    payload = {
        # 所有压力请求统一调用同一个 LoRA 模型入口。
        "model": LORA_MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        # 性能实验关闭随机采样，使不同并发级别的生成条件尽量一致。
        "temperature": 0.0,
        "seed": 42,
        # 由命令行 --max-tokens 控制每个请求最多新增的 token 数。
        "max_tokens": max_tokens,
        "ignore_eos": True,  # 固定输出长度，避免不同结束位置干扰吞吐量比较。
        # 流式返回用于分别记录首 token 和最后一个 token 的时间。
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    started = time.perf_counter()
    first_token_at = None
    last_token_at = None
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
            if choices and ((choices[0].get("delta") or {}).get("content") or ""):
                now = time.perf_counter()
                first_token_at = first_token_at or now
                last_token_at = now

    finished = time.perf_counter()
    if first_token_at is None or usage is None:
        raise RuntimeError("压力请求没有收到有效 token 或 usage。")

    output_tokens = int(usage["completion_tokens"])
    ttft_ms = (first_token_at - started) * 1000
    e2e_ms = (finished - started) * 1000
    tpot_ms = 0.0
    if output_tokens > 1 and last_token_at is not None:
        tpot_ms = (last_token_at - first_token_at) * 1000 / (output_tokens - 1)
    return {
        "prompt_tokens": int(usage["prompt_tokens"]),
        "output_tokens": output_tokens,
        "ttft_ms": round(ttft_ms, 3),
        "tpot_ms": round(tpot_ms, 3),
        "e2e_latency_ms": round(e2e_ms, 3),
    }


def main() -> int:
    args = parse_args()
    if args.concurrency < 1 or args.requests < args.concurrency:
        raise ValueError("concurrency 至少为 1，requests 不能小于 concurrency。")

    # 两次预热不进入统计，避免首次编译和 CUDA 初始化抬高正式结果。
    for i in range(2):
        send_one(PROMPTS[i], args.max_tokens, args.timeout)

    started = time.perf_counter()
    results = []
    # 每个工作线程模拟一个闭环客户端：收到本次响应后才继续领取下一项任务。
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [
            pool.submit(
                send_one,
                PROMPTS[i % len(PROMPTS)],
                args.max_tokens,
                args.timeout,
            )
            for i in range(args.requests)
        ]
        for future in as_completed(futures):
            results.append(future.result())
    wall_seconds = time.perf_counter() - started

    ttfts = [item["ttft_ms"] for item in results]
    tpots = [item["tpot_ms"] for item in results]
    e2es = [item["e2e_latency_ms"] for item in results]
    output_tokens = sum(item["output_tokens"] for item in results)
    summary = {
        "concurrency": args.concurrency,
        "requests": args.requests,
        "wall_seconds": round(wall_seconds, 5),
        "request_throughput_rps": round(args.requests / wall_seconds, 4),
        "output_throughput_tokens_per_second": round(output_tokens / wall_seconds, 3),
        "ttft_p50_ms": round(percentile(ttfts, 0.50), 3),
        "ttft_p95_ms": round(percentile(ttfts, 0.95), 3),
        "tpot_p50_ms": round(percentile(tpots, 0.50), 3),
        "e2e_p50_ms": round(percentile(e2es, 0.50), 3),
        "e2e_p95_ms": round(percentile(e2es, 0.95), 3),
        "mean_output_tokens": round(statistics.mean(item["output_tokens"] for item in results), 3),
    }
    report = {
        "checkpoint": "PASS",
        "label": args.label,
        "api_base": API_BASE,
        "model": LORA_MODEL_NAME,
        "protocol": {
            "closed_loop_clients": True,
            "warmup_requests": 2,
            "fixed_max_tokens": args.max_tokens,
            "ignore_eos": True,
            "same_prompt_pool": True,
        },
        "summary": summary,
        "raw_requests": results,
    }
    out = OUTPUT_DIR / f"step03_{args.label}.json"
    write_json(out, report)

    print(f"label: {args.label}")
    print(f"concurrency/requests: {args.concurrency}/{args.requests}")
    print(
        "throughput: "
        f"{summary['request_throughput_rps']:.4f} req/s, "
        f"{summary['output_throughput_tokens_per_second']:.3f} output token/s"
    )
    print(
        "TTFT: "
        f"p50={summary['ttft_p50_ms']:.3f} ms, "
        f"p95={summary['ttft_p95_ms']:.3f} ms"
    )
    print(f"TPOT: p50={summary['tpot_p50_ms']:.3f} ms/token")
    print(
        "E2E: "
        f"p50={summary['e2e_p50_ms']:.3f} ms, "
        f"p95={summary['e2e_p95_ms']:.3f} ms"
    )
    print("PASS step03 vLLM pressure test")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
