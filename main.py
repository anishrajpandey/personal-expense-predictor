import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("data/consolidated_purchases.csv")

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

weekly_spending = df.resample('W')['Cost'].sum()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(weekly_spending.index, weekly_spending.values, marker='o', linestyle='-')
ax.set_xlabel('Date')
ax.set_ylabel('Weekly Cost')
ax.set_title('Weekly Spending O ver Time')
plt.grid(True)
plt.show()

print(weekly_spending.head())
