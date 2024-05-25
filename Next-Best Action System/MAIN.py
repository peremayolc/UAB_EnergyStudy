
from ExtractData import *

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from Plotting import *
from ComfortMeasures import *

class JsonFileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # This function is called when a file is modified
        print('find modified')
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
    print(f"Starting to monitor: {path}")
    event_handler = JsonFileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
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
