from models import Job
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "jobs.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            salary INTEGER NOT NULL,
            location TEXT NOT NULL,
            remote BOOLEAN NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def get_job(job_id: int) -> Job | None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, company, salary, location, remote
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return Job(
        company=row[1],
        salary=row[2],
        location=row[3],
        remote=bool(row[4]),
        job_id=row[0]
    )

def create_job(job: Job) -> Job:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO jobs (company, salary, location, remote)
        VALUES (?, ?, ?, ?)
    """, (
        job.company,
        job.salary,
        job.location,
        job.remote
    ))

    connection.commit()

    job.id = cursor.lastrowid

    connection.close()

    return job

def get_jobs() -> list[Job]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, company, salary, location, remote
        FROM jobs
    """)

    rows = cursor.fetchall()

    connection.close()

    jobs = []

    for row in rows:
        job = Job(
            company=row[1],
            salary=row[2],
            location=row[3],
            remote=bool(row[4]),
            job_id=row[0]
        )
        jobs.append(job)

    return jobs
def update_job(job_id: int, salary: int):
    connection=get_connection()
    cursor= connection.cursor()

    cursor.execute("""
        UPDATE jobs
        SET salary = ?
        WHERE id = ?
        """, (salary, job_id))

    connection.commit()
    connection.close()

def delete_job(job_id:int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM jobs
        WHERE id = ?
    """, (job_id,))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    
    job = get_job(5)

    print(job)
""""
    new_job = Job(
        "Microsoft",
        75000,
        "London",
        True
    )

    create_job(new_job)

    jobs = get_jobs()

    for job in jobs:
        print(job)

    create_job(
        "Google",
        80000,
        "London",
        True
    )"""
