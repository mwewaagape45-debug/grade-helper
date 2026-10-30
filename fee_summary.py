
# fee_summary.py

name = input("Enter student name: ")
programme = input("Enter programme: ")

total_fees = float(input("Enter total fees: K"))
amount_paid = float(input("Enter amount paid: K"))

balance = total_fees - amount_paid

print("\n----- STUDENT FEE REPORT -----")

print(f"Student name: {name}")
print(f"Programme: {programme}")
print(f"Total fees: K{total_fees:.2f}")
print(f"Amount paid: K{amount_paid:.2f}")
print(f"Outstanding balance: K{balance:.2f}")

print("------------------------------")

