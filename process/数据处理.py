import pandas as pd
import numpy as np

df = pd.read_csv("../original_data/医疗相关市场规模（百万美元）.csv")
hl = pd.read_csv("../original_data/美元汇率.csv")
df2 = pd.read_csv("../original_data/医疗相关企业数量（个）.csv")

# |%%--%%| <sFRqXvorah|FyxPPsF0Rj>

df["时间"] = pd.to_datetime(df["时间"])
hl["时间"] = pd.to_datetime(hl["时间"])
df2["时间"] = pd.to_datetime(df2["时间"])

# |%%--%%| <FyxPPsF0Rj|mgpSo49riu>

df = df[df["时间"] >= "2014-12-01"]
df = df[df["时间"] <= "2024-01-01"]

hl = hl[hl["时间"] >= "2014-12-01"]
hl = hl[hl["时间"] <= "2024-01-01"]

df2 = df2[df2["时间"] >= "2014-12-01"]
df2 = df2[df2["时间"] <= "2024-01-01"]

# |%%--%%| <mgpSo49riu|r12blqh8WX>

for i in df.columns[1:]:
    df[i] = df[i].values * hl.iloc[:, 1].values / 100

# |%%--%%| <r12blqh8WX|MI2IHDJ83O>

df.to_csv("../data/2014-2023医疗相关市场规模（亿人民币）.csv", index=False)
df2.to_csv("../data/2014-2023医疗相关企业数量（个）.csv", index=False)

# |%%--%%| <MI2IHDJ83O|0nA5jySPLN>

sum1 = pd.DataFrame()
sum1['时间'] = df['时间']
sum1['市场规模'] = df.iloc[:, 1:].sum(axis=1)

#|%%--%%| <0nA5jySPLN|ssl1A4MsG7>

sum2 = pd.DataFrame()
sum2['时间'] = df2['时间']
sum2['企业数量'] = df2.iloc[:, 1:].sum(axis=1)

#|%%--%%| <ssl1A4MsG7|ifoJOyreHC>

sum1.to_csv("../data/2014-2023医疗相关市场规模汇总（亿人民币）.csv", index=False)
sum2.to_csv("../data/2014-2023医疗相关企业数量汇总（个）.csv", index=False)
