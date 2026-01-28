from groq import Groq
import os
import logging

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_notes(text: str) -> str:
    """Generate study notes from lecture transcript using Groq API.
    
    Returns None if GROQ_API_KEY is not set.
    """
    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not set - skipping note generation")
        return None

    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""
Create clear, structured study notes from this lecture transcript.
Use headings and bullet points.

Transcript:
{text}
"""

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.exception("Failed to generate notes")
        return None
