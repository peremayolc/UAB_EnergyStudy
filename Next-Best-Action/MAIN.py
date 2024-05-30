from ExtractData import *
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from Plotting import *
from ComfortMeasures import *
from drive_upload import authenticate_drive, upload_file

class JsonFileChangeHandler(FileSystemEventHandler):
    def __init__(self, drive_service, folder_id=None):
        self.drive_service = drive_service
        self.folder_id = folder_id
        super().__init__()

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

            # Execute plotting functions and get file paths
            temp_plot_path = plot_and_save_TEMP(timestamps, apparent_temps, f"Apparent Temp for {plot_id}", plot_id)
            aiq_plot_path = plot_and_save_AIQ(timestamps, aiq_values, f"AIQ for {plot_id}", plot_id)

            # Upload the plots to Google Drive
            upload_file(self.drive_service, temp_plot_path, self.folder_id)
            upload_file(self.drive_service, aiq_plot_path, self.folder_id)

def start_monitoring(path, drive_service, folder_id=None):
    print(f"Starting to monitor: {path}")
    event_handler = JsonFileChangeHandler(drive_service, folder_id)
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

    # Authenticate and get the Google Drive client
    drive_service = authenticate_drive()

    # Specify the correct Google Drive folder ID where you want to save the files
    folder_id = '1PuFfVamE2cC-9mfCxCM9BpEcC4NLttg-'  # Replace with your actual folder ID

    # Start file monitoring in the main thread or another thread if preferred
    file_monitoring_thread = threading.Thread(target=start_monitoring, args=('C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/sensor_data_json', drive_service, folder_id))
    file_monitoring_thread.start()

    # Optional: Wait for these threads if necessary
    mqtt_thread.join()
    file_monitoring_thread.join()
