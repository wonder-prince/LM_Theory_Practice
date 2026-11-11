# 教学说明：本文件用于Step 04（扩展）：比较统一 INT4 与“敏感张量保留 FP16”的混合精度方案。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 04（扩展）：比较统一 INT4 与“敏感张量保留 FP16”的混合精度方案。"""

from __future__ import annotations

import argparse
import json
import math

import torch
from safetensors import safe_open

from quant_utils import ADAPTER_DIR, MODEL_DIR, OUTPUT_DIR, write_json

MODULES = [
    "self_attn.q_proj",
    "self_attn.k_proj",
    "self_attn.v_proj",
    "self_attn.o_proj",
    "mlp.gate_proj",
    "mlp.up_proj",
    "mlp.down_proj",
]
GROUP_SIZE = 64


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="扫描全部层并生成 Mixed 模型的 FP16 模块建议")
    parser.add_argument(
        "--keep-fp16",
        type=int,
        default=5,
        help="保留为 FP16 的敏感模块数量，可按需要指定，默认 5",
    )
    parser.add_argument("--show-top", type=int, default=10, help="终端显示的敏感张量数量")
    return parser.parse_args()


def model_layer_count() -> int:
    """从本地 config.json 读取网络层数，避免把 24 层写死在代码中。"""
    config = json.loads((MODEL_DIR / "config.json").read_text(encoding="utf-8"))
    return int(config["num_hidden_layers"])


def adapter_scaling() -> float:
    """读取 LoRA 的 alpha/r；本实验适配器未使用 DoRA 或分层秩配置。"""
    config = json.loads((ADAPTER_DIR / "adapter_config.json").read_text(encoding="utf-8"))
    return float(config["lora_alpha"]) / float(config["r"])


def effective_weight(base_handle, adapter_handle, name: str, scaling: float):
    """返回合并 LoRA 后的等效权重；未挂载 LoRA 的投影直接返回基座权重。"""
    weight = base_handle.get_tensor(name).float()
    # PEFT 保存的键名前缀比基座权重多一层 base_model.model。
    adapter_prefix = "base_model.model." + name.removesuffix(".weight")
    a_key = adapter_prefix + ".lora_A.weight"
    b_key = adapter_prefix + ".lora_B.weight"
    if a_key not in adapter_handle.keys() or b_key not in adapter_handle.keys():
        return weight, False
    lora_a = adapter_handle.get_tensor(a_key).float()
    lora_b = adapter_handle.get_tensor(b_key).float()
    return weight + scaling * (lora_b @ lora_a), True


def score(weight: torch.Tensor) -> dict[str, float | int]:
    """用 64 参数分组 INT4 重建一个张量，并计算其量化误差。"""
    flat = weight.float().flatten()
    padding = (-flat.numel()) % GROUP_SIZE
    groups = torch.nn.functional.pad(flat, (0, padding)).view(-1, GROUP_SIZE)
    scale = groups.abs().amax(dim=1, keepdim=True).clamp_min(1e-12) / 7
    restored = (torch.round(groups / scale).clamp(-8, 7) * scale).flatten()[: flat.numel()]
    error = flat - restored
    squared_error = error.pow(2).sum().item()
    signal_energy = flat.pow(2).sum().item()
    mse = squared_error / flat.numel()
    return {
        "elements": flat.numel(),
        "scale_count": groups.shape[0],
        "mse": mse,
        "squared_error": squared_error,
        "signal_energy": signal_energy,
        "sqnr_db": 10 * math.log10(signal_energy / max(squared_error, 1e-30)),
    }


def aggregate(rows: list[dict], fp16_names: set[str]) -> dict[str, float | int]:
    """估算选中张量保留 FP16、其余张量使用分组 INT4 的误差与位宽。"""
    total_elements = sum(int(row["elements"]) for row in rows)
    signal_energy = sum(float(row["signal_energy"]) for row in rows)
    squared_error = sum(
        0.0 if row["tensor"] in fp16_names else float(row["squared_error"])
        for row in rows
    )
    storage_bits = sum(
        int(row["elements"]) * 16
        if row["tensor"] in fp16_names
        else int(row["elements"]) * 4 + int(row["scale_count"]) * 16
        for row in rows
    )
    return {
        "fp16_tensor_count": len(fp16_names),
        "estimated_bits": storage_bits,
        "quantization_error_energy": round(squared_error, 6),
        "average_bits_per_parameter": round(storage_bits / total_elements, 4),
        "compression_ratio_vs_fp16": round(total_elements * 16 / storage_bits, 4),
        "aggregate_sqnr_db": round(
            10 * math.log10(signal_energy / max(squared_error, 1e-30)), 4
        ),
    }


