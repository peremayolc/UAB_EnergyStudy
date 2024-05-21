import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp  # Ensure these functions are correctly imported
from ExtractData import *
# Function to read data from JSON file
def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to process the data
def process_data(data):
    # Extract data and parse timestamps
    entries = [(datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S"), entry) for entry in data]
    # Sort entries based on timestamps
    entries.sort(key=lambda x: x[0])

    timestamps = []
    aiq_values = []
    apparent_temps = []

    for date_time, entry in entries:
        timestamps.append(date_time)

        # Assuming the indices are mapped correctly to your data structure
        co2 = entry[3]
        humidity = entry[4]
        temp = entry[9]
        tvoc = entry[10]
        o3 = entry[12]
        pm10 = entry[14]
        pm2_5 = entry[15]

        air_speed = 0.1  # Assuming a constant air speed; modify as necessary

        # Calculate AIQ and apparent temperature
        aiq = calculate_aiq(co2, tvoc, o3, pm10, pm2_5)
        apparent_temp = calculate_apparent_temp(temp, humidity, air_speed, met=1.2, clo=0.5)

        aiq_values.append(aiq)
        apparent_temps.append(apparent_temp)
        print('a')

    return timestamps, aiq_values, apparent_temps


# Function to plot data
def plot_AIQ(timestamps, aiq_values, title):
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, aiq_values, marker='o', linestyle='-', color='red')  # Continuous line
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('AIQ')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_temp(timestamps, apparent_temps, title):
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, apparent_temps, marker='o', linestyle='-', color='blue')  # Continuous line
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Apparent Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main script to process all files in the directory
directory_path = 'C:/GitHub Repositories/UAB_EnergyStudy/sensor_data'
files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    try:
        data = read_sensor_data(file_path)
        timestamps, aiq_values, apparent_temps = process_data(data)
        plot_AIQ(timestamps, aiq_values, file_name.replace('.json', ''))
        plot_temp(timestamps,apparent_temps, file_name.replace('.json', ''))
    except Exception as e:
        print(f"Failed to process {file_name}: {e}")
