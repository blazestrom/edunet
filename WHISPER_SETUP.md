# 🔧 Installation Guide - ffmpeg & Whisper Setup

## The Problem
Your backend is returning 500 errors because **ffmpeg is not installed**. Whisper depends on ffmpeg to decode audio files (MP3, M4A, WAV, etc.), but Python's pip cannot install system-level dependencies like ffmpeg.

## Why ffmpeg is Required
- **OpenAI Whisper** transcribes audio files
- Whisper uses ffmpeg to decode audio (MP3, M4A, FLAC, WAV, etc.)
- Without ffmpeg → `FileNotFoundError` or decoding errors
- This is a **system dependency**, not a Python package

## Installation Steps

### ✅ Step 1: Install ffmpeg on Windows

**Option A: Using Chocolatey (Recommended)**
```powershell
# Run PowerShell as Administrator
choco install ffmpeg -y
```

**Option B: Manual Download**
1. Go to: https://ffmpeg.org/download.html
2. Download: Windows build from https://github.com/GyanD/codecs/releases
3. Look for: `ffmpeg-release-full.7z` or `.zip`
4. Extract to: `C:\ffmpeg`
5. The folder should contain: `bin\ffmpeg.exe`
6. Add to PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "User variables" → New
   - Variable name: `Path`
   - Variable value: `C:\ffmpeg\bin`
   - Click OK, close everything

### ✅ Step 2: Verify ffmpeg Installation
```powershell
ffmpeg -version
```
Should show version info (not "command not found")

### ✅ Step 3: Install Python Packages
```bash
# From project root
pip install --upgrade openai-whisper groq fastapi uvicorn python-multipart python-dotenv torch
```

### ✅ Step 4: Test Whisper
```python
python -c "import whisper; print('✅ Whisper imported successfully')"
python -c "whisper --version"
```

### ✅ Step 5: Run Backend
```bash
cd backend
python -m uvicorn app:app --host 127.0.0.1 --port 8080 --reload
```

Or use the batch file:
```bash
double-click start-backend.bat
```

## Troubleshooting

### Error: "ffmpeg not found"
- ffmpeg is not in your PATH
- Restart your terminal after installing
- Verify: `ffmpeg -version` should work

### Error: "No module named 'whisper'"
1. Ensure ffmpeg is installed first
2. Run: `pip install --upgrade openai-whisper`
3. Test: `python -c "import whisper"`

### Error: "FileNotFoundError" during transcription
- ffmpeg is installed but can't find ffmpeg.exe
- Add ffmpeg's `bin` folder to PATH
- Restart terminal and try again

### Transcription is slow
- First run downloads the model (~1.5GB for "base")
- Subsequent runs use cached model
- Use "tiny" model (390MB) for faster results:
  ```python
  AudioTranscriptionService(model_name="tiny")
  ```

### Memory issues during transcription
- "tiny" model: ~390MB
- "base" model: ~1.5GB
- "small" model: ~2.8GB
- Use smallest model that meets accuracy needs

## Configuration

### Backend Environment Variables
Create `.env` in `backend/` folder:
```env
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
TRANSCRIPTION_PROVIDER=whisper
```

### Whisper Model Selection
In `backend/services/audio_service.py`:
```python
# Options: tiny, base, small, medium, large
# tiny = 390MB (faster)
# base = 1.5GB (balanced) 
# large = 3GB (highest accuracy)
_load_global_model(model_name="tiny")
```

## Quick Start

**Windows:**
```bash
# From project root
double-click start-backend.bat
```

**All Platforms:**
```bash
# From project root/backend
python -m uvicorn app:app --host 127.0.0.1 --port 8080 --reload
```

## Testing

**Backend Health:**
```bash
curl http://127.0.0.1:8080/health
```

**Transcribe Audio:**
```bash
curl -X POST http://127.0.0.1:8080/api/process \
  -F "file=@test_audio.m4a"
```

**Frontend:** http://localhost:5174

## Key Points

✅ ffmpeg must be installed at system level (not pip)  
✅ Whisper model loads once at startup (shared globally)  
✅ First transcription download model (~1.5GB), then cached  
✅ Use "tiny" model for development (faster)  
✅ Use "base" or "small" for production (better accuracy)  
✅ Always test `ffmpeg -version` after install  

---

**Still having issues?** Check:
1. `ffmpeg -version` works in terminal
2. `python -c "import whisper"` works
3. Backend logs at http://127.0.0.1:8080/health
4. Frontend accessible at http://localhost:5174
