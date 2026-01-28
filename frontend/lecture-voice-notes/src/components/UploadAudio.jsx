import { useState } from "react";
import { uploadAudio } from "../services/api";
import "../styles/UploadAudio.css";

export default function UploadAudio({ setResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an audio file");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await uploadAudio(file);

      if (result && result.success && result.transcript) {
        setResult(result);
        setError(null);
      } else {
        setError(result?.detail || "Unexpected response from server");
      }
    } catch (err) {
      console.error("Upload error:", err);
      setError(
        err.response?.data?.detail || err.message || "Server not reachable"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <label htmlFor="audio-input" className="file-label">
        📁 Select Audio File
      </label>
      <input
        id="audio-input"
        type="file"
        accept="audio/*"
        onChange={(e) => {
          setFile(e.target.files[0]);
          setError(null);
        }}
        className="file-input"
      />
      {file && (
        <div className="file-info">
          <span>✓ {file.name}</span>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={loading || !file}
        className="btn btn-primary"
      >
        {loading ? "⏳ Processing..." : "🚀 Upload & Process"}
      </button>

      {error && (
        <div className="alert alert-error">
          <span>❌</span> {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Transcribing audio with Whisper AI...</p>
        </div>
      )}
    </div>
  );
}
