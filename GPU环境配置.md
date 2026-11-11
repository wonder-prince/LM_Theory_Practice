# 第九、十周 GPU 环境配置

本说明用于把整个项目迁移到 GPU 电脑后安装环境。安装脚本只安装依赖并检查 CUDA，不下载模型、不训练、不执行实验、不启动服务。

## 1. 选择电脑

- 推荐 Ubuntu 22.04/24.04 x86_64，或 Windows + WSL2 Ubuntu，使用 NVIDIA GPU。
- 推荐 Python 3.11；安装脚本支持 3.10–3.12。vLLM 0.8.5.post1 不支持 Python 3.13。
- 推荐 RTX 30/40 系列、A10、A100 等显卡，显存 8 GB 或以上更方便；指导书提供了 4 GB 的服务参数，但实际余量需到目标机器验证。
- 本配置沿用 PyTorch 2.6.0 + CUDA 12.4。RTX 50 系列等更新架构需要重新核对 PyTorch/vLLM 支持，不能直接假定这套旧版本可用。
- GPU 电脑应已安装支持 CUDA 12.4 的 NVIDIA 驱动，建议驱动 550.54.14 或更新；在 Linux/WSL2 中确认 `nvidia-smi` 能正常显示显卡。WSL2 使用 Windows 主机驱动。
- 预留约 20 GB 以上磁盘空间供两个环境、下载缓存和课程模型使用；实际占用因依赖版本而异。

PyTorch wheel 自带所需 CUDA 运行库，通常不必另装完整 CUDA Toolkit。若 Ubuntu 缺少 venv 或编译工具，由管理员安装 `python3-venv`、`python3-dev`、`build-essential`；指定 Python 3.11 时，还需与它匹配的 venv 模块。安装脚本不更改系统驱动或系统包。

## 2. 复制整个项目

保留中文目录及相对层级。不要把 Mac 上的 `.venv` 复制到 Linux；虚拟环境必须在 GPU 电脑重新创建。用 Git 迁移时，未提交或被忽略的资产不会自动传过去，需要单独复制。

两周完整实验需要以下输入：

| 输入 | 项目内默认路径 | 说明 |
| --- | --- | --- |
| 官方基座模型 | `第六周实验/models/Qwen2.5-0.5B-Instruct/` | 包含 `model.safetensors`、配置和完整分词器文件 |
| 验证集 | `第六周实验/data/validation.jsonl` | 第九周定量评估需要 |
| 第七周训练后的 LoRA | `第七周实验/adapters/qwen05b-learning-companion-lora-finetuned/` | 包含 `adapter_config.json` 和 `adapter_model.safetensors` |
| 第六周演示 LoRA | `第六周实验/adapters/qwen05b-learning-companion-lora-demo/` | 仅第十周 Multi-LoRA 扩展需要，不能替代训练后的适配器 |

本次检查时，上述模型、数据和适配器尚未放入仓库目录；环境安装成功不代表这些输入已准备。基座的固定版本、文件列表及哈希见 `第六周实验/classroom/download_official_model.py`，需要下载时再使用该脚本。数据与适配器按第六、七周说明准备或从原实验电脑复制。

第九周脚本目前使用固定相对路径，应按表中位置放置资产。第十周支持 `COURSE_MODEL_DIR`、`COURSE_ADAPTER_DIR`、`COURSE_DEMO_ADAPTER_DIR`、`COURSE_FINETUNED_ADAPTER_DIR` 覆盖路径；设置为 GPU 电脑上的绝对路径，并在启动服务的同一个终端导出。默认路径正确时无需设置。

## 3. 安装两个独立环境

在 GPU 电脑的项目根目录，用 Bash 执行 `bash scripts/setup_gpu_env.sh 9` 安装第九周环境，再执行 `bash scripts/setup_gpu_env.sh 10` 安装第十周环境。

脚本默认用 `python3`。如需指定解释器，可用 `PYTHON_BIN=python3.11 bash scripts/setup_gpu_env.sh 9`，第十周同理。脚本通过自身位置定位项目，可从其他目录以完整路径调用。

