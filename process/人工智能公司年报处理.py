import pandas as pd
import numpy as np
from mtb.tools import prefer_settings

prefer_settings()

df = pd.read_csv("../original_data/人工智能年报数据.csv")
# df.set_index("公司代码_CompanyCode", inplace=True)
df["截止日期_EndDt"] = pd.to_datetime(df["截止日期_EndDt"])

# df = df[df["信息来源_InfoSource"] != "审计报告"]
# df.loc[df["信息来源_InfoSource"] == "第一季报", "信息来源_InfoSource"] = "Q1"
# df.loc[df["信息来源_InfoSource"] == "半年报", "信息来源_InfoSource"] = "Q2"
# df.loc[df["信息来源_InfoSource"] == "中期报告", "信息来源_InfoSource"] = "Q2"
# df.loc[df["信息来源_InfoSource"] == "半年度报告", "信息来源_InfoSource"] = "Q2"
# df.loc[df["信息来源_InfoSource"] == "第三季报", "信息来源_InfoSource"] = "Q3"
df.loc[df["信息来源_InfoSource"] == "年度报告", "信息来源_InfoSource"] = "Q4"

df["code"] = df["公司代码_CompanyCode"]
df["name"] = df["最新公司全称_LComNm"]
df["end_date"] = df["截止日期_EndDt"]
df["put_date"] = df["信息发布日期_InfoPubDt"]
df["source"] = df["信息来源_InfoSource"]
df["zc"] = df["资产总计(元)_TotAss"]
df = df[["code", "name", "end_date", "put_date", "source", "zc"]]
df = df.set_index("code")
df["year"] = df["end_date"].dt.year

df = df[df['year']>=2013]
df = df[df['year']<=2022]

# |%%--%%| <vpMKHxQ3UN|EW87eNpryh>

# 选出季报数量大于39的公司
df.sort_values(["code", "put_date"], inplace=True)

report_amount = pd.DataFrame(df.index.value_counts())
chosen = df.loc[report_amount[report_amount["count"] == 10].index, :]

code = chosen.index.unique()
years = [i for i in range(2014, 2023)]
judger = 0

for i in code:
    tmp = chosen.loc[i, :]["year"].values
    for j in years:
        if j not in tmp:
            print(i, j)
            judger = 1

if judger == 0:
    print("年份正常")

# |%%--%%| <EW87eNpryh|5UMByDlkZo>

group = df['zc'].groupby(df['year'])
result = group.sum()
result.to_csv("../data/人工智能企业资产合计.csv")

