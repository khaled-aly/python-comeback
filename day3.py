import json
file_path = 'jobs.json'
def load_json_file(file_path):
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

jobs_data = load_json_file(file_path)

print (jobs_data[0])

for job in jobs_data:
    print(job['company'])

high_salary_jobs = [job for job in jobs_data if job['salary'] > 65000]

remote_jobs = [job for job in jobs_data if job['remote'] == True and job['location'] == 'London' and job['salary'] >= 60000]


company_location = {job["company"]: job["location"] for job in jobs_data}

def find_jobs(jobs, minimum_salary, location):
    list_of_jobs = [job["company"] for job in jobs if job["salary"] >= minimum_salary and job["location"] == location and job["remote"]]
    return list_of_jobs
print(find_jobs(jobs_data, 60000, "London"))