# 教学说明：本文件用于Step 04：离线加载已训练的微型模型，展示五组句子补全概率。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 04：离线加载已训练的微型模型，展示五组句子补全概率。
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import torch

from common import ASSET_DIR, MODEL_DIR, ensure_dirs, save_json
from completion_data import CANDIDATES, EVALUATION_PROMPTS, encode
from completion_model import AttentionCompletionClassifier


CHECKPOINT_PATH = MODEL_DIR / "toy_attention_completion.pt"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


def load_trained_model() -> tuple[AttentionCompletionClassifier, dict, dict[str, int]]:
    """读取本地权重和元数据，按训练时完全相同的结构重建模型。"""
    if not CHECKPOINT_PATH.is_file():
        raise FileNotFoundError(
            f"缺少 {CHECKPOINT_PATH}；请先运行 classroom/tools/train_toy_completion.py"
        )
    # weights_only=True 禁止 checkpoint 反序列化任意 Python 对象，更适合分发。
    checkpoint = torch.load(CHECKPOINT_PATH, map_location="cpu", weights_only=True)
    config = checkpoint["model_config"]
    # Python 文件保存“网络结构”，.pt 文件保存训练参数；二者缺一不可。
    model = AttentionCompletionClassifier(**config)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    id_to_word = checkpoint["id_to_word"]
    word_to_id = {word: index for index, word in enumerate(id_to_word)}
    return model, checkpoint, word_to_id


def predict(model, prompt: str, word_to_id: dict[str, int]) -> dict:
    """编码一条恰好含 4 个 token 的提示、前向运行，再整理成便于阅读的结果。"""
    input_ids = torch.tensor([encode(prompt, word_to_id)], dtype=torch.long)
    with torch.inference_mode():
        result = model(input_ids)
    probabilities = result["probabilities"][0]
    predicted_index = int(probabilities.argmax())
    return {
        "prompt": prompt,
        "predicted": CANDIDATES[predicted_index],
        "probabilities": {
            word: round(float(probabilities[index]), 6)
            for index, word in enumerate(CANDIDATES)
        },
        # 每个头中，最后一个 Query 对四个输入词的注意力，形状 [H,4]。
        "last_query_attention": result["attention_weights"][0, :, -1, :].tolist(),
    }


def plot_probabilities(rows: list[dict], path: Path) -> None:
    """画概率条形图；它直接回答“模型认为哪个补全词更可能”。"""
    figure, axes = plt.subplots(len(rows), 1, figsize=(10, 12), sharex=True)
    colors = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756"]
    for axis, row in zip(axes, rows):
        values = [row["probabilities"][word] for word in CANDIDATES]
        bars = axis.bar(CANDIDATES, values, color=colors)
        axis.set_ylim(0, 1.02)
        axis.set_ylabel("概率")
        axis.set_title(f'{row["prompt"]} ……（预测：{row["predicted"]}）')
        for bar, value in zip(bars, values):
            axis.text(bar.get_x() + bar.get_width() / 2, value + 0.02,
                      f"{value:.3f}", ha="center")
    figure.suptitle("自实现多头注意力句子补全：五个候选词概率")
    figure.tight_layout()
    figure.savefig(path, dpi=170)
    plt.close(figure)


def main() -> None:
    ensure_dirs()
    model, checkpoint, word_to_id = load_trained_model()
    # 连续运行五种语义场景，避免只展示一个“我喜欢机器学习”简单例子。
    rows = []
    for prompt, expected in EVALUATION_PROMPTS:
        row = predict(model, prompt, word_to_id)
        row["expected"] = expected
        rows.append(row)

    figure_path = ASSET_DIR / "completion_probabilities.png"
    plot_probabilities(rows, figure_path)
    # 正确性验收紧跟结果：五条最高概率词都必须等于预期词。
    all_correct = all(row["predicted"] == row["expected"] for row in rows)
    if not all_correct:
        raise AssertionError("至少一条固定示例补全错误，请检查 checkpoint 与代码版本")

    save_json("step04_sentence_completion.json", {
        "status": "PASS", "mode": "offline inference from saved checkpoint",
        "checkpoint": str(CHECKPOINT_PATH),
        "training_samples": checkpoint["training_samples"], "epochs": checkpoint["epochs"],
        "candidate_words": CANDIDATES, "evaluation": rows,
        "probability_figure": str(figure_path),
    })

    print("[Step 04] 加载已训练权重，离线运行句子补全")
    print(f"checkpoint: {CHECKPOINT_PATH}")
    print(f"training summary: {checkpoint['training_samples']} samples, "
          f"{checkpoint['epochs']} epochs, final_loss={checkpoint['final_loss']:.6f}")
    for row in rows:
        probability_text = ", ".join(
            f"{word}={row['probabilities'][word]:.4f}" for word in CANDIDATES
        )
        print(f"prompt: {row['prompt']} ……")
        print(f"  probabilities: {probability_text}")
        print(f"  predicted: {row['predicted']} | expected: {row['expected']}")
    print("result check: 5/5 correct")
    print("checkpoint: PASS")


if __name__ == "__main__":
    main()

