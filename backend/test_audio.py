import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required packages are installed"""
    try:
        import fastapi
        print("✓ FastAPI installed")
        
        import uvicorn
        print("✓ Uvicorn installed")
        
        import requests
        print("✓ Requests installed")
        
        from dotenv import load_dotenv
        print("✓ Python-dotenv installed")
        
        try:
            import pyaudio
            print("✓ PyAudio installed (microphone support available)")
        except ImportError:
            print("✗ PyAudio not installed (microphone support disabled)")
        
        print("\n✓ All core packages installed successfully!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Missing package: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config.settings import REVERB_API_KEY, REVERB_API_URL
        print("\n✓ Configuration loaded")
        print(f"  API Key: {REVERB_API_KEY[:10]}..." if REVERB_API_KEY else "  API Key: Not set")
        print(f"  API URL: {REVERB_API_URL}")
        return True
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        return False

def test_audio_service():
    """Test audio service initialization"""
    try:
        from services.audio_service import AudioTranscriptionService
        service = AudioTranscriptionService()
        print("\n✓ Audio service initialized successfully")
        service.cleanup()
        return True
    except Exception as e:
        print(f"\n✗ Audio service error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Rev.ai Audio Transcription Setup")
    print("=" * 50)
    
    all_tests_passed = True
    
    all_tests_passed &= test_imports()
    all_tests_passed &= test_config()
    all_tests_passed &= test_audio_service()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✓ All tests passed! Setup is complete.")
        print("\nYou can now start the server with:")
        print("  uvicorn main:app --reload")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 50)
