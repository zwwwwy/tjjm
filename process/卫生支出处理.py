import pandas as pd
from mtb.tools import prefer_settings

prefer_settings()

df = pd.read_csv("../original_data/政府卫生支出（季度）.csv")
df = df.iloc[28:]
df = df.rename({"Unnamed: 0": "时间"}, axis=1)
df['时间'] = pd.to_datetime(df['时间'])
df = df[df["时间"] >= "2014-01-01"]
df = df[df['时间']<='2023-12-31']
df['财政支出:一般公共预算支出:卫生健康'] = df['财政支出:一般公共预算支出:卫生健康'].astype('float')
#|%%--%%| <g0CkM0Tv4C|aIrhBnz7sl>

import matplotlib.pyplot as plt

plt.plot(df['时间'], df['财政支出:一般公共预算支出:卫生健康'])

