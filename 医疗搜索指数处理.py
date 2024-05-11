import pandas as pd
from mtb.tools import prefer_settings
prefer_settings()

df = pd.read_excel("./original_data/医疗_全国.xlsx")
df['合计'] = df.iloc[:,3:].sum(axis=1).values
df = df[['时间','合计']]
df['时间'] = pd.to_datetime(df['时间'])
df['时间'] = df['时间'].dt.year
group = df.groupby('时间').sum()
group.pct_change().to_csv("./data/医疗搜索指数变化率.csv")
