import pandas as pd
from tqdm import tqdm
from mtb.tools import prefer_settings
import math
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import callbacks
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

prefer_settings()


# |%%--%%| <ECbFJu67jK|eQjO35mWh9>

df1 = pd.read_csv("./gold1.csv")
df2 = pd.read_csv("./gold2.csv")
df = pd.concat([df1, df2])
df = df[["交易日期_TrdDt", "收盘价(元/克)_ClPr", "合约代码_ContCd"]]

df["交易日期_TrdDt"] = pd.to_datetime(df["交易日期_TrdDt"])
df = df.rename(
    columns={
        "交易日期_TrdDt": "Trddt",
        "收盘价(元/克)_ClPr": "Clsprc",
        "合约代码_ContCd": "cd",
    }
)

# |%%--%%| <eQjO35mWh9|kct8pvDlww>

group = df[["Trddt", "Clsprc"]].groupby(["Trddt"])
mean_clsprc = group.mean()
mean_clsprc = mean_clsprc.reset_index()

# |%%--%%| <kct8pvDlww|mf1JcnFtYc>

# 填充缺失值并以收盘价计算日收益率和平均日收益率
# fj2_data = fj2_data.sort_values(["Stkcd", "Trddt"])
# fj2_stkcd = fj2_data["Stkcd"].unique()
# sort_list = []
# average_earning_list = []
# for i in tqdm(fj2_stkcd):
#     tmp = fj2_data[fj2_data["Stkcd"] == i]
#     start_date = tmp["Trddt"].min()
#     end_date = tmp["Trddt"].max()
#     date_range = pd.date_range(start=start_date, end=end_date)
#     tmp = tmp.set_index("Trddt").reindex(date_range).rename_axis("Trddt").reset_index()
#     tmp.fillna(method="ffill", inplace=True)
#     tmp["earning_rate"] = tmp["Clsprc"].pct_change()
#     average_earning_list.append(
#         pd.DataFrame(
#             {"Stkcd": [i], "average_earning_rate": [tmp["earning_rate"].mean()]}
#         )
#     )
#     sort_list.append(tmp)
#
#
# fj2_data = pd.concat(sort_list)
# average_earning = pd.concat(average_earning_list)

# |%%--%%| <mf1JcnFtYc|aK6q9G2dkI>


def genWindows(x, y, window_size):
    x_out = []
    y_out = []
    length = x.shape[0]
    for i in range(window_size, length):
        x_out.append(x[i - window_size : i])
        y_out.append(y[i])
    return np.array(x_out), np.array(y_out)


def rnn_test(data):
    data = data.set_index("Trddt")

    data["previous_Clsprc"] = data["Clsprc"].shift(1)
    data = data.dropna()
    # 归一化
    # features = data[
    #     ["Opnprc", "Hiprc", "Loprc", "Clsprc", "Dnshrtrd", "Dnvaltrd", "Dsmvosd"]
    # ]
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # features = scaler.fit_transform(features)
    # data[["Opnprc", "Hiprc", "Loprc", "Clsprc", "Dnshrtrd", "Dnvaltrd", "Dsmvosd"]] = (
    #     features
    # )
    features = data[["Clsprc", "previous_Clsprc"]]
    scaler = MinMaxScaler(feature_range=(0, 1))
    features = scaler.fit_transform(features)
    data[["Clsprc", "previous_Clsprc"]] = features

    # 按0.8比例划分训练集和测试集并构建滑窗数据

    x = data.drop(columns=["Clsprc"])
    y = data["Clsprc"]

    split_point = math.floor(len(data) * 0.8)
    # x = x[["Opnprc", "Hiprc", "Loprc", "Dnshrtrd", "Dnvaltrd", "Dsmvosd"]]
    x = x[["previous_Clsprc"]]
    x_train = x[:split_point]
    y_train = y[:split_point]
    x_test = x[split_point:]
    y_test = y[split_point:]

    x_train_windows, y_train_windows = genWindows(
        x_train.to_numpy(), y_train.to_numpy(), 5
    )
    x_test_windows, y_test_windows = genWindows(x_test.to_numpy(), y_test.to_numpy(), 5)

    early_stopping = callbacks.EarlyStopping(
        monitor="loss", patience=10, restore_best_weights=True
    )

    input_shape = (x_train_windows.shape[1], x_train_windows.shape[2])
    model = Sequential(
        [
            layers.Input(shape=input_shape),
            # layers.SimpleRNN(units=128, return_sequences=True),
            # layers.SimpleRNN(64, return_sequences=False),
            # layers.Dense(1, activation="linear"),
            layers.LSTM(units=128, return_sequences=True),
            layers.LSTM(64, return_sequences=False),
            layers.Dense(1, activation="linear"),
            # layers.TimeDistributed(layers.Dense(1)),
        ]
    )

    optimizer = keras.optimizers.Nadam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="mse")
    model.summary()

    batch_size = 20
    epochs = 50
    model.fit(
        x_train_windows,
        y_train_windows,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=[early_stopping],
    )

    pred_train_y = model.predict(x_train_windows)
    # print(pred_train_y)
    fig, axs = plt.subplots(1, 2)
    axs[0].plot(np.array(y_train), label="预测值")
    axs[0].plot(pred_train_y, label="真实值")
    axs[0].legend()
    axs[0].set_title("金价收盘价均值历史数据预测", fontsize=15)

    pred_test_y = model.predict(x_test_windows)

    axs[1].plot(np.array(y_test), label="预测值")
    axs[1].plot(pred_test_y, label="真实值")
    axs[1].legend()
    axs[1].set_title("金价收盘价均值未来数据预测", fontsize=15)
    plt.show()

    # mtb.regression_report(pred_test_y, y_test_windows)


