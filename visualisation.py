import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Suppress pandas warning about pymysql connection
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")


# Connect to MySQL
conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='Itsm3abhilash!',
                       db='etl')

# Read data from MySQL into a DataFrame
sql_query = "SELECT * FROM logg_daata1"
df = pd.read_sql(sql_query, conn)

# Close the MySQL connection
conn.close()

# Calculate KPIs
# Number of Users
num_users = df['ip_address'].nunique()

# Number of Requests per User
requests_per_user = df['ip_address'].value_counts()

# Total Number of Successful Requests
total_successful_requests = len(df)

# Plotting
# Bar plot for Number of Users
plt.figure(figsize=(8, 6))
plt.bar(['Number of Users'], [num_users], color='skyblue')
plt.xlabel('KPI')
plt.ylabel('Count')
plt.title('Number of Users')
plt.show()

# Bar plot for Number of Requests per User
plt.figure(figsize=(12, 6))
requests_per_user.plot(kind='bar', color='skyblue')
plt.xlabel('User ID')
plt.ylabel('Number of Requests')
plt.title('Number of Requests per User')
plt.xticks(rotation=45)
plt.show()

# Pie chart for Total Number of Successful Requests
plt.figure(figsize=(8, 8))
plt.pie([total_successful_requests], labels=['Total Successful Requests'], autopct='%1.1f%%', colors=['skyblue'])
plt.title('Total Successful Requests')
plt.show()
