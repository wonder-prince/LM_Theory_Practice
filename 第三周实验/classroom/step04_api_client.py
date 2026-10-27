"""Step 04：调用已经启动的本地 OpenAI 兼容 API。

先在第一个 VS Code 终端运行 classroom/start_local_api.ps1；再在第二个终端
运行本脚本。客户端只发送 HTTP JSON，不直接加载 GGUF，因此不会占第二份显存。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests


# 客户端只需要知道服务地址和结果保存位置，不需要知道 GGUF 文件路径。
PROJECT_DIR = Path(__file__).resolve().parents[1]
BASE_URL = "http://127.0.0.1:18080"
OUTPUT_PATH = PROJECT_DIR / "outputs" / "step04_api_response.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--details",
        action="store_true",
        help="额外显示模型列表、HTTP 状态和 token usage",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("[Step 04] 本地 API 交互演示")

    # GET /v1/models 用于确认服务存在，并查看服务器暴露的模型名称。
    model_reply = requests.get(f"{BASE_URL}/v1/models", timeout=20)
    model_reply.raise_for_status()
    models = model_reply.json()
    model_id = models["data"][0]["id"]

    # payload 的结构与 OpenAI Chat Completions 接口一致：指定模型、消息和生成参数。
    # system 负责设定身份，user 是本次通过 HTTP 发送给服务器的问题。
    question = "请用一句话解释本地大模型 API 的作用，并在回答中包含‘本地 API’。"
    payload = {
        "model": "qwen2.5-7b-local",
        "messages": [
            {"role": "system", "content": "你是部署在本机的中文课程助教。"},
            {
                "role": "user",
                "content": question,
            },
        ],
        "max_tokens": 96,
        "temperature": 0.1,
        "seed": 42,
    }

    started = time.perf_counter()
    # POST 请求只传输 JSON；真正的模型推理发生在另一个终端中的本地服务器进程。
    reply = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        json=payload,
        timeout=180,
    )
    elapsed = time.perf_counter() - started
    reply.raise_for_status()
    # raise_for_status 会在 4xx/5xx 时立即报错；成功后再解析 JSON 与回答文本。
    response = reply.json()
    answer = response["choices"][0]["message"]["content"].strip()
    if not answer:
        raise RuntimeError("API 返回的回答为空，演示检查失败。")

    print(f"service: READY ({model_id})")
    print(f"user: {question}")
    print(f"assistant: {answer}")
    print(f"request time: {elapsed:.2f} s")
    if args.details:
        print("GET /v1/models ->", json.dumps(models, ensure_ascii=False))
        print("status:", reply.status_code)
        print("usage:", response.get("usage", {}))

    # 同时保存请求和完整响应，便于观察 API 字段，而不只保留最终一句回答。
    record = {
        "base_url": BASE_URL,
        "models": models,
        "request": payload,
        "response": response,
        "request_seconds": round(elapsed, 2),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {OUTPUT_PATH.relative_to(PROJECT_DIR)}")
    print("checkpoint: PASS（客户端通过 localhost API 获得模型回答）")


if __name__ == "__main__":
    main()
