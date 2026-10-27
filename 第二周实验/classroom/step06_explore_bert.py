"""Step 06：离线加载 BERT，查看架构并完成一次 [MASK] 填词前向运行。
"""

from __future__ import annotations

import gc

import torch
from transformers import AutoConfig, AutoModelForPreTraining, AutoTokenizer

from common import BERT_LOCAL_DIR, OUTPUT_DIR, ensure_dirs, save_json, select_device


def parameter_count(model) -> int:
    """统计模型中全部参数元素的数量，而不是 Python 层的数量。"""
    return sum(p.numel() for p in model.parameters())


def main() -> None:
    ensure_dirs()
    # 只从项目 models 目录读取；没有本地文件就明确报错，不在本步骤下载。
    device = select_device()
    config = AutoConfig.from_pretrained(BERT_LOCAL_DIR, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(BERT_LOCAL_DIR, local_files_only=True)
    model = AutoModelForPreTraining.from_pretrained(
        BERT_LOCAL_DIR, local_files_only=True
    ).to(device).eval()

    # bert-base-uncased 主要使用英文语料；[MASK] 必须恰好出现一次。
    prompt = "The capital of France is [MASK]."
    # 分词器把文本转成 input_ids 和 attention_mask，形状都是 [B,L]。
    inputs = tokenizer(prompt, return_tensors="pt")
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    inputs = {name: tensor.to(device) for name, tensor in inputs.items()}
    # output_hidden_states=True 让课堂能观察 12 层之外还包含嵌入层输出，共 13 组。
    with torch.inference_mode():
        outputs = model(**inputs, output_hidden_states=True)

    mask_positions = (inputs["input_ids"] == tokenizer.mask_token_id).nonzero(as_tuple=False)
    assert mask_positions.shape[0] == 1
    mask_index = int(mask_positions[0, 1])
    # prediction_logits=[B,L,V]；只取 [MASK] 所在位置的 V 维分数。
    probabilities = outputs.prediction_logits[0, mask_index].softmax(dim=-1)
    values, indices = probabilities.topk(5)
    predictions = [
        {"token": tokenizer.decode([int(index)]).strip(), "probability": float(value)}
        for value, index in zip(values.cpu(), indices.cpu())
    ]

    # str(model) 是 Transformers 根据 config 创建的 Python 模块树。前面增加
    # 阅读说明，使模块树不只是类名清单，而能直接与架构图和终端形状对应。
    architecture_text = """[BERT 模块树阅读说明]
BertForPreTraining = BERT 主体 bert + 两个预训练任务头 cls。
bert.embeddings：把 token、位置和句段三种 embedding 相加并归一化。
bert.encoder.layer (0-11)：12 个顺序堆叠的 BertLayer；每层都包含：
  attention.self：多头双向自注意力，query/key/value 为三组线性投影；
  attention.output：注意力输出投影，并在 forward 中完成残差连接和 LayerNorm；
  intermediate：前馈网络第一层，把 768 维扩展到 3072 维并使用 GELU；
  output：前馈网络第二层，把 3072 维压回 768 维，再做残差连接和 LayerNorm。
bert.pooler：读取 [CLS] 位置形成句级表示，供 NSP 等句级任务使用。
cls.predictions：MLM 头，把每个位置的 768 维表示映射为 30,522 个词表分数。
cls.seq_relationship：NSP 头，把句级表示映射为“下一句/非下一句”两个分数。
注意：hidden_states 是各层输出张量的集合，不是模块树中的一个网络层。

[Transformers 输出的完整模块树]
""" + str(model)
    (OUTPUT_DIR / "bert_architecture.txt").write_text(architecture_text, encoding="utf-8")
    peak_memory = (
        torch.cuda.max_memory_allocated() / (1024**2)
        if device.type == "cuda" else 0.0
    )
    result = {
        "status": "PASS",
        "local_model": str(BERT_LOCAL_DIR),
        "model_class": model.__class__.__name__,
        "device": str(device),
        "parameter_count": parameter_count(model),
        "num_hidden_layers": config.num_hidden_layers,
        "hidden_size": config.hidden_size,
        "num_attention_heads": config.num_attention_heads,
        "intermediate_size": config.intermediate_size,
        "vocab_size": config.vocab_size,
        "max_position_embeddings": config.max_position_embeddings,
        "prompt": prompt,
        "tokens": tokens,
        "input_ids_shape": list(inputs["input_ids"].shape),
        "embedding_output_shape": list(outputs.hidden_states[0].shape),
        "mlm_logits_shape": list(outputs.prediction_logits.shape),
        "nsp_logits_shape": list(outputs.seq_relationship_logits.shape),
        "hidden_state_count": len(outputs.hidden_states),
        "last_hidden_state_shape": list(outputs.hidden_states[-1].shape),
        "mask_index": mask_index,
        "top_5_mask_predictions": predictions,
        "cuda_peak_memory_mib": round(peak_memory, 2),
        "module_output_map": {
            "model.bert.embeddings": list(outputs.hidden_states[0].shape),
            "model.bert.encoder.layer": list(outputs.hidden_states[-1].shape),
            "model.cls.predictions": list(outputs.prediction_logits.shape),
            "model.cls.seq_relationship": list(outputs.seq_relationship_logits.shape),
        },
    }
    save_json("step06_bert.json", result)

    print("[Step 06] BERT 架构探索与前向运行")
    print(f"model class: {result['model_class']}")
    print(f"parameters: {result['parameter_count']:,}")
    print(f"layers={config.num_hidden_layers}, hidden={config.hidden_size}, heads={config.num_attention_heads}")
    print(f"intermediate size={config.intermediate_size}, vocab={config.vocab_size}")
    print("\n[按架构图从左到右核对]")
    print(f"1 输入框 -> tokenizer -> tokens: {tokens}")
    print(f"  input_ids: {tuple(inputs['input_ids'].shape)}  # [B, L]")
    print("2 Embeddings 框 -> model.bert.embeddings")
    print(f"  hidden_states[0]: {tuple(outputs.hidden_states[0].shape)}  # [B, L, H]")
    print(f"3 Encoder Layer x{config.num_hidden_layers} -> model.bert.encoder.layer")
    print(f"  hidden_states[-1]: {tuple(outputs.hidden_states[-1].shape)}  # [B, L, H]")
    print(f"  hidden_states 共 {len(outputs.hidden_states)} 组 = 1 组嵌入 + {config.num_hidden_layers} 层 Encoder")
    print("4 MLM 头 -> model.cls.predictions")
    print(f"  prediction_logits: {tuple(outputs.prediction_logits.shape)}  # [B, L, V]")
    print("5 NSP 头 -> model.cls.seq_relationship")
    print(f"  seq_relationship_logits: {tuple(outputs.seq_relationship_logits.shape)}  # [B, 2]")
    print("\n[只读取 [MASK] 位置的 MLM logits，再经 softmax 得到 top-5]")
    for item in predictions:
        print(f"  {item['token']!r}: {item['probability']:.4f}")
    print(f"CUDA peak allocated: {peak_memory:.2f} MiB")
    print("module tree: outputs\\bert_architecture.txt（文件开头含阅读说明）")
    print("checkpoint: PASS")

    del model, outputs
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

