import React, { useState } from "react";
import "./ApplicationForm.css";

const intial_data = {
  company_name: "",
  job_title: "",
  job_location: "",
  work_location: "Remote",
  status: "Applied",
  date_applied: new Date().toISOString().split("T")[0],
};

export function ApplicationForm({ application, onSubmit, onCancel }) {
  const [formData, setFormData] = useState(
    application
      ? {
          company_name: application.company_name ?? "",
          job_title: application.job_title ?? "",
          job_location: application.job_location ?? "",
          work_location: application.work_location ?? "Remote",
          status: application.status ?? "Applied",
          date_applied:
            application.date_applied?.split("T")[0] ??
            new Date().toISOString().split("T")[0],
        }
      : intial_data,
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      await onSubmit(formData);
      setFormData(intial_data);
    } catch {
      setError("Unable to save the application.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="app-form" onSubmit={handleSubmit}>
      <h3 className="form-title">
        {" "}
        {application ? "Edit Job Application" : "Add Job Application"}
      </h3>

      {error && <p role="alert">{error}</p>}

      <div className="form-group">
        <label htmlFor="company_name">Company Name *</label>
        <input
          type="text"
          id="company_name"
          name="company_name"
          value={formData.company_name}
          onChange={handleChange}
          required
          placeholder="Example Company"
        />
      </div>

      <div className="form-group">
        <label htmlFor="job_title">Job Title *</label>
        <input
          type="text"
          id="job_title"
          name="job_title"
          value={formData.job_title}
          onChange={handleChange}
          required
          placeholder="Software Engineer"
        />
      </div>

      <div className="form-group">
        <label htmlFor="job_location">Job Location (City/State) *</label>
        <input
          type="text"
          id="job_location"
          name="job_location"
          value={formData.job_location}
          onChange={handleChange}
          required
          placeholder="Houston, TX"
        />
      </div>

      <div className="form-row">
        <div>
          <label htmlFor="work_location">Work Location</label>
          <select
            id="work_location"
            name="work_location"
            value={formData.work_location}
            onChange={handleChange}
          >
            <option value="On-site">On-site</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
          </select>

          <label htmlFor="job_title">Status *</label>
          <select
            id="status"
            name="status"
            value={formData.status}
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
        </div>
      </div>

      <div className="form-actions">
        {onCancel && (
          <button type="button" className="btn-secondary" onClick={onCancel}>
            Cancel
          </button>
        )}
        <button type="button" className="btn-primary" onClick={handleSubmit}>
          {isSubmitting
            ? "Saving..."
            : application
              ? "Update Application"
              : "Save Application"}
        </button>
      </div>
    </form>
  );
}
