# Vaani Voice Assistant Startup Script
# This script starts the Vaani voice assistant

Write-Host "🎙️ Starting Vaani Voice Assistant..." -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ Configuration file (.env) found" -ForegroundColor Green
} else {
    Write-Host "⚠️ Warning: .env file not found. Some features may not work." -ForegroundColor Yellow
}

# Check internet connection
try {
    $connection = Test-Connection -ComputerName google.com -Count 1 -Quiet
    if ($connection) {
        Write-Host "✅ Internet connection: Available" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Internet connection: Offline (Limited features)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Could not check internet connection" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host " Vaani - AI Voice Assistant for Farmers " -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting in 2 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Start Vaani
python -m vaani.core.main
