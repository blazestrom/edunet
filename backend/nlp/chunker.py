"""
Text chunking module for splitting transcripts into manageable pieces for LLM processing
"""
import tiktoken
from typing import List, Dict, Optional
from utils.logger import logger

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count tokens in text using tiktoken.
    
    Args:
        text: Input text
        model: OpenAI model name
    
    Returns:
        Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        logger.warning(f"Failed to count tokens with tiktoken: {e}. Using fallback.")
        # Fallback: approximate 1 token ≈ 4 characters
        return len(text) // 4

def chunk_by_tokens(text: str, max_tokens: int = 2000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks based on token count with optional overlap.
    
    Args:
        text: Input text to chunk
        max_tokens: Maximum tokens per chunk (default 2000)
        overlap: Number of tokens to overlap between chunks (default 200)
    
    Returns:
        List of text chunks
    """
    logger.info(f"Chunking text (max tokens: {max_tokens}, overlap: {overlap})...")
    
    # Split into sentences
    sentences = text.split('. ')
    
    chunks = []
    current_chunk = []
    current_tokens = 0
    overlap_buffer = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Add period back if it was removed
        if not sentence.endswith('.'):
            sentence += '.'
        
        sentence_tokens = count_tokens(sentence)
        
        # If single sentence exceeds max tokens, split it further
        if sentence_tokens > max_tokens:
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append(chunk_text)
                # Keep overlap
                overlap_buffer = current_chunk[-int(len(current_chunk) * overlap/max_tokens):]
                current_chunk = overlap_buffer.copy()
                current_tokens = count_tokens(' '.join(current_chunk))
            
            # Split long sentence by words
            words = sentence.split()
            word_chunk = []
            word_tokens = 0
            
            for word in words:
                word_token_count = count_tokens(word)
                if word_tokens + word_token_count > max_tokens and word_chunk:
                    chunks.append(' '.join(word_chunk))
                    word_chunk = [word]
                    word_tokens = word_token_count
                else:
                    word_chunk.append(word)
                    word_tokens += word_token_count
            
            if word_chunk:
                chunks.append(' '.join(word_chunk))
            
            continue
        
        # Check if adding this sentence exceeds limit
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(chunk_text)
            # Keep overlap
            overlap_buffer = current_chunk[-int(len(current_chunk) * overlap/max_tokens):]
            current_chunk = overlap_buffer + [sentence]
            current_tokens = count_tokens(' '.join(current_chunk))
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    logger.info(f"Created {len(chunks)} chunks")
    return chunks

def chunk_by_time(segments: List[Dict], max_duration: int = 300) -> List[str]:
    """
    Chunk transcript by time segments (e.g., every 5 minutes).
    
    Args:
        segments: List of {start, end, text} dicts from Whisper
        max_duration: Maximum duration in seconds per chunk
    
    Returns:
        List of text chunks
    """
    logger.info(f"Chunking by time (max duration: {max_duration}s)...")
    
    chunks = []
    current_chunk = []
    chunk_start = 0
    
    for segment in segments:
        if segment['start'] - chunk_start >= max_duration:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [segment['text']]
            chunk_start = segment['start']
        else:
            current_chunk.append(segment['text'])
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    logger.info(f"Created {len(chunks)} time-based chunks")
    return chunks

def chunk_by_lines(text: str, lines_per_chunk: int = 50) -> List[str]:
    """
    Split text into chunks by number of lines.
    
    Args:
        text: Input text
        lines_per_chunk: Number of lines per chunk
    
    Returns:
        List of text chunks
    """
    lines = text.split('\n')
    chunks = []
    
    for i in range(0, len(lines), lines_per_chunk):
        chunk = '\n'.join(lines[i:i + lines_per_chunk])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def chunk_by_characters(text: str, max_chars: int = 5000, overlap: int = 500) -> List[str]:
    """
    Split text into chunks by character count with overlap.
    
    Args:
        text: Input text
        max_chars: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    logger.info(f"Chunking by character count (max: {max_chars}, overlap: {overlap})...")
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + max_chars, len(text))
        
        # Try to break at sentence boundary if possible
        if end < len(text):
            last_period = text.rfind('.', start, end)
            if last_period > start + max_chars * 0.75:  # Only if sentence is reasonably close to limit
                end = last_period + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap if end < len(text) else end
    
    logger.info(f"Created {len(chunks)} character-based chunks")
    return chunks