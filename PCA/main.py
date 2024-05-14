import pandas as pd
import mtb
import numpy as np
from mtb.tools import prefer_settings
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

prefer_settings()

x = pd.read_excel("../data/人工智能指标.xlsx")
x = x.iloc[:, 1:]
# x = MinMaxScaler().fit_transform(x)
pd.DataFrame(x).describe()

# |%%--%%| <RqixKwFEqJ|msCnaOmMZO>

from sklearn.decomposition import PCA

pca = PCA(n_components=6)
X2D = pca.fit_transform(x)

evr = pca.explained_variance_ratio_
sum_evr = evr.cumsum()
data1 = [f"f{i}" for i in range(1, 7)]
table1 = pd.DataFrame(columns=["主成分", "方差解释比例", "累计方差解释比例"])
table1["主成分"] = data1
table1["方差解释比例"] = evr
table1["累计方差解释比例"] = sum_evr
table1.to_excel("./主成分分析贡献率.xlsx", index=False)
# |%%--%%| <msCnaOmMZO|7FMyBFXU13>

pca = PCA(n_components=2)
X2D = pca.fit_transform(x)
pca.components_
data2 = [f"x{i}" for i in range(1, 7)]
table2 = pd.DataFrame(columns=data2, data=pca.components_)
table2["f"] = ["f1", "f2"]
table2 = table2.set_index("f")
table2.to_excel("./主成分分析因子载荷矩阵.xlsx")

# |%%--%%| <7FMyBFXU13|VHpimz7QhQ>


k = 0
result = "f_1="
for i in table2.loc["f1"]:
    k += 1
    result += f"{round(i,4)}\cdot x{k}"
print(result)
k = 0
result = "f_2="
for i in table2.loc["f2"]:
    k += 1
    result += f"{round(i,4)}\cdot x{k}"
print(result)
# |%%--%%| <VHpimz7QhQ|mFlBo1QTN8>

l1 = table1.iloc[0, 1]
l2 = table1.iloc[1, 1]
result = X2D[:, 0] * l1 / (l1 + l2) + X2D[:, 1] * l2 / (l1 + l2)
result = MinMaxScaler().fit_transform(result.reshape(-1, 1))
result = pd.DataFrame(result, columns=["f"])
result["year"] = range(2013, 2023)
result.set_index("year", inplace=True)
result.to_csv("../data/综合指数/PCA_人工智能综合指数.csv")
#|%%--%%| <mFlBo1QTN8|Smms8SUjiC>

from sklearn.decomposition import KernelPCA
kpca = KernelPCA(n_components=2, kernel="rbf", gamma=0.04)
X2D = kpca.fit_transform(x)
X2D
