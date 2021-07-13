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
fieldnames = ["Timestamp", "Force_X", "Force_Y", "Force_Z", "Torqe_X", "Torqe_Y", "Torqe_Z"]


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

    axis1   = json_Dict['joints'][0]
    axis2   = json_Dict['joints'][1]
    axis3   = json_Dict['joints'][2]
    axis4   = json_Dict['joints'][3]
    axis5   = json_Dict['joints'][4]
    axis6   = json_Dict['joints'][5]
    axis7   = json_Dict['joints'][6]
    torque1 = json_Dict['torques'][0]
    torque2 = json_Dict['torques'][1]
    torque3 = json_Dict['torques'][2]
    torque4 = json_Dict['torques'][3]
    torque5 = json_Dict['torques'][4]
    torque6 = json_Dict['torques'][5]
    torque7 = json_Dict['torques'][6]

    forcex = json_Dict['forces'][0]
    forcey = json_Dict['forces'][1]
    forcez = json_Dict['forces'][2]

    torqex = json_Dict['external_torqes'][0]
    torqey = json_Dict['external_torqes'][1]
    torqez = json_Dict['external_torqes'][2]

    with open('forces.csv', 'a') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "Timestamp" : ts,
            "Force_X"   : forcex,
            "Force_Y"   : forcey,
            "Force_Z"   : forcez,
            "Torqe_X"   : torqex,
            "Torqe_Y"   : torqey,
            "Torqe_Z"   : torqez
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

    with open('forces.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    mqttc.loop_forever()


if __name__ == '__main__':
    main()

main()
