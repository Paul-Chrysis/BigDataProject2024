import pandas as pd

df = pd.read_csv('./../sources/vehicles.csv')
df_sorted = df.sort_values(by='t')
df_sorted.to_csv('./../sources/sorted_vehicles.csv', index=False)