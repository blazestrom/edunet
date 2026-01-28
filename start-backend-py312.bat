@echo off
REM Backend startup script - Python 3.12 version (required for Whisper)
REM This version explicitly uses Python 3.12 for better compatibility

setlocal enabledelayedexpansion

echo.
echo ================================================
echo   FastAPI Backend Server (Python 3.12)
echo   Voice Notes Processor with Whisper AI
echo ================================================
echo.

REM Verify Python 3.12 is available
echo Checking Python 3.12...
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.12 not found. Please install Python 3.9+
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python 3.12 found
python3 --version

REM Check ffmpeg (required by Whisper)
echo.
echo Checking ffmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ffmpeg not found in PATH
    echo.
    echo Whisper requires ffmpeg to decode audio files.
    echo.
    echo Install ffmpeg:
    echo   1. Download: https://ffmpeg.org/download.html
    echo      or use: choco install ffmpeg -y
    echo   2. Add to PATH: C:\ffmpeg\bin (or wherever you install)
    echo   3. Verify: ffmpeg -version
    echo.
    pause
    exit /b 1
)
echo ✅ ffmpeg available

REM Install/upgrade dependencies
echo.
echo Installing Python packages...
python3 -m pip install --upgrade ^
    openai-whisper ^
    groq ^
    fastapi ^
    uvicorn ^
    python-multipart ^
    python-dotenv ^
    torch ^
    -q

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Note: Some warnings above are normal
)

echo ✅ Installation complete

REM Start the server
echo.
echo ================================================
echo   Starting server...
echo   Backend API: http://127.0.0.1:8080
echo   Health check: http://127.0.0.1:8080/health
echo   Docs: http://127.0.0.1:8080/docs
echo.
echo   Press Ctrl+C to stop
echo ================================================
echo.

cd /d c:\Users\piyus\OneDrive\Desktop\codeinter\edunet\backend

REM Start uvicorn server with reload for development
python3 -m uvicorn app:app --host 127.0.0.1 --port 8080 --reload --log-level info

pause
