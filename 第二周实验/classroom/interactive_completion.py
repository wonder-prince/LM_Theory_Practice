# 教学说明：本文件用于课堂交互入口：输入四个中文词，离线查看五个候选补全词的概率。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""课堂交互入口：输入四个中文词，离线查看五个候选补全词的概率。

示例：天空 乌云 密布 将要。输入 q 退出。注意：这是 50 条数据训练的封闭五分类器，不会自由生成任意词。
"""

from __future__ import annotations

import argparse

from step04_sentence_completion import load_trained_model, predict


def show(prompt: str, model, word_to_id: dict[str, int]) -> None:
    """运行一次预测，并按概率从高到低打印。"""
    row = predict(model, prompt, word_to_id)
    ranking = sorted(row["probabilities"].items(), key=lambda item: item[1], reverse=True)
    print(f"预测：{row['predicted']}")
    for word, probability in ranking:
        print(f"  {word:<4} {probability:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="非交互测试：提供一条四词提示后退出")
    args = parser.parse_args()
    model, _, word_to_id = load_trained_model()
    if args.prompt:
        show(args.prompt, model, word_to_id)
        return

    print("请输入恰好四个用空格分隔的词；输入 q 退出。")
    while True:
        prompt = input("四词提示> ").strip()
        if prompt.lower() == "q":
            break
        try:
            show(prompt, model, word_to_id)
        except ValueError as error:
            print(f"输入错误：{error}")


if __name__ == "__main__":
    main()

