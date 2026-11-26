# Windows 本地运行记录

## 2026-11-26：50条验证集后台运行

**已完成**：北京时间05:08处理完50/50题，模型及工作/监督进程均已退出。完整产物约7.13 MiB，全部归档；结果、失败原因及文件索引见 [val50结果摘要](../artifacts/qwen_gpu_val50_20261126_004832/README.md)。

整题精确匹配率0%（0/50），字段匹配率25.04%，15/50题全部金额字段匹配，工具调用成功率71.24%（213/299）。40题返回结构化结果，8题超时、1题输出超限、1题耗尽决策轮数。主要问题是事件ID/交易ID混淆、复核标记错误、订单覆盖不完整，且没有调用计算或方案校验工具。总耗时约4小时19分，本地API费用0，硬件/电费未实测。

已于北京时间 00:49 启动本地Qwen验证集全量50题，单题预算600秒、最多12轮决策、上下文16384、单轮输出2048；保持当前NF4/BF16和SDPA配置。此次只读取 `val`，不访问留出测试集。

- 结果目录：`artifacts/qwen_gpu_val50_20261126_004832/`。
- `run_status.json`：实时阶段、进程PID、当前任务和已处理数量。`phase=finished`表示50题全部处理完，不代表全部答对。
- `summary.json`、`traces.json`、`traces.md`、`evaluation.md`：每题后更新。未跑完时准确率仅针对已处理任务，请同时查看 `run_progress`。
- 日志与进程状态：原位于 `artifacts/gpu_setup/val50_20261126_004832/`，已将 `stdout.log`、`stderr.log` 和 `process_status.json` 一并复制到结果目录归档。

入口现支持一次最多50题，使用同一模型顺序运行；检查点JSON通过临时文件替换保存。正常结束和异常退出均在finally中释放模型，然后Python进程退出，销毁其CUDA上下文。`run_status.json`记录清理结果，监督进程在工作进程退出后也自动退出。新增的50题保存与异常清理生命周期检查后，共107项测试通过。

## 2026-11-26：逐题评分与成本统计

已新增独立的运行后评测，真实API与本地Qwen入口都会自动生成 `accuracy`、`cost`、`evaluation` 和 `evaluation.md`。当前104项测试通过，包含错误金额、pending退款、重复/多余订单、末次提交覆盖、缺失提交、费用估算和离线评分无模型调用等检查。

指标口径：

- `accuracy`：结构化方案整题精确匹配率（单题0或1）。订单覆盖、7项金额、收款/退款/待退款交易ID、复核标记、未分配交易必须全对，且正常返回最终文本。另有字段匹配率；不会从查询工具的正确回执自动拼装答案替模型得分。
- `evaluation`：方案来源、逐字段期望/实际差异、工具成功率、校验结果及失败代码。只在运行结束后读取对应train/val参考答案，不进入模型消息；脚本/规则演示不计入模型准确率。
- `cost`：本地 `api_fee=0`；真实记录耗时、token、输出速度。硬件/电费未实测，`compute_fee_estimate`仅在提供每小时单价后填写。API费用没有单价或usage时明确标记缺失；提供单价时是估算，不是账单。

已为先前两次Qwen实跑补评，并更新原目录的 `summary.json`、`traces.json` 和 Markdown；原始未评分JSON保留为 `summary.unscored.json`、`traces.unscored.json`。补评未改变模型消息、工具动作或最终回答，也未重跑GPU。

| 旧样例 | 整题结构化方案准确率 | 工具成功率 | 耗时/秒 | API费用 | 原因 |
| --- | ---: | ---: | ---: | ---: | --- |
| 单订单 | 0% | 75%（3/4） | 468.547 | 0 USD | 缺少结构化方案提交 |
| 三订单 | 0% | 25%（2/8） | 514.953 | 0 USD | 缺少结构化方案提交，另有6次工具报错 |

旧提示词没有强制要求结构化输出，已标记 `submission_contract_requested=false`。这里的0%表示未满足当前方案交付规范，不等于判定单订单文字中的所有金额都错误；自然语言报告、证据引用、复核理由和缺失字段说明未自动评分。后续提示词已要求提交结构化方案。新旧提示设置不同，不能直接据此比较模型能力变化。

