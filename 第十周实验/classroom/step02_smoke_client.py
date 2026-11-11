# 教学说明：本文件用于Step 02：调用 vLLM 的 OpenAI 兼容接口，输出完整回答并测量一次请求。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 02：调用 vLLM 的 OpenAI 兼容接口，输出完整回答并测量一次请求。"""

from __future__ import annotations

import json
import time

import requests

from course_paths import API_BASE, LORA_MODEL_NAME, OUTPUT_DIR, write_json

QUESTION = "你是谁"


def stream_chat(question: str) -> dict:
    payload = {
        # vLLM 把启动时挂载的 LoRA 名称作为可调用的模型名称。
        "model": LORA_MODEL_NAME,
        # messages 是聊天上下文；服务端还会套用 Qwen 的聊天模板和控制 token。
        "messages": [{"role": "user", "content": question}],
        # 冒烟测试重在复现与计时，关闭随机采样，避免回答波动干扰比较。
        "temperature": 0.0,
        "seed": 42,
        # 最多新增 64 个输出 token，不包含输入提示词所占的 token。
        "max_tokens": 64,
        # 流式返回可记录第一个输出 token 到达的时刻。
        "stream": True,
        # 最后一条流式事件返回 prompt_tokens 和 completion_tokens。
        "stream_options": {"include_usage": True},
    }

    started = time.perf_counter()
    first_token_at = None
    last_token_at = None
    answer_parts: list[str] = []
    usage = None

    with requests.post(
        f"{API_BASE}/v1/chat/completions",
        json=payload,
        stream=True,
        timeout=180,
    ) as response:
        # HTTP 状态不是 2xx 时立即抛出异常，避免把错误页面当作模型输出。
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
            if not choices:
                continue
            content = (choices[0].get("delta") or {}).get("content") or ""
            if content:
                now = time.perf_counter()
                first_token_at = first_token_at or now
                last_token_at = now
                answer_parts.append(content)

    finished = time.perf_counter()
    if first_token_at is None or usage is None:
        raise RuntimeError("没有收到有效的流式 token 或 usage，请检查 vLLM 服务端日志。")

    output_tokens = int(usage["completion_tokens"])
    ttft_ms = (first_token_at - started) * 1000
    e2e_ms = (finished - started) * 1000
    # TPOT 不包含首 token；只生成一个 token 时没有后续间隔，因此记为 0。
    tpot_ms = 0.0
    if output_tokens > 1 and last_token_at is not None:
        tpot_ms = (last_token_at - first_token_at) * 1000 / (output_tokens - 1)

    return {
        "question": question,
        "answer": "".join(answer_parts).strip(),
        "prompt_tokens": int(usage["prompt_tokens"]),
        "completion_tokens": output_tokens,
        "ttft_ms": round(ttft_ms, 3),
        "tpot_ms": round(tpot_ms, 3),
        "e2e_latency_ms": round(e2e_ms, 3),
    }


def main() -> int:
    # 先读取服务暴露的模型列表，确认 LoRA 已经成功挂载。
    models_response = requests.get(f"{API_BASE}/v1/models", timeout=30)
    models_response.raise_for_status()
    model_ids = [item["id"] for item in models_response.json()["data"]]
    if LORA_MODEL_NAME not in model_ids:
        raise RuntimeError(f"模型列表中没有 {LORA_MODEL_NAME}：{model_ids}")

    result = stream_chat(QUESTION)
    report = {"checkpoint": "PASS", "available_models": model_ids, **result}
    out = OUTPUT_DIR / "step02_smoke.json"
    write_json(out, report)

    print(f"available models: {', '.join(model_ids)}")
    print(f"user: {result['question']}")
    print(f"assistant: {result['answer']}")
    print(
        "usage: "
        f"prompt={result['prompt_tokens']}, completion={result['completion_tokens']}"
    )
    print(
        "latency: "
        f"TTFT={result['ttft_ms']:.3f} ms, "
        f"TPOT={result['tpot_ms']:.3f} ms, "
        f"E2E={result['e2e_latency_ms']:.3f} ms"
    )
    print("PASS step02 vLLM smoke test")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
