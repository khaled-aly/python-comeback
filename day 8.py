jobs = ["Apple", "Meta", "Google"]
salaries = [55000, 55555, 90000]
for i, job in enumerate(jobs, start=1):
    print(i, job)

for s,c in zip(jobs, salaries):
    print(s,c)

