import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Whisper Settings
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
    
    # LLM Settings
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Audio Settings
    SAMPLE_RATE = 16000
    CHUNK_LENGTH_MS = 30000  # 30 seconds
    
    # File Upload
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100 MB
    ALLOWED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".ogg", ".flac"]
    
    # Paths
    UPLOAD_DIR = "uploads"
    OUTPUT_DIR = "outputs"
    PROMPTS_DIR = "prompts"
    
    # Chunking
    MAX_CHUNK_TOKENS = 4000
    
config = Config()