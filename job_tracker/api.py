from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import Job
from db import (
    create_tables,
    get_jobs as db_get_jobs,
    get_job,
    create_job as db_create_job,
    update_job as db_update_job,
    delete_job as db_delete_job,
    search_jobs as db_search_jobs
)

app = FastAPI()

create_tables()

class JobResponse(BaseModel):
    id: int
    company: str
    salary: int
    location: str
    remote: bool


class JobCreate(BaseModel):
    company: str
    salary: int
    location: str
    remote: bool


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}


@app.get("/jobs", response_model=list[JobResponse])
def get_all_jobs():
    return db_get_jobs()

@app.get("/jobs/search", response_model=list[JobResponse])
def search_jobs(
    minimum_salary: int,
    location: str,
    remote: bool
):
    return db_search_jobs(minimum_salary, location, remote)

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_single_job(job_id: int):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job_salary(job_id: int, salary: int):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db_update_job(job_id, salary)

    return get_job(job_id)

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db_delete_job(job_id)

    return {
        "message": "Job deleted successfully"
    }

@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate):
    new_job = Job(
        company=job.company,
        salary=job.salary,
        location=job.location,
        remote=job.remote
    )
    return db_create_job(new_job)

