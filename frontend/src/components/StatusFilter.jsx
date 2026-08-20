import { useState } from "react";
import "./StatusFilter.css";

export function StatusFilter({ applications = [], onResultsChange }) {
  const [filterStatus, setFilterStatus] = useState("All");

  function handleStatusChange(event) {
    const value = event.target.value;
    setFilterStatus(value);

    const results =
      value === "All"
        ? applications
        : applications.filter((app) => app.status === value);

    onResultsChange?.(results);
  }

  return (
    <div className="filter-border">
      <label htmlFor="status-filter" className="filter-text">
        Filter by Status:
      </label>
      <select
        id="status-filter"
        value={filterStatus}
        onChange={handleStatusChange}
        className="status-option"
      >
        <option value="All">All</option>
        <option value="Saved">Saved</option>
        <option value="Applied">Applied</option>
        <option value="Assessment">Assessment</option>
        <option value="Interview">Interview</option>
        <option value="Offer">Offer</option>
        <option value="Rejected">Rejected</option>
        <option value="Withdrawn">Withdrawn</option>
      </select>
    </div>
  );
}
