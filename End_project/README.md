# 订单—收款—退款智能对账 Agent

《大模型原理与应用》期末项目任务清单。

当前状态：数据准备、8工具、LangGraph、本地Qwen GPU推理和独立评分已接入，114项测试通过。最新1000秒预算已从头完成val50：整题正确19/50（38%）、字段匹配率50.09%、工具调用成功率66.16%。单订单19/28正确，批量对账0/22。全部原始结果及与前次600秒预算的逐题对照已归档。未执行训练，尚无正式留出集总体正确率。

## 快速开始

**第一次在另一台 Windows 电脑运行，请先看 [Windows 从零复现指南](docs/Windows从零复现指南.md)**：从安装 Python/Git、创建独立环境，到下载固定版本 Qwen 权重、单题/批量运行和结果验收。仓库不包含模型权重、虚拟环境或密钥。

Windows 本地环境配置及本次用例实跑结果见 [Windows运行说明](docs/Windows运行说明.md)。无需模型 API 的完整八工具规则用例入口为 `python -X utf8 scripts/run_local_case.py`。

本机 RTX 4060 的 Qwen3-4B GPU 环境及真实本地模型用例入口见 [Qwen本地测试](docs/Qwen模型下载与本地测试.md)。权重已下载，可直接运行 `scripts/run_local_qwen.py`，支持 `--split val --limit 5` 小批量测试。

2026-11-27 12:58—15:50 已用1000秒单题预算从第1题独立重跑全部50题，见 [最新val50报告与全部轨迹](artifacts/qwen_gpu_val50_1000s_20261127_125739/README.md)。较前次600秒预算新增3题正确，原16题正确结果全部保持；3题此前均因超时判失败，本次均在600秒内完成，因此不能把6个百分点的提高单独归因于预算放宽。工具错误仍为101次交易不可用和32次参数错误，批量任务仍需改进。

此前600秒预算的新版流程评测见 [600秒val50报告](artifacts/qwen_gpu_val50_20261127_completed_081945/README.md)。与2026-11-26旧流程同50题相比，整题正确率由0%升至32%，字段匹配率由25.04%升至47.80%，工具成功率由71.24%降至66.16%。原批次在准备第37题时遇到Windows状态文件替换权限错误；已添加有限重试和 `--resume-from`，保留原36条记录并补齐14题。该历史对照涉及提示、余额计算、提交核验与反馈修正，使用同一未训练基模。

2026-11-26 已完成本地 NF4 4bit 基模的验证集50题：40题返回结构化结果，8题超时，1题输出超限，1题耗尽决策轮数。15题全部金额字段匹配，但交易ID、复核标记或方案覆盖不满足整题要求。模型和后台进程已自动退出。查看 [val50结果摘要与全部轨迹](artifacts/qwen_gpu_val50_20261126_004832/README.md)；环境与实跑记录见 [Windows运行说明](docs/Windows运行说明.md)。

仓库包含已生成的 610 道对账任务及其环境和参考答案。使用 Python 3.13 可直接校验，无需下载 CSV、安装依赖或配置模型 API。

```bash
git clone https://github.com/wonder-prince/LM_Theory_Practice.git
cd LM_Theory_Practice/End_project
python3 scripts/validate_data.py datasets/prepared
```

