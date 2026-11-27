# Windows 从零复现指南

适用于朋友在另一台 Windows 10/11 电脑上复现 `End_project` 的“订单—收款—退款智能对账 Agent”。整理日期：2026-11-27。下面的命令都在 **PowerShell** 中执行；除下载代码一步外，工作目录均为仓库的 `End_project`。

目前可复现：已生成数据的校验、八工具规则演示、LangGraph 调用流程、本地 Qwen 基模推理及运行后独立评分。项目尚未完成 SFT 训练，因此本指南没有训练后权重或训练前后对照步骤。

## 1. 准备电脑和软件

| 路线 | 所需条件 | 可以运行什么 |
| --- | --- | --- |
| 基础验证（先做） | Windows 64 位、Python 3.11 64 位、Git、网络 | 数据校验、业务工具、单元测试和图流程；无需显卡或 API Key |
| 本地模型（可选） | 上述条件，加支持 CUDA 和 BF16 的 NVIDIA 显卡及驱动 | Qwen3-4B 的 NF4 4bit 推理，不需要模型 API |
| API 模型（可选） | 基础环境，加支持工具调用的兼容 API 及自己的 Key | 通过云端模型运行 Agent，无需本地 GPU |

本地模型已在 RTX 4060 Laptop 8GB 上运行过。建议使用同级或更高配置、16GB 以上内存，并为模型、PyTorch 和缓存预留至少 25GB 磁盘空间；这是准备建议，不是所有设备都实测通过。当前 CUDA 11.8 / PyTorch 2.5.0 组合面向已验证设备，较新显卡可能需要另选兼容的 PyTorch/CUDA 版本。

