param(
    [string]$CodexSkillsDir = "$env:USERPROFILE\.codex\skills",
    [switch]$Pull
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Src = Join-Path $RepoRoot "skills"

if (-not (Test-Path -LiteralPath $Src)) {
    throw "skills directory not found at $Src"
}

# 可选：安装前拉取最新提交。
if ($Pull -and (Test-Path -LiteralPath (Join-Path $RepoRoot ".git"))) {
    git -C $RepoRoot pull --ff-only
}

New-Item -ItemType Directory -Force -Path $CodexSkillsDir | Out-Null
Get-ChildItem -LiteralPath $Src -Directory | ForEach-Object {
    $Target = Join-Path $CodexSkillsDir $_.Name
    if (Test-Path -LiteralPath $Target) {
        Remove-Item -LiteralPath $Target -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $Target -Recurse
    Write-Output "copied $($_.Name)"
}

Write-Output "Done"