从 Olist 原始 CSV 重新生成任务并核对文件哈希，见[复跑命令](#复跑命令)。运行 LangGraph Agent 见[环境具备依赖后的运行命令](#环境具备依赖后的运行命令)。

## 1. 项目目标与范围

针对一个订单或一个账期，查询模拟订单、收款和退款，输出已匹配项、差异金额、待复核项，以及可追溯的证据引用。

- 请求 A：单订单核查，例如“订单 O1001 收齐了吗，退款是否正常？”
- 请求 B：账期批量对账，例如“核对指定账期的全部订单，列出差异和无法确认的项目。”
- 数据路线：公开 Olist 订单与支付金额打底，程序构造明确标注来源的模拟支付事件与异常；保持 BRL 原币种，本地执行。
- 覆盖分笔收款、部分退款、多次退款、重复通知、同额异单、缺失凭证和截止时间边界。
- 第一版暂不覆盖手续费、汇率、一笔付款跨多个订单分摊或真实资金操作。
- 金额使用整数分或 Decimal 精确计算，不使用二进制浮点数直接核对金额。

## 2. 正式要求与项目计划

正式要求依据所提供的《大模型原理与应用_大作业》，示例中的较小规模不替代正式验收标准。

| 项目 | 正式要求 | 本项目建议 |
| --- | --- | --- |
| 完成方式 | 每人独立完成 | 单 Agent，明确模型决策边界 |
| 业务工具 | 自编并注册至少 8 种 | 8 种正式业务工具已实现，模型调用待接入 |
| 请求类型 | 至少两种，展示不同工具链 | 单订单核查、账期批量对账 |
| 跨工具链 | 至少一条接续使用 3 种工具的实际结果 | 查询订单、收款、退款后计算并核验 |
| 工具测试 | 每工具至少一个正常输入和一个错误或空结果 | 八工具正常/错误覆盖及关键边界，当前总计54项测试 |
| Agent 演示 | 至少一条正常任务和一条异常任务 | 正常、歧义挂起、重复流水三类 |
| 训练路线 | SFT 或带可验证奖励的 RL | 优先 SFT，RL 可选 |
| SFT 规模 | 建议覆盖至少 150 个任务 | 200 个训练任务、50 个验证任务 |
| 独立留出评测 | 至少 300 条，建议 300～500 条 | 360 条，三类各 120 条 |
| 测试分类 | 基础、跨工具、异常边界各不少于 40 条 | 覆盖每项功能与关键约束 |
| 两组比较 | 相同题目、工具、提示和预算，只切换权重 | 固定环境快照和配置 |
| 正确率 | 工具使用及最终结果正确率均以 80% 为目标 | 据实报告，未达标分析原因 |

任务数不等于动作样本条数：一个任务可能产生多条助手动作监督样本。200/50/360 为本阶段环境任务的目标规模，实际生成数见第 10 节；这些任务和参考答案还不是 SFT 工具轨迹。

## 3. 实施任务清单

### 阶段一：确定规则、框架与模型

- [x] 选定LangGraph，编写1.x依赖声明；未安装、未生成环境锁文件，实际版本待部署验证。
- [x] 明确数据阶段的输入字段、参考输出和错误语义；Agent 输出接口仍待实现。
- [x] 定义应收、成功收款、成功退款、净收和差额口径，区分收款不足与正常退款。
- [x] 定义筛选订单状态、模拟交易/退款状态、截止时间及固定时区假设。
- [x] 定义强关联证据、候选匹配条件与必须挂起的歧义情形；不能仅因同额而强行匹配。
- [x] 明确交易归属及截止规则；仅纳入截止前已生效且已观察的事件，退款必须关联截止前可确认的成功收款。
- [ ] 选择可实际微调和重新部署的开放权重模型，核对许可证、工具调用模板与机器资源。
- [ ] 选择训练和推理环境；先验证真实基座能输出可执行工具调用，再启动大规模数据生成。

验收：规则明确，模型可调用，框架和模型选择有记录。只使用商用 API 无法替代实际模型微调。

### 阶段二：建立模拟数据与独立参考答案

- [x] 定义订单、收款、退款、重复通知、规则版本和参考答案结构；对账草稿接口留待业务工具阶段。
- [x] 保留订单号、支付交易号、原交易引用、事件标识、客户引用、金额、币种、状态及时间字段。
- [x] 明确一笔模拟交易与多条重复事件通知的关系，避免把通知条数当成收款笔数。
- [x] 编写带固定随机种子的混合环境生成器，保留源字段与模拟字段 provenance。
- [x] 预先划分训练、验证、留出测试；隔离源订单、客户、交易与环境实例。场景和模板共享，不宣称参数组合域外隔离。
- [x] 生成单订单与真正多订单批量任务，每个任务都有完整环境快照。
- [x] 用隐藏事实归属和业务规则产生独立参考答案，再由可见证据重算核验。
- [x] 校验跨切分重复、金额和关键边界覆盖，记录策略和种子；模板近重复的局限见第 10 节。

验收：任一任务都能重置并重算参考答案，留出集不参与训练、提示优化或奖励调试。

### 阶段三：实现并测试 8 种正式业务工具

历史初稿曾规划 9 工具（含 `get_reconciliation_rules`、`query_receipts`、`calculate_order_balance`、`validate_match_plan` 和保存草稿）；已由确认的分支流程取代，保存草稿不在本阶段范围。

| 正式工具 | 已实现职责 | 状态 |
| --- | --- | --- |
| `query_orders` | 按订单号或账期筛选任务范围订单，支持真实三订单批量 | 已实现/测试 |
| `search_receipts` | 精确按订单/商户/交易引用、时间和状态筛选，可补查未归属收款 | 已实现/测试 |
| `find_match_candidates` | 返回可见候选、强弱证据及冲突，同额不是强证据 | 已实现/测试 |
| `get_transaction_evidence` | 返回现有事件、原支付引用和具体缺失字段/补证请求 | 已实现/测试 |
| `check_duplicate_events` | 同一交易通知去重、检测冲突，不合并不同交易同额收款 | 已实现/测试 |
| `query_refunds` | 按订单或原支付交易号查询，保留pending | 已实现/测试 |
| `calculate_reconciliation` | 仅计算显式分配交易，区分收款差额、净收和pending退款 | 已实现/测试 |
| `validate_reconciliation` | 整批核验覆盖、归属证据、重复占用、金额和待复核说明 | 已实现/测试 |

- [x] 标准function schema、独立参数校验、统一JSON回执及空结果语义。
- [x] 每工具正常和错误/空结果测试，以及金额、通知、退款、截止边界测试。
- [x] 只读快照，无共享分配状态，隔离每次session。
- [x] 与Agent框架解耦；尚未接入模型，不提供save工具。

验收：八工具独立可用；确定性规则演示不代表Agent模型能力，具体入口见第11节。

### 阶段四：跑通未训练基座 Agent

- [ ] 接入真实基座模型、工具 schema、提示和调用循环。
- [ ] 让模型根据上下文选择工具、填写参数、阅读回执并决定继续、回答或挂起。
- [ ] 设置最大模型决策步数、工具调用预算、重试上限、超时和结束条件。
- [ ] 将参数校验和关键业务约束放在程序中，但保留需要学习的工具决策。
- [ ] 跑通两种请求及至少一条连续依赖三种工具结果的调用链。
- [ ] 演示正常任务、证据不足与工具空结果任务。
- [ ] 将任务输入、消息、工具 schema、调用参数、真实回执、最终输出、版本和耗时记录为本地轨迹。
- [ ] 在开发集统计并分类失败：工具选错、参数错误、忽略回执、重复调用、提前结束等。

验收：可从统一入口复跑成功或失败轨迹，模型确实参与决策，不能将完整正确工具顺序全部写死。

### 阶段五：整理轨迹并执行 SFT

- [ ] 先修复工具和环境错误，再冻结训练及正式对照所用工具与规则版本。
- [ ] 收集正常轨迹、人工纠正轨迹或教师在真实工具环境中执行的轨迹。
- [ ] 独立核验教师或人工轨迹的参数、工具回执和最终结论，剔除错误与虚构结果。
- [ ] 展示至少一例“失败轨迹 → 正确动作 → 实际执行核验 → 训练样本”。
- [ ] 按模型 chat template 转换数据；用户消息和工具回执作上下文，只监督助手调用和回答。
- [ ] 在支持的开放权重模型上使用适当的 LoRA 或 QLoRA 配置执行 SFT。
- [ ] 保存模型标识、数据划分、依赖、种子、训练配置、日志、checkpoint 和适配器权重。
- [ ] 用验证集选 checkpoint，记录选择依据；不使用留出测试结果选模型。
- [ ] 将训练后的模型接回同一框架，实现基座与 SFT 模型配置切换。

验收：完成真实参数训练，并能切换权重复跑同一任务。编排框架本身不替代训练框架。

### 阶段六：正式对照评测

- [ ] 冻结至少 300 条独立留出任务；建议 360 条，基础、跨工具、异常各 120 条。
- [ ] 对两组使用相同工具定义、提示、输入、推理参数和调用预算，只切换权重。
- [ ] 每题每组重置到相同环境快照，防止草稿、占用记录和历史状态污染比较。
- [ ] 使用独立评分器核对交易归属、退款、差额、证据、待复核理由及必要工具行为。
- [ ] 工具评分允许达到同一正确结果的合理路径，不强制唯一调用顺序。
- [ ] 报告两组工具使用与最终结果正确数、正确率，以及百分点差值。
- [ ] 补充错配、漏配、重复占用、歧义正确挂起率和平均调用次数。
- [ ] 保存逐题轨迹、原始回答、参考答案、评分原因和错误类型。
- [ ] 分析提升与退化案例；未达 80% 如实说明，不修改测试集迎合结果。

验收：同一条留出题可分别复跑基座和训练后结果，并核对实际轨迹与判分。

### 阶段七：提交与现场展示

- [ ] 整理项目代码、环境说明、运行入口和配置示例，不提交密钥。
- [ ] 整理实际训练及验证数据、切分清单、训练配置、日志和权重位置。
- [ ] 整理测试题、环境快照、参考答案、评分规则、逐题结果及评测报告。
- [ ] 准备至少一组同题前后问答及正常、异常演示。
- [ ] 制作个人汇报 PPT，说明场景、框架、工具、训练、评测和局限。
- [ ] 在干净环境按运行说明复跑，检查提交材料完整性。

截止时间原文：第 18 周周日（1 月 10 日）24:00 前；以课程通知为准。

## 4. 可选 RL 扩展

正式作业允许 SFT 或可验证奖励 RL，不要求两者都做。本项目优先完成 SFT 全流程。

- [ ] 提供可重置的多步工具环境与独立结果评分器。
- [ ] 设计覆盖归属正确、金额正确、证据完整、歧义正确挂起的奖励。
- [ ] 约束错误匹配、重复占用、虚构证据与调用预算；不按调用数量正向奖励。
- [ ] 核实所选训练实现确实支持多轮工具交互；不能直接把普通文本 GRPO 脚本当作完整 Agent RL。
- [ ] 从基座或 SFT checkpoint 训练，在固定留出集比较 Base/SFT/RL。

## 5. 框架比较与选择记录

资料核对日期：2026-11-24。以下是针对本作业的工程判断，不是两者的通用排名。框架最终由项目作者选择，当前尚未安装或锁定框架。

| 维度 | LangGraph | DeepSeek Harness |
| --- | --- | --- |
| 官方定位 | 面向有状态、长运行 Agent 的底层编排框架与运行时 | 以 Cordis 为内核、能力皆插件的 Agent 运行环境 |
| 当前官方表述 | 支持状态图、持久化、流式输出及人工介入 | 仍处于开发者预览，核心插件和 API 会继续演进 |
| 本项目接入方式 | Python 业务工具、模型节点、工具循环与状态控制 | 编写或配置业务工具插件及模型适配，围绕运行时组织任务 |
| 对账约束 | 可显式组织状态和校验节点，方便混合确定性检查与模型决策 | 可通过插件扩展，但需验证任务隔离和业务约束接入方式 |
| 轨迹 | 自行记录统一 JSONL；LangSmith 可选，不是本项目必需 | 官方提供追加式会话日志和 Trajectory 查看，仍需转换为训练格式 |
| SFT/RL | 在外部训练后接回模型，不直接完成参数训练 | 官网定位是运行环境；不能据此认为内置可用的 SFT/RL 训练流程 |
| 模型切换 | 在自建适配层统一工具调用协议和消息模板 | 模型适配器可替换；仍需实测本地微调模型兼容性 |
| Python 训练衔接 | Agent、数据与训练脚本可围绕 Python 组织 | 官方启动入口基于 Node.js，Code Mode SDK 使用 TypeScript；与 Python 训练链路需要接口衔接 |
| 对课程项目的主要成本 | 需自己定义状态、记录轨迹及批量评测入口 | 需学习插件机制，并验证批量重置、导出与模型接入；要应对预览版接口变化 |
| 更适合的目标 | 可控的领域 Agent、训练对照和可复现评测 | 探索插件化通用 Agent 环境，利用内置交互与轨迹界面 |

建议：优先 LangGraph。原因是本项目核心是业务工具决策、训练数据和固定条件评测；统一 Python 实现更容易把这些部分接起来。DeepSeek Harness 也可实现，但应先验证“业务工具注册、开放权重模型接入、轨迹导出、无交互批量任务及环境重置”五项，再正式采用。

重要区别：DeepSeek Harness 不等于 DeepSeek 模型。选择 LangGraph 同样可以接入兼容模型；用于教师生成的商用模型与最终必须实际微调的学生模型应分开记录。

若使用 LangGraph，建议从“模型决策 → 执行工具 → 回传结果 → 模型再次决策”的简单循环起步，加上预算和校验边界。不要把每类任务的完整工具顺序全部固定，否则难以证明训练改善了模型工具选择。

## 6. 实际目录与后续规划

```text
End_project/
├── README.md
├── scripts/
│   ├── fetch_olist.py     # 无凭证公开下载、固定提交镜像、可追溯本地导入
│   ├── prepare_data.py    # 源数据筛选、客户级切分、模拟环境与任务
│   ├── reference.py       # 隐藏事实账本的独立参考计算
│   ├── validate_data.py   # 仅从可见证据重算，校验切分、版本与产物
│   └── audit_sources.py   # 检查四表哈希/行数/字节数，比较 Kaggle 和镜像记录
├── tests/
│   └── test_data.py       # 独立金额案例、错误输入和全场景检查
└── datasets/
    ├── raw/               # 可选的固定提交镜像，仅保存在本地
    ├── raw_kaggle/        # 按需下载的本地 CSV 缓存；正式数据从这里生成
    ├── source_audit.json  # 两来源的哈希、行数和 CSV 内容比较
    ├── verification_report.json # 本次执行命令与验收汇总
    ├── smoke/             # 先运行的小样本
    └── prepared/          # 完整数据
        ├── agent_visible/ # rules.json、各split/tasks.jsonl及environments/*.json
        ├── hidden/        # 各split的facts、ground_truth、source_assignments JSONL
        └── statistics.json
```

八种框架无关业务工具、schema注册入口及规则CLI已实现，见根目录 `business_tools.py`、`tool_demo.py`、`tests/test_tools.py` 和 `artifacts/tool_demos/`。Agent、模型适配、真实轨迹、训练和正式模型对照仍待实现。小样本与完整数据的实际验证记录见第10节。

## 7. 设计审核与归档

2026-11-25，用户已确认带条件分支、补查回路及待复核出口的对账业务流程。工具设计改为先梳理业务流程，再提取所需能力；此前 9 工具列表是初稿，后续应按已确认流程重新核定。当前流程涉及8项核心能力：查询订单、筛选收款、候选检索、凭证补查、通知查重、退款查询、差额计算、整批复核；现已实现对应八种只读业务工具，框架仍待选、模型仍未接入。

归档目录为 `docs/`：

- `对账Agent业务流程图.png`：可直接插入报告或汇报的流程图图片。
- `对账Agent业务流程图.svg`：对应矢量图，支持放大及后续编辑。
- 两份过程与数据说明文档在该目录归档，记录决策、数据来源、合成策略及实际完成边界。

流程图已归档为 PNG 和 SVG，可直接使用；旧的 macOS 专用一次性导出脚本已清理。

## 8. 下一步待决定

1. 框架选择：LangGraph（建议）或 DeepSeek Harness。
2. 训练资源：本机硬件、是否有 NVIDIA GPU 或远程 GPU，决定学生模型规模和训练方式。
3. 最小原型：先完成单订单任务、真实基座工具循环和三类异常，再扩展批量任务。

## 9. 官方参考资料

- LangGraph 概览：https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph 快速开始：https://docs.langchain.com/oss/python/langgraph/quickstart
- DeepSeek Harness 官方介绍：https://deepseek.com/harness/en/

DeepSeek Harness 的定位、插件、模式和预览状态依据官方页面的检索摘要；本次完整网页抓取超时，未据此承诺具体版本 API、训练支持或未经验证的模型兼容性。实现前需进一步核对所选版本文档。

## 10. 已实现的数据准备路线

### 来源、许可与可追溯性

2026-11-25 重新读取 Olist 原始发布页面： https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce ，页面明确标注 **CC BY-NC-SA 4.0**。原数据由 Olist 提供，包含 2016～2018 年匿名电商订单。数据及本项目的数据衍生物仅用于非商业课程实验，保留 Olist 署名、来源、变更说明，并按相同许可分享；许可原文：https://creativecommons.org/licenses/by-nc-sa/4.0/ 。公开可下载不等于无使用限制。本项目的修改包括金额转整数分、订单筛选、业务标识重建、合成事件及等额干扰单，均非 Olist 原始异常日志。

**本次实际来源是 Kaggle 无凭证公开逐文件 API**，没有读取 Kaggle Token 或其他私有凭证。2026-11-25 四表全部下载成功到 `datasets/raw_kaggle/`，请求模式为 `https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce/{filename}`，响应重定向至 Kaggle 的 Google Cloud Storage ZIP，解压并验证 CSV。该目录是本次 smoke 和 prepared 的唯一源目录，没有用合成数据冒充公开数据。清单保留请求/最终地址、载荷及 CSV SHA-256、字节数与行数；最终签名地址会过期，复跑应使用稳定请求接口。上游数据版本号未独立确定，不能把哈希等同版本号。

仓库中的 `statistics.json` 保留原始 CSV 的哈希和稳定下载地址，下载重定向地址仅保留来源域名和路径。

| 文件 | 实际数据行数（不含表头） | CSV 字节数 |
| --- | ---: | ---: |
| olist_orders_dataset.csv | 99,441 | 17,654,914 |
| olist_order_items_dataset.csv | 112,650 | 15,438,671 |
| olist_order_payments_dataset.csv | 103,886 | 5,777,138 |
| olist_customers_dataset.csv | 99,441 | 9,033,957 |

历史下载记录和镜像清单保存在本地 `datasets/raw/`。

- 仓库：https://github.com/cstuer/olist-ecommerce-analysis
- 固定提交：`21baca68a891817e8370b832273ba62d05a3d719`，目录 `raw/`。
- 镜像下载核验预期 Git blob SHA-1，清单为 `datasets/raw/source_manifest.json`，历史错误保存在 `previous_errors`。
- `datasets/source_audit.json` 对两个来源重新计算四表 SHA-256、行数与字节数。明细、支付、客户三表逐字节一致；orders 字节不同，但解析为 CSV 后忽略行序的记录多重集合完全一致，两侧独有记录均为 0。未把镜像伪记成 Kaggle 下载。
- 仅下载 orders、order_items、order_payments、customers；customers 用于隔离复购客户。未下载评论、地理位置、商品或卖家文件。

### 规则、来源字段与答案隔离

所有金额为 **BRL 整数分**，使用 `Decimal` 从源 CSV 转换。仅选已送达、连接完整、金额为正、明细与支付总额精确相等的订单；不一致的源订单直接筛除并统计，绝不将源差额解释成退款。

原始 `payment_installments` 仅作为源属性保留，**不能解释成实际到账分笔**；Olist 支付行也不被当作有实际到账时间的银行流水。模拟收款以合格源订单总额构造，分笔场景单独拆分且金额守恒。所有支付事件时间、成功状态、退款、通知、交易号、商户引用和异常均是模拟。

`hidden/*/facts.jsonl` 保存每个源订单原记录、明细、支付行、原客户唯一标识，以及逐字段或实体的 `original / derived / synthetic / modified` provenance。等额干扰单的应收可被修改，隐藏侧显式标记 `modified`；来源审计信息不提供给 Agent，避免变更标记提示答案。可见环境只含重新生成的随机业务 ID、订单、源支付方式/分期属性及业务事件；ID 不编码场景、类别、切分或源订单 ID。

时间统一用模拟的固定 `UTC-03:00`。源下单时间没有时区，添加这一偏移是实验假设，不声称已恢复真实时区或夏令时。交易生效时间与通知观察时间都必须 `<= cutoff`；等于截止时点计入，晚 1 秒排除。重复通知按同一 `transaction_id` 去重，冲突通知报错。仅成功退款减少净收，处理中退款不扣款；退款引用原交易，累计成功退款不能超过原成功收款。

先用订单强引用关联，缺失时用唯一商户引用恢复，退款用原交易引用关联。同额只能产生候选，不能确认归属，即使金额候选只有一个也不据此强配；同额歧义输出 `review` 和未分配交易。每笔交易只可分配一次。

参考字段中 `collection_gap_cents = expected - received` 表示少收；`net_cents = received - refunded`；`net_vs_original_cents = expected - net` 单独表示相对原应收的净差。正常成功部分退款可以同时满足“收齐”和“净收减少”，不会被误报为少收。`pending_refund_ids / pending_refund_cents` 单独保留处理中退款，供核查但不从净收扣除。

生成前按 `int(SHA256(seed:customer_unique_id).hexdigest()[:8], 16) % 100` 划分源池（取哈希前 8 个十六进制字符）：0～69 train、70～79 val、80～99 test。随后在池内选择源订单，每个源订单仅用于一个任务，没有跨任务复用的源订单变体；客户也不跨切分。单订单歧义任务可包含候选干扰订单；`period_batch` 是实际 3 个订单的封闭环境，按 `[period_start, period_end)` 查询，再按 cutoff 核验。批量的三单均来自同一切分。

`reference.py` 仅消费隐藏事实账本生成参考答案；`validate_data.py` 仅从可见业务引用与事件重算，再逐题与参考答案比较。验证器能访问隐藏侧用于验收，**未来 Agent 只能由业务工具读取 `agent_visible/`，不得挂载 `hidden/`、原始 CSV、统计文件、生成器或参考代码**。目前目录隔离已完成，模型运行时的文件访问隔离仍需在下一阶段实现。

### 复跑命令

在 macOS、Linux 或 Windows 的 WSL 中，进入 `End_project/`，使用 Python 3.13 运行以下命令。下载、生成和校验只使用 Python 标准库。下载脚本会校验已有 CSV 缓存，生成器要求输出目录为空；多次运行时可更换 `repro_prepared` 目录名。

```bash
python3 scripts/fetch_olist.py --output datasets/raw_kaggle --timeout 60 \
  && python3 scripts/prepare_data.py --raw datasets/raw_kaggle --output datasets/repro_prepared --counts 200 50 360 --seed 20261124 \
  && python3 scripts/validate_data.py datasets/repro_prepared --record \
  && python3 - <<'PY'
import json
from pathlib import Path

published = json.loads(Path('datasets/prepared/statistics.json').read_text(encoding='utf-8'))
rebuilt = json.loads(Path('datasets/repro_prepared/statistics.json').read_text(encoding='utf-8'))
if rebuilt['output_sha256'] != published['output_sha256']:
    raise SystemExit('复现产物与仓库中的文件哈希不一致')
print(f"复现成功，{len(rebuilt['output_sha256'])} 个产物文件哈希一致。")
PY
```

哈希比较覆盖任务、环境、事实和参考答案。`statistics.json` 的运行时间和源下载元数据随运行变化。小样本和镜像审计可按需运行。固定提交镜像的订单表行序与 Kaggle 不同，直接用镜像生成会抽到不同的订单。

```bash
# 生成并校验 48 道小样本任务
python3 scripts/prepare_data.py --raw datasets/raw_kaggle --output datasets/repro_smoke --counts 12 12 24 --seed 20261124
python3 scripts/validate_data.py datasets/repro_smoke --record

# 下载固定提交镜像并比较来源
python3 scripts/fetch_olist.py --mirror --timeout 30
python3 scripts/audit_sources.py --primary datasets/raw_kaggle --mirror datasets/raw --output datasets/source_audit_repro.json
```

如需离线导入，将四个 CSV 放在同一目录，并提供真实下载地址或镜像仓库地址（下例使用上述已核查镜像来源）。该路径记录为 `imported_mirror_or_local`，不会伪称 Kaggle 原始下载：

```bash
python3 scripts/fetch_olist.py --import-dir /path/to/olist_csv --source-url https://github.com/cstuer/olist-ecommerce-analysis --output datasets/raw_imported
python3 scripts/prepare_data.py --raw datasets/raw_imported --output datasets/repro_imported --counts 200 50 360 --seed 20261124
python3 scripts/validate_data.py datasets/repro_imported --record
```

`statistics.json` 保存版本、seed、源清单、筛选原因、池规模、任务统计、代码/测试哈希、所有环境与隐藏答案哈希，以及 `--record` 实际验证结果。代码或产物变化后，旧数据验证会报告 hash 不一致；应使用新输出目录重新生成。

### 本次实际执行与统计（2026-11-25）

环境为 Python 3.13.12，仅使用标准库，生成版本 `olist-sim-v2`，规则版本 `brl-reconciliation-v1`，seed `20261124`。先读取原有全部代码及 README，确认之前只有两表下载完成、无 smoke/prepared，再补齐下载和实现；保留已有源 CSV 与失败记录。未安装 Agent 框架、未使用付费模型。

实际执行的生成命令如下；目录已存在，再生成请使用前述 `repro_*` 新目录。验证命令可直接重复运行。

```bash
python3 -m unittest discover -s tests -v
python3 scripts/prepare_data.py --raw datasets/raw_kaggle --output datasets/smoke --counts 12 12 24 --seed 20261124
python3 scripts/validate_data.py datasets/smoke --record
python3 scripts/prepare_data.py --raw datasets/raw_kaggle --output datasets/prepared --counts 200 50 360 --seed 20261124
python3 scripts/validate_data.py datasets/prepared --record
```

**32 项测试通过**，含 11 场景 × 2 请求模式的子测试，以及整数分、分笔守恒、成功/处理中退款、多次退款累计上限、退款早于收款、退款通知晚到、重复/冲突通知、缺失/冲突引用、同额歧义、截止边界、批量范围排除和错误输入。新增校验会拒绝非法订单金额/币种，以及退款与原收款的商户引用冲突。分期属性 12 仍只生成一笔 normal 收款的专项测试通过，未从 `payment_installments` 生成真实到账分笔。

小样本共 48 个任务（12/12/24），全部验证通过，核验 61 个产物文件。完整数据共 **610 个任务**，全部由可见证据重算并与隐藏参考逐题一致，核验 623 个产物文件；这不代表模型正确率。

| 完整数据切分 | 任务 | 源订单/可见订单 | 单订单任务 | 三订单批量任务 | 事件通知 | 独立交易 | 退款事件 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 200 | 386 | 111 | 89 | 551 | 537 | 105 |
| val | 50 | 96 | 28 | 22 | 137 | 133 | 26 |
| test | 360 | 696 | 200 | 160 | 996 | 972 | 192 |
| 合计 | 610 | 1,178 | 339 | 271 | 1,684 | 1,642 | 323 |

测试集 basic/cross_tool/boundary 各 120 题。11 类场景分别为 normal、split_receipts、partial_refund、pending_refund、recoverable_reference、multiple_refunds、duplicate_event、ambiguous_amount、cutoff、refund_cutoff、refund_observed_cutoff；每个完整切分均覆盖全部场景。批量任务实际处理环境内的 3 个源订单；单订单歧义任务另含候选订单。

源池合格订单 95,904 个：train 67,290、val 9,475、test 19,139。筛除未送达 2,963、金额/字段不一致 573、关联缺失 1，总计与 99,441 个源订单守恒。完整数据跨切分源订单交集为 0、客户交集为 0，业务订单/交易/事件标识无跨任务复用；54 个目标订单正确标为 review。严格筛选仅决定任务底座，不声称这 573 个源订单都是真实业务异常。

完整统计与验证结果在 `datasets/prepared/statistics.json`，小样本在 `datasets/smoke/statistics.json`；来源比较在 `datasets/source_audit.json`，执行汇总在 `datasets/verification_report.json`。两组同 seed 数据有重叠，仅 prepared 用作后续正式切分。没有真实工具轨迹、SFT 样本、训练日志或模型评测结果。

### 局限与下一阶段

这是以真实订单金额打底的受控模拟对账任务，不是现实银行到账、支付渠道退款日志或生产分布。当前仅 11 类场景，跨切分共享场景和请求模板；源订单与客户独立不等于模板、商户或时间域外泛化。批量环境仅包含选中的 3 个订单，账期范围取这些订单的下单区间，不是 Olist 全站某月的完整账单。

原始金额严格一致筛选、仅已送达订单、固定时区和简化成功/处理中状态都会造成选择偏差；未模拟手续费、汇率、争议拒付、复杂退款状态迁移或一笔支付跨单分摊。不要据此宣称生产代表性或真实异常识别效果。`smoke/` 仅作流水线验收，同 seed 下与完整数据可重叠，不能合并成额外独立样本；测试切分不得用于后续提示或模型调优。

已生成的任务与隐藏参考答案 **不是 SFT 轨迹**，确定性验证通过率 **不是 Agent 正确率**。框架已选LangGraph，接入代码与配置见第12节；下一阶段需准备运行依赖和可调用模型，将已实现的八种业务工具接入真实模型或教师调用循环，记录真实调用与回执，独立核验后再转换SFT样本、训练和进行同题权重对照。

## 11. 八工具入口与实际演示（2026-11-25）

`business_tools.py` 仅依赖标准库。`ToolSession(environment, scope)` 支持注入单环境可见快照；`ToolSession.from_visible(visible_root, split, environment_file, scope)` 是文件加载入口，仅允许真实 `agent_visible/train` 或 `val` 下的单个 `environments/*.json`，拒绝绝对路径、上级逃逸和符号链接。scope直接使用可见任务的query对象（single_order或period_batch）。查询订单始终与任务范围求交；收款补查可检索当前环境全部可见收款。所有事件仅在effective_at和observed_at均不晚于固定scope.cutoff时可用。

`tool_schemas()` 返回8个标准 `type:function / function.name / description / parameters` 定义；`register_tools(session)` 返回可直接注册的名称到调用函数映射。`session.call(name, arguments)` 校验参数并统一返回 `{ok,data,error}`；合法空查询返回ok=true和空数组，非法参数、未知交易或截止后交易返回ok=false和具体code/message/details。构造加载失败抛出BusinessError，供宿主拒绝启动。返回对象经过JSON复制，调用方不能修改session快照；没有跨session分配状态。

计算需要显式提供order_id、receipt_ids、refund_ids，成功退款与pending退款都在refund_ids中指定。只计算指定交易，不自动求完整分配；退款必须关联本次指定成功收款，校验时间、引用及累计上限。整批plan格式为 `{orders:[{order_id,receipt_ids,refund_ids,review,review_reason,missing_fields,balance}],unallocated_transaction_ids:[]}`，balance使用计算回执。验证返回 `{valid,errors}`，错误包含可操作的订单/交易标识及纠正说明，不返回完整正确分配。缺失引用只从现有事件报告missing_fields及补证请求，没有另造补凭证表。冲突交易补证返回原始events、conflicting_fields和transaction=null，不擅自选择一条正确凭证；退款订单查询先筛选相关父交易，隔离无关订单冲突；没有可见归属歧义依据的待复核结论会返回UNJUSTIFIED_REVIEW。

运行时不导入生成器、隐藏参考或现成可见环境求解器。此阶段没有模型文件访问沙箱；未来宿主须只暴露注册工具，禁止给模型通用文件读取能力。工具代码不实现调用预算；预算、重试及超时由未来调度器控制。

项目根目录运行：

```bash
python3 -m unittest discover -s tests -v
python3 tool_demo.py --schemas
python3 tool_demo.py --environment environments/f3c95789ace1a9542c5d6baed2eac902.json --scope '{"mode":"single_order","order_id":"cbf27734ac1035250b66402800e03d2c","cutoff":"2018-01-24T21:10:49-03:00"}'
python3 tool_demo.py --environment environments/460f661f900f5390875004e94dae694b.json --scope '{"mode":"period_batch","period_start":"2017-04-25T21:49:31-03:00","period_end":"2017-12-13T14:21:16-03:00","cutoff":"2017-12-23T14:21:15-03:00"}'
```

CLI的 `--output 新路径.json` 可保存实际参数与工具回执，拒绝覆盖已有文件。已实际保存 `artifacts/tool_demos/normal.json`（8次调用，1订单，valid=true）和 `artifacts/tool_demos/ambiguous_batch.json`（20次调用，3订单，2笔未分配，valid=true，相关订单挂起）。两份都标记deterministic_rule_script_demo和model_connected=false，是显式规则脚本演示，不是Agent轨迹或SFT数据。

当前54项测试通过：原32项保持未修改，新增17项工具测试及5项独立复核测试覆盖八工具正常/错误或空结果、精确引用、缺字段、同额弱证据、重复/冲突通知、pending退款、生效及观察截止、累计超退、错误原交易与退款早到、双占用、遗漏订单/交易、金额不符、路径逃逸/链接、session隔离及真实train三订单流程。未读取留出任务或hidden调试工具。未修改生成器和prepared数据；实际重算旧statistics中记录的6个代码文件哈希，mismatches=[]。旧statistics的哈希验证仅检查已记录文件，不会因新增工具与测试文件自动改变；现有导出脚本未造成这些已记录文件的哈希差异。新增文件不会追写旧statistics，也未重新生成数据。最终另运行原命令 `python3 scripts/validate_data.py datasets/prepared` 作既有数据只读验收（未使用--record）：status=passed，200/50/360任务通过，623个产物哈希通过。该原有验收器访问其参考答案仅用于数据一致性验收，未将留出或隐藏内容用于业务工具调试。

主代理额外用确定性脚本逐个加载 train 200、val 50 个可见任务，工具闭环共 250/250 通过方案复核；该检查未使用隐藏答案，也不是模型正确率。汇总记录见 [artifacts/tool_verification.json](artifacts/tool_verification.json)。Markdown归档见 [项目交互与设计过程记录](docs/项目交互与设计过程记录.md) 与 [数据来源与合成说明](docs/数据来源与合成说明.md)。

## 12. LangGraph 接入代码与 API 配置

用户已选择LangGraph，并要求本阶段只写代码与配置，不安装依赖。`requirements.txt` 声明 `langgraph>=1.0,<2.0`，这是待解析的兼容范围，尚无经过安装验证的锁文件。

| 文件 | 职责 |
| --- | --- |
| `agent_runtime.py` | 真正的StateGraph：START → model → tools → model，或结束；8工具schema、真实回执、多工具调用配对、预算与日志 |
| `model_backends.py` | OpenAI兼容Chat Completions HTTP适配；本地脚本后端仅作控制图测试 |
| `agent_cli.py` | train/val单题及最多20题批量入口，每题独立session与backend |
| `.env.example` | 本地API变量示例，只有占位符 |
| `requirements.txt` | 依赖配置，本轮未执行安装 |
| `tests/test_langgraph.py`、`tests/test_agent_review.py` | 图循环、错误、预算、隔离、HTTP与计量回归测试 |

### API 配置

程序只读取环境变量，**不会自动加载 `.env`**。可在项目目录复制 `.env.example` 为 `.env`，仅在本地填写，再在shell中导出：

```bash
cp .env.example .env
# 在 .env 中填入本地密钥后导出变量
set -a
source .env
set +a
```

必填项：`OPENAI_API_KEY`、`OPENAI_BASE_URL`、`MODEL_NAME`。用户已选择DeepSeek官方API，`.env.example`预填 `OPENAI_BASE_URL=https://api.deepseek.com` 和 `MODEL_NAME=deepseek-flash`，密钥仍为占位符。`OPENAI_`只是兼容接口变量名，不代表使用OpenAI服务。若用自有中转或其他模型，应替换地址和模型标识。服务地址填写接口前缀，不要包含 `/chat/completions`；程序会追加该路径。

依据[DeepSeek官方首次调用文档](https://api-docs.deepseek.com/zh-cn/)和[思考模式文档](https://api-docs.deepseek.com/zh-cn/guides/thinking_mode)（2026-11-25核查），官方当前示例模型为`deepseek-flash`。其思考模式默认开启，工具调用的思考模式需要回传`reasoning_content`；本阶段先测普通工具调用基线，适配器仅对`api.deepseek.com`显式发送`thinking: {type: disabled}`，不向其他服务发送该专有参数。后续如比较思考模式，需要先补全对应消息字段及测试。服务需支持标准function tool calls及tool_call_id。密钥文件、虚拟环境和API运行结果已配置git忽略；日志递归脱敏当前密钥，不记录HTTP错误正文。`.env`应只放可信的本地配置。

`SFT_OPENAI_API_KEY`、`SFT_OPENAI_BASE_URL`、`SFT_MODEL_NAME`用于将来的部署切换，入口存在不代表已训练。API默认temperature=0、单请求socket超时30秒、最多重试1次；总预算默认12次模型决策、48次工具尝试、60总步、120秒。响应读取逐块检查总期限。工具报错会作为真实错误回执返回模型；预算截断后未执行的调用也返回对应tool_call_id的停止错误。

### 环境具备依赖后的运行命令

以下命令是待运行入口，本轮未据此宣称图已运行或模型效果已验证。每次使用尚不存在的输出目录：

```bash
# 仅本地脚本控制图烟测，不发送外部API请求
python3 agent_cli.py --backend scripted --split train --limit 1 --output-dir artifacts/langgraph_smoke/run_001

# API配置完成后的单题与小批量基座运行
python3 agent_cli.py --backend api --split train --limit 1 --output-dir artifacts/api_base_001
python3 agent_cli.py --backend api --split val --limit 5 --output-dir artifacts/api_base_val_001

# 后续已有SFT模型部署时，切换端点；目前未执行训练
python3 agent_cli.py --backend api --profile sft --split val --limit 5 --output-dir artifacts/api_sft_val_001
```

输出 `traces.json`（输入、模型动作、工具参数及真实回执、最终文本、停止原因、已报告token）、`summary.json` 和 `evaluation.md`。真实模型任务结束后，独立评分器读取对应train/val参考答案，填写每题 `accuracy`、`cost`、`evaluation`；参考答案不传给模型。`accuracy`是结构化方案整题精确匹配率，缺失提交计失败，另报告字段匹配率与工具成功率；中文叙述、证据引用和复核理由未自动评分。真实模型须返回报告并通过运行时提交核验，才会标记 `completed`。提交可以来自 `validate_reconciliation` 调用或报告末尾的 JSON 块。模型填写订单、交易归属和复核字段，运行时计算 `balance`。未通过时返回具体业务错误，最多触发两轮提交修正，并继续遵守原有决策、步数和超时预算。`submission_rejected` 表示修正后仍未通过，原始回答和核验错误保存在轨迹中。汇总的 `submission_validated_tasks` 记录通过提交核验的题数。脚本烟测排除出模型准确率。

本地 `cost.api_fee=0`，同时记录实际耗时、token和输出速度；硬件/电费未实测，可用 `--compute-price-per-hour` 配置算力估价。API费用需同时提供 `--input-price-per-million` 和 `--output-price-per-million`，币种用 `--cost-currency` 指定；缺失单价会明确标记，usage不全时只报告部分用量估算。费额是用户单价估算，不是服务商账单，不自动处理缓存折扣。`model_connected`只在真实模型返回有效助手消息后为true。缺少API配置时，在读取任务或发送请求前报错退出。

已有JSON/JSONL轨迹可用 `python -X utf8 agent_cli.py --evaluate-trace artifacts/某次运行/traces.json --split train --output-dir artifacts/新的评测目录` 离线评分，不重跑模型。结果及指标解释见 [Windows运行说明](docs/Windows运行说明.md)。

### 本次实际校验

运行 `python3 -m unittest discover -s tests -v`：**80项中62项通过、18项因未安装LangGraph跳过，无失败**。其中原54项业务测试均通过，新增8项无依赖配置/HTTP解析测试通过，包含DeepSeek专有参数仅发送给官方端点的检查。另用127.0.0.1临时服务验证了HTTP适配器响应读取；没有连接外部API。18项图与图内HTTP测试在该次系统Python检查时未执行；后续使用已有.venv的真实运行与完整测试见第13节。

## 13. DeepSeek真实API首次试跑（2026-11-25）

用户配置API并授权试跑后，检查发现项目已有.venv内可用LangGraph 1.2.24，直接使用，不安装任何依赖。模型为deepseek-flash，thinking关闭，默认预算不变；仅使用train任务，未读取隐藏答案或留出集进行调试。

| 试跑 | 模型决策 | 工具调用 | 耗时（秒） | API报告总token | 方案核验 |
| --- | ---: | ---: | ---: | ---: | --- |
| 正常订单首轮 | 8 | 11 | 15.73 | 31,418 | 未通过，BALANCE_MISMATCH |
| 同题补全schema后 | 5 | 7 | 9.23 | 18,149 | valid=true |
| 三订单同额歧义 | 7 | 20 | 17.44 | 38,172 | valid=true |

首轮模型将balance理解为金额小计，只传7个金额字段；工具实际要求复制calculate_reconciliation完整data（含order_id、receipt_ids、refund_ids、pending_refund_ids、evidence_event_ids）。原schema仅声明object，错误提示没有说明漏了哪些非金额字段，模型3次复核未通过，最终如实报告未通过。修复仅补全balance schema字段、必填项及复制完整data说明，未放宽判定、未修改金额计算，也没有做参数训练。已补schema与真实计算回执字段一致的回归断言。首轮与复跑的工具定义不同，属于接口修复验证，不是受控训练前后对照。

复跑正常订单应收和实收均10,697分（BRL106.97），无退款、差额0。歧义任务中1单匹配15,668分，2单待复核；两笔各101,402分的同额收款保留为unallocated，未强行分配，并要求补order_id或merchant_reference。未确认归属的差额不等于已经证实客户欠款。

实际回执目录：`artifacts/api_base_first_20261125_1056/`、`artifacts/api_base_schema_fix_20261125_1100/`、`artifacts/api_base_ambiguity_20261125_1100/`，各含summary.json和traces.jsonl。全套测试在项目.venv执行80项全通过，无跳过。总token为多轮请求累计，包含反复发送的上下文，不代表唯一文本长度；费用未计算。三次试跑涉及两个训练集任务，仅验证实际调用与业务工具自检，不报告独立正确率，也不能据此宣称泛化或训练效果。

### 14:28 安装检查与再次运行

用户授权安装依赖后，在项目`.venv`执行`python -m pip install -r requirements.txt`，全部依赖已满足，LangGraph保持1.2.24；`pip check`返回No broken requirements found。全套80项unittest通过，无跳过。

再次真实运行正常训练任务：deepseek-flash，5次模型决策、9次工具调用，耗时10.54秒，API累计报告19,634 tokens。首次计算误将event_id传入receipt_ids，工具返回TRANSACTION_UNAVAILABLE；模型收到错误后改用transaction_id重算，最终validate_reconciliation返回valid=true、errors=[]。最终应收/实收均BRL106.97，无退款、差额0。此次没有改提示或工具判定来消除错误，保留完整错误与自行纠正轨迹。结果在`artifacts/api_install_check_20261125_1428/summary.json`与`traces.jsonl`。该单题结果仍不是独立正确率。

## 14. 完整轨迹分行保存（2026-11-25）

按用户15:46的修订，后续运行仅输出`traces.json`与`summary.json`。`traces.json`是完整任务数组，用UTF-8、中文原文和2空格缩进保存，JSON结构自动分行；所有历史输入、工具参数、真实回执和最终回答均保留，不省略、不重写。字符串内部换行仍按JSON规范转义，以便程序正常解析。

不再额外生成Markdown、省略版、pretty副本或单行JSONL。`trace_readable.py`属于上一版审阅方案，已从保存入口移除，旧产物保留作为历史记录。新轨迹可用`json.load`读取，返回任务列表。

已有单行JSONL或完整JSON也能离线格式化，无需API配置。输出目录必须尚不存在：

```bash
.venv/bin/python agent_cli.py --render-trace artifacts/api_install_check_20261125_1428/traces.jsonl --output-dir artifacts/formatted_trace_new
```

本地示例位于 `artifacts/formatted_trace_20261125_1546/traces.json`。测试检查离线转换完整保留字段值、只输出两文件，并兼容 JSON/JSONL 读取。
