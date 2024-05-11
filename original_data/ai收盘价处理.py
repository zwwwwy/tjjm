import pandas as pd
from mtb.tools import prefer_settings
prefer_settings()
df = pd.read_csv('./人工智能指数-收盘价(前复权).csv')
df = df[['国家','Unnamed: 1']]
df = df.iloc[7:-2,:]

df = df.rename(columns={'国家':'year','Unnamed: 1':'close'})
df['year'] = pd.to_datetime(df['year'])
df['year'] = df['year'].dt.year

#|%%--%%| <n9DFazIzmg|BtQpzwNITw>

last = df.groupby('year')['close'].last()
last = last[last.index>=2013]
last = last[last.index<=2022]
last.to_csv('../data/ai企业收盘价.csv')

