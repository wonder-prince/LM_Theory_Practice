# 教学说明：本文件用于Step 01：加载第六周清洗数据，构造训练/验证 DataLoader，输出统计。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 01：加载第六周清洗数据，构造训练/验证 DataLoader，输出统计。"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from torch.utils.data import DataLoader
from transformers import AutoTokenizer

from data_utils import SFTDataset, format_sample, load_jsonl

PROJECT = Path(__file__).resolve().parents[1]
# 第七周只负责把第六周产物转换成可供训练循环使用的 Dataset 和 DataLoader。
MODEL_DIR = PROJECT.parent / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
TRAIN = PROJECT.parent / "第六周实验" / "data" / "train.jsonl"
VAL = PROJECT.parent / "第六周实验" / "data" / "validation.jsonl"


def parse_args() -> argparse.Namespace:
    # batch-size 影响 DataLoader 的批次数；max-length 会在编码阶段拦截过长样本。
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--train", type=Path, default=TRAIN)
    parser.add_argument("--val", type=Path, default=VAL)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=576)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    # 先检查输入文件，再加载 tokenizer，错误会更早暴露且提示更明确。
    if not args.model_dir.is_dir():
        raise FileNotFoundError(f"模型目录不存在：{args.model_dir}（按第六周 5.2 下载）")
    if not args.train.is_file() or not args.val.is_file():
        raise FileNotFoundError(f"第六周清洗数据不存在：{args.train} / {args.val}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    # 同一 tokenizer 同时处理训练集和验证集，保证 token 数统计具有可比性。
    train_items = load_jsonl(args.train)
    val_items = load_jsonl(args.val)
    train_ds = SFTDataset(tokenizer, train_items, args.max_length)
    val_ds = SFTDataset(tokenizer, val_items, args.max_length)
    train_dl = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_dl = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    # 合并两份编码结果只用于统计最长序列，不会把验证样本混入训练 DataLoader。
    all_encoded = train_ds.encoded + val_ds.encoded
    # 选择带 input 且整条序列较短的样本，完整展示模板化后的“指令—输入—回答”。
    example_candidates = [
        index for index, item in enumerate(train_items) if item.get("input")
    ]
    example_index = min(
        example_candidates,
        key=lambda index: int(train_ds.encoded[index]["sequence_tokens"]),
    )
    example_item = train_items[example_index]
    enc = train_ds[example_index]
    # 报告把样本数量、批次数、token 长度和一个完整模板示例放在一起，便于核对 mask 是否正确。
    report = {
        "train": len(train_items),
        "validation": len(val_items),
        "train_task_types": dict(Counter(x["task_type"] for x in train_items)),
        "train_difficulties": dict(Counter(x["difficulty"] for x in train_items)),
        "train_batches_per_epoch": len(train_dl),
        "validation_batches": len(val_dl),
        "max_length": args.max_length,
        "longest_sample_tokens": max(int(x["sequence_tokens"]) for x in all_encoded),
        "truncated_samples": 0,
        "tokenizer_vocab": tokenizer.vocab_size,
        "example_id": example_item.get("id", "unknown"),
        "example_formatted_sample": format_sample(example_item),
        "example_prompt_tokens": int(enc["answer_start"]),
        "example_answer_tokens": int(enc["answer_tokens"]),
        "example_sequence_tokens": int(enc["sequence_tokens"]),
        "checkpoint": "PASS",
    }
    # step01 只生成检查报告，不修改 train.jsonl 和 validation.jsonl。
    out = PROJECT / "outputs" / "step01_data_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PASS step01 prepare data")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
