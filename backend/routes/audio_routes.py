from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile, os

from services.audio_service import AudioTranscriptionService
from nlp.summarizer import generate_notes

router = APIRouter(prefix="/api/audio", tags=["audio"])

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        service = AudioTranscriptionService()
        transcript = service.transcribe_file(tmp_path)

        if not transcript:
            raise HTTPException(400, "No speech detected")

        notes = generate_notes(transcript)

        return {
            "transcript": transcript,
            "notes": notes
        }

    finally:
        os.remove(tmp_path)
