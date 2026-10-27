# 教学说明：本文件用于第七周环境检查：CUDA、依赖、模型与数据是否就绪。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""第七周环境检查：CUDA、依赖、模型与数据是否就绪。"""

from __future__ import annotations

import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
# 模型和数据沿用第六周的产物；这里用绝对路径检查，避免从不同目录启动时找错文件。
MODEL_DIR = PROJECT.parent / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
TRAIN = PROJECT.parent / "第六周实验" / "data" / "train.jsonl"
VAL = PROJECT.parent / "第六周实验" / "data" / "validation.jsonl"


def main() -> int:
    # 依赖在函数内部导入，便于环境缺包时直接看到具体的 ImportError。
    import torch
    import matplotlib

    # 版本信息与文件、CUDA 状态一起写入报告，方便判断“代码问题”还是“环境未就绪”。
    packages = {name: importlib.metadata.version(name) for name in
                ["torch", "transformers", "peft", "accelerate", "matplotlib"]}
    info = {
        "torch_cuda_available": torch.cuda.is_available(),
        "torch_cuda_runtime": torch.version.cuda,
        "packages": packages,
        "model_dir_ok": MODEL_DIR.is_dir() and (MODEL_DIR / "model.safetensors").is_file(),
        "train_file_ok": TRAIN.is_file(),
        "val_file_ok": VAL.is_file(),
        "model_dir": str(MODEL_DIR),
        "train_file": str(TRAIN),
        "val_file": str(VAL),
    }
    # 四项条件同时满足才允许进入后续训练；依赖版本本身只记录，不单独决定 PASS。
    info["passed"] = (info["torch_cuda_available"] and info["model_dir_ok"]
                      and info["train_file_ok"] and info["val_file_ok"])
    # 输出 JSON 既供人查看，也供后续排查脚本直接读取。
    out = PROJECT / "outputs" / "environment.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False, indent=2))
    print("PASS Week 7 environment" if info["passed"] else "FAIL Week 7 environment")
    return 0 if info["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
