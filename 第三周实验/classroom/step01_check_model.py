# 教学说明：本文件用于Step 01：检查官方 Qwen2.5-7B-Instruct GGUF 分片与 SHA-256。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 01：检查官方 Qwen2.5-7B-Instruct GGUF 分片与 SHA-256。

本脚本只读取文件，不加载模型。它回答三个部署前问题：
1. 下载的是不是大纲要求的 7B 级模型；
2. 两个 Q4_K_M 分片是否齐全；
3. 文件是否在下载或复制过程中损坏。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


# 根据脚本自身位置寻找项目目录，学生复制整个“第三周实验”文件夹后无需修改绝对路径。
PROJECT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_DIR / "models" / "Qwen2.5-7B-Instruct-GGUF"
MANIFEST_PATH = MODEL_DIR / "download_manifest.json"


def sha256(path: Path) -> str:
    """分块读取大文件，避免一次把 4 GB 模型读入内存。"""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(16 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    # 清单记录模型来源、固定版本、文件大小和正确的 SHA-256，是后续校验的依据。
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(f"缺少模型清单：{MANIFEST_PATH}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print("[Step 01] 检查官方 7B 模型文件")
    print(f"official source: {manifest['source']}")
    print(f"revision: {manifest['revision']}")
    print(f"parameters: {manifest['model_parameters']}")
    print(f"quantization: {manifest['quantization']}")

    total_bytes = 0
    for record in manifest["files"]:
        # 对每个 GGUF 分片分别检查“文件存在、大小一致、哈希一致”。
        path = MODEL_DIR / record["file"]
        if not path.is_file():
            raise FileNotFoundError(f"缺少模型分片：{path}")
        actual_size = path.stat().st_size
        actual_hash = sha256(path)
        size_ok = actual_size == record["bytes"]
        hash_ok = actual_hash.lower() == record["sha256"].lower()
        print(f"\nfile: {path.name}")
        print(f"size: {actual_size:,} bytes ({actual_size / 1024**3:.3f} GiB)")
        print(f"sha256: {actual_hash}")
        print(f"check: {'PASS' if size_ok and hash_ok else 'FAIL'}")
        if not size_ok or not hash_ok:
            raise RuntimeError(f"模型分片校验失败：{path.name}")
        total_bytes += actual_size

    print(f"\ntotal on disk: {total_bytes:,} bytes")
    print(f"decimal size: {total_bytes / 1000**3:.2f} GB")
    print(f"binary size: {total_bytes / 1024**3:.2f} GiB")
    print("checkpoint: PASS（两个官方 Q4_K_M 分片完整）")


if __name__ == "__main__":
    main()
