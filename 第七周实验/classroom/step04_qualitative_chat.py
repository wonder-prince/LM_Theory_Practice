# 教学说明：本文件用于Step 04：交互式输入问题，实时比较基座模型与 LoRA 微调模型的回答。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 04：交互式输入问题，实时比较基座模型与 LoRA 微调模型的回答。

运行后逐次输入问题，每次输入都会看到两个模型各自的回答、生成 token 数和
停止原因，方便课堂逐段检查事实和教学风格。"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT = Path(__file__).resolve().parents[1]
# 交互实验复用第六周基座和第七周训练得到的适配器，输出另存为本周 JSON 记录。
MODEL_DIR = PROJECT.parent / "第六周实验" / "models" / "Qwen2.5-0.5B-Instruct"
ADAPTER_DIR = PROJECT / "adapters" / "qwen05b-learning-companion-lora-finetuned"
DEFAULT_OUTPUT = PROJECT / "outputs" / "step04_qualitative_chat.json"


def parse_args() -> argparse.Namespace:
    # max-new-tokens 是单次回答的长度上限，防止学生输入开放问题后生成过久。
    parser = argparse.ArgumentParser(description="交互式输入问题比较基座/微调模型")
    parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--adapter", type=Path, default=ADAPTER_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-new-tokens", type=int, default=256)
    return parser.parse_args()


def load_base(model_dir: Path, device: str):
    # 基座和“基座+适配器”各加载一份，才能让同一个问题同时得到两种回答。
    dtype = torch.float16 if device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, local_files_only=True, torch_dtype=dtype, low_cpu_mem_usage=True
    ).to(device)
    model.eval()
    return model


def format_prompt(question: str) -> str:
    # 使用训练阶段相同的指令/输入/回答模板，避免推理格式与训练格式不一致。
    return f"### 指令\n{question}\n### 输入\n\n### 回答\n"


def generate(tokenizer, model, question: str, max_new_tokens: int) -> tuple[str, int, str]:
    device = next(model.parameters()).device
    # 只编码当前问题；模型回答生成后，输入 token 会从结果中切除。
    encoded = tokenizer(format_prompt(question), return_tensors="pt").to(device)
    model.generation_config.do_sample = False
    model.generation_config.temperature = None
    model.generation_config.top_p = None
    model.generation_config.top_k = None
    output = model.generate(**encoded, max_new_tokens=max_new_tokens, do_sample=False,
                            pad_token_id=tokenizer.eos_token_id,
                            eos_token_id=tokenizer.eos_token_id)
    # output 同时包含输入和新生成部分，因此从输入长度处截取新 token。
    generated_ids = output[0, encoded.input_ids.shape[1]:]
    stop_reason = (
        "eos" if generated_ids.numel() and generated_ids[-1].item() == tokenizer.eos_token_id
        else "max_new_tokens"
    )
    # eos 表示模型主动结束，达到 max_new_tokens 表示被长度上限截断。
    answer = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    return answer, int(generated_ids.shape[0]), stop_reason


def main() -> int:
    args = parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 同时加载两个模型，每次输入问题后立即对比；两者共享 tokenizer 和生成上限。
    base = load_base(args.model_dir, device)
    tuned_base = load_base(args.model_dir, device)
    tuned = PeftModel.from_pretrained(tuned_base, args.adapter, local_files_only=True).to(device)
    tuned.eval()

    print("== 终端定性对比（交互模式）==")
    print(f"共同生成上限：max_new_tokens={args.max_new_tokens}（仅作安全限制）")
    print("逐次输入问题，每次会看到基座模型和微调模型各自的回答。")

    rows = []
    while True:
        question = input("\n请输入问题（直接回车退出）：").strip()
        if not question:
            break

        # 对同一个自然语言问题分别生成，学生可直接观察微调前后的风格和知识差异。
        base_answer, base_tokens, base_stop = generate(
            tokenizer, base, question, args.max_new_tokens)
        tuned_answer, tuned_tokens, tuned_stop = generate(
            tokenizer, tuned, question, args.max_new_tokens)

        print(f"\n[基座模型；{base_tokens} token；停止原因={base_stop}]\n{base_answer}")
        print(f"\n[微调模型；{tuned_tokens} token；停止原因={tuned_stop}]\n{tuned_answer}")

        # 每次交互立即保存在内存列表中，退出时统一写入 JSON，保留问题和停止原因。
        rows.append({
            "question": question,
            "base": base_answer, "base_tokens": base_tokens, "base_stop": base_stop,
            "tuned": tuned_answer, "tuned_tokens": tuned_tokens, "tuned_stop": tuned_stop,
        })

    if not rows:
        print("没有输入问题，实验结束。")
        return 0

    # 报告用于课后复盘；回答内容仍需人工检查，自动记录不等于事实核验。
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "device": device,
        "max_new_tokens": args.max_new_tokens,
        "questions": rows,
        "note": (
            "基座模型和微调模型使用相同的 max_new_tokens；该值只限制最长生成量，"
            "不是质量指标。课堂仍需人工核查事实正确性和回答完整性。"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n完整回答已保存：{args.output}")
    print("PASS step04 qualitative chat")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
