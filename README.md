# 🎓 Lecture Voice-to-Notes Generator

**Convert lecture recordings into comprehensive study materials with AI-powered transcription and content generation.**

Transform your lectures into well-organized study notes, quiz questions, and flashcards - perfect for exam preparation and efficient learning.

---

## ✨ Features

- 🎤 **Speech-to-Text Transcription**: Uses OpenAI Whisper for highly accurate audio transcription
- 📝 **Intelligent Note Generation**: Creates structured, hierarchical study notes optimized for learning
- 📋 **Quiz Question Generation**: Automatically generates multiple-choice questions from lecture content
- 🎴 **Flashcard Creation**: Produces review flashcards in Q&A format for spaced repetition
- 📄 **Multiple Export Formats**: Save as Markdown, HTML, PDF, TXT, or JSON
- 🌐 **Web Interface**: User-friendly browser-based UI for uploading and processing lectures
- ⚡ **Fast Processing**: Efficient pipeline from audio to study materials
- 🛡️ **Production-Ready**: Built with FastAPI for reliability and performance

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (for GPT-4 or GPT-3.5-turbo)
- pip package manager

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd edunet
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4
```

### 4. Run the Application

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the Interface

Open your browser and navigate to:
- **Web UI**: http://localhost:8000/test
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📖 Usage Guide

### Via Web Interface

1. **Upload Audio or Paste Transcript**
   - Click "Click to upload audio file" or switch to "Text Input" tab
   - Supported formats: WAV, MP3, FLAC, OGG, M4A, etc.

2. **Add Metadata (Optional)**
   - Course Name: e.g., "Advanced Python"
   - Topic: e.g., "Object-Oriented Programming"

3. **Configure Generation Options**
   - Check/uncheck "Quiz Questions" and "Flashcards"
   - Adjust slider for number of questions/cards

4. **Click "Process"**
   - Wait for processing to complete
   - Results appear in the "Results" panel

5. **View & Use Results**
   - Copy content directly from the interface
   - Download generated files (PDF, Markdown, etc.)

### Via API

#### Transcribe Audio File

```bash
curl -X POST "http://localhost:8000/api/audio/transcribe-file" \
  -F "file=@lecture.mp3"
```

Response:
```json
{
  "transcript": "Today we'll discuss...",
  "success": true,
  "message": "File transcription completed",
  "duration_seconds": 1234
}
```

#### Process Complete Pipeline

```bash
curl -X POST "http://localhost:8000/api/audio/process" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Your lecture transcript...",
    "course_name": "Python 101",
    "topic": "Functions",
    "generate_quiz": true,
    "generate_flashcards": true,
    "quiz_questions": 5,
    "flashcard_count": 10
  }'
```

Response:
```json
{
  "success": true,
  "message": "Audio processing completed successfully",
  "request_id": "abc123...",
  "transcript": "Cleaned transcript...",
  "notes": "## Study Notes\n...",
  "quiz": "Q: ...\nA) ...",
  "flashcards": "Q: ...\nA: ...",
  "output_files": {
    "markdown": "/output/lecture_notes.md",
    "html": "/output/lecture_notes.html",
    "pdf": "/output/lecture_notes.pdf"
  }
}
```

---

## 🏗️ Architecture

```
edunet/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   └── settings.py         # Configuration management
│   ├── routes/
│   │   └── audio_routes.py     # API endpoints
│   ├── services/
│   │   └── audio_service.py    # Audio transcription service
│   ├── nlp/
│   │   ├── cleaner.py          # Text cleaning & normalization
│   │   ├── chunker.py          # Text segmentation
│   │   └── summarizer.py       # Content generation with LLM
│   ├── output/
│   │   ├── formatter.py        # Output formatting
│   │   └── exporter.py         # File export functionality
│   ├── utils/
│   │   └── logger.py           # Logging setup
│   ├── prompts/                # LLM prompt templates
│   ├── static/
│   │   └── test.html           # Web interface
│   └── requirements.txt        # Backend dependencies
├── frontend/                   # (Optional) Full frontend app
├── requirements.txt            # Root dependencies
├── .env.example                # Environment configuration template
└── README.md                   # This file
```

---

## 🔧 API Reference

### Health Check
```
GET /health
GET /api/audio/health
```

### Transcription
```
POST /api/audio/transcribe-file
- file: Audio file (multipart/form-data)
- model_size: Whisper model (tiny, base, small, medium, large)

