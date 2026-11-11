# 教学说明：本文件用于Step 05：根据真实模型配置比较三种 KV cache 分配方式。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

"""Step 05：根据真实模型配置比较三种 KV cache 分配方式。"""

from __future__ import annotations

import math

from transformers import AutoConfig

from course_paths import MODEL_DIR, OUTPUT_DIR, write_json

# 用一组长短不同的请求模拟真实服务中的变长序列。
SEQUENCE_LENGTHS = [72, 95, 113, 148, 191, 207, 266, 319, 401, 447, 503, 611]
BLOCK_SIZE = 16  # PagedAttention 每个逻辑块容纳 16 个 token。
STATIC_MAX_LENGTH = 640  # 静态方案为每个请求统一预留 640 个 token。
KV_DTYPE_BYTES = 2  # 本实验 KV Cache 使用 FP16，每个元素占 2 byte。


def main() -> int:
    config = AutoConfig.from_pretrained(MODEL_DIR, local_files_only=True)
    layers = config.num_hidden_layers
    kv_heads = getattr(config, "num_key_value_heads", config.num_attention_heads)
    head_dim = getattr(config, "head_dim", config.hidden_size // config.num_attention_heads)

    # 每层同时保存 K 和 V；每项还包含 KV head、head_dim 和数据类型字节数。
    bytes_per_token = 2 * layers * kv_heads * head_dim * KV_DTYPE_BYTES
    # exact_tokens 是没有任何预留浪费时需要保存的有效 token 总数。
    exact_tokens = sum(SEQUENCE_LENGTHS)
    static_tokens = len(SEQUENCE_LENGTHS) * STATIC_MAX_LENGTH
    # 分页方案必须按整块分配，因此每条序列向上取整到 16 的倍数。
    paged_tokens = sum(math.ceil(length / BLOCK_SIZE) * BLOCK_SIZE for length in SEQUENCE_LENGTHS)

    allocation = {
        "static_mib": static_tokens * bytes_per_token / 1024**2,
        "exact_mib": exact_tokens * bytes_per_token / 1024**2,
        "paged_mib": paged_tokens * bytes_per_token / 1024**2,
        "static_waste_percent": (static_tokens - exact_tokens) / static_tokens * 100,
        "paged_internal_waste_percent": (paged_tokens - exact_tokens) / paged_tokens * 100,
    }
    report = {
        "checkpoint": "PASS",
        "model": MODEL_DIR.name,
        "kv_kib_per_token": bytes_per_token / 1024,
        "sequence_lengths": SEQUENCE_LENGTHS,
        "block_size": BLOCK_SIZE,
        "allocation": allocation,
        "scope_note": "只比较 KV cache，不包含权重、激活、页表和框架工作区。",
    }
    out = OUTPUT_DIR / "step05_paged_kv_math.json"
    write_json(out, report)

    print(f"KV cache: {report['kv_kib_per_token']:.2f} KiB/token")
    print(
        f"static: {allocation['static_mib']:.2f} MiB, "
        f"waste={allocation['static_waste_percent']:.2f}%"
    )
    print(f"exact contiguous: {allocation['exact_mib']:.2f} MiB")
    print(
        f"paged({BLOCK_SIZE}): {allocation['paged_mib']:.2f} MiB, "
        f"internal waste={allocation['paged_internal_waste_percent']:.2f}%"
    )
    print("PASS step05 paged KV math")
    print(f"完整报告已写入：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
