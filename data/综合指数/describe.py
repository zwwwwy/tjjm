import pandas as pd

df = pd.read_excel('./控制变量.xlsx')
df.describe().to_excel('./控制变量描述.xlsx')
#|%%--%%| <6RDHTPVsLp|NJpYUla7YW>

df2 = pd.read_excel('../医疗指标.xlsx')
df2 = df2[df2["year"]<=2022]
df2 = df2[df2["year"]>=2013]
df2

#|%%--%%| <NJpYUla7YW|tXpLJ7BR61>

df3 = pd.read_excel('../人工智能指标.xlsx')
df3 = df3[df3["year"]<=2022]
df3 = df3[df3["year"]>=2013]


#|%%--%%| <tXpLJ7BR61|Mz4OuIFcJ3>

df2.describe().to_excel('./医疗指标描述.xlsx')
df3.describe().to_excel('./人工智能指标描述.xlsx')

#|%%--%%| <Mz4OuIFcJ3|w80lNQprwU>



