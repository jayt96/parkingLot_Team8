import sqlite3

from enums import AccountStatus


class Payment:
    @staticmethod
    def make_payment(amount, account):
        print(f"Charge amount: {amount}")

        while True:
            try:
                payment_input = float(input("Enter the payment amount: "))
            except ValueError:
                print("Invalid input. Please enter a valid payment amount.")
                continue
            if payment_input > amount:
                print("Payment successful. Change: {:.2f}".format(payment_input - amount))
                account.account_status = AccountStatus.SUBSCRIBED
                conn = sqlite3.connect("AccountDB.db")
                cursor = conn.cursor()
                cursor.execute(f"UPDATE accounts SET accountType = 4 WHERE login = '{account.login}'")
                break
            elif payment_input == amount:
                print("Payment successful. No change.")
                account.account_status = AccountStatus.SUBSCRIBED
                conn = sqlite3.connect("AccountDB.db")
                cursor = conn.cursor()
                cursor.execute(f"UPDATE accounts SET accountType = 4 WHERE login = '{account.login}'")
                conn.commit()
                break
            else:
                print("Payment amount is less than the charge. Your account is now BLOCKED.\n")
                print("In order to unblock your account contact: fakeadmin@admin.com")
                account.account_status = AccountStatus.BLOCKED
                conn = sqlite3.connect("AccountDB.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE accounts SET account_status = ? WHERE login = ?",
                               (account.account_status.value, account.login))
                conn.commit()
                conn.close()
                break
