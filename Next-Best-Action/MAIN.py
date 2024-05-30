from ExtractData import *
import threading
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

            #function miguel: input = json actualizado
                # return json with +1 predcited

            timestamps, aiq_values, apparent_temps = process_data(data) #devolver predicted data de las functiones de miguel
                        #aiq_predicted  #apparent_predicted         #current and #data +1

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
    mqtt_client = setup_mqtt()

    # Start MQTT client in a new thread
    mqtt_thread = threading.Thread(target=start_mqtt_client, args=(mqtt_client,))
    mqtt_thread.start()

    # Start file monitoring in the main thread or another thread if preferred
    file_monitoring_thread = threading.Thread(target=start_monitoring, args=('C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/sensor_data_json',))
    file_monitoring_thread.start()

    # Optional: Wait for these threads if necessary
    mqtt_thread.join()
    file_monitoring_thread.join()
