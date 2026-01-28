# PowerShell script to install ffmpeg on Windows
# This script downloads ffmpeg and adds it to PATH

Write-Host "🔧 ffmpeg Installation Script for Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if ffmpeg is already installed
Write-Host ""
Write-Host "Checking if ffmpeg is installed..." -ForegroundColor Yellow
$ffmpeg_test = & {
    try {
        $output = & ffmpeg -version 2>&1
        if ($LASTEXITCODE -eq 0) { 
            Write-Host "✅ ffmpeg is already installed!" -ForegroundColor Green
            return $true
        }
    } catch {
        return $false
    }
}

if ($ffmpeg_test) {
    Write-Host "No action needed. Exiting."
    exit 0
}

Write-Host "❌ ffmpeg not found in PATH" -ForegroundColor Red
Write-Host ""
Write-Host "Two options to install ffmpeg:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Option 1: Download from https://ffmpeg.org/download.html" -ForegroundColor Cyan
Write-Host "  - Windows builds: https://github.com/GyanD/codecs/releases" -ForegroundColor Cyan
Write-Host "  - Download ffmpeg-release-full.7z" -ForegroundColor Cyan
Write-Host "  - Extract to: C:\ffmpeg" -ForegroundColor Cyan
Write-Host "  - Add C:\ffmpeg\bin to your PATH" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 2: Use Chocolatey (if installed)" -ForegroundColor Cyan
Write-Host "  choco install ffmpeg -y" -ForegroundColor Cyan
Write-Host ""
Write-Host "After installing, restart your terminal and run:" -ForegroundColor Yellow
Write-Host "  ffmpeg -version" -ForegroundColor Yellow
Write-Host ""
Write-Host "Then restart the backend server." -ForegroundColor Yellow
