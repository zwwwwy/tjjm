import pandas as pd

df = pd.read_excel("./地区gdp.xlsx")
df = df.iloc[28:, :]
df.rename(columns={"Unnamed: 0": "year"}, inplace=True)

df["year"] = pd.to_datetime(df["year"])
df["year"] = df["year"].dt.year
df["year"] = df["year"].astype(int)
# |%%--%%| <azchdrHJen|axL7T2ZMFW>
df = df[df["year"] >= 2013]
df = df[df["year"] <= 2022]

s = df.iloc[:, 1:].std(axis=1)
m = df.iloc[:, 1:].mean(axis=1)

# |%%--%%| <axL7T2ZMFW|w8bqDahS8U>

result = pd.DataFrame(columns=["year"], data=range(2013,2023))
result['变异系数'] = (s / m).values
result.to_excel("../../控制变量遍历/地区gdp变异系数.xlsx", index=False)

