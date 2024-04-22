import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV into a DataFrame
csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# Total number of records in the dataset
total_successful_requests = len(df)

# Plotting
plt.figure(figsize=(6, 4))
plt.bar(['Total Requests'], [total_successful_requests], color='skyblue')
plt.text('Total Requests', total_successful_requests, str(total_successful_requests), ha='center', va='bottom')
plt.xlabel('Requests')
plt.ylabel('Number of Requests')
plt.title('Total Number of Requests in the Dataset')
plt.show()
