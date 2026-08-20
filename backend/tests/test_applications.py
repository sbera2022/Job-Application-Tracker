import pytest

def test_create_and_retrieve_all_applications(client, auth_user_a):
    payload = {
        "company_name": "Stripe",
        "job_title": "Backend Engineer",
        "work_location": "Remote",
        "status": "Applied",
    }

    create_res = client.post(
        "/applications",
        json=payload,
        headers=auth_user_a["headers"],
    )

    assert create_res.status_code == 201
    assert "application_id" in create_res.json

    get_res = client.get(
        "/applications",
        headers=auth_user_a["headers"],
    )

    assert get_res.status_code == 200
    assert len(get_res.json) == 1
    assert get_res.json[0]["company_name"] == "Stripe"


def test_retrieve_single_application(client, auth_user_a):
    payload = {"company_name": "Netflix", "work_location": "On-site", "job_title": "Senior UI Developer"}
    create_res = client.post('/applications', json=payload, headers=auth_user_a["headers"])
    assert create_res.status_code == 201, create_res.json
    job_id = create_res.json["application_id"]

    response = client.get(f'/applications/{job_id}', headers=auth_user_a["headers"])
    assert response.status_code == 200
    assert response.json["company_name"] == "Netflix"

def test_update_application(client, auth_user_a):
    create_res = client.post('/applications', json={"company_name": "Apple", "work_location": "Hybrid", "job_title": "Intern"}, headers=auth_user_a["headers"])
    job_id = create_res.json["application_id"]

    update_payload = {"company_name": "Apple", "job_title": "Full Time Engineer", "status": "Interview"}
    update_res = client.patch(f'/applications/{job_id}', json=update_payload, headers=auth_user_a["headers"])
    assert update_res.status_code == 200


    get_res = client.get(f'/applications/{job_id}', headers=auth_user_a["headers"])
    assert get_res.json["job_title"] == "Full Time Engineer"
    assert get_res.json["status"] == "Interview"


def test_delete_application(client, auth_user_a):
    create_res = client.post('/applications', json={"company_name": "Meta", "work_location": "On-site", "job_title": "Production Eng"}, headers=auth_user_a["headers"])
    job_id = create_res.json["application_id"]

    delete_res = client.delete(f'/applications/{job_id}', headers=auth_user_a["headers"])
    assert delete_res.status_code == 200

    get_res = client.get(f'/applications/{job_id}', headers=auth_user_a["headers"])
    assert get_res.status_code == 404


def test_tenant_isolation_security(client, auth_user_a, auth_user_b):
    payload = {"company_name": "Secret Corp", "job_title": "CEO", "work_location": "Remote"}
    create_res = client.post('/applications', json=payload, headers=auth_user_a["headers"])
    user_a_job_id = create_res.json["application_id"]

    user_b_list = client.get('/applications', headers=auth_user_b["headers"])
    assert user_b_list.status_code == 200
    assert len(user_b_list.json) == 0

    unauthorized_get = client.get(f'/applications/{user_a_job_id}', headers=auth_user_b["headers"])
    assert unauthorized_get.status_code == 404

    unauthorized_patch = client.patch(f"/applications/{user_a_job_id}", json={"company_name": "Hacked",},
        headers=auth_user_b["headers"],
    )
    assert unauthorized_patch.status_code == 404

    unauthorized_delete = client.delete(f'/applications/{user_a_job_id}', headers=auth_user_b["headers"])
    assert unauthorized_delete.status_code == 200


