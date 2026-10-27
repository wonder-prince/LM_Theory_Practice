"""Step 07：离线加载 GPT-2，查看架构、下一个 token 概率并续写完整句子。
"""

from __future__ import annotations

import gc

import torch
from transformers import (
    AutoConfig, AutoModelForCausalLM, AutoTokenizer, StoppingCriteria,
    StoppingCriteriaList,
)

from common import GPT2_LOCAL_DIR, OUTPUT_DIR, ensure_dirs, save_json, select_device


def parameter_count(model) -> int:
    """统计全部可训练与不可训练参数元素的数量。"""
    return sum(p.numel() for p in model.parameters())


def make_tokens_readable(tokens: list[str]) -> list[str]:
    """把 GPT-2 的特殊空白标记改成便于课堂阅读的 ASCII 文本。

    GPT-2 tokenizer 用 ``Ġ`` 表示“这个子词前面原本有一个空格”。部分旧版
    Windows/Conda 终端不能用 GBK 输出该字符，因此终端显示为 ``<space>``；
    模型内部的 token id 和计算过程完全没有改变。
    """
    return [token.replace("Ġ", "<space>").replace("Ċ", "<newline>") for token in tokens]


class StopAfterSentence(StoppingCriteria):
    """生成至少 min_new_tokens 后，一旦续写中出现英文句末标点就停止。"""

    def __init__(self, tokenizer, prompt_length: int, min_new_tokens: int = 12) -> None:
        self.tokenizer = tokenizer
        self.prompt_length = prompt_length
        self.min_new_tokens = min_new_tokens

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        # 太早遇到缩写句点时不停止，保证示例包含足够内容。
        if input_ids.shape[1] - self.prompt_length < self.min_new_tokens:
            return False
        continuation = self.tokenizer.decode(
            input_ids[0, self.prompt_length:], skip_special_tokens=True
        )
        return any(mark in continuation for mark in (".", "!", "?"))


