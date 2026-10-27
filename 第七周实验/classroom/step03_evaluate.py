# 教学说明：本文件用于Step 03：定量评估基座模型与 LoRA 模型。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 03：定量评估基座模型与 LoRA 模型。

本脚本只计算验证集上的回答区 loss、perplexity 和 ROUGE-L。
终端输入问题并观察两种模型回答的实验由 step04_qualitative_chat.py 完成。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

import torch
from peft import PeftModel
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer

from data_utils import SFTDataset, format_prompt, load_jsonl, make_collate

os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
PROJECT = Path(__file__).resolve().parents[1]
# 评估阶段复用第六周基座、验证集和第七周训练得到的 LoRA 适配器。
MODEL_DIR = PROJECT.parent / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
VAL = PROJECT.parent / "第六周实验" / "data" / "validation.jsonl"
ADAPTER_DIR = PROJECT / "adapters" / "qwen05b-learning-companion-lora-finetuned"


def parse_args() -> argparse.Namespace:
    # batch-size/max-length 只影响评估资源；max-new-tokens 影响后面示例回答长度。
    parser = argparse.ArgumentParser(description="定量比较基座模型与 LoRA 模型")
    parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--val", type=Path, default=VAL)
    parser.add_argument("--adapter", type=Path, default=ADAPTER_DIR)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=576)
    parser.add_argument("--max-new-tokens", type=int, default=120)
    return parser.parse_args()


def load_model(model_dir: Path, device: str):
    """每次独立加载一个模型，避免 PEFT 把基座对象原地改写。"""
    # GPU 使用半精度节省显存，CPU 使用 float32 兼容普通推理环境。
    dtype = torch.float16 if device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, local_files_only=True, torch_dtype=dtype, low_cpu_mem_usage=True
    ).to(device)
    model.eval()
    return model


def loss_on(items, tokenizer, model, batch_size: int, max_length: int) -> tuple[float, float]:
    """只对 labels 中未被 -100 屏蔽的回答 token 计算交叉熵。"""
    collate = make_collate(tokenizer.pad_token_id)
    # 评估使用与训练相同的答案区 mask，确保 loss 只衡量回答 token。
    loader = DataLoader(SFTDataset(tokenizer, items, max_length), batch_size=batch_size,
                        shuffle=False, collate_fn=collate)
    loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-100)
    device = next(model.parameters()).device
    total, batches = 0.0, 0
    with torch.inference_mode():
        for batch in loader:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            # inference_mode 不创建反向图；这里只需要模型输出 logits。
            logits = model(input_ids=ids, attention_mask=mask).logits
            # 因果语言模型用当前位置预测下一个 token，因此 logits 和 labels 要错开一位。
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            total += loss_fct(shift_logits.view(-1, shift_logits.size(-1)),
                              shift_labels.view(-1)).item()
            batches += 1
    # 以 batch 平均 loss 作为整体指标，再取指数得到 perplexity。
    average = total / max(batches, 1)
    return average, math.exp(average)


