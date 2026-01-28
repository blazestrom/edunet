from pydub import AudioSegment
import os
from typing import Tuple
from utils.logger import logger

def get_audio_info(file_path: str) -> dict:
    """
    Get audio file metadata
    """
    try:
        audio = AudioSegment.from_file(file_path)
        return {
            "duration_seconds": len(audio) / 1000,
            "channels": audio.channels,
            "sample_rate": audio.frame_rate,
            "sample_width": audio.sample_width,
            "file_size_mb": os.path.getsize(file_path) / (1024 * 1024)
        }
    except Exception as e:
        logger.error(f"Error getting audio info: {e}")
        raise

def convert_to_wav(input_path: str, output_path: str) -> str:
    """
    Convert audio to WAV format for Whisper
    """
    try:
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1)  # Mono
        audio = audio.set_frame_rate(16000)  # 16kHz
        audio.export(output_path, format="wav")
        logger.info(f"Converted audio to WAV: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        raise

def validate_audio_file(file_path: str, max_size_mb: int = 100) -> Tuple[bool, str]:
    """
    Validate audio file
    """
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File too large: {file_size_mb:.2f}MB (max: {max_size_mb}MB)"
    
    ext = os.path.splitext(file_path)[1].lower()
    allowed_formats = [".mp3", ".wav", ".m4a", ".ogg", ".flac"]
    if ext not in allowed_formats:
        return False, f"Unsupported format: {ext}"
    
    return True, "Valid"