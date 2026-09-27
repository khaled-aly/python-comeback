from models import Job
from storage import save_jobs, load_jobs

def get_remote_choice() -> bool:
    while True:
        remote_input = input("Is this job remote True/False:").lower()

        if remote_input == "true":
            return True
        elif remote_input == "false":
            return False
        else:
            print("Please enter True or False")

def get_salary() -> int:
    while True:
        try:
            salary = int(input("enter salary : "))
            return salary
        except ValueError:
            print("Invalid Salary. please enter a number. ")

    
def get_job_details() -> Job:
    company = input("enter company name: ")
    salary = get_salary()

    location = input("enter company location: ")

    remote = get_remote_choice()

    return Job(company, salary, location, remote)


jobs = load_jobs()

for job in jobs:
    print(job)

while True:
    print("1. Add job")
    print("2. View jobs")
    print("3. Find suitable jobs")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        new_job = get_job_details()
        jobs.append(new_job)
        save_jobs(jobs)

    elif choice == "2":
        if not jobs:
            print("No Jobs found.")
        else:
            for job in jobs:
                print(job)

    elif choice == "3":
        minimum_salary = get_salary()

        location = input("Location: ")

        remote = get_remote_choice()

        for job in jobs:
            if job.is_suitable(minimum_salary, location, remote):
                print(job)

    elif choice == "4":
        break