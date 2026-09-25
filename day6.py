
class Job:
    def __init__(self, company, salary, location, remote=False):
        self.company = company
        self.salary = salary
        self.location = location
        self.remote = remote
    def __str__(self):
        return f"{self.company} | {self.salary} | {self.location} | {self.remote}"
    def is_suitable(self, minimum_salary, location, remote):
        return self.salary >= minimum_salary and self.location == location and self.remote==remote

def get_job_details():
    company = input("enter company name: ")
    while True:
        try:
            salary = int(input("enter salary : "))
            break
        except ValueError:
            print("Invalid Salary. please enter a number. ")
    location = input("enter company location: ")

    while True:
        remote_input = input("is this job remote True/False: ").lower()
        if remote_input == "true":
            remote = True
            break
        elif remote_input == "false":
            remote = False
            break
        else:
            print("Please enter True or false")

    job = Job(company, salary, location, remote) 
    return job
jobs = []

while True:
    print("1. Add job")
    print("2. View jobs")
    print("3. Find suitable jobs")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        new_job = get_job_details()
        jobs.append(new_job)
    elif choice == "2":
        if not jobs:
            print("No Jobs found.")
        else:
            for job in jobs:
                print(job)
    elif choice == "3":
        minimum_salary = int(input("Minimum salary: "))
        location = input("Location: ")
        while True:
            remote_input = input("is this job remote True/False: ").lower()
            if remote_input == "true":
                remote = True
                break
            elif remote_input == "false":
                remote = False
                break
            else:
                print("Please enter True or false")
        for job in jobs:
            if job.is_suitable(minimum_salary, location, remote):
                print(job)
    elif choice == "4":
        break




