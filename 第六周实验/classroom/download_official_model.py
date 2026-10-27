# 教学说明：本文件用于下载并校验课程指定的官方模型。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Download or verify the pinned official Qwen 0.5B Transformers checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from huggingface_hub import snapshot_download


PROJECT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT / "models" / "Qwen2.5-0.5B-Instruct"
REPO = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
REQUIRED = ["config.json", "generation_config.json", "merges.txt", "model.safetensors",
            "tokenizer.json", "tokenizer_config.json", "vocab.json"]
EXPECTED_WEIGHT_BYTES = 988_097_824
EXPECTED_WEIGHT_SHA256 = "fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if not args.verify_only:
        snapshot_download(repo_id=REPO, revision=REVISION, local_dir=MODEL_DIR,
                          allow_patterns=[*REQUIRED, "README.md"])
    missing = [name for name in REQUIRED if not (MODEL_DIR / name).is_file()]
    weights = MODEL_DIR / "model.safetensors"
    digest = sha256_file(weights) if weights.is_file() else "MISSING"
    report = {"passed": not missing and weights.stat().st_size == EXPECTED_WEIGHT_BYTES and digest == EXPECTED_WEIGHT_SHA256,
              "repo_id": REPO, "revision": REVISION, "local_dir": str(MODEL_DIR), "missing": missing,
              "weight_bytes": weights.stat().st_size if weights.is_file() else 0, "weight_sha256": digest}
    out = PROJECT / "outputs" / "model_verification.json"; out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PASS pinned official base model" if report["passed"] else "FAIL base model")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
