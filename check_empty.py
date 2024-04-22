import pymysql

# Establish connection to MySQL database
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='Itsm3abhilash!',
                       db='etl')

# Create a cursor object
cursor = conn.cursor()

# Define the columns you want to check
columns_to_check = ['ip_address', 'user_id']

# Iterate over each column
for column in columns_to_check:
    # Define SQL statement to count NULL values in the column
    count_null_sql = f"SELECT COUNT(*) FROM user_data WHERE {column} IS NULL;"

    # Execute SQL statement to count NULL values
    cursor.execute(count_null_sql)
    null_count = cursor.fetchone()[0]

    # Check if there are any NULL values in the column
    if null_count > 0:
        print(f"Column '{column}' contains NULL values.")
    else:
        print(f"Column '{column}' does not contain NULL values.")

# Close the cursor and connection
cursor.close()
conn.close()
