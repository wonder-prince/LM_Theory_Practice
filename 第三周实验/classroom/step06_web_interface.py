# 教学说明：本文件用于Step 06：启动一个复用本地模型 API 的浏览器交互界面。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 06：启动一个复用本地模型 API 的浏览器交互界面。

本脚本不加载 GGUF，也不创建第二个模型实例。它只提供网页，并把浏览器的
JSON 请求转发给已经运行在 127.0.0.1:18080 的 OpenAI 兼容 API。
"""

from __future__ import annotations

import argparse
import json
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_DIR = Path(__file__).resolve().parents[1]
WEB_FILE = Path(__file__).resolve().parent / "web" / "index.html"
OUTPUT_PATH = PROJECT_DIR / "outputs" / "step06_web_response.json"
DEFAULT_API_BASE = "http://127.0.0.1:18080"
DEFAULT_WEB_HOST = "127.0.0.1"
DEFAULT_WEB_PORT = 18081
MAX_BODY_BYTES = 128 * 1024


def api_request(api_base: str, path: str, payload: dict | None = None) -> tuple[int, bytes]:
    """Send one request to the local model server without adding a web framework."""

    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    request = Request(f"{api_base.rstrip('/')}{path}", data=body, headers=headers)
    try:
        with urlopen(request, timeout=180) as response:
            return response.status, response.read()
    except HTTPError as error:
        return error.code, error.read()


class WebHandler(BaseHTTPRequestHandler):
    api_base = DEFAULT_API_BASE

    def log_message(self, format: str, *args) -> None:
        print(f"[Web] {self.address_string()} - {format % args}")

    def send_bytes(self, status: int, content_type: str, content: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status: int, payload: dict) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_bytes(status, "application/json; charset=utf-8", content)

    def do_GET(self) -> None:
        if self.path == "/":
            try:
                self.send_bytes(HTTPStatus.OK, "text/html; charset=utf-8", WEB_FILE.read_bytes())
            except OSError as error:
                self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(error)})
            return

        if self.path == "/api/status":
            try:
                status, body = api_request(self.api_base, "/v1/models")
                if status >= 400:
                    self.send_json(status, {"ready": False, "upstream": body.decode("utf-8", "replace")})
                else:
                    self.send_json(HTTPStatus.OK, {"ready": True, "models": json.loads(body)})
            except (URLError, TimeoutError, json.JSONDecodeError) as error:
                self.send_json(HTTPStatus.BAD_GATEWAY, {"ready": False, "error": str(error)})
            return

        self.send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path != "/api/chat":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY_BYTES:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid request body size"})
            return

        try:
            payload = json.loads(self.rfile.read(length))
            messages = payload.get("messages")
            if not isinstance(messages, list) or not messages:
                raise ValueError("messages must be a non-empty list")
            request_payload = {
                "model": payload.get("model", "qwen2.5-7b-local"),
                "messages": messages,
                "max_tokens": int(payload.get("max_tokens", 160)),
                "temperature": float(payload.get("temperature", 0.2)),
            }
            started = time.perf_counter()
            status, body = api_request(self.api_base, "/v1/chat/completions", request_payload)
            elapsed = time.perf_counter() - started
            # 保存浏览器实际发送的消息、上游 API 完整响应和耗时，便于课堂对照三层数据流。
            try:
                upstream_response = json.loads(body)
            except json.JSONDecodeError:
                upstream_response = {"raw_text": body.decode("utf-8", "replace")}
            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT_PATH.write_text(
                json.dumps(
                    {
                        "web_route": "/api/chat",
                        "model_api": f"{self.api_base}/v1/chat/completions",
                        "request": request_payload,
                        "response": upstream_response,
                        "request_seconds": round(elapsed, 2),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            content_type = "application/json; charset=utf-8"
            self.send_bytes(status, content_type, body)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except (URLError, TimeoutError) as error:
            self.send_json(HTTPStatus.BAD_GATEWAY, {"error": f"Local model API unavailable: {error}"})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve a browser UI for the local model API")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--host", default=DEFAULT_WEB_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_WEB_PORT)
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not WEB_FILE.is_file():
        raise FileNotFoundError(f"Web page not found: {WEB_FILE}")

    WebHandler.api_base = args.api_base.rstrip("/")
    server = ThreadingHTTPServer((args.host, args.port), WebHandler)
    address = f"http://{args.host}:{args.port}"
    print("[Step 06] Local Web interface")
    print(f"browser: {address}")
    print(f"model API: {WebHandler.api_base}")
    print("The web process does not load the model; it forwards requests to the API.")
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nweb server stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
