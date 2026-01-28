@echo off
REM Streamlit Voice Notes App Launcher
REM Runs on port 8501 by default

echo.
echo ================================================
echo   Streamlit Voice Notes Processor
echo ================================================
echo.

REM Check Python 3.12
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.12 not found
    exit /b 1
)
echo ✅ Python 3.12 found

REM Check ffmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ffmpeg not found
    exit /b 1
)
echo ✅ ffmpeg found

REM Install/upgrade Streamlit
echo.
echo Installing Streamlit...
python3 -m pip install --upgrade streamlit -q
echo ✅ Streamlit ready

REM Start Streamlit app
echo.
echo Starting app on http://localhost:8501
echo.

cd /d c:\Users\piyus\OneDrive\Desktop\codeinter\edunet
python3 -m streamlit run app_streamlit.py --logger.level=error

pause