合并结果见 [两题评测报告](../artifacts/qwen_gpu_evaluation_20261126/evaluation.md)。也可离线补评其他已保存的JSON/JSONL：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 agent_cli.py --evaluate-trace artifacts/qwen_gpu_initial_20261126/traces.unscored.json --split train --output-dir artifacts/qwen_evaluation_new
```

输出目录须不存在。`--split`及数据集需与轨迹一致。若要按自定单价估算本地算力，可添加 `--compute-price-per-hour` 和 `--cost-currency`；API估价使用 `--input-price-per-million`、`--output-price-per-million`。

## 2026-11-26：本地 Qwen GPU 环境

已补齐 `.venv-gpu` 的依赖并解决 NumPy 冲突：PyTorch 2.5.0+cu118、Transformers 4.55.4、Accelerate 1.10.1、bitsandbytes 0.47.0、NumPy 1.24.4。该环境复用父级 Conda 的 CUDA PyTorch，不修改全局环境。`pip check` 无冲突，89 项现有测试通过，CUDA 矩阵运算和 BF16 检查通过。

模型目录为 `models/Qwen3-4B-Instruct-2507`。全部 12 个文件已按本地下载清单重新校验大小与 SHA256；三片权重完整。使用 NF4 4bit 在 RTX 4060 Laptop 8GB 上加载，以 BF16 计算。

```powershell
Set-Location 'D:\All_ws\LM_Theory_Practice\End_project'
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py
# 一次加载模型，测试前两条训练任务（单订单及三订单批量）
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --limit 2
```

入口现支持小批量、逐题保存、逐轮生成日志和 Markdown 轨迹。默认上下文 16384、每轮最多生成 2048 tokens，并限制 CPU 线程为 4。原有 `.venv` 仍可运行下方的 API/规则用例。完整依赖安装及参数说明见 [Qwen本地测试](Qwen模型下载与本地测试.md)。

已清理下载完成后不再需要的 `scripts/download_qwen.py`、`scripts/download_ranges.py` 和依赖 macOS 字体的一次性 `scripts/export_pipeline.py`；模型、数据、流程图及测试保留。

### 已完成的单订单试跑

结果：`artifacts/qwen_gpu_initial_20261126/`，包含完整 `traces.json`、`summary.json` 和 `traces.md`。任务 ID 为 `f3c95789ace1a9542c5d6baed2eac902`，使用原入口参数（8192 上下文、1024 输出上限、600 秒预算）。

- 真实本地模型连接成功，5 轮决策、4 次工具调用，468.547 秒后生成最终报告，累计生成 1021 tokens。PyTorch 峰值已分配显存 3249.4 MiB；这个数字不含其他程序及驱动占用。
- 第一次 `query_orders` 同时提供订单号和账期，被工具拒绝；下一轮自行纠正参数。之后调用 `search_receipts` 和 `query_refunds`。
- 读到应收/实收 10697 BRL 分、退款 0，最终金额及差额描述与回执一致。
- 未调用查重、计算或 `validate_reconciliation`，因此无完整方案校验通过证据。
- 最终文本错误地称交易时间“等于截止时间”：工具回执中的交易时间是 2018-01-22，截止是 2018-01-24；还为单订单请求自行补充了账期描述。

这次试跑说明当前基模能完成基础工具查询与错误参数纠正，但存在证据表述错误和校验遗漏。`completed` 不代表业务正确，不能据一题声称总体正确率。

### 三订单批量试跑

结果：`artifacts/qwen_gpu_batch_20261126/`，含 JSON/Markdown 完整轨迹和摘要。实际命令：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --task-id 004498f4b987f7c1cc9c26a813678d7a --timeout 600 --max-decisions 16 --output-dir artifacts/qwen_gpu_batch_20261126
```

输出目录已经存在，复跑时请换一个新名称。此次上下文 16384、每轮输出上限 2048、CPU 线程 4。实跑 9 轮决策、8 次工具调用，其中 6 次报错；514.953 秒后生成最终文本，累计输出 1119 tokens，PyTorch 峰值已分配显存 3413.71 MiB。平均生成速度约 2.2 tokens/秒，当前端到端耗时偏长。

