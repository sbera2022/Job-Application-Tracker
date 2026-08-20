import pytest
import io

def test_upload_valid_pdf(client, auth_user_a, monkeypatch):
    monkeypatch.setattr(
        "app.routes.resumes.resume_parser.extract_resume_text",
        lambda file_path, ext: "Python Flask PostgreSQL",
    )

    data = {
        "file": (
            io.BytesIO(b"fake pdf bytes"),
            "cv.pdf",
        )
    }

    response = client.post(
        "/resumes",
        data=data,
        content_type="multipart/form-data",
        headers=auth_user_a["headers"],
    )

    assert response.status_code == 201
    assert response.json["resume"]["original_file"] == "cv.pdf"


def test_reject_unsupported_file_extensions(client, auth_user_a):
    invalid_data = {"file": (io.BytesIO(b"malicious payload"), "script.exe")}
    response = client.post('/resumes', data=invalid_data, content_type='multipart/form-data', headers=auth_user_a["headers"])

    assert response.status_code == 400
    assert "error" in response.json


def test_list_and_delete_resumes_flow(client, auth_user_a, monkeypatch):
    monkeypatch.setattr(
        "app.routes.resumes.resume_parser.extract_resume_text",
        lambda file_path, ext: "Parsed resume text",
    )

    file_payload = {
        "file": (
            io.BytesIO(b"resume content"),
            "primary_resume.pdf",
        )
    }

    upload_res = client.post(
        "/resumes",
        data=file_payload,
        content_type="multipart/form-data",
        headers=auth_user_a["headers"],
    )

    assert upload_res.status_code == 201, upload_res.json

    resume_id = upload_res.json["resume"]["id"]


def test_duplicate_filenames_generate_unique_uuids(client, auth_user_a, monkeypatch):
    monkeypatch.setattr(
        "app.routes.resumes.resume_parser.extract_resume_text",
        lambda file_path, ext: "Parsed resume text",
    )

    shared_payload = {
        "file": (
            io.BytesIO(b"content variant A"),
            "my_resume.pdf",
        )
    }

    shared_payload_2 = {
        "file": (
            io.BytesIO(b"content variant B"),
            "my_resume.pdf",
        )
    }

    res1 = client.post(
        "/resumes",
        data=shared_payload,
        content_type="multipart/form-data",
        headers=auth_user_a["headers"],
    )

    res2 = client.post(
        "/resumes",
        data=shared_payload_2,
        content_type="multipart/form-data",
        headers=auth_user_a["headers"],
    )

    assert res1.status_code == 201, res1.json
    assert res2.status_code == 201, res2.json

    storage_1 = res1.json["resume"]["storage_key"]
    storage_2 = res2.json["resume"]["storage_key"]

    assert storage_1 != storage_2
    assert storage_1.endswith(".pdf")
    assert storage_2.endswith(".pdf")


def test_resume_tenant_isolation_boundary(client, auth_user_a, auth_user_b, monkeypatch):
    monkeypatch.setattr(
        "app.routes.resumes.resume_parser.extract_resume_text",
        lambda file_path, ext: "Confidential resume text",
    )

    file_payload = {
        "file": (
            io.BytesIO(b"confidential"),
            "private_data.pdf",
        )
    }

    user_a_upload = client.post(
        "/resumes",
        data=file_payload,
        content_type="multipart/form-data",
        headers=auth_user_a["headers"],
    )

    assert user_a_upload.status_code == 201, user_a_upload.json

    user_a_resume_id = (
        user_a_upload.json["resume"]["id"]
    )

    user_b_list = client.get(
        "/resumes",
        headers=auth_user_b["headers"],
    )

    assert user_b_list.status_code == 200
    assert len(user_b_list.json) == 0

    malicious_delete = client.delete(
        f"/resumes/{user_a_resume_id}",
        headers=auth_user_b["headers"],
    )

    assert malicious_delete.status_code == 404

