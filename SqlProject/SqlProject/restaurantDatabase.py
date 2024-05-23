import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurant",
                 user="root",
                 password="Yemen123"):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def addCustomer(self, customer_name, contact_info):
        try:
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                query = "INSERT INTO customers (customer_name, contact_info) VALUES (%s, %s)"
                self.cursor.execute(query, (customer_name, contact_info))
                self.connection.commit()
                print("Customer added successfully")
        except Error as e:
            print("Error adding customer:", e)

    def findCustomer(self, customer_name):
        try:
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                query = "SELECT customerId FROM customers WHERE customer_name = %s"
                self.cursor.execute(query, (customer_name,))
                result = self.cursor.fetchone()
                if result:
                    return result[0]  # Return customerId if customer exists
                else:
                    return None  # Customer not found
        except Error as e:
            print("Error finding customer:", e)
            return None

    def addReservation(self, customer_name, reservation_time, number_of_guests, special_requests):
        try:
            if self.connection.is_connected():
                # Check if customer exists or add new customer
                customer_id = self.findCustomer(customer_name)
                if not customer_id:
                    self.addCustomer(customer_name, "")  # Add customer with empty contact_info
                    customer_id = self.findCustomer(customer_name)

                # Insert reservation
                self.cursor = self.connection.cursor()
                query = "INSERT INTO reservations (customerId, reservation_time, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests))
                self.connection.commit()
                print("Reservation added successfully")
        except Error as e:
            print("Error adding reservation:", e)

    def getAllReservations(self):
        try:
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                query = "SELECT r.reservationId, c.customer_name, r.reservation_time, r.numberOfGuests, r.specialRequests FROM reservations r INNER JOIN customers c ON r.customerId = c.customerId"
                self.cursor.execute(query)
                records = self.cursor.fetchall()
                return records
        except Error as e:
            print("Error fetching reservations:", e)
            return []

    def closeConnection(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
                print("MySQL connection is closed")
        except Error as e:
            print("Error closing MySQL connection:", e)