def lcs_len(a: str, b: str) -> int:
    """计算两个字符串的最长公共子序列长度，供 ROUGE-L 使用。"""
    # 动态规划只保留上一行和当前行，空间复杂度从二维表降为 O(len(b))。
    previous = [0] * (len(b) + 1)
    for char_a in a:
        current = [0] * (len(b) + 1)
        for j, char_b in enumerate(b, start=1):
            current[j] = previous[j - 1] + 1 if char_a == char_b else max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def rouge_l(reference: str, hypothesis: str) -> float:
    """返回去空白后的 ROUGE-L F 值；该指标只反映表面重合，不代表事实正确。"""
    # 去空白后计算最长公共子序列，避免中英文回答因换行差异影响表面重合度。
    ref = re.sub(r"\s+", "", reference)
    hyp = re.sub(r"\s+", "", hypothesis)
    if not ref or not hyp:
        return 0.0
    lcs = lcs_len(ref, hyp)
    precision = lcs / len(hyp)
    recall = lcs / len(ref)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def generate(tokenizer, model, prompt: str, max_new_tokens: int) -> str:
    """确定性生成，用于让同一输入的前后对比更容易复现。"""
    device = next(model.parameters()).device
    # 编码后的输入放到与模型相同的设备；生成结果后面会切掉原始 prompt。
    encoded = tokenizer(prompt, return_tensors="pt").to(device)
    # 本实验使用贪心解码；清除模型目录中仅供随机采样使用的参数，避免无效警告。
    model.generation_config.do_sample = False
    model.generation_config.temperature = None
    model.generation_config.top_p = None
    model.generation_config.top_k = None
    # 贪心生成每次选择当前概率最高的 token，减少前后模型比较中的随机差异。
    output = model.generate(**encoded, max_new_tokens=max_new_tokens, do_sample=False,
                            pad_token_id=tokenizer.eos_token_id,
                            eos_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0, encoded.input_ids.shape[1]:], skip_special_tokens=True).strip()


def main() -> int:
    args = parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    # 验证集同时用于 loss、PPL 和前 20 条样本的 ROUGE-L/回答对比。
    items = load_jsonl(args.val)

    # 先完整测量基座模型，再释放显存；随后重新加载基座并挂载适配器。
    # 先评估基座并保存回答，再释放基座显存，之后加载同一基座并挂载 LoRA。
    base = load_model(args.model_dir, device)
    base_loss, base_ppl = loss_on(items, tokenizer, base, args.batch_size, args.max_length)
    rouge_base, rouge_tuned = [], []
    base_answers = []
    for item in items[:20]:
        base_answers.append(generate(tokenizer, base, format_prompt(item), args.max_new_tokens))
    del base
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # PeftModel 不复制完整基座，只把 adapter 配置和增量权重挂到新加载的基座上。
    tuned = PeftModel.from_pretrained(load_model(args.model_dir, device), args.adapter,
                                      local_files_only=True).to(device)
    tuned.eval()
    tuned_loss, tuned_ppl = loss_on(items, tokenizer, tuned, args.batch_size, args.max_length)
    for item, base_answer in zip(items[:20], base_answers):
        tuned_answer = generate(tokenizer, tuned, format_prompt(item), args.max_new_tokens)
        rouge_base.append(rouge_l(item["output"], base_answer))
        rouge_tuned.append(rouge_l(item["output"], tuned_answer))

    # 报告将自动指标和指标局限性一起保存，避免把 ROUGE-L 误读为事实正确率。
    report = {
        "checkpoint": "PASS",
        "quantitative": {
            "validation_loss": {"base": round(base_loss, 5), "tuned": round(tuned_loss, 5)},
            "validation_perplexity": {"base": round(base_ppl, 3), "tuned": round(tuned_ppl, 3)},
            "rouge_l_avg_f_over_20": {
                "base": round(sum(rouge_base) / max(len(rouge_base), 1), 4),
                "tuned": round(sum(rouge_tuned) / max(len(rouge_tuned), 1), 4),
            },
            "note": "ROUGE-L 只反映文本表面重合，不能单独证明回答事实正确。",
        },
    }
    out = PROJECT / "outputs" / "step03_evaluate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("== 定量对比 ==")
    print(f"validation loss:  基座 {base_loss:.5f} -> 微调后 {tuned_loss:.5f}")
    print(f"validation ppl:   基座 {base_ppl:.3f} -> 微调后 {tuned_ppl:.3f}")
    print(f"ROUGE-L F(前20条): 基座 {sum(rouge_base) / max(len(rouge_base), 1):.4f} -> 微调后 {sum(rouge_tuned) / max(len(rouge_tuned), 1):.4f}")
    print(f"完整报告已写入：{out}")
    print("PASS step03 evaluate")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
