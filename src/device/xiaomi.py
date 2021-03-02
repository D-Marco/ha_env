import json


def build_config_topic(device_type, serial, alias):
    """
    返回设备配置的主题
    :param device_type:  设备类型，如sensor, binary_sensor,switch
    :param serial: 设备串号
    :param alias: 设备别名
    :return: 
    """
    return 'homeassistant/{sensor_type}/{serial}/{alias}/config'.format(sensor_type=device_type, serial=serial, alias=alias)


def build_ill_sensor_ill_config_topic(serial):
    return build_config_topic("sensor", serial, "illuminance_lux")


def build_person_sensor_person_config_topic(serial):
    return build_config_topic("binary_sensor", serial, "occupancy")


def build_th_sensor_temp_config_topic(serial):
    return build_config_topic("sensor", serial, "temperature")


def build_th_sensor_hump_config_topic(serial):
    return build_config_topic("sensor", serial, "humidity")


def build_magnetic_sensor_magnetic_config_topic(serial):
    return build_config_topic("binary_sensor", serial, "contact")


def build_leak_sensor_leak_config_topic(serial):
    return build_config_topic("binary_sensor", serial, "water_leak")


def build_smoke_sensor_smoke_config_topic(serial):
    return build_config_topic("binary_sensor", serial, "smoke")


def build_alarm_switch_config_topic(serial):
    return build_config_topic("switch", serial, "alarm")


def build_config_payload(serial, manufacturer_name, model_name, class_name, short_name, device_type, unit="", binary_reverse=False):
    """

    :param serial: 设备串号
    :param manufacturer_name: 产商名称
    :param model_name: 设备模块名称
    :param class_name: 设备类名（前端用于分类设备图标和样式）
    :param short_name: 设备下的某个传感器或执行器的名称
    :param device_type: 设备类型，0:binary_sensor; 1:sensor 2:switch
    :param unit: 传感器单位
    :param binary_reverse: 二进制传感器是否需要数值对调
    :return: json字符串
    """
    payload = {}
    device_obj = {"identifiers": ["zigbee2mqtt_" + serial], "manufacturer": manufacturer_name, "model": model_name, "name": serial, "sw_version": "Zigbee2MQTT 1.17.0"}
    payload["device"] = device_obj
    if device_type != 2:
        payload["device_class"] = class_name

    payload["json_attributes_topic"] = "zigbee2mqtt/" + serial
    payload["name"] = "{serial} {short_name}".format(serial=serial, short_name=short_name)
    payload["state_topic"] = "zigbee2mqtt/" + serial
    payload["unique_id"] = "{serial}_{short_name}_zigbee2mqtt".format(serial=serial, short_name=short_name)
    if device_type == 0:
        payload["payload_off"] = binary_reverse
        payload["payload_on"] = not binary_reverse
        payload["value_template"] = "{{ value_json." + short_name + " }}"

    if device_type == 1:
        payload["unit_of_measurement"] = unit
        payload["value_template"] = "{{ value_json." + short_name + " }}"

    if device_type == 2:
        payload["command_topic"] = "{serial}/down".format(serial=serial, short_name=short_name)
        payload["payload_off"] = '{"status":"0"}'
        payload["payload_on"] = '{"status":"1"}'
        payload["state_off"] = "OFF"
        payload["state_on"] = "ON"
    return json.dumps(payload)


def build_ill_sensor_ill_config_payload(serial):
    """
    返回小米光照传感器中光照配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "MiJia light intensity sensor (GZCGQ01LM)", "illuminance", "illuminance_lux", 1, "lx")


def build_person_sensor_person_config_payload(serial):
    """
    返回小米温人体传感器的人体配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "Aqara human body movement and illuminance sensor (RTCGQ11LM)", "motion", "occupancy", 0)


def build_th_sensor_temp_config_payload(serial):
    """
    返回小米温湿度传感器中温度的配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "Aqara temperature, humidity and pressure sensor (WSDCGQ11LM)", "temperature", "temperature", 1, "°C")


def build_th_sensor_hum_config_payload(serial):
    """
    返回小米温湿度传感器中湿度的配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "Aqara temperature, humidity and pressure sensor (WSDCGQ11LM)", "humidity", "humidity", 1, "%")


