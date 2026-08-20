import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/api";
import "./ApplicationDetailsPage.css";
import ResumeUpload from "../components/ResumeUpload";
import ResumeList from "../components/ResumeList";

export function ApplicationDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [successRAMessage, setSuccessRAMessage] = useState("");
  const [successAppMessage, setSuccessAppMessage] = useState("");

  const [analysis, setAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState("");

  const [resumes, setResumes] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [resumeLoading, setResumeLoading] = useState(true);

  const [formData, setFormData] = useState(null);
  const [appData, setAppData] = useState(null);

  useEffect(() => {
    async function fetchJobData() {
      try {
        setLoading(true);
        setError("");

        const response = await api.get(`/applications/${id}`);

        setAppData(response.data);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem("accessToken");
          navigate("/login");
          return;
        }

        setError(
          err.response?.data?.error ?? "Could not retrieve application details",
        );
      } finally {
        setLoading(false);
      }
    }

    fetchJobData();
  }, [id, navigate]);

  useEffect(() => {
    async function fetchResumes() {
      try {
        const response = await api.get("/resumes");
        setResumes(response.data);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem("accessToken");
          navigate("/login");
          return;
        }

        setError(err.response?.data?.error ?? "Unable to load resumes");
      } finally {
        setResumeLoading(false);
      }
    }

    fetchResumes();
  }, [navigate]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  function startEditing() {
    setFormData({ ...appData });
    setIsEditing(true);
  }

  function cancelEditing() {
    setFormData(null);
    setIsEditing(false);
    setError("");
  }

  const getScoreClass = (score) => {
    if (score >= 75) return "high";
    if (score >= 40) return "medium";
    return "low";
  };

  async function handleAnalyzeResume(resumeId) {
    setAnalysisLoading(true);
    setAnalysisError("");

    try {
      try {
        await api.post(`/applications/${id}/resumes/${resumeId}`);

        const isSuccessful = true;

        if (isSuccessful) {
          setSuccessRAMessage("Resume analysis completed Successfully!");

          setTimeout(() => setSuccessRAMessage(""), 3000);
        }
      } catch (attachError) {
        if (attachError.response?.status !== 409) {
          throw attachError;
        }
      }

      const response = await api.post(
        `/applications/${id}/analyze-resume/${resumeId}`,
      );

      setAnalysis(response.data.analysis);
    } catch (err) {
      setAnalysisError(err.response?.data?.error ?? "Unable to analyze resume");
    } finally {
      setAnalysisLoading(false);
    }
  }

  const handleFormChange = async (event) => {
    event.preventDefault();

    try {
      const response = await api.patch(`/applications/${id}`, formData);

      const isSuccessful = true;

      if (isSuccessful) {
        setSuccessAppMessage("Application updated Successfully!");

        setTimeout(() => setSuccessAppMessage(""), 3000);
      }

      setAppData(response.data);
      setFormData(null);
      setIsEditing(false);
      setError("");
    } catch (err) {
      setError(err.response?.data?.error ?? "Unable to update application");
    }
  };

  if (loading && !appData) {
    return <div className="data-fetch">Fetching data record...</div>;
  }

  if (error && !appData) {
    return <div className="data-fetch">{error}</div>;
  }

  const formatDateTime = (value) =>
    value ? new Date(value).toLocaleString() : "Not available";

  return (
    <main className="application-details-page">
      <div className="application-details-layout">
        <section className="application-main-card">
          <header className="form-details">
            <div>
              <button
                type="button"
                onClick={() => navigate("/dashboard")}
                className="btn-primary"
              >
                Back to Dashboard
              </button>

              <div className="form-id">
                <div>
                  <strong>Application ID:</strong>{" "}
                  {appData.id ?? appData.application_id}
                </div>

                <div>
                  <strong>Created:</strong> {formatDateTime(appData.created_at)}
                  {" | "}
                  <strong>Last Active:</strong>{" "}
                  {formatDateTime(appData.last_activity)}
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={isEditing ? cancelEditing : startEditing}
              className={`btn-secondary ${
                isEditing ? "btn-secondary-edit" : "btn-secondary-set-edit"
              }`}
            >
              {isEditing ? "Cancel Changes" : "Edit Details"}
            </button>
          </header>

          {error && <p role="alert">{error}</p>}
          {successAppMessage && (
            <div className="success-display">{successAppMessage}</div>
          )}

          {!isEditing ? (
            <section className="application-details">
              <h1>{appData.job_title}</h1>
              <h2>{appData.company_name}</h2>

              <div className="detail-row">
                <strong>Status:</strong>
                <span>{appData.status}</span>
              </div>

              <div className="detail-row">
                <strong>Work Type:</strong>
                <span>{appData.work_location}</span>
              </div>

              <div className="detail-row">
                <strong>Location:</strong>
                <span>{appData.job_location || "Not specified"}</span>
              </div>

              <div className="detail-row">
                <strong>Date applied:</strong>
                <span>{appData.date_applied || "Not specified"}</span>
              </div>

              <div className="detail-row">
                <strong>Salary:</strong>
                <span>
                  {appData.salary_min || appData.salary_max
                    ? `${appData.currency ?? "USD"} ${
                        appData.salary_min ?? "Not specified"
                      } – ${appData.salary_max ?? "Not specified"}`
                    : "Not specified"}
                </span>
              </div>

              <div className="detail-row">
                <strong>Job URL:</strong>
                {appData.job_url ? (
                  <a href={appData.job_url} target="_blank" rel="noreferrer">
                    Open job posting
                  </a>
                ) : (
                  <span>Not provided</span>
                )}
              </div>

              <div className="detail-section">
                <h3>Notes</h3>
                <p>{appData.notes || "No notes added."}</p>
              </div>

              <div className="detail-section">
                <h3>Job Description</h3>
                <p>
                  {appData.job_description || "No job description provided."}
                </p>
              </div>
            </section>
          ) : formData ? (
            <form className="application-edit-form" onSubmit={handleFormChange}>
              <label htmlFor="company_name">Company Name</label>
              <input
                id="company_name"
                name="company_name"
                value={formData.company_name ?? ""}
                onChange={handleChange}
                required
              />

              <label htmlFor="job_title">Job Title</label>
              <input
                id="job_title"
                name="job_title"
                value={formData.job_title ?? ""}
                onChange={handleChange}
                required
              />

              <label htmlFor="job_location">Job Location</label>
              <input
                id="job_location"
                name="job_location"
                value={formData.job_location ?? ""}
                onChange={handleChange}
              />

              <label htmlFor="work_location">Work Type</label>
              <select
                id="work_location"
                name="work_location"
                value={formData.work_location ?? "Remote"}
                onChange={handleChange}
              >
                <option value="Remote">Remote</option>
                <option value="Hybrid">Hybrid</option>
                <option value="On-site">On-site</option>
              </select>

              <label htmlFor="status">Status</label>
              <select
                id="status"
                name="status"
                value={formData.status ?? "Applied"}
                onChange={handleChange}
              >
                <option value="Saved">Saved</option>
                <option value="Applied">Applied</option>
                <option value="Assessment">Assessment</option>
                <option value="Interview">Interview</option>
                <option value="Offer">Offer</option>
                <option value="Rejected">Rejected</option>
                <option value="Withdrawn">Withdrawn</option>
              </select>

              <label htmlFor="date_applied">Date Applied</label>
              <input
                type="date"
                id="date_applied"
                name="date_applied"
                value={formData.date_applied?.split("T")[0] ?? ""}
                onChange={handleChange}
              />

              <label htmlFor="notes">Notes</label>
              <textarea
                id="notes"
                name="notes"
                value={formData.notes ?? ""}
                onChange={handleChange}
              />

              <label htmlFor="job_description">Job Description</label>
              <textarea
                id="job_description"
                name="job_description"
                value={formData.job_description ?? ""}
                onChange={handleChange}
              />

              <button type="submit" className="btn-primary">
                Save Changes
              </button>
            </form>
          ) : (
            <p>Preparing edit form...</p>
          )}
        </section>
        <section className="resume-analysis-section">
          <h2>Resume Analysis</h2>

          <ResumeUpload
            onUploadSuccess={(newResume) => {
              setResumes((current) => [newResume, ...current]);

              setSelectedResumeId(newResume.id ?? newResume.resume_id);
            }}
          />
          <ResumeList resumes={resumes} setResumes={setResumes} />
          {resumeLoading ? (
            <p>Loading resumes...</p>
          ) : resumes.length === 0 ? (
            <p>You haven't uploaded any resumes yet.</p>
          ) : (
            <>
              <label htmlFor="resume-select">Select Resume</label>

              <select
                id="resume-select"
                value={selectedResumeId}
                onChange={(event) => setSelectedResumeId(event.target.value)}
              >
                <option value="">Choose a resume</option>

                {resumes.map((resume) => (
                  <option
                    key={resume.id ?? resume.resume_id}
                    value={resume.id ?? resume.resume_id}
                  >
                    {resume.resume_name}
                  </option>
                ))}
              </select>

              <button
                type="button"
                disabled={!selectedResumeId || analysisLoading}
                onClick={() => handleAnalyzeResume(selectedResumeId)}
              >
                {analysisLoading ? "Analyzing..." : "Analyze Resume"}
              </button>
            </>
          )}

          {analysisError && <p role="alert">{analysisError}</p>}
          {successRAMessage && (
            <div className="success-display">{successRAMessage}</div>
          )}

          {analysis && (
            <div className="resume-analysis">
              <div className="tracker-result-box">
                <div className="tracker-header">
                  <span>Job Description Similarity</span>
                  <span>{analysis.match_score}%</span>
                </div>

                <div className="tracker-progress-track">
                  <div
                    className={`tracker-progress-fill ${getScoreClass(analysis.match_score)}`}
                    style={{ width: `${analysis.match_score}%` }}
                  />
                </div>
              </div>

              <h3>Matching Skills</h3>

              {analysis.matching_skills?.length > 0 ? (
                <ul>
                  {analysis.matching_skills.map((skill) => (
                    <li key={skill}>✔️{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No matching skills detected.</p>
              )}

              <h3>Missing Skills</h3>

              {analysis.missing_skills?.length > 0 ? (
                <ul>
                  {analysis.missing_skills.map((skill) => (
                    <li key={skill}>🔴{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No missing skills detected.</p>
              )}

              <h3>Resume Skills</h3>
              {analysis.resume_skills?.length > 0 ? (
                <ul>
                  {analysis.resume_skills.map((skill) => (
                    <li key={skill}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No resume skills detected.</p>
              )}

              <h3>Job Skills</h3>
              {analysis.job_skills?.length > 0 ? (
                <ul>
                  {analysis.job_skills.map((skill) => (
                    <li key={skill}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No job skills detected.</p>
              )}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

export default ApplicationDetailsPage;
