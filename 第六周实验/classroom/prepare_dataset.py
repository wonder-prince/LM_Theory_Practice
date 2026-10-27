"""Clean Week 5 learning-companion JSONL and create a deterministic train/validation split.

学生练习流程：先用 --no-quality 验证规则清洗，再补全 calculate_perplexities：
1. 规则清洗：字段完整、task_type/difficulty 合法、代码围栏平衡；再做"重复度去重"——
   两段文本的字符 4-gram 覆盖率 >= 0.95 视为重复（只删几乎相同的问题，保留换关键词的变体）。
2. 模型级质量清洗：学生实现本地 Qwen2.5-0.5B 困惑度计算，现有代码过滤 >1000 的乱码/噪声。

训练/验证划分在两步清洗之后进行。--val-ratio 控制验证集占比（默认 0.1）。
固定随机种子 202606 保证可复现。保留的 train/validation 是"规则+困惑度"双重清洗后的数据集。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import shutil
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT.parent / "第五周实验" / "data" / "course_learning_500_flash_think.jsonl"
ALLOWED_TYPES = {
    "foundation_deployment",
    "data_finetuning",
    "optimization_evaluation",
    "agent_development",
}
ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
PERPLEXITY_THRESHOLD = 1000.0
PPL_MAX_LENGTH = 192


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean and split Week 5 learning-companion data")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="第五周生成的学习伴侣JSONL路径")
    parser.add_argument("--val-ratio", type=float, default=0.1,
                        help="验证集占比，默认 0.1（即 90/10 划分）")
    parser.add_argument("--report", action="store_true",
                        help="清洗后额外输出轻量质量报告（长度分布、分类/难度计数、字符n-gram近似重复提示）")
    parser.add_argument("--quality", action=argparse.BooleanOptionalAction, default=True,
                        help="完成练习函数后运行完整流程；--no-quality 只检查规则清洗")
    return parser.parse_args()


def normalize(value: str) -> str:
    return re.sub(r"[ \t]+", " ", value.replace("\r\n", "\n").replace("\r", "\n")).strip()


def _gram_set(text: str, n: int = 4) -> set[str]:
    """相邻 n 字符组（默认 4-gram）。去掉空白后取滑动窗口子串；
    4-gram 能反映真实词组重叠，避免常用双字组造成的误判。"""
    text = re.sub(r"\s+", "", text)
    return {text[i:i + n] for i in range(max(0, len(text) - n + 1))}


def overlap_dedup(items: list[dict], threshold: float = 0.95) -> tuple[set[str], dict[str, str]]:
    """重复度去重：任一文本的 4-gram 被另一文本覆盖 >= threshold 即视为重复。

    对 instruction+input 与 output 分别做两两对比；覆盖率为 交集大小 / 自身大小。
    阈值取 0.95：只删除"几乎相同"的问题/回答，保留仅换一个关键词（如 d_k 改 d_v）的
    不同知识点题目。500 条两两对比约 12 万次集合运算，秒级完成。"""
    removed: set[str] = set()
    reasons: dict[str, str] = {}

    def grams_by_field(field: str):
        if field == "instruction":
            return [(x["id"], _gram_set(x["instruction"] + x["input"])) for x in items]
        return [(x["id"], _gram_set(x["output"])) for x in items]

    for field in ("instruction", "output"):
        gs = grams_by_field(field)
        n = len(gs)
        for i in range(n):
            id_i, gi = gs[i]
            if id_i in removed:
                continue
            for j in range(i + 1, n):
                id_j, gj = gs[j]
                if id_j in removed or not gi or not gj:
                    continue
                inter = len(gi & gj)
                cov_i = inter / len(gi)
                cov_j = inter / len(gj)
                if cov_i >= threshold and cov_j >= threshold:
                    drop = id_i if len(gi) <= len(gj) else id_j
                    removed.add(drop)
                    reasons[drop] = f"overlap_duplicate_{field}"
                elif cov_i >= threshold:
                    removed.add(id_i)
                    reasons[id_i] = f"overlap_duplicate_{field}"
                elif cov_j >= threshold:
                    removed.add(id_j)
                    reasons[id_j] = f"overlap_duplicate_{field}"
    return removed, reasons


def rule_clean(source: Path) -> tuple[list[dict], list[dict]]:
    """第一层：规则清洗（结构检查 + 重复度去重）。返回 (accepted, rejected)。"""
    # 第一层只做可解释的规则检查：字段、枚举值和代码围栏错误应先被拦截。
    # 这一步不判断知识是否正确，因此不能替代人工抽查。
    # 1) 结构检查
    candidates: list[dict] = []
    rejected: list[dict] = []
    required = ["instruction", "input", "output", "task_type", "difficulty"]
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            item = json.loads(line)
            cleaned = {field: normalize(str(item.get(field, ""))) for field in required}
            reason = None
            if not all(field in item for field in required):
                reason = "missing_field"
            elif not cleaned["instruction"]:
                reason = "empty_instruction"
            elif not cleaned["output"]:
                reason = "empty_output"
            elif cleaned["task_type"] not in ALLOWED_TYPES:
                reason = f"unknown_task_type:{cleaned['task_type']}"
            elif cleaned["difficulty"] not in ALLOWED_DIFFICULTIES:
                reason = f"unknown_difficulty:{cleaned['difficulty']}"
            elif cleaned["output"].count("```") % 2:
                reason = "unbalanced_code_fence"
            if reason:
                rejected.append({"line": line_number, "reason": reason})
            else:
                candidates.append(
                    {
                        "_line": line_number,
                        "id": item.get("id", f"llm_course_sft_{len(candidates) + 1:04d}"),
                        "generation": item.get("generation", {}),
                        **cleaned,
                    }
                )
        except Exception as error:
            rejected.append({"line": line_number, "reason": f"{type(error).__name__}: {error}"})

    # 第二步删除几乎相同的样本，避免同一问题同时出现在不同集合中。
    # 4-gram 覆盖率只适合发现近乎重复，不能识别所有语义重复。
    # 2) 重复度去重（instruction+input 与 output，4-gram 覆盖率 >= 0.95）
    removed_ids, reasons = overlap_dedup(candidates)
    for item in candidates:
        if item["id"] in removed_ids:
            rejected.append({"line": item["_line"], "id": item["id"], "reason": reasons[item["id"]]})
    accepted = [x for x in candidates if x["id"] not in removed_ids]
    return accepted, rejected


def calculate_perplexities(items: list[dict]) -> list[float]:
    """TODO（学生实现）：按输入顺序返回每条样本的困惑度。

    对接要求：
    - 返回 list[float]，长度必须等于 len(items)，顺序必须与 items 完全一致；
    - 每个值必须是大于 0 的有限浮点数，并保留两位小数；
    - 使用本地 Qwen2.5-0.5B-Instruct，不允许联网下载模型；
    - 不在本函数中删除样本、改变 items 或生成报告。
    """
    raise NotImplementedError("请按照实验指导书 7.3 实现 calculate_perplexities()")


def apply_model_quality(items: list[dict]) -> tuple[dict, list[dict]]:
    """调用学生实现的困惑度函数，并按固定阈值生成报告和剔除清单。"""
    ppl_list = calculate_perplexities(items)
    if len(ppl_list) != len(items):
        raise ValueError("calculate_perplexities 返回长度必须与 items 相同")
    if any(not isinstance(ppl, (int, float)) or not math.isfinite(ppl) or ppl <= 0 for ppl in ppl_list):
        raise ValueError("calculate_perplexities 必须返回大于 0 的有限数值")
    ppl_list = [round(float(ppl), 2) for ppl in ppl_list]

    removed = [
        {"id": item["id"], "reason": f"perplexity_{ppl}"}
        for item, ppl in zip(items, ppl_list)
        if ppl > PERPLEXITY_THRESHOLD
    ]
    report = {
        "perplexity": {
            "min": min(ppl_list), "max": max(ppl_list),
            "mean": round(sum(ppl_list) / len(ppl_list), 2),
            "over_1000": sum(1 for p in ppl_list if p > PERPLEXITY_THRESHOLD),
            "formula": "PPL = exp(loss) = exp(-(1/N) * Σ log P(w_i | w_<i))",
            "note": "困惑度=exp(交叉熵)，>1000 视为乱码/噪声",
        },
        "removed_count": len(removed),
        "removed": removed[:10],
    }
    return report, removed


def build_quality_report(items: list[dict]) -> dict:
    """轻量质量报告：长度分布、字符 bigram 近似重复提示。"""
    inst_lens = [len(x["instruction"]) for x in items]
    output_lens = [len(x["output"]) for x in items]
    stats = {
        "instruction_length": {"min": min(inst_lens), "max": max(inst_lens),
                               "mean": round(sum(inst_lens) / len(inst_lens), 1)},
        "output_length": {"min": min(output_lens), "max": max(output_lens),
                          "mean": round(sum(output_lens) / len(output_lens), 1)},
    }

    def grams(text: str, n: int = 2) -> set[str]:
        text = re.sub(r"\s+", "", text)
        return {text[i:i + n] for i in range(max(0, len(text) - n + 1))}

    near_pairs, limit = [], 5
    for i in range(len(items)):
        gi = grams(items[i]["instruction"] + items[i]["input"])
        for j in range(i + 1, len(items)):
            gj = grams(items[j]["instruction"] + items[j]["input"])
            if not gi or not gj:
                continue
            sim = len(gi & gj) / len(gi | gj)
            if sim >= 0.8:
                near_pairs.append({"ids": [items[i]["id"], items[j]["id"]], "bigram_jaccard": round(sim, 3)})
                if len(near_pairs) >= limit:
                    break
        if len(near_pairs) >= limit:
            break
    stats["near_duplicate_hints"] = near_pairs
    return stats


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    if not source.is_file():
        report = {
            "passed": False,
            "skipped": True,
            "reason": "第五周数据未就绪，未执行清洗；数据生成后运行：python -s .\\classroom\\prepare_dataset.py --source <文件路径>",
            "expected_source": str(source),
        }
        out = PROJECT / "outputs" / "data_preparation_report.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("SKIPPED: Week 5 dataset not ready (data cleaning deferred).")
        return 0

    if not 0 < args.val_ratio < 1:
        raise ValueError("--val-ratio 必须在 (0,1) 之间")

    raw_copy = PROJECT / "data" / "source_week5_learning_companion.jsonl"
    raw_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, raw_copy)

    accepted, rejected = rule_clean(source)
    model_report = None

    # 模型级质量清洗必须发生在划分之前，确保 train/validation 使用同一批清洗后样本。
    if args.quality and accepted:
        model_report, removed = apply_model_quality(accepted)
        removed_ids = {r["id"] for r in removed}
        accepted = [x for x in accepted if x["id"] not in removed_ids]
        rejected += [{"line": None, "id": r["id"], "reason": r["reason"]} for r in removed]

    # 固定随机种子保证同一份输入每次得到相同划分，便于复现实验。
    rng = random.Random(202606)
    rng.shuffle(accepted)
    validation_size = max(1, int(round(len(accepted) * args.val_ratio)))
    validation, train = accepted[:validation_size], accepted[validation_size:]
    def _strip(item: dict) -> dict:
        return {k: v for k, v in item.items() if k != "_line"}

    outputs = {
        "cleaned.jsonl": [_strip(x) for x in accepted],
        "train.jsonl": [_strip(x) for x in train],
        "validation.jsonl": [_strip(x) for x in validation],
    }
    for name, items in outputs.items():
        (PROJECT / "data" / name).write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in items), encoding="utf-8"
        )

    report = {
        "passed": len(train) >= 1 and len(validation) >= 1,
        "skipped": False,
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "rule_rejected": [r for r in rejected if r.get("line") is not None],
        "quality_rejected": [r for r in rejected if r.get("line") is None],
        "accepted": len(accepted),
        "rejected": rejected,
        "train": len(train),
        "validation": len(validation),
        "split_seed": 202606,
        "val_ratio": args.val_ratio,
        "task_type_counts": dict(Counter(item["task_type"] for item in accepted)),
        "difficulty_counts": dict(Counter(item["difficulty"] for item in accepted)),
        "overlap_ids": sorted(set(x["id"] for x in train) & set(x["id"] for x in validation)),
    }
    if args.report and accepted:
        report["quality_report"] = build_quality_report(accepted)
    if model_report is not None:
        report["model_quality"] = model_report
    out = PROJECT / "outputs" / "data_preparation_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PASS clean and split" if report["passed"] else "FAIL data preparation")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
