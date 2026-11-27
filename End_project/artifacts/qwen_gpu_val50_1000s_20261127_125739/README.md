# Qwen3-4B完整val50：1000秒预算重跑

**已独立重跑50/50题，正确19/50（38.00%），模型已释放。**
本次所有任务从第1题开始执行，`resumed_tasks=0`，没有复用前次结果。

模型：`Qwen/Qwen3-4B-Instruct-2507`，未训练，NF4 4bit / double quantization / BF16 / SDPA，RTX4060 Laptop 8GB。
代码提交：`607fc14c6c2db463086b4e76359dcb54e70ba798`。源文件、50个环境快照和模型版本记录见 [source_provenance.json](source_provenance.json)。

## 与前次600秒预算的同50题对照

| 指标 | 本次1000秒 | 前次600秒 | 变化（百分点） |
| --- | ---: | ---: | ---: |
| 整题正确率 | 19/50，38.00% | 16/50，32.00% | +6.00 |
| 字段匹配率 | 568/1134，50.09% | 542/1134，47.80% | +2.29 |
| 模型显式工具成功率 | 260/393，66.16% | 260/393，66.16% | +0.00 |

同题结果：两次均正确16题，本次新增正确3题，前次正确但本次失败0题，两次均失败31题。逐题停止原因和耗时对照见 [comparison.json](comparison.json)。

### 如何理解这次改善

新增正确的3题，正是前次结构化方案已完全匹配、但因超时而未正常结束的3题。本次耗时如下，全部小于原600秒限制：

| 任务ID | 前次停止原因 | 前次耗时/秒 | 本次耗时/秒 |
| --- | --- | ---: | ---: |
| 7f997d6ed7aa6422de146a5b31739cf0 | timeout | 600.078 | 134.406 |
| bd5d5f9c3276a58df77a2419a5efad6c | timeout | 600.500 | 343.859 |
| 01b486c3b0d11490d9b3d0369b87ebd4 | timeout | 600.328 | 320.437 |

因此，这次结果体现了这3题完成状态的改善，不能把提高的6个百分点单独归因于延长超时预算。工具显式调用总数、成功数和错误数均与前次相同，仍有101次交易不可用、32次参数错误；批量任务仍为0/22正确。

停止原因迁移：`{"completed -> completed": 16, "timeout -> timeout": 1, "decision_budget -> decision_budget": 14, "timeout -> submission_rejected": 5, "timeout -> completed": 3, "submission_rejected -> submission_rejected": 6, "timeout -> decision_budget": 5}`。前次14题超时，本次其中3题正确完成、5题耗尽决策轮数、5题提交被拒绝、1题仍超时。超时数下降不等于其余错误全部解决。

这次改变的是单题超时预算（600→1000秒）。模型、Agent提示词、业务工具、评分器及其余推理预算已核对一致；前次采用36+14断点恢复，本次从头独立运行。设备执行和缓存热身差异也可能影响超时，单次对照不替代重复实验。尚未执行训练或正式留出test推理。

## 配置和运行状态

- 每题1000秒；最多12轮决策、48次工具调用、60步。
- 上下文16384；每轮最多输出2048 tokens；贪心解码；CPU线程4。
- 开始：2026-11-27T12:58:42.986343+08:00；结束：2026-11-27T15:50:12.271109+08:00（北京时间）。
- 墙钟约171.5分钟；逐题耗时合计10243.870秒。
- 停止原因：`{"completed": 19, "timeout": 1, "decision_budget": 19, "submission_rejected": 11}`。
- 提交核验通过19题；模型清理：`{"status": "closed", "allocated_after_close_mib": 8.13}`。
- 本地API费用0 USD；硬件、电费未实测，未提供算力单价。

`phase=finished`表示50题均已处理。进程退出码1可由部分题超时、预算耗尽或提交被拒引起，具体看逐题停止原因。`completed`要求生成报告且通过运行时核验；整题正确率还核对独立参考答案。余额计算和提交核验由运行时执行，工具成功率只统计模型显式调用。中文报告、证据引用文字及复核理由未自动做语义评分。

## 请求类型和场景

| 请求类型 | 正确/任务数 | 准确率 |
| --- | ---: | ---: |
| period_batch | 0/22 | 0.00% |
| single_order | 19/28 | 67.86% |

| 场景分类 | 正确/任务数 | 准确率 |
| --- | ---: | ---: |
| basic | 11/17 | 64.71% |
| boundary | 6/16 | 37.50% |
| cross_tool | 2/17 | 11.76% |

## 工具和失败记录

模型显式工具调用次数：`{"query_orders": 78, "search_receipts": 96, "query_refunds": 58, "find_match_candidates": 95, "get_transaction_evidence": 66}`。
未显式选择的工具：`["calculate_reconciliation", "check_duplicate_events", "validate_reconciliation"]`。
工具错误：`{"INVALID_ARGUMENT": 32, "TRANSACTION_UNAVAILABLE": 101}`。
结构化方案完全匹配但未正常结束、仍按失败计的题数：1。

具体错误和原始回执见 [evaluation.md](evaluation.md)、[traces.json](traces.json)。所有超时和失败题均保留，未依据得分挑选重试。

## 归档与核查

已确认50个任务ID各出现一次且顺序与运行清单一致，全部环境/源码哈希与启动记录相符，离线重新评分与保存结果一致。见 [verification.json](verification.json)。

- [summary.json](summary.json)：总体和逐题指标。
- [evaluation.md](evaluation.md)：独立评分及字段差异。
- [traces.json](traces.json)、[traces.md](traces.md)：完整已保存轨迹。
- [comparison.json](comparison.json)：与600秒预算的逐题对照和分组统计。
- [run_manifest.json](run_manifest.json)、[run_status.json](run_status.json)：参数、50题清单和清理状态。
- [stdout.log](stdout.log)、[stderr.log](stderr.log)、[process_status.json](process_status.json)：日志和进程退出记录。
- [source_provenance.json](source_provenance.json)、[environment.txt](environment.txt)：模型版本、源码/环境快照。
- [archive_manifest.json](archive_manifest.json)：归档文件大小和SHA256，保留原始Windows换行字节。

## 复跑

在 `End_project` 目录运行，输出目录必须不存在：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 50 --timeout 1000 --max-decisions 12 --max-context 16384 --max-new-tokens 2048 --output-dir artifacts/qwen_val50_1000s_new
```
