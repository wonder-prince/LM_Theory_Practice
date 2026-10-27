# 教学说明：本文件用于检查本周实验所需的环境、依赖和模型状态。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Record Week 6 hardware, CUDA, package, base-model, and input-data evidence."""

from __future__ import annotations

import ctypes
import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import winreg
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
MODEL = PROJECT / "models" / "Qwen2.5-0.5B-Instruct"


class MemoryStatus(ctypes.Structure):
    _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                ("total", ctypes.c_ulonglong), ("available", ctypes.c_ulonglong),
                ("total_page", ctypes.c_ulonglong), ("available_page", ctypes.c_ulonglong),
                ("total_virtual", ctypes.c_ulonglong), ("available_virtual", ctypes.c_ulonglong),
                ("available_extended", ctypes.c_ulonglong)]


def reg(path: str, name: str) -> str:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
        return str(winreg.QueryValueEx(key, name)[0]).strip()


def command(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return (result.stdout or result.stderr).strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    import torch
    from transformers import AutoConfig

    memory = MemoryStatus(); memory.length = ctypes.sizeof(MemoryStatus)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
    config = AutoConfig.from_pretrained(MODEL, local_files_only=True)
    weights = MODEL / "model.safetensors"
    disk = shutil.disk_usage(PROJECT.anchor)
    packages = {name: importlib.metadata.version(name) for name in
                ["torch", "transformers", "peft", "accelerate", "huggingface-hub", "safetensors"]}
    info = {
        "os": reg(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "ProductName"),
        "os_display_version": reg(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "DisplayVersion"),
        "os_build": platform.version(),
        "cpu": reg(r"HARDWARE\DESCRIPTION\System\CentralProcessor\0", "ProcessorNameString"),
        "logical_processors": int(os.environ.get("NUMBER_OF_PROCESSORS", "0")),
        "ram_total_gib": round(memory.total / 1024**3, 2),
        "ram_available_gib": round(memory.available / 1024**3, 2),
        "gpu": command(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]),
        "nvcc": command(["nvcc", "--version"]),
        "python": sys.version.split()[0], "python_executable": sys.executable,
        "torch_cuda_available": torch.cuda.is_available(), "torch_cuda_runtime": torch.version.cuda,
        "packages": packages,
        "base_model": {"repo": "Qwen/Qwen2.5-0.5B-Instruct", "model_type": config.model_type,
                       "revision": "7ae557604adf67be50417f59c2c2f167def9a775",
                       "hidden_size": config.hidden_size, "layers": config.num_hidden_layers,
                       "attention_heads": config.num_attention_heads,
                       "weight_bytes": weights.stat().st_size,
                       "weight_sha256": sha256_file(weights)},
        "c_drive_free_gib": round(disk.free / 1024**3, 2),
    }
    info["passed"] = torch.cuda.is_available() and config.model_type == "qwen2" and weights.stat().st_size == 988_097_824
    out = PROJECT / "outputs" / "environment.json"; out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False, indent=2))
    print("PASS Week 6 environment" if info["passed"] else "FAIL Week 6 environment")
    return 0 if info["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
