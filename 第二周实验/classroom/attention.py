"""从零实现单头和多头自注意力：本文件只定义网络层，直接运行它不会出现实验结果。
"""

from __future__ import annotations

import math

import torch
from torch import nn


class SingleHeadSelfAttention(nn.Module):
    """一个最小的单头自注意力层"""

    def __init__(self, embed_dim: int) -> None:
        """创建 Q、K、V 三组可训练投影；embed_dim 是每个词向量的维度。"""
        super().__init__()
        self.embed_dim = embed_dim
        # 虽然 Q、K、V 都来自同一个输入 X，但三个 Linear 拥有互不共享的参数。
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        """让序列中每个位置读取同一序列的全部位置，并返回中间量供课堂观察。"""
        # Linear 只改变最后一维，因此 Q、K、V 仍都是 [B, L, D]。
        query = self.q_proj(x)
        key = self.k_proj(x)
        value = self.v_proj(x)

        # 矩阵乘法 [B,L,D] @ [B,D,L] 得到 [B,L,L]：
        # 第 i 行第 j 列表示“位置 i 的 Query 与位置 j 的 Key 有多匹配”。
        scores = query @ key.transpose(-2, -1) / math.sqrt(self.embed_dim)

        # softmax 在最后一维做归一化：每一行都变成非负且总和为 1 的权重。
        weights = torch.softmax(scores, dim=-1)

        # [B,L,L] @ [B,L,D] -> [B,L,D]。
        # 每个输出位置都是所有 Value 的加权和，因此词与词之间发生了信息交换。
        context = weights @ value
        return {
            "query": query,
            "key": key,
            "value": value,
            "scores": scores,
            "weights": weights,
            "context": context,
        }


class MultiHeadSelfAttention(nn.Module):
    """多头：把 D 维表示拆到 H 个子空间并行计算，再拼回 D 维。
    """

    def __init__(self, embed_dim: int, num_heads: int) -> None:
        """embed_dim 必须能被 num_heads 整除，使每头维度 d_h=D/H 为整数。"""
        super().__init__()
        if embed_dim % num_heads != 0:
            raise ValueError("embed_dim 必须能够被 num_heads 整除")
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        # 与单头相同，先用三个 Linear 生成完整的 D 维 Q/K/V。
        # 与单头不同，后面不会直接用这 D 维做一次注意力，而是把它们拆给 H 个头。
        # 工程实现通常一次产生完整 D 维 Q/K/V，再 reshape；这样可并行计算所有头。
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        # 单头示例可直接把 Context 当作输出；多头在拼接后通常再做一次输出投影。
        # out_proj 让来自不同头的特征发生线性混合，而不只是机械地并排放在一起。
        self.out_proj = nn.Linear(embed_dim, embed_dim)

    def split_heads(self, x: torch.Tensor) -> torch.Tensor:
        """把 [B, L, D] 变成 [B, H, L, d_h]。"""
        batch_size, seq_len, _ = x.shape
        # 第一步只“分组”：
        # [B,L,D] -> [B,L,H,d_h]。
        # D=8、H=2 时，每个 token 原来的 8 个特征被顺序分成 [前4维] 和 [后4维]。
        x = x.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
        # 第二步只交换维度顺序：[B,L,H,d_h] -> [B,H,L,d_h]。
        # 把 H 放到 L 前面后，PyTorch 可在同一次矩阵乘法中并行处理全部注意力头。
        return x.transpose(1, 2)

    def merge_heads(self, x: torch.Tensor) -> torch.Tensor:
        """把 [B, H, L, d_h] 拼回 [B, L, D]。"""
        batch_size, _, seq_len, _ = x.shape
        # 先把维度顺序还原：[B,H,L,d_h] -> [B,L,H,d_h]。
        x = x.transpose(1, 2).contiguous()
        # 再把H个头的d_h 合成 D
        return x.reshape(batch_size, seq_len, self.embed_dim)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        """执行多头自注意力，并保留每一步张量以便验证与可视化。"""
        # 与单头相同：先把输入 X 分别投影为 Q、K、V，形状都是 [B,L,D]。
        query_projected = self.q_proj(x)
        key_projected = self.k_proj(x)
        value_projected = self.v_proj(x)


        # [B,L,D] -> [B,H,L,d_h]，本例是 [1,4,8] -> [1,2,4,4]。
        query = self.split_heads(query_projected)
        key = self.split_heads(key_projected)
        value = self.split_heads(value_projected)

        scores = query @ key.transpose(-2, -1) / math.sqrt(self.head_dim)
        weights = torch.softmax(scores, dim=-1)
        context_per_head = weights @ value

        # 把同一 token 在 H 个头中的结果按特征维首尾拼接，回到 [B,L,D]。
        merged_context = self.merge_heads(context_per_head)
        
        # 最后通过 out_proj 融合不同头的信息；数值会改变，但形状仍是 [B,L,D]。
        output = self.out_proj(merged_context)
        return {
            "query_projected": query_projected,
            "key_projected": key_projected,
            "value_projected": value_projected,
            "query": query,
            "key": key,
            "value": value,
            "scores": scores,
            "weights": weights,
            "context_per_head": context_per_head,
            "merged_context": merged_context,
            "output": output,
        }


def copy_weights_to_torch_mha(
    custom: MultiHeadSelfAttention,
    reference: nn.MultiheadAttention,
) -> None:
    """把自实现参数复制到官方层；只用于 Step 03 验证，不参与核心实现。"""
    with torch.no_grad():
        # 官方实现把 Q/K/V 三个权重按行拼在 in_proj_weight 中。
        reference.in_proj_weight.copy_(torch.cat([
            custom.q_proj.weight,
            custom.k_proj.weight,
            custom.v_proj.weight,
        ], dim=0))
        reference.in_proj_bias.copy_(torch.cat([
            custom.q_proj.bias,
            custom.k_proj.bias,
            custom.v_proj.bias,
        ], dim=0))
        reference.out_proj.weight.copy_(custom.out_proj.weight)
        reference.out_proj.bias.copy_(custom.out_proj.bias)
