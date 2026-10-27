"""Step 03：在 VS Code 终端中与本地 7B 模型进行多轮对话。

与单轮推理相比，本脚本新增 messages 历史列表。模型每回答一次，程序就把
user/assistant 两条消息保存下来；下一轮把完整历史再次送入模型，从而形成
“记得上一轮”的效果。输入 exit 可结束；使用 --demo 可自动演示两轮。
"""

from __future__ import annotations

import argparse
from pathlib import Path

from windows_cuda_runtime import prepare_cuda_dll_search


# 由脚本位置推导项目目录，复制整个项目后不需要修改模型的绝对路径。
PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = (
    PROJECT_DIR
    / "models"
    / "Qwen2.5-7B-Instruct-GGUF"
    / "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"
)


def parse_args() -> argparse.Namespace:
    """读取演示开关和单轮生成上限；不传 --demo 时进入人工交互模式。"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="自动运行两轮课堂演示")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="单轮最多生成多少个 token；默认 220，可通过参数单独修改",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_tokens is not None and args.max_tokens <= 0:
        raise ValueError("--max-tokens 必须是正整数")
    # 不传参数时统一使用已实测的 220；需要更长回答时可由命令行单独覆盖。
    max_tokens = args.max_tokens if args.max_tokens is not None else 220
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"缺少模型：{MODEL_PATH}")

    # Windows 必须先准备 CUDA 动态库搜索路径，再导入 llama_cpp。
    prepare_cuda_dll_search()
    from llama_cpp import Llama

    print("[Step 03] 正在加载本地 7B 模型……")
    # 采用与 Step 02 相同的 CPU/GPU 混合部署参数。模型只在程序启动时加载一次，
    # 后续每轮对话复用同一个 model 对象，不会重复读取 4.36 GiB 权重。
    model = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=2048,
        n_gpu_layers=16,
        n_threads=8,
        n_threads_batch=8,
        chat_format="chatml",
        verbose=False,
    )

    # system 消息只描述助手身份与回答方式，不把模型参数或问题答案预先告诉模型。
    # 它始终位于历史列表首位，对后续每一轮回答都有效。
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "你是《大模型原理与应用》课程助教。"
                "请用清晰、准确、适合大学生理解的中文回答问题，并结合已有对话保持上下文连贯。"
            ),
        }
    ]
    # 只有传入 --demo 时才依次使用下面两题；普通交互模式读取学生在终端中的输入。
    demo_questions = [
        "我是小红，解释一下大模型中的 token 是什么。",
        "我是谁？",
    ]

    print("模型已经就绪。输入 exit 结束对话。")
    turn = 0
    while True:
        # 自动演示与人工输入共用后面的消息保存和模型生成代码。
        if args.demo:
            if turn >= len(demo_questions):
                break
            question = demo_questions[turn]
            print(f"\nuser> {question}")
        else:
            question = input("\nuser> ").strip()
            if question.lower() in {"exit", "quit"}:
                break
            if not question:
                continue

        # 先把本轮问题追加到历史，再把包含 system 和此前问答的完整列表交给模型。
        messages.append({"role": "user", "content": question})
        response = model.create_chat_completion(
            messages=messages,
            # max_tokens 限制新生成长度；较低 temperature 让课堂演示更稳定、便于复现。
            max_tokens=max_tokens,
            temperature=0.1,
            top_p=0.9,
            seed=42 + turn,
        )
        # 抽取回答后也写回 messages；下一轮因此能够读取这一轮的问答内容。
        answer = response["choices"][0]["message"]["content"].strip()
        messages.append({"role": "assistant", "content": answer})
        print(f"assistant> {answer}")
        print(f"history: {len(messages)} messages（含1条system消息）")
        turn += 1

    print("对话结束。模型进程退出后，本次内存中的历史也随之清空。")


if __name__ == "__main__":
    main()
