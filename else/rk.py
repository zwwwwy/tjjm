import pandas as pd
import numpy as np
import mtb
import matplotlib.pyplot as plt
from mtb.tools import prefer_settings

prefer_settings()
df = pd.read_csv("./rk.csv")

# |%%--%%| <VLBxmjTiIg|2ppEdD46Ph>

df.isna().sum()

# |%%--%%| <2ppEdD46Ph|8GocjXnWMs>

df.describe()

# |%%--%%| <8GocjXnWMs|myXcd0WPjQ>

corr = mtb.corr_heatmap(df, figsize=(30, 30), save_path="./corr.png")

# corr.index[5:]

# |%%--%%| <myXcd0WPjQ|gTjM82WX1C>

plt.figure(figsize=(15, 15))
plt.plot(corr.iloc[5:, 1])
plt.xticks(rotation="vertical")
plt.show()
#|%%--%%| <gTjM82WX1C|K4cfbppSmM>

sr = pd.read_csv('./sr.csv')
mtb.corr_heatmap(sr,figsize=(30,15),save_path='./sr.png')

