# 教学说明：本文件用于第七周：用 Optuna 的 TPE 贝叶斯优化搜索 LoRA 微调超参。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""第七周：用 Optuna 的 TPE 贝叶斯优化搜索 LoRA 微调超参。

为什么不用网格搜索：超参维度多、loss 平滑，网格点数随维度指数爆炸且不利用已跑结果。
前 3 个 trial 用于初始探索；之后 TPE 把历史试验按好坏分成两组，
按 l(x)/g(x) 最大化采样下一个点（近似最大化期望提升）。

用法（先安装 optuna）：
    python -s -m pip install optuna
    python -s .\\classroom\\search_hyperparams.py --trials 10 --limit 128 --epochs 3 --n-startup-trials 3
结果写入 outputs/hyperparam_search_report.json，含最优超参与每次 trial 明细。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import torch
from peft import LoraConfig, TaskType, get_peft_model
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer

from data_utils import SFTDataset, load_jsonl, make_collate

PROJECT = Path(__file__).resolve().parents[1]
# 这里的每个 trial 都会重新从同一个基座模型开始，保证比较的是超参而不是上一次的训练状态。
MODEL_DIR = PROJECT.parent / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
TRAIN = PROJECT.parent / "第六周实验" / "data" / "train.jsonl"
VAL = PROJECT.parent / "第六周实验" / "data" / "validation.jsonl"


def parse_args() -> argparse.Namespace:
    # limit 控制每个 trial 的训练样本数，max-length 控制单条样本允许的最长 token 数。
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--train", type=Path, default=TRAIN)
    parser.add_argument("--val", type=Path, default=VAL)
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--limit", type=int, default=128, help="每个 trial 用多少训练样本，控制单次耗时")
    parser.add_argument("--max-length", type=int, default=576)
    parser.add_argument("--seed", type=int, default=202606)
    parser.add_argument("--n-startup-trials", type=int, default=3,
                        help="TPE 初始随机探索轮数，之后进入引导阶段")
    return parser.parse_args()


def train_eval(args, lr, batch_size, r):
    # Optuna 每调用一次本函数，就完成一次“加载→训练→验证→释放”的完整实验。
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    # 每个 trial 都重新加载基座，保证不同超参之间没有共享梯度或适配器状态。
    base = AutoModelForCausalLM.from_pretrained(args.model_dir, local_files_only=True,
                                                torch_dtype=torch.float16, low_cpu_mem_usage=True).to(device)
    base.config.use_cache = False
    # r 是 LoRA 低秩维度；它会改变可训练参数量，但不会解冻基座模型。
    config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=r, lora_alpha=16, lora_dropout=0.05,
                        target_modules=["q_proj", "v_proj"], bias="none")
    model = get_peft_model(base, config)
    # 训练只取 limit 条，验证仍使用完整 validation 集，作为不同 trial 的统一比较标准。
    train_items = load_jsonl(args.train)[:args.limit]
    val_items = load_jsonl(args.val)
    collate = make_collate(tokenizer.pad_token_id)
    train_dl = DataLoader(SFTDataset(tokenizer, train_items, args.max_length),
                          batch_size=batch_size, shuffle=True, collate_fn=collate)
    val_dl = DataLoader(SFTDataset(tokenizer, val_items, args.max_length),
                        batch_size=batch_size, shuffle=False, collate_fn=collate)
    # 优化器只接收 LoRA 参数；冻结的基座权重不会产生更新状态。
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=lr)
    loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-100)
    # trial 内部只使用训练子集更新 LoRA，结束后在完整 validation 上测量目标值。
    for _ in range(args.epochs):
        model.train()
        for batch in train_dl:
            # 每个 batch 先搬到同一设备，再执行前向、交叉熵、反向传播和参数更新。
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            logits = model(input_ids=ids, attention_mask=mask).logits
            sl, slb = logits[..., :-1, :].contiguous(), labels[..., 1:].contiguous()
            loss = loss_fct(sl.view(-1, sl.size(-1)), slb.view(-1))
            # 清空上一个 batch 的梯度；set_to_none 可减少无用的零张量分配。
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
    # 评估阶段关闭 dropout 和梯度，得到可比较的 validation loss。
    model.eval()
    vsum, vn = 0.0, 0
    with torch.inference_mode():
        for batch in val_dl:
            # 验证只做前向，不保留反向图，所以显存和耗时都低于训练阶段。
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            logits = model(input_ids=ids, attention_mask=mask).logits
            sl, slb = logits[..., :-1, :].contiguous(), labels[..., 1:].contiguous()
            vsum += loss_fct(sl.view(-1, sl.size(-1)), slb.view(-1)).item()
            vn += 1
    # 一个 trial 完成后显式删除模型并清理 CUDA 缓存，避免下一个 trial 继承显存占用。
    del model, base
    torch.cuda.empty_cache()
    return vsum / vn


def main() -> int:
    args = parse_args()
    try:
        import optuna
        from optuna.samplers import TPESampler
    except ImportError:
        print("请先安装：python -s -m pip install optuna", file=sys.stderr)
        return 1

    def objective(trial):
        # TPE 负责选择参数；本函数只负责把参数交给一次真实训练并返回 validation loss。
        lr = trial.suggest_float("lr", 1e-4, 1e-3, log=True)
        # 576-token 样本在 4GB 显存上不再搜索 batch_size=4，避免长样本批次 OOM。
        batch_size = trial.suggest_categorical("batch_size", [1, 2])
        r = trial.suggest_categorical("r", [4, 8, 16])
        start = time.perf_counter()
        val_loss = train_eval(args, lr, batch_size, r)
        trial.set_user_attr("seconds", round(time.perf_counter() - start, 1))
        return val_loss

    # 默认 n_startup_trials=3，前 3 个 trial 随机探索，之后 TPE 引导。
    # 固定 sampler 种子后，课堂可以复现同一组候选超参顺序。
    sampler = TPESampler(seed=args.seed, n_startup_trials=args.n_startup_trials)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=args.trials)
    # 报告同时保留最优结果和每个 trial 的状态，避免只看到“最优值”却无法追溯搜索过程。
    report = {
        "sampler": {"name": "TPE", "startup_trials": args.n_startup_trials},
        "epochs_per_trial": args.epochs,
        "train_subset_samples": min(args.limit, len(load_jsonl(args.train))),
        "validation_samples": len(load_jsonl(args.val)),
        "best_params": study.best_params,
        "best_val_loss": round(study.best_value, 5),
        "trials": [
            {"params": t.params, "val_loss": round(t.value, 5),
             "seconds": t.user_attrs.get("seconds"), "state": str(t.state)}
            for t in study.trials
        ],
        "note": "前3个 trial 初始探索，第4～10个由 TPE 根据历史验证 loss 引导；正式训练再用最优超参运行 Step 02",
    }
    out = PROJECT / "outputs" / "hyperparam_search_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"最优超参：{study.best_params}，验证 loss {study.best_value:.5f}")
    print("PASS hyperparameter search")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
