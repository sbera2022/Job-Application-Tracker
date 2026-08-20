import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ApplicationCard } from "../components/ApplicationCard";
import { ApplicationForm } from "../components/ApplicationForm";
import SearchBar from "../components/SearchBar";
import "./DashboardPage.css";

import api from "../api/api";

function DashboardPage() {
  const navigate = useNavigate();

  const [applications, setApplications] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingApplication, setEditingApplication] = useState(null);
  const [filteredApplications, setFilteredApplications] = useState([]);

  useEffect(() => {
    fetchApplications();
  }, []);

  async function fetchApplications() {
    try {
      const response = await api.get("/applications");
      setApplications(response.data);
      setFilteredApplications(response.data);
    } catch (requestError) {
      if (requestError.response?.status === 401) {
        localStorage.removeItem("accessToken");
        navigate("/login");
        return;
      }

      setError("Unable to load applications.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleEdit(application) {
    console.log("Edit application:", application);
    setEditingApplication(application);
    setIsFormOpen(true);
  }

  async function handleDelete(applicationId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this application?",
    );

    if (!confirmed) {
      return;
    }

    try {
      await api.delete(`/applications/${applicationId}`);

      setApplications((currentApplications) =>
        currentApplications.filter(
          (application) =>
            application.application_id !== applicationId &&
            application.id !== applicationId,
        ),
      );
    } catch {
      setError("Unable to delete application.");
    }
  }

  async function handleFormSubmit(formData) {
    setError("");

    try {
      const applicationId =
        editingApplication?.application_id ?? editingApplication?.id;

      if (applicationId) {
        await api.patch(`/applications/${applicationId}`, formData);
      } else {
        await api.post("/applications", formData);
      }

      await fetchApplications();

      setIsFormOpen(false);
      setEditingApplication(null);
    } catch (requestError) {
      setError(
        requestError.response?.data?.error ?? "Unable to save application.",
      );

      throw requestError;
    }
  }

  function handleView(applicationId) {
    navigate(`/applications/${applicationId}`);
  }

  function handleLogout() {
    localStorage.removeItem("accessToken");
    navigate("/login");
  }

  if (isLoading) {
    return <p>Loading applications...</p>;
  }

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <h1>💼Job Application Tracker🔎</h1>
          <p>Manage and review your job applications.</p>
        </div>

        <div className="header-actions">
          <button type="button" onClick={handleLogout}>
            Log out
          </button>
          <button
            type="button"
            onClick={() => {
              setEditingApplication(null);
              setIsFormOpen(true);
            }}
          >
            Add Application
          </button>
        </div>
      </header>

      <SearchBar
        applications={applications}
        onResultsChange={setFilteredApplications}
      />

      {error && <p role="alert">{error}</p>}

      {isFormOpen && (
        <ApplicationForm
          application={editingApplication}
          onSubmit={handleFormSubmit}
          onCancel={() => {
            setIsFormOpen(false);
            setEditingApplication(null);
          }}
        />
      )}

      <section className="applications-section">
        {applications.length === 0 ? (
          <div className="empty-state">
            <h2>No applications yet</h2>
            <p>Add your first job application to get started.</p>
          </div>
        ) : filteredApplications.length === 0 ? (
          <div className="empty-state">
            <h2>No matching applications</h2>
            <p>Try another company name or job title.</p>
          </div>
        ) : (
          <div className="applications-grid">
            {filteredApplications.map((application) => {
              const applicationId =
                application.application_id ?? application.id;

              return (
                <ApplicationCard
                  key={applicationId}
                  company_name={application.company_name}
                  job_title={application.job_title}
                  status={application.status}
                  work_location={application.work_location}
                  job_location={application.job_location}
                  date_applied={application.date_applied}
                  onView={() => handleView(applicationId)}
                  onEdit={() => handleEdit(application)}
                  onDelete={() => handleDelete(applicationId)}
                />
              );
            })}
          </div>
        )}
      </section>
    </main>
  );
}

export default DashboardPage;
