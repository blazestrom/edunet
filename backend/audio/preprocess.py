from pydub import AudioSegment
from pydub.effects import normalize
from typing import List
import os
from config import config
from utils.logger import logger

def normalize_audio(audio: AudioSegment) -> AudioSegment:
    """
    Normalize audio levels
    """
    return normalize(audio)

def split_audio(audio: AudioSegment, chunk_length_ms: int = 30000) -> List[AudioSegment]:
    """
    Split audio into chunks
    """
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunks.append(chunk)
    logger.info(f"Split audio into {len(chunks)} chunks")
    return chunks

def preprocess_audio(input_path: str, output_path: str) -> str:
    """
    Preprocess audio: normalize, convert to mono, set sample rate
    """
    try:
        logger.info(f"Preprocessing audio: {input_path}")
        
        # Load audio
        audio = AudioSegment.from_file(input_path)
        
        # Normalize
        audio = normalize_audio(audio)
        
        # Convert to mono
        audio = audio.set_channels(1)
        
        # Set sample rate to 16kHz (optimal for Whisper)
        audio = audio.set_frame_rate(config.SAMPLE_RATE)
        
        # Export
        audio.export(output_path, format="wav")
        
        logger.info(f"Preprocessed audio saved: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error preprocessing audio: {e}")
        raise

def remove_silence(audio: AudioSegment, silence_thresh: int = -40) -> AudioSegment:
    """
    Remove silence from audio
    """
    from pydub.silence import split_on_silence
    
    chunks = split_on_silence(
        audio,
        min_silence_len=1000,  # 1 second
        silence_thresh=silence_thresh,
        keep_silence=500  # Keep 500ms of silence
    )
    
    return sum(chunks) if chunks else audio