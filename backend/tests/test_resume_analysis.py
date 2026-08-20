import pytest
from app.extensions import db
from app.models import JobApplication, Resume, ApplicationResume


@pytest.fixture
def user_a_resources(app, auth_user_a):
    job = JobApplication(
        company_name="OpenAI",
        job_title="Research Scientist",
        job_description=(
            "We are seeking a scientist with deep "
            "knowledge of Python and neural networks."
        ),
        work_location="Remote",
        user_id=auth_user_a["user_id"],
    )

    resume = Resume(
        resume_name="cv.pdf",
        original_file="cv.pdf",
        storage_key="abc.pdf",
        m_type="application/pdf",
        file_size_bytes=100,
        user_id=auth_user_a["user_id"],
    )

    db.session.add_all([job, resume])
    db.session.commit()

    attachment = ApplicationResume(
        application_id=job.application_id,
        resume_id=resume.resume_id,
    )

    db.session.add(attachment)
    db.session.commit()

    return {
        "application_id": job.application_id,
        "resume_id": resume.resume_id,
    }


def test_successful_resume_analysis(client, auth_user_a, user_a_resources, monkeypatch):
    monkeypatch.setattr(
        "app.routes.applications.os.path.exists",
        lambda path: True,
    )

    monkeypatch.setattr(
        "app.routes.applications."
        "resume_parser.extract_resume_text",
        lambda path, ext: (
            "Python neural networks machine learning"
        ),
    )

    response = client.post(
        f"/applications/"
        f"{user_a_resources['application_id']}"
        f"/analyze-resume/"
        f"{user_a_resources['resume_id']}",
        headers=auth_user_a["headers"],
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert "analysis" in response.json
    assert "match_score" in response.json["analysis"]
    assert "matching_skills" in response.json["analysis"]
    assert "missing_skills" in response.json["analysis"]
    assert "resume_skills" in response.json["analysis"]
    assert "job_skills" in response.json["analysis"]


def test_reject_analysis_without_job_description(
    client,
    auth_user_a,
    user_a_resources,
    monkeypatch,
):
    job = db.session.get(
        JobApplication,
        user_a_resources["application_id"],
    )

    job.job_description = ""
    db.session.commit()

    monkeypatch.setattr(
        "app.routes.applications.os.path.exists",
        lambda path: True,
    )

    monkeypatch.setattr(
        "app.routes.applications."
        "resume_parser.extract_resume_text",
        lambda path, ext: "Python Flask SQL",
    )

    response = client.post(
        f"/applications/"
        f"{user_a_resources['application_id']}"
        f"/analyze-resume/"
        f"{user_a_resources['resume_id']}",
        headers=auth_user_a["headers"],
    )

    assert response.status_code == 400
    assert "error" in response.json


@pytest.mark.parametrize(
    "invalid_target",
    [
        "application",
        "resume",
        "both",
    ],
)
def test_invalid_resource_ids(
    client,
    auth_user_a,
    user_a_resources,
    invalid_target,
):
    valid_app_id = user_a_resources["application_id"]
    valid_resume_id = user_a_resources["resume_id"]

    if invalid_target == "application":
        application_id = 999
        resume_id = valid_resume_id

    elif invalid_target == "resume":
        application_id = valid_app_id
        resume_id = 999

    else:
        application_id = 999
        resume_id = 999

    response = client.post(
        f"/applications/{application_id}"
        f"/analyze-resume/{resume_id}",
        headers=auth_user_a["headers"],
    )

    assert response.status_code == 404
    assert "error" in response.json


def test_analysis_ownership_cross_contamination(client, auth_user_a, auth_user_b):
    job_a = JobApplication(company_name="UserA-Corp", job_title="Dev", work_location="Hybrid", user_id=auth_user_a["user_id"])
    resume_a = Resume(original_file="a.pdf", storage_key="a.pdf", resume_name="A_resume", m_type="application/pdf", user_id=auth_user_a["user_id"])
    db.session.add_all([job_a, resume_a])
    db.session.commit()

    job_b = JobApplication(company_name="UserB-Corp", job_title="QA", work_location="Hybrid", user_id=auth_user_b["user_id"])
    resume_b = Resume(original_file="b.pdf", storage_key="b.pdf", resume_name="B_resume", m_type="application/pdf", user_id=auth_user_b["user_id"])
    db.session.add_all([job_b, resume_b])
    db.session.commit()

    compromise_payload = {
        "application_id": job_a.application_id,
        "resume_id": resume_b.resume_id,
        "job_description": "Require deep system auditing background."
    }

    response = client.post(f"/applications/"
        f"{job_a.application_id}"
        f"/analyze-resume/"
        f"{resume_b.resume_id}", json=compromise_payload, headers=auth_user_b["headers"])

    assert response.status_code == 404
    assert "error" in response.json
