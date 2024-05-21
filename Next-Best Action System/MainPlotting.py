import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp
from ExtractData import *


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

def plot_and_save_TEMP(timestamps, temp_values, title, plot_id):
    plt.figure(figsize=(10, 5))
    times_of_day = [ts.strftime('%H:%M') for ts in timestamps]
    plt.plot(times_of_day, temp_values, 'bo-', label='Apparent Temperature')

    plt.ylim(17, 30)

    # Add horizontal lines for temperature thresholds
    plt.axhline(y=19, color='orange', linestyle='--', label='Min Temp Threshold (19°C)')
    plt.axhline(y=24, color='orange', linestyle='--', label='Max Temp Threshold (24°C)')

    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Apparent Temperature')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plot_file_path = os.path.join('C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_jpg/TEMP', f"{plot_id}.jpg")
    plt.savefig(plot_file_path, format='jpg')
    plt.close()


def plot_and_save_AIQ(timestamps, aiq_values, title, plot_id):
    plt.figure(figsize=(10, 5))
    times_of_day = [ts.strftime('%H:%M') for ts in timestamps]
    plt.plot(times_of_day, aiq_values, 'ro-', label='AIQ')

    plt.ylim(0, 100)

    # Add horizontal lines for AIQ thresholds
    plt.axhline(y=25, color='orange', linestyle='--', label='Min AIQ Threshold (25)')
    plt.axhline(y=75, color='orange', linestyle='--', label='Max AIQ Threshold (75)')

    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('AIQ')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plot_file_path = os.path.join('C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_jpg/AIQ', f"{plot_id}.jpg")
    plt.savefig(plot_file_path, format='jpg')
    plt.close()



directory_path = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_json'
files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    try:
        data = read_sensor_data(file_path)
        timestamps, aiq_values, apparent_temps = process_data(data)
        
        # Generate a unique ID or use filename for plot identification
        plot_id = file_name.replace('.json', '')
        
        # Plot and save AIQ
        plot_and_save_AIQ(timestamps, aiq_values, f"{plot_id} AIQ", plot_id)
        plot_and_save_TEMP(timestamps, apparent_temps, f"{plot_id} Apparent Temp", plot_id)

    except Exception as e:
        print(f"Failed to process {file_name}: {e}")


