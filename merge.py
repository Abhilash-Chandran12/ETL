import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV into a DataFrame
csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# Count the number of requests made by each user
requests_per_user = df['ip_address'].value_counts()

# Count the frequency of each number of requests made
requests_count_frequency = requests_per_user.value_counts().sort_index()

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(requests_count_frequency.index, requests_count_frequency, color='skyblue')
plt.xlabel('Number of Requests Made')
plt.ylabel('Number of Users')
plt.title('Distribution of Number of Requests per User')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate bars with the number of users
for bar in bars:
    height = bar.get_height()
    plt.annotate('{}'.format(height),
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom')

plt.show()
