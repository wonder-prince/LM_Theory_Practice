# 教学说明：本文件用于Step 01：核验 Linux、CUDA、vLLM、量化依赖和课程模型路径。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 01：核验 Linux、CUDA、vLLM、量化依赖和课程模型路径。"""

from __future__ import annotations

import json
import platform
import sys

import torch
import vllm

from course_paths import ADAPTER_DIR, MODEL_DIR, OUTPUT_DIR, write_json


def main() -> int:
    # vLLM 的 CUDA 版本要求 Linux；WSL 中 platform.system() 同样返回 Linux。
    if platform.system() != "Linux":
        raise RuntimeError("本周主实验必须在 Linux 或 WSL2 中运行，不能在原生 Windows 中运行。")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU 不可用，请先检查驱动、WSL GPU 透传或服务器 GPU 分配。")
    if not MODEL_DIR.is_dir():
        raise FileNotFoundError(f"未找到第六周基础模型：{MODEL_DIR}")
    if not ADAPTER_DIR.is_dir():
        raise FileNotFoundError(f"未找到第七周 LoRA 适配器：{ADAPTER_DIR}")

    # adapter_config.json 记录 LoRA 的秩 r；启动 vLLM 时 max_lora_rank 不得小于它。
    adapter_config_file = ADAPTER_DIR / "adapter_config.json"
    adapter_config = json.loads(adapter_config_file.read_text(encoding="utf-8"))
    lora_rank = int(adapter_config["r"])

    capability = torch.cuda.get_device_capability(0)
    gpu_memory_total_mib = round(
        torch.cuda.get_device_properties(0).total_memory / 1024**2
    )
    report = {
        "checkpoint": "PASS",
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "vllm": vllm.__version__,
        "torch": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "gpu": torch.cuda.get_device_name(0),
        "compute_capability": f"{capability[0]}.{capability[1]}",
        "gpu_memory_total_mib": gpu_memory_total_mib,
        "model_dir": str(MODEL_DIR),
        "adapter_dir": str(ADAPTER_DIR),
        "lora_rank": lora_rank,
    }
    out = OUTPUT_DIR / "step01_environment.json"
    write_json(out, report)

    print(f"platform: {report['platform']}")
    print(f"python: {report['python']}")
    print(f"vllm: {report['vllm']}")
    print(f"torch/cuda: {report['torch']} / {report['cuda_runtime']}")
    print(
        f"gpu: {report['gpu']} "
        f"({report['gpu_memory_total_mib']} MiB, "
        f"compute capability {report['compute_capability']})"
    )
    print(f"base model: {report['model_dir']}")
    print(f"LoRA adapter: {report['adapter_dir']} (r={lora_rank})")
    print("PASS step01 vLLM environment")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
