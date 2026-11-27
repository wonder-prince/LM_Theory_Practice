# 新版 Agent：Qwen3-4B 完整 val50 结果

**已处理50/50题，独立评分正确16/50（32.00%）。**
本批次由原运行的36题和断点续跑的14题组成，前36条结果对象逐字段保留，全部50个任务ID与原清单一致，无重复或漏题。

模型：`Qwen/Qwen3-4B-Instruct-2507`，未微调，NF4 4bit、double quantization、BF16、SDPA，RTX4060 Laptop 8GB。
框架核心为提交 `5519521` 的新版流程；启动时仓库HEAD为 `cd65a68`。续跑只修复批处理入口的状态写入重试并增加 `--resume-from`，Agent提示词、业务工具、模型后端与评分器未变。源码哈希见 [source_provenance.json](source_provenance.json)。

## 与历史同50题对照

| 指标 | 本次新版流程 | 2026-11-26历史流程 | 变化（百分点） |
| --- | ---: | ---: | ---: |
| 整题精确匹配率 | 16/50，32.00% | 0/50，0.00% | +32.00 |
| 字段匹配率 | 542/1134，47.80% | 284/1134，25.04% | +22.75 |
| 模型显式工具调用成功率 | 260/393，66.16% | 213/299，71.24% | -5.08 |

运行时提交核验通过：16题。停止原因：`{"completed": 16, "timeout": 14, "decision_budget": 14, "submission_rejected": 6}`。

本次整题准确率比历史同50题提高32个百分点，字段匹配率提高22.75个百分点，模型显式工具成功率下降5.08个百分点。单订单正确16/28，批量对账0/22；批量题的停止原因是14题耗尽决策轮数、7题超时、1题提交被拒绝。流程已能使部分单订单形成正确闭环，批量覆盖、交易归属及错误恢复仍是主要短板。

393次模型显式调用只覆盖 `query_orders`、`search_receipts`、`query_refunds`、`find_match_candidates`、`get_transaction_evidence` 五种工具。`check_duplicate_events`、`calculate_reconciliation` 和 `validate_reconciliation` 未被模型显式选择，后两项的提交计算/核验由运行时处理。工具错误为101次交易不可用、32次参数错误。这些计数与通过运行时提交核验的16题应分开理解。

新旧使用同一验证集、基模与推理预算，但Agent提示词、余额计算及提交修正流程不同；这是流程改动的对照，不是训练前后模型能力对照。当前 `completed` 要求报告及提交核验通过，历史 `completed` 仅表示返回文本。程序自动计算余额和核验不能算作模型自行正确计算；工具成功率仅统计模型显式调用，不包含运行时内部计算/核验。中文报告、证据引用文字与复核理由未做自动语义评分。

## 请求类型和场景

| 请求类型 | 正确/任务数 | 准确率 |
| --- | ---: | ---: |
| period_batch | 0/22 | 0.00% |
| single_order | 16/28 | 57.14% |

| 场景分类 | 正确/任务数 | 准确率 |
| --- | ---: | ---: |
| basic | 9/17 | 52.94% |
| boundary | 6/16 | 37.50% |
| cross_tool | 1/17 | 5.88% |

## 失败与运行中断

工具报错统计：

- `INVALID_ARGUMENT`：32 次。
- `TRANSACTION_UNAVAILABLE`：101 次。

失败还包括超时、耗尽决策预算及提交核验未通过。逐题的字段差异、停止原因及真实回执以 [evaluation.md](evaluation.md) 和 [traces.json](traces.json) 为准。结构化方案完全匹配但未正常结束的题仍按失败计，共3题。

初始运行时间：2026-11-27T00:54:23.621238+08:00 至 2026-11-27T04:46:28.279841+08:00（北京时间）。在准备第37题、替换 `run_status.json.tmp` 为 `run_status.json` 时出现 `PermissionError: [WinError 5]`，保存的36题完整。具体文件占用者未定位。原始异常日志及36题记录见 [原运行归档](../qwen_gpu_val50_20261127_005227/README.md)。

续跑时间：2026-11-27T08:21:28.894717+08:00 至 2026-11-27T09:27:49.410525+08:00（北京时间）。新入口对JSON临时文件写入/替换的 `PermissionError` 做最多10次有限退避重试；`--resume-from` 校验任务清单、预算、模型目录、规则及核心源码哈希，只执行剩余14题并写入新目录。

两段活动墙钟时间合计约 298.4 分钟，不包含两段间等待。逐题耗时合计 17861.025 秒。本地API费用0 USD；硬件和电费未实测。两次加载及缓存热身可能影响计时和超时，报告明确保留了分段事实。

处理结束后模型清理状态：`{"status": "closed", "allocated_after_close_mib": 8.13}`。仅运行val，未执行训练或留出test推理。

## 验证与文件

离线重新评分与已保存评分一致；确认50个ID各出现一次、原36条结果完全保留、推理预算与历史一致；检查结果见 [verification.json](verification.json)。完整归档文件的SHA256见 [archive_manifest.json](archive_manifest.json)。

- [summary.json](summary.json)：50题总体及逐题指标。
- [evaluation.md](evaluation.md)：独立评分和字段差异。
- [traces.md](traces.md)、[traces.json](traces.json)：全部已保存轨迹。
- [comparison.json](comparison.json)：同50题指标、请求类型及分类统计。
- [run_manifest.json](run_manifest.json)、[run_status.json](run_status.json)：任务、参数和清理状态。
- [stdout.log](stdout.log)、[stderr.log](stderr.log)、[process_status.json](process_status.json)：续跑控制台和进程退出记录。
- [source_provenance.json](source_provenance.json)、[environment.txt](environment.txt)：续跑源码哈希和环境快照，前36题来源另见原运行。

## 复跑及断点恢复

在 `End_project` 中完整运行到新的输出目录：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 50 --timeout 600 --max-decisions 12 --max-context 16384 --max-new-tokens 2048 --output-dir artifacts/qwen_val50_new
```

如果进程因基础设施错误中断，可保持相同参数，增加 `--resume-from 原结果目录`，并指定另一个不存在的输出目录。已保存的超时或错误题也会保留，续跑只补尚未保存的任务，避免按结果挑选重试。
