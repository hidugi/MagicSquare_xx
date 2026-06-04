# MagicSquare_xx — 가상환경 dev 의존성 설치 (회사 프록시 SSL 우회)
# 사용: .\.venv\Scripts\Activate.ps1 후 .\scripts\install-dev.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Pip = Join-Path $Root ".venv\Scripts\pip.exe"
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    Write-Host "가상환경 없음. 생성 중: python -m venv .venv"
    Set-Location $Root
    python -m venv .venv
}

$trusted = @(
    "--trusted-host", "pypi.org",
    "--trusted-host", "files.pythonhosted.org"
)

Write-Host "pip / setuptools / wheel 업그레이드..."
& $Python -m pip install --upgrade pip setuptools wheel @trusted

Write-Host "pytest 설치 (requirements-dev.txt)..."
& $Pip install -r (Join-Path $Root "requirements-dev.txt") @trusted

Write-Host "검증: pytest --version"
& $Python -m pytest --version
Write-Host "완료."
