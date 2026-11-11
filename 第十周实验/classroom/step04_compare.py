# 教学说明：本文件用于Step 04：汇总已经逐次运行得到的 vLLM 压测 JSON。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 04：汇总已经逐次运行得到的 vLLM 压测 JSON。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from course_paths import OUTPUT_DIR, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="汇总 vLLM 压测结果")
    parser.add_argument(
        "--name",
        default="comparison",
        help="汇总文件名标识，例如 baseline 或 tuning",
    )
    parser.add_argument(
        "labels",
        nargs="+",
        help="按展示顺序填写结果标签，例如 baseline_c1 baseline_c2 baseline_c4 baseline_c8",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = []
    for label in args.labels:
        # 只读取已经生成的单轮压测 JSON，不在汇总阶段重新请求模型。
        path = OUTPUT_DIR / f"step03_{label}.json"
        if not path.exists():
            raise FileNotFoundError(f"缺少 {path.name}，请先单独运行对应压力测试。")
        report = json.loads(path.read_text(encoding="utf-8"))
        rows.append({"label": label, **report["summary"]})

    for row in rows:
        # 终端只逐项打印原始汇总，便于定位某次实验；横向定量比较放在指导书表格中。
        print(f"result: {row['label']}")
        print(
            f"  concurrency={row['concurrency']}; "
            f"req/s={row['request_throughput_rps']:.4f}; "
            f"token/s={row['output_throughput_tokens_per_second']:.3f}"
        )
        print(
            f"  TTFT p95={row['ttft_p95_ms']:.3f} ms; "
            f"TPOT p50={row['tpot_p50_ms']:.3f} ms; "
            f"E2E p95={row['e2e_p95_ms']:.3f} ms"
        )

    # 保存机器可读的统一结果，指导书表格由这些字段整理得到。
    out = OUTPUT_DIR / f"step04_{args.name}.json"
    write_json(out, {"checkpoint": "PASS", "rows": rows})
    print("PASS step04 vLLM comparison")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
