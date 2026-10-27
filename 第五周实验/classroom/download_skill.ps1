param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,
    [string]$Branch = "main",
    [Parameter(Mandatory = $true)]
    [string]$Path,
    [Parameter(Mandatory = $true)]
    [string]$OutDir
)

# 直接从 GitHub 下载仓库 ZIP，解压后只保留指定的 Skill 目录。
# 例如 find-skills：Repo=vercel-labs/skills, Path=skills/find-skills。
# 只复制文本文件，不执行任何远程代码。
$ErrorActionPreference = "Stop"

$zipUrl = "https://codeload.github.com/$Repo/zip/refs/heads/$Branch"
$zipPath = Join-Path $env:TEMP ("skill_" + [IO.Path]::GetRandomFileName() + ".zip")
$extractDir = Join-Path $env:TEMP ("skill_" + [IO.Path]::GetRandomFileName())

Write-Host "Downloading ZIP: $zipUrl"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -UseBasicParsing
Expand-Archive -LiteralPath $zipPath -DestinationPath $extractDir -Force

$repoName = ($Repo -split '/')[-1]
$src = Join-Path (Join-Path $extractDir "$repoName-$Branch") $Path
if (-not (Test-Path -LiteralPath $src)) {
    Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $extractDir -Recurse -Force -ErrorAction SilentlyContinue
    throw "ZIP 中未找到 $Path，请核对路径。"
}

New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

# 只允许文本类型；图片、二进制、压缩包直接跳过，避免保存无法人工检查的文件。
$allowedExt = @('.md', '.markdown', '.yaml', '.yml', '.txt', '.json', '.py', '.sh', '.ps1', '.js', '.ts', '.tsx', '.css', '.html', '.toml')
$copied = 0
$skipped = 0
Get-ChildItem -LiteralPath $src -Recurse -File | ForEach-Object {
    if ($_.Extension.ToLowerInvariant() -in $allowedExt) {
        $rel = $_.FullName.Substring($src.Length).TrimStart('\')
        $dest = Join-Path $OutDir $rel
        $parent = Split-Path -Parent $dest
        if ($parent -and -not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
        Write-Host "copied: $rel"
        $copied++
    }
    else {
        Write-Host "skipped (non-text): $($_.Name)"
        $skipped++
    }
}

Remove-Item -LiteralPath $zipPath -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $extractDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "done: copied $copied text files, skipped $skipped, saved to $OutDir"
Write-Host "important: only read and inspect these texts, do NOT execute any script or command inside the skill."
