# 教学说明：本文件用于从 Hugging Face 官方仓库下载本周指定的两个 Q4_K_M 分片。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""从 Hugging Face 官方仓库下载本周指定的两个 Q4_K_M 分片。

学生拿到的课程项目已经包含模型时，脚本会复用本地文件；模型缺失时才联网。
huggingface_hub 会维护下载缓存并支持断点续传，不需要自己实现 HTTP 协议。
"""

from __future__ import annotations

from pathlib import Path

from huggingface_hub import hf_hub_download


# 下载脚本位于 classroom/tools，因此向上两级才是“第三周实验”项目目录。
PROJECT_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_DIR / "models" / "Qwen2.5-7B-Instruct-GGUF"
REPO_ID = "Qwen/Qwen2.5-7B-Instruct-GGUF"
REVISION = "bb5d59e06d9551d752d08b292a50eb208b07ab1f"
FILENAMES = (
    "qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
    "qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf",
)


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"official repository: https://huggingface.co/{REPO_ID}")
    print(f"pinned revision: {REVISION}")

    for filename in FILENAMES:
        # local_dir 把两个分片统一放入项目 models 目录；断线重试时可复用已有缓存。
        path = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            revision=REVISION,
            local_dir=MODEL_DIR,
        )
        size = Path(path).stat().st_size
        print(f"ready: {filename} ({size / 1024**3:.3f} GiB)")

    print("下载完成。请运行 classroom\\step01_check_model.py 校验 SHA-256。")


if __name__ == "__main__":
    main()
