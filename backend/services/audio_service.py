import os
import logging
import subprocess

logger = logging.getLogger(__name__)

# Try to import whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Whisper not available: {e}")
    WHISPER_AVAILABLE = False

# Try to import torch (optional - for CUDA detection)
# Safe import with fallback - torch may not be available in all environments
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None  # Explicitly set to None if not available

# Global model instance - loaded once at module level for efficiency
_global_model = None
_model_load_error = None


def _check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True, timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _load_global_model(model_name="tiny"):
    """
    Load Whisper model once at startup.
    Uses "tiny" model by default (minimal memory: ~390MB).
    """
    global _global_model, _model_load_error
    
    if _global_model is not None:
        return _global_model
    
    if not WHISPER_AVAILABLE:
        _model_load_error = "Whisper module not installed. Install with: pip install openai-whisper"
        logger.error(_model_load_error)
        return None
    
    if not _check_ffmpeg():
        _model_load_error = "ffmpeg not found. Whisper requires ffmpeg. Install: https://ffmpeg.org/download.html"
        logger.error(_model_load_error)
        return None
    
    try:
        # Detect CUDA if torch available
        device = "cpu"  # Default to CPU
        if TORCH_AVAILABLE and torch is not None:
            try:
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except:
                device = "cpu"
        
        logger.info(f"Loading Whisper model '{model_name}' on device: {device}")
        _global_model = whisper.load_model(model_name, device=device)
        logger.info(f"✅ Whisper model loaded successfully on {device}")
        return _global_model
    except Exception as e:
        _model_load_error = str(e)
        logger.exception(f"Failed to load Whisper model: {e}")
        return None


class AudioTranscriptionService:
    """
    Audio transcription service using OpenAI Whisper.
    Models: tiny (minimal), base (balanced), small/medium/large (higher accuracy)
    
    Uses global model instance loaded once to avoid memory spikes.
    """

    def __init__(self, model_name="tiny"):
        """
        Initialize Whisper service.
        
        Args:
            model_name: One of "tiny", "base", "small", "medium", "large"
                       Default: "tiny" (390MB) for faster startup
        """
        self.model_name = model_name
        self.model = _load_global_model(model_name)
        if self.model is None and _model_load_error:
            raise RuntimeError(_model_load_error)

    def transcribe_file(self, file_path: str) -> str:
        """
        Transcribe an audio file using Whisper.
        
        Args:
            file_path: Path to the audio file (mp3, wav, m4a, flac, etc.)
            
        Returns:
            Transcribed text (or error message if transcription fails)
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
            RuntimeError: If Whisper model not available
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        if not self.model:
            raise RuntimeError("Whisper model failed to load. Check logs for details.")

        try:
            logger.info(f"Transcribing: {file_path}")
            result = self.model.transcribe(file_path, language="en")
            transcript = result["text"].strip()
            logger.info(f"✅ Transcription complete. Length: {len(transcript)} chars")
            return transcript
        except Exception as e:
            logger.exception(f"Transcription failed for {file_path}")
            raise RuntimeError(f"Transcription failed: {str(e)}")
