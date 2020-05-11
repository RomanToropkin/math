import pandas as pd

df = pd.read_csv('MAT_nba.xls')
df = df.fillna(0)

print(df.corr(method = 'kendall'))