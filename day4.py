jobs = ["Apple", "Meta", "Google"]
try:
    number = int(input("enter job num: "))
    selected_job = jobs[number]
except ValueError:
    print("please enter a number")
except IndexError:
    print("please enter a number between 0 and 2")
else:
    print (selected_job)
finally:
    print ("program finished")

def calculate_salary(salary):
    if salary < 0:
        raise ValueError("Salary cannot be negative")
    return salary

def add_job(jobs, company, salary):
    if salary < 0:
        raise ValueError("Salary cannot be negative")

    new_job = {
        "company": company,
        "salary": salary
    }
    jobs.append(new_job)
    return jobs
