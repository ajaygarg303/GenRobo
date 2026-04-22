# Run API with reload scoped to ./app only (avoids endless reloads from .venv / OneDrive).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not $env:DATABASE_URL) {
    $env:DATABASE_URL = "sqlite+aiosqlite:///./data/app.db"
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Create a venv first: python -m venv .venv && .\.venv\Scripts\Activate.ps1 && pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

& .\.venv\Scripts\python.exe -m uvicorn app.main:app `
    --reload `
    --reload-dir app `
    --reload-exclude ".venv" `
    --reload-exclude "**/.venv/**" `
    --reload-exclude "data/**" `
    --host 127.0.0.1 `
    --port 8000
