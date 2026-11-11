# 教学说明：本文件用于Step 03：汇总各模式的真实结果，不重新加载模型。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 03：汇总各模式的真实结果，不重新加载模型。"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from quant_utils import OUTPUT_DIR, write_json

PRIMARY_MODES = ("fp16", "fp4", "nf4", "mixed")


def read_reports() -> list[dict]:
    """读取四个独立进程已经生成的基准报告。"""
    reports = []
    for mode in PRIMARY_MODES:
        path = OUTPUT_DIR / f"step02_benchmark_{mode}.json"
        if not path.exists():
            raise FileNotFoundError(f"必须先生成 {path.name}。")
        report = json.loads(path.read_text(encoding="utf-8"))
        report["source"] = path.name
        reports.append(report)
    return reports


def main() -> int:
    reports = read_reports()
    by_name = {r["source"].removeprefix("step02_benchmark_").removesuffix(".json"): r for r in reports}
    base = by_name["fp16"]
    rows = []
    for name, report in by_name.items():
        footprint = report["model_footprint_mib"]
        speed = report["generation"]["median_tokens_per_second"]
        ppl = report["validation"]["answer_only_perplexity"]
        # 所有百分比都以 FP16 组为基线，正负号保留变化方向。
        rows.append({
            "mode": name,
            "model_footprint_mib": footprint,
            "peak_cuda_mib": report["cuda_memory_after_generation"]["peak_allocated_mib"],
            "load_seconds": report["load_seconds"],
            "median_latency_seconds": report["generation"]["median_latency_seconds"],
            "median_tokens_per_second": speed,
            "answer_only_loss": report["validation"]["answer_only_loss"],
            "answer_only_perplexity": ppl,
            "footprint_reduction_percent_vs_fp16": round((1 - footprint / base["model_footprint_mib"]) * 100, 2),
            "speed_change_percent_vs_fp16": round((speed / base["generation"]["median_tokens_per_second"] - 1) * 100, 2),
            "perplexity_change_percent_vs_fp16": round((ppl / base["validation"]["answer_only_perplexity"] - 1) * 100, 2),
        })

    summary = {
        "checkpoint": "PASS",
        "comparison_rule": "同一基座、同一 LoRA、同一提示词/种子/生成长度/预热/重复次数；每个模式独立进程。",
        "rows": rows,
        "interpretation_guardrail": "4-bit 的首要收益是权重占用下降；实际速度由硬件和算子实现决定，不能预设一定更快。",
    }
    write_json(OUTPUT_DIR / "step03_comparison.json", summary)
    csv_path = OUTPUT_DIR / "step03_comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # 完整指标已经写入 JSON 和 CSV，终端不再重复打印不完整表格。
    print(r"结果已保存到：outputs\step03_comparison.json")
    print(r"CSV 已保存到：outputs\step03_comparison.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
