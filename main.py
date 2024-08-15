from models import User, Car, Rental
from database import Database
import bcrypt

def main():
    print("Starting the program...")
    db = Database()
    User.add_admin(db)
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            User.register_user(db)
        elif choice == '2':
            user = User.login_user(db)
            if user:
                if user[4] == 'admin':
                    print("Admin logged in.\n\n")
                    while True:
                        print("\n1. Add Car\n2. View Cars\n3. Update Car\n4. Delete Car\n5. Manage Rental Bookings\n6. Exit")
                        choice = input("Enter choice: ")
                        if choice == '1':
                            Car.add_car(db)
                        elif choice == '2':
                            Car.view_cars(db)
                        elif choice == '3':
                            Car.update_car(db)
                        elif choice == '4':
                            Car.delete_car(db)
                        elif choice == '5':
                            Rental.manage_rental_bookings(db)
                        elif choice == '6':
                            print("Exiting")
                            db.close()
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    while True:
                        print("\n1. View Cars\n2. Book Car\n3. Exit")
                        choice = input("Enter choice: ")
                        if choice == '1':
                            Car.view_cars(db)
                        elif choice == '2':
                            Rental.book_car(db, user[0])  # Pass user ID to book_car
                        elif choice == '3':
                            print("Exiting")
                            db.close()
                            break
                        else:
                            print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting program...")
            db.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
