import os
import pymysql
import re
from datetime import datetime

# Connect to MySQL
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='Itsm3abhilash!',
                       db='etl')

# Create a cursor object
cursor = conn.cursor()

# Define the SQL statement to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS logg_daata1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(255),
    user_id VARCHAR(255),
    timestamp DATETIME,
    http_method VARCHAR(10),
    requested_url VARCHAR(255),
    http_version VARCHAR(10),
    status_code INT,
    bytes_sent INT,
    referer VARCHAR(255),
    user_agent VARCHAR(255)
);
"""

# Execute the SQL statement to create the table
cursor.execute(create_table_sql)

# Directory containing the log files
log_directory = r'C:\Users\chand\Downloads\logs'

# Get a list of all log files in the directory
log_files = [os.path.join(log_directory, file) for file in os.listdir(log_directory) if file.endswith('.log')]

# Function to parse log entry and insert into database
def parse_log_entry(line):
    fields = line.strip().split(' ')
    if len(fields) < 10:
        print(f"Error: Insufficient number of fields in log entry: {line}")
    else:
        if len(fields) < 10:
            print(f"Error: Insufficient number of fields in log entry: {line}")
        else:
            ip_address_user_id = fields[0]
            ip_address = ip_address_user_id.split('-')[0].strip()

            match = re.search(r'-(\d+) ', ip_address_user_id)
            if match:
                user_id = match.group(1)
            else:
                user_id = None  # Set user_id to None if user ID is not present

        # Extract timestamp from the log entry
        timestamp_str = fields[3][1:] + ' ' + fields[4][:-1]
        # Convert timestamp to datetime object
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')

        request_info = ' '.join(fields[5:8])
        status_code = fields[8]
        bytes_sent = fields[9]

        # Extracting HTTP method from the request information
        http_method = request_info.split()[0]

        # Extracting requested URL from the request information
        requested_url = request_info.split()[1]

        # Extracting HTTP version from the request information
        http_version = request_info.split()[2]

        referer = fields[10] if len(fields) >= 11 else ''
        user_agent = ' '.join(fields[11:]) if len(fields) >= 12 else ''

        try:
            cursor.execute("INSERT INTO logg_daata1 (ip_address, user_id, timestamp, http_method, requested_url, http_version, status_code, bytes_sent, referer, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ip_address, user_id, timestamp, http_method, requested_url, http_version, int(status_code), int(bytes_sent), referer, user_agent))
        except Exception as e:
            print(f"Error inserting log entry into database: {e}")

# Iterate through each log file
for log_file in log_files:
    # Open the log file
    with open(log_file, 'r') as file:
        # Iterate through each line in the file
        for line_number, line in enumerate(file, start=1):
            parse_log_entry(line)

# Commit the changes
conn.commit()

# Execute SQL query to fetch data from log_data table
cursor.execute("SELECT * FROM logg_daata1")

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
