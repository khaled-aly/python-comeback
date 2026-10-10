import os
import pytest
import db
from models import Job


@pytest.fixture
def test_database(monkeypatch):
    database_url = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://khaledaly@localhost/job_tracker_test"
    )

    monkeypatch.setattr("db.DATABASE_URL", database_url)

    db.create_tables()

    yield

    with db.get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM jobs")

def test_create_job(test_database):
    job = Job(
        "Apple",
        70000,
        "London",
        True
    )

    db.create_job(job)

    jobs = db.get_jobs()

    assert len(jobs) == 1
    assert jobs[0].company == "Apple"
    assert jobs[0].salary == 70000
    assert jobs[0].location == "London"
    assert jobs[0].remote is True




def test_get_job_not_found(test_database):
    result = db.get_job(999)

    assert result is None

def test_get_job(test_database):
    job = Job(
        "Google",
        80000,
        "London",
        True
    )

    db.create_job(job)

    result = db.get_job(job.id)

    assert result is not None
    assert result.id == job.id
    assert result.company == "Google"
    assert result.salary == 80000


def test_update_job(test_database):
    job = Job(
        "Apple",
        70000,
        "London",
        True
    )

    db.create_job(job)

    db.update_job(job.id, 90000)

    result = db.get_job(job.id)

    assert result is not None
    assert result.salary == 90000


def test_delete_job(test_database):
    job = Job(
        "Apple",
        70000,
        "London",
        True
    )

    db.create_job(job)

    db.delete_job(job.id)

    result = db.get_job(job.id)

    assert result is None