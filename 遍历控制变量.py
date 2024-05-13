import os
import pandas as pd
import numpy as np
from tqdm import tqdm

files = os.listdir("./控制变量遍历")
df_lst = []
for i in files:
    df_lst.append(pd.read_excel(f"./控制变量遍历/{i}"))


year = pd.DataFrame(columns=["year"], data=np.arange(2013, 2023))
result = [year]
for i in tqdm(df_lst):
    length = len(result)
    for j in range(length):
        result.append(pd.concat([result[j], i], axis=1))

result.sort(key=lambda x: x.shape[1], reverse=False)
result = result[1:]

# |%%--%%| <0oMdK8Wfzv|0JAUPvux5N>

k = 0
for i in result:
    if i.shape[1] <= 4:
        continue
    k += 1
    i.to_csv(f"./控制变量结果/{k}.csv", index=False)
#|%%--%%| <0JAUPvux5N|vFPZiHqZj1>

result[0].shape

