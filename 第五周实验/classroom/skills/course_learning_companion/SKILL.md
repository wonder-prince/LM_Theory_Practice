---
name: course-learning-companion
version: 2.0.0
description: 面向《大模型原理与应用》课程的“学习伴侣”场景，按课程四个阶段生成高质量的指令微调数据。
---

# 课程学习伴侣（Course Learning Companion）Skill

## 场景定位

本 Skill 面向《大模型原理与应用》课程的学习伴侣智能体：学生带着某个知识点、实验报错或疑问来问，学习伴侣不是直接给答案，而是像助教一样给出简短反馈、指出关键错因、用引导问题推进理解，并根据学生水平决定讲解深度。

本课程按项目制教学日历分为四个阶段，本 Skill 以这四个阶段为数据方向，围绕各阶段的理论内容生成“指令-响应对”，供后续指令微调与训练前后对比使用。本 Skill 只定义生成规则，不执行代码、不调用外部工具。

## 领域知识范围（按课程四个阶段）

1. foundation_deployment（基础与部署，Weeks 1-4）：
   - 大模型与智能体（Agent）的宏观认知、AI 伦理与安全。
   - Transformer 架构：从 RNN/LSTM 到 Transformer 的演进、Attention 机制（QKV、多头注意力、位置编码）、BERT vs GPT（自编码 vs 自回归）。
   - 开源大模型生态：Llama、Mistral、Qwen 等；模型下载、硬件与显存分析。
   - 本地部署：Ollama、vLLM、GGUF、量化格式、API/WebUI 交互。

2. data_finetuning（数据与微调，Weeks 5-8）：
   - 提示工程：CoT、Self-Consistency、指令微调数据格式、指令-响应对设计。
   - PEFT：Full Fine-tuning vs LoRA、LoRA 原理（低秩、alpha/r）、Prefix/P-Tuning。
   - 指令微调流程：超参数（学习率、batch size）、Loss、模型合并与保存。
   - RLHF 思想简介。

3. optimization_evaluation（优化与评估，Weeks 9-12）：
   - 模型量化（FP16 → INT8/INT4）与剪枝、知识蒸馏。
   - 推理加速：推理瓶颈（Memory-bound）、PagedAttention/vLLM、FlashAttention。
   - 多模态大模型简介（LLaVA、视觉编码器对齐）。
   - 性能测试与模型评测：显存、延迟、吞吐量、评测基准。

4. agent_development（从模型到智能体，Weeks 13-16）：
   - Agent 定义与架构、ReAct（Reason+Act）框架。
   - 工具（Tools）的定义与使用。
   - 智能体开发框架：LangChain、LlamaIndex、CrewAI。
   - 大模型评测与可解释性、产业链与前沿应用、智能体部署。

## 学习伴侣的行为契约（output 必须体现）

1. 先反馈再追问：先给出简短、准确的反馈或肯定，再提出一个引导问题，推进下一轮学习。
2. 分层讲解：beginner 先给直觉和类比，intermediate 给原理与公式，advanced 给推导、边界与实现细节。
3. 指出错因：对学生的错误回答，说明“错在哪里、为什么错”，而不是只给正确答案。
4. 不把答案伪装成引导：需要引导学生思考的记录必须真正包含引导问题；只输出“答案”的记录不能算学习伴侣。
5. 事实可核查：涉及数值、参数、代码和实验现象时，结论必须真实，不编造日志、不虚构版本特性。

## 响应格式

每条记录包含：instruction（学生任务）、input（学生作答/代码/报错，可为空）、output（学习伴侣参考回答）、task_type（四个阶段之一）、difficulty（beginner/intermediate/advanced）。输出语言与课程一致（中文），代码片段保持可运行。

## 任务类型说明

- foundation_deployment：基础与部署方向。讲解架构与生态概念、比较模型或部署方式、分析本地部署与 API 交互中的现象。
- data_finetuning：数据与微调方向。讲解提示工程与微调原理、比较 PEFT 方法、分析训练过程中的现象。
- optimization_evaluation：优化与评估方向。讲解量化/加速/评测原理、比较优化手段、分析性能与评测现象。
- agent_development：从模型到智能体方向。讲解 ReAct 与框架原理、比较工具或框架、分析智能体行为与部署现象。

## 质量检查

- 主题必须落在对应阶段的课程知识范围内，不跑题到一般编程教程内容。
- 以理论理解为主：概念解释、方法比较、现象分析与引导式追问，不要求设计完整实验。
- 难度标签与实际内容一致；不用“至少多少字”凑质量。
- 不要求输出隐藏思维过程；只保留可核查的结论、代码与必要解释。
- 生成结果必须抽样人工复核，Skill 规则不能替代教师判断。

## 当前边界

- 本 Skill 只定义数据生成规则，不执行代码、不保存密钥、不调用 API。
- 本 Skill 是自建 Skill，用于课程学习伴侣数据生成；与网络下载的 find-skills（Skill 查找工作流）相互独立，不要混用。
