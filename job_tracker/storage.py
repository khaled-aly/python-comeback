import json
from pathlib import Path
from models import Job

BASE_DIR = Path(__file__).resolve().parent
JOBS_FILE = BASE_DIR / "jobs.json"


def save_jobs(
    jobs: list[Job],
    file_path: Path = JOBS_FILE
) -> None:
    job_data = [job.to_dict() for job in jobs]

    with open(file_path, "w") as file:
        json.dump(job_data, file, indent=4)


def load_jobs(
    file_path: Path = JOBS_FILE
) -> list[Job]:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        jobs: list[Job] = []

        for job_data in data:
            job = Job.from_dict(job_data)
            jobs.append(job)

        return jobs

    except FileNotFoundError:
        return []