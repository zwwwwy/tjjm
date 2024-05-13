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

#|%%--%%| <hpJiNupXWa|BEPkLl1WLa>

control = ["卫生总费用(亿元)", "政府卫生支出(亿元)", "人均卫生费用(元)"]
df_control = df.loc[:, control]
df_copy = df.drop(control, axis=1)
df_copy

# |%%--%%| <BEPkLl1WLa|UgHk10ZlrP>

# 投入
df = df_copy[["卫生机构床位数(万张)", "卫生人员数(万人)", "医疗机构数量"]]
sum_col = df.sum()
p = pd.DataFrame()
e_lst = dict()
k = 1 / np.log(len(df))
for i in df.columns:
    p[i] = df[i] / sum_col[i]
    tmp = np.log(p[i]) * p[i]
    e_lst[i] = -k * tmp.sum()

# |%%--%%| <UgHk10ZlrP|lcR57B7rUF>

e = pd.Series(e_lst.values(), index=e_lst.keys())
g = 1 - e
w1 = g / g.sum()
w1

# |%%--%%| <lcR57B7rUF|r0RLMkor9F>

# CRITIC
corr = df.corr()
std = df.std()
r = 1 - corr
r = r.sum()
c = std * r
w2 = c / c.sum()
# |%%--%%| <r0RLMkor9F|UMH2flvK3O>

w = (w1 + w2) / 2
result1 = (df * w).sum(axis=1)
result1.name = "投入"
result1

# result.to_csv("./data/综合指数/医疗综合指数.csv")
# w.to_csv("./data/综合指数/医疗指标权重.csv")
# print("完成")
#|%%--%%| <UMH2flvK3O|JAMsMtG3Kq>

# 产出
df = df_copy.iloc[:,2:6]

sum_col = df.sum()
p = pd.DataFrame()
e_lst = dict()
k = 1 / np.log(len(df))
for i in df.columns:
    p[i] = df[i] / sum_col[i]
    tmp = np.log(p[i]) * p[i]
    e_lst[i] = -k * tmp.sum()

#|%%--%%| <JAMsMtG3Kq|3fobo17CGq>

e = pd.Series(e_lst.values(), index=e_lst.keys())
g = 1 - e
w1 = g / g.sum()
w1

#|%%--%%| <3fobo17CGq|wJG7CEOpzk>

# CRITIC
corr = df.corr()
std = df.std()
r = 1 - corr
r = r.sum()
c = std * r
w2 = c / c.sum()
#|%%--%%| <wJG7CEOpzk|WwzyOXmzVJ>

w = (w1 + w2) / 2
result2 = (df * w).sum(axis=1)
result2.name = "产出"
result2
# result.to_csv("./data/综合指数/医疗综合指数.csv")
# w.to_csv("./data/综合指数/医疗指标权重.csv")
# print("完成")
#|%%--%%| <WwzyOXmzVJ|wZgSW4cRvy>

# 聚合
df = pd.concat([result1, result2,df_copy.iloc[:,-1],df_copy.iloc[:,-2]], axis=1)
sum_col = df.sum()
p = pd.DataFrame()
e_lst = dict()
k = 1 / np.log(len(df))
for i in df.columns:
    p[i] = df[i] / sum_col[i]
    tmp = np.log(p[i]) * p[i]
    e_lst[i] = -k * tmp.sum()

# |%%--%%| <wZgSW4cRvy|SU7s8wwrfg>

e = pd.Series(e_lst.values(), index=e_lst.keys())
g = 1 - e
w1 = g / g.sum()
w1

# |%%--%%| <SU7s8wwrfg|cloiIR2M8Y>

# CRITIC
corr = df.corr()
std = df.std()
r = 1 - corr
r = r.sum()
c = std * r
w2 = c / c.sum()
# |%%--%%| <cloiIR2M8Y|D4vYyBouAq>

w = (w1 + w2) / 2
result = (df * w).sum(axis=1)
result.to_csv("./data/综合指数/医疗综合指数.csv")
w.to_csv("./data/综合指数/医疗指标权重.csv")
print("完成")
#|%%--%%| <D4vYyBouAq|xzoAR6uJes>

std
