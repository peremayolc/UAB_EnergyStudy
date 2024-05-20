import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp  # Ensure these functions are correctly imported

# Function to read data from JSON file
def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to process the data
def process_data(data):
    timestamps = []
    aiq_values = []
    apparent_temps = []

    for entry in data:
        # Parse the date time
        date_time = datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S")
        timestamps.append(date_time)

        # Extracting relevant sensor data
        co2 = entry[3]
        tvoc = entry[4]
        temp = entry[9]
        humidity = entry[10]
        air_speed = entry[11] if entry[11] is not None else 0  # defaulting air speed to 0 if null

        # Calculate AIQ and apparent temperature
        aiq = calculate_aiq(co2, tvoc)
        apparent_temp = calculate_apparent_temp(temp, humidity, air_speed, met=1.2, clo=0.5)

        aiq_values.append(aiq)
        apparent_temps.append(apparent_temp)

    return timestamps, aiq_values, apparent_temps

# Function to plot data
def plot_data(timestamps, aiq_values, apparent_temps, title):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('AIQ', color=color)
    ax1.plot(timestamps, aiq_values, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Apparent Temperature (°C)', color=color)
    ax2.plot(timestamps, apparent_temps, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(title)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

# Main script to process all files in the directory
directory_path = 'C:/GitHub Repositories/UAB_EnergyStudy/sensor_data'
files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    try:
        data = read_sensor_data(file_path)
        timestamps, aiq_values, apparent_temps = process_data(data)
        plot_data(timestamps, aiq_values, apparent_temps, file_name.replace('.json', ''))
    except Exception as e:
        print(f"Failed to process {file_name}: {e}")
