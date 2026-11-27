# 新版 Agent 首段运行：36/50题中断记录

**剩余14题已在断点恢复中补齐，最终结论请看 [完整val50报告](../qwen_gpu_val50_20261127_completed_081945/README.md)。** 本目录保留初始运行的原始记录，指标分母为36。准备第37题时替换 `run_status.json.tmp` 发生 `PermissionError: [WinError 5]`；该题尚未执行，具体文件占用者未定位。原36条结果已逐字段继承到完整归档。

模型为本地 Qwen/Qwen3-4B-Instruct-2507，未微调。运行版本和源码 SHA256 见 [source_provenance.json](source_provenance.json)。

开始：2026-11-27T00:54:23.621238+08:00；结束：2026-11-27T04:46:28.279841+08:00。
运行状态：`failed`；已处理 36/50 题。

| 指标 | 本次前36题 | 历史相同36题（2026-11-26） |
| --- | ---: | ---: |
| 整题精确匹配率 | 30.56% | 0.00% |
| 字段匹配率 | 52.07%（427/820） | 19.15%（157/820） |
| 工具调用成功率 | 65.59%（183/279） | 69.91%（151/216） |

通过运行时提交核验的题数：11。
停止原因：`{"completed": 11, "timeout": 11, "decision_budget": 10, "submission_rejected": 4}`。
模型清理：`{"status": "closed", "allocated_after_close_mib": 8.13}`。

本次仅运行 val，不运行留出测试集。使用 NF4 4bit/BF16，单题600秒、12轮决策、上下文16384、每轮输出2048 tokens，与历史推理预算相同。新版流程自动计算提交余额、核验方案并反馈错误；因此是 Agent 流程对照，不是训练前后比较，工具调用统计也需结合新流程中的隐式核验解释。

当前 completed 要求报告及运行时方案核验通过，历史 completed 仅表示返回文本；业务正确性以独立评分为准。局部结果或超时题如实保留。仅在所有50题均处理后才能将本次指标称为完整 val50 结果。

- [evaluation.md](evaluation.md)：独立评分和字段差异。
- [summary.json](summary.json)：逐题和总体指标。
- [traces.md](traces.md)、[traces.json](traces.json)：完整已保存轨迹。
- [comparison.json](comparison.json)：与历史批次的指标对照。
- [run_manifest.json](run_manifest.json)、[run_status.json](run_status.json)：任务、参数与清理状态。
- [process_status.json](process_status.json)、[stdout.log](stdout.log)、[stderr.log](stderr.log)：退出码和控制台日志。
- [environment.txt](environment.txt)：启动时 Python 包版本。
- [verification.json](verification.json)：离线重新评分及原始文件核查。
- [archive_manifest.json](archive_manifest.json)：本目录归档文件SHA256。
