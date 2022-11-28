import time

course = "Software engineering"
group = "group3"
project_name = "Pet^2 dont cry"

print("Course: " + course)
print("Loading", end = "")
for i in range(10):
    print(".", end = '', flush = True)
    time.sleep(0.5)
print("done")
print("Hello " + group)
print("Our project name is: " + project_name)
for i in range(30):
    print("-", end = '', flush = True)
    time.sleep(0.1)