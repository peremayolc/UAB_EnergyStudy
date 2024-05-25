import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp, v_relative
#from ExtractData import *

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from watchdog.events import LoggingEventHandler
import hashlib


def read_sensor_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print("Data loaded:", data)  # Add this line to print the loaded data
    return data

def process_data(data):
    entries = [(datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S"), entry) for entry in data]
    entries.sort(key=lambda x: x[0])

    timestamps = []
    aiq_values = []
    apparent_temps = []

    for date_time, entry in entries:
        timestamps.append(date_time)
        co2 = entry.get('co2')
        humidity = entry.get('humidity')
        temp = entry.get('temperature')
        tvoc = entry.get('tvoc')
        o3 = entry.get('o3', None)  # Using .get() for optional fields
        pm10 = entry.get('pm10', None)
        pm2_5 = entry.get('pm2_5', None)

        air_speed = 0.1  # Assumption

        aiq = calculate_aiq(co2, tvoc, o3, pm10, pm2_5)
        apparent_temp = calculate_apparent_temp(temp, humidity, air_speed)

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

class JsonFileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # This function is called when a file is modified
        if event.is_directory:
            return
        if event.src_path.endswith('.json'):
            print(f"Detected change in: {event.src_path}")
            data = read_sensor_data(event.src_path)
            timestamps, aiq_values, apparent_temps = process_data(data)

            # Extract the plot_id or sensor name from filename
            plot_id = os.path.basename(event.src_path).split('.')[0]

            # Execute plotting functions
            plot_and_save_TEMP(timestamps, apparent_temps, f"Apparent Temp for {plot_id}", plot_id)
            plot_and_save_AIQ(timestamps, aiq_values, f"AIQ for {plot_id}", plot_id)


def start_monitoring(path):
    event_handler = JsonFileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)  # Set recursive=True if subdirectories should also be monitored
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    json_files_directory = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_json'
    start_monitoring(json_files_directory)
