# 教学说明：本文件用于Step 05：分别生成四种权重格式的回答，再汇总为定性对比。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 05：分别生成四种权重格式的回答，再汇总为定性对比。"""

from __future__ import annotations

import argparse
import json

import torch

from quant_utils import (
    OUTPUT_DIR,
    load_tokenizer,
    load_tuned_model,
    set_seed,
    synchronize,
    write_json,
)

QUESTION = (
    "vLLM 的 PagedAttention 为什么能提高显存利用率？"
    "请与普通 attention 的 KV cache 管理方式做对比。"
)
PROMPT = f"### 指令\n{QUESTION}\n### 回答\n"
MODES = ("fp16", "fp4", "nf4", "mixed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成或汇总 FP16/FP4/NF4 定性回答")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mode", choices=MODES)
    group.add_argument("--compare", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    return parser.parse_args()


def generate(mode: str, max_new_tokens: int) -> None:
    """在指定权重模式下生成一次完整回答并保存 JSON。"""
    set_seed(2026)
    tokenizer = load_tokenizer()
    model, _ = load_tuned_model(mode)
    encoded = tokenizer(PROMPT, return_tensors="pt").to("cuda")
    with torch.inference_mode():
        generated = model.generate(
            **encoded,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    synchronize()
    # 只截取提示词之后新增的 token，避免把问题重复写入回答。
    new_ids = generated[0, encoded.input_ids.shape[1]:]
    answer = tokenizer.decode(new_ids, skip_special_tokens=True).strip()
    report = {
        "checkpoint": "PASS",
        "mode": mode,
        "question": QUESTION,
        "control": {
            "same_adapter": True,
            "seed": 2026,
            "do_sample": False,
            "max_new_tokens": max_new_tokens,
        },
        "generated_tokens": int(new_ids.numel()),
        "answer": answer,
    }
    out = OUTPUT_DIR / f"step05_qualitative_{mode}.json"
    write_json(out, report)
    print(f"问题：{QUESTION}")
    print(f"{mode}：{answer}")
    print(f"生成 token：{report['generated_tokens']}")
    print(f"完整报告已写入：{out}")


def compare() -> None:
    """读取四份独立结果，并按相同问题顺序打印完整回答。"""
    reports = []
    for mode in MODES:
        path = OUTPUT_DIR / f"step05_qualitative_{mode}.json"
        if not path.exists():
            raise FileNotFoundError(f"必须先生成 {path.name}。")
        reports.append(json.loads(path.read_text(encoding="utf-8")))
    # 问题不一致时拒绝比较，避免把不同任务的回答放在一起下结论。
    questions = {report["question"] for report in reports}
    if len(questions) != 1:
        raise ValueError("四份报告使用的问题不一致，不能直接比较。")
    print(f"问题：{reports[0]['question']}")
    for report in reports:
        print(f"\n[{report['mode']}]\n{report['answer']}")
    print("\nPASS step05 qualitative comparison")


def main() -> int:
    args = parse_args()
    if args.compare:
        compare()
    else:
        generate(args.mode, args.max_new_tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
