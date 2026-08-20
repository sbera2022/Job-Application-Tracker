import { useMemo, useState } from "react";
import "./SearchBar.css";

function SearchBar({ applications = [], onResultsChange }) {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredApplications = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();

    if (!query) {
      return applications;
    }
    return applications.filter((application) => {
      const company = application.company_name?.toLowerCase() ?? "";
      const title = application.job_title?.toLowerCase() ?? "";

      return company.includes(query) || title.includes(query);
    });
  }, [applications, searchQuery]);

  function handleSearchChange(event) {
    const value = event.target.value;
    setSearchQuery(value);

    if (onResultsChange) {
      const query = value.trim().toLowerCase();

      const results = !query
        ? applications
        : applications.filter((application) => {
            const company = application.company_name?.toLowerCase() ?? "";
            const title = application.job_title?.toLowerCase() ?? "";

            return company.includes(query) || title.includes(query);
          });

      onResultsChange(results);
    }
  }

  return (
    <div className="search-bar">
      <label htmlFor="application-search" className="search-title">
        Search Applications
      </label>

      <input
        id="application-search"
        type="text"
        placeholder="Search by company or role..."
        value={searchQuery}
        onChange={handleSearchChange}
        className="search-text"
      />
      <span className="search-icon" aria-hidden="true">
        🔍
      </span>

      <p className="search-filter">
        {filteredApplications.length} result
        {filteredApplications.length === 1 ? "" : "s"}
      </p>
    </div>
  );
}

export default SearchBar;
