
# discount.py

price = float(input("Enter original price: "))
discount_percent = float(input("Enter discount percentage: "))

discount = price * discount_percent / 100

final_price = price - discount

print(f"Original price: K{price:.2f}")
print(f"Discount: K{discount:.2f}")
print(f"Final price: K{final_price:.2f}")

