# 教学说明：本文件用于Step 05：不更换模型，只改 system prompt，构造三种应用场景。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 05：不更换模型，只改 system prompt，构造三种应用场景。

本脚本复用 Step 04 已启动的本地 API。三次请求使用同一套 7B 权重，变化的是
角色、任务约束和输入内容，因此它们是三个“应用配置”，不是三个新训练模型。
"""

from __future__ import annotations

import json
from pathlib import Path

import requests


PROJECT_DIR = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:18080/v1/chat/completions"
OUTPUT_PATH = PROJECT_DIR / "outputs" / "step05_application_scenarios.json"

# 三个场景使用不同的 system 和 user 内容；这里没有复制或修改任何模型权重。
SCENARIOS = {
    "编程助手": {
        "system": "你是Python编程助手。先指出错误原因，再给最小修改后的代码。",
        "user": "下面代码为什么报错？请修改：\nitems=[1,2,3]\nfor i in range(4):\n    print(items[i])",
    },
    "学习伴侣": {
        "system": (
            "你是耐心的学习伴侣。请根据用户的问题，用清晰、适合初学者的方式引导理解。"
            "对于需要推导的概念，可以先提出一个小问题，再根据后续回答继续解释；"
            "本轮用一到两句话提出一个引导问题，不直接公布完整答案，除非用户明确要求。"
        ),
        "user": "我不理解为什么注意力分数要除以根号dk，请带着我想明白。",
    },
    "游戏NPC": {
        "system": "你是蒸汽城图书馆守门人伊诺，谨慎、简短，只知道城内公开传闻。保持角色口吻。",
        "user": "我想进入禁书区，你能告诉我需要什么凭证吗？",
    },
}


def main() -> None:
    print("[Step 05] 同一模型的三种应用配置")
    records = []
    for name, prompt in SCENARIOS.items():
        # 每次循环重新构造一段独立对话，因此三个场景不会共享上一场景的聊天历史。
        payload = {
            "model": "qwen2.5-7b-local",
            "messages": [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
            ],
            "max_tokens": 160,
            # 编程与知识讲解强调稳定性，NPC 使用较高温度以增加措辞变化。
            "temperature": 0.2 if name != "游戏NPC" else 0.7,
            "seed": 42,
        }
        # 三次请求都发往 Step 04 启动的同一个本地 7B 模型服务。
        reply = requests.post(URL, json=payload, timeout=180)
        reply.raise_for_status()
        response = reply.json()
        answer = response["choices"][0]["message"]["content"].strip()
        print(f"\n--- {name} ---")
        print("system:", prompt["system"])
        print("user:", prompt["user"])
        print("assistant:", answer)
        records.append({"scenario": name, "request": payload, "answer": answer})

    # 把三种配置、输入和回答集中保存，便于横向比较 system prompt 的作用。
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nsaved: {OUTPUT_PATH.relative_to(PROJECT_DIR)}")
    print("checkpoint: PASS（同一7B模型完成三种应用输出）")


if __name__ == "__main__":
    main()
