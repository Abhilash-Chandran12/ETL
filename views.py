import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # Replace with your MySQL host
            user='root',  # Replace with your MySQL username
            password='Itsm3abhilash!',  # Replace with your MySQL password
            database='etl'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def create_view(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE ALGORITHM = UNDEFINED
            DEFINER = `root`@`localhost`
            SQL SECURITY DEFINER
            VIEW `etl`.`request_vie` AS
            SELECT 
                `etl`.`logg_daata`.`ip_address` AS `ip_address`,
                COUNT(0) AS `request_count`
            FROM
                `etl`.`logg_daata`
            GROUP BY `etl`.`logg_daata`.`ip_address`
        """)
        print("View 'request_vie' created successfully")
    except Error as e:
        print(f"Error creating view: {e}")

def select_from_view(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM etl.request_vie;")
        rows = cursor.fetchall()
        if rows:
            print("Values in the 'request_vie' view:")
            for row in rows:
                print(row)
        else:
            print("No values found in the 'request_vie' view")
    except Error as e:
        print(f"Error selecting from view: {e}")

def main():
    connection = connect_to_mysql()
    if connection:
        create_view(connection)
        select_from_view(connection)
        connection.close()
        print('Connection closed')

if __name__ == "__main__":
    main()