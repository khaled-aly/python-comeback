
class Job:
    def __init__(self, company, salary, location, remote=False):
        self.company = company
        self.salary = salary
        self.location = location
        self.remote = remote

    def is_remote(self):
        return self.remote

    def is_suitable(self, minimum_salary, location):
        return self.salary>=minimum_salary and self.location == location and self.remote
    
    def __str__(self):
        return f"{self.company} | {self.salary} | {self.location}"


job1 = Job("Apple", 65000, "London", remote=True)
job2 = Job("Meta", 70000, "San Francisco", remote=False)
job3 = Job("Yoto", 55000, "London", remote= True)

jobs = [job1, job2, job3]
for job in jobs:
    if job.is_suitable(60000, "London"):
        print(job.company)



print (job1)
print (job2)
print (job3)