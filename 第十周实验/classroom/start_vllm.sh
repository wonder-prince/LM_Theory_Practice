#!/usr/bin/env bash
# 在 GPU 电脑上手动执行；配置环境时不会自动启动服务。
set -euo pipefail

usage() {
  cat <<'EOF'
用法：bash 第十周实验/classroom/start_vllm.sh [baseline|tuned|apc]
  baseline  max-num-seqs=4，关闭 APC（默认；也用于 apc_off 测量）
  tuned     max-num-seqs=8，关闭 APC
  apc       max-num-seqs=4，开启 APC（用于 apc_on 测量）
先激活 week10 环境。路径沿用 course_paths.py，可用 COURSE_* 环境变量覆盖。
COURSE_API_HOST 默认 127.0.0.1，COURSE_API_PORT 默认 8000。
EOF
}

profile="${1:-baseline}"
case "$profile" in
  -h|--help) usage; exit 0 ;;
  baseline|tuned|apc) ;;
  *) usage >&2; exit 2 ;;
esac
if [[ $# -gt 1 ]]; then
  usage >&2
  exit 2
fi
if [[ "$(uname -s)" != "Linux" ]]; then
  echo "vLLM CUDA 服务需要 Linux 或 WSL2。" >&2
  exit 1
fi

# 无论从哪个目录调用，都能正确导入 classroom.course_paths。
week_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$week_dir"
model_dir="$(python -s -c 'from classroom.course_paths import MODEL_DIR; print(MODEL_DIR)')"
adapter_dir="$(python -s -c 'from classroom.course_paths import ADAPTER_DIR; print(ADAPTER_DIR)')"
for required_file in \
  "$model_dir/config.json" "$model_dir/model.safetensors" \
  "$model_dir/tokenizer_config.json" "$model_dir/tokenizer.json" \
  "$adapter_dir/adapter_config.json" "$adapter_dir/adapter_model.safetensors"; do
  if [[ ! -s "$required_file" ]]; then
    echo "缺少模型或 LoRA 文件：$required_file" >&2
    exit 1
  fi
done

max_num_seqs=4
extra_args=()
if [[ "$profile" == "tuned" ]]; then
  max_num_seqs=8
elif [[ "$profile" == "apc" ]]; then
  extra_args+=(--enable-prefix-caching)
fi
export VLLM_USE_V1=0
printf '启动配置：%s；max-num-seqs=%s；APC=%s\n' "$profile" "$max_num_seqs" "$([[ "$profile" == "apc" ]] && echo on || echo off)"
exec python -s -m vllm.entrypoints.openai.api_server \
  --model "$model_dir" \
  --served-model-name qwen05b-base \
  --quantization bitsandbytes \
  --load-format bitsandbytes \
  --dtype half \
  --enable-lora \
  --max-lora-rank 16 \
  --lora-modules "learning-companion=$adapter_dir" \
  --max-model-len 1024 \
  --gpu-memory-utilization 0.75 \
  --max-num-seqs "$max_num_seqs" \
  --max-num-batched-tokens 1024 \
  --swap-space 0 \
  --enforce-eager \
  --disable-custom-all-reduce \
  --host "${COURSE_API_HOST:-127.0.0.1}" \
  --port "${COURSE_API_PORT:-8000}" \
  "${extra_args[@]}"