先安装 [Git for Windows](https://git-scm.com/download/win) 和 [Python 3.11](https://www.python.org/downloads/windows/)，保留 Python Launcher。安装后重新打开 PowerShell，确认：

```powershell
git --version
py -3.11 --version
py -3.11 -c "import struct; print(struct.calcsize('P') * 8)"
```

后两项应分别显示 `Python 3.11.x` 和 `64`。没有 `py`、但已有 Python 3.11 的电脑，可将后文的 `py -3.11` 换为该解释器的完整路径；先核对版本，避免默认 `python` 指向其他环境。

## 2. 下载仓库

示例放在当前用户目录下，不需要创建与作者相同的 D 盘路径：

```powershell
Set-Location $env:USERPROFILE
git clone https://github.com/wonder-prince/LM_Theory_Practice.git
Set-Location .\LM_Theory_Practice\End_project
git rev-parse HEAD
```

记下最后输出的提交号，便于交流复现结果。如果已经克隆过仓库，进入现有目录即可，不要在同一位置重复克隆。

仓库已经包含 `datasets/prepared` 的 610 个任务、环境快照和参考答案（train 200、val 50、test 360），基础运行无需下载 Olist 原始 CSV，也无需 Kaggle 账号。支付/退款事件及异常包含程序合成内容，来源见[数据说明](数据来源与合成说明.md)。

**仓库不包含模型权重、虚拟环境和个人密钥。** 旧文档中“模型已下载”指作者电脑；新电脑请执行第 6 节。

## 3. 创建基础环境

直接调用虚拟环境里的 Python，无需激活环境，也无需修改 PowerShell 执行策略：

```powershell
py -3.11 -m venv .venv
& '.\.venv\Scripts\python.exe' -X utf8 -m pip install --upgrade pip
& '.\.venv\Scripts\python.exe' -X utf8 -m pip install -r requirements.lock.txt --progress-bar off
& '.\.venv\Scripts\python.exe' -X utf8 -m pip check
```

每条命令成功后再执行下一条；`pip check` 应显示 `No broken requirements found.`。`requirements.lock.txt` 是作者基础环境的版本快照，不包含 GPU 推理依赖。若提示某个固定版本不存在，先确认正在使用 Python 3.11、软件源能访问该版本；确实无法取得时，可改装 `requirements.txt` 验证功能，但这会重新解析版本，不能再称为相同依赖环境。

`-X utf8` 请保留，后续代码会读取中文 JSON 和说明文件。不要复制作者的 `.venv` 目录到另一台电脑。

## 4. 验证数据和代码

```powershell
& '.\.venv\Scripts\python.exe' -X utf8 scripts/validate_data.py datasets/prepared
& '.\.venv\Scripts\python.exe' -X utf8 scripts/validate_data.py datasets/smoke
& '.\.venv\Scripts\python.exe' -X utf8 -m unittest discover -s tests -v
```

两套数据校验应成功，单元测试末尾应为 `OK`。具体测试数量以当前提交为准。数据校验包含静态完整性检查，不会让模型对留出测试题作答。

## 5. 先跑通不需要模型的演示

```powershell
# 第一条训练任务：单订单
& '.\.venv\Scripts\python.exe' -X utf8 scripts/run_local_case.py

# 三订单批量对账
& '.\.venv\Scripts\python.exe' -X utf8 scripts/run_local_case.py --task-id 004498f4b987f7c1cc9c26a813678d7a

# 单独检查 LangGraph 的模型节点/工具节点循环
$smokeOutput = 'artifacts/windows_smoke_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff')
& '.\.venv\Scripts\python.exe' -X utf8 agent_cli.py --backend scripted --split train --limit 1 --output-dir $smokeOutput
```

前两条会自动创建 `artifacts/local_case_时间戳/`，打印路径，并写入 `summary.json` 和 `traces.json`。应看到 8 种不同工具、`validation.valid=true`、`errors=[]`；单订单有 8 次调用，三订单有 16 次调用。

单订单应收/实收均为 10697 BRL 分（106.97 BRL），退款为 0。三订单应收/实收分别为 9643、15995、16302 分，第一单成功退款 3214 分、净收 6429 分，三单收款差额均为 0。

这些是确定性业务工具自检。`scripted` 只检查图流程，不执行完整对账；它们均不代表真实模型能力。做到这里，没有 NVIDIA 显卡的朋友也已完成基础复现。

## 6. 配置本地 Qwen GPU 环境（需要 NVIDIA 显卡）

### 6.1 安装独立依赖

先在 PowerShell 运行 `nvidia-smi`。能显示显卡和驱动后，再创建一个独立环境：

```powershell
nvidia-smi
py -3.11 -m venv .venv-gpu
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip install --upgrade pip
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cu118 --progress-bar off
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip install -r requirements.lock.txt --progress-bar off
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip install -r requirements-gpu.txt -c requirements.lock.txt --progress-bar off
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip check
```

这里使用干净环境，不继承作者电脑上的 Conda 包。主要版本为 torch 2.5.0+cu118、Transformers 4.55.4、Accelerate 1.10.1、bitsandbytes 0.47.0、NumPy 1.24.4；其余 GPU 间接依赖尚未完全锁定。

PyTorch CUDA wheel 的官方安装入口见 [PyTorch 历史版本](https://pytorch.org/get-started/previous-versions/#v250)。该 wheel 带运行所需的 CUDA 库，电脑仍需兼容的 NVIDIA 驱动；`nvidia-smi` 中显示的 CUDA 数字不必恰好等于 11.8。

检查实际使用的是 CUDA wheel，并验证 BF16 运算：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -c "import torch; print('torch:', torch.__version__, 'runtime:', torch.version.cuda); print('CUDA:', torch.cuda.is_available()); assert torch.cuda.is_available(), 'CUDA unavailable'; print('GPU:', torch.cuda.get_device_name(0)); print('BF16:', torch.cuda.is_bf16_supported()); assert torch.cuda.is_bf16_supported(), 'BF16 unavailable'; x=torch.ones((256,256),device='cuda',dtype=torch.bfloat16); print('matmul:', (x @ x)[0,0].item())"
```

应看到 `2.5.0+cu118`、`CUDA: True`、`BF16: True`、显卡名称和 `matmul: 256.0`。当前本地推理入口强制使用 CUDA/BF16，不支持直接切换为 CPU、AMD 或 Intel 显卡。

### 6.2 下载模型

使用官方 [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)。以下固定到作者下载清单记录的 Hugging Face 提交 `cdbee75f17c01a7cc42f958dc650907174af0554`，避免以后默认分支变化。下载方法见 [Hugging Face 官方说明](https://huggingface.co/docs/huggingface_hub/v0.34.4/guides/download)。

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Qwen/Qwen3-4B-Instruct-2507', revision='cdbee75f17c01a7cc42f958dc650907174af0554', local_dir='models/Qwen3-4B-Instruct-2507')"
```

原始权重约 8GB（十进制），下载时间取决于网络；4bit 是运行时量化方式，仍需先下载完整原始权重。下载中断后可重新执行同一命令。若本机无法访问 Hugging Face，可在能访问的电脑完成下载，再复制整个模型目录；只复制权重分片会缺少配置和 tokenizer。

下载后，`models/Qwen3-4B-Instruct-2507/` 至少应有 `config.json`、`generation_config.json`、`tokenizer.json`、`tokenizer_config.json`、`vocab.json`、`merges.txt`、`model.safetensors.index.json` 和 3 个权重分片。可对照作者本地下载记录验证三个权重文件，读取全部文件可能需要几分钟：

```powershell
$expectedHashes = @{
    'model-00001-of-00003.safetensors' = '75311d91bb08cf0b882913da464a1e722a31fb44db35208663487efb7a3d8ed6'
    'model-00002-of-00003.safetensors' = '0b48adbb1f60e901153d91907ba11ce63bd4b8b584482e730f48808d055dfba1'
    'model-00003-of-00003.safetensors' = '7dd39ccca5e4de123c74c14af44c9bf2eb75df33b4614382af0134528e060d5d'
}
foreach ($file in $expectedHashes.Keys) {
    $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path 'models/Qwen3-4B-Instruct-2507' $file) -ErrorAction Stop).Hash
    if ($actualHash -ne $expectedHashes[$file]) { throw "权重校验失败：$file" }
    Write-Host "SHA256 OK: $file"
}
```

### 6.3 从一题开始，再跑批量

插上电源，关闭占用显存较多的程序。以下命令会真实加载模型、由模型选择工具，并在生成后评分；无需设置 API Key：

```powershell
# 单订单：默认第一条训练任务
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py

# 三订单批量任务
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --task-id 004498f4b987f7c1cc9c26a813678d7a

# 先做5题验证，再决定是否跑完整50题；每条命令各加载一次模型
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 5
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 50 --timeout 600 --max-decisions 12 --max-context 16384 --max-new-tokens 2048
```

默认输出到新建的 `artifacts/local_qwen_时间戳/`，每题结束保存一次。单题默认最多 600 秒，不含模型加载；作者历史 50 题约耗时 4 小时 19 分，仅供安排时间。运行结束后会释放模型并退出进程。中途需要停止时按 `Ctrl+C`，保留已写入结果。再次运行默认新建批次；如需补齐未处理的题目，可增加 `--resume-from`，同时保留原批次的切分、任务数量、预算和模型目录，并指定一个不存在的新输出目录：

```powershell
& '.\.venv-gpu\Scripts\python.exe' -X utf8 scripts/run_local_qwen.py --split val --limit 50 --timeout 600 --max-decisions 12 --max-context 16384 --max-new-tokens 2048 --resume-from artifacts/qwen_val50_interrupted --output-dir artifacts/qwen_val50_continued
```

将上面的原结果目录换成自己的路径。续跑会校验已有轨迹前缀及相关配置，将已保存题目原样载入新目录，只执行剩余任务；已保存的超时或错误题也保留原结果。Windows 上 JSON 临时文件写入/替换遇到 `PermissionError` 时，入口最多进行10次有限退避重试；持续的权限错误仍会明确报告。

主要结果文件：

| 文件 | 看什么 |
| --- | --- |
| `run_status.json` | 加载/运行/结束状态、已处理数量、模型清理情况 |
| `run_manifest.json` | 本次任务 ID 和实际命令参数 |
| `summary.json` | 总体及逐题指标、停止原因、耗时和版本信息 |
| `evaluation.md` | 独立评分、字段差异、工具成功率 |
| `traces.md` / `traces.json` | 模型消息、工具参数、真实回执及最终回答 |

`phase=finished` 表示批次处理结束。当前真实模型入口的 `completed` 要求返回报告并通过运行时方案核验，但仍需通过 `accuracy` 和 `evaluation` 检查是否与独立参考答案一致；历史轨迹的 `completed` 只要求返回文本。退出码 1 可能是部分题超时、耗尽预算或提交核验失败（`submission_rejected`），先查结果文件，不要直接判断环境安装失败。`pip check` 及第 4 节的测试也可用 `.venv-gpu` 的 Python 再执行，以检查该环境。

## 7. 没有 GPU 时用 API 运行（可选）

完成第 3～5 节后，准备一个支持工具调用的 OpenAI 兼容服务。在当前 PowerShell 设置自己的配置；将示例地址和模型名替换为服务商提供的实际值：

```powershell
$env:OPENAI_BASE_URL = 'https://your-provider.example/v1'
$env:MODEL_NAME = 'your-tool-calling-model'
$apiSecret = Read-Host '输入你自己的 API Key' -AsSecureString
$env:OPENAI_API_KEY = ([System.Net.NetworkCredential]::new('', $apiSecret)).Password
$apiOutput = 'artifacts/api_windows_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff')
& '.\.venv\Scripts\python.exe' -X utf8 agent_cli.py --backend api --split train --limit 1 --timeout 600 --output-dir $apiOutput
Remove-Item Env:OPENAI_API_KEY
Remove-Variable apiSecret
```

项目不会自动加载 `.env`；只创建该文件不足以配置本入口。API 路线会向所选服务发送任务和工具回执，并可能产生服务费用，模型也与本地 Qwen 不同。API 结果可用于验证流程，不能当作本地 Qwen 的复现结果。

## 8. 常见问题

| 现象 | 处理方法 |
| --- | --- |
| 提示找不到脚本、依赖文件或数据 | 确认当前位置为 `LM_Theory_Practice\End_project`，运行 `Get-Location` 检查 |
| `Activate.ps1` 被执行策略拦截 | 使用上面的 `& '.\.venv\Scripts\python.exe' ...`，无需激活 |
| 中文读取报 GBK/Unicode 错误 | 保留 Python 命令中的 `-X utf8` |
| `No module named langgraph` 等 | 核对正在调用哪一个虚拟环境，在同一个环境重新执行安装及 `pip check` |
| `CUDA: False` 或 CPU 版 torch | 检查 `nvidia-smi`、解释器路径及 torch 版本；在 `.venv-gpu` 中重新安装指定 CUDA wheel |
| `BF16: False` | 该显卡不能使用当前本地入口；使用基础验证或 API 路线 |
| 模型配置/tokenizer/分片缺失 | 确认第 6.2 节下载完成、目录没有多套一层；自定义位置时传 `--model-dir '完整路径'` |
| `CUDA_OUT_OF_MEMORY` | 关闭其他显存占用程序；可尝试 `--max-context 8192 --max-new-tokens 1024`，并记录参数变更；更小预算可能引发上下文/输出超限 |
| `DEADLINE_EXCEEDED` / `LOCAL_OUTPUT_LIMIT` / 上下文超限 | 查轨迹，必要时调整 `--timeout` / `--max-new-tokens` / `--max-context`；调整后的结果属于另一组配置 |
| 输出目录已存在 | 改用新的 `--output-dir`，或让本地用例/Qwen 脚本自动生成时间戳目录 |
| 首次加载和逐轮生成很慢 | 先运行单题检查进度；Windows 上该组合确有较高耗时，历史诊断见 [Windows运行记录](Windows运行说明.md) |

## 9. 对照结果与记录复现信息

历史 [2026-11-26 验证集50题报告](../artifacts/qwen_gpu_val50_20261126_004832/README.md) 的整题精确匹配为 0/50、字段匹配率 25.04%、工具成功率 71.24%。这是未训练基模在当时提示词和运行时下的实际表现，不是复现成功应达到的目标；随后提交 `5519521` 调整了结构化方案核验逻辑，当前代码不能与该历史批次直接视为相同配置。

如果要研究历史批次，请在另一个克隆目录切换到包含归档的 `3f497bd`，再按相同模型、依赖和预算运行；不同硬件仍可能造成耗时和结果差异。当前正常使用请保留最新提交。正式留出集 `test` 不在现有模型入口开放范围内，指南仅用 train/val。

分享结果时，附上 Git 提交号、Python/依赖版本、显卡/驱动、运行命令及上述结果目录。可在运行所在环境导出信息，例如 GPU 路线：

```powershell
git rev-parse HEAD
& '.\.venv-gpu\Scripts\python.exe' --version
& '.\.venv-gpu\Scripts\python.exe' -X utf8 -m pip freeze | Out-File -Encoding utf8 artifacts/windows-gpu-environment.txt
nvidia-smi
```

基础或 API 路线可换成 `.venv`。请保留原始轨迹和失败原因，比较时说明所用代码和参数；模型答错也可以是一次有效的复现实验记录。
