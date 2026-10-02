from fastapi import FastAPI
from models import Job
from storage import load_jobs, save_jobs
from pydantic import BaseModel

app = FastAPI()

class JobResponse(BaseModel):
    company: str
    salary: int
    location: str
    remote: bool

class JobCreate(BaseModel):
    company: str
    salary: int
    location: str
    remote: bool

def get_jobs_from_storage():
    return load_jobs()

def save_jobs_to_storage(jobs):
    save_jobs(jobs)

@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate):
    new_job = Job(
        company=job.company,
        salary=job.salary,
        location=job.location,
        remote=job.remote
    )
    jobs = get_jobs_from_storage()
    jobs.append(new_job)
    save_jobs_to_storage(jobs)
    return new_job

@app.get("/jobs", response_model=list[JobResponse])
def get_jobs():
    jobs = get_jobs_from_storage()

    return jobs

@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}
