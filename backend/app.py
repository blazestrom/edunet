from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import tempfile, os, uuid, logging

# import heavy/optional modules lazily inside the request handler

logger = logging.getLogger("backend.app")
logging.basicConfig(level=logging.INFO)

print("🔥 NEW APP.PY LOADED 🔥")

app = FastAPI(
    title="Voice Notes Processor",
    description="Convert speech to notes using AI Whisper",
    version="1.0.0"
)

# Configure CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "*"  # Allow all origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API is running."""
    return {"status": "ok", "message": "Voice Notes Processor API"}


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return JSONResponse({"status": "healthy", "message": "API is operational"})


@app.post("/api/process", tags=["Processing"])
async def process_audio(file: UploadFile = File(...)):
    """Process audio file: transcribe and generate notes."""
    job_id = str(uuid.uuid4())
    tmp_path = None

    try:
        # Lazy imports to avoid heavy dependencies at startup
        try:
            from services.audio_service import AudioTranscriptionService
            from nlp.summarizer import generate_notes
        except ModuleNotFoundError as e:
            logger.error(f"Missing dependency: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Server misconfiguration: {str(e)}. Please install required packages."
            )
        
        # write upload to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
            tmp.write(content)
            tmp_path = tmp.name

        logger.info(f"Processing file: {file.filename} (size: {len(content)} bytes)")

        service = AudioTranscriptionService()
        try:
            logger.info("Starting transcription with Whisper...")
            transcript = service.transcribe_file(tmp_path)
        except Exception as e:
            logger.exception("Transcription failed")
            raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

        if not transcript or transcript.strip() == "":
            raise HTTPException(status_code=400, detail="No speech detected in audio")

        logger.info(f"Transcription complete. Length: {len(transcript)} chars")

        # Generate notes (optional, won't fail if Groq is unavailable)
        notes = None
        try:
            logger.info("Generating notes with Groq...")
            notes = generate_notes(transcript)
            if notes:
                logger.info(f"Notes generated. Length: {len(notes)} chars")
        except Exception as e:
            logger.warning(f"Note generation skipped: {str(e)}")

        return JSONResponse({
            "success": True,
            "job_id": job_id,
            "transcript": transcript,
            "notes": notes
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unhandled error in /api/process")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
                logger.debug(f"Cleaned up temp file: {tmp_path}")
            except Exception:
                logger.warning(f"Failed to remove temp file: {tmp_path}")