暴露的问题：

1. `query_orders` 成功取得 3 单，但模型将订单创建账期误用为收款的 `effective_start/end`，筛掉了账期结束后、核查截止前的合法收款。
2. 收款检索为空后，它把 3 个 `merchant_reference` 当作 `transaction_id`，分别调用候选匹配和交易凭证查询，产生 6 次 `TRANSACTION_UNAVAILABLE`。
3. 没有重新检索收款，也没有调用 `query_refunds`、计算或方案校验；最终错误声称所有交易均缺失，并建议补数据。

运行结束后，仅通过可见工具复查：不附加错误时间筛选即可查到 3 笔成功收款（9643、15995、16302 分，均在 2018-06-13 生效），逐单查询还能查到第一单 3214 分的成功退款（2018-06-14 生效）。这些都早于 2018-06-15 核查截止，因此该题失败来自模型的参数选择与错误恢复。复查保存在 `visible_tool_audit.json`，明确标注为运行后的审阅查询，不属于模型轨迹，也没有把复查结果反馈给模型。

两道训练样例均确实由本地 GPU 基模决策；没有读取留出测试题、训练或接入 API。两题均未提交方案校验，业务闭环通过数为 0；这里不据此推算总体正确率。当前配置的基础查询能力可用，多订单、时间边界、ID 类型区分和方案校验仍需改进。测试过程未修改现有系统提示词来引导特定答案。

### 输出速度诊断

2026-11-26 追加性能对照。已确认所有模型参数都在 `cuda:0`，KV cache 已启用（DynamicCache），机器接通电源。20 次 2048×2048 BF16 GPU 矩阵乘法约 0.031 秒。

复用三订单任务首轮的实际提示词（2277 tokens），固定生成 32 tokens：

| 注意力设置 | 耗时 | 速度 |
| --- | ---: | ---: |
| 默认，允许 cuDNN SDPA | 15.156 秒 | 2.11 tokens/秒 |
| 关闭 cuDNN SDPA，其余配置相同 | 4.842 秒 | 6.61 tokens/秒 |

这次对照的生成 token IDs 完全一致。当前主要瓶颈指向这套 PyTorch 2.5.0+cu118 / Windows 环境中的 cuDNN 注意力执行路径。短提示词首次生成 16 tokens 约 2.82 tokens/秒，同样输入及长度再次运行约 14.29 tokens/秒，表现符合新形状准备或缓存开销较大的情况；Agent 上下文和解码长度持续变化，会反复遇到新形状。这是对照实验支持的推断，尚未通过完整 CUDA 时间线细分具体 cuDNN 内部耗时。

NF4 double quantization 的尺度解码也有次要开销：短提示词关闭 cuDNN 后约 14.4 tokens/秒，在内存中预先解开量化尺度后约 17.6 tokens/秒。这不是 Agent 长提示词的速度，不能混用。

关闭 cuDNN 后本机诊断记录中的解码走 SDPA math 后端，不能称为 Flash Attention 提速。后续应分别处理预填充与逐 token 解码的后端选择，再验证长上下文显存和完整 Agent 耗时。上述是诊断实验；生产推理配置及先前业务轨迹没有据此替换。

临时诊断程序与原始结果位于 `artifacts/gpu_setup/diagnose_latency.py`、`latency_diagnosis.json`（忽略目录）。

## 2026-11-25：API 与规则用例历史记录

2026-11-25，在 `D:\All_ws\LM_Theory_Practice\End_project` 实际执行。

## 环境

- Windows，Python 3.11.10；项目虚拟环境为 `.venv`。
- LangGraph 1.2.24；本次安装的完整依赖版本保存于 `requirements.lock.txt`。
- 本机 GPU 为 NVIDIA GeForce RTX 4060 Laptop GPU，显存 8188 MiB。本次规则演示和 LangGraph 脚本烟测使用 CPU，无需安装 PyTorch/CUDA。
- `pip check` 通过，86 项 unittest 全部通过，无跳过。

PowerShell 中进入项目后执行以下命令，无需激活虚拟环境。`-X utf8` 用于避免 Windows 默认 GBK 读取中文依赖说明和 JSON 时出错。

