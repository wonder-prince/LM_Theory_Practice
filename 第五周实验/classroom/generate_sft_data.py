"""第五周：调用商业 API，按参数批量生成并保存 SFT JSONL 数据。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests


# 所有课程资源都按脚本所在位置定位，而不是依赖当前 PowerShell 目录。
# 因此从“第五周实验”目录运行命令时，Prompt、Skill、数据和日志仍会写到固定位置。
PROJECT_DIR = Path(__file__).resolve().parents[1]
PROMPT_PATH = Path(__file__).resolve().parent / "prompt_template.txt"
SKILLS_DIR = Path(__file__).resolve().parent / "skills"
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"
ALLOWED_TYPES = {
    "foundation_deployment",
    "data_finetuning",
    "optimization_evaluation",
    "agent_development",
}
ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
BASE_SYSTEM_PROMPT = (
    "你是严谨的指令微调数据生成助手。"
    "必须遵守用户给出的字段、类别和 JSON 格式，不输出隐藏思维过程。"
)


def parse_args() -> argparse.Namespace:
    """读取生成数量、Skill、思考模式、续传和输出位置等课堂参数。"""
    parser = argparse.ArgumentParser(description="Generate SFT data with a commercial API")
    parser.add_argument("--count", type=int, required=True, help="目标数据量，例如10或500")
    parser.add_argument("--batch-size", type=int, default=10, help="每次API请求的条数")
    parser.add_argument("--output", type=Path, help="JSONL输出路径")
    parser.add_argument("--resume", action="store_true", help="从已有JSONL数量继续生成")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="可选：限制每批最大输出token；不指定时由服务商默认上限决定",
    )
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument(
        "--json-mode",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="要求兼容服务返回JSON对象；不兼容时可使用--no-json-mode",
    )
    parser.add_argument(
        "--thinking",
        action="store_true",
        help="按思考模式发送reasoning_effort并移除temperature；服务商开关由COMMERCIAL_API_EXTRA_JSON提供",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "high", "max"],
        default="low",
        help="思考模式强度；批量JSON建议先使用low",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=None,
        help="classroom/skills下的Skill目录名，可重复指定",
    )
    parser.add_argument("--dry-run", action="store_true", help="只显示组合后的Skill和Prompt，不调用API")
    return parser.parse_args()


def load_api_config() -> tuple[str, str, str, dict]:
    """从当前 PowerShell 会话读取 API 配置。"""
    # URL、Key 和模型名都由环境变量传入：代码可以发给学生，个人密钥不会被写入文件。
    api_url = os.environ.get("COMMERCIAL_API_URL", "").strip()
    api_key = os.environ.get("COMMERCIAL_API_KEY", "").strip()
    model = os.environ.get("COMMERCIAL_API_MODEL", "").strip()
    missing = [
        name
        for name, value in (
            ("COMMERCIAL_API_URL", api_url),
            ("COMMERCIAL_API_KEY", api_key),
            ("COMMERCIAL_API_MODEL", model),
        )
        if not value
    ]
    if missing:
        raise RuntimeError("缺少环境变量：" + ", ".join(missing))

    # 厂商专用参数使用一个 JSON 对象集中传入，例如百炼的 enable_thinking。
    # 这里先校验格式，防止把拼写错误的文本直接发送给远程接口。
    extra_text = os.environ.get("COMMERCIAL_API_EXTRA_JSON", "").strip()
    try:
        extra_payload = json.loads(extra_text) if extra_text else {}
    except json.JSONDecodeError as error:
        raise RuntimeError("COMMERCIAL_API_EXTRA_JSON不是合法JSON") from error
    if not isinstance(extra_payload, dict):
        raise RuntimeError("COMMERCIAL_API_EXTRA_JSON必须是JSON对象")
    return api_url, api_key, model, extra_payload


def load_skill(skill_name: str) -> tuple[str, str]:
    """读取一个本地 SKILL.md；Skill 只作为规则文本注入 system prompt。"""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.is_file():
        raise FileNotFoundError(f"Skill不存在：{skill_path}")
    # utf-8-sig 同时兼容普通UTF-8和旧PowerShell可能写入的BOM。
    return skill_name, skill_path.read_text(encoding="utf-8-sig")


def build_prompt(batch_index: int, batch_size: int, total_count: int) -> str:
    """将批次编号和数量填入 Prompt 模板，生成本次 user prompt。"""
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return (
        template.replace("{{BATCH_INDEX}}", str(batch_index))
        .replace("{{BATCH_SIZE}}", str(batch_size))
        .replace("{{TOTAL_COUNT}}", str(total_count))
    )


def build_system_prompt(skill_text: str) -> str:
    """把基础数据生成规则和一个或多个 Skill 合并为 system prompt。"""
    if not skill_text.strip():
        return BASE_SYSTEM_PROMPT
    return f"{BASE_SYSTEM_PROMPT}\n\n当前启用的可复用 Skills：\n{skill_text}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def call_api(
    api_url: str,
    api_key: str,
    model: str,
    prompt: str,
    system_prompt: str,
    temperature: float,
    max_tokens: int,
    timeout: int,
    json_mode: bool,
    extra_payload: dict,
    thinking: bool,
    reasoning_effort: str,
) -> tuple[str, dict]:
    """发送一次 OpenAI Chat Completions 兼容请求，只返回最终 content 和完整响应。"""
    # 先构造各家兼容接口都认识的标准请求：模型、两段消息和是否流式返回。
    # system 消息负责约束数据格式，user 消息负责说明本批要生成多少条数据。
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "stream": False,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    # 再把百炼等服务商的扩展字段合并进去，标准字段与厂商字段互不混写。
    payload.update(extra_payload)
    if thinking:
        # 思考模式下不发送 temperature，并显式传递推理强度。
        # 不同服务商的开关字段不同：百炼使用 enable_thinking，DeepSeek
        # 官方使用 thinking。具体开关由 COMMERCIAL_API_EXTRA_JSON 提供，
        # 避免生成器擅自发送不兼容的供应商专用字段。
        payload.pop("temperature", None)
        payload.setdefault("reasoning_effort", reasoning_effort)

    # timeout 只限制本次网络请求；若网络波动或返回内容不合格，外层批次循环负责重试。
    response = requests.post(
        api_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    if not response.ok:
        raise RuntimeError(f"API HTTP {response.status_code}: {response.text[:500]}")
    body = response.json()
    message = body["choices"][0]["message"]
    return (message.get("content") or "").strip(), body


def parse_json_array(text: str) -> list[dict]:
    """兼容顶层数组和 {\"items\": [...]} 两种响应，提取数据列表。"""
    # 有些模型会给 JSON 套上 Markdown 代码围栏，先去掉围栏再寻找真正的 JSON 起点。
    cleaned = text.replace("```json", "").replace("```", "").strip()
    if not cleaned:
        raise ValueError("API回答content为空")
    starts = [index for index in (cleaned.find("{"), cleaned.find("[")) if index >= 0]
    if not starts:
        raise ValueError("API回答中没有JSON对象或数组")
    value, _ = json.JSONDecoder().raw_decode(cleaned[min(starts):])
    if isinstance(value, dict):
        value = value.get("items")
    if not isinstance(value, list):
        raise ValueError("JSON顶层必须是数组，或包含items数组的对象")
    return value


def save_failed_response(
    batch_index: int,
    attempt: int,
    model: str,
    content: str,
    response_body: dict | None,
    error: Exception,
) -> Path:
    # 失败响应单独存档，便于课后检查；它不会混入通过校验的训练数据。
    path = OUTPUT_DIR / "failed_responses" / f"batch_{batch_index:03d}_attempt_{attempt}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "model": model,
                "batch": batch_index,
                "attempt": attempt,
                "error": str(error),
                "content": content,
                "response": response_body,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def normalize_record(record: dict) -> dict:
    """统一字段并拦截空记录、未知任务类别和未知难度。"""
    if not isinstance(record, dict):
        raise ValueError("记录不是JSON对象")
    normalized = {
        "instruction": str(record.get("instruction", "")).strip(),
        "input": str(record.get("input", "")).strip(),
        "output": str(record.get("output", "")).strip(),
        "task_type": str(record.get("task_type", "")).strip(),
        "difficulty": str(record.get("difficulty", "")).strip(),
    }
    if not normalized["instruction"] or not normalized["output"]:
        raise ValueError("instruction或output为空")
    if normalized["task_type"] not in ALLOWED_TYPES:
        raise ValueError(f"未知task_type：{normalized['task_type']}")
    if normalized["difficulty"] not in ALLOWED_DIFFICULTIES:
        raise ValueError(f"未知difficulty：{normalized['difficulty']}")
    return normalized


def record_key(record: dict) -> tuple[str, str]:
    return record["instruction"], record["input"]


def read_existing(path: Path) -> list[dict]:
    """逐行读取已有 JSONL；任何损坏行都会阻止错误续传。"""
    if not path.is_file():
        return []
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise RuntimeError(f"已有文件第{line_number}行不是合法JSON") from error
    return records


def append_records(path: Path, records: list[dict]) -> None:
    """将本批成功记录立即追加到 JSONL，支持中断后继续。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        stream.flush()


def save_manifest(path: Path, payload: dict) -> None:
    """保存模型、Skill、哈希、数量和耗时，便于复现比较。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_DIR))
    except ValueError:
        return str(path)


