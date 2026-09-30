from models import Job
import pytest

@pytest.fixture
def apple_job():
    return Job("Apple", 65000, "London", True)

def test_job_creation(apple_job):

    assert apple_job.company == "Apple"
    assert apple_job.salary == 65000
    assert apple_job.location == "London"
    assert apple_job.remote is True

def test_job_is_suitable(apple_job):

    assert apple_job.is_suitable(60000, "London", True) is True

def test_job_not_suitable_salary(apple_job):

    assert apple_job.is_suitable(70000, "London", True) is False

def test_job_not_suitable_location(apple_job):

    assert apple_job.is_suitable(60000, "Liverpool", True) is False

def test_job_not_suitable_remote(apple_job):

    assert apple_job.is_suitable(60000, "London", False) is False

def test_job_to_dict(apple_job):

    result = apple_job.to_dict()

    assert result == {
        "company": "Apple",
        "salary": 65000,
        "location": "London",
        "remote": True
    }

def test_job_from_dict():
    data = {
        "company": "Apple",
        "salary": 65000,
        "location": "London",
        "remote": True
    }

    job = Job.from_dict(data)

    assert job.company == "Apple"
    assert job.salary == 65000
    assert job.location == "London"
    assert job.remote is True