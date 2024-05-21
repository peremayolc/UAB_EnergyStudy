import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from ComfortMeasures import calculate_aiq, calculate_apparent_temp, v_relative
from ExtractData import *

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


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


class ChangeHandler(FileSystemEventHandler):
    """Handle file system events - focusing on modified files."""
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.jpg'):
            print(f"JPEG file changed: {event.src_path}")
            # Add your logic here for what happens when a file is modified

def monitor_folder(path):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    return observer

if __name__ == "__main__":
    # Folders to monitor
    folder1 = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_json'
    folder2 = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_json'

    observer1 = monitor_folder(folder1)
    observer2 = monitor_folder(folder2)

    print("Monitoring started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer1.stop()
        observer2.stop()

    observer1.join()
    observer2.join()

