"""课堂训练步骤：训练微型补全模型并保存本地 checkpoint。

学生用 5×10=50 条小样本在 CPU 上训练，并把网络参数、词表和模型配置保存为
models/toy_attention_completion.pt。Step 04 随后加载刚生成的权重并进行离线推理。
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn

# 本文件位于 classroom/tools；把 classroom 加入导入路径才能读取课程模块。
CLASSROOM_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CLASSROOM_DIR))

from common import MODEL_DIR, ensure_dirs  # noqa: E402
from completion_data import (  # noqa: E402
    CANDIDATES, EVALUATION_PROMPTS, build_vocabulary, encode, make_training_tensors,
)
from completion_model import AttentionCompletionClassifier  # noqa: E402


CHECKPOINT_PATH = MODEL_DIR / "toy_attention_completion.pt"


def set_seed(seed: int = 2026) -> None:
    """固定 Python、NumPy 和 PyTorch 的随机数，使课堂输出可以复现。"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def main() -> None:
    ensure_dirs()
    set_seed()

    # build_vocabulary 建立“文本 token -> 整数 id”的映射；训练张量中，
    # inputs的形状是 [50, 4]，表示 50 条样本、每条 4 个 token；
    # 每个整数标签对应“学习、下雨、健康、阅读、回家”中的一个候选词。
    word_to_id, id_to_word = build_vocabulary()
    inputs, labels = make_training_tensors(word_to_id)

    # 下面的配置同时决定词嵌入表、注意力层和五分类输出层的大小。
    # embed_dim=32、num_heads=4 表示每个 token 用 32 维向量表示，并拆成
    # 4 个注意力头；每个头处理 8 维特征。
    model_config = {
        "vocab_size": len(id_to_word), "num_classes": len(CANDIDATES),
        "max_length": 4, "embed_dim": 32, "num_heads": 4,
    }
    model = AttentionCompletionClassifier(**model_config)

    # AdamW 根据反向传播得到的梯度更新参数。
    # CrossEntropyLoss 接收模型输出的5 个原始分数（logits）与正确类别 id；
    # label_smoothing=0.1 避免模型把训练样本的正确类别推到绝对 100%，因此最终概率通常约为 0.92。
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.012, weight_decay=0.001)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    print("[Step 04A] 课堂训练微型补全模型（CPU）")
    start = time.perf_counter()
    losses = []
    model.train()
    for epoch in range(1, 501):
        # 一个 epoch 会把全部 50 条样本同时送入模型：
        # 1）清除上一轮梯度；2）前向得到 [50,5] logits；
        # 3）计算五分类损失；4）反向求梯度；5）让优化器更新参数。
        optimizer.zero_grad()
        result = model(inputs)
        loss = criterion(result["logits"], labels)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
        if epoch in (1, 100, 200, 300, 400, 500):
            accuracy = (result["logits"].argmax(-1) == labels).float().mean()
            print(f"epoch {epoch:>3}: loss={loss.item():.6f}, accuracy={accuracy:.3f}")

    # 训练后切换到 eval 模式，并用未参与反向传播的固定示例检查五类语义。
    # torch.inference_mode() 会关闭梯度记录，减少内存占用并加快验证。
    model.eval()
    correct = 0
    with torch.inference_mode():
        for prompt, expected in EVALUATION_PROMPTS:
            ids = torch.tensor([encode(prompt, word_to_id)])
            predicted = CANDIDATES[int(model(ids)["logits"].argmax(-1))]
            correct += int(predicted == expected)
    if correct != len(EVALUATION_PROMPTS):
        raise AssertionError(f"训练后固定示例仅 {correct}/5 正确，不保存 checkpoint")

    elapsed = time.perf_counter() - start

    # checkpoint 不只保存权重，还保存重新创建网络所需的配置、词表、候选词
    # 顺序和训练摘要。step04_sentence_completion.py 先按 model_config 创建同样
    # 的网络，再把 model_state_dict 中的已训练参数装回去。
    torch.save({
        "format_version": 1, "model_state_dict": model.state_dict(),
        "model_config": model_config, "id_to_word": id_to_word,
        "candidate_words": CANDIDATES, "training_samples": int(inputs.shape[0]),
        "epochs": 500, "initial_loss": losses[0], "final_loss": losses[-1],
        "fixed_examples_correct": correct,
    }, CHECKPOINT_PATH)
    print(f"saved: {CHECKPOINT_PATH}")
    print(f"size: {CHECKPOINT_PATH.stat().st_size / 1024:.1f} KiB")
    print(f"elapsed: {elapsed:.2f} s, fixed examples: {correct}/5")
    print("checkpoint: PASS")


if __name__ == "__main__":
    main()

