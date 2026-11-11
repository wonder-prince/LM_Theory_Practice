# 教学说明：本文件用于Step 07：在同一个vLLM服务中调用两个LoRA适配器。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 07：在同一个vLLM服务中调用两个LoRA适配器。"""

from __future__ import annotations

import time

import requests

from course_paths import (
    API_BASE,
    DEMO_LORA_MODEL_NAME,
    FINETUNED_LORA_MODEL_NAME,
    OUTPUT_DIR,
    write_json,
)


QUESTIONS = ["说明LoRA为什么能够减少可训练参数。"]
MODEL_NAMES = (DEMO_LORA_MODEL_NAME, FINETUNED_LORA_MODEL_NAME)


def ask(model_name: str, question: str) -> dict:
    """model字段决定当前请求使用哪个LoRA，两个LoRA共享同一份基座权重。"""
    payload = {
        # model 字段在同一基座模型上选择当前请求使用的 LoRA。
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "请用不超过三句话直接回答；不知道时明确说明，不要反问。",
            },
            {"role": "user", "content": question},
        ],
        # 路由对比固定生成条件，避免随机采样掩盖适配器差异。
        "temperature": 0.0,
        "seed": 42,
        # 给完整回答留出空间；实际生成仍可因 EOS 提前结束。
        "max_tokens": 160,
    }
    started = time.perf_counter()
    response = requests.post(
        f"{API_BASE}/v1/chat/completions", json=payload, timeout=180
    )
    response.raise_for_status()
    body = response.json()
    usage = body["usage"]
    return {
        "model": model_name,
        "question": question,
        "answer": body["choices"][0]["message"]["content"].strip(),
        "prompt_tokens": int(usage["prompt_tokens"]),
        "completion_tokens": int(usage["completion_tokens"]),
        "e2e_ms": round((time.perf_counter() - started) * 1000, 3),
    }


def main() -> int:
    # 先确认两个适配器名称都出现在服务模型列表中。
    models_response = requests.get(f"{API_BASE}/v1/models", timeout=30)
    models_response.raise_for_status()
    available = [item["id"] for item in models_response.json()["data"]]
    missing = [name for name in MODEL_NAMES if name not in available]
    if missing:
        raise RuntimeError(f"服务没有暴露以下LoRA名称：{missing}；当前模型：{available}")

    # 同一道问题依次发送给两个 LoRA，基座模型和生成参数保持不变。
    results = [ask(model, question) for question in QUESTIONS for model in MODEL_NAMES]
    report = {
        "checkpoint": "PASS",
        "available_models": available,
        "shared_base_model": "qwen05b-base",
        "results": results,
    }
    out = OUTPUT_DIR / "step07_multi_lora.json"
    write_json(out, report)

    print(f"available models: {', '.join(available)}")
    for item in results:
        print(f"\nmodel: {item['model']}")
        print(f"user: {item['question']}")
        print(f"assistant: {item['answer']}")
        print(
            "usage/latency: "
            f"prompt={item['prompt_tokens']}, completion={item['completion_tokens']}, "
            f"E2E={item['e2e_ms']:.3f} ms"
        )
    print("\nPASS step07 Multi-LoRA routing")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
