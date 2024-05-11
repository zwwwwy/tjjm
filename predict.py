import mtb
import pandas as pd

df = pd.read_csv('./data/综合指数/医疗综合指数.csv')

#|%%--%%| <WyAq7BJ8px|QRfqgmCS2i>

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense

# 假设我们的输入数据是10个时间步长的序列，每个时间步长有50个特征
input_shape = (10, 50)

# 创建一个Sequential模型
model = Sequential()

# 添加一个SimpleRNN层
# 我们设置32个单元，这是RNN层的输出维度
model.add(SimpleRNN(32, input_shape=input_shape))

# 添加一个Dense层，用于分类输出
# 假设我们有10个类别，所以我们设置10个单元
model.add(Dense(10, activation='softmax'))

# 编译模型，设置损失函数，优化器和评估指标
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 打印模型的概要
model.summary()


#|%%--%%| <QRfqgmCS2i|TDu4V833OS>

model.fit(df['0'].values+0.1, epochs=100, batch_size=1, verbose=1)

