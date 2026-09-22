jobs = [
    {"company": "Apple", "salary": 65000},
    {"company": "Meta", "salary": 80000},
    {"company": "Startup", "salary": 55000},
    {"company": "Google", "salary": 75000}
]

highest_salary = 0
lowest_salary = 100000000
total_salary = 0

for job in jobs:
    total_salary += job["salary"]

    if job["salary"] > highest_salary:
        highest_salary = job["salary"]
        highest_company = job["company"]

    if job["salary"] < lowest_salary:
        lowest_salary = job["salary"]

print("Average:", total_salary / len(jobs))
print("High salary:", highest_salary)
print("Low salary:", lowest_salary)
print("Highest paying:", highest_company)
print("Number:", len(jobs))