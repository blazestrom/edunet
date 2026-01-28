import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

AUDIO_SAMPLE_RATE = 16000

APP_NAME = "Lecture Voice-to-Notes Generator"
