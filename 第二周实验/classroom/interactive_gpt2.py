"""GPT-2 交互续写：输入英文开头，离线生成到完整句末或安全上限。

这里的“交互”是逐条提示续写，不是聊天；每轮不会自动记住上一轮。输入 q 退出。
"""

from __future__ import annotations

import argparse

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteriaList

from common import GPT2_LOCAL_DIR, select_device
from step07_explore_gpt2 import StopAfterSentence


def generate(prompt: str, tokenizer, model, device) -> str:
    """以贪心方式续写；相同输入得到相同输出，便于课堂复现。"""
    if not prompt.strip():
        raise ValueError("提示不能为空")

    # GPT-2 使用 byte-level BPE 子词，而不是简单地按空格切单词。tokenizer
    # 把提示转换为 [B,L] 的整数 id；一个英文单词可能对应一个或多个 token。
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 记录提示本身的 token 数，StopAfterSentence 才能只检查“新生成部分”，
    # 避免提示中已有的句点让生成过早停止。
    start_length = inputs["input_ids"].shape[1]
    with torch.inference_mode():
        # generate 会执行自回归循环：读取当前最后位置的词表分数，选择一个
        # 新 token，追加到序列末尾，再继续预测。do_sample=False 表示每次取
        # 最高分 token（贪心解码），因此相同提示得到相同输出。
        generated_ids = model.generate(
            **inputs, max_new_tokens=60, do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=StoppingCriteriaList([
                StopAfterSentence(tokenizer, start_length, min_new_tokens=8)
            ]),
        )
    # generated_ids 同时包含原提示和新 token；decode 将整条 id 序列还原为文本。
    return tokenizer.decode(generated_ids[0], skip_special_tokens=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="非交互测试：续写一条提示后退出")
    args = parser.parse_args()
    device = select_device()

    # 两个对象都从项目本地权重目录读取。AutoModelForCausalLM 加载的是
    # GPT-2 主体加语言模型头，能够给每个位置输出“下一个 token”的词表分数。
    tokenizer = AutoTokenizer.from_pretrained(GPT2_LOCAL_DIR, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        GPT2_LOCAL_DIR, local_files_only=True
    ).to(device).eval()
    if args.prompt:
        print(generate(args.prompt, tokenizer, model, device))
        return
    print("输入英文开头进行续写；输入 q 退出。")
    while True:
        prompt = input("GPT-2> ").strip()
        if prompt.lower() == "q":
            break
        try:
            print(generate(prompt, tokenizer, model, device))
        except ValueError as error:
            print(f"输入错误：{error}")


if __name__ == "__main__":
    main()

