import { useState } from "react";
import api from "../api/api";
import { data } from "react-router-dom";
import "./ResumeUpload.css";

function ResumeUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [resumeName, setResumeName] = useState("");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResumeName(selectedFile.name);
      setError("");
    }
  };

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setUploading(true);
    setError("");

    const formData = new FormData();

    formData.append("file", file);
    formData.append("resume_name", resumeName);

    try {
      const response = await api.post("/resumes", formData);

      if (onUploadSuccess) {
        onUploadSuccess(response.data.resume);

        setSuccessMessage("Resume Uploaded Successfully!");

        setTimeout(() => setSuccessMessage(""), 3000);
      }

      setFile(null);
      setResumeName("");
      event.target.reset();
    } catch (err) {
      setError(
        err.response?.data?.error ?? "Something went wrong during the upload.",
      );
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="resume-page">
      <h3>Upload Resume</h3>

      <form onSubmit={handleSubmit}>
        <div className="file-type">
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleChange}
            disabled={uploading}
          />
        </div>

        {resumeName && (
          <p className="resume-name">
            Selected: <strong>{resumeName}</strong>
          </p>
        )}

        {error && <p className="error-display">⚠️ {error}</p>}

        <button
          type="submit"
          disabled={uploading || !file}
          className="upload-button"
        >
          {uploading ? "Uploading..." : "Upload File"}
        </button>

        {successMessage && (
          <div className="success-display">{successMessage}</div>
        )}
      </form>
    </div>
  );
}

export default ResumeUpload;
