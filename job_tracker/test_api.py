from fastapi.testclient import TestClient

from api import app
from models import Job


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

    def fake_create_job(job):
        job.id = 123
        test_jobs.append(job)
        return job

    monkeypatch.setattr(
        "api.db_create_job",
        fake_create_job
    )

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
    assert data["id"] == 123
    assert data["company"] == "Test Company"
    assert data["salary"] == 60000
    assert data["location"] == "London"
    assert data["remote"] is True

    assert len(test_jobs) == 1
    assert test_jobs[0].company == "Test Company"


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


def test_get_single_job(monkeypatch):
    test_job = Job(
        "Apple",
        72000,
        "London",
        True,
        job_id=5
    )

    def fake_get_job(job_id):
        return test_job

    monkeypatch.setattr(
        "api.get_job",
        fake_get_job
    )

    response = client.get("/jobs/5")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 5
    assert data["company"] == "Apple"
    assert data["salary"] == 72000
    assert data["location"] == "London"
    assert data["remote"] is True


def test_get_single_job_not_found(monkeypatch):
    def fake_get_job(job_id):
        return None

    monkeypatch.setattr(
        "api.get_job",
        fake_get_job
    )

    response = client.get("/jobs/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }


def test_delete_job(monkeypatch):
    deleted_ids = []

    def fake_get_job(job_id):
        return Job(
            "Apple",
            72000,
            "London",
            True
        )

    def fake_delete_job(job_id):
        deleted_ids.append(job_id)

    monkeypatch.setattr(
        "api.get_job",
        fake_get_job
    )

    monkeypatch.setattr(
        "api.db_delete_job",
        fake_delete_job
    )

    response = client.delete("/jobs/5")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Job deleted successfully"
    }

    assert deleted_ids == [5]


def test_delete_job_not_found(monkeypatch):
    def fake_get_job(job_id):
        return None

    monkeypatch.setattr(
        "api.get_job",
        fake_get_job
    )

    response = client.delete("/jobs/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Job not found"
    }

def test_update_job(monkeypatch):
   
    updated_job = Job(
        "Apple",
        90000,
        "London",
        True,
        job_id=5
    )

    def fake_get_job(job_id):
        return updated_job

    updated_ids = []

    def fake_update_job(job_id, salary):
        updated_ids.append((job_id, salary))

    monkeypatch.setattr(
        "api.get_job",
        fake_get_job
    )

    monkeypatch.setattr(
        "api.db_update_job",
        fake_update_job
    )

    response = client.put(
        "/jobs/5?salary=90000"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 5
    assert data["company"] == "Apple"
    assert data["salary"] == 90000
    assert data["location"] == "London"
    assert data["remote"] is True

    assert updated_ids == [(5, 90000)]

def test_search_jobs(monkeypatch):
    test_jobs = [
        Job(
            "Apple",
            72000,
            "London",
            True,
            job_id=5
        ),
        Job(
            "Google",
            80000,
            "London",
            True,
            job_id=6
        )
    ]

    def fake_search_jobs(minimum_salary, location, remote):
        assert minimum_salary == 70000
        assert location == "London"
        assert remote is True

        return test_jobs

    monkeypatch.setattr(
        "api.db_search_jobs",
        fake_search_jobs
    )

    response = client.get(
        "/jobs/search"
        "?minimum_salary=70000"
        "&location=London"
        "&remote=true"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 5
    assert data[0]["company"] == "Apple"
    assert data[1]["id"] == 6
    assert data[1]["company"] == "Google"

def test_search_jobs_invalid_salary():
    response = client.get(
        "/jobs/search"
        "?minimum_salary=hello"
        "&location=London"
        "&remote=true"
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "int_parsing"
    assert data["detail"][0]["loc"] == [
        "query",
        "minimum_salary"
    ]