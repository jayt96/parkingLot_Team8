import sqlite3

from payment import Payment
from account import Admin, Account
from enums import AccountStatus
from parking_lot import ParkingLot
from vehicle import Car, Truck, Motorcycle, Van, Handicapped

parking_lot = None

while True:
    admin_choice = 0

    choice = input("Enter login choice.\n"
                   "1 Sign in as admin. \n"
                   "2 Sign in as user. \n"
                   "3 Create new account \n"
                   "4 Exit\n"
                   "Your choice: ")
    try:
        choice = int(choice)
    except ValueError:
        print('Invalid choice type.')
        continue
    else:
        if choice == 1:
            admin_username = input("Enter admin username: ")
            admin_password = input("Enter admin password: ")
            admin = Admin(admin_username, admin_password)
            admin.login()

            while True:
                admin_choice = input("Admin Menu:\n"
                                     "1 Add Parking Lot\n"
                                     "2 Add Parking floor\n"
                                     "3 Set new name for the parking lot\n"
                                     "4 Get Parking Lot Information\n"
                                     "5 Exit to Main Menu\n"
                                     "Your choice: ")
                try:
                    admin_choice = int(admin_choice)
                except ValueError:
                    print('Invalid choice type.')
                    continue
                else:
                    if admin_choice == 1:
                        lot_name = input("Enter the name of the new parking lot: ")
                        parking_lot = ParkingLot(lot_name)
                        print(lot_name, "was created successfully")
                        continue
                    elif admin_choice == 2:
                        floor_name = input("Enter the name of the new parking floor: ")
                        parking_lot = Admin.add_parking_floor(parking_lot, floor_name)
                        print("Floor '" + floor_name + "' was added successfully")
                        continue
                    elif admin_choice == 3:
                        new_name = input("Enter the new name of the existing parking lot")
                        Admin.set_lot_name(parking_lot, new_name)
                        print("The parking lot was renamed to", new_name)
                        continue
                    elif admin_choice == 4:
                        print('Parking lot name:', parking_lot.name)
                        print('Parking lot floors:', parking_lot.parking_floors)
                        print('Tickets issued:', parking_lot.cnt)
                    elif admin_choice == 5:
                        break
                    else:
                        print("Invalid admin choice.")
                        continue
            if admin_choice == 5:
                continue

        elif choice == 2:
            if parking_lot is None:
                print('Parking lot has not been created yet. Wait until admin will add it')
                continue
            user_username = input("Enter username: ")
            user_password = input("Enter password: ")
            user = Account(user_username, user_password)
            user.login()
            while True:
                choice = input("Enter Parking choice.\n"
                               "1 Parking entry Gate.\n"
                               "2 Parking exit Gate.\n"
                               "3 Check parking status.\n"
                               "4 Check vehicle status.\n"
                               "5 Buy Subscription\n"
                               "6 Exit to the main menu\n"
                               "Your Choice: ")
                try:
                    choice = int(choice)
                except ValueError:
                    print('Invalid choice type.')
                else:
                    if choice == 1:
                        vehicle_type = input("Enter vehicle type. \n"
                                             "1 Car.\n"
                                             "2 Motorcycle, \n"
                                             "3 Truck.\n"
                                             "4 Van\n"
                                             "5 Handicapped\n"
                                             "Your choice: ")
                        try:
                            vehicle_type = int(vehicle_type)
                        except ValueError:
                            print('Invalid vehicle type.')
                        else:
                            if vehicle_type < 0 or vehicle_type > 5:
                                print('Invalid vehicle type.')
                            else:
                                vehicle_number = input("Enter vehicle Number: ")
                                if vehicle_type == 1:
                                    vehicle = Car(vehicle_number)
                                elif vehicle_type == 2:
                                    vehicle = Motorcycle(vehicle_number)
                                elif vehicle_type == 3:
                                    vehicle = Truck(vehicle_number)
                                elif vehicle_type == 4:
                                    vehicle = Van(vehicle_number)
                                elif vehicle_type == 5:
                                    vehicle = Handicapped(vehicle_number)
                                else:
                                    print("Error")
                                    continue
                                ticket_number = parking_lot.get_new_parking_ticket(vehicle, user.account_status)
                                print(f"Ticket number: {ticket_number}")
                                continue
                    elif choice == 2:
                        ticket_number = input("Enter ticket Number: ")
                        try:
                            ticket_number = int(ticket_number)
                        except ValueError:
                            print("Invalid ticket number.")
                            continue
                        else:
                            vehicle_number, parking_cost = parking_lot.leave_parking(ticket_number)
                            print(f"Vehicle Number: {vehicle_number}. Parking cost: {parking_cost}.")
                            continue
                    elif choice == 3:
                        parking_status = parking_lot.get_empty_spot_number()
                        print(parking_status)
                        continue
                    elif choice == 4:
                        ticket_number = input("Enter ticket Number: ")
                        try:
                            ticket_number = int(ticket_number)
                        except ValueError:
                            print("Invalid ticket number.")
                            continue
                        else:
                            vehicle_status = parking_lot.vehicle_status(ticket_number)
                            print(vehicle_status)
                            continue
                    elif choice == 5:
                        if user.account_status == AccountStatus.SUBSCRIBED:
                            print("You already subscribed")
                            continue
                        print("The payment will cost you around 50,000 KRW. Do you want to buy it?")
                        print("Type [Y] for Yes and [N] for No: ")
                        user_input = input()
                        if user_input.lower() == 'y':
                            amount_to_pay = 50000
                            Payment.make_payment(amount_to_pay, user)
                        else:
                            continue
                    elif choice == 6:
                        break
                    else:
                        print("Invalid admin choice.")
                        continue
                if choice == 6:
                    continue

        elif choice == 3:
            new_user_name = input("Enter a new username: ")
            new_password = input("Enter a new password: ")
            new_email = input("Enter a new email: ")

            conn = sqlite3.connect("AccountDB.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO accounts (login, password, accountType, emai) VALUES (?, ?, ?, ?)",
                           (new_user_name, new_password, 2, new_email))
            conn.commit()
            conn.close()

            print(f"New user account created with username: {new_user_name}")
            print("Please sign in again")
            continue

        elif choice == 4:
            exit()
        else:
            print("Invalid choice.")
            continue
