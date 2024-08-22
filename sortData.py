import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
csv_file = 'laptop_data_newegg.csv'
df = pd.read_csv(csv_file)

# Count the number of laptops with and without fingerprint scanners overall
fingerprint_count = df['Fingerprint Scanner'].value_counts()

# Group by page and count the number of laptops with and without fingerprint scanners per page
page_fingerprint_counts = df.groupby(['Page', 'Fingerprint Scanner']).size().unstack(fill_value=0)

# Create a bar plot for overall fingerprint availability
plt.figure(figsize=(10, 6))
bars = plt.bar(fingerprint_count.index.map({True: 'With Fingerprint', False: 'Without Fingerprint'}), 
               fingerprint_count.values, color=['#4CAF50', '#FF5733'])

# Adding labels and title for overall fingerprint availability
plt.xlabel('Fingerprint Scanner Availability')
plt.ylabel('Number of Laptops')
plt.title('Distribution of Laptops by Fingerprint Scanner Availability')

# Adding value labels on top of each bar for overall fingerprint availability
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom')

# Show the plot for overall fingerprint availability
plt.tight_layout()
plt.show()

# Create a plot for fingerprint scanner availability per page (without total)
page_fingerprint_counts.plot(kind='bar', stacked=True, figsize=(12, 8), color=['#4CAF50', '#FF5733'])

# Adding labels and title for per page fingerprint availability
plt.xlabel('Page Number')
plt.ylabel('Number of Laptops')
plt.title('Fingerprint Scanner Availability per Page')

# Adding value labels on top of each bar for per page fingerprint availability
for i, row in page_fingerprint_counts.iterrows():
    plt.text(i - 1.5, row[True] + row[False] + 2, f'With: {row[True]}', ha='center', va='bottom')
    plt.text(i - 1.5, row[False] / 2, f'Without: {row[False]}', ha='center', va='center')

# Show the plot for per page fingerprint availability
plt.tight_layout()
plt.show()

# Optionally, save the plot to a file
# plt.savefig('fingerprint_scanner_per_page_distribution.png', dpi=300, bbox_inches='tight')
