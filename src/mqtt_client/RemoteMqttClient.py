import json

from src.mqtt_client.MqttClient import MqttClient
import logging

from src.device.xiaomi import XIAOMI_DEVICE_BUILD_DIC

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


class RemoteMqttClient(MqttClient):
    config_msg_times = {}

    def __init__(self, host, port, user_id, name):
        super(RemoteMqttClient, self).__init__(host, port, user_id, name)
        topic = '{user}/{sign}/up'.format(user=user_id, sign='+')
        self.mqtt_client.subscribe(topic=topic)

    def on_message(self, client, user_data, msg):
        super(RemoteMqttClient, self).on_message(client, user_data, msg)
        payload = str(msg.payload.decode("utf-8"))
        topic = msg.topic
        self.dispatch_msg_to_local(topic, payload)

    def dispatch_msg_to_local(self, topic, payload):
        payload_json = json.loads(payload)
        serial = (topic.split('/', 3))[1]
        if "deviceType" in payload_json and payload_json["deviceType"] != '':  # 小米设备报文,deviceType由虚拟仿真平台定义的key
            device_type = payload_json["deviceType"]
            config_array = XIAOMI_DEVICE_BUILD_DIC[device_type]["config"]
            if device_type not in self.config_msg_times:
                self.config_msg_times[device_type] = 0
            if self.config_msg_times[device_type] % 10 == 0:
                for item in config_array:
                    config_topic_result = item["topic_fun"](serial)
                    config_payload_result = item["payload_fun"](serial)
                    self.opposite_mqtt.send_msg(config_topic_result, config_payload_result)

            data_topic_result = XIAOMI_DEVICE_BUILD_DIC[device_type]["data"]["topic_fun"](serial)
            data_payload_result = XIAOMI_DEVICE_BUILD_DIC[device_type]["data"]["payload_fun"](payload_json)
            self.config_msg_times[device_type] += 1
            self.opposite_mqtt.send_msg(data_topic_result, data_payload_result)
        else:  # 普通mqtt报文
            target = str(self.userId) + "/"
            target_index = topic.index(target) + len(target)
            to_local_topic = topic[target_index:]
            if len(to_local_topic) != 0:
                self.opposite_mqtt.send_msg(to_local_topic, payload)
