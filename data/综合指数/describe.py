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

x = pd.read_csv('./人工智能综合指数.csv')
y = pd.read_csv('./医疗综合指数.csv')

x.rename(columns={'0':'x'},inplace=True)
x['y'] = y['0'].values

#|%%--%%| <w80lNQprwU|NrWNp07SlK>

x.describe().to_excel('./综合指数描述.xlsx')

