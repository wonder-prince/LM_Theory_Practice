# 教学说明：本文件用于Step 05：从 Hugging Face 官方仓库下载 BERT 与 GPT-2 checkpoint。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 05：从 Hugging Face 官方仓库下载 BERT 与 GPT-2 checkpoint。
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import requests
from transformers import AutoConfig, AutoTokenizer

from common import (
    BERT_LOCAL_DIR,
    BERT_REPO_ID,
    GPT2_LOCAL_DIR,
    GPT2_REPO_ID,
    ensure_dirs,
    local_model_ready,
    model_size_mib,
    save_json,
)


MODEL_FILES = {
    BERT_REPO_ID: [
        "config.json", "tokenizer_config.json", "tokenizer.json", "vocab.txt",
        "model.safetensors", "README.md",
    ],
    GPT2_REPO_ID: [
        "config.json", "generation_config.json", "merges.txt", "tokenizer.json",
        "tokenizer_config.json", "vocab.json", "model.safetensors", "README.md",
    ],
}
MODEL_REVISIONS = {
    BERT_REPO_ID: "86b5e0934494bd15c9632b12f734a8a67f723594",
    GPT2_REPO_ID: "607a30d783dfa663caf39e06633721c8d4cfcd7e",
}


def download_file(repo_id: str, filename: str, local_dir: Path, endpoint: str) -> None:
    """下载一个固定 revision 的文件；已有完整文件直接复用，.part 支持续传。"""
    destination = local_dir / filename
    # 避免每次上课重复下载数百 MiB 权重。
    if destination.is_file() and destination.stat().st_size > 0:
        return
    local_dir.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    downloaded = temporary.stat().st_size if temporary.exists() else 0
    # 上次中断时从 .part 已有字节后继续；服务器若不支持 Range 会重新写入。
    headers = {"Range": f"bytes={downloaded}-"} if downloaded else {}
    revision = MODEL_REVISIONS[repo_id]
    url = f"{endpoint.rstrip('/')}/{repo_id}/resolve/{revision}/{filename}"
    print(f"GET {url}")
    with requests.get(url, headers=headers, stream=True, timeout=(20, 90)) as response:
        response.raise_for_status()
        mode = "ab" if downloaded and response.status_code == 206 else "wb"
        if mode == "wb":
            downloaded = 0
        expected = int(response.headers.get("content-length", "0")) + downloaded
        next_report = 10
        with temporary.open(mode) as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                file.write(chunk)
                downloaded += len(chunk)
                if expected:
                    percent = int(downloaded * 100 / expected)
                    if percent >= next_report:
                        print(f"  {filename}: {percent}%")
                        next_report += 10
    temporary.replace(destination)


def download_one(repo_id, local_dir, endpoint):
    """确保一套 checkpoint 文件齐全，并让 Transformers 做配置/分词器检查。"""
    if local_model_ready(local_dir):
        status = "already present"
    else:
        print(f"downloading {repo_id} -> {local_dir} via {endpoint}")
        for filename in MODEL_FILES[repo_id]:
            download_file(repo_id, filename, local_dir, endpoint)
        status = "downloaded"
    # local_files_only=True 是关键验证：这两行不得偷偷访问网络。
    AutoConfig.from_pretrained(local_dir, local_files_only=True)
    AutoTokenizer.from_pretrained(local_dir, local_files_only=True)
    if not local_model_ready(local_dir):
        raise RuntimeError(f"模型文件不完整：{local_dir}")
    return {"repo_id": repo_id, "revision": MODEL_REVISIONS[repo_id],
            "local_dir": str(local_dir),
            "status": status, "size_mib": round(model_size_mib(local_dir), 2)}


def main() -> None:
    # --model 允许教师只补下载缺失的一种模型；默认下载/检查二者。
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["all", "bert", "gpt2"], default="all")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("HF_ENDPOINT", "https://huggingface.co"),
        help="模型文件端点；默认官方地址，网络受限时可用 https://hf-mirror.com",
    )
    args = parser.parse_args()
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    ensure_dirs()
    rows = []
    if args.model in ("all", "bert"):
        rows.append(download_one(BERT_REPO_ID, BERT_LOCAL_DIR, args.endpoint))
    if args.model in ("all", "gpt2"):
        rows.append(download_one(GPT2_REPO_ID, GPT2_LOCAL_DIR, args.endpoint))
    save_json("step05_models.json", {"status": "PASS", "models": rows})
    print("[Step 05] Hugging Face 官方模型下载与本地完整性检查")
    for row in rows:
        print(f"{row['repo_id']}: {row['status']}, {row['size_mib']:.2f} MiB")
        print(f"local path: {row['local_dir']}")
    print("checkpoint: PASS")


if __name__ == "__main__":
    main()

