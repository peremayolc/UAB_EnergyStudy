import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pytz
from collections import deque
import os
# Initialize dictionaries to store data for each sensor
def setup_mqtt():
    sensor_data = {}

    # Application information
    APPID = "sensors-openlab@ttn"
    PSW = 'NNSXS.AKU22YDKMFUNHGKYVJMMQVDLOBYMQBLAACLENZA.2KOWOPCVUXWCLN6SVP4LRZUYKBKMP7XDWB7OJHQENFMTVF4JSLFA'
    APPEUIs_AM107 = ["q4-1003-7456", "eui-24e124128c147470", "eui-24e124128c147446", "eui-24e124710c408089", "eui-24e124128c147500", "eui-24e124128c147204", "eui-24e124725c461468"]
    APPEUIs_AM300 = ["am3019-testqc2090", "am307-9074"]

    # Sensor name mapping
    sensors_name = {
        "q4-1003-7456": "Q4-1003",
        "eui-24e124128c147470": "UNKNOWN1",
        "eui-24e124128c147446": "UNKNOWN2",
        "eui-24e124710c408089": "OpenLab - Laser Room",
        "eui-24e124128c147500": "OpenLab - Main Room",
        "eui-24e124128c147204": "DigitalLab",
        "eui-24e124725c461468": "Test AM103 qc2090",
        "am3019-testqc2090": "Test device qc2090",
        "am307-9074": "Computer Room"
    }

    # List of all possible variables for both sensor types
    all_possible_variables = [
        "activity", "co2", "humidity", "illumination", "infrared", "infrared_and_visible", 
        "pressure", "temperature", "tvoc", "light_level", "o3", "pir", "pm10", "pm2_5"
    ]

    # Co2 / Humid / ( illum or light ) / temp / tvoc / o3 / pm10 / pm2.5
    # Create a directory for storing sensor data files
    data_dir = 'C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/sensor_data_json'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Callback function for message reception
    def on_message(mqttc, userdata, msg):
        hour = datetime.now(pytz.timezone('Europe/Madrid'))
        hour_values = hour.strftime("%Y-%m-%d %H:%M:%S")

        print("\nMessage received, ", hour_values)

        if msg.topic.startswith('v3/' + APPID + '/devices/'):
            on_message2(mqttc, userdata, msg)

    # Callback function for MQTT connection
    def on_connect(mqttc, mosq, obj, rc):
        print("Connected with result code:" + str(rc))
        # Subscribe to the uplink messages of all devices AM107
        for appeui in APPEUIs_AM107:
            mqttc.subscribe('v3/' + APPID + '/devices/' + appeui + '/up')
            print("Subscribed to topic: v3/" + APPID + "/devices/" + appeui + "/up")

        # Subscribe to the uplink messages of all devices AM300
        for appeui in APPEUIs_AM300:
            mqttc.subscribe('v3/' + APPID + '/devices/' + appeui + '/up')
            print("Subscribed to topic: v3/" + APPID + "/devices/" + appeui + "/up")

    # Callback function for detailed message processing
    def save_data_to_file(sensor_name, data):
        filename = f"{sensor_name.replace(' ', '_')}.json"
        filepath = os.path.join(data_dir, filename)
        
        # Convert deque to a list for JSON serialization
        data_to_save = list(data)
        
        # Write the current deque (max 7 entries) to file
        with open(filepath, 'w') as file:
            json.dump(data_to_save, file)
            file.flush()
            os.fsync(file.fileno())


    def on_message2(mqttc, userdata, msg):
        payload = json.loads(msg.payload.decode())
        try:
            decoded_payload = payload["uplink_message"]["decoded_payload"]
            end_device_ids = payload["end_device_ids"]
            device_id = end_device_ids.get("device_id")

            if device_id in sensors_name:
                room_name = sensors_name[device_id]
                print("Sensor Data for", room_name + ":")

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Create a deque for the room if it does not exist
                if room_name not in sensor_data:
                    sensor_data[room_name] = deque(maxlen=14)

                # Extract all possible variables from the payload and form a dictionary
                data_dict = {"timestamp": timestamp, "room_name": room_name}
                for var in all_possible_variables:
                    data_dict[var] = decoded_payload.get(var, None)

                print(data_dict)

                # Append new data to the deque, automatically managing overflow
                sensor_data[room_name].append(data_dict)

                # Save to file
                save_data_to_file(room_name, sensor_data[room_name])
            else:
                print("Error: Unknown device ID")
        except Exception as e:
            print("Error:", e)


    def load_existing_data():
        # Ensure the directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            return  # No files to load if the directory was just created

        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                sensor_name = filename.replace('_', ' ').replace('.json', '')
                filepath = os.path.join(data_dir, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    # Ensure the deque for each sensor is initialized properly
                    if sensor_name not in sensor_data:
                        sensor_data[sensor_name] = deque(maxlen=14)
                    # Load the data into the deque
                    for item in data:
                        sensor_data[sensor_name].append(item)

    # Call the function to load data at startup
    # Load existing data from files
    load_existing_data()

    # MQTT client setup and connection
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.username_pw_set(APPID, PSW)
    mqttc.connect("eu1.cloud.thethings.network", 1883, 60)

    return mqttc


def start_mqtt_client(mqttc):
    try:
        mqttc.loop_forever()
    except Exception as e:
        print(f"An error occurred in MQTT loop: {e}")

if __name__ == "__main__":
    mqtt_client = setup_mqtt()
    start_mqtt_client(mqtt_client)