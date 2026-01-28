import requests

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/audio/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("Testing EduNet Audio API")
    print("=" * 50 + "\n")
    
    try:
        test_root()
        test_health()
        print("✓ All basic tests passed!")
        print("\nTo test transcription:")
        print("1. Go to http://localhost:8000/docs")
        print("2. Try POST /api/audio/transcribe-live")
        print("3. Speak into your microphone when prompted")
    except Exception as e:
        print(f"✗ Test failed: {e}")
