
# grade_helper.py

mark = float(input("Enter your mark: "))

if mark >= 50 and mark <= 100:
    result = "Pass"
elif mark >= 0 and mark < 50:
    result = "Fail"
else:
    result = "Invalid mark"

print(f"Result: {result}")

