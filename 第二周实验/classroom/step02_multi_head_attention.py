"""Step 02：运行多头自注意力，重点观察“拆头—并行—合并”的形状变化。
"""

from __future__ import annotations

import torch

from attention import MultiHeadSelfAttention
from common import save_json, select_device


TOKENS = ["学生", "通过", "注意力", "建模"]


def rounded(tensor: torch.Tensor) -> list:
    """把张量转为适合写入 JSON 的四位小数列表。"""
    return tensor.detach().cpu().round(decimals=4).tolist()


def main() -> None:
    # 1. 固定随机种子。
    torch.manual_seed(2026)
    device = select_device()

    # 2. X=[B,L,D]=[1,4,8]。文字只作标签，实际输入仍是 8 维随机向量。
    x = torch.randn(1, len(TOKENS), 8, device=device)

    # 3. D=8、H=2，所以每个头 d_h=D/H=4；D 不能被 H 整除时类会主动报错。
    model = MultiHeadSelfAttention(embed_dim=8, num_heads=2).to(device).eval()

    # 4. 调用 attention.py 的 forward，得到各中间张量；此处不训练。
    with torch.inference_mode():
        result = model(x)

    # 5. 先根据公式写出理论形状，再用 assert 自动检查实际形状。
    #    若 split_heads 的 reshape/transpose 顺序写错，这里会立刻失败。
    expected = {
        "qkv": (1, 2, 4, 4),
        "weights": (1, 2, 4, 4),
        "merged": (1, 4, 8),
        "output": (1, 4, 8),
    }
    assert tuple(result["query"].shape) == expected["qkv"]
    assert tuple(result["weights"].shape) == expected["weights"]
    assert tuple(result["merged_context"].shape) == expected["merged"]
    assert tuple(result["output"].shape) == expected["output"]

    # 6. 保存关键中间量，课后可在 outputs/step02_multi_head.json 中继续查看。
    save_json("step02_multi_head.json", {
        "status": "PASS",
        "tokens": TOKENS,
        "input_shape": list(x.shape),
        "input_token_0": rounded(x[0, 0]),
        "qkv_after_split_shape": list(result["query"].shape),
        "attention_weights_shape": list(result["weights"].shape),
        "merged_context_shape": list(result["merged_context"].shape),
        "output_shape": list(result["output"].shape),
        "query_token_0_before_split": rounded(result["query_projected"][0, 0]),
        "value_token_0_before_split": rounded(result["value_projected"][0, 0]),
        "query_token_0_head_0": rounded(result["query"][0, 0, 0]),
        "query_token_0_head_1": rounded(result["query"][0, 1, 0]),
        "head_0_weights": rounded(result["weights"][0, 0]),
        "head_1_weights": rounded(result["weights"][0, 1]),
        "context_token_0_head_0": rounded(result["context_per_head"][0, 0, 0]),
        "context_token_0_head_1": rounded(result["context_per_head"][0, 1, 0]),
        "merged_context_token_0": rounded(result["merged_context"][0, 0]),
        "output_first_token": rounded(result["output"][0, 0]),
    })

    print("[Step 02] 从单头扩展到多头自注意力")
    print(f"device: {device}")
    print(f"tokens: {TOKENS}")
    print(f"input: {tuple(x.shape)}  # [B=1, L=4, D=8]")
    print(f"Q after q_proj, before split_heads: {tuple(result['query_projected'].shape)}")
    print(f"Q/K/V after split_heads: {tuple(result['query'].shape)}")
    print(f"attention weights: {tuple(result['weights'].shape)}")
    print(f"context per head: {tuple(result['context_per_head'].shape)}")
    print(f"merged context: {tuple(result['merged_context'].shape)}")
    print(f"final output: {tuple(result['output'].shape)}")

    # 先并列观察 X、Q、V，避免把“拆头前的 Q”误认为原始输入或 Value。
    print("\n[变量对照] token 0（学生）的 X、Q、V")
    print("X input (8 维，尚未做 Q/K/V 投影):")
    print(x[0, 0].detach().cpu().round(decimals=4))
    print("Q after q_proj, before split_heads (8 维):")
    print(result["query_projected"][0, 0].detach().cpu().round(decimals=4))
    print("V after v_proj, before split_heads (8 维；与 Step 01 的 Value 相同):")
    print(result["value_projected"][0, 0].detach().cpu().round(decimals=4))

    print("\n[拆头演示] 把 token 0（学生）的 Q 拆成两个头")
    for head in range(model.num_heads):
        print(f"after split - head {head} (4 维):")
        print(result["query"][0, head, 0].detach().cpu().round(decimals=4))

    print("\n[合并演示] token 0（学生）的每头 Context")
    for head in range(model.num_heads):
        print(f"head {head} context (4 维):")
        print(result["context_per_head"][0, head, 0].detach().cpu().round(decimals=4))
    print("merged context（两个头的 Context 首尾拼接，8 维）:")
    print(result["merged_context"][0, 0].detach().cpu().round(decimals=4))

    print("after out_proj (8 维，形状不变但不同头的信息已线性混合):")
    print(result["output"][0, 0].detach().cpu().round(decimals=4))
    print("checkpoint: PASS")


if __name__ == "__main__":
    main()

