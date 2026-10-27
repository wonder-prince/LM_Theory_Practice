# 教学说明：本文件用于定义“词嵌入 + 自实现注意力 + 分类头”的微型补全模型。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""定义“词嵌入 + 自实现注意力 + 分类头”的微型补全模型。

注意：MultiHeadSelfAttention 本身只输出上下文向量和注意力权重，
不会直接产生“下一个词”的概率。本文件增加嵌入层和分类头，
把上下文向量映射到五个候选词的 logits，再用 softmax 转成概率。
"""

from __future__ import annotations

import torch
from torch import nn

from attention import MultiHeadSelfAttention


class AttentionCompletionClassifier(nn.Module):
    """把四词提示映射为五个候选词的概率；仅用于教学，不是通用语言模型。"""

    def __init__(
        self,
        vocab_size: int,
        num_classes: int,
        max_length: int = 4,
        embed_dim: int = 32,
        num_heads: int = 4,
    ) -> None:
        # nn.Module 的子类必须先初始化父类，PyTorch 才能登记后续可训练参数。
        super().__init__()
        self.max_length = max_length

        # token_embedding：把离散词 id 变成 D 维向量，表示“这是哪个词”。
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        # position_embedding：给第 0~3 个位置不同向量，补充“词出现在哪里”。
        self.position_embedding = nn.Embedding(max_length, embed_dim)

        # 这里必须调用我们在 attention.py 中从零实现的多头自注意力。
        self.attention = MultiHeadSelfAttention(embed_dim, num_heads)

        # 注意力后会做残差相加与 LayerNorm；这是 Transformer 块的典型结构。
        self.norm1 = nn.LayerNorm(embed_dim)
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 2),
            nn.GELU(),
            nn.Linear(embed_dim * 2, embed_dim),
        )
        self.norm2 = nn.LayerNorm(embed_dim)

        # 分类头把最后一个位置的 D 维表示映射为五个未归一化分数 logits。
        self.classifier = nn.Linear(embed_dim, num_classes)

    def forward(self, input_ids: torch.Tensor) -> dict[str, torch.Tensor]:
        """input_ids=[B,4]；返回 logits、概率、注意力权重和隐藏状态。"""
        # 解包形状，B 可以变化，但本教学任务固定要求每条提示四个词。
        batch_size, seq_len = input_ids.shape
        if seq_len != self.max_length:
            raise ValueError(f"本教学模型要求每条提示恰好 {self.max_length} 个词")

        # 先产生 [0,1,2,3]，再复制成 B 行，与 input_ids 的批大小一致。
        positions = torch.arange(seq_len, device=input_ids.device)
        positions = positions.unsqueeze(0).expand(batch_size, -1)
        # 两种嵌入逐元素相加，得到 [B,4,D] 的初始隐藏表示。
        hidden = self.token_embedding(input_ids) + self.position_embedding(positions)

        # 调用 attention.py 中“从零实现”的多头自注意力，而不是官方封装。
        attention_result = self.attention(hidden)
        # 残差让原输入可直接流向后面；LayerNorm 稳定数值尺度。
        hidden = self.norm1(hidden + attention_result["output"])
        hidden = self.norm2(hidden + self.feed_forward(hidden))

        # 取第 4 个提示词（索引 -1）的隐藏表示，作为整句的上下文摘要。
        logits = self.classifier(hidden[:, -1, :])
        return {
            "logits": logits,
            # softmax 把五个 logits 转为和为 1 的候选词概率。
            "probabilities": torch.softmax(logits, dim=-1),
            "attention_weights": attention_result["weights"],
            "hidden_states": hidden,
        }
