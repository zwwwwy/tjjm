import pandas as pd
from mtb.tools import prefer_settings
from sklearn.linear_model import Ridge

prefer_settings()

df = pd.read_csv("./FUCK.csv")
# |%%--%%| <zW7cDTHub4|UoLntlqUZJ>

df = df.iloc[:, 1:]
Y = df.iloc[:, 1]
X = df.drop("Index_HM", axis=1)

# |%%--%%| <UoLntlqUZJ|fiXfTgB1kt>

ridge_reg = Ridge(alpha=0.1939)
ridge_reg.fit(X, Y)

#|%%--%%| <fiXfTgB1kt|RmxMMc884N>

ridge_reg.coef_

