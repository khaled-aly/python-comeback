import pytest

from db import (
    create_tables,
    create_job,
    get_jobs,
    get_job,
    update_job,
    delete_job
)
from models import Job


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test_jobs.db"

    monkeypatch.setattr(
        "db.DATABASE",
        str(database_path)
    )

    create_tables()

    return database_path


def test_create_job(test_database):
    job = Job(
        "Apple",
        70000,
        "London",
        True
    )

    create_job(job)

    jobs = get_jobs()

    assert len(jobs) == 1
    assert jobs[0].company == "Apple"
    assert jobs[0].salary == 70000
    assert jobs[0].location == "London"
    assert jobs[0].remote is True


def test_get_job(test_database):
    job = Job(
        "Google",
        80000,
        "London",
        True
    )

    create_job(job)

    jobs = get_jobs()
    job_id = 1

    result = get_job(job_id)

    assert result is not None
    assert result.id == 1
    assert result.company == "Google"
    assert result.salary == 80000


def test_get_job_not_found(test_database):
    result = get_job(999)

    assert result is None


def test_update_job(test_database):
    job = Job(
        "Apple",
        70000,
        "London",
        True
    )

    create_job(job)

    update_job(1, 90000)

    result = get_job(1)

    assert result is not None
    assert result.salary == 90000


def test_delete_job(test_database):
    job = Job(
        "Apple",
        70000,
        "London",
        True
    )

    create_job(job)

    delete_job(1)

    result = get_job(1)

    assert result is None