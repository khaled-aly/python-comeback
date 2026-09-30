import pytest
from models import Job
from storage import save_jobs, load_jobs

@pytest.fixture
def jobs_file(tmp_path):
    return tmp_path / "jobs.json"

def test_save_and_load_jobs(jobs_file):

    jobs = [
        Job("Apple", 65000, "London", True),
        Job("Meta", 70000, "London", False)
    ]

    save_jobs(jobs, jobs_file)

    loaded_jobs = load_jobs(jobs_file)

    assert len(loaded_jobs) == 2
    assert loaded_jobs[0].company == "Apple"
    assert loaded_jobs[0].salary == 65000
    assert loaded_jobs[1].company == "Meta"

def test_load_jobs_when_file_does_not_exist(jobs_file):

    jobs = load_jobs(jobs_file)

    assert jobs == []

def test_save_empty_jobs(jobs_file):

    save_jobs([], jobs_file)

    jobs = load_jobs(jobs_file)

    assert jobs == []