def pretty_json_path(jsonl_path: Path) -> Path:
    """为逐行存储的 JSONL 自动生成同名、缩进可读的 JSON 数组文件。"""
    return jsonl_path.with_suffix(".json") if jsonl_path.suffix == ".jsonl" else jsonl_path.with_name(jsonl_path.name + ".json")


def save_pretty_json(jsonl_path: Path, records: list[dict]) -> Path:
    """将当前全部记录保存为适合人工阅读的缩进 JSON。"""
    path = pretty_json_path(jsonl_path)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main() -> None:
    """按“参数→Skill→API→检查→分批保存”的顺序执行完整生成流程。"""
    args = parse_args()
    if args.count <= 0 or args.batch_size <= 0:
        raise ValueError("count和batch-size必须大于0")

    # 1. Skill 组合阶段：默认使用自建的课程学习伴侣 Skill（course_learning_companion）。
    # 多次传入 --skill 时，按命令顺序把多个 SKILL.md 合并到同一 system prompt。
    # 混合数据默认不注入外部 Skill；Prompt 已经定义五类任务和质量规则。
    # Skill 只在明确指定 --skill 时启用，避免网络Skill的工作区或Git审查规则污染所有样本。
    skill_names = args.skill or []
    if len(skill_names) != 1:
        raise ValueError("本课程每个数据集场景必须且只能启用一个Skill；学习伴侣使用 course_learning_companion")
    loaded_skills = [load_skill(name) for name in skill_names]
    skill_name = ",".join(name for name, _ in loaded_skills)
    skill_text = "\n\n".join(
        f"### Skill: {name}\n{text}" for name, text in loaded_skills
    )
    skill_versions = {
        name: next(
            (line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("version:")),
            "unknown",
        )
        for name, text in loaded_skills
    }
    system_prompt = build_system_prompt(skill_text)
    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
    if args.dry_run:
        # dry-run 只检查最终文本，不读取密钥、不发网络请求，也不创建数据文件。
        print(f"skill: {skill_name}")
        print(f"skill_sha256: {sha256_text(skill_text)}")
        print(f"prompt_sha256: {sha256_text(prompt_text)}")
        print("--- system prompt ---")
        print(system_prompt)
        print("--- user prompt ---")
        print(build_prompt(1, min(args.batch_size, args.count), args.count))
        print("checkpoint: PASS（dry-run未调用API）")
        return
    api_url, api_key, model, extra_payload = load_api_config()
    output_path = args.output or DATA_DIR / f"commercial_api_sft_{args.count}.jsonl"
    output_path = output_path if output_path.is_absolute() else PROJECT_DIR / output_path
    if output_path.exists() and not args.resume:
        raise FileExistsError(f"输出已存在：{output_path}。需要续传时增加 --resume。")

    # 2. 续传阶段：--count 是最终总数；--resume 从已有 JSONL 数量继续补足。
    records = read_existing(output_path) if args.resume else []
    if len(records) > args.count:
        raise RuntimeError("已有记录数超过目标count")
    seen = {record_key(normalize_record(record)) for record in records}
    if records:
        save_pretty_json(output_path, records)
    api_calls = 0
    started = time.perf_counter()
    batch_index = len(records) // args.batch_size + 1
    manifest_path = OUTPUT_DIR / f"{output_path.stem}_manifest.json"

    print("[Week 5] 商业API批量生成SFT数据")
    print(f"model: {model}")
    print(f"target: {args.count}")
    print(f"skill: {skill_name}")
    print(f"resume from: {len(records)}")
    print(f"output: {display_path(output_path)}")

    # 每个成功批次都会立即落盘；程序中途停止后，可用 --resume 从已有数量继续补足。
    while len(records) < args.count:
        # 3. 批次阶段：每次只请求 batch-size 条，失败时保存原始响应并有限重试。
        request_count = min(args.batch_size, args.count - len(records))
        accepted: list[dict] = []
        last_error: Exception | None = None
        for attempt in range(1, args.max_retries + 1):
            raw = ""
            response_body: dict | None = None
            try:
                prompt = build_prompt(batch_index, request_count, args.count)
                raw, response_body = call_api(
                    api_url,
                    api_key,
                    model,
                    prompt,
                    system_prompt,
                    args.temperature,
                    args.max_tokens,
                    args.timeout,
                    args.json_mode,
                    extra_payload,
                    args.thinking,
                    args.reasoning_effort,
                )
                api_calls += 1
                candidates = parse_json_array(raw)
                # 4. 结构检查与去重：无效类别、空字段和重复 instruction/input 不写入文件。
                for candidate in candidates:
                    try:
                        normalized = normalize_record(candidate)
                    except ValueError:
                        continue
                    key = record_key(normalized)
                    if key in seen or any(record_key(item) == key for item in accepted):
                        continue
                    accepted.append(normalized)
                    if len(accepted) == request_count:
                        break
                if len(accepted) == request_count:
                    break
                raise ValueError(f"有效且不重复的数据只有{len(accepted)}/{request_count}条")
            except (requests.RequestException, KeyError, ValueError, RuntimeError) as error:
                # 本次响应整体作废并保存诊断信息，避免把半批或格式错误的数据追加到 JSONL。
                last_error = error
                accepted = []
                failure_path = save_failed_response(
                    batch_index,
                    attempt,
                    model,
                    raw,
                    response_body,
                    error,
                )
                print(
                    f"batch {batch_index} attempt {attempt}: RETRY ({error}); "
                    f"saved {display_path(failure_path)}"
                )
                if attempt < args.max_retries:
                    time.sleep(2)
        if len(accepted) != request_count:
            raise RuntimeError(f"batch {batch_index}生成失败：{last_error}")

        timestamp = datetime.now(timezone.utc).isoformat()
        # 5. 溯源信息：每条数据附加模型、批次和生成时间，便于比较不同模型结果。
        enriched = []
        for item in accepted:
            seen.add(record_key(item))
            sequence = len(records) + len(enriched) + 1
            enriched.append(
                {
                    "id": f"llm_course_sft_{sequence:04d}",
                    **item,
                    "generation": {
                        "model": model,
                        "batch": batch_index,
                        "generated_at": timestamp,
                    },
                }
            )
        append_records(output_path, enriched)
        records.extend(enriched)
        # 6. 双格式保存：JSONL 适合追加和训练；缩进 JSON 数组适合人工阅读。
        pretty_path = save_pretty_json(output_path, records)
        elapsed = time.perf_counter() - started
        print(f"batch {batch_index}: saved {len(records)}/{args.count} ({elapsed:.1f}s)")
        print(f"readable JSON: {display_path(pretty_path)}")
        save_manifest(
            # 7. manifest 记录参数、Skill版本、哈希和调用次数，不记录 API Key。
            manifest_path,
            {
                "status": "RUNNING" if len(records) < args.count else "PASS",
                "target_count": args.count,
                "saved_count": len(records),
                "api_calls": api_calls,
                "model": model,
                "skill": skill_name,
                "thinking": args.thinking,
                "reasoning_effort": args.reasoning_effort if args.thinking else None,
                "skill_version": skill_versions,
                "skill_sha256": sha256_text(skill_text),
                "prompt_sha256": sha256_text(prompt_text),
                "output": display_path(output_path),
                "task_type_counts": Counter(item["task_type"] for item in records),
                "elapsed_seconds": round(elapsed, 2),
            },
        )
        batch_index += 1

    print("task types:", dict(Counter(item["task_type"] for item in records)))
    print(f"saved: {display_path(output_path)}")
    print("checkpoint: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
