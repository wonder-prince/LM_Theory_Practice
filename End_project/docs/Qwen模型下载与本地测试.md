# Qwen3-4B 本地 GPU 测试

新电脑请先阅读 [Windows 从零复现指南](Windows从零复现指南.md)，其中提供固定版本权重下载、SHA256 校验和独立 GPU 环境安装命令。下文“已下载”及 Conda 路径描述的是作者本机，模型权重没有上传到 GitHub。

本地模型已经位于 `models/Qwen3-4B-Instruct-2507`，包含三片 safetensors、tokenizer 和下载校验清单 `download_manifest.json`。直接加载这些权重，不需要重新下载。模型为 Qwen3-4B-Instruct-2507，未做本项目微调。

最新完整评测见 [2026-11-27：1000秒预算独立重跑val50](../artifacts/qwen_gpu_val50_1000s_20261127_125739/README.md)：50/50题全部处理，正确19/50（38%）、字段匹配率50.09%、工具成功率66.16%。使用提交 `607fc14`，从第1题独立运行，模型已释放；与前次600秒预算的逐题对照及全部轨迹均已归档。

## 本机环境

2026-11-26 已检查并补齐 `.venv-gpu` 依赖：

| 项目 | 实际配置 |
| --- | --- |
| Python | 3.11.10 |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU，8188 MiB |
| PyTorch | 2.5.0+cu118，CUDA runtime 11.8 |
| Transformers / Accelerate | 4.55.4 / 1.10.1 |
| bitsandbytes | 0.47.0 |
| NumPy | 1.24.4 |
| 加载方式 | NF4 4bit、double quantization、BF16 计算、SDPA |

现有 `.venv-gpu` 继承 `D:\conda_data\envs\python311` 的系统包，复用其中的 CUDA PyTorch。将虚拟环境自己的 NumPy 调整为 1.24.4，以同时满足继承的 numba 和 torchtnt。`pip check` 已通过，CUDA 矩阵运算与 BF16 支持检查通过，89 项现有单元测试通过。

核验命令：

```powershell
Set-Location 'D:\All_ws\LM_Theory_Practice\End_project'
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip check
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

## 运行真实 Agent

```powershell
# 第一条训练任务：单订单
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py

# 三订单批量任务
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --task-id 004498f4b987f7c1cc9c26a813678d7a

# 小批量验证；一次加载模型，逐题保存
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 5

# 验证集全量50题；处理结束后自动释放模型并退出
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 50
```

默认上下文 16384、每轮输出上限 2048 tokens、单题超时 1000 秒、最多 12 轮决策。可用 `--max-context`、`--max-new-tokens`、`--timeout`、`--max-decisions` 调整。`--limit`支持1到50，和`--task-id`互斥，只开放train/val。`run_status.json`记录运行进度与结束后的模型清理状态。

模型使用官方 tokenizer 工具模板，自主决定工具与参数。运行不读取 `.env`，无需 API。每题结束即保存 UTF-8 的 `traces.json`、`summary.json`、可直接阅读的 `traces.md` 和 `evaluation.md`，默认输出到新的 `artifacts/local_qwen_时间戳/`。

摘要记录逐题停止原因、工具错误数、最后一次方案校验回执、token 用量、耗时及 PyTorch 峰值已分配显存。`completed` 只代表生成了最终文本；`tool_validated_tasks` 只统计最后一次工具校验通过的题数，不能视为独立评测正确率。实际结果见 [Windows运行说明](Windows运行说明.md)。

现已接入独立评分：每题 `accuracy` 比较模型显式提交的结构化方案与train/val隐藏参考答案，检查订单覆盖、7项金额、交易归属、复核标记及未分配交易；`evaluation`包含字段差异和工具成功率。提交方式为最后一次 `validate_reconciliation(plan)` 或最终文本中的 `<reconciliation_result>JSON方案</reconciliation_result>`，无法完成的题按失败记录。中文报告未做自动语义评分。评分发生在推理结束后，参考答案不会反馈给模型。

`cost`对象区分本地API费用（0）与算力估价，同时记录实际耗时、已报告token与输出速度。没有实测电费；只有显式提供 `--compute-price-per-hour` 后才计算算力估价，币种使用 `--cost-currency`。旧轨迹可通过 `agent_cli.py --evaluate-trace` 离线补评，无需重新加载GPU模型。

## 重建环境

保留当前环境即可运行。若在另一台 Windows 机器重建，可创建隔离的 Python 3.11 环境，再安装 CUDA wheel：

```powershell
python -m venv .venv-gpu
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cu118 --progress-bar off
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip install -r requirements-gpu.txt --progress-bar off
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip check
```

当前机器没有重新下载 PyTorch，也没有更改全局 Conda 环境。依赖兼容范围见 [bitsandbytes 0.47.0 官方安装说明](https://huggingface.co/docs/bitsandbytes/v0.47.0/installation)。

## 脚本清理

已删除完成下载后不再使用的 `download_qwen.py`、`download_ranges.py`，以及硬编码 macOS 字体路径的一次性 `export_pipeline.py`。现有模型、下载校验清单和流程图 PNG/SVG 保留。

保留数据准备/审计/校验、独立参考答案、规则演示、LangGraph 烟测和真实本地推理入口，供复现与排查使用。权重、虚拟环境和密钥不提交到仓库。模型许可见模型目录 `LICENSE`。
