import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

df1 = pd.read_csv("./2014-2023医疗相关市场规模汇总（亿人民币）.csv")
df1 = df1.iloc[::-1]
# df1['市场规模'] = StandardScaler().fit_transform(df1['市场规模'].values.reshape(-1, 1))
df1["市场规模"] = np.log(df1["市场规模"])
# df1.to_csv('./y.csv')

# |%%--%%| <gjUDLaoKi2|CQCQ1Sih1i>

df2 = pd.read_csv("./一堆指标的组合（前序填充）.csv")
for i in df2.columns[1:]:
    df2[i] = np.log(df2[i])
    # df2[i] = StandardScaler().fit_transform(df2[i].values.reshape(-1, 1))
# df2.to_csv('./x.csv')
fuck = pd.concat([df1['市场规模'], df2], axis=1)
fuck["市场规模"] = fuck["市场规模"].values[::-1]
# fuck = fuck.values[::-1]
fuck.iloc[::-1]

# |%%--%%| <CQCQ1Sih1i|sv2XUCWQwD>

import mtb
from mtb.tools import prefer_settings

prefer_settings()
# fuck = fuck.drop("year",axis=1)
# fuck = fuck.drop("时间",axis=1)
mtb.corr_heatmap(fuck, figsize=(30, 30), save_path="./fuck.png")
# |%%--%%| <sv2XUCWQwD|XksM37Jz6c>

fuck = fuck.dropna(axis=1)
fuck.to_csv('./data.csv')

# |%%--%%| <XksM37Jz6c|D26BaruDQl>

fuck = fuck.fillna(method="ffill")
mtb.evr_plot(fuck, 0.99)

# |%%--%%| <D26BaruDQl|GxskArxYCS>
