import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("data/consolidated_purchases.csv")
df['Date']=pd.to_datetime(df['Date'])
print(df.head())
