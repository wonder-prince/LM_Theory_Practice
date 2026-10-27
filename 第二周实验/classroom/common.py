"""第二周所有脚本共用的基础工具；把项目路径、模型位置、设备选择和 JSON 保存集中在这里，
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import torch


# common.py 位于“项目根目录/classroom”，所以 parents[1] 就是项目根目录。
# 所有输出目录都由项目根目录派生，学生移动整个项目后无需修改绝对路径。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOG_DIR = PROJECT_ROOT / "logs"
MODEL_DIR = PROJECT_ROOT / "models"
ASSET_DIR = PROJECT_ROOT / "assets"

# Hugging Face 官方仓库名称及其在本项目中的本地保存位置。
BERT_REPO_ID = "google-bert/bert-base-uncased"
GPT2_REPO_ID = "openai-community/gpt2"
BERT_LOCAL_DIR = MODEL_DIR / "google-bert_bert-base-uncased"
GPT2_LOCAL_DIR = MODEL_DIR / "openai-community_gpt2"


def ensure_dirs() -> None:
    """首次运行时创建输出目录；目录已存在时不会覆盖其中的文件。"""
    for path in (OUTPUT_DIR, LOG_DIR, MODEL_DIR, ASSET_DIR):
        path.mkdir(parents=True, exist_ok=True)


def select_device() -> torch.device:
    """优先使用可用的 NVIDIA CUDA，否则自动回退到 CPU。"""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def save_json(filename: str, data: dict[str, Any]) -> Path:
    """把结构化实验结果保存到 outputs，便于课后核对而不影响终端演示。"""
    ensure_dirs()
    path = OUTPUT_DIR / filename
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return path


def local_model_ready(path: Path) -> bool:
    """检查本地模型是否同时具备配置、分词器和权重三类必要文件。"""
    config_ok = (path / "config.json").is_file()
    tokenizer_ok = any((path / name).is_file() for name in (
        "tokenizer.json", "vocab.txt", "vocab.json"
    ))
    weights_ok = any((path / name).is_file() for name in (
        "model.safetensors", "pytorch_model.bin"
    ))
    return config_ok and tokenizer_ok and weights_ok


def model_size_mib(path: Path) -> float:
    """统计模型目录中全部文件的总大小，单位为 MiB。"""
    total = sum(p.stat().st_size for p in path.rglob("*") if p.is_file())
    return total / (1024**2)


def configure_offline_mode() -> None:
    """禁止 Hugging Face 访问网络，确保探索步骤只读取项目中的本地模型。"""
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
