"""Step 01：运行 attention.py 中的单头自注意力，并解释每项输出。
"""

from __future__ import annotations

import torch

from attention import SingleHeadSelfAttention
from common import save_json, select_device


# 四个文字标签只用于帮助阅读输出；真正送进网络的是下面随机生成的 8 维向量。
TOKENS = ["学生", "通过", "注意力", "建模"]


def rounded(tensor: torch.Tensor) -> list:
    """把 GPU 张量转到 CPU、保留四位小数，再转成可写入 JSON 的列表。"""
    return tensor.detach().cpu().round(decimals=4).tolist()


def main() -> None:
    # 1. 固定随机种子。
    torch.manual_seed(2026)

    # 2. 若 CUDA 可用就用 GPU，否则自动使用 CPU。
    device = select_device()

    # 3. 构造 X。形状 [1,4,8] 分别表示：1 句话、4 个词、每个词 8 个特征。
    x = torch.randn(1, len(TOKENS), 8, device=device)

    # 4. 实例化 attention.py 中定义的类，并移到同一设备。
    model = SingleHeadSelfAttention(embed_dim=8).to(device).eval()

    # 5. 前向运行。inference_mode 表示本步骤只观察输出，不计算训练所需梯度。
    with torch.inference_mode():
        result = model(x)

    # 6. 自动验收：context 应和输入同形；softmax 后每行权重之和应约等于 1。
    row_sums = result["weights"].sum(dim=-1)
    row_sum_error = (row_sums - 1).abs().max().item()

    # 用第一行权重手工加权四个 Value，验证它等于模型返回的第 0 个 context。
    # [4] @ [4, 8] -> [8]：四个标量权重分别乘四个 8 维 Value 后逐维相加。
    manual_context_0 = result["weights"][0, 0] @ result["value"][0]
    manual_context_error = (
        manual_context_0 - result["context"][0, 0]
    ).abs().max().item()

    assert result["context"].shape == x.shape
    assert row_sum_error < 1e-6
    assert manual_context_error < 1e-6

    # 7. 保存结构化输出。终端用于课堂观察，JSON 用于课后复查精确结果。
    save_json("step01_single_head.json", {
        "status": "PASS",
        "tokens": TOKENS,
        "input_shape": list(x.shape),
        "q_shape": list(result["query"].shape),
        "scores_shape": list(result["scores"].shape),
        "context_shape": list(result["context"].shape),
        "attention_weights": rounded(result["weights"][0]),
        "value_vectors": rounded(result["value"][0]),
        "context_first_token": rounded(result["context"][0, 0]),
        "manual_context_max_error": manual_context_error,
        "row_sum_max_error": row_sum_error,
    })

    print("[Step 01] 单头缩放点积自注意力")
    print(f"tokens: {TOKENS}")
    print(f"device: {device}")
    print(f"X/Q/K/V shape: {tuple(x.shape)}  # [B=1, L=4, D=8]")
    print(f"scores/weights shape: {tuple(result['weights'].shape)}")
    print("attention weights（行=Query，列=Key；每行之和为 1）:")
    print(result["weights"][0].detach().cpu().round(decimals=4))
    print("Value vectors（四行依次对应：学生、通过、注意力、建模）:")
    print(result["value"][0].detach().cpu().round(decimals=4))
    print("first-token context（第 0 行权重对四个 Value 加权求和）:")
    print(result["context"][0, 0].detach().cpu().round(decimals=4))
    print(f"manual context max error: {manual_context_error:.3e}")
    print(f"row-sum max error: {row_sum_error:.3e}")
    print("checkpoint: PASS")


if __name__ == "__main__":
    main()

