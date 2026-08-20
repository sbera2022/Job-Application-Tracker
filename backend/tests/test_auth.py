import pytest

def test_user_registration_and_login_flow(client):
    user_payload = {
        "email": "applicant@example.com",
        "password": "SecurePassword123",
        "first_name": "Test",
        "last_name": "User",
    }

    reg_response = client.post(
        "/auth/register",
        json=user_payload,
    )

    assert reg_response.status_code == 201
    assert reg_response.json["email"] == "applicant@example.com"

    login_response = client.post(
        "/auth/login",
        json={
            "email": "applicant@example.com",
            "password": "SecurePassword123",
        },
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json

    token = login_response.json["access_token"]

    protected_response = client.get(
        "/applications",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert protected_response.status_code == 200


def test_login_with_incorrect_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "CorrectPassword",
            "first_name": "Wrong",
            "last_name": "Pass",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "IncorrectPassword",
        },
    )

    assert response.status_code == 401
    assert "error" in response.json


def test_registration_duplicate_email(client):
    user_payload = {
        "email": "duplicate@example.com",
        "password": "Password1",
        "first_name": "Duplicate",
        "last_name": "User",
    }

    first_attempt = client.post(
        "/auth/register",
        json=user_payload,
    )

    assert first_attempt.status_code == 201

    second_attempt = client.post(
        "/auth/register",
        json=user_payload,
    )

    assert second_attempt.status_code in (400, 409)
    assert "error" in second_attempt.json


def test_protected_route_without_jwt(client):
    response = client.get('/applications')

    assert response.status_code == 401
    assert "msg" in response.json
