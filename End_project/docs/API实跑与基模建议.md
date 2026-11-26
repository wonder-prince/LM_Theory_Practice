# API 实跑与基模建议（2026-11-25）

## 本次真实模型运行

使用用户补充的 API 配置调用 `deepseek-flash`，通过项目原有 LangGraph 编排和八工具接口运行训练集任务。未修改提示、工具或业务判定。两题所有工具调用均成功，最终 `validate_reconciliation` 均返回 `valid=true, errors=[]`。

| 任务 | 决策数 | 工具调用数 | 耗时 | 累计 API tokens | 结果目录 |
| --- | ---: | ---: | ---: | ---: | --- |
| 单订单 `f3c95789ace1a9542c5d6baed2eac902` | 5 | 8 | 19.344 秒 | 18,767 | `artifacts/api_windows_20261125_232751/` |
| 三订单 `004498f4b987f7c1cc9c26a813678d7a` | 6 | 14 | 24.875 秒 | 29,310 | `artifacts/api_windows_batch_20261125_232842/` |

单订单应收与实收均 BRL 106.97，无退款、差额 0。三订单应收及实收合计 BRL 419.40，成功退款 BRL 32.14，净收 BRL 387.26；收款差额 0，正常退款没有误报为少收。模型输出了对应交易与事件证据，完整请求、工具回执及最终回答保存在各目录的 `traces.json`，汇总为 `summary.json`。

累计 tokens 为多轮请求之和，含重复发送的上下文。费用未计算。这是两道开发任务的工具核验结果，未进行独立评分，不能报告总体正确率。

配置原先填在 Git 跟踪的 `.env.example`，已迁移到被 Git 忽略的 `.env`，示例文件中的密钥字段已清空。此次由启动进程读取 `.env` 并注入环境变量；`agent_cli.py` 本身仍不自动加载 `.env`。

## 本机资源与首选

RTX 4060 Laptop GPU，8188 MiB 显存；检查时空闲仅 820 MiB。训练前需要释放其他 GPU 占用，不能根据总显存推断当前有足够空间。本次 API 调用不使用本机 GPU。项目 `.venv` 当前未安装 torch、transformers、peft、bitsandbytes、trl，尚未执行本地模型显存测试。

首选 **`Qwen/Qwen3-4B-Instruct-2507` + 4bit QLoRA**。这是约 4.0B 参数的开放权重指令模型，Apache-2.0 许可，原生工具调用模板，支持中文，且只使用非思考模式，便于为工具调用和最终答案构造助手监督样本。官方报告了工具使用与 Agent 能力，但这些公开成绩不等于本项目准确率。

本项目把金额计算与证据核验放在程序中，模型主要学习选择工具、正确填写交易 ID、理解工具回执和识别待复核场景。因此优先选择具备指令跟随及工具调用能力的 4B 模型；本项目中的“基模”可采用微调前的 Instruct 权重，无需从纯预训练 Base 权重开始教基本对话。

| 候选 | 在本机的定位 | 主要取舍 |
| --- | --- | --- |
| `Qwen/Qwen3-4B-Instruct-2507` | 首选，NF4 4bit QLoRA | 工具能力和资源开销较均衡；长上下文训练可能超过 8GB |
| `Qwen/Qwen3-1.7B` | 显存不足时的备选 | 上下文和激活显存余量更大；需固定 `enable_thinking=False`，复杂歧义任务能力需实测 |
| `Qwen/Qwen2.5-3B-Instruct` | 现有课程工具链仅支持 Qwen2.5 时考虑 | 支持工具模板和结构化输出，但许可为 Qwen Research，不能当作 Apache-2.0 |
| 7B/8B 模型 | 本机首轮不优先 | 4bit 推理可能可行，但训练激活、优化器和长工具历史使 8GB 余量不足 |

4B 的 BF16 权重本身约 8GB（十进制），再加激活和运行时，无法在这张卡上舒适地训练。4bit 权重的理论主体约 2GB，但量化元数据、未量化层、KV cache、激活、LoRA 和优化器仍占显存。4B QLoRA 在短序列、batch size 1 下可作为 8GB 的尝试方案，是否能跑必须以本机峰值显存为准；不保证完整长轨迹都能装下。

## 建议起步参数与上下文限制

- 从原始 Hugging Face 权重加载并做 NF4 4bit 量化，开启 double quantization，BF16 计算；不要把 GGUF 推理文件作为 PEFT 训练权重。
- micro batch size 1，gradient accumulation 8～16，gradient checkpointing，LoRA rank 8，先以 `q_proj`、`v_proj` 作为目标模块做小规模验证，再考虑增加模块和 rank。
- 先拿一条真实样本测 `forward + backward + optimizer step`；以 4096 token 作为显存探测起点，不直接启动整批训练。需要更长上下文而 4B 放不下时，切换 1.7B 或采用更大显存设备。
- 将每次助手决策拆成训练样本，保留该决策所依赖的历史工具结果；只对助手调用及最终回答计算 loss。不能直接截掉参数 schema、依赖回执或目标动作来凑长度。

本次单订单每轮输入为 2,268～4,389 tokens，批量任务为 2,309～6,837 tokens（DeepSeek tokenizer 计数）。因此 2048 token 训练长度很可能连规则和 schema 都放不下，4096 也不足以覆盖所有后期决策；必须用 Qwen tokenizer 重新统计长度，再确定 6144/8192 的可行性或有依据地压缩上下文。模型标称的 256K 上下文不代表 8GB 显卡能使用该长度。

训练前后使用同一个模型及 tokenizer、量化设置、工具 schema、提示、预算和推理配置，只切换 LoRA 权重做对照。DeepSeek API 可用于收集和核验教师轨迹，不能把 DeepSeek 与 Qwen 的差异作为 SFT 提升。

建议另建训练环境，避免改变当前已验证的 Agent 环境。原生 Windows 的 bitsandbytes 已有官方 CUDA wheel，RTX 4060 对应硬件可用；实际还要验证 PyTorch/CUDA/量化版本组合。若选用主要面向 Linux 的训练优化或服务框架，再考虑 WSL2。Qwen3 需要 transformers 至少 4.51.0，最终依赖组合应安装后实测锁定。

## 查阅来源

- [Qwen3-4B-Instruct-2507 官方模型卡](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)：参数、许可、非思考模式、工具调用及框架要求。
- [Qwen3-1.7B 官方模型卡](https://huggingface.co/Qwen/Qwen3-1.7B)：小显存备选及思考模式开关。
- [Qwen2.5-3B-Instruct 官方模型卡](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)：模型许可和工具模板。
- [bitsandbytes 安装文档](https://huggingface.co/docs/bitsandbytes/main/en/installation)：Windows CUDA 与 NF4 支持；main 文档随开发更新，安装时以所选稳定版要求为准。