def main() -> int:
    args = parse_args()
    layer_count = model_layer_count()
    scaling = adapter_scaling()
    if args.keep_fp16 <= 0:
        raise ValueError("--keep-fp16 必须大于 0。")

    rows = []
    lora_merged_tensor_count = 0
    # 遍历全部网络层；先合并本组 LoRA，再评估注意力与前馈网络的全部 7 类投影。
    with safe_open(MODEL_DIR / "model.safetensors", framework="pt", device="cpu") as base_handle, safe_open(
        ADAPTER_DIR / "adapter_model.safetensors", framework="pt", device="cpu"
    ) as adapter_handle:
        for layer in range(layer_count):
            for module in MODULES:
                name = f"model.layers.{layer}.{module}.weight"
                weight, adapter_applied = effective_weight(
                    base_handle, adapter_handle, name, scaling
                )
                lora_merged_tensor_count += int(adapter_applied)
                statistics = score(weight)
                rows.append({
                    "tensor": name,
                    "shape": list(weight.shape),
                    "lora_merged": adapter_applied,
                    **statistics,
                })
    # SQNR 越低，表示该张量在当前量化规则下越敏感。
    rows.sort(key=lambda item: item["sqnr_db"])
    for rank, row in enumerate(rows, start=1):
        row["sensitivity_rank"] = rank
    keep_count = min(args.keep_fp16, len(rows))
    sensitive_rows = rows[:keep_count]
    sensitive_names = {row["tensor"] for row in sensitive_rows}
    recommended_modules = [row["tensor"].removesuffix(".weight") for row in sensitive_rows]
    uniform_int4 = aggregate(rows, set())
    mixed_precision = aggregate(rows, sensitive_names)
    mixed_precision["error_reduction_percent_vs_uniform_int4"] = round(
        (1 - mixed_precision["quantization_error_energy"]
         / uniform_int4["quantization_error_energy"]) * 100,
        2,
    )
    report = {
        "checkpoint": "PASS",
        "method": f"symmetric groupwise INT4, group_size={GROUP_SIZE}; lower SQNR means higher reconstruction sensitivity",
        "experiment_scope": f"本组LoRA与基座合并后的等效权重；扫描全部{layer_count}层的7类线性投影，共{len(rows)}个张量",
        "adapter_dir": str(ADAPTER_DIR),
        "lora_scaling_alpha_div_r": scaling,
        "lora_merged_tensor_count": lora_merged_tensor_count,
        "layer_count": layer_count,
        "module_types": MODULES,
        "rows": rows,
        "uniform_int4": uniform_int4,
        "mixed_precision": {
            "rule": f"SQNR最低的{keep_count}个张量保留FP16，其余张量使用分组INT4",
            "fp16_tensors": sorted(sensitive_names),
            "recommended_module_names": recommended_modules,
            **mixed_precision,
        },
        "discussion": "混合方案以更高平均位宽换取更低的权重重建误差；它仍需完整模型验证loss才能判断端到端收益。",
    }
    out = OUTPUT_DIR / "step04_layer_sensitivity.json"
    write_json(out, report)
    show_count = min(max(args.show_top, keep_count), len(rows))
    print(f"已合并本组 LoRA：{lora_merged_tensor_count} 个投影张量，缩放系数 alpha/r={scaling:g}")
    print(f"已扫描：{layer_count} 层 × {len(MODULES)} 类投影 = {len(rows)} 个张量")
    print(f"最敏感的 {show_count} 个张量（SQNR 越低，敏感度越高）：")
    for row in rows[:show_count]:
        print(f"{row['sensitivity_rank']:2d}. {row['tensor']}: {row['sqnr_db']:.3f} dB")
    print("\n请复制到 quant_utils.py：")
    print("MIXED_FP16_MODULES = [")
    for name in recommended_modules:
        print(f'    "{name}",')
    print("]")
    print(
        f"统一 INT4（仅 168 个投影权重的估算）："
        f"{uniform_int4['average_bits_per_parameter']:.3f} bit/参数，"
        f"聚合 SQNR={uniform_int4['aggregate_sqnr_db']:.3f} dB"
    )
    print(
        f"混合精度（仅 168 个投影权重的估算）："
        f"{mixed_precision['average_bits_per_parameter']:.3f} bit/参数，"
        f"聚合 SQNR={mixed_precision['aggregate_sqnr_db']:.3f} dB，"
        f"误差能量下降={mixed_precision['error_reduction_percent_vs_uniform_int4']:.2f}%"
    )
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
