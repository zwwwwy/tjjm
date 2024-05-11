import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from mtb.tools import prefer_settings

prefer_settings()

scaler = MinMaxScaler()
df = pd.read_excel("./data/医疗指标.xlsx")
df = df.set_index("year")
df = df.loc[2022:2013, :]

for i in df.columns:
    df[i] = scaler.fit_transform(df[i].values.reshape(-1, 1))
df = df.sort_index(ascending=True)

# |%%--%%| <URpM8k8Gl3|BEPkLl1WLa>

control = ["卫生总费用(亿元)", "政府卫生支出(亿元)", "人均卫生费用(元)"]
df_control = df.loc[:, control]
df = df.drop(control, axis=1)

# |%%--%%| <BEPkLl1WLa|7BYS9wRI8J>

sum_col = df.sum()
p = pd.DataFrame()
e_lst = dict()
k = 1 / np.log(len(df))
for i in df.columns:
    p[i] = df[i] / sum_col[i]
    tmp = np.log(p[i]) * p[i]
    e_lst[i] = -k * tmp.sum()

# |%%--%%| <7BYS9wRI8J|QvkdMJZ4sr>

e = pd.Series(e_lst.values(), index=e_lst.keys())
g = 1 - e
w1 = g / g.sum()
w1

# |%%--%%| <QvkdMJZ4sr|ZedYteWGJI>

# CRITIC
corr = df.corr()
std = df.std()
r = 1 - corr
r = r.sum()
c = std * r
w2 = c / c.sum()
#|%%--%%| <ZedYteWGJI|D4vYyBouAq>

w = (w1+w2)/2
result = (df*w).sum(axis=1)
result.to_csv('./data/综合指数/医疗综合指数.csv')
w.to_csv("./data/综合指数/医疗指标权重.csv")
print("完成")



