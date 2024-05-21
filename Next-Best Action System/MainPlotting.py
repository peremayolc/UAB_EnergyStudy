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




def hash_file_contents(file_path):
    """ Generate a hash of the file contents """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

class ContentChangeHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        self.file_hashes = {}
        for file in os.listdir(directory):
            if file.endswith('.json'):
                file_path = os.path.join(directory, file)
                self.file_hashes[file] = hash_file_contents(file_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            new_hash = hash_file_contents(event.src_path)
            file_name = os.path.basename(event.src_path)
            if self.file_hashes.get(file_name) != new_hash:
                print(f"Detected content change in: {event.src_path}")
                self.file_hashes[file_name] = new_hash
                self.process_file(event.src_path)

    def process_file(self, file_path):
        # Your existing processing and plotting logic
        print(f"Processing updated file: {file_path}")

def start_monitoring(path):
    event_handler = ContentChangeHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    json_directory_path = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best Action System/sensor_data_json'
    start_monitoring(json_directory_path)
    print('a')
