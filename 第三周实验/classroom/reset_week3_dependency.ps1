# 第三周依赖重置工具。
#
# 作用：只卸载第三周新增的 llama-cpp-python 核心包，用于重新测试联网安装流程。
# 本脚本不会删除 llm-course Conda 环境，也不会删除模型文件。FastAPI、Uvicorn
# 等附加依赖予以保留，因为后续实验仍可能继续使用。

# 加上 -Preview 时只检查目标环境，不执行卸载，适合学生先确认脚本会操作哪个 Python。
param(
    [switch]$Preview
)

# 任意 PowerShell 命令报错时立即停止；同时统一 Python 的终端编码为 UTF-8。
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

# 从 CONDA_PREFIX 直接定位当前环境的 python.exe，不依赖 PATH 中多个 Python 的排序。
# 这项保护可以避免误卸载 Anaconda base 或系统 Python 中的包。
if (-not $env:CONDA_PREFIX) {
    throw "No Conda environment is active. Run: conda activate llm-course"
}

$PythonExe = Join-Path $env:CONDA_PREFIX "python.exe"
if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "python.exe was not found in the active environment: $PythonExe"
}

# 进一步核对路径末尾，只有明确处于 llm-course 环境时才允许继续。
$ExpectedSuffix = "\envs\llm-course\python.exe"
if (-not $PythonExe.EndsWith($ExpectedSuffix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "The active environment is not llm-course: $PythonExe"
}

Write-Host "target python: $PythonExe"
Write-Host "package to remove: llama-cpp-python"

if ($Preview) {
    Write-Host "PREVIEW PASS: no package was removed."
    exit 0
}

# `[server]` 是安装附加依赖的写法，真正需要卸载的核心发行包仍叫 llama-cpp-python。
& $PythonExe -s -m pip uninstall -y llama-cpp-python
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

# 卸载完成后查询 llama_cpp 模块；找不到该模块才说明重置真正成功。
& $PythonExe -s -c "import importlib.util; removed = importlib.util.find_spec('llama_cpp') is None; print('llama_cpp removed:', removed); raise SystemExit(0 if removed else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "llama_cpp is still importable; the reset check failed."
}

Write-Host "RESET PASS: the Week 3 core dependency was removed."
Write-Host "Re-run the install command with --no-cache-dir to test a real network download."
