import pandas as pd
from mtb.tools import prefer_settings

prefer_settings()
zls = pd.read_csv("./中国_有效量_发明专利_国内.csv")
rk = pd.read_csv("./中国_总人口.csv")

# |%%--%%| <KFJNoVkmMP|ED52Oo3BHe>

zls = zls.rename(columns={"指标名称": "year"})
zls = zls.iloc[:-2, :]
zls["year"] = pd.to_datetime(zls["year"])
zls["year"] = zls["year"].dt.year
zls = zls[["year", "中国:有效量:发明专利:国内"]]
zls = zls.set_index("year")
rk = rk[["指标名称", "中国:总人口"]]
rk = rk.rename(columns={"指标名称": "year"})
rk = rk.iloc[:-2, :]
rk["year"] = pd.to_datetime(rk["year"])
rk["year"] = rk["year"].dt.year
rk = rk.set_index("year")

# |%%--%%| <ED52Oo3BHe|SSeCn0Vndd>

grouped = zls.groupby(zls.index)
zls = grouped.max()
zls = zls[zls.index >= 2013]
zls = zls[zls.index <= 2022]
zls

# |%%--%%| <SSeCn0Vndd|t9VcQUgwGR>

rk = rk[rk.index >= 2013]
rk = rk[rk.index <= 2022]
grouped = rk.groupby(rk.index)
rk = grouped.sum()
rk = rk * 10000
# |%%--%%| <t9VcQUgwGR|06lOolOFls>

result = pd.DataFrame(
    columns=["year", "人均专利保有量（件/人）"],
    data=[
        {
            "year": zls.index[i],
            "人均专利保有量（件/人）": zls.values[i][0] / rk.values[i][0],
        }
        for i in range(len(zls.index))
    ],
)

result.set_index("year")

result.to_csv("./人均专利保有量.csv", index=False)
#|%%--%%| <06lOolOFls|3rptICq8Js>

rk_mean = rk/9598077
# rk_mean.to_csv("人口密度(人/平方千米).csv", index=False)
rk_mean.to_csv("./人口密度(人平方千米).csv")