POST /api/audio/transcribe-live
- duration: Recording length in seconds (1-60)
- model_size: Whisper model
```

### Complete Processing
```
POST /api/audio/process
- transcript: Raw or cleaned transcript text
- course_name: (Optional) Course name
- topic: (Optional) Lecture topic
- generate_quiz: Boolean (default: true)
- generate_flashcards: Boolean (default: true)
- quiz_questions: Number of quiz questions (1-20)
- flashcard_count: Number of flashcards (5-50)
```

---

## 🛠️ Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key
LLM_MODEL=gpt-4

# Audio Settings
AUDIO_SAMPLE_RATE=16000
MAX_AUDIO_FILE_SIZE=104857600  # 100MB

# NLP Settings
MAX_CHUNK_TOKENS=2000
TEMPERATURE=0.7

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# CORS Configuration
CORS_ORIGINS=*
```

---

## 📋 Supported Formats

### Input Audio
- WAV, MP3, FLAC, OGG, M4A, AAC, OPUS, etc.
- Maximum file size: 100MB
- Automatic format detection

### Output Formats
- **Markdown (.md)**: Great for version control
- **HTML (.html)**: Styled, web-ready documents
- **PDF (.pdf)**: Print-friendly format
- **TXT (.txt)**: Plain text format
- **JSON (.json)**: Structured data export

---

## 🚨 Troubleshooting

### "OPENAI_API_KEY not configured"
- Ensure `.env` file exists with a valid OpenAI API key
- Generate API key at: https://platform.openai.com/account/api-keys

### "Transcription failed" or "No speech detected"
- Check audio file is valid and contains clear speech
- Ensure audio file is < 100MB
- Verify microphone permissions if using live recording

### Slow Processing
- Use smaller Whisper model: `base` instead of `large`
- Reduce output length limits in configuration
- Process shorter audio segments separately

### CORS Errors
- Frontend and backend need matching CORS settings
- Update `CORS_ORIGINS` in `.env` if needed

---

## 📦 Dependencies

### Core
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-dotenv**: Environment configuration

### AI/ML
- **OpenAI**: GPT models for content generation
- **Whisper**: Speech-to-text transcription
- **Tiktoken**: Token counting

### Processing
- **Markdown**: Markdown generation
- **FPDF**: PDF export
- **PyAudio**: Optional microphone recording

See `requirements.txt` for complete list with versions.

---

## 🎯 Example Workflow

1. **Record or Upload Lecture**
   - Use microphone or upload pre-recorded audio file

2. **System Processes Audio**
   - Whisper transcribes audio to text
   - Text is cleaned and normalized

3. **AI Generates Content**
   - Study notes extracted and structured
   - Quiz questions created from key concepts
   - Flashcards generated for revision

4. **Export Results**
   - Download in preferred format (PDF, Markdown, HTML)
   - Use immediately for studying or share with classmates

---

## 🔐 Security Notes

- **API Keys**: Never commit `.env` file to version control
- **File Upload**: Implement proper authentication in production
- **Rate Limiting**: Add rate limiting for production deployment
- **Input Validation**: All inputs are validated and sanitized

---

## 📈 Performance

- **Transcription**: ~30 seconds for 1 hour lecture (depends on Whisper model)
- **Content Generation**: ~60-120 seconds for complete pipeline
- **Memory Usage**: ~4-8GB with large Whisper model
- **Concurrent Requests**: Depends on server resources

---

## 🛣️ Roadmap

- [ ] Support for multiple languages
- [ ] Advanced customization of prompt templates
- [ ] Database integration for storing results
- [ ] User authentication and multi-user support
- [ ] Batch processing for multiple lectures
- [ ] Real-time processing status updates
- [ ] Integration with learning platforms (Canvas, Blackboard)
- [ ] Mobile app for iOS/Android

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 💬 Support & Contact

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Full API docs at `/docs`

---

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for Whisper and GPT models
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- The open-source community for various dependencies

---

**Last Updated**: January 2026
**Version**: 1.0.0
