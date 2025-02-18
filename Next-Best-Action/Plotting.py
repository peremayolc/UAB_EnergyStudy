import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp, v_relative
import time
from recommender import *
# Function to determine the current state based on sensor data


def read_sensor_data(file_path):
    retry_count = 0
    while retry_count < 3:  # Try to read the file up to 3 times
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            retry_count += 1
            time.sleep(0.5)  # Wait for 0.5 seconds before trying again
    raise Exception(f"Failed to read {file_path} after several attempts.")

def process_data(data):
    entries = [(datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S"), entry) for entry in data]
    entries.sort(key=lambda x: x[0])

    timestamps = []
    aiq_values = []
    apparent_temps = []

    for date_time, entry in entries:
        timestamps.append(date_time)
        co2 = entry.get('co2')
        print(co2)
        humidity = entry.get('humidity')
        temp = entry.get('temperature')
        tvoc = entry.get('tvoc')
        o3 = entry.get('o3')  # Using .get() for optional fields
        pm10 = entry.get('pm10')
        pm2_5 = entry.get('pm2_5')

        air_speed = 0.1  # Assumption
        met = 1.2
        clo = 0.5
        
        #predicted aiq = funcion miguel
        #predicted apparent = function miguel

        aiq = calculate_aiq(co2, tvoc, o3, pm10, pm2_5)
        apparent_temp = calculate_apparent_temp(temp, humidity, air_speed, met, clo)

        aiq_values.append(aiq)
        apparent_temps.append(apparent_temp)
    
    current_state, problem_type  = determine_state(aiq, apparent_temp, external_temp = 25, external_conditions= 'sunny', illumination = 250)

    return timestamps, aiq_values, apparent_temps, current_state, problem_type


def plot_and_save_TEMP(timestamps, temp_values, title, plot_id): #predicted temps and predicted aiq
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

    plot_file_path = os.path.join('C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/sensor_data_jpg/TEMP', f"{plot_id}.jpg")
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

    plot_file_path = os.path.join('C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/sensor_data_jpg/AIQ', f"{plot_id}.jpg")
    plt.savefig(plot_file_path, format='jpg')
    plt.close()