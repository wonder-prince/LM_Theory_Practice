# 教学说明：本文件用于实现本周实验中与该文件对应的可运行功能。
# 阅读时先确认输入与路径，再观察核心处理和输出；修改后应重新运行对应步骤。

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Expected = @{
    "models\google-bert_bert-base-uncased\model.safetensors" = "68D45E234EB4A928074DFD868CEAD0219AB85354CC53D20E772753C6BB9169D3"
    "models\openai-community_gpt2\model.safetensors" = "248DFC3911869EC493C76E65BF2FCF7F615828B0254C12B473182F0F81D3A707"
}

foreach ($RelativePath in $Expected.Keys) {
    $Path = Join-Path $ProjectRoot $RelativePath
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "模型权重不存在：$Path"
    }
    $Actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash
    if ($Actual -ne $Expected[$RelativePath]) {
        throw "SHA-256 不一致：$RelativePath"
    }
    Write-Host "PASS $RelativePath"
}

Write-Host "ALL MODEL HASHES PASSED"

