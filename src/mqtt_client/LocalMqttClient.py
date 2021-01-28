from src.mqtt_client.MqttClient import MqttClient

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class LocalMqttClient(MqttClient):
    def __init__(self, host, port, user_id, name):
        super(LocalMqttClient, self).__init__(host, port, user_id, name)
        self.mqtt_client.subscribe(topic="{sign}/down".format(sign='+'))

    def on_message(self, client, user_data, msg):
        super(LocalMqttClient, self).on_message(client, user_data, msg)
        payload = str(msg.payload.decode("utf-8"))
        topic = msg.topic
        target = str(self.userId) + "/"
        to_remote_topic = target + topic
        logger.debug("local  mqtt client  send topic:  " + to_remote_topic + ",    payload:" + payload)
        self.opposite_mqtt.send_msg(to_remote_topic, payload)