| 环境 | 默认目录 | 关键版本 |
| --- | --- | --- |
| 第九周 | `~/.venvs/lm-theory-practice/week09` | torch 2.6.0、transformers 4.55.4、peft 0.17.1、bitsandbytes 0.47.0 |
| 第十周 | `~/.venvs/lm-theory-practice/week10` | torch 2.6.0、vLLM 0.8.5.post1、transformers 4.51.3、bitsandbytes 0.45.5 |

两周的 transformers 与 bitsandbytes 版本不同，必须分开安装。脚本先从 PyTorch 官方 cu124 索引安装 CUDA wheel，再安装对应周的 requirements，最后执行 `pip check` 和依赖导入、CUDA 可见性检查。它不会加载模型或生成实验结果。成功后将实际依赖版本保存到各环境的 `requirements.installed.txt`。

重复执行会复用同名环境并按清单安装依赖，不删除环境。可用 `COURSE_VENV_ROOT` 指定其他环境根目录。安装会下载较大的 GPU 依赖，需要联网。

使用第九周时激活 `source ~/.venvs/lm-theory-practice/week09/bin/activate`，使用第十周时激活 `source ~/.venvs/lm-theory-practice/week10/bin/activate`。VS Code 中使用“Python: Select Interpreter”选择相应目录的 `bin/python`。Windows 用户须先在 WSL 中打开项目。

## 4. 第十周服务配置

以下启动入口供后续实际实验时使用，本次配置阶段不执行。先激活 week10 环境并准备好基座和训练后的 LoRA，然后从项目根目录调用：

| 服务配置 | 启动入口 | 用途 |
| --- | --- | --- |
| 基线 | `bash 第十周实验/classroom/start_vllm.sh baseline` | max-num-seqs=4，APC 关闭；单请求、并发基线、APC 关闭组 |
| 调度优化 | `bash 第十周实验/classroom/start_vllm.sh tuned` | 只将 max-num-seqs 改为 8 |
| 前缀缓存 | `bash 第十周实验/classroom/start_vllm.sh apc` | 基线配置加 `--enable-prefix-caching` |
| Multi-LoRA | 进入 `第十周实验` 后执行 `bash classroom/step07_start_multi_lora.sh` | 原有脚本，加载两个分组适配器 |

前三种配置注册的 LoRA 名称均为 `learning-companion`，与 Step 02/03/06 客户端一致。Multi-LoRA 注册 `group-a-demo`、`group-b-finetuned`，用于 Step 07，切换前须停止旧服务以释放 GPU 和 8000 端口。每个服务都在前台持续运行，按 Ctrl+C 停止。

新入口默认监听 `127.0.0.1:8000`，可以通过 `COURSE_API_HOST` 和 `COURSE_API_PORT` 修改。客户端使用 `COURSE_API_BASE`，默认 `http://127.0.0.1:8000`，不要附加 `/v1`。修改端口时必须同时更新客户端地址。需要从 Mac 连接远端时，可通过 SSH 端口转发访问远端回环地址。

APC 开关必须通过服务重启切换。客户端的 `--label apc_off` / `--label apc_on` 只标记报告，不会切换服务状态。

## 5. 当前准备状态

- 已准备可迁移的依赖配置、分周安装脚本及服务启动入口；尚未在 Linux GPU 机器安装或验证。
- 2026-11-11 已通过两个新 Shell 脚本的语法及帮助入口检查，并按 Linux x86_64、Python 3.11、CUDA 12.4 完成依赖元数据解析：第九周 42 个包、第十周 155 个包，均未发现版本约束冲突。该检查未安装 GPU 依赖，不能代替目标机器上的导入、驱动和模型加载验证。
- Mac 上此前创建的 `.venv/week09-10` 只完成了 Python 3.11 虚拟环境创建；依赖安装已取消，不应作为可用实验环境。
- 第九周 `classroom/step01_quantization_math.py` 的两个量化函数仍是教学 TODO，后续执行该步骤前需要按指导书完成；本次仅配置环境，保留练习代码。
- 尚未下载模型、准备验证集或训练 LoRA，也未运行实验或生成实验报告。