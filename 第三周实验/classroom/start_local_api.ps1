# Step 04：启动 llama-cpp-python 官方 OpenAI 兼容服务器。
# 保持本终端运行；在第二个 VS Code 终端执行 step04_api_client.py。

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

# $PSScriptRoot 是 classroom 目录；向上一级得到项目根目录，再拼出本地 GGUF 路径。
# 使用脚本相对路径后，学生复制整个项目文件夹时不需要修改盘符或用户名。
$ProjectDir = Split-Path -Parent $PSScriptRoot
$ModelPath = Join-Path $ProjectDir "models\Qwen2.5-7B-Instruct-GGUF\qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"
if (-not (Test-Path -LiteralPath $ModelPath)) {
    throw "缺少模型文件：$ModelPath"
}

# 优先使用当前 Conda 会话的 CONDA_PREFIX，但必须确认它确实是 llm-course；
# 嵌套 PowerShell 可能把 CONDA_PREFIX 重设为 Anaconda base，不能只判断变量存在。
# 嵌套 PowerShell 可能丢失 CONDA_PREFIX，此时直接定位 Anaconda 的命名环境，
# 避免提示符仍显示 llm-course、实际却回退到 base Python。
$ActivePython = if ($env:CONDA_PREFIX) { Join-Path $env:CONDA_PREFIX "python.exe" } else { $null }
$ActiveIsCourseEnv = $env:CONDA_PREFIX -and $env:CONDA_PREFIX.EndsWith(
    "\envs\llm-course",
    [System.StringComparison]::OrdinalIgnoreCase
)
if ($ActiveIsCourseEnv -and (Test-Path -LiteralPath $ActivePython)) {
    $PythonExe = Join-Path $env:CONDA_PREFIX "python.exe"
} else {
    $CondaCommand = Get-Command conda -ErrorAction SilentlyContinue
    if ($CondaCommand) {
        $CondaBase = (& conda info --base 2>$null).Trim()
        $NamedPython = Join-Path $CondaBase "envs\llm-course\python.exe"
        if (Test-Path -LiteralPath $NamedPython) {
            $PythonExe = $NamedPython
        }
    }
    if (-not $PythonExe) {
        $PythonExe = (Get-Command python -ErrorAction Stop).Source
    }
}
$ExpectedSuffix = "\envs\llm-course\python.exe"
if (-not $PythonExe.EndsWith($ExpectedSuffix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "当前 python 不是 llm-course：$PythonExe。请先执行 conda activate llm-course。"
}
Write-Host "python: $PythonExe"

Write-Host "正在加载 Qwen2.5-7B-Instruct Q4_K_M……"
Write-Host "服务就绪后访问：http://127.0.0.1:18080/docs"
Write-Host "按 Ctrl+C 停止服务。"

# server_launcher.py 先处理 Windows CUDA DLL，再运行官方 llama_cpp.server。
# 下列参数依次指定：模型文件与 API 别名、Qwen 对话模板、仅限本机访问的地址、
# 服务端口、上下文长度、转移到 GPU 的网络层数、CPU 线程数以及日志详细程度。
& $PythonExe -s (Join-Path $PSScriptRoot "server_launcher.py") `
    --model $ModelPath `
    --model_alias qwen2.5-7b-local `
    --chat_format chatml `
    --host 127.0.0.1 `
    --port 18080 `
    --n_ctx 2048 `
    --n_gpu_layers 16 `
    --n_threads 8 `
    --verbose False

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

