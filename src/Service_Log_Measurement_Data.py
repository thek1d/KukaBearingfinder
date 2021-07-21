from matplotlib import animation
import paho.mqtt.client as mqtt
import json
import csv
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# MQTT Settings
MQTT_Broker = "192.168.0.33"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "BearingFinder"
MQTT_Topic_Enable_Logging = "BearingFinder/EnableDBLogging"
global mqttc
fieldnames = ["Timestamp", "Force_X", "Force_Y", "Force_Z", "Torque_X", "Torque_Y", "Torque_Z"]


def on_connect(mosq, obj, rc, properties=None):
    pass


def on_message(mosq, obj, msg):
    if msg.topic == MQTT_Topic_Enable_Logging:
        Messbox_Enable_DB_Handler(msg.topic, msg.payload)
    else:
        Messbox_Data_Handler(msg.topic, msg.payload)


def on_subscribe(mosq, obj, mid, granted_qos):
    pass


def Messbox_Enable_DB_Handler(topic, jsonData):
    global enableDBLogging
    json_Dict = json.loads(jsonData)

    enable = json_Dict['enable']
    if enable == 'true':
        enableDBLogging = True
    else:
        enableDBLogging = False


def Messbox_Data_Handler(topic, jsonData):
    # Parse Data
    global enableDBLogging
    global Forces
    if not enableDBLogging:
        return
    json_Dict = json.loads(jsonData)

    ts = json_Dict['start']

    forcex = json_Dict['forces'][0]
    forcey = json_Dict['forces'][1]
    forcez = json_Dict['forces'][2]

    external_torquex = json_Dict['external_torques'][0]
    external_torquey = json_Dict['external_torques'][1]
    external_torquez = json_Dict['external_torques'][2]

    with open('Measurement_Data.csv', 'a') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "Timestamp"  : ts,
            "Force_X"    : forcex,
            "Force_Y"    : forcey,
            "Force_Z"    : forcez,
            "Torque_X"   : external_torquex,
            "Torque_Y"   : external_torquey,
            "Torque_Z"   : external_torquez
        }

        csv_writer.writerow(info)

def main():
    global mqttc, enableDBLogging
    enableDBLogging = False

    mqttc = mqtt.Client()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    mqttc.subscribe(MQTT_Topic, 0)
    mqttc.subscribe(MQTT_Topic_Enable_Logging, 0)

    with open('Measurement_Data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    mqttc.loop_forever()


if __name__ == '__main__':
    main()

main()
