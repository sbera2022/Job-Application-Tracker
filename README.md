# Job Application Tracker

A full-stack web application for tracking job applications and analyzing resume compatibility with job descriptions.

Users can create an account, manage job applications, track applications through different stages of the hiring process, upload and manage resumes, and analyze how well a selected resume matches a job description.

## Features

- JWT-based user authentication
- Create, view, edit, and delete job applications
- Track application status through stages such as:
  - Applied
  - Assessment
  - Interview
  - Offer
  - Rejected
- View detailed information for individual applications
- Search and filter job applications
- Save job descriptions
- Upload and manage resumes
- Support for PDF and DOCX resumes
- Attach resumes to job applications
- Analyze resume compatibility with job descriptions
- Compare resume skills and keywords against job requirements
- Display resume match statistics and analysis results
- Secure user-specific application and resume data
- UUID-based resume file storage to prevent filename conflicts
- Dashboard for managing applications

## Tech Stack

### Frontend

- React
- JavaScript
- CSS

### Backend

- Python
- Flask
- Flask-JWT-Extended
- SQLAlchemy

### Database

- PostgreSQL
- SQLite (automated testing)

## API Endpoints

### Authentication

- `POST /auth/register`
- `POST /auth/login`

### Applications

- `POST /applications`
- `GET /applications`
- `GET /applications/{id}`
- `PATCH /applications/{id}`
- `DELETE /applications/{id}`
- `GET /applications/{id}/history`

### Resume Management

- `POST /resumes`
- `GET /resumes`
- `DELETE /resumes/{id}`
- `POST /applications/{application_id}/resumes/{resume_id}`

### Resume Analysis

- `POST /applications/{application_id}/analyze-resume/{resume_id}`

## Setup and Running

### 1. Clone the repository

Clone the repository and navigate to the project directory.

### 2. Backend Setup

Navigate to:

`Job-Application-Tracker/backend`

Install the required Python dependencies.

Apply the database migrations:

```bash
flask db upgrade
