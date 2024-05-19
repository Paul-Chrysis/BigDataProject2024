import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('./../sources/vehicles.csv')

# Sort the DataFrame based on a specific field, for example, 't'
df_sorted = df.sort_values(by='t')

# Write the sorted DataFrame back to a CSV file
df_sorted.to_csv('./../sources/sorted_vehicles.csv', index=False)