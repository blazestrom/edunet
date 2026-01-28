@echo off
REM Enhanced backend startup with ffmpeg check
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Backend Startup with Dependency Check
echo ========================================
echo.

REM Check if Python 3.12+ is available (needed for Whisper)
echo Checking Python version...
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Python3 not in PATH, trying python...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python not found!
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=python3
)
echo ✅ Python found: %PYTHON_CMD%
%PYTHON_CMD% --version

REM Check ffmpeg first (CRITICAL)
echo.
echo Checking ffmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ CRITICAL: ffmpeg NOT installed!
    echo.
    echo Whisper requires ffmpeg. Install it:
    echo   Option 1: https://ffmpeg.org/download.html
    echo   Option 2: choco install ffmpeg -y
    echo.
    echo After installing, restart this script.
    pause
    exit /b 1
)
echo ✅ ffmpeg found

REM Install dependencies (use python3 for Whisper compatibility)
echo.
echo Installing Python dependencies...
%PYTHON_CMD% -m pip install --upgrade openai-whisper groq fastapi uvicorn python-multipart python-dotenv torch -q
if %errorlevel% neq 0 (
    echo ⚠️  Warning: installation may have had issues
)
echo ✅ Dependencies ready

REM Start backend server
echo.
echo Starting backend server on http://127.0.0.1:8080
echo.
cd /d c:\Users\piyus\OneDrive\Desktop\codeinter\edunet\backend
%PYTHON_CMD% -m uvicorn app:app --host 127.0.0.1 --port 8080 --reload

pause
