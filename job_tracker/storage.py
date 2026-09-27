import json
from pathlib import Path
from models import Job

BASE_DIR = Path(__file__).resolve().parent
JOBS_FILE = BASE_DIR / "jobs.json"


def save_jobs(jobs: list[Job]) -> None:
    job_data = [job.to_dict() for job in jobs]

    with open(JOBS_FILE, "w") as file:
        json.dump(job_data, file, indent=4)


def load_jobs() -> list[Job]:
    try:
        with open(JOBS_FILE, "r") as file:
            data = json.load(file)

        jobs: list[Job] = []

        for job_data in data:
            job = Job.from_dict(job_data)
            jobs.append(job)

        return jobs

    except FileNotFoundError:
        return []