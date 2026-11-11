"""第十周各步骤共用的相对路径与 JSON 写入工具。"""

from __future__ import annotations

import json
import os
from pathlib import Path


# classroom 位于“项目工作坊/第十周实验/classroom”。向上两级即可回到项目工作坊，
# 因此复制整个“项目工作坊”后不需要修改任何用户名或盘符。
WORKSHOP_DIR = Path(__file__).resolve().parents[2]

# 如服务器上的文件不在默认位置，可通过环境变量覆盖；未设置时沿用课程相对目录。
MODEL_DIR = Path(
    os.environ.get(
        "COURSE_MODEL_DIR",
        WORKSHOP_DIR / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct",
    )
).expanduser().resolve()
ADAPTER_DIR = Path(
    os.environ.get(
        "COURSE_ADAPTER_DIR",
        WORKSHOP_DIR
        / "第七周实验"
        / "adapters"
        / "qwen05b-learning-companion-lora-finetuned",
    )
).expanduser().resolve()

# Multi-LoRA 扩展同时使用第六周演示适配器和第七周微调适配器。
# 两者必须来自同一个基础模型；课堂交换适配器时可通过环境变量覆盖路径。
DEMO_ADAPTER_DIR = Path(
    os.environ.get(
        "COURSE_DEMO_ADAPTER_DIR",
        WORKSHOP_DIR
        / "第六周实验"
        / "adapters"
        / "qwen05b-learning-companion-lora-demo",
    )
).expanduser().resolve()
FINETUNED_ADAPTER_DIR = Path(
    os.environ.get("COURSE_FINETUNED_ADAPTER_DIR", ADAPTER_DIR)
).expanduser().resolve()
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

API_BASE = os.environ.get("COURSE_API_BASE", "http://127.0.0.1:8000").rstrip("/")
BASE_MODEL_NAME = "qwen05b-base"
LORA_MODEL_NAME = "learning-companion"
DEMO_LORA_MODEL_NAME = "group-a-demo"
FINETUNED_LORA_MODEL_NAME = "group-b-finetuned"


def write_json(path: Path, payload: dict) -> None:
    """以 UTF-8 写出结果，便于 WPS、记事本和 Python 继续读取。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
