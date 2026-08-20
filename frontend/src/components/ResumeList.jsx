import { useState } from "react";
import "./ResumeList.css";
import api from "../api/api";

export default function ResumeList({ resumes, setResumes }) {
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  async function handleDelete(resumeId) {
    try {
      await api.delete(`/resumes/${resumeId}`);

      const isSuccessful = true;

      if (isSuccessful) {
        setSuccessMessage("Resume Deleted Successfully!");

        setTimeout(() => setSuccessMessage(""), 3000);
      }

      setResumes((current) =>
        current.filter(
          (resume) => (resume.id ?? resume.resume_id) !== resumeId,
        ),
      );
    } catch (err) {
      setError(err.response?.data?.error ?? "Unable to delete resume");
    }
  }

  return (
    <section className="resume-management">
      <h2>My Resumes</h2>

      {error && <p role="alert">{error}</p>}

      {resumes.length === 0 ? (
        <p>No resumes uploaded yet.</p>
      ) : (
        resumes.map((resume) => {
          const resumeId = resume.id ?? resume.resume_id;

          return (
            <article key={resumeId} className="resume-outline">
              <h3>{resume.resume_name}</h3>

              <p>File: {resume.original_file}</p>

              <p>Type: {resume.m_type}</p>

              <button type="button" onClick={() => handleDelete(resumeId)}>
                Delete Resume
              </button>
            </article>
          );
        })
      )}

      {successMessage && (
        <div className="success-display">{successMessage}</div>
      )}
    </section>
  );
}
