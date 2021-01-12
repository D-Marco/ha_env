# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class MqttClient:
    oppositeMqtt = None

    def on_connect(self, client, userdata, flags, rc):
        # logger.debug('send data to mqtt topic:%s , payload:%s' % (topic, msg_recv))
        logger.debug(self.name + " mqtt on connect success")

    def on_message(self, client, userdata, msg):
        payload = str(msg.payload.decode("utf-8"))
        topic = msg.topic
        logger.debug(self.name + " mqtt receive topic:" + topic + ",payload:" + payload)
        if self.name == "local":
            target = str(self.userId) + "/"
            to_remote_topic = target + topic
            logger.debug(self.name + " mqtt send topic:" + to_remote_topic + ",payload:" + payload)
            self.oppositeMqtt.send_msg(to_remote_topic, payload)
        if self.name == "remote":
            target = str(self.userId) + "/"
            target_index = topic.index(target) + len(target)
            to_local_topic = topic[target_index:]
            if len(to_local_topic) != 0:
                logger.debug(self.name + " mqtt send topic:=" + to_local_topic + ",payload:=" + payload)
                self.oppositeMqtt.send_msg(to_local_topic, payload)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def on_disconnect(self, client, userdata, rc):
        pass

    def set_opposite_mqtt(self, _mqtt):
        self.oppositeMqtt = _mqtt

    def send_msg(self, topic, payload):
        self.mqttClient.publish(topic=topic, payload=payload)

    def __init__(self, name, host, port, user_id):
        self.name = name
        self.host = host
        self.port = port
        self.userId = user_id
        self.mqttClient = mqtt.Client(name)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.on_subscribe = self.on_subscribe
        self.mqttClient.on_disconnect = self.on_disconnect
        self.mqttClient.connect(self.host, self.port, 60)
        if name == "remote":
            topic = '{user}/{sign}/up'.format(user=user_id, sign='+')
            self.mqttClient.subscribe(topic=topic)
        else:
            self.mqttClient.subscribe(topic="{sign}/down".format(sign='+'))

    def start(self):
        self.mqttClient.loop_forever()
