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

def remove_duplicates(connection):
    try:
        cursor = connection.cursor()

        # SQL query to remove duplicates based on requested_url
        delete_query = """
            DELETE ld1
            FROM logg_daata ld1
            JOIN (
                SELECT MIN(id) AS id
                FROM logg_daata
                GROUP BY requested_url
            ) ld2 ON ld1.id <> ld2.id;
        """

        # Execute the delete query
        cursor.execute(delete_query)

        # Commit the changes
        connection.commit()
        print("Duplicates removed from the 'logg_daata' table")
    except Error as e:
        connection.rollback()
        print(f"Error removing duplicates: {e}")

def main():
    connection = connect_to_mysql()
    if connection:
        remove_duplicates(connection)
        connection.close()
        print('Connection closed')

if __name__ == "__main__":
    main()