```powershell
Set-Location 'D:\All_ws\LM_Theory_Practice\End_project'

# 本机环境已创建。另一台机器可先用 Python 3.11 创建：
python -m venv .venv
& '.\.venv\Scripts\python.exe' -X utf8 -m pip install -r requirements.lock.txt --progress-bar off
& '.\.venv\Scripts\python.exe' -X utf8 -m pip check
```

## 数据

复用仓库已准备好的 Olist 衍生对账数据，无需重复下载原始 CSV。订单与金额来源于公开数据，收款/退款事件及异常由程序合成；详细来源见同目录的《数据来源与合成说明.md》。

| 数据目录 | 训练 | 验证 | 留出测试 | 校验文件哈希数 |
| --- | ---: | ---: | ---: | ---: |
| `datasets/prepared` | 200 | 50 | 360 | 623 |
| `datasets/smoke` | 12 | 12 | 24 | 61 |

两套数据均通过 `validate_data.py` 校验，跨切分源订单与客户重叠均为 0。本次留出集仅做静态数据完整性校验，用例运行选用训练集。

```powershell
& '.\.venv\Scripts\python.exe' -X utf8 scripts/validate_data.py datasets/prepared
& '.\.venv\Scripts\python.exe' -X utf8 scripts/validate_data.py datasets/smoke
```

## 完整业务用例

新增入口自动读取任务及对应环境，执行既有八工具规则演示，将完整请求、工具参数、回执及方案保存为 UTF-8 缩进 JSON。它使用确定性规则选择工具，无需模型 API。

```powershell
# 默认运行第一条训练任务，输出到带时间戳的新目录
& '.\.venv\Scripts\python.exe' -X utf8 scripts/run_local_case.py

# 指定三订单批量任务，输出目录同样自动生成
& '.\.venv\Scripts\python.exe' -X utf8 scripts/run_local_case.py --task-id 004498f4b987f7c1cc9c26a813678d7a

# 可选：--split val、--task-id 指定任务、--output-dir 指定不存在的新目录
```

实跑结果：

1. 单订单任务 `f3c95789ace1a9542c5d6baed2eac902`：8 次调用覆盖全部 8 种工具，应收和实收均为 BRL 106.97，退款 0，收款差额 0，`valid=true`、`errors=[]`。结果位于 `artifacts/local_case_windows_20261125/summary.json` 和 `traces.json`。
2. 三订单任务 `004498f4b987f7c1cc9c26a813678d7a`：16 次调用覆盖全部 8 种工具，3 单应收/实收分别为 BRL 96.43、159.95、163.02；第一单已退 BRL 32.14、净收 BRL 64.29，3 单收款差额均为 0，`valid=true`、`errors=[]`。结果位于 `artifacts/local_batch_windows_20261125/summary.json` 和 `traces.json`。

## LangGraph 调用流程

```powershell
# 指定尚不存在的目录，可更换末尾名称再次运行
& '.\.venv\Scripts\python.exe' -X utf8 agent_cli.py --backend scripted --split train --limit 1 --output-dir artifacts/windows_smoke_new
& '.\.venv\Scripts\python.exe' -X utf8 -m unittest discover -s tests -v
```

本次烟测目录为 `artifacts/windows_smoke_20261125/`，3 次脚本决策、2 次工具调用，正常结束。该烟测只检查 LangGraph 查询回路，不执行完整对账；完整业务验证使用上一节的规则用例。

## 真实模型接入状态

首次环境准备时未检测到模型 API 配置，当时只执行了规则用例与图调用流程。用户随后补充配置，已使用 deepseek-flash 跑通真实单订单及三订单任务，最终方案均通过工具核验；详见 [API实跑与基模建议](API实跑与基模建议.md)。这两题不代表总体正确率或微调训练完成。

如需实际模型决策，在当前 PowerShell 会话中设置 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`MODEL_NAME`，再执行：

```powershell
& '.\.venv\Scripts\python.exe' -X utf8 agent_cli.py --backend api --split train --limit 1 --output-dir artifacts/api_windows_new
```

项目当前通过环境变量读取配置，不会自动加载 `.env`。变量名称及服务示例见 `.env.example`；真实密钥保存在本地，不写入提交文件。
