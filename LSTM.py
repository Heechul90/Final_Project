import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



data = pd.read_csv('Data/Watt(시계열 일별 전체 전력량).csv',
                   encoding = 'euc-kr')
data.head()
data['yearmonthday'] = data['yearmonthday'].astype(str)
data.dtypes




data['yearmonthday'] = pd.to_datetime(data['yearmonthday'])
data.dtypes
data = data.set_index('yearmonthday')

data.plot()



split_date = pd.Timestamp('31-12-2017')
# 2011/1/1 까지의 데이터를 트레이닝셋.
# 그 이후 데이터를 테스트셋으로 한다.

train = data.loc[:split_date, ['elec']]
test = data.loc[split_date:, ['elec']]
# Feature는 Unadjusted 한 개

ax = train.plot()
test.plot(ax=ax)
plt.legend(['train', 'test'])



from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler()

train_sc = sc.fit_transform(train)
test_sc = sc.transform(test)

train_sc


train_sc_df = pd.DataFrame(train_sc, columns=['Scaled'], index=train.index)
test_sc_df = pd.DataFrame(test_sc, columns=['Scaled'], index=test.index)
train_sc_df.head()


for s in range(1, 13):
    train_sc_df['shift_{}'.format(s)] = train_sc_df['Scaled'].shift(s)
    test_sc_df['shift_{}'.format(s)] = test_sc_df['Scaled'].shift(s)

train_sc_df.head(13)


X_train = train_sc_df.dropna().drop('Scaled', axis=1)
y_train = train_sc_df.dropna()[['Scaled']]

X_test = test_sc_df.dropna().drop('Scaled', axis=1)
y_test = test_sc_df.dropna()[['Scaled']]



X_train = X_train.values
X_test = X_test.values

y_train = y_train.values
y_test = y_test.values
print(X_train.shape)
print(X_train)
print(y_train.shape)
print(y_train)



X_train_t = X_train.reshape(X_train.shape[0], 12, 1)
X_test_t = X_test.reshape(X_test.shape[0], 12, 1)

print("최종 DATA")
print(X_train_t.shape)
print(X_train_t)
print(y_train)






from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense
import keras.backend as K
from keras.callbacks import EarlyStopping


K.clear_session()
model = Sequential() # Sequeatial Model
model.add(LSTM(20, input_shape=(12, 1))) # (timestep, feature)
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.summary()



early_stop = EarlyStopping(monitor='loss', patience=1, verbose=1)

history = model.fit(X_train_t, y_train,
                    epochs=500,
                    batch_size=10,
                    verbose=1,
                    callbacks=[early_stop])

print("\n Test Accuracy: %.4f" % (model.evaluate(X_test, y_test)[1]))

print(X_test_t)

y_pred = model.predict(X_test_t)
print(y_pred)

len(y_pred)