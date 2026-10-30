
# fuel_cost.py

distance = float(input("Enter distance in km: "))
rate = float(input("Enter cost per km: "))

cost = distance * rate

print(f"Distance: {distance} km")
print(f"Rate per km: K{rate:.2f}")
print(f"Total fuel cost: K{cost:.2f}")

