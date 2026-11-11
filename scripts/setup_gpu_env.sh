#!/usr/bin/env bash
# 只安装依赖并核验 CUDA，不下载模型、不训练、不启动推理服务。
set -euo pipefail

usage() {
  cat <<'EOF'
用法：bash scripts/setup_gpu_env.sh {9|10}
要求：Linux x86_64（含 WSL2）、NVIDIA GPU、Python 3.10–3.12。
可选环境变量：
  PYTHON_BIN        Python 命令或绝对路径，默认 python3
  COURSE_VENV_ROOT  环境保存目录，默认 ~/.venvs/lm-theory-practice
EOF
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
  9) week_name="第九周实验"; env_name="week09" ;;
  10) week_name="第十周实验"; env_name="week10" ;;
  *) usage >&2; exit 2 ;;
esac
if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "请在 Linux x86_64 GPU 电脑或 WSL2 中执行此安装脚本。" >&2
  exit 1
fi
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "未找到 nvidia-smi，请先让管理员配置 NVIDIA 驱动与 GPU 访问。" >&2
  exit 1
fi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python3}"
venv_root="${COURSE_VENV_ROOT:-$HOME/.venvs/lm-theory-practice}"
venv_dir="$venv_root/$env_name"

"$python_bin" -s - <<'PY'
import sys
if not (3, 10) <= sys.version_info[:2] <= (3, 12):
    raise SystemExit("请用 PYTHON_BIN 指定 Python 3.10、3.11 或 3.12；推荐 3.11。")
PY

if [[ -e "$venv_dir" ]]; then
  if [[ ! -f "$venv_dir/pyvenv.cfg" || ! -x "$venv_dir/bin/python" ]]; then
    echo "目标目录不是有效虚拟环境，请通过 COURSE_VENV_ROOT 指定其他目录：$venv_dir" >&2
    exit 1
  fi
else
  "$python_bin" -m venv "$venv_dir"
fi
env_python="$venv_dir/bin/python"
"$env_python" -s - <<'PY'
import sys
if sys.prefix == sys.base_prefix or not (3, 10) <= sys.version_info[:2] <= (3, 12):
    raise SystemExit("现有环境需要 Python 3.10–3.12，请换一个 COURSE_VENV_ROOT 后重试。")
PY

"$env_python" -s -m pip install --upgrade pip
# 先从 PyTorch 官方索引安装 CUDA 12.4 wheel，避免误装 CPU 版。
torch_packages=("torch==2.6.0")
if [[ "$env_name" == "week10" ]]; then
  torch_packages+=("torchvision==0.21.0" "torchaudio==2.6.0")
fi
"$env_python" -s -m pip install "${torch_packages[@]}" \
  --index-url https://download.pytorch.org/whl/cu124
"$env_python" -s -m pip install -r "$repo_dir/$week_name/requirements.txt"
"$env_python" -s -m pip check

# 不加载课程模型，只检查依赖能否导入、GPU 是否对当前环境可见。
"$env_python" -s - "$env_name" <<'PY'
import importlib
import sys
import torch

packages = ["transformers", "bitsandbytes"]
packages += ["peft", "accelerate", "numpy", "safetensors", "psutil"] if sys.argv[1] == "week09" else ["vllm", "requests"]
for name in packages:
    module = importlib.import_module(name)
    print(f"{name}: {getattr(module, '__version__', 'installed')}")
print(f"Python: {sys.version.split()[0]}")
print(f"PyTorch: {torch.__version__}; CUDA runtime: {torch.version.cuda}")
if not torch.cuda.is_available():
    raise SystemExit("依赖已安装，但 CUDA 不可用。请检查驱动、GPU 分配和 CUDA_VISIBLE_DEVICES。")
print(f"GPU: {torch.cuda.get_device_name(0)}")
print("PASS 依赖导入与 CUDA 可见性检查（尚未验证模型推理）")
PY

"$env_python" -s -m pip freeze > "$venv_dir/requirements.installed.txt"
printf '\n环境已准备：%s\n' "$venv_dir"
printf '激活命令：source %q/bin/activate\n' "$venv_dir"
printf '实际依赖版本：%s/requirements.installed.txt\n' "$venv_dir"