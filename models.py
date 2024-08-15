import bcrypt
from database import Database
from abc import ABC, abstractmethod
from datetime import datetime

class UserFactory(ABC):
    @abstractmethod
    def create_user(self, username, email, password):
        pass

class AdminFactory(UserFactory):
    def create_user(self, username, email, password):
        return User(username, email, password, role='admin')

class CustomerFactory(UserFactory):
    def create_user(self, username, email, password):
        return User(username, email, password, role='customer')

class User:
    def __init__(self, username, email, password, role='customer'):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role
    
    def save(self, db):
        """Save the user to the database."""
        query = '''
            INSERT INTO users (username, email, password, role)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                username = VALUES(username),
                email = VALUES(email),
                password = VALUES(password),
                role = VALUES(role)
        '''
        params = (self.username, self.email, self.password, self.role)
        db.execute_query(query, params)

    def check_exists(self, db):
        """Check if the username or email already exists in the database."""
        query = '''
            SELECT 1 FROM users
            WHERE username = %s OR email = %s
        '''
        params = (self.username, self.email)
        result = db.fetch_one(query, params)
        return result is not None

    def add_admin(db):
        factory = AdminFactory()  # Create an instance of AdminFactory
        user = factory.create_user('admin', 'admin', 'admin')
        user.save(db)

    def register_user(db):
        factory = CustomerFactory()
        print("Registering a new user...")
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = factory.create_user(username, email, password)
        if user.check_exists(db):
            print("User Info Exist.")
        else:
            user.save(db)
            print("User registered successfully.")

    def login_user(db):
        print("Logging in...")
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        user = db.fetch_one('SELECT * FROM users WHERE email = %s', (email,))
        
        if user:
            hashed_password = user[3].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                print(f"Welcome, {user[1]}!")
                return user
        
        print("Invalid credentials.")
        return None