rnn_test(mean_clsprc)
# |%%--%%| <aK6q9G2dkI|9qIKZphodg>


def rnn(data, step=90):
    data = data.set_index("Trddt")

    data["previous_Clsprc"] = data["Clsprc"].shift(1)
    data = data.dropna()
    # 归一化
    features = data[["Clsprc", "previous_Clsprc"]]
    scaler = MinMaxScaler(feature_range=(0, 1))
    features = scaler.fit_transform(features)
    data[["Clsprc", "previous_Clsprc"]] = features

    # 按0.8比例划分训练集和测试集并构建滑窗数据

    x = data.drop(columns=["Clsprc"])
    y = data["Clsprc"]

    x = x[["previous_Clsprc"]]

    x_train_windows, y_train_windows = genWindows(x.to_numpy(), y.to_numpy(), 5)

    early_stopping = callbacks.EarlyStopping(
        monitor="loss", patience=10, restore_best_weights=True
    )

    input_shape = (x_train_windows.shape[1], x_train_windows.shape[2])
    # input_shape = (1, 1)
    model = Sequential(
        [
            layers.Input(shape=input_shape),
            # layers.LSTM(units=128, return_sequences=True),
            # layers.LSTM(64, return_sequences=True),
            # layers.TimeDistributed(layers.Dense(1)),
            layers.LSTM(units=128, return_sequences=True),
            layers.LSTM(64, return_sequences=False),
            layers.Dense(1, activation="linear"),
        ]
    )

    optimizer = keras.optimizers.Nadam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="mse")

    batch_size = 20
    epochs = 50
    model.fit(
        x_train_windows,
        y_train_windows,
        # x,
        # y,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=[early_stopping],
    )

    result_lst = []
    tmp = x_train_windows[-1]
    for i in range(step):
        result = model.predict([tmp])

        tmp = np.vstack([tmp[1:], result[-1]])
        result_lst.append(result[-1][0])
    var = np.var(np.array(result_lst))
    # tmp = x
    # for i in range(step):
    #     result = model.predict(tmp)
    #     tmp = np.vstack([tmp[1:], result[-1]])
    #     result_lst.append(result[-1][0])

    return result_lst, var


# |%%--%%| <9qIKZphodg|9Alqa2PSTi>

result = rnn(mean_clsprc)

#|%%--%%| <9Alqa2PSTi|imGhYl75F7>

result

# |%%--%%| <imGhYl75F7|ZztImPiJDF>

# result_dics = []
# for i in tqdm(fj2_data["Stkcd"].unique()):
#     data = fj2_data[fj2_data["Stkcd"] == i]
#     result = rnn(data)
#     result_dics.append({"Stkcd": i, "result": result[-1]})
# |%%--%%| <ZztImPiJDF|XKB3SlwzQo>

import multiprocessing


def process_data(stock_code):
    data = fj2_data[fj2_data["Stkcd"] == stock_code]
    if len(data) < 500:
        return {"Stkcd": stock_code, "result": None}
    result, var = rnn(data)
    return {"Stkcd": stock_code, "result": result[-1], "var": var}


pool = multiprocessing.Pool()
result_dics = list(
    tqdm(
        pool.imap(process_data, fj2_data["Stkcd"].unique()),
        total=len(fj2_data["Stkcd"].unique()),
    )
)
pool.close()
pool.join()
# |%%--%%| <XKB3SlwzQo|E2StmwyQUj>

result_dics
