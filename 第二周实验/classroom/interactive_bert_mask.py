"""BERT 交互演示：输入一条含且仅含一个 [MASK] 的英文句子，查看 Top-5 填词。

这不是多轮对话：每次输入都独立计算，BERT 没有保存上一轮内容。输入 q 退出。
"""

from __future__ import annotations

import argparse

import torch
from transformers import AutoModelForPreTraining, AutoTokenizer

from common import BERT_LOCAL_DIR, select_device


def predict(text: str, tokenizer, model, device) -> None:
    """对唯一 [MASK] 位置计算词表概率，并打印最可能的五个 token。"""
    # 本例只讨论一个待填位置。没有 [MASK] 或同时出现多个 [MASK] 时，程序
    # 无法用一个 mask_index 表示目标位置，因此直接给出输入错误。
    if text.count(tokenizer.mask_token) != 1:
        raise ValueError("句子中必须恰好包含一个大写 [MASK]")

    # tokenizer 完成三件事：加入 [CLS]/[SEP]、把文本切成 WordPiece token、
    # 再把 token 换成整数 id。return_tensors="pt" 让结果直接成为 PyTorch
    # 张量；.to(device) 将这些张量放到与模型相同的 CPU 或 GPU。
    inputs = tokenizer(text, return_tensors="pt").to(device)

    # input_ids 与 mask_token_id 比较后得到 [MASK] 的坐标 [批索引, 位置索引]。
    # 本程序批大小为 1，所以取 nonzero() 第一行的第 2 个数作为序列位置。
    mask_index = int((inputs["input_ids"] == tokenizer.mask_token_id).nonzero()[0, 1])
    with torch.inference_mode():
        # AutoModelForPreTraining 同时返回 MLM 和 NSP 两个头。填词只读取
        # prediction_logits=[B,L,V]，再取 [MASK] 位置的 V 个词表分数。
        logits = model(**inputs).prediction_logits[0, mask_index]

    # softmax 把 30,522 个原始分数变成和为 1 的概率；topk(5) 返回概率最高
    # 的五个词表 id。decode 将 id 还原为可读 token，并替换回原句。
    values, indices = logits.softmax(-1).topk(5)
    for rank, (value, index) in enumerate(zip(values, indices), start=1):
        token = tokenizer.decode([int(index)]).strip()
        completed = text.replace(tokenizer.mask_token, token)
        print(f"{rank}. {token!r}: {float(value):.4f} -> {completed}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="非交互测试：运行一条含 [MASK] 的句子后退出")
    args = parser.parse_args()
    device = select_device()

    # local_files_only=True 保证只读取项目 models 目录，不在课堂交互时联网。
    # tokenizer 负责文本与 token id 的转换；model 负责真正的 BERT 前向计算。
    tokenizer = AutoTokenizer.from_pretrained(BERT_LOCAL_DIR, local_files_only=True)
    # 使用与 checkpoint 完全匹配的预训练头，避免丢弃 NSP 参数的警告。
    model = AutoModelForPreTraining.from_pretrained(
        BERT_LOCAL_DIR, local_files_only=True
    ).to(device).eval()
    if args.text:
        predict(args.text, tokenizer, model, device)
        return
    print("输入含一个 [MASK] 的英文句子；输入 q 退出。")
    while True:
        text = input("BERT> ").strip()
        if text.lower() == "q":
            break
        try:
            predict(text, tokenizer, model, device)
        except ValueError as error:
            print(f"输入错误：{error}")


if __name__ == "__main__":
    main()
