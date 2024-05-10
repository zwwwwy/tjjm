import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mtb.tools import prefer_settings

prefer_settings()

df = pd.read_csv("../original_data/人均可支配收入（季度）.csv")
df = df.T
tmp = df.iloc[1:, :]
df = pd.DataFrame(columns=["时间", "收入累计值"])
df["时间"] = tmp.index
df["收入累计值"] = tmp.values.reshape(
    len(tmp.values),
)

# |%%--%%| <qCBvyioNR0|yjrdXmefeW>

time_lst = []
years = np.arange(2014, 2024)
seasons = np.array(["第一季度", "第二季度", "第三季度", "第四季度"])
for year in years:
    k = 0
    for season in seasons:
        k += 1
        time_lst.append({f"{year}年{season}": f"{year}Q{k}"})


df = df[df["时间"].isin([list(i.keys())[0] for i in time_lst])]
for i in time_lst:
    df["时间"] = df["时间"].replace(i)

df["year"] = df["时间"].str.extract(r"(\d{4})")

df = df.sort_values("时间")
# |%%--%%| <yjrdXmefeW|EeocrZCwL7>

diff_result = []
for i in df["year"].unique():
    data = df[df["year"] == i]
    tmp = data.iloc[0, 1]
    data["收入"] = data["收入累计值"].diff()
    data.fillna(tmp, inplace=True)
    diff_result.append(data)
diff_df = pd.concat(diff_result)
plt.plot(diff_df["时间"], diff_df["收入"],label='差分')
plt.plot(df["时间"], df["收入累计值"],label='原始')
plt.legend()
plt.show()
#|%%--%%| <EeocrZCwL7|uufxPXwtCc>

diff_df.to_csv("../dathandled_dataa/人均可支配收入.csv", index=False)

