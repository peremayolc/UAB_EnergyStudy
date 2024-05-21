import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp



def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def process_data(data):
    entries = [(datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S"), entry) for entry in data]
    entries.sort(key=lambda x: x[0])

    timestamps = []
    aiq_values = []
    apparent_temps = []

    for date_time, entry in entries:
        timestamps.append(date_time)
        co2 = entry[3]
        humidity = entry[4]
        temp = entry[9]
        tvoc = entry[10]
        o3 = entry[12] if len(entry) > 12 else None
        pm10 = entry[14] if len(entry) > 14 else None
        pm2_5 = entry[15] if len(entry) > 15 else None

        air_speed = 0.1

        aiq = calculate_aiq(co2, tvoc, o3, pm10, pm2_5)
        apparent_temp = calculate_apparent_temp(temp, humidity, air_speed, met=1.2, clo=0.5)

        aiq_values.append(aiq)
        apparent_temps.append(apparent_temp)

    return timestamps, aiq_values, apparent_temps

def plot_AIQ(timestamps, aiq_values, title):
    plt.figure(figsize=(10, 5))

    # Convert datetime objects to just time (HH:MM)
    times_of_day = [ts.strftime('%H:%M') for ts in timestamps]

    # Plot using only the time of day
    plt.plot(times_of_day, aiq_values, 'ro-', label='AIQ')  # Red color, circle markers, and solid lines

    plt.title(title)
    plt.xlabel('Time of Day')
    plt.ylabel('AIQ')
    plt.xticks(rotation=45)  # Rotate labels for better legibility
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_temp(timestamps, apparent_temps, title):

    plt.figure(figsize=(10, 5))

    times_of_day = [ts.strftime('%H:%M') for ts in timestamps]

    plt.plot(times_of_day, apparent_temps, 'bo-', label='Apparent Temperature')  # Blue color, circle marker, solid line
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Apparent Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()  # This will display the legend using the label defined in plt.plot
    plt.tight_layout()
    plt.show()


directory_path = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_json'
files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    try:
        data = read_sensor_data(file_path)
        timestamps, aiq_values, apparent_temps = process_data(data)
        print(timestamps)
        plot_AIQ(timestamps, aiq_values, file_name.replace('.json', ''))
        plot_temp(timestamps, apparent_temps, file_name.replace('.json', ''))
    except Exception as e:
        print(f"Failed to process {file_name}: {e}")
