import mysql.connector

class Database:
    def __init__(self, host='localhost', user='root', password='minrui1992', database='car_rental'):
        # Connect to the MySQL database
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Create the users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(10) NOT NULL
            )
        ''')
        
        # Create the cars table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                make VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                mileage INT NOT NULL,
                daily_rate DECIMAL(10, 2) NOT NULL,
                min_rent_period INT NOT NULL,
                max_rent_period INT NOT NULL,
                available_now TINYINT(1) NOT NULL DEFAULT 1
            )
        ''')
        
        # Create the rentals table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                userId INT NOT NULL,
                carId INT NOT NULL,
                startDate DATE NOT NULL,
                endDate DATE NOT NULL,
                status VARCHAR(20) NOT NULL,
                FOREIGN KEY(userId) REFERENCES users(id),
                FOREIGN KEY(carId) REFERENCES cars(id)
            )
        ''')
        
        # Commit the changes to the database
        self.connection.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
