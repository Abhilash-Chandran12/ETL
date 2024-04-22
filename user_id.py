import pymysql
import re
import os

def extract_user_id_and_ip(record):
    # Define a regular expression pattern to match the user ID and IP address
    pattern = r'(\d+\.\d+\.\d+\.\d+) - (\d+) \['
    match = re.search(pattern, record)
    if match:
        ip_address = match.group(1)
        user_id = match.group(2)
        return ip_address, user_id
    else:
        return None, None

# Establish connection to MySQL database
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='Itsm3abhilash!',
                       db='etl')
# Create a cursor object
cursor = conn.cursor()

# Define SQL statement to create the table (if it doesn't exist)
create_table_sql = """
CREATE TABLE IF NOT EXISTS user_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(255),
    user_id INT
);
"""

# Execute SQL statement to create the table
cursor.execute(create_table_sql)

# Directory containing the log files
log_directory = r'C:\Users\chand\Downloads\logs'

# Iterate over each log file in the directory
for filename in os.listdir(log_directory):
    if filename.endswith('.log'):
        log_file_path = os.path.join(log_directory, filename)
        # Open the log file
        with open(log_file_path, 'r') as file:
            # Process each record in the log file
            batch_records = []
            for line in file:
                # Process each record
                ip_address, user_id = extract_user_id_and_ip(line)
                if ip_address and user_id:
                    batch_records.append((ip_address, user_id))
                    # Insert records in batch
                    if len(batch_records) == 100:  # Adjust batch size as needed
                        try:
                            cursor.executemany("INSERT INTO user_data (ip_address, user_id) VALUES (%s, %s)", batch_records)
                            conn.commit()  # Commit the transaction after each batch insertion
                            batch_records = []  # Reset batch records
                        except Exception as e:
                            print(f"Error inserting data into database: {e}")

            # Insert remaining records in the last batch
            if batch_records:
                try:
                    cursor.executemany("INSERT INTO user_data (ip_address, user_id) VALUES (%s, %s)", batch_records)
                    conn.commit()  # Commit the transaction for the last batch insertion
                except Exception as e:
                    print(f"Error inserting data into database: {e}")
cursor.execute("SELECT * FROM user_data")

# Fetch all rows
rows = cursor.fetchall()

# Print column names
print("ID\tIP Address\tUser ID\tTimestamp\t\t\tHTTP Method\tRequested URL\tHTTP Version\tStatus Code\tBytes Sent\tReferer\t\tUser Agent")
print("-------------------------------------------------------------------------------------------------------------------------------")

# Print each row
for row in rows:
    print("\t".join(map(str, row)))
# Close the cursor and connection
cursor.close()
conn.close()
