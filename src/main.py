import _thread
import json
import os
import sys
import time

cur_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path + "/..")
from xml.dom.minidom import parse
from src.mqtt_client.LocalMqttClient import LocalMqttClient
from src.mqtt_client.RemoteMqttClient import RemoteMqttClient


def start_mqtt(mqtt):
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

    local_mqtt = LocalMqttClient(local_mqtt_url, int(local_mqtt_port), userId, "local mqtt client ")
    remote_mqtt = RemoteMqttClient(remote_mqtt_url, int(remote_mqtt_port), userId, "remote mqtt client ")

    local_mqtt.set_opposite_mqtt(remote_mqtt)
    remote_mqtt.set_opposite_mqtt(local_mqtt)
    try:
        _thread.start_new_thread(start_mqtt, (local_mqtt,))
        _thread.start_new_thread(start_mqtt, (remote_mqtt,))
    except:
        print("error thread start")
    while True:
        time.sleep(1)