def main() -> None:
    ensure_dirs()
    # config、tokenizer、权重全部从 models 读取；本步骤可完全离线运行。
    device = select_device()
    config = AutoConfig.from_pretrained(GPT2_LOCAL_DIR, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(GPT2_LOCAL_DIR, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        GPT2_LOCAL_DIR, local_files_only=True
    ).to(device).eval()

    prompt = "Artificial intelligence can help students"
    # 分词器输出 [B,L] 的整数 id；GPT-2 使用子词 token，不等于按空格切词。
    inputs = tokenizer(prompt, return_tensors="pt")
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    readable_tokens = make_tokens_readable(tokens)
    inputs = {name: tensor.to(device) for name, tensor in inputs.items()}
    with torch.inference_mode():
        outputs = model(**inputs, output_hidden_states=True)
        # logits=[B,L,V]；[-1] 只取最后位置对“下一个 token”的 V 个分数。
        next_probabilities = outputs.logits[0, -1].softmax(dim=-1)
        values, indices = next_probabilities.topk(5)
        # 旧版固定只生成 12 token，会在 "and it can help" 处硬截断。
        # 现在最多生成 60 token，并在形成完整英文句子后提前停止。
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            stopping_criteria=StoppingCriteriaList([
                StopAfterSentence(tokenizer, inputs["input_ids"].shape[1])
            ]),
        )

    predictions = [
        {"token": tokenizer.decode([int(index)]), "probability": float(value)}
        for value, index in zip(values.cpu(), indices.cpu())
    ]
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    architecture_text = """[GPT-2 模块树阅读说明]
GPT2LMHeadModel = GPT-2 Transformer 主体 transformer + 语言模型头 lm_head。
transformer.wte：token embedding；把 50,257 个 token id 映射为 768 维向量。
transformer.wpe：position embedding；表示 token 在序列中的位置。
transformer.h (0-11)：12 个顺序堆叠的 GPT2Block；每个 token 都依次通过全部 12 层。
每个 GPT2Block 包含：
  ln_1 + attn：归一化后执行带因果约束的多头自注意力，再做残差连接；
  attn.c_attn：一次线性投影同时生成 Q、K、V，768×3=2304；
  attn.c_proj：把多头注意力结果投影回 768 维；
  ln_2 + mlp：归一化后通过 768→3072→768 的前馈网络，再做残差连接。
transformer.ln_f：12 个 Block 之后的最终 LayerNorm。
lm_head：把每个位置的 768 维表示映射为 50,257 个下一个-token分数。
注意：token 是可变长度子词，不等于一个字节或一个完整单词；hidden_states 是
嵌入输出与每个 Block 输出的集合，也不是单独的网络层。

[Transformers 输出的完整模块树]
""" + str(model)
    (OUTPUT_DIR / "gpt2_architecture.txt").write_text(architecture_text, encoding="utf-8")
    peak_memory = (
        torch.cuda.max_memory_allocated() / (1024**2)
        if device.type == "cuda" else 0.0
    )
    result = {
        "status": "PASS",
        "local_model": str(GPT2_LOCAL_DIR),
        "model_class": model.__class__.__name__,
        "device": str(device),
        "parameter_count": parameter_count(model),
        "num_hidden_layers": config.n_layer,
        "hidden_size": config.n_embd,
        "num_attention_heads": config.n_head,
        "vocab_size": config.vocab_size,
        "max_position_embeddings": config.n_positions,
        "prompt": prompt,
        "tokens": tokens,
        "display_tokens": readable_tokens,
        "input_ids_shape": list(inputs["input_ids"].shape),
        "embedding_output_shape": list(outputs.hidden_states[0].shape),
        "logits_shape": list(outputs.logits.shape),
        "hidden_state_count": len(outputs.hidden_states),
        "last_hidden_state_shape": list(outputs.hidden_states[-1].shape),
        "top_5_next_token_predictions": predictions,
        "generated_text": generated_text,
        "cuda_peak_memory_mib": round(peak_memory, 2),
        "module_output_map": {
            "model.transformer.wte+wpe": list(outputs.hidden_states[0].shape),
            "model.transformer.h+ln_f": list(outputs.hidden_states[-1].shape),
            "model.lm_head": list(outputs.logits.shape),
        },
    }
    save_json("step07_gpt2.json", result)

    print("[Step 07] GPT-2 架构探索与前向运行")
    print(f"model class: {result['model_class']}")
    print(f"parameters: {result['parameter_count']:,}")
    print(f"layers={config.n_layer}, hidden={config.n_embd}, heads={config.n_head}")
    print(f"vocab={config.vocab_size}, max positions={config.n_positions}")
    print("\n[按架构图从左到右核对]")
    print(f"1 提示文本 -> tokenizer -> tokens: {readable_tokens}")
    print(f"  input_ids: {tuple(inputs['input_ids'].shape)}  # [B, L]")
    print("2 Token + Position Embeddings -> model.transformer.wte + wpe")
    print(f"  hidden_states[0]: {tuple(outputs.hidden_states[0].shape)}  # [B, L, H]")
    print(f"3 Transformer Block x{config.n_layer} + Final LayerNorm -> model.transformer.h + ln_f")
    print(f"  hidden_states[-1]: {tuple(outputs.hidden_states[-1].shape)}  # [B, L, H]")
    print(f"  hidden_states 共 {len(outputs.hidden_states)} 组 = 1 组嵌入 + {config.n_layer} 个 Block 后的状态")
    print("4 LM Head -> model.lm_head")
    print(f"  logits: {tuple(outputs.logits.shape)}  # [B, L, V]")
    print("\n[只读取最后位置 logits，经 softmax 得到下一个 token 的 top-5]")
    for item in predictions:
        print(f"  {item['token']!r}: {item['probability']:.4f}")
    print("\n[model.generate 重复执行“取最后位置 -> 选下一个 token -> 追加到输入”]")
    print(f"generated text (stopped at sentence end): {generated_text}")
    print(f"CUDA peak allocated: {peak_memory:.2f} MiB")
    print("module tree: outputs\\gpt2_architecture.txt（文件开头含阅读说明）")
    print("checkpoint: PASS")

    del model, outputs
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

