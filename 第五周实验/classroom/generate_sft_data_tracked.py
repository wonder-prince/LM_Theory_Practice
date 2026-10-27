# 教学说明：本文件用于第五周包装脚本：不改动 generate_sft_data.py，额外记录耗时与 API token 用量/费用。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""第五周包装脚本：不改动 generate_sft_data.py，额外记录耗时与 API token 用量/费用。

用法与原脚本一致，把脚本名换成 generate_sft_data_tracked.py 即可：

    python -s .\\classroom\\generate_sft_data_tracked.py \
        --count 500 --skill course_learning_companion \
        --thinking --reasoning-effort high \
        --output .\\data\\course_learning_500_pro_high.jsonl

说明：
- 它把原始 generate_sft_data.main() 原样跑一遍（复用其全部逻辑），只在其外层
  监听每次 HTTP 响应的 usage 字段并计时，因此不修改任何原始代码。
- 可选费用估算（元/百万 token），不配置则只记录 token 用量：
      $env:COMMERCIAL_API_PRICE_IN = "2"
      $env:COMMERCIAL_API_PRICE_OUT = "8"
- 运行结束后会把耗时、token 用量与费用补写进原脚本生成的 manifest。
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

import generate_sft_data as g  # 复用原脚本，不修改它


# 1. 在外层监听每次 API 调用的响应，用于累计 usage。
_captured: list = []
_orig_post = requests.post


def _tracked_post(*args, **kwargs):
    response = _orig_post(*args, **kwargs)
    _captured.append(response)
    return response


requests.post = _tracked_post


def _parse_price(name: str) -> float | None:
    text = os.environ.get(name, "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        print(f"[tracked] 警告：{name} 不是合法数字，忽略费用估算：{text}")
        return None


def _summarize() -> dict:
    prompt_tokens = completion_tokens = total_tokens = 0
    usage_calls = 0
    for response in _captured:
        if not response.ok:
            continue
        try:
            usage = response.json().get("usage") or {}
        except Exception:
            continue
        if usage:
            usage_calls += 1
            prompt_tokens += int(usage.get("prompt_tokens") or 0)
            completion_tokens += int(usage.get("completion_tokens") or 0)
            total_tokens += int(usage.get("total_tokens") or 0)

    price_in = _parse_price("COMMERCIAL_API_PRICE_IN")
    price_out = _parse_price("COMMERCIAL_API_PRICE_OUT")
    estimated_cost = None
    if price_in is not None and price_out is not None:
        estimated_cost = round(
            prompt_tokens / 1_000_000 * price_in + completion_tokens / 1_000_000 * price_out,
            6,
        )
    return {
        "usage_calls": usage_calls,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "price_cny_per_million": {"prompt": price_in, "completion": price_out},
        "estimated_cost_cny": estimated_cost,
    }


def _augment_manifest(extra: dict) -> None:
    candidates = sorted(
        g.OUTPUT_DIR.glob("*_manifest.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        print("[tracked] 未找到原脚本生成的 manifest，跳过补写。")
        return
    path = candidates[0]
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(extra)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[tracked] 已把耗时/token/费用补写进: {path}")


def main() -> None:
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    try:
        g.main()  # 原脚本完整逻辑，参数、输出、manifest 行为完全不变
    finally:
        elapsed = time.perf_counter() - started
        finished_at = datetime.now(timezone.utc).isoformat()
        summary = _summarize()

        print("\n[tracked] 汇总")
        print(f"[tracked] started_at: {started_at}")
        print(f"[tracked] finished_at: {finished_at}")
        print(f"[tracked] elapsed: {elapsed:.2f}s")
        print(
            f"[tracked] tokens: prompt={summary['prompt_tokens']}, "
            f"completion={summary['completion_tokens']}, total={summary['total_tokens']}"
        )
        if summary["estimated_cost_cny"] is not None:
            print(f"[tracked] estimated cost: {summary['estimated_cost_cny']:.4f} 元")
        else:
            print("[tracked] estimated cost: 未配置 COMMERCIAL_API_PRICE_IN/OUT，仅记录 token 用量")

        _augment_manifest(
            {
                "tracked_started_at": started_at,
                "tracked_finished_at": finished_at,
                "tracked_elapsed_seconds": round(elapsed, 2),
                "tracked_usage": summary,
            }
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"[tracked] ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