def build_magnetic_sensor_door_config_payload(serial):
    """
    返回小米门磁传感器的门磁配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "Aqara door & window contact sensor (MCCGQ11LM)", "door", "contact", 0, binary_reverse=True)


def build_water_sensor_leak_config_payload(serial):
    """
    返回小米水浸传感器的水浸配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "Aqara water leak sensor (SJCGQ11LM)", "moisture", "water_leak", 0)


def build_smoke_sensor_smoke_config_payload(serial):
    """
    返回小米烟雾传感器的烟雾配置payload
    :param serial:
    :return:
    """
    return build_config_payload(serial, "Xiaomi", "MiJia Honeywell smoke detector (JTYJ-GD-01LM/BW)", "smoke", "smoke", 0)


def build_alarm_config_payload(serial):
    return build_config_payload(serial, "Xiaomi", "MiJia simulate alarm", "", "alarm", 2)


def build_data_topic(serial):
    """
     构建传感器数据发送主题
    :param serial:
    :return:
    """
    return "zigbee2mqtt/{serial}".format(serial=serial)


def parse_ill_data(json_data):
    """
     构建光照传感器数据payload
    :param json_data: 原生仿真平台数据
    :return:
    """
    return json.dumps({"illuminance_lux": json_data["illuminance_lux"]})


def parse_person_data(json_data):
    """
    构建人体体感器数据payload
    :param json_data: 原生仿真平台数据
    :return:
    """
    return json.dumps({"occupancy": True if json_data["occupancy"] == "1" else False})


def parse_th_data(json_data):
    """
    构建温湿度传感器数据payload
    :param json_data: 原生仿真平台数据
    :return:
    """
    return json.dumps({"humidity": json_data["humidity"], "temperature": json_data["temperature"]})


def parse_magnetic_data(json_data):
    """
    构建门磁传感器数据payload
    :param json_data: 原生仿真平台数据
    :return:
    """
    return json.dumps({"contact": False if json_data["contact"] == "1" else True})


def parse_leak_data(json_data):
    """
    构建水浸传感器数据payload
    :param json_data: 原生仿真平台数据
    :return:
    """
    return json.dumps({"water_leak": True if json_data["water_leak"] == "1" else False})


def parse_smoke_data(json_data):
    """
    构建烟雾传感器数据payload
    :param json_data: 原生仿真平台数据
    :return:
    """
    return json.dumps({"smoke": True if json_data["smoke"] == "1" else False})


def parse_alarm_data(json_data):
    return json_data["status"]


XIAOMI_DEVICE_BUILD_DIC = {
    "illumination_xiaomi": {"config": [{"topic_fun": build_ill_sensor_ill_config_topic, "payload_fun": build_ill_sensor_ill_config_payload}],
                            "data": {"topic_fun": build_data_topic, "payload_fun": parse_ill_data}},

    "body_xiaomi": {"config": [{"topic_fun": build_person_sensor_person_config_topic, "payload_fun": build_person_sensor_person_config_payload}],
                    "data": {"topic_fun": build_data_topic, "payload_fun": parse_person_data}},

    "humiture_xiaomi": {"config": [{"topic_fun": build_th_sensor_temp_config_topic, "payload_fun": build_th_sensor_temp_config_payload},
                                   {"topic_fun": build_th_sensor_hump_config_topic, "payload_fun": build_th_sensor_hum_config_payload}],
                        "data": {"topic_fun": build_data_topic, "payload_fun": parse_th_data}},

    "door_xiaomi": {"config": [{"topic_fun": build_magnetic_sensor_magnetic_config_topic, "payload_fun": build_magnetic_sensor_door_config_payload}],
                    "data": {"topic_fun": build_data_topic, "payload_fun": parse_magnetic_data}},

    "water_leak_xiaomi": {"config": [{"topic_fun": build_leak_sensor_leak_config_topic, "payload_fun": build_water_sensor_leak_config_payload}],
                          "data": {"topic_fun": build_data_topic, "payload_fun": parse_leak_data}},

    "smoke_xiaomi": {"config": [{"topic_fun": build_smoke_sensor_smoke_config_topic, "payload_fun": build_smoke_sensor_smoke_config_payload}],
                     "data": {"topic_fun": build_data_topic, "payload_fun": parse_smoke_data}},

    "alarmLamp_xiaomi": {"config": [{"topic_fun": build_alarm_switch_config_topic, "payload_fun": build_alarm_config_payload}],
                         "data": {"topic_fun": build_data_topic, "payload_fun": parse_alarm_data}}
}
