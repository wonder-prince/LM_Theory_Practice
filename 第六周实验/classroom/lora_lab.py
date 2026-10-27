"""Load a Hugging Face PEFT LoRA adapter onto Qwen2.5-0.5B and verify the loading is correct.

本周只做"加载 LoRA 适配器 + 验证加载是否正确"，不做反向传播/参数更新
（完整微调训练与训练前后对比属于第七周）。验证点：
1. get_peft_model 注入 LoRA 后，只有 LoRA 参数可训练（占比很小）。
2. q_proj/v_proj 下出现 lora_A / lora_B 子模块。
3. 一次前向得到形状正确的 logits。
4. LoRA 初始权重 B=0，保存并重载后前向输出与基座一致（未训练不改变输出）。
5. 重载后的模型能使用标准聊天模板生成一条示例回答。
本实验的保存/重载验证只证明适配器可序列化和重新挂载；真正的输出变化要到第七周更新 LoRA 参数后观察。

进阶参数：
- --r 4|8|16 扫描不同秩对可训练参数与显存的影响。
- --method lora|dora 对照标准 LoRA 与 DoRA（权重分解为幅度×方向）。
- --targets qv|qkvo|all 扫描 LoRA 挂载范围：qv=q_proj/v_proj；qkvo=四个注意力投影；
  all=注意力+MLP（q/k/v/o/gate/up/down）。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import torch
from peft import LoraConfig, PeftModel, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer


# 根据脚本位置定位本周目录，统一读取本地基座模型、保存适配器。
PROJECT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT / "models" / "Qwen2.5-0.5B-Instruct"
ADAPTER_DIR = PROJECT / "adapters" / "qwen05b-learning-companion-lora-demo"

# 只用于检查一次前向计算。
# 使用当前模型的分词器后，该文本恰好包含 23 个 token，便于解释 logits 形状。
PROBE_TEXT = "LoRA适配器的模型执行一次前向计算，用于验证输出张量的形状是否正确。"
SAMPLE_QUESTION = "请只输出“LoRA适配器加载成功”，不要补充其他内容。"

# 投影层决定把 LoRA 加到模型的哪些位置：q/v 是注意力中的查询/值投影；
# qkvo 覆盖全部注意力投影，all 还包括前馈网络中的 gate/up/down 投影。
TARGET_SETS = {
    "qv": ["q_proj", "v_proj"],
    "qkvo": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "all": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
}


def parse_args() -> argparse.Namespace:
    # 从终端接收实验变量，学生可分别调整秩、适配方法和挂载范围进行对比。
    parser = argparse.ArgumentParser()
    parser.add_argument("--r", type=int, default=8, choices=[4, 8, 16], help="LoRA 低秩矩阵的秩")
    parser.add_argument("--method", type=str, default="lora", choices=["lora", "dora"],
                        help="lora=标准LoRA；dora=DoRA（use_dora=True）")
    parser.add_argument("--targets", type=str, default="qv", choices=["qv", "qkvo", "all"],
                        help="LoRA 挂载范围：qv / qkvo / all")
    return parser.parse_args()


def gpu() -> str:
    # 调用 NVIDIA 自带工具，获取显卡名称、当前已用/总显存和利用率。
    # 这里记录的是显卡整体状态，后面 PyTorch 的峰值统计只针对张量分配。
    result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu",
                             "--format=csv,noheader"], capture_output=True, text=True, check=False)
    return (result.stdout or result.stderr).strip()


def lora_summary(model) -> dict:
    modules: set[str] = set()
    # 同一个投影层会同时出现 A、B 两个低秩分支；用父层名称去重后，
    # 得到实际挂载了适配器的投影层数量，而不是把 A、B 各算一层。
    for name, _ in model.named_modules():
        lowered = name.lower()
        if ".lora_a" in lowered or ".lora_b" in lowered:
            parent = name.split(".lora_")[0]
            modules.add(parent)
    return {"lora_module_count": len(modules)}


def main() -> int:
    args = parse_args()
    # 固定随机种子，减少多次实验中初始化随机性带来的差异。
    torch.manual_seed(202606)

    # 只读取已经下载好的模型；半精度加载并放到 GPU，降低权重占用的显存。
    # 此处关闭生成缓存，本周的单次前向检查不需要保存历史 token 的缓存。
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    base = AutoModelForCausalLM.from_pretrained(MODEL_DIR, local_files_only=True, torch_dtype=torch.float16,
                                                low_cpu_mem_usage=True).to("cuda")
    base.config.use_cache = False
    full_params = sum(p.numel() for p in base.parameters())

    # r 控制 A、B 的中间维度；标准 LoRA 的增量为 (alpha/r)×B×A。
    # dropout 是 LoRA 分支的训练正则项；本周不训练，仅检查适配器是否正确挂载。
    config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=args.r, lora_alpha=16, lora_dropout=0.05,
                        target_modules=TARGET_SETS[args.targets], bias="none",
                        use_dora=(args.method == "dora"))
    # 注入后冻结基座权重，将 LoRA A/B 标为可训练；DoRA 还包含可训练的幅度参数。
    # requires_grad=True 只说明参数允许参与训练，本脚本没有反向传播或优化器更新。
    model = get_peft_model(base, config)
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    lora = lora_summary(model)

    # 一次前向：把示例提示编码后送入带 LoRA 的模型，只取 logits，不更新任何参数。
    encoded = tokenizer(PROBE_TEXT, return_tensors="pt", truncation=True, max_length=192).to("cuda")
    before_gpu = gpu()
    torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    with torch.inference_mode():
        # logits 为每个位置预测下一个 token 的原始分数，尚未转换为概率。
        # 形状依次为：[批次大小, 输入 token 数, 词表大小]。
        logits = model(**encoded).logits
    seconds = time.perf_counter() - start
    peak_mib = round(torch.cuda.max_memory_allocated() / 1024**2, 1)

    # 适配器只保存增量参数和配置；重新加载时需要再次提供同一个基座模型。
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(ADAPTER_DIR)
    tokenizer.save_pretrained(ADAPTER_DIR)

    # 先释放旧模型及空闲显存缓存，再重新加载基座和刚才保存的适配器，
    # 验证文件能否独立重载，避免只检查仍留在内存中的原模型。
    del model, base
    torch.cuda.empty_cache()
    reload_base = AutoModelForCausalLM.from_pretrained(MODEL_DIR, local_files_only=True, torch_dtype=torch.float16,
                                                       low_cpu_mem_usage=True).to("cuda")
    reloaded = PeftModel.from_pretrained(reload_base, ADAPTER_DIR, local_files_only=True)
    # 切换评估模式，关闭 dropout 等训练时的随机行为。
    reloaded.eval()

    with torch.inference_mode():
        # 使用相同输入再做一次前向，随后对比保存前后的 logits。
        reloaded_logits = reloaded(**encoded).logits

        # 聊天模板会补齐用户角色标记和助手回答起点，让输入符合模型训练时的格式。
        chat_input_ids = tokenizer.apply_chat_template(
            [{"role": "user", "content": SAMPLE_QUESTION}],
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to("cuda")
        # 采用确定性生成，最多新增 20 个 token；不做随机采样，便于课堂复现。
        generated = reloaded.generate(
            input_ids=chat_input_ids,
            attention_mask=torch.ones_like(chat_input_ids),
            max_new_tokens=20,
            do_sample=False,
            temperature=None,
            top_p=None,
            top_k=None,
            pad_token_id=tokenizer.eos_token_id,
        )
        # generate 的结果包含原始问题，切掉输入部分后只解码新生成的回答。
        generated_answer = tokenizer.decode(
            generated[0, chat_input_ids.shape[1]:], skip_special_tokens=True
        ).strip()
    # 逐元素相减并取最大绝对差，衡量适配器保存前后是否保持一致。
    max_diff = float((logits - reloaded_logits).abs().max().item())

    adapter_files = {p.name: p.stat().st_size for p in ADAPTER_DIR.iterdir() if p.is_file()}
    # 此处直接比较的是保存前与重载后的输出；未训练的标准 LoRA 初始 B=0，
    # 理论上增量也为零。DoRA 涉及幅度/方向分解，允许更大的数值漂移。
    diff_threshold = 1e-3 if args.method == "lora" else 1.0
    # 汇总可训练参数占比、投影层数量、输出形状、显存和示例回答。
    # passed 表示本次加载与重载检查通过，不表示模型已经完成微调。
    report = {
        "passed": (
            logits.shape[0] == 1
            and lora["lora_module_count"] >= 2
            and max_diff < diff_threshold
            and bool(generated_answer)
        ),
        "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
        "base_parameters": full_params,
        "lora": {"method": args.method, "r": args.r, "alpha": 16, "dropout": 0.05,
                 "target_modules": TARGET_SETS[args.targets], **lora},
        "trainable_parameters": trainable,
        "trainable_percent": round(100 * trainable / full_params, 4),
        "logits_shape": list(logits.shape),
        "reload_max_abs_diff": round(max_diff, 8),
        "forward_seconds": round(seconds, 2),
        "peak_cuda_memory_mib": peak_mib,
        "gpu_before": before_gpu,
        "gpu_after_reload": gpu(),
        "verified_example": {"question": SAMPLE_QUESTION, "answer": generated_answer},
        "adapter_directory": str(ADAPTER_DIR),
        "adapter_files": adapter_files,
        "boundary": "本周只加载并验证 LoRA 适配器；完整微调训练与训练前后对比属于第七周。",
    }
    # 将同一份结果同时保存到 JSON 并打印到终端，方便对照和保留实验记录。
    out = PROJECT / "outputs" / "lora_lab_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PASS PEFT LoRA load/verify" if report["passed"] else "FAIL LoRA lab")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
