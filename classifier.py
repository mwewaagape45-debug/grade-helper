
# grade_classifier.py

score = int(input("Enter score (0-100): "))

if score < 0 or score > 100:
    print("Invalid score")

elif score >= 80:
    print("Grade: Distinction")

elif score >= 70:
    print("Grade: Merit")

elif score >= 60:
    print("Grade: Credit")

elif score >= 50:
    print("Grade: Pass")

else:
    print("Grade: Fail")

