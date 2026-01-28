import { useState } from "react";
import UploadAudio from "../components/UploadAudio";
import "../styles/Home.css";

export default function Home() {
  const [result, setResult] = useState(null);

  return (
    <div className="home-container">
      <div className="home-card">
        <h1>🎤 Voice Notes Processor</h1>
        <p className="subtitle">Convert speech to notes using AI Whisper</p>

        {/* Upload Component */}
        <UploadAudio setResult={setResult} />

        {/* Result Display */}
        {result && (
          <div className="result-section">
            <div className="result-card">
              <h2>📝 Transcript</h2>
              <p className="result-text">{result.transcript}</p>
              <small className="char-count">
                ({result.transcript.length} characters)
              </small>
            </div>

            {result.notes && (
              <div className="result-card">
                <h2>📋 Generated Notes</h2>
                <div className="notes-content">{result.notes}</div>
              </div>
            )}

            <div className="result-meta">
              <small>Job ID: {result.job_id}</small>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
