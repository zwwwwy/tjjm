import pandas as pd
df1 = pd.read_csv("./人工智能综合指数.csv")
df2 = pd.read_csv('./医疗综合指数.csv')
df3 = pd.read_csv('./控制变量.csv')
df = pd.concat([df1,df2,df3],axis=1)
print(df)
