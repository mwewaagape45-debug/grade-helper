import sqlite3
from datetime import datetime

print("WELCOME TO AIRTEL MOBILE MONEY")

DB_FILE = "airtel.db"
conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row

logged_in_number = None


# ---------- Database setup ----------
def setup_database():
    """Create the tables and add the starting accounts."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            phone INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            pin INTEGER NOT NULL,
            balance REAL NOT NULL CHECK (balance >= 0)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender INTEGER NOT NULL,
            receiver INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (sender) REFERENCES accounts(phone),
            FOREIGN KEY (receiver) REFERENCES accounts(phone)
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM accounts"
    ).fetchone()[0]

    if count == 0:
        conn.executemany(
            """INSERT INTO accounts
            (phone, name, pin, balance)
            VALUES (?, ?, ?, ?)""",
            [
                (970337157, "Gift Muleya", 1010, 500.00),
                (966123456, "Jane Banda", 2020, 300.00),
                (977654321, "John Phiri", 3030, 150.00),
            ],
        )

    conn.commit()


# ---------- Helper functions ----------
def get_account(phone):
    """Find an account using its phone number."""
    return conn.execute(
        "SELECT * FROM accounts WHERE phone = ?",
        (phone,)
    ).fetchone()


def read_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None


def read_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
        return None


# ---------- Login ----------
def login():
    global logged_in_number

    number = read_int("Enter your phone number: ")
    pin = read_int("Enter your pin: ")

    if number is None or pin is None:
        return False

    acc = get_account(number)

    if acc is not None and acc["pin"] == pin:
        logged_in_number = number
        print(f"\nAccess Granted. Welcome, {acc['name']}!")
        return True

    print("Access Denied: wrong phone number or pin.")
    return False


# ---------- View balance ----------
def view_balance():
    acc = get_account(logged_in_number)
    print(f"Your balance is: {acc['balance']:.2f}")


# ---------- Send money ----------
def send_money():
    destination = read_int("Enter destination phone number: ")

    if destination is None:
        return

    dest_acc = get_account(destination)

    if dest_acc is None:
        print("That account does not exist.")
        return

    if destination == logged_in_number:
        print("You cannot send money to your own account.")
        return

    amount = read_amount("Enter amount to send: ")

    if amount is None:
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    sender = get_account(logged_in_number)

    if amount > sender["balance"]:
        print("Insufficient balance.")
        return

    try:
        with conn:
            conn.execute(
                """UPDATE accounts
                SET balance = balance - ?
                WHERE phone = ?""",
                (amount, logged_in_number),
            )

            conn.execute(
                """UPDATE accounts
                SET balance = balance + ?
                WHERE phone = ?""",
                (amount, destination),
            )

            cur = conn.execute(
                """INSERT INTO transactions
                (sender, receiver, amount, status, timestamp)
                VALUES (?, ?, ?, 'completed', ?)""",
                (
                    logged_in_number,
                    destination,
                    amount,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )

            txn_id = cur.lastrowid

    except sqlite3.Error as e:
        print(f"Transaction failed. No money was moved. ({e})")
        return

    new_balance = get_account(logged_in_number)["balance"]

    print(f"Debited {amount:.2f} from your account.")
    print(f"Credited {amount:.2f} to {dest_acc['name']} ({destination}).")
    print(f"Transaction ID: {txn_id}")
    print(f"Your new balance: {new_balance:.2f}")


# ---------- Deposit money ----------
def deposit_money():
    amount = read_amount("Enter amount to deposit: ")

    if amount is None:
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    with conn:
        conn.execute(
            """UPDATE accounts
            SET balance = balance + ?
            WHERE phone = ?""",
            (amount, logged_in_number),
        )

    new_balance = get_account(logged_in_number)["balance"]

    print(
        f"Deposited {amount:.2f}. "
        f"New balance: {new_balance:.2f}"
    )


# ---------- Transaction history ----------
def transaction_history():
    rows = conn.execute(
        """SELECT * FROM transactions
        WHERE sender = ? OR receiver = ?
        ORDER BY id""",
        (logged_in_number, logged_in_number),
    ).fetchall()

    if not rows:
        print("No transactions yet.")
        return

    print("\n--- Transaction History ---")

    for t in rows:
        if t["sender"] == logged_in_number:
            print(
                f"ID {t['id']}: Sent {t['amount']:.2f} "
                f"to {t['receiver']} [{t['status']}] "
                f"{t['timestamp']}"
            )
        else:
            print(
                f"ID {t['id']}: Received {t['amount']:.2f} "
                f"from {t['sender']} [{t['status']}] "
                f"{t['timestamp']}"
            )


# ---------- Reverse transaction ----------
def reverse_transaction():
    txn_id = read_int("Enter transaction ID to reverse: ")

    if txn_id is None:
        return

    txn = conn.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (txn_id,)
    ).fetchone()

    if txn is None:
        print("Transaction not found.")
        return

    if txn["status"] == "reversed":
        print("This transaction has already been reversed.")
        return

    if txn["sender"] != logged_in_number:
        print("You can only reverse transactions you sent.")
        return

    receiver = get_account(txn["receiver"])

    if receiver["balance"] < txn["amount"]:
        print(
            "Cannot reverse: the receiver no longer has "
            "enough balance."
        )
        return

    with conn:
        conn.execute(
            """UPDATE accounts
            SET balance = balance + ?
            WHERE phone = ?""",
            (txn["amount"], txn["sender"]),
        )

        conn.execute(
            """UPDATE accounts
            SET balance = balance - ?
            WHERE phone = ?""",
            (txn["amount"], txn["receiver"]),
        )

        conn.execute(
            """UPDATE transactions
            SET status = 'reversed'
            WHERE id = ?""",
            (txn_id,),
        )

    new_balance = get_account(logged_in_number)["balance"]

    print(
        f"Transaction {txn_id} reversed. "
        f"{txn['amount']:.2f} returned to your account."
    )

    print(f"Your new balance: {new_balance:.2f}")


# ---------- Change PIN ----------
def change_pin():
    acc = get_account(logged_in_number)

    old_pin = read_int("Enter current pin: ")

    if old_pin is None:
        return

    if old_pin != acc["pin"]:
        print("Incorrect current pin.")
        return

    new_pin = read_int("Enter new pin: ")

    if new_pin is None:
        return

    with conn:
        conn.execute(
            """UPDATE accounts
            SET pin = ?
            WHERE phone = ?""",
            (new_pin, logged_in_number),
        )

    print("Pin changed successfully.")


# ---------- Main menu ----------
def main_menu():
    while True:
        print("\n1. View Balance")
        print("2. Send Money")
        print("3. Deposit Money")
        print("4. Transaction History")
        print("5. Reverse Transaction")
        print("6. Change Pin")
        print("7. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_balance()

        elif choice == "2":
            send_money()

        elif choice == "3":
            deposit_money()

        elif choice == "4":
            transaction_history()

        elif choice == "5":
            reverse_transaction()

        elif choice == "6":
            change_pin()

        elif choice == "7":
            print("Logged out.\n")
            break

        else:
            print("Invalid option.")


# ---------- Main program ----------
def main():
    setup_database()
    attempts = 3

    while attempts > 0:
        if login():
            main_menu()

            again = input(
                "Log in as another user? (y/n): "
            ).strip().lower()

            if again == "y":
                attempts = 3
                continue

            print("Goodbye!")
            break

        attempts -= 1
        print(f"{attempts} attempts remaining")

        if attempts == 0:
            print("No attempts left. Exiting.")
            break

    conn.close()


if __name__ == "__main__":
    main()
