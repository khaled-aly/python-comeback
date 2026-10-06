import psycopg

from config import DATABASE_URL
from models import Job

def get_connection():
    return psycopg.connect(DATABASE_URL)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            company TEXT NOT NULL,
            salary INTEGER NOT NULL,
            location TEXT NOT NULL,
            remote BOOLEAN NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def get_job(job_id: int) -> Job | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, company, salary, location, remote
                FROM jobs
                WHERE id = %s
            """, (job_id,))

            row = cursor.fetchone()

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
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO jobs (company, salary, location, remote)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            job.company,
            job.salary,
            job.location,
            job.remote
        ))

        job.id = cursor.fetchone()[0]

    return job

def get_jobs() -> list[Job]:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, company, salary, location, remote
            FROM jobs
        """)

        rows = cursor.fetchall()

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
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE jobs
            SET salary = %s
            WHERE id = %s
        """, (salary, job_id))

def delete_job(job_id: int):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM jobs
            WHERE id = %s
        """, (job_id,))

def search_jobs(minimum_salary: int, location: str, remote: bool) -> list[Job]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, company, salary, location, remote
        FROM jobs
        WHERE salary >= %s AND location = %s AND remote = %s
    """, (minimum_salary, location, remote))

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