class Car:
    def __init__(self, make, model, year, mileage, daily_rate, min_rent_period, max_rent_period, available_now=True):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.daily_rate = daily_rate
        self.min_rent_period = min_rent_period
        self.max_rent_period = max_rent_period
        self.available_now = available_now


    def save(self, db):
        """Save the car to the database."""
        query = '''
            INSERT INTO cars (make, model, year, mileage, daily_rate, min_rent_period, max_rent_period, available_now)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (self.make, self.model, self.year, self.mileage, self.daily_rate, self.min_rent_period, self.max_rent_period, self.available_now)
        db.execute_query(query, params)

    def add_car(db):
        print("Adding a new car...")
        make = input("Enter car make: ")
        model = input("Enter car model: ")
    
        # Input validation for year
        while True:
            user_input = input("Enter car year: ")
            if user_input.isdigit():
                year = int(user_input)
                break
            else:
                print("Please enter a valid year (numeric).")
        
        # Input validation for mileage
        while True:
            user_input = input("Enter car mileage: ")
            if user_input.isdigit():
                mileage = int(user_input)
                break
            else:
                print("Please enter a valid mileage (numeric).")
        
        # Input for daily_rate
        while True:
            daily_rate_input = input("Enter car daily_rate: ")
            if daily_rate_input.isdigit():
                try:
                    daily_rate = float(daily_rate_input)
                    if daily_rate < 0:
                        raise ValueError("daily_rate cannot be negative.")
                    break
                except ValueError:
                    print("Please enter a valid daily_rate (numeric).")

        # Input for minimum and maximum rent periods
        while True:
            min_rent_period_input = input("Enter minimum rent period (in days): ")
            if min_rent_period_input.isdigit():
                min_rent_period = int(min_rent_period_input)
                break
            else:
                print("Please enter a valid minimum rent period (numeric).")

        while True:
            max_rent_period_input = input("Enter maximum rent period (in days): ")
            if max_rent_period_input.isdigit():
                max_rent_period = int(min_rent_period_input)
                break
            else:
                print("Please enter a valid maximum rent period (numeric).")
        
        # Create a Car instance
        car = Car(make, model, year, mileage, daily_rate, min_rent_period, max_rent_period, available_now=True)
        car.save(db)
        print("Car added successfully.")

    def view_cars(db):
        print("Viewing available cars...")
        cars = db.fetch_all('SELECT * FROM cars WHERE available_now = 1')
        if cars:
            for car in cars:
                print(f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Daily Rate: ${car[5]:.2f}, Min Rent Period: {car[6]},Max Rent Period: {car[7]}")
        else:
            print("No available cars.")

    def update_car(db):
        print("Updating a car...")
        
        # Prompt for the car ID to update
        car_id = input("Enter the ID of the car you want to update: ")
        
        if not car_id.isdigit():
            print("Invalid car ID. Please enter a numeric value.")
            return
        
        car_id = int(car_id)

        # Fetch the current details of the car
        current_car = db.fetch_one('SELECT * FROM cars WHERE id = %s', (car_id,))
        
        if not current_car:
            print("Car not found.")
            return
        if current_car[8]:
            availability = 'yes'
        else:
            availability = 'no'

        print(f"Current details: Make: {current_car[1]}, Model: {current_car[2]}, Year: {current_car[3]}, "
            f"Mileage: {current_car[4]}, Daily Rate: {current_car[5]}, "
            f"Min Rent Period: {current_car[6]}, Max Rent Period: {current_car[7]}, "
            f"Available Now: {availability}")

        # Prompt for new details
        make = input("Enter new car make (leave blank to keep current): ")
        model = input("Enter new car model (leave blank to keep current): ")
        
        # Input validation for year
        while True:
            year_input = input("Enter new car year (leave blank to keep current): ")
            if year_input == "":
                year = current_car[3]  # Keep current year
                break
            elif year_input.isdigit():
                year = int(year_input)
                break
            else:
                print("Please enter a valid year (numeric).")
        
        # Input validation for mileage
        while True:
            mileage_input = input("Enter new car mileage (leave blank to keep current): ")
            if mileage_input == "":
                mileage = current_car[4]  # Keep current mileage
                break
            elif mileage_input.isdigit():
                mileage = int(mileage_input)
                break
            else:
                print("Please enter a valid mileage (numeric).")

        # Input for daily_rate
        while True:
            daily_rate_input = input("Enter new car daily rate (leave blank to keep current): ")
            if daily_rate_input == "":
                daily_rate = current_car[5]  # Keep current daily rate
                break
            try:
                daily_rate = float(daily_rate_input)
                if daily_rate < 0:
                    raise ValueError("Daily rate cannot be negative.")
                break
            except ValueError:
                print("Please enter a valid daily rate (numeric).")

        # Input for minimum and maximum rent periods
        while True:
            min_rent_period_input = input("Enter new minimum rent period (leave blank to keep current): ")
            if min_rent_period_input == "":
                min_rent_period = current_car[6]  # Keep current minimum rent period
                break
            elif min_rent_period_input.isdigit():
                min_rent_period = int(min_rent_period_input)
                break
            else:
                print("Please enter a valid minimum rent period (numeric).")

        while True:
            max_rent_period_input = input("Enter new maximum rent period (leave blank to keep current): ")
            if max_rent_period_input == "":
                max_rent_period = current_car[7]  # Keep current maximum rent period
                break
            elif max_rent_period_input.isdigit():
                max_rent_period = int(max_rent_period_input)
                break
            else:
                print("Please enter a valid maximum rent period (numeric).")

        # Input for available_now
        while True:
            available_now_input = input("Is the car available now? (yes/no, leave blank to keep current): ")
            if available_now_input.lower() == 'yes':
                available_now = 1
                break
            elif available_now_input.lower() == 'no':
                available_now = 0
                break
            elif available_now_input == '':
                available_now = current_car[8]  # Keep current availability
                break
            else:
                print("Please enter a valid yes/no.")

        # Update the car in the database
        update_query = '''
            UPDATE cars
            SET make = %s, model = %s, year = %s, mileage = %s,
                daily_rate = %s, min_rent_period = %s,
                max_rent_period = %s, available_now = %s
            WHERE id = %s
        '''
        params = (make if make else current_car[1],
                model if model else current_car[2],
                year,
                mileage,
                daily_rate,
                min_rent_period,
                max_rent_period,
                available_now,
                car_id)
        
        db.execute_query(update_query, params)
        print("Car updated successfully.")


    def delete_car(db):
        print("Deleting a car...")
        try:
            car_id = input("Enter the ID of the car to delete: ")
            
            if not car_id.isdigit():
                print("Invalid input. Please enter a valid car ID (numeric).")
                return
            
            car_id = int(car_id)
            
            query = '''
                DELETE FROM cars
                WHERE id = %s
            '''
            
            db.execute_query(query, (car_id,))
            
            if db.cursor.rowcount > 0:
                print(f"Car with ID {car_id} has been deleted successfully.")
            else:
                print(f"No car found with ID {car_id}.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

class Rental:
    def __init__(self, user_id, car_id, start_date, end_date, status='pending'):
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def save(self, db):
        """Save the rental to the database."""
        query = '''
            INSERT INTO rentals (user_id, car_id, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s)
        '''
        params = (self.user_id, self.car_id, self.start_date, self.end_date, self.status)
        db.execute_query(query, params)

    def calculate_rental_fee(daily_rate, start_date, end_date):
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        rental_duration = (end_date_obj - start_date_obj).days

        if rental_duration <= 0:
            print("Invalid rental duration.")
            return 0

        total_fee = rental_duration * daily_rate
        return total_fee

    def book_car(db, user_id):
        Car.view_cars(db)  # Show available cars
        car_id = input("Enter the ID of the car you want to book: ")
        
        # Validate car ID
        if not car_id.isdigit():
            print("Invalid car ID.")
            return
        
        car_id = int(car_id)
        
        start_date = input("Enter rental start date (YYYY-MM-DD): ")
        end_date = input("Enter rental end date (YYYY-MM-DD): ")
        
        # Validate dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start_date_obj >= end_date_obj:
                print("End date must be after start date.")
                return
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Fetch car details to get the daily rate
        car = db.fetch_one('SELECT * FROM cars WHERE id = %s', (car_id,))
        if not car:
            print("Car not found.")
            return
        
        daily_rate = car[5]
        rental_fee = Rental.calculate_rental_fee(daily_rate, start_date, end_date)
        
        # Create a Rental instance
        rental = Rental(user_id=user_id, car_id=car_id, start_date=start_date, end_date=end_date)
        rental.save(db)  # Save the rental to the database
        print(f"Car booked successfully! Rental Fee: ${rental_fee:.2f}")

    def manage_rental_bookings(db):
        print("Managing Rental Bookings...")
        rentals = db.fetch_all('SELECT * FROM rentals')
        
        for rental in rentals:
            print(f"Rental ID: {rental[0]}, User ID: {rental[1]}, Car ID: {rental[2]}, Start Date: {rental[3]}, End Date: {rental[4]}, Status: {rental[5]}")
        
        
        while True:
            print("\n1. Manage Bookings\n2. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                rental_id = input("Enter the Rental ID to approve/reject: ")
                if not rental_id.isdigit() or not rental_id in rentals:
                    print("Invalid Rental ID.")
                    return
                
                rental_id = int(rental_id)
                action = input("Enter 'approve' to approve or 'reject' to reject: ").strip().lower()
                
                if action == 'approve':
                    db.execute_query('UPDATE rentals SET status = %s WHERE id = %s', ('approved', rental_id))
                    print("Rental approved.")
                elif action == 'reject':
                    db.execute_query('UPDATE rentals SET status = %s WHERE id = %s', ('rejected', rental_id))
                    print("Rental rejected.")
                else:
                    print("Invalid action.")
            if choice == '2':
                break
