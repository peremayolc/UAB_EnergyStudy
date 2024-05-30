import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError


def ComputerRoom_temp(json_file, uni_model_temp = 'Recommender/Models/Unidirectional 1 LSTM model.h5', df_train_file = 'Recommender/csv_train/Computer_Room_train_temp.csv'):

    ComputerRoom_json = pd.DataFrame(json_file)
    ComputerRoom_json['timestamp'] = pd.to_datetime(ComputerRoom_json['timestamp'])
    ComputerRoom_json['Month'] = ComputerRoom_json['timestamp'].dt.month
    ComputerRoom_json['Hour'] = ComputerRoom_json['timestamp'].dt.hour
    ComputerRoom_json['Minutes'] = ComputerRoom_json['timestamp'].dt.minute

    ComputerRoom_json = ComputerRoom_json[['timestamp','Month', 'Hour', 'Minutes', 'light_level', 'temperature']]
    last_row = ComputerRoom_json.iloc[-1]
    new_timestamp = last_row['timestamp'] + pd.Timedelta(minutes=10)

    new_row = {
        'timestamp': new_timestamp,
        'Month': new_timestamp.month,
        'Hour': new_timestamp.hour,
        'Minutes': new_timestamp.minute,
        'light_level': last_row['light_level'],  
        'temperature': 0  
    }
    ComputerRoom_json = ComputerRoom_json.append(new_row, ignore_index=True)
    #print(ComputerRoom_json)

    #RS COLUMN
    url = "https://www.radiacionsolar.es/cerdanyola-del-valles.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    radiation_values = [int(v.get_text().strip()) for v in soup.select('#RHDia1 strong')]
    hours = [int(h.get_text().strip()[:-3]) for h in soup.select('.hora')][:len(radiation_values)]
    radiation_data = pd.DataFrame({'Hour': hours, 'RS_outdoor': radiation_values})

    def get_radiation_value(row):
        matching_row = radiation_data[radiation_data['Hour'] == row['Hour']]
        if not matching_row.empty:
            return matching_row.iloc[0]['RS_outdoor']
        return None

    ComputerRoom_json['RS_outdoor'] = ComputerRoom_json.apply(get_radiation_value, axis=1)
    ComputerRoom_json = ComputerRoom_json.fillna(0)
    #print(ComputerRoom_json)

    #TM COLUMN
    url = "https://weather.com/weather/hourbyhour/l/63283ca65cbdbe646d6a62f6838cd1e92711f32c1ad68b21065fafd6d2c32a5a"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    hours = [h.get_text().strip() for h in soup.select('.DetailsSummary--daypartName--kbngc')][:23]
    temperatures_fahrenheit = [int(t.get_text().strip()[:-1]) for t in soup.select('.DetailsSummary--tempValue--jEiXE')][:23]

    def convert_hour_to_24(hour_str):
        period = hour_str[-2:]
        hour = int(hour_str[:-2].strip())
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        return hour

    hours_24 = [convert_hour_to_24(hour) for hour in hours]
    temperatures_celsius = [(temp - 32) * 5.0/9.0 for temp in temperatures_fahrenheit]
    temperature_data = pd.DataFrame({'Hour': hours_24, 'TM_outdoor': temperatures_celsius})
    #print(temperature_data)

    def get_temperature_value(row):
        matching_row = temperature_data[temperature_data['Hour'] == row['Hour']]
        if not matching_row.empty:
            return matching_row.iloc[0]['TM_outdoor']
        return None

    ComputerRoom_json['TM_outdoor'] = ComputerRoom_json.apply(get_temperature_value, axis=1)
    ComputerRoom_json['TM_outdoor'].fillna(method='ffill', inplace=True)
    ComputerRoom_json = ComputerRoom_json[['Month', 'Hour', 'Minutes', 'light_level','RS_outdoor','TM_outdoor','temperature']]
    #print(ComputerRoom_json)

    #load the model
    temp_uni_model = load_model(uni_model_temp, compile=False)
    optimizer = Adam(learning_rate=0.0005)
    temp_uni_model.compile(optimizer=optimizer, loss=MeanSquaredError())

    df_train = pd.read_csv(df_train_file)
    scaler= StandardScaler()
    scaler.fit(df_train)

    y_mean=df_train['temperature'].mean()
    y_std=scaler.scale_[df_train.shape[1]-1]
    #print(y_mean, y_std)

    lags = 14
    for i in range(lags, len(ComputerRoom_json)):
        X_test = ComputerRoom_json.iloc[i-lags:i].copy()
        X_test_scaled = scaler.transform(X_test)

        val = temp_uni_model.predict(X_test_scaled.reshape(1, lags, X_test_scaled.shape[1]))
        val2 = y_std * val[:, 0] + y_mean
        ComputerRoom_json.loc[i, 'temperature'] = val2

    ComputerRoom_json['temperature'] = ComputerRoom_json['temperature'].round(2)
    #print(ComputerRoom_json)
    last_row_json = ComputerRoom_json.iloc[-1].to_json()
    #print(last_row_json)

    with open('last_row.json', 'w') as file:
        file.write(last_row_json)

with open("Next-Best-Action/sensor_data_json/Computer_Room.json", 'r') as f:
        json_data = json.load(f)

ComputerRoom_temp(json_file = json_data)