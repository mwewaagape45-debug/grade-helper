
# menu.py

names = []

while True:

    print("\n----- MAIN MENU -----")
    print("1. Add a name")
    print("2. View names")
    print("q. Quit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter name: ")
        names.append(name)
        print("Name added successfully!")

    elif choice == "2":
        if len(names) > 0:
            print("Saved names:")
            for name in names:
                print(name)
        else:
            print("No names have been saved.")

    elif choice == "q":
        print("Thank you for using the program.")
        break

    else:
        print("Invalid option. Please try again.")

