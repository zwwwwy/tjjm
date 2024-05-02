import pandas as pd
import numpy as np
from mtb.tools import prefer_settings

prefer_settings()

df = pd.read_csv("../original_data/人工智能公司季报.csv")
# df.set_index("公司代码_CompanyCode", inplace=True)
df["截止日期_EndDt"] = pd.to_datetime(df["截止日期_EndDt"])

df = df[df["信息来源_InfoSource"] != "审计报告"]
df.loc[df["信息来源_InfoSource"] == "第一季报", "信息来源_InfoSource"] = "Q1"
df.loc[df["信息来源_InfoSource"] == "半年报", "信息来源_InfoSource"] = "Q2"
df.loc[df["信息来源_InfoSource"] == "中期报告", "信息来源_InfoSource"] = "Q2"
df.loc[df["信息来源_InfoSource"] == "半年度报告", "信息来源_InfoSource"] = "Q2"
df.loc[df["信息来源_InfoSource"] == "第三季报", "信息来源_InfoSource"] = "Q3"
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

# |%%--%%| <rICmlSNLIA|EW87eNpryh>

# 选出季报数量大于39的公司
df.sort_values(["code", "put_date"], inplace=True)

report_amount = pd.DataFrame(df.index.value_counts())
chosen = df.loc[report_amount[report_amount["count"] > 38].index, :]

code = chosen.index.unique()
years = [i for i in range(2014, 2024)]
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

len(chosen.index.unique())

# |%%--%%| <5UMByDlkZo|HRcQzLnmCr>

df_lst = []
columns = chosen.columns.tolist()
columns.extend(["idx", "code"])


def processor(code, num_q, tmp_year, idx):
    if num_q > 1:
        q = tmp_year[tmp_year["source"] == code].iloc[-1, :]
        q["idx"] = idx
    elif num_q == 0:
        q = pd.DataFrame(columns=columns)
        q = q.set_index("code")
        q.loc[i, :] = None
        q.loc[i, "source"] = code
        q.loc[i, "idx"] = idx
    else:
        q = tmp_year[tmp_year["source"] == code].iloc[0, :]
        q["idx"] = idx
    return q


for i in code:
    tmp = chosen.loc[i, :]
    idx = -4
    for year in years:
        idx += 4
        tmp_year = tmp[tmp["year"] == year]
        tmp.loc[:, "idx"] = None
        source = tmp_year["source"].values.tolist()

        num_q1 = source.count("Q1")
        num_q2 = source.count("Q2")
        num_q3 = source.count("Q3")
        num_q4 = source.count("Q4")

        if num_q1 == 1 and num_q2 == 1 and num_q3 == 1 and num_q4 == 1:
            tmp_year.loc[:, "idx"] = [idx + 1, idx + 2, idx + 3, idx + 4]
            df_lst.append(tmp_year)

        else:

            q1 = processor("Q1", num_q1, tmp_year, idx + 1)
            q2 = processor("Q2", num_q2, tmp_year, idx + 2)
            q3 = processor("Q3", num_q3, tmp_year, idx + 3)
            q4 = processor("Q4", num_q4, tmp_year, idx + 4)

            error_lst = []

            for z in [q1, q2, q3, q4]:
                if len(z) != 1:
                    error_lst.append(pd.DataFrame(z).T)
                else:
                    error_lst.append(z)
            tmp_year = pd.concat(error_lst)

            df_lst.append(tmp_year)


# |%%--%%| <HRcQzLnmCr|ywyQEthCBX>

df = pd.concat(df_lst)
df.isna().sum()

# |%%--%%| <ywyQEthCBX|EKbtB0KdtP>

import mtb

judger = 0
k = 0
error_code = []
full_code = []

for i in code:
    current = df.loc[i, :]
    if current["zc"].isna().sum() > 0:
        error_code.append(i)
        k += 1
        predict_x = current[current["zc"].isna()]["idx"].values
        x = current[~current["zc"].isna()]["idx"].values
        y = current[~current["zc"].isna()]["zc"].values[-10:]
        a = mtb.Grey_model_11()
        a.fit(y)
        a.predict(1)
        print("#" * 70)
        if predict_x[0] != 40:
            judger = 1
    else:
        full_code.append(i)
if judger == 0:
    print(f"均为末位缺失, 缺失{k}个")

# |%%--%%| <EKbtB0KdtP|dJtgkd57Fw>

full_df = df[df.index.isin(full_code)]
data = full_df["zc"].groupby(full_df["idx"]).sum()
time = []
for i in range(2014, 2024):
    for j in range(1, 5):
        time.append(f"{i}Q{j}")
result = pd.DataFrame()
result["时间"] = time
result["资产"] = data.values

result.to_csv("./data/人工智能代表公司季报资产.csv", index=False)
# |%%--%%| <dJtgkd57Fw|aIOMTwCbou>

df
