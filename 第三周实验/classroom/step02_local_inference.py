"""Step 02：把官方 Qwen2.5-7B Q4_K_M 模型加载到本机并完成一次回答。

本脚本同时记录加载前后的系统内存和 GPU 显存。它不只证明“能回答”，
还让我们看到 n_gpu_layers=16 时 CPU/GPU 混合部署的真实资源变化。
"""

from __future__ import annotations

import ctypes
import json
import subprocess
import time
from pathlib import Path

from windows_cuda_runtime import prepare_cuda_dll_search


# 所有输入和输出都由项目目录相对定位，避免把教师电脑上的绝对路径写进代码。
PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_DIR / "models" / "Qwen2.5-7B-Instruct-GGUF"
MODEL_PATH = MODEL_DIR / "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"
SECOND_SHARD = MODEL_DIR / "qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf"
OUTPUT_PATH = PROJECT_DIR / "outputs" / "step02_local_inference.json"


class MemoryStatus(ctypes.Structure):
    """对应 Windows API 的 MEMORYSTATUSEX 结构。"""

    _fields_ = [
        ("length", ctypes.c_ulong),
        ("memory_load", ctypes.c_ulong),
        ("total_physical", ctypes.c_ulonglong),
        ("available_physical", ctypes.c_ulonglong),
        ("total_page_file", ctypes.c_ulonglong),
        ("available_page_file", ctypes.c_ulonglong),
        ("total_virtual", ctypes.c_ulonglong),
        ("available_virtual", ctypes.c_ulonglong),
        ("available_extended_virtual", ctypes.c_ulonglong),
    ]


def available_ram_gib() -> float:
    """返回 Windows 当前可用物理内存，单位 GiB。"""

    status = MemoryStatus()
    status.length = ctypes.sizeof(MemoryStatus)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError("GlobalMemoryStatusEx 调用失败")
    return round(status.available_physical / 1024**3, 2)


def gpu_memory_mib() -> dict[str, int | str]:
    """使用 nvidia-smi 读取当前显存；不依赖额外 Python 库。"""

    result = subprocess.run(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.used,memory.total",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    name, used, total = [part.strip() for part in result.stdout.split(",")]
    return {"name": name, "used_mib": int(used), "total_mib": int(total)}


def snapshot() -> dict[str, object]:
    """把同一时刻的系统可用内存和 GPU 显存整理成一个字典。"""

    return {"available_ram_gib": available_ram_gib(), "gpu": gpu_memory_mib()}


def main() -> None:
    for path in (MODEL_PATH, SECOND_SHARD):
        if not path.is_file():
            raise FileNotFoundError(f"缺少模型分片：{path}")

    # 先处理 Windows DLL 搜索路径，再导入 CUDA 版 llama_cpp。
    prepare_cuda_dll_search()
    from llama_cpp import Llama, llama_supports_gpu_offload

    if not llama_supports_gpu_offload():
        raise RuntimeError("当前 llama-cpp-python 不支持 GPU offload，请检查 CUDA wheel。")

    # 在加载模型之前留下一次资源快照，加载后再测一次，两者之差就是本次实测增量。
    model_bytes = MODEL_PATH.stat().st_size + SECOND_SHARD.stat().st_size
    before = snapshot()
    print("[Step 02] 本地加载并运行 Qwen2.5-7B-Instruct")
    print(f"model files on disk: {model_bytes / 1024**3:.2f} GiB（两个 GGUF 分片）")
    print("deployment: Q4_K_M, n_ctx=2048, n_gpu_layers=16, CPU/GPU 混合推理")
    print(f"before load: {json.dumps(before, ensure_ascii=False)}", flush=True)

    load_started = time.perf_counter()
    # n_ctx 控制本次最多保留多少词元的上下文；n_gpu_layers=16 表示只把部分网络层
    # 放到 GPU，其余层留在 CPU/系统内存。chatml 是 Qwen Instruct 使用的对话模板。
    model = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=2048,
        n_gpu_layers=16,
        n_threads=8,
        n_threads_batch=8,
        chat_format="chatml",
        verbose=False,
    )
    load_seconds = time.perf_counter() - load_started
    after = snapshot()
    ram_change = round(before["available_ram_gib"] - after["available_ram_gib"], 2)
    vram_change = after["gpu"]["used_mib"] - before["gpu"]["used_mib"]

    print(f"after load: {json.dumps(after, ensure_ascii=False)}")
    print(f"measured RAM increase: about {ram_change:.2f} GiB")
    print(f"measured VRAM increase: about {vram_change} MiB")
    print(f"load time: {load_seconds:.2f} s", flush=True)

    prompt = "请用三条编号短句说明：为什么4GB显存运行7B模型时要使用4位量化和CPU/GPU混合推理？"
    generation_started = time.perf_counter()
    
    # system 规定回答身份和格式，user 提供本轮实际问题。这里执行的是推理，不会训练权重。
    response = model.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "你是《大模型原理与应用》课程的中文助教。只输出三条编号短句，每条不超过35个汉字，总计不超过120个汉字。",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=220,
        temperature=0.1,
        top_p=0.9,
        seed=42,
    )
    generation_seconds = time.perf_counter() - generation_started
    # OpenAI 兼容响应把最终文本放在 choices[0].message.content 中。
    answer = response["choices"][0]["message"]["content"].strip()
    usage = response.get("usage", {})
    completion_tokens = int(usage.get("completion_tokens", 0))
    speed = completion_tokens / generation_seconds if generation_seconds else 0.0

    # 同时打印真实问题与回答，使终端输出能够直接证明模型完成了前向生成。
    print("\nuser:", prompt)
    print("assistant:", answer)
    print(f"usage: {usage}")
    print(f"generation: {generation_seconds:.2f} s, {speed:.2f} token/s")

    # 保存完整实验记录，便于课后核对模型参数、资源变化、输入和输出。
    record = {
        "model": "Qwen2.5-7B-Instruct-GGUF",
        "parameters": "7.62B",
        "quantization": "Q4_K_M",
        "model_bytes": model_bytes,
        "n_ctx": 2048,
        "n_gpu_layers": 16,
        "resources_before": before,
        "resources_after_load": after,
        "measured_ram_increase_gib": ram_change,
        "measured_vram_increase_mib": vram_change,
        "load_seconds": round(load_seconds, 2),
        "prompt": prompt,
        "answer": answer,
        "usage": usage,
        "generation_seconds": round(generation_seconds, 2),
        "completion_tokens_per_second": round(speed, 2),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {OUTPUT_PATH.relative_to(PROJECT_DIR)}")
    print("checkpoint: PASS（7B模型完成本地前向生成）")


if __name__ == "__main__":
    main()
