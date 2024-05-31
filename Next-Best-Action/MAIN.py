from ExtractData import *
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

from Plotting import *
from ComfortMeasures import *

from modelwork import *

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

            if event.src_path == 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/sensor_data_json/Computer_Room.json':
                ComputerRoom_temp(json_file = data)

            timestamps, aiq_values, apparent_temps, current_state, problem_type = process_data(data) #devolver predicted data de las functiones de miguel
                        #aiq_predicted  #apparent_predicted         #current and #data +1

            
            
            # Extract the plot_id or sensor name from filename
            plot_id = os.path.basename(event.src_path).split('.')[0]

            # Execute plotting functions
            plot_and_save_TEMP(timestamps, apparent_temps, f"Apparent Temp for {plot_id}", plot_id)
            plot_and_save_AIQ(timestamps, aiq_values, f"AIQ for {plot_id}", plot_id)

            if current_state:
                # Get the top two actions for the current state
                actions = get_top_actions(current_state)
                if problem_type == 'AIQ Threshold Problem':
                    if actions is not None:
                        first_action, second_action = actions
                        print(f"Recommended Actions:\n1. {first_action}\n2. {second_action}")
                    else:
                        print("No recommended actions found for the current state.")
                if problem_type == 'Temperature Low Problem' or 'Temperature High Problem':
                    if actions is not None:
                        first_action, second_action = actions
                        print(f"Recommended Actions:\n1. {first_action}\n2. {second_action}")
                    else:
                        print("No recommended actions found for the current state.")

            else:
                print("The classroom is within comfort thresholds.")


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
