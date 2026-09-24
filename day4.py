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
