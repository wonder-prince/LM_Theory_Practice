# 教学说明：本文件用于第七周共享数据工具：样本格式化、答案区 mask、加载 JSONL、DataLoader。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""第七周共享数据工具：样本格式化、答案区 mask、加载 JSONL、DataLoader。"""

from __future__ import annotations

import json
from pathlib import Path

import torch
from torch.utils.data import Dataset


def format_prompt(item: dict) -> str:
    """构造学习伴侣样本的输入模板（不含回答）。"""
    # 训练和生成必须使用同一套模板；input 为空时仍保留统一的“回答”起点。
    prompt = f"### 指令\n{item['instruction']}\n"
    if item.get("input"):
        prompt += f"### 输入\n{item['input']}\n"
    return prompt + "### 回答\n"


def format_sample(item: dict) -> str:
    """完整样本 = 输入模板 + 回答（训练时对回答部分计算 loss）。"""
    # 这个字符串主要用于检查和报告；真正送入模型前还要经过 tokenizer 编码。
    return format_prompt(item) + item["output"]


def encode_with_answer_mask(tokenizer, item: dict, max_length: int = 576) -> dict:
    """编码完整样本，只对回答与结尾 EOS 计算 loss。

    如果样本超过 max_length，直接报错，避免静默截断回答。返回值中的 labels
    与 input_ids 等长：提示区为 -100，回答区和 EOS 保留真实 token id。
    """
    prompt = format_prompt(item)
    # 分开编码提示与回答，才能知道 labels 中哪一段应设置为 -100。
    prompt_ids = tokenizer(prompt, add_special_tokens=False).input_ids
    answer_ids = tokenizer(item["output"], add_special_tokens=False).input_ids
    if tokenizer.eos_token_id is None:
        raise ValueError("分词器缺少 eos_token_id，无法标记回答结束位置")
    answer_ids.append(tokenizer.eos_token_id)

    input_ids = prompt_ids + answer_ids
    if len(input_ids) > max_length:
        sample_id = item.get("id", "unknown")
        raise ValueError(
            f"样本 {sample_id} 共 {len(input_ids)} token，超过 max_length={max_length}；"
            "请提高上限或缩短样本，不能静默截断回答"
        )

    # input_ids、attention_mask、labels 保持相同长度，方便 collate 拼成批次。
    input_ids = torch.tensor(input_ids, dtype=torch.long)
    attention_mask = torch.ones_like(input_ids)
    labels = input_ids.clone()
    answer_start = len(prompt_ids)
    # CrossEntropyLoss(ignore_index=-100) 会跳过提示区，只学习模型生成回答的行为。
    labels[:answer_start] = -100
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
        "answer_start": answer_start,
        "answer_tokens": len(answer_ids),
        "sequence_tokens": len(input_ids),
    }


def load_jsonl(path: Path) -> list[dict]:
    records = []
    # JSONL 每一行是一个独立 JSON 对象，因此可以逐行读取，不必一次加载原始文本。
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


class SFTDataset(Dataset):
    """把已清洗的 JSONL 记录编码成训练样本。"""

    def __init__(self, tokenizer, items: list[dict], max_length: int = 576):
        # 在 Dataset 创建时一次性编码，训练循环中只负责取已经准备好的张量。
        self.encoded = [encode_with_answer_mask(tokenizer, it, max_length) for it in items]

    def __len__(self) -> int:
        return len(self.encoded)

    def __getitem__(self, idx: int) -> dict:
        return self.encoded[idx]


def make_collate(pad_id: int):
    """DataLoader collate：把一批长度不同的样本 padding 到该批最大长度。"""

    def collate(batch: list[dict]) -> dict:
        # 动态 padding 只补到当前批次最长样本，通常比所有样本统一补到 max_length 更省显存。
        max_len = max(b["input_ids"].shape[0] for b in batch)
        ids = torch.full((len(batch), max_len), pad_id, dtype=torch.long)
        mask = torch.zeros((len(batch), max_len), dtype=torch.long)
        labels = torch.full((len(batch), max_len), -100, dtype=torch.long)
        # 每个 batch 按自身最长样本 padding；labels 的 padding 保持 -100，不参与 loss。
        for i, b in enumerate(batch):
            n = b["input_ids"].shape[0]
            ids[i, :n] = b["input_ids"]
            mask[i, :n] = b["attention_mask"]
            labels[i, :n] = b["labels"]
        return {"input_ids": ids, "attention_mask": mask, "labels": labels}

    return collate
