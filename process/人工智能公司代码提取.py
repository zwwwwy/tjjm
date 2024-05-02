import pandas as pd

df = pd.read_excel("../original_data/搜狐股票人工智能板块.xlsx")
df["股票代码"] = df["股票代码"].astype("str")

# |%%--%%| <4X9eVhBFCi|A9AwsFuQTa>

for i in df["股票代码"].values:
    length = len(i)
    if length < 6:
        print("0" * (6 - length) + i + " ", end="")
    else:
        print(i + " ", end="")
#|%%--%%| <A9AwsFuQTa|kYH5bgjOle>

df

