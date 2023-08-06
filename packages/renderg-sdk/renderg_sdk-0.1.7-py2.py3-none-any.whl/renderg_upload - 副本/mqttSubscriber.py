import time

import paho.mqtt.client as mqtt


class MqttClient:
    client = None
    callbacks = {}
    rc = None

    def __init__(self, username, password):
        if MqttClient.client is None:
            broker_address = "v.renderg.com"
            port = 1883

            MqttClient.client = mqtt.Client(username)
            MqttClient.client.on_connect = MqttClient.on_connect
            MqttClient.client.on_message = MqttClient.on_message
            MqttClient.client.connect(broker_address, port)
            if username and password:
                MqttClient.client.username_pw_set(username, password)
            MqttClient.client.loop_start()
            time.sleep(5)

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
        else:
            print("Connection failed with code {rc}".format(rc=rc))
        MqttClient.rc = rc

    @staticmethod
    def on_message(client, userdata, message):
        print('收到消息')
        topic = message.topic
        payload = message.payload.decode('utf-8')
        if topic in MqttClient.callbacks:
            callback = MqttClient.callbacks[topic]
            callback(payload)

    @staticmethod
    def connect_status():
        return MqttClient.rc

    @staticmethod
    def subscribe(topic, callback):
        while True:
            if MqttClient.rc == 0:
                print('订阅主题：{topic}'.format(topic=topic))
                MqttClient.client.subscribe(topic, qos=0)
                MqttClient.callbacks[topic] = callback
                break
            else:
                time.sleep(1)

    @staticmethod
    def unsubscribe(topic):
        if topic in MqttClient.callbacks:
            del MqttClient.callbacks[topic]
            MqttClient.client.unsubscribe(topic)
