#!/usr/bin/env bash
# 教学说明：本文件用于完成指导书中与本步骤对应的输入、处理和结果保存。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

set -euo pipefail

# 路径由 course_paths.py 按课程目录结构计算；交换适配器时也可用环境变量覆盖。
MODEL_DIR=$(python -s -c "from classroom.course_paths import MODEL_DIR as p; print(p)")
A_DIR=$(python -s -c "from classroom.course_paths import DEMO_ADAPTER_DIR as p; print(p)")
B_DIR=$(python -s -c "from classroom.course_paths import FINETUNED_ADAPTER_DIR as p; print(p)")

# V0 引擎在本课程使用的 vLLM 0.8.5.post1 与 4 GB 配置上已经完成实测。
export VLLM_USE_V1=0
# 下面只加载一份4-bit NF4基座权重，再同时挂载两个LoRA适配器。
vllm serve "$MODEL_DIR" \
  --served-model-name qwen05b-base \
  --quantization bitsandbytes \
  --load-format bitsandbytes \
  --dtype half \
  --enable-lora \
  --max-loras 2 \
  --max-cpu-loras 2 \
  --max-lora-rank 16 \
  --lora-modules "group-a-demo=$A_DIR" "group-b-finetuned=$B_DIR" \
  --max-model-len 1024 \
  --gpu-memory-utilization 0.75 \
  --max-num-seqs 4 \
  --max-num-batched-tokens 1024 \
  --swap-space 0 \
  --enforce-eager \
  --disable-custom-all-reduce \
  --host 0.0.0.0 \
  --port 8000
