# Quick Start Script for Creative Media Co-Pilot
# PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creative Media Co-Pilot - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "[1/3] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "      Virtual environment created!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[1/3] Virtual environment exists" -ForegroundColor Green
    Write-Host ""
}

# Install dependencies
Write-Host "[2/3] Installing dependencies..." -ForegroundColor Yellow
& venv\Scripts\python.exe -m pip install --quiet --upgrade pip
& venv\Scripts\python.exe -m pip install --quiet -r requirements.txt
Write-Host "      Dependencies installed!" -ForegroundColor Green
Write-Host ""

# Run the application
Write-Host "[3/3] Running Creative Media Co-Pilot..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& venv\Scripts\python.exe main.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Run complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
