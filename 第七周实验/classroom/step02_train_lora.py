"""Step 02：手写 LoRA 训练循环（不用 Trainer），输出 Loss 曲线并保存适配器。

训练要点：
- 只用"回答"部分计算 loss（labels 中指令/输入区置 -100）。
- 默认超参：lr=3.688e-4、epochs=6、batch_size=1、max_length=576、r=16、alpha=16、q_proj+v_proj。
- 每 epoch 打印 train/val loss；用 matplotlib 画 Loss 曲线；保存 adapter。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from peft import LoraConfig, TaskType, get_peft_model
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer

from data_utils import SFTDataset, load_jsonl, make_collate

PROJECT = Path(__file__).resolve().parents[1]
# 这些路径分别指向第六周模型/数据、本周适配器和 Loss 曲线资产。
MODEL_DIR = PROJECT.parent / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
TRAIN = PROJECT.parent / "第六周实验" / "data" / "train.jsonl"
VAL = PROJECT.parent / "第六周实验" / "data" / "validation.jsonl"
ADAPTER_DIR = PROJECT / "adapters" / "qwen05b-learning-companion-lora-finetuned"
LOSS_PLOT = PROJECT / "assets" / "loss_curve.png"


def parse_args() -> argparse.Namespace:
    # 训练参数都可从命令行覆盖，便于学生比较学习率、LoRA 秩和 batch size。
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--train", type=Path, default=TRAIN)
    parser.add_argument("--val", type=Path, default=VAL)
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--lr", type=float, default=0.0004600214305049643)
    parser.add_argument("--max-length", type=int, default=576)
    parser.add_argument("--r", type=int, default=16)
    parser.add_argument("--alpha", type=int, default=16)
    parser.add_argument("--seed", type=int, default=202606)
    return parser.parse_args()


def gpu() -> str:
    # 记录训练前的显卡状态；峰值显存则由 torch.cuda 单独统计。
    r = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.used,memory.total",
                        "--format=csv,noheader"], capture_output=True, text=True, check=False)
    return (r.stdout or r.stderr).strip()


def main() -> int:
    args = parse_args()
    # 固定随机种子，让同一套数据和参数尽可能得到可比较的训练曲线。
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    # 基座权重保持冻结；后续只在其上注入 LoRA 适配器。
    base = AutoModelForCausalLM.from_pretrained(
        args.model_dir, local_files_only=True, torch_dtype=torch.float16, low_cpu_mem_usage=True
    ).to(device)
    # 训练时不需要生成缓存；关闭 use_cache 可以避免缓存与反向传播图同时占用显存。
    base.config.use_cache = False
    full_params = sum(p.numel() for p in base.parameters())

    # alpha/r 决定 LoRA 增量的缩放；目标层只选 q_proj、v_proj，控制训练参数量。
    config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=args.r, lora_alpha=args.alpha,
                        lora_dropout=0.05, target_modules=["q_proj", "v_proj"], bias="none")
    # PEFT 将可训练的低秩矩阵挂到目标线性层，原始模型参数仍保持冻结。
    model = get_peft_model(base, config)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)

    collate = make_collate(tokenizer.pad_token_id)
    train_items = load_jsonl(args.train)
    val_items = load_jsonl(args.val)
    # Dataset 负责编码和答案区 mask，collate 负责把不同长度样本拼成当前 batch。
    train_dl = DataLoader(SFTDataset(tokenizer, train_items, args.max_length),
                          batch_size=args.batch_size, shuffle=True, collate_fn=collate)
    val_dl = DataLoader(SFTDataset(tokenizer, val_items, args.max_length),
                        batch_size=args.batch_size, shuffle=False, collate_fn=collate)

    # 只有 requires_grad=True 的 LoRA 参数交给 AdamW，基座参数保持不变。
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=args.lr)
    loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-100)

    train_loss_history: list[float] = []
    val_loss_history: list[float] = []
    total_steps = 0
    started = time.perf_counter()
    peak_mib = 0.0
    before_gpu = gpu()
    torch.cuda.reset_peak_memory_stats() if torch.cuda.is_available() else None
    best_val = float("inf")
    best_epoch = 0
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)

    # 每个 epoch 都经历训练阶段和验证阶段；验证阶段不反向传播。
    for epoch in range(1, args.epochs + 1):
        model.train()
        epoch_loss = 0.0
        epoch_steps = 0
        for batch in train_dl:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            # 前向得到 logits，再用错位后的 labels 计算回答区交叉熵；提示区标签为 -100。
            outputs = model(input_ids=ids, attention_mask=mask)
            logits = outputs.logits
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
            # 三步分别清空旧梯度、反向传播、更新 LoRA 参数；每步只更新一次。
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            epoch_steps += 1
            total_steps += 1
            if torch.cuda.is_available():
                peak_mib = max(peak_mib, round(torch.cuda.max_memory_allocated() / 1024**2, 1))
        train_avg = epoch_loss / epoch_steps
        train_loss_history.append(round(train_avg, 5))

        # 切换到评估模式关闭 dropout，再用 inference_mode 节省验证阶段显存。
        model.eval()
        vsum = 0.0
        vn = 0
        with torch.inference_mode():
            for batch in val_dl:
                ids = batch["input_ids"].to(device)
                mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                logits = model(input_ids=ids, attention_mask=mask).logits
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = labels[..., 1:].contiguous()
                loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
                vsum += loss.item()
                vn += 1
        val_avg = vsum / vn
        val_loss_history.append(round(val_avg, 5))
        # 最佳检查点选择：本脚本会跑完所有 epoch，只保存验证 loss 最低的适配器。
        if val_avg < best_val:
            best_val = val_avg
            best_epoch = epoch
            model.save_pretrained(ADAPTER_DIR)
            tokenizer.save_pretrained(ADAPTER_DIR)
        elapsed = time.perf_counter() - started
        print(f"epoch {epoch}/{args.epochs}: train_loss={train_avg:.5f} val_loss={val_avg:.5f} "
              f"steps={total_steps} elapsed={elapsed:.1f}s")

    # Loss 曲线把每个 epoch 的训练/验证趋势保存为 PNG，供课堂观察是否过拟合。
    LOSS_PLOT.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 4))
    plt.plot(range(1, args.epochs + 1), train_loss_history, marker="o", label="train loss")
    plt.plot(range(1, args.epochs + 1), val_loss_history, marker="s", label="validation loss")
    plt.xlabel("epoch")
    plt.ylabel("loss (only on answer tokens)")
    plt.title("LoRA Fine-tuning Loss Curve")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(LOSS_PLOT, dpi=150)
    plt.close()

    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
    tokenizer.save_pretrained(ADAPTER_DIR)
    adapter_size = sum(p.stat().st_size for p in ADAPTER_DIR.iterdir() if p.is_file())
    total_seconds = round(time.perf_counter() - started, 2)

    # 最终 JSON 同时记录超参、参数量、损失、耗时和资产路径，便于第八周继续使用适配器。
    report = {
        "checkpoint": "PASS",
        "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
        "hyperparams": {"epochs": args.epochs, "batch_size": args.batch_size, "lr": args.lr,
                        "max_length": args.max_length, "r": args.r, "alpha": args.alpha,
                        "target_modules": ["q_proj", "v_proj"]},
        "train_samples": len(train_items), "validation_samples": len(val_items),
        "base_parameters": full_params, "trainable_parameters": trainable,
        "trainable_percent": round(100 * trainable / full_params, 4),
        "train_loss_per_epoch": train_loss_history,
        "val_loss_per_epoch": val_loss_history,
        "best_epoch": best_epoch,
        "best_val_loss": round(best_val, 5),
        "note": "已保存验证 loss 最低的 epoch 的适配器；本脚本采用最佳检查点选择，不在中途 break",
        "total_steps": total_steps,
        "total_seconds": total_seconds,
        "avg_step_seconds": round(total_seconds / max(total_steps, 1), 3),
        "peak_cuda_memory_mib": peak_mib,
        "gpu_before": before_gpu,
        "loss_plot": str(LOSS_PLOT),
        "adapter_directory": str(ADAPTER_DIR),
        "adapter_bytes": adapter_size,
    }
    out = PROJECT / "outputs" / "step02_train_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Loss 曲线已保存：{LOSS_PLOT}")
    print("PASS step02 train lora")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
