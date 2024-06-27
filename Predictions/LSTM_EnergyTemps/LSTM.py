'''
Imports
'''
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import LSTM
from keras.callbacks import EarlyStopping

print('Imports done')

'''
Load dataset
'''
dataset = pd.read_csv('Merged.csv')
print(dataset.head())

# Convert DateTime column to datetime
dataset['DateTime'] = pd.to_datetime(dataset['DateTime'])
dataset.index = dataset['DateTime']
del dataset['DateTime']

# Manually specify column names
dataset.columns = ['HumitatRelMax', 'VelVent', 'DirVent', 'Temp', 'HumRel', 'Precip', 'Sol', 'TempMax', 'TempMin', 'HumRelMin', 'PrecipMax', 'Energy']
dataset.index.name = 'DateTime'

values = dataset.values

# Integer encode direction (assuming 'DirVent' is the 3rd column, index 2)
encoder = LabelEncoder()
values[:, 2] = encoder.fit_transform(values[:, 2])

# Ensure all data is float
values = values.astype('float32')

# Normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

'''
Convert series to supervised learning
'''
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # Input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # Forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1)) for j in range(n_vars)]
    # Put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # Drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

# Frame as supervised learning
reframed = series_to_supervised(scaled, 1, 1)

# Keep the Energy column as the target, drop the others
reframed.drop(reframed.columns[[i for i in range(len(dataset.columns)) if dataset.columns[i] != 'Energy']], axis=1, inplace=True)
print(reframed.head())

'''
Split data by date
'''
split_date1 = '2022-01-01'
split_date2 = '2023-01-01'
train = reframed.loc[:split_date1].values
validation = reframed.loc[split_date1:split_date2].values
test = reframed.loc[split_date2:].values

# Split into input and outputs
train_X, train_y = train[:, :-1], train[:, -1]
val_X, val_y = validation[:, :-1], validation[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

# Reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
val_X = val_X.reshape((val_X.shape[0], 1, val_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

print(train_X.shape, train_y.shape, val_X.shape, val_y.shape, test_X.shape, test_y.shape)

'''
Design and train the LSTM model
'''
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

# Define early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=7, verbose=1, restore_best_weights=True)

# Fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(val_X, val_y), verbose=2, callbacks=[early_stopping], shuffle=False)

# Plot history
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

'''
Evaluate the model
'''
# Make a prediction
yhat = model.predict(test_X)

# Reshape test_X to be 2D [samples, features]
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

# Concatenate the predicted values with the original features
inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)

# Calculate the number of columns that were dropped
original_feature_count = scaled.shape[1]
current_feature_count = reframed.shape[1]
dropped_columns = original_feature_count - current_feature_count + 1

# Add the dropped columns back as zeros to match the original number of features
inv_yhat = concatenate((inv_yhat, np.zeros((inv_yhat.shape[0], dropped_columns))), axis=1)

# Invert scaling for forecast
inv_yhat = scaler.inverse_transform(inv_yhat)

# Extract the forecasted energy
inv_yhat = inv_yhat[:, np.where(dataset.columns == 'Energy')[0][0]]

# Invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)

# Add the dropped columns back as zeros to match the original number of features
inv_y = concatenate((inv_y, np.zeros((inv_y.shape[0], dropped_columns))), axis=1)

# Invert scaling for actual
inv_y = scaler.inverse_transform(inv_y)

# Extract the actual energy
inv_y = inv_y[:, np.where(dataset.columns == 'Energy')[0][0]]

# Calculate RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

'''
Save the model
'''
model.save('lstm_model.keras')

'''
Plot the predictions values
'''
# Plot the actual 'Energy' values of the validation set
plt.figure(figsize=(10,6))
plt.plot(val_y, label='Actual Energy')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.title('Actual Energy')
plt.legend()
plt.show()

# Plot the actual 'Energy' values of the test set
plt.figure(figsize=(10,6))
plt.plot(inv_y, label='Actual Energy')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.title('Actual Energy')
plt.legend()
plt.show()

# Plot the predicted 'Energy' values
plt.figure(figsize=(10,6))
plt.plot(inv_yhat, label='Predicted Energy', color='orange')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.title('Predicted Energy')
plt.legend()
plt.show()

# Plot the actual 'Energy' values of the test set with the predicted ones
plt.figure(figsize=(10,6))
plt.plot(inv_y, label='Actual Energy')
plt.plot(inv_yhat, label='Predicted Energy', color='orange')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.title('Evaluation Energy')
plt.legend()
plt.show()
