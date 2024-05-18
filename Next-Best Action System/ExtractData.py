import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pytz
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import pyodbc
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pythermalcomfort.models import at
from pythermalcomfort.utilities import v_relative
import numpy as np


# Initialize the main dictionary
sensors2 = {}
sensors1 = {}

# Example data for demonstration purposes
collected_data1 = []
collected_data2 = []

# Application information
APPID = "sensors-openlab@ttn"
PSW = 'NNSXS.AKU22YDKMFUNHGKYVJMMQVDLOBYMQBLAACLENZA.2KOWOPCVUXWCLN6SVP4LRZUYKBKMP7XDWB7OJHQENFMTVF4JSLFA'
APPEUIs_AM107 = ["q4-1003-7456", "eui-24e124128c147470", "eui-24e124128c147446", "eui-24e124710c408089", "eui-24e124128c147500", "eui-24e124128c147204", "eui-24e124725c461468"]
APPEUIs_AM300 = ["am3019-testqc2090", "am307-9074"]

# Sensor name mapping
sensors_name = {
    "q4-1003-7456": "Q4-1003",
    "eui-24e124128c147470": "UNKNOWN",
    "eui-24e124128c147446": "UNKNOWN",
    "eui-24e124710c408089": "OpenLab - Laser Room",
    "eui-24e124128c147500": "OpenLab - Main Room",
    "eui-24e124128c147204": "DigitalLab",
    "eui-24e124725c461468": "Test AM103 qc2090",
    "am3019-testqc2090": "Test device qc2090",
    "am307-9074": "Computer Room"
}

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

            if device_id in APPEUIs_AM107:
                # AM107
                activity = decoded_payload.get("activity")
                co2 = decoded_payload.get("co2")
                humidity = decoded_payload.get("humidity")
                illumination = decoded_payload.get("illumination")
                infrared = decoded_payload.get("infrared")
                infrared_and_visible = decoded_payload.get("infrared_and_visible")
                pressure = decoded_payload.get("pressure")
                temperature = decoded_payload.get("temperature")
                tvoc = decoded_payload.get("tvoc")

                print("Activity:", activity)
                print("CO2:", co2)
                print("Humidity:", humidity)
                print("Illumination:", illumination)
                print("Infrared:", infrared)
                print("Infrared and Visible:", infrared_and_visible)
                print("Pressure:", pressure)
                print("Temperature:", temperature)
                print("TVOC:", tvoc)

                collected_data1.append([timestamp, room_name, co2, humidity, illumination, temperature, tvoc])

                if room_name not in sensors2:
                    sensors2[room_name] = {}
                sensors2[room_name][timestamp] = [co2, humidity, illumination, temperature, tvoc]

                # Save data to Excel after printing sensor data
                #save_data_to_excel(collected_data1, "sensor_data_AM107.xlsx")

            elif device_id in APPEUIs_AM300:
                # AM300
                co2 = decoded_payload.get("co2")
                humidity = decoded_payload.get("humidity")
                light_level = decoded_payload.get("light_level")
                o3 = decoded_payload.get("o3")
                pir = decoded_payload.get("pir")
                pm10 = decoded_payload.get("pm10")
                pm2_5 = decoded_payload.get("pm2_5")
                pressure = decoded_payload.get("pressure")
                temperature = decoded_payload.get("temperature")
                tvoc = decoded_payload.get("tvoc")

                print("CO2:", co2)
                print("Humidity:", humidity)
                print("Light Level:", light_level)
                print("O3:", o3)
                print("PIR:", pir)
                print("PM10:", pm10)
                print("PM2.5:", pm2_5)
                print("Pressure:", pressure)
                print("Temperature:", temperature)
                print("TVOC:", tvoc)

                collected_data2.append([timestamp, room_name, co2, humidity, light_level, o3, pm10, pm2_5, temperature, tvoc])

                if room_name not in sensors2:
                    sensors2[room_name] = {}
                sensors2[room_name][timestamp] = [co2, humidity, light_level, o3, pm10, pm2_5, temperature, tvoc]

                # Save data to Excel after printing sensor data
                #save_data_to_excel(collected_data2, "sensor_data_AM300.xlsx")
            else:
                print("Unknown device type:", device_id)
        else:
            print("Error: Unknown device ID")
    except Exception as e:
        print("Error:", e)

# MQTT client setup
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu1.cloud.thethings.network", 1883, 60)

mqttc.loop_forever()
