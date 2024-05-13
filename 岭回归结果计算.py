import pandas as pd
import mtb

df = pd.read_csv('./r2.csv')
df
#|%%--%%| <23kBd6yZfM|bGYQUbRkuL>

mtb.regression_report(df['pred'],df['real'])

#|%%--%%| <bGYQUbRkuL|x8pLWnp2Z0>

df

#|%%--%%| <x8pLWnp2Z0|Eq6XAl8WRg>

from scipy.stats import f_oneway
f, p = f_oneway(df['real'],df['pred'])
f

