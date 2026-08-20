import { useEffect, useRef, useState } from "react";
import "./ApplicationCard.css";

export function ApplicationCard({
  company_name,
  job_title,
  status,
  work_location,
  job_location,
  date_applied,
  onView,
  onEdit,
  onDelete,
}) {
  const [contextMenu, setContextMenu] = useState(null); // { x, y } or null
  const menuRef = useRef(null);

  function handleContextMenu(event) {
    event.preventDefault();
    setContextMenu({ x: event.clientX, y: event.clientY });
  }

  function closeMenu() {
    setContextMenu(null);
  }

  function runAction(action) {
    closeMenu();
    action?.();
  }

  useEffect(() => {
    if (!contextMenu) return;

    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        closeMenu();
      }
    }

    function handleKeyDown(event) {
      if (event.key === "Escape") closeMenu();
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeyDown);
    window.addEventListener("scroll", closeMenu, true);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("scroll", closeMenu, true);
    };
  }, [contextMenu]);

  const getStatus = (statusStr = "") => {
    switch (statusStr) {
      case "Saved":
        return "status-saved";
      case "Applied":
        return "status-applied";
      case "Assessment":
        return "status-assessment";
      case "Interview":
        return "status-interview";
      case "Offer":
        return "status-offer";
      case "Rejected":
        return "status-rejected";
      case "Withdrawn":
        return "status-withdraw";
      default:
        return "status-default";
    }
  };

  const formattedDate = date_applied
    ? new Date(date_applied).toLocaleDateString()
    : "Not specified";

  return (
    <article className="job-card" onContextMenu={handleContextMenu}>
      <div className="job-card-header">
        <h3 className="company-name">{company_name}</h3>

        <span className={`status-badge ${getStatus(status)}`}>{status}</span>
      </div>

      <div className="job-card-body">
        <h4 className="job-title">{job_title}</h4>

        <div className="meta-row">
          <span className="meta-label">Loacation:</span>
          <span className="meta-value">{work_location || job_location}</span>
        </div>

        <div className="meta-row">
          <span className="meta-label">Applied:</span>
          <span className="meta-value">{formattedDate}</span>
        </div>
      </div>

      {contextMenu && (
        <div
          ref={menuRef}
          className="job-card-context-menu"
          style={{ top: contextMenu.y, left: contextMenu.x }}
        >
          <button
            type="button"
            className="context-menu-item context-menu-item-view"
            onClick={() => runAction(onView)}
          >
            View Details
          </button>

          <button
            type="button"
            className="context-menu-item"
            onClick={() => runAction(onEdit)}
          >
            Edit
          </button>

          <button
            type="button"
            className="context-menu-item context-menu-item-delete"
            onClick={() => runAction(onDelete)}
          >
            Delete
          </button>
        </div>
      )}
    </article>
  );
}
