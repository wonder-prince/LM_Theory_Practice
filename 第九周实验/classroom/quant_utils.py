"""第九周共享工具：路径、模型加载、显存记录与报告写入。"""

from __future__ import annotations

import json
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
WEEK9 = Path(__file__).resolve().parents[1]
WORKSHOP = WEEK9.parent
MODEL_DIR = WORKSHOP / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
VAL_PATH = WORKSHOP / "第六周实验" / "data" / "validation.jsonl"
ADAPTER_DIR = WORKSHOP / "第七周实验" / "adapters" / "qwen05b-learning-companion-lora-finetuned"
OUTPUT_DIR = WEEK9 / "outputs"
MIXED_FP16_MODULES = [
    "model.layers.16.self_attn.v_proj",
    "model.layers.20.self_attn.v_proj",
    "model.layers.22.self_attn.v_proj",
    "model.layers.21.self_attn.v_proj",
    "model.layers.2.self_attn.v_proj",
]
# 该列表来自本组 Step 04 输出；条目数量由 --keep-fp16 N 决定，并不固定为 3。
# 各组应完整复制自己的 N 个结果，不能照抄示例中的层号。
# bitsandbytes 量化时跳过这些模块，使它们保留 FP16。
MIXED_SKIP_MODULES = ["lm_head", *MIXED_FP16_MODULES]


def set_seed(seed: int) -> None:
    """统一 Python、NumPy、PyTorch 与 CUDA 的随机种子。"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def synchronize() -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def reset_cuda_peak() -> None:
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()


def cuda_memory() -> dict[str, float | None]:
    """读取当前 CUDA 已分配、已保留与峰值显存，单位为 MiB。"""
    if not torch.cuda.is_available():
        return {"allocated_mib": None, "reserved_mib": None, "peak_allocated_mib": None}
    mib = 1024**2
    return {
        "allocated_mib": round(torch.cuda.memory_allocated() / mib, 2),
        "reserved_mib": round(torch.cuda.memory_reserved() / mib, 2),
        "peak_allocated_mib": round(torch.cuda.max_memory_allocated() / mib, 2),
    }


def result_name(mode: str) -> str:
    return mode


def load_tokenizer(model_dir: Path = MODEL_DIR):
    """从本地模型目录加载分词器，不访问网络。"""
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def load_tuned_model(
    mode: str,
    model_dir: Path = MODEL_DIR,
    adapter_dir: Path = ADAPTER_DIR,
):
    """加载相同基座与相同 LoRA；唯一自变量是基座权重表示。"""
    if not torch.cuda.is_available():
        raise RuntimeError("本实验的 bitsandbytes 4-bit 对照需要 CUDA GPU。")
    if mode not in {"fp16", "nf4", "fp4", "mixed"}:
        raise ValueError(f"不支持的模式：{mode}")

    kwargs = {
        "local_files_only": True,
        "low_cpu_mem_usage": True,
        "device_map": {"": 0},
    }
    if mode == "fp16":
        # FP16 组直接加载半精度基座，作为未量化基线。
        kwargs["torch_dtype"] = torch.float16
    else:
        # FP4、NF4 和 mixed 都使用 4-bit 线性层；mixed 额外跳过敏感模块。
        kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4" if mode == "mixed" else mode,
            bnb_4bit_compute_dtype=torch.float16,
            llm_int8_skip_modules=MIXED_SKIP_MODULES if mode == "mixed" else None,
        )

    reset_cuda_peak()
    started = time.perf_counter()
    base = AutoModelForCausalLM.from_pretrained(model_dir, **kwargs)
    # 四组都挂载同一个第七周 LoRA，保证唯一自变量是基座权重表示。
    model = PeftModel.from_pretrained(base, adapter_dir, local_files_only=True)
    model.eval()
    synchronize()
    load_seconds = time.perf_counter() - started
    return model, load_seconds


def model_footprint_mib(model) -> float:
    return round(model.get_memory_footprint() / 1024**2, 2)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
