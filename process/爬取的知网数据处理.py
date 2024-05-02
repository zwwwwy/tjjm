import pandas as pd
import matplotlib.pyplot as plt
from mtb.tools import prefer_settings

prefer_settings()

df = pd.read_csv('../data/爬取的知网论文数据.csv')
#|%%--%%| <GvKDuX9dop|VbKBkm8FMJ>

result = df['发表时间'].str[:4].value_counts()
result = result.reset_index()
result['发表时间'] = result['发表时间'].astype(int)
result = result.sort_values(by='发表时间')
result['发表时间'] = result['发表时间'].astype(str)

plt.plot(result['发表时间'], result['count'])
for i in range(len(result)):
    plt.vlines(result['发表时间'][i], 0, result['count'][i], linestyles='dashed')
plt.show()
