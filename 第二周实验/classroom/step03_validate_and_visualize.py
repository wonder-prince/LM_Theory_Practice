"""Step 03：与 PyTorch 官方多头注意力做公平的数值对照。
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn

from attention import MultiHeadSelfAttention, copy_weights_to_torch_mha
from common import ASSET_DIR, ensure_dirs, save_json, select_device


TOKENS = ["我", "喜欢", "机器", "学习"]


def draw_heatmap(weights: torch.Tensor, output_path: str) -> None:
    matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False
    data = weights.detach().cpu().numpy()
    fig, axes = plt.subplots(1, data.shape[0], figsize=(9.6, 4.2), constrained_layout=True)
    if data.shape[0] == 1:
        axes = [axes]
    for head, ax in enumerate(axes):
        image = ax.imshow(data[head], vmin=0, vmax=max(0.5, data.max()), cmap="Blues")
        ax.set_title(f"注意力头 {head}")
        ax.set_xlabel("Key（被关注位置）")
        ax.set_ylabel("Query（当前输出位置）")
        ax.set_xticks(range(len(TOKENS)), TOKENS)
        ax.set_yticks(range(len(TOKENS)), TOKENS)
        for i in range(len(TOKENS)):
            for j in range(len(TOKENS)):
                value = data[head, i, j]
                ax.text(j, i, f"{value:.3f}", ha="center", va="center",
                        color="white" if value > 0.34 else "black", fontsize=9)
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle("简化多头自注意力权重（固定随机种子，未训练）", fontsize=14)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    torch.manual_seed(2026)
    device = select_device()
    x = torch.randn(1, len(TOKENS), 8, device=device, requires_grad=True)
    custom = MultiHeadSelfAttention(8, 2).to(device).eval()
    reference = nn.MultiheadAttention(8, 2, batch_first=True, dropout=0.0).to(device).eval()
    # 主要正确性验证：把自实现层的参数复制到 PyTorch 官方层。
    # 只有输入与参数都完全相同，两个独立实现的逐元素对照才有意义。
    copy_weights_to_torch_mha(custom, reference)

    custom_result = custom(x)
    # 官方分支只用于数值对照，不参与梯度检查。
    with torch.inference_mode():
        reference_output, reference_weights = reference(
            x.detach(), x.detach(), x.detach(),
            need_weights=True, average_attn_weights=False,
        )
    # 如果拆头、缩放因子、矩阵乘法、合并顺序或 out_proj 任一步写错，
    # 自实现输出就不会再与官方输出一致。这比重复同一条 Weights @ V 公式更完整。
    output_abs_difference = (custom_result["output"].detach() - reference_output).abs()
    output_diff = output_abs_difference.max().item()
    weight_diff = (custom_result["weights"].detach() - reference_weights).abs().max().item()

    # 结构检查：softmax 后每个 Query 对所有 Key 的权重之和必须为 1。
    row_sum_error = (custom_result["weights"].sum(dim=-1) - 1).abs().max().item()

    # 稳定性检查：同一模型、同一输入、eval 模式下重复运行，输出应完全一致。
    repeat_result = custom(x.detach())
    repeat_diff = (
        custom_result["output"].detach() - repeat_result["output"]
    ).abs().max().item()

    # 信息交换检查：只修改第 0 个 token，如果其他位置输出随之变化，
    # 说明这些位置确实通过自注意力读取了第 0 个位置的信息。
    perturbed_x = x.detach().clone()
    perturbed_x[:, 0, :] += 0.5
    perturbed_output = custom(perturbed_x)["output"]
    other_positions_change = (
        perturbed_output[:, 1:, :] - custom_result["output"].detach()[:, 1:, :]
    ).abs().max().item()

    # 可训练性检查：反向传播后，每个核心参数应获得有限且非零的梯度。
    loss = custom_result["output"].square().mean()
    loss.backward()
    gradient_norms = {
        name: parameter.grad.norm().item()
        for name, parameter in custom.named_parameters()
        if parameter.grad is not None
    }
    min_gradient_norm = min(gradient_norms.values())
    all_finite = all(torch.isfinite(t).all().item() for t in custom_result.values())

    thresholds = {
        "row_sum_error": 1e-6,
        "reference_output_error": 1e-5,
        "reference_weight_error": 1e-5,
    }
    assert all_finite
    assert row_sum_error < thresholds["row_sum_error"]
    assert output_diff < thresholds["reference_output_error"]
    assert weight_diff < thresholds["reference_weight_error"]
    assert repeat_diff == 0.0
    assert min_gradient_norm > 0
    assert other_positions_change > 0

    # 热力图不是正确性证明，也不参与上述误差计算。
    # 它只把 [H,L,L] 权重矩阵画成颜色，帮助学生观察每个头分别关注哪些位置。
    heatmap_path = ASSET_DIR / "attention_heatmap.png"
    draw_heatmap(custom_result["weights"][0], str(heatmap_path))
    save_json("step03_validation.json", {
        "status": "PASS",
        "device": str(device),
        "tokens": TOKENS,
        "custom_output": custom_result["output"].detach().cpu().tolist(),
        "reference_output": reference_output.cpu().tolist(),
        "output_abs_difference": output_abs_difference.cpu().tolist(),
        "row_sum_max_error": row_sum_error,
        "reference_output_max_abs_error": output_diff,
        "reference_weight_max_abs_error": weight_diff,
        "repeat_output_max_abs_error": repeat_diff,
        "other_positions_max_change_after_token_0_perturbation": other_positions_change,
        "minimum_parameter_gradient_norm": min_gradient_norm,
        "gradient_norms": gradient_norms,
        "all_intermediate_tensors_finite": all_finite,
        "thresholds": thresholds,
        "heatmap": str(heatmap_path),
    })

    print("[Step 03] 与 PyTorch 官方实现做数值对照；热力图仅作观察")
    print("\n自实现 MultiHeadSelfAttention 输出 [L=4,D=8]:")
    print(custom_result["output"][0].detach().cpu().round(decimals=6))
    print("\n官方 torch.nn.MultiheadAttention 输出 [L=4,D=8]:")
    print(reference_output[0].cpu().round(decimals=6))
    print("\n两者逐元素绝对差值 [L=4,D=8]:")
    print(output_abs_difference[0].cpu().round(decimals=9))
    print(f"attention row-sum max error: {row_sum_error:.3e}")
    print(f"vs torch output max abs error: {output_diff:.3e}")
    print(f"vs torch weight max abs error: {weight_diff:.3e}")
    print(f"deterministic repeat error: {repeat_diff:.3e}")
    print(f"minimum parameter gradient norm: {min_gradient_norm:.6e}")
    print(f"other-position change after modifying token 0: {other_positions_change:.6e}")
    print(f"heatmap: {heatmap_path}")
    print("checkpoint: PASS")


if __name__ == "__main__":
    main()

