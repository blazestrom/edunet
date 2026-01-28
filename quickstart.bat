@echo off
REM Quick Start Script for Lecture Voice-to-Notes Generator (Windows)
REM Run this script to set up and start the application

cls
echo 🎓 Lecture Voice-to-Notes Generator - Quick Start
echo ==================================================
echo.

REM Check Python installation
echo ✓ Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo ✓ Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Check for .env file
echo.
echo ✓ Checking environment configuration...
if not exist .env (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env and add your OPENAI_API_KEY
    echo    You can get one at: https://platform.openai.com/account/api-keys
    echo.
    pause
)

REM Create output directories
echo.
echo ✓ Creating output directories...
if not exist uploads mkdir uploads
if not exist output mkdir output

REM Start the server
echo.
echo ✓ Starting server...
echo ==================================================
echo.
echo 🚀 Server is running!
echo.
echo Access the application at:
echo   • Web Interface: http://localhost:8000/test
echo   • API Docs: http://localhost:8000/docs
echo   • ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.
echo ==================================================
echo.

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
