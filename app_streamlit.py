import streamlit as st
import os
import sys
from pathlib import Path
import tempfile

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from services.audio_service import AudioTranscriptionService
from nlp.summarizer import generate_notes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Voice Notes Processor",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        border-radius: 10px;
    }
    .transcript-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #6366f1;
    }
    .notes-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
    }
    .success-box {
        background-color: #d1fae5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        color: #065f46;
    }
    .error-box {
        background-color: #fee2e2;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ef4444;
        color: #7f1d1d;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 🎤 Voice Notes Processor")
st.markdown("Convert speech to notes using AI Whisper")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.markdown("**🎵 Audio Settings**")
    model_size = st.selectbox(
        "Whisper Model Size",
        ["tiny", "base", "small", "medium", "large"],
        index=0,
        help="tiny=fast but less accurate, large=accurate but slower"
    )
    model_info = {
        "tiny": "390MB - Fastest (⚡⚡⚡)",
        "base": "1.5GB - Balanced (⚡⚡)",
        "small": "2.8GB - Better accuracy (⚡)",
        "medium": "3GB - High accuracy",
        "large": "3.1GB - Best accuracy (🐢)"
    }
    st.info(model_info[model_size])
    
    st.markdown("**📝 Note Generation**")
    note_type = st.selectbox(
        "Note Format",
        ["Summary Notes", "Flashcards", "Quiz Questions", "Bullet Points"],
        help="Choose the type of notes you want"
    )
    
    note_length = st.select_slider(
        "Note Length",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )
    
    include_timestamps = st.checkbox("Include timestamps", value=False)
    
    st.markdown("---")
    st.markdown("**ℹ️ About**")
    st.info("🎤 Transcribe audio using Whisper\n\n📝 Generate smart notes with Groq AI")

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📁 Select Audio File")
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["mp3", "m4a", "wav", "flac", "ogg"],
        help="Supported formats: MP3, M4A, WAV, FLAC, OGG"
    )
    
    if uploaded_file:
        st.success(f"✓ File selected: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size / 1024:.1f} KB")

with col2:
    st.markdown("### 🚀 Process Audio")
    
    if uploaded_file is None:
        st.warning("Please select an audio file first")
    else:
        if st.button("Upload & Process", use_container_width=True, type="primary"):
            with st.spinner("⏳ Processing audio... (This may take 1-2 minutes)"):
                try:
                    # Save uploaded file to temp location
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        tmp_path = tmp.name
                    
                    try:
                        # Transcribe with Whisper
                        st.info("🎵 Transcribing audio with Whisper...")
                        service = AudioTranscriptionService(model_name=model_size)
                        transcript = service.transcribe_file(tmp_path)
                        
                        if not transcript or transcript.strip() == "":
                            st.error("❌ No speech detected in audio file")
                        else:
                            st.session_state.transcript = transcript
                            st.success("✅ Transcription complete!")
                            
                            # Generate notes
                            st.info("📝 Generating study notes...")
                            notes_prompt = f"""
Based on the following transcript, generate {note_type.lower()} in {note_length} format.

Format: {note_type}
Length: {note_length}

Transcript:
{transcript}
"""
                            notes = generate_notes(notes_prompt)
                            
                            if notes:
                                st.session_state.notes = notes
                                st.session_state.note_type = note_type
                                st.success("✅ Notes generated!")
                            else:
                                st.warning("⚠️ Could not generate notes (check GROQ_API_KEY)")
                                st.session_state.notes = None
                    
                    finally:
                        # Clean up temp file
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.transcript = None
                    st.session_state.notes = None

# Display results
st.markdown("---")

if "transcript" in st.session_state and st.session_state.transcript:
    st.markdown("### 📄 Transcript")
    with st.container():
        st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Copy Transcript", use_container_width=True):
            st.success("Copied to clipboard!")
    with col2:
        if st.button("⬇️ Download Transcript", use_container_width=True):
            st.download_button(
                label="Download as .txt",
                data=st.session_state.transcript,
                file_name=f"transcript_{uploaded_file.name.split('.')[0]}.txt",
                mime="text/plain",
                use_container_width=True
            )

if "notes" in st.session_state and st.session_state.notes:
    st.markdown("### 📚 Study Notes")
    with st.container():
        st.markdown(f'<div class="notes-box">{st.session_state.notes}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Copy Notes", use_container_width=True):
            st.success("Copied to clipboard!")
    with col2:
        if st.button("⬇️ Download Notes", use_container_width=True):
            st.download_button(
                label="Download as .txt",
                data=st.session_state.notes,
                file_name=f"notes_{uploaded_file.name.split('.')[0]}.txt",
                mime="text/plain",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("""
<center>
    <p style="color: #999; font-size: 12px;">
        Powered by OpenAI Whisper 🤖 & Groq API ⚡
    </p>
</center>
""", unsafe_allow_html=True)

# Initialize session state
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "notes" not in st.session_state:
    st.session_state.notes = None
