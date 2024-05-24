import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pytz
import psycopg2
import io

# Initialize dictionaries to store data for each sensor
sensor_data = {}

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

# List of all possible variables for both sensor types
all_possible_variables = [
    "activity", "co2", "humidity", "illumination", "infrared", "infrared_and_visible", 
    "pressure", "temperature", "tvoc", "light_level", "o3", "pir", "pm10", "pm2_5"
]

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="a",
    host="localhost"
)
cur = conn.cursor()

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

            # Extract all possible variables from the payload
            data = {
                "timestamp": timestamp,
                "room_name": room_name,
            }
            for var in all_possible_variables:
                data[var] = decoded_payload.get(var, None)

            print(data)

            # Save data to PostgreSQL
            save_data_to_postgresql(device_id, room_name, timestamp, data)
        else:
            print("Error: Unknown device ID")
    except Exception as e:
        print("Error:", e)

def save_data_to_postgresql(device_id, room_name, timestamp, data):
    cur.execute("""
        INSERT INTO sensor_data (device_id, room_name, timestamp, data)
        VALUES (%s, %s, %s, %s)
    """, (device_id, room_name, timestamp, json.dumps(data)))
    conn.commit()

# MQTT client setup and connection
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
print("test")
mqttc.username_pw_set(APPID, PSW)
mqttc.connect("eu1.cloud.thethings.network", 1883, 60)
print("test2")
mqttc.loop_forever()

# Don't forget to close the database connection when the application terminates
cur.close()
conn.close()
