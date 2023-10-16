import sqlite3
from enums import AccountStatus
from parking_lot import ParkingLot

db = sqlite3.connect('AccountDB.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS accounts(
    login TEXT,
    password TEXT,
    email TEXT,
    phone TEXT,
    accountType INTEGER
    )""")

db.commit()
db.close()

conn = sqlite3.connect("AccountDB.db")
cursor = conn.cursor()


class Account:
    def __init__(self, user_name, password, status=AccountStatus.ACTIVE):
        self.__user_name = user_name
        self.__password = password
        self.account_status = status

    def reset_password(self, new_pass):
        self.__password = new_pass

    def login(self):
        while True:
            cursor.execute("SELECT accountType FROM accounts WHERE login = ? AND password = ?",
                           (self.__user_name, self.__password))
            row = cursor.fetchone()
            if row:
                account_status = row[0]
                self.account_status = AccountStatus(account_status)
                break
            else:
                print("Login failed. Please try again or type 'exit' to exit.")
                user_input = input("Enter 'username:password': ")
                if user_input.lower() == 'exit':
                    exit()
                parts = user_input.split(":")
                if len(parts) == 2:
                    self.__user_name, self.__password = parts[0], parts[1]


class Admin(Account):
    def __init__(self, user_name, password):
        super().__init__(user_name, password)

    def login(self):
        while True:
            super().login()
            if self.account_status == AccountStatus.ADMIN:
                print("Admin login successful.")
                break
            else:
                print("Admin login failed. Please try again or type 'exit' to exit.")
                user_login_input = input("Enter your username or 'exit' in order to exit")
                if user_login_input.lower() == 'exit':
                    exit()
                else:
                    user_pass_input = input("Enter your password")

                self.__user_name = user_login_input
                self.__password = user_pass_input

    @staticmethod
    def add_parking_lot(name):
        parking_lot = ParkingLot(name)
        return parking_lot

    @staticmethod
    def add_parking_floor(parking_lot, floor_name):
        parking_lot.parking_floors.append(
            {'name': floor_name})
        print(f"Added a new parking floor: {floor_name}")
        parking_lot.floor_count += 1
        parking_lot.update_max_capacity()
        return parking_lot

    @staticmethod
    def set_lot_name(parking_lot, new_name):
        parking_lot.name = new_name
        print(f"Parking lot name changed to {new_name}")
