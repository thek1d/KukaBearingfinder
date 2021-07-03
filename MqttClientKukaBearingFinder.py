import paho.mqtt.client as mqtt
import json
import pymssql

# MQTT Settings
MQTT_Broker = "192.168.0.33"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "BearingFinder"
MQTT_Topic_Enable_Logging = "BearingFinder/EnableDBLogging"
global mqttc
global enableDBLogging
global dbObj


class DatabaseManager():
    def __init__(self):
        self.conn = pymssql.connect(server='192.168.0.48', user='bearingfinder',
                                    password='BearingFinder100%', database='KukaBearingFinder')
        # self.conn.execute('pragma foreign_keys = on')
        # self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()


def on_connect(mosq, obj, rc):
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
    if not enableDBLogging:
        return
    json_Dict = json.loads(jsonData)

    ts = json_Dict['start']

    axis1 = json_Dict['joints'][0]
    axis2 = json_Dict['joints'][1]
    axis3 = json_Dict['joints'][2]
    axis4 = json_Dict['joints'][3]
    axis5 = json_Dict['joints'][4]
    axis6 = json_Dict['joints'][5]
    axis7 = json_Dict['joints'][6]
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


    dbObj.add_del_update_db_record(
        "insert into dbo.KukaLogger(timestamp, Axis_1_j, Axis_1_mt, Axis_2_j, Axis_2_mt, Axis_3_j, Axis_3_mt, Axis_4_j, Axis_4_mt, Axis_5_j, Axis_5_mt, Axis_6_j, Axis_6_mt, Axis_7_j, Axis_7_mt, ef_x, ef_y, ef_z) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (ts, axis1, torque1, axis2, torque2, axis3, torque3, axis4, torque4, axis5, torque5, axis6, torque6, axis7, torque7, forcex, forcey, forcez))

def main():
    global dbObj, mqttc, enableDBLogging
    enableDBLogging = False
    dbObj = DatabaseManager()
    mqttc = mqtt.Client()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    mqttc.subscribe(MQTT_Topic, 0)
    mqttc.subscribe(MQTT_Topic_Enable_Logging, 0)
    mqttc.loop_forever()


if __name__ == '__main__':
    main()

main()
