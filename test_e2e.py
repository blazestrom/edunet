#!/usr/bin/env python3
"""
End-to-end test for the voice-to-notes application
Tests: Backend API, Whisper transcription, Streamlit connection
"""
import requests
import json
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"
UPLOADS_DIR = Path("uploads")

def test_backend_health():
    """Test if backend is running"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running on port 8000")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend not responding on port 8000")
        return False

def test_upload_audio():
    """Test audio transcription endpoint"""
    print("\n🔍 Testing audio transcription...")
    
    # Check for test audio files
    audio_files = list(UPLOADS_DIR.glob("*.m4a")) + list(UPLOADS_DIR.glob("*.mp3")) + list(UPLOADS_DIR.glob("*.wav"))
    
    if not audio_files:
        print("⚠️  No test audio files found in uploads/ directory")
        print("   To test, upload an audio file through the Streamlit UI")
        return None
    
    test_file = audio_files[0]
    print(f"   Using test file: {test_file.name} ({test_file.stat().st_size / 1024:.1f} KB)")
    
    try:
        with open(test_file, "rb") as f:
            files = {"file": (test_file.name, f)}
            response = requests.post(
                f"{API_BASE}/api/process",
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            data = response.json()
            transcript = data.get("transcript", "")[:100]
            print(f"✅ Transcription successful!")
            print(f"   Transcript (first 100 chars): {transcript}...")
            if "notes" in data:
                print(f"   Notes generated: {len(data['notes'])} characters")
            return True
        else:
            print(f"❌ Transcription failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return False

def test_streamlit():
    """Test Streamlit app"""
    print("\n🔍 Testing Streamlit UI...")
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit is running on port 8501")
            print("   Access at: http://localhost:8501")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Streamlit not responding on port 8501")
        return False

def main():
    print("=" * 60)
    print("🚀 Voice-to-Notes Application - End-to-End Test")
    print("=" * 60)
    
    backend_ok = test_backend_health()
    streamlit_ok = test_streamlit()
    audio_ok = test_upload_audio()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Backend:    {'✅ OK' if backend_ok else '❌ FAILED'}")
    print(f"   Streamlit:  {'✅ OK' if streamlit_ok else '❌ FAILED'}")
    print(f"   Audio Test: {'✅ OK' if audio_ok else ('⚠️  SKIPPED' if audio_ok is None else '❌ FAILED')}")
    
    if backend_ok and streamlit_ok:
        print("\n🎉 Application is ready!")
        print("   1. Open http://localhost:8501 in your browser")
        print("   2. Upload an audio file (MP3, M4A, WAV, FLAC)")
        print("   3. Select note format and settings")
        print("   4. Click 'Process Audio' to transcribe and generate notes")
    print("=" * 60)

if __name__ == "__main__":
    main()
