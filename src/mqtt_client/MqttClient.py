import logging
import random
from abc import abstractmethod

import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class MqttClient:
    opposite_mqtt = None

    def __init__(self, host, port, user_id, name):
        self.host = host
        self.port = port
        self.userId = user_id
        self.name = name
        self.mqtt_client = mqtt.Client(''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 33)))
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect(self.host, self.port, 60)

    def on_connect(self, client, user_data, flags, rc):
        logger.debug(self.name + "on connect success")
        pass

    def on_subscribe(self, client, user_data, mid, granted_qos):
        logger.debug(self.name + "on subscribe success")

    def on_disconnect(self, client, user_data, rc):
        logger.debug(self.name + "on disconnect ")

    @abstractmethod
    def on_message(self, client, user_data, msg):
        logger.debug(self.name + "receive topic:  " + msg.topic + ",    payload:" + str(msg.payload.decode("utf-8")))

    def send_msg(self, topic, payload):
        logger.debug(self.name + "send topic:  " + topic + ",payload: " + payload)
        self.mqtt_client.publish(topic=topic, payload=payload)

    def set_opposite_mqtt(self, mqtt_client):
        self.opposite_mqtt = mqtt_client

    def start(self):
        self.mqtt_client.loop_forever()
