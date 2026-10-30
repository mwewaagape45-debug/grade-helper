
# app.py

number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))
operator = input("Enter operator (+, -, *, /): ")

if operator == "+":
    answer = number1 + number2

elif operator == "-":
    answer = number1 - number2

elif operator == "*":
    answer = number1 * number2

elif operator == "/":
    if number2 != 0:
        answer = number1 / number2
    else:
        answer = None
        print("Cannot divide by zero")

else:
    answer = None
    print("Invalid operator")

if answer is not None:
    print(f"First number: {number1}")
    print(f"Second number: {number2}")
    print(f"Answer: {answer}")

