# 教学说明：本文件用于Step 01：在真实模型权重上手写对称 INT4 量化与反量化。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 01：在真实模型权重上手写对称 INT4 量化与反量化。"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import torch
from safetensors import safe_open

from quant_utils import MODEL_DIR, OUTPUT_DIR, write_json

TENSOR_NAME = "model.layers.0.self_attn.q_proj.weight"
GROUP_SIZE = 64


def quantize_per_tensor(weight: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    # TODO：根据 5.2 的五步完成逐张量对称 INT4 量化。
    return scale, codes * scale


def quantize_groupwise(weight: torch.Tensor, group_size: int) -> tuple[torch.Tensor, torch.Tensor]:
    # TODO：把权重展平并按 group_size 分组，再对每组重复 5.2 的五步。
    return scales.squeeze(1), restored


def metrics(original: torch.Tensor, restored: torch.Tensor) -> dict[str, float]:
    """计算量化前后权重的 MSE、最大绝对误差和 SQNR。"""
    error = original - restored
    signal = original.float().pow(2).mean().item()
    mse = error.float().pow(2).mean().item()
    sqnr = 10 * math.log10(signal / max(mse, 1e-30))
    return {
        "mse": mse,
        "max_abs_error": error.abs().max().item(),
        "sqnr_db": sqnr,
    }


def main() -> int:
    model_file = MODEL_DIR / "model.safetensors"
    # 只读取一个真实 q_proj 权重，避免为量化数学演示加载完整模型。
    with safe_open(model_file, framework="pt", device="cpu") as handle:
        weight = handle.get_tensor(TENSOR_NAME).float()

    # 用同一真实权重分别进行逐张量量化和 64 参数分组量化。
    per_scale, per_restored = quantize_per_tensor(weight)
    group_scales, group_restored = quantize_groupwise(weight, GROUP_SIZE)
    per = metrics(weight, per_restored)
    grouped = metrics(weight, group_restored)
    report = {
        "checkpoint": "PASS",
        "tensor": TENSOR_NAME,
        "shape": list(weight.shape),
        "elements": weight.numel(),
        "quantizer": "symmetric signed INT4, q=clip(round(w/s), -8, 7)",
        "per_tensor": {"scale_count": 1, "scale": per_scale.item(), **per},
        "groupwise": {"group_size": GROUP_SIZE, "scale_count": group_scales.numel(), **grouped},
    }
    out = OUTPUT_DIR / "step01_quantization_math.json"
    write_json(out, report)
    # 终端只提示结果文件位置；完整指标统一在 JSON 中查看和解释。
    print(r"结果已保存到：outputs\step01_quantization_math.json")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
