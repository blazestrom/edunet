"""
Text cleaning and normalization module for lecture transcripts
"""
import re
from typing import List
from utils.logger import logger

# Common filler words and phrases in lectures
FILLER_WORDS = [
    "um", "uh", "er", "ah", "like", "you know", "basically", "actually",
    "literally", "sort of", "kind of", "i mean", "right", "okay", "so",
    "well", "you see", "i think", "i guess", "at least", "don't you know",
    "furthermore", "moreover", "in addition"
]

def remove_filler_words(text: str) -> str:
    """
    Remove common filler words from transcript.
    
    Args:
        text: Input transcript text
    
    Returns:
        Cleaned text without filler words
    """
    cleaned = text
    for filler in FILLER_WORDS:
        # Case-insensitive replacement with word boundaries
        pattern = r'\b' + re.escape(filler) + r'\b'
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def fix_punctuation(text: str) -> str:
    """
    Fix common punctuation issues in transcripts.
    
    Args:
        text: Input text with punctuation issues
    
    Returns:
        Text with corrected punctuation
    """
    # Remove space before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Add space after punctuation if missing
    text = re.sub(r'([.,!?;:])([A-Za-z])', r'\1 \2', text)
    
    # Fix multiple periods
    text = re.sub(r'\.{2,}', '.', text)
    
    # Ensure proper capitalization at sentence start
    sentences = re.split(r'([.!?])\s*', text)
    result = []
    capitalize_next = True
    
    for i, part in enumerate(sentences):
        if part in ['.', '!', '?']:
            result.append(part + ' ')
            capitalize_next = True
        elif part.strip():
            if capitalize_next and part:
                part = part[0].upper() + part[1:] if len(part) > 0 else part
                capitalize_next = False
            result.append(part)
    
    return ''.join(result).strip()

def normalize_text(text: str) -> str:
    """
    Normalize text by removing special characters and extra whitespace.
    
    Args:
        text: Input text
    
    Returns:
        Normalized text
    """
    # Remove special unicode characters but keep common punctuation
    text = re.sub(r'[^\w\s\-.,!?;:\'"()]', '', text, flags=re.UNICODE)
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def segment_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences intelligently.
    
    Args:
        text: Input text
    
    Returns:
        List of sentences
    """
    # Split by common sentence-ending patterns
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Clean and filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def remove_repetitions(text: str) -> str:
    """
    Remove repeated phrases (common in lectures).
    
    Args:
        text: Input text
    
    Returns:
        Text with repeated phrases removed
    """
    words = text.split()
    
    # Remove consecutive duplicate words
    cleaned_words = []
    prev_word = None
    for word in words:
        if word.lower() != prev_word:
            cleaned_words.append(word)
        prev_word = word.lower()
    
    return ' '.join(cleaned_words)

def clean_transcript(text: str) -> str:
    """
    Complete transcript cleaning pipeline.
    
    Args:
        text: Raw transcript from speech-to-text
    
    Returns:
        Cleaned and normalized transcript
    """
    logger.info("Starting transcript cleaning...")
    
    # Step 1: Normalize unicode characters
    text = normalize_text(text)
    logger.debug("Normalized unicode characters")
    
    # Step 2: Remove filler words
    text = remove_filler_words(text)
    logger.debug("Removed filler words")
    
    # Step 3: Fix punctuation
    text = fix_punctuation(text)
    logger.debug("Fixed punctuation")
    
    # Step 4: Remove repeated characters
    text = re.sub(r'([a-z])\1{2,}', r'\1', text, flags=re.IGNORECASE)
    logger.debug("Removed repeated characters")
    
    # Step 5: Remove consecutive duplicate words
    text = remove_repetitions(text)
    logger.debug("Removed repetitions")
    
    # Step 6: Final whitespace cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    logger.debug("Final whitespace cleanup")
    
    logger.info(f"Transcript cleaning completed")
    
    return text

def split_paragraphs(text: str, max_chars: int = 500) -> List[str]:
    """
    Split text into paragraphs for better readability.
    
    Args:
        text: Input text
        max_chars: Maximum characters per paragraph
    
    Returns:
        List of paragraphs
    """
    sentences = segment_into_sentences(text)
    paragraphs = []
    current_para = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length > max_chars and current_para:
            paragraphs.append(' '.join(current_para))
            current_para = [sentence]
            current_length = sentence_length
        else:
            current_para.append(sentence)
            current_length += sentence_length + 1  # +1 for space
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs