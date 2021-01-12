import _thread
import json
import os
import time
from xml.dom.minidom import parse

from MqttClient import MqttClient


def start_mqtt(thread_name, mqtt):
    mqtt.start()


if __name__ == '__main__':
    docEnv = os.popen('echo $docEnv')  # 需要替换
    docEnvStr = docEnv.read()
    docEnvJson = json.loads(docEnvStr)
    userId = docEnvJson["userId"]
    print(str(userId))
    domTree = parse("config.xml")
    rootNode = domTree.documentElement
    local_mqtt_url = rootNode.getElementsByTagName("local_mqtt_url")[0].childNodes[0].data
    local_mqtt_port = rootNode.getElementsByTagName("local_mqtt_port")[0].childNodes[0].data
    remote_mqtt_url = rootNode.getElementsByTagName("remote_mqtt_url")[0].childNodes[0].data
    remote_mqtt_port = rootNode.getElementsByTagName("remote_mqtt_port")[0].childNodes[0].data
    localMqtt = MqttClient("local", local_mqtt_url, int(local_mqtt_port), userId)
    remoteMqtt = MqttClient("remote", remote_mqtt_url, int(remote_mqtt_port), userId)
    localMqtt.set_opposite_mqtt(remoteMqtt)
    remoteMqtt.set_opposite_mqtt(localMqtt)
    try:
        _thread.start_new_thread(start_mqtt, ("localMqttThread", localMqtt,))
        _thread.start_new_thread(start_mqtt, ("remoteMqttThread", remoteMqtt,))
    except:
        print("error thread start")
    while True:
        time.sleep(1)

