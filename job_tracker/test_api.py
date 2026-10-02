from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Tracker API is running"
    }

def test_get_jobs():
    response = client.get("/jobs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_job(monkeypatch):
    test_jobs = []

    def fake_load_jobs():
        return test_jobs

    def fake_save_jobs(jobs):
        test_jobs.clear()
        test_jobs.extend(jobs)

    monkeypatch.setattr("api.get_jobs_from_storage", fake_load_jobs)
    monkeypatch.setattr("api.save_jobs_to_storage", fake_save_jobs)

    response = client.post(
        "/jobs",
        json={
            "company": "Test Company",
            "salary": 60000,
            "location": "London",
            "remote": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Test Company"
    assert data["salary"] == 60000
    assert data["location"] == "London"
    assert data["remote"] is True

def test_create_job_invalid_salary():
    response = client.post(
        "/jobs",
        json={
            "company": "Test Company",
            "salary": "hello",
            "location": "London",
            "remote": True
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "int_parsing"
    assert data["detail"][0]["loc"] == ["body", "salary"]

def test_create_job_missing_remote():
    response = client.post(
        "/jobs",
        json={
            "company": "Test Company",
            "salary": 60000,
            "location": "London"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", "remote"]