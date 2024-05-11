import pandas as pd
from mtb.tools import prefer_settings

prefer_settings()

bd1 = pd.read_excel("../original_data/ai_全国.xlsx")
bd2 = pd.read_excel("../original_data/人工智能_全国.xlsx")
zw = pd.read_excel("../original_data/知网指数.xlsx")

# |%%--%%| <VpD7SrNP7d|rm302PxR5V>

bd1["时间"] = pd.to_datetime(bd1["时间"])
bd2["时间"] = pd.to_datetime(bd2["时间"])
# zw["时间"] = pd.to_datetime(zw["时间"])

# |%%--%%| <rm302PxR5V|QYMNjPyJRh>

sum_ai = bd1.iloc[:, 3].groupby(bd1["时间"].dt.year).sum()
sum_rgzn = bd2.iloc[:, 3].groupby(bd2["时间"].dt.year).sum()
sum_bd = pd.DataFrame()
sum_bd["时间"] = bd1["时间"].dt.year.unique()
sum_bd["搜索指数"] = sum_ai.values + sum_rgzn.values
sum_bd.to_csv("../data/ai+人工智能搜索指数.csv", index=False)

#|%%--%%| <QYMNjPyJRh|Zbv4cG1TXh>

zw_wx = zw['ai中文相关文献量'].values + zw['人工智能中文相关文献量'].values
zw_by = zw['ai文献被引量'].values + zw['人工智能文献被引量'].values
sum_zw = pd.DataFrame()
sum_zw["时间"] = zw["时间"]
sum_zw["文献量"] = zw_wx
sum_zw["被引量"] = zw_by
sum_zw.to_csv("../data/ai+人工智能知网指数.csv", index=False)



