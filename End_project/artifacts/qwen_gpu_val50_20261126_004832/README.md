# Qwen3-4B 验证集50题实跑结果

2026-11-26（北京时间）00:49:23—05:08:36，使用本地 `Qwen/Qwen3-4B-Instruct-2507` 顺序处理完整50题验证集。工作进程及监督进程均已退出，模型已释放。未微调，也未运行留出测试集。

## 结果摘要

| 指标 | 结果 |
| --- | ---: |
| 已处理任务 | 50/50 |
| 整题方案精确匹配率 | **0%（0/50）** |
| 字段匹配率 | 25.04% |
| 全部7项金额字段匹配的任务 | 30%（15/50） |
| 返回结构化结果 | 80%（40/50，包含空方案） |
| 工具调用成功率 | 71.24%（213/299） |
| 工具报错 | 86次 |
| 总墙钟时间 | 约4小时19分 |
| 单题平均运行时间 | 310.21秒，不含模型加载和评分 |
| 本地API费用 | 0 USD，硬件/电费未实测 |

停止原因：40题正常返回文本，8题超时，1题达到单轮输出上限，1题耗尽决策轮数。`completed`只表示返回了最终文本，不能视为业务正确。进程退出码1表示批次中存在未正常完成的题目；50题均已处理，批次未因中途崩溃漏题。

共记录1,116,135输入tokens和63,203输出tokens，合计1,179,338；输入包含多轮重复历史。部分生成因超时/输出限制未计入，因此这不是完整用量。

## 主要失败情况

- 32处将 `event_id` 填入要求 `transaction_id` 的收款或退款列表。
- 24个已提交订单的 `review` 标记与独立参考答案不符，包含把正常匹配订单标为待复核的情况。
- 批量任务出现遗漏订单、提交空 `orders`，以及误用收款时间筛选的情况。
- 全批没有调用 `calculate_reconciliation` 或 `validate_reconciliation`。部分金额由模型自行填写，出现金额扩大十倍、净收差额符号错误等问题。
- 工具错误分布：`TRANSACTION_UNAVAILABLE` 70次、`INVALID_ARGUMENT` 14次、`INVALID_KIND` 2次。

整题评分要求订单覆盖、7项金额、收款/退款/待退款交易归属、复核标记和未分配交易全部匹配，并正常返回最终文本。15题金额字段全部正确仍未满足整题要求，不能把0%理解成所有金额都算错。

参考答案只在各题生成结束后由独立评分器读取，没有反馈给模型。中文报告、证据引用文字、复核理由与缺失字段说明不做自动语义评分。这是当前提示词、量化方式及预算下的验证集表现，不能替代正式留出集评测或训练前后对照。

## 配置与复跑

- RTX4060 Laptop，8GB显存；PyTorch峰值已分配显存3684.07 MiB。
- NF4 4bit、double quantization、BF16计算、SDPA；本次保持默认cuDNN SDPA设置，未应用后续诊断中的后端调整。
- PyTorch 2.5.0+cu118，Transformers 4.55.4，Accelerate 1.10.1，bitsandbytes 0.47.0。
- 每题600秒，最多12轮决策、48次工具调用、60步；上下文16384，单轮最多生成2048 tokens；贪心解码，CPU线程4。

在 `End_project` 目录运行，输出目录应为不存在的新目录：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 50 --timeout 600 --max-decisions 12 --max-context 16384 --max-new-tokens 2048 --output-dir artifacts/qwen_gpu_val50_new
```

保持本次模型目录和依赖版本，详细安装说明见 [Qwen本地测试](../../docs/Qwen模型下载与本地测试.md)。模型权重、虚拟环境和密钥不在结果归档中。

## 文件索引

- [summary.json](summary.json)：总体及逐题指标、失败原因和字段差异。
- [evaluation.md](evaluation.md)：逐题评测表与差异明细。
- [traces.json](traces.json)：50题的已保存模型消息、工具调用、回执及最终输出。
- [traces.md](traces.md)：便于人工查看的完整轨迹。
- [run_manifest.json](run_manifest.json)：50个任务ID及实际参数。
- [run_status.json](run_status.json)：批次最终状态与模型清理记录。
- [process_status.json](process_status.json)：监督进程记录的退出状态。
- [stdout.log](stdout.log)、[stderr.log](stderr.log)：工作进程控制台日志。

原有6个结果文件合计7,480,195字节（约7.13 MiB），体积适中，全部归档，无抽样删减。控制台日志和退出状态另行补入。JSON为程序处理入口；较大的Markdown或JSON可下载后本地查看。
