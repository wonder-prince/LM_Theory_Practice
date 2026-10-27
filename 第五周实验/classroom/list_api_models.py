# 教学说明：本文件用于查询当前 API Key 可见的模型列表，不打印或保存 API Key。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""查询当前 API Key 可见的模型列表，不打印或保存 API Key。"""

from __future__ import annotations

import argparse
import json
import os
from urllib.parse import urlparse

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List models visible to the configured API key")
    parser.add_argument(
        "--url",
        help="可选的模型列表地址；默认根据COMMERCIAL_API_URL推导",
    )
    return parser.parse_args()


def infer_models_url(chat_url: str) -> str:
    """按常见OpenAI兼容规则把chat/completions地址转换为models地址。"""
    marker = "/chat/completions"
    if marker in chat_url:
        return chat_url.split(marker, 1)[0] + "/models"
    parsed = urlparse(chat_url)
    return f"{parsed.scheme}://{parsed.netloc}/v1/models"


def main() -> None:
    """使用当前会话中的Key查询模型，不打印或写入Key。"""
    args = parse_args()
    api_key = os.environ.get("COMMERCIAL_API_KEY", "").strip()
    chat_url = os.environ.get("COMMERCIAL_API_URL", "").strip()
    if not api_key:
        raise RuntimeError("缺少COMMERCIAL_API_KEY")
    models_url = args.url or infer_models_url(chat_url)
    if not models_url:
        raise RuntimeError("请设置COMMERCIAL_API_URL或使用--url")

    # 只发送一次轻量 GET 请求；中转站若不支持该路由，应按其文档使用 --url。
    response = requests.get(
        models_url,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(f"模型列表请求失败 HTTP {response.status_code}: {response.text[:300]}")
    body = response.json()
    print(f"models endpoint: {models_url}")
    for item in body.get("data", []):
        print(item.get("id", "<missing id>"))
    print(f"visible models: {len(body.get('data', []))}")
    print("API key was used only for this request and was not printed or saved.")


if __name__ == "__main__":
    main()
