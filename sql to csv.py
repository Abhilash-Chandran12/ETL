import pandas as pd
from sqlalchemy import create_engine

# Create SQLAlchemy engine
engine = create_engine('mysql+pymysql://root:Itsm3abhilash!@127.0.0.1/etl')

# Execute SQL query to fetch data from log_data table
query = "SELECT * FROM loggu_daata"
df = pd.read_sql_query(query, engine)

# Close the engine connection
engine.dispose()

# Save DataFrame to CSV in the specified directory
csv_file = r'C:\Users\chand\OneDrive\Desktop\log_data.csv'
df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}")
