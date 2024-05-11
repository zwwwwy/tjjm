import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from mtb.tools import prefer_settings

prefer_settings()

scaler = MinMaxScaler()
df = pd.read_excel('./data/人工智能指标.xlsx')
df = df.set_index("year")
for i in df.columns:
    df[i] = scaler.fit_transform(df[i].values.reshape(-1, 1))
df = df.sort_index(ascending=True)

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

e = pd.Series(e_lst.values(),index=e_lst.keys())
g = 1 - e
w1 = g/g.sum()
w1

#|%%--%%| <QvkdMJZ4sr|ZedYteWGJI>

# CRITIC
corr = df.corr()
std = df.std()
r = 1-corr
r = r.sum()
c = std*r
w2 = c/c.sum()
#|%%--%%| <ZedYteWGJI|iM7TCCSUXi>

w = (w1+w2)/2
result = (df*w).sum(axis=1)
result.to_csv('./data/综合指数/人工智能综合指数.csv')
print("完成")
