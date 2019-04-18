import json
import paho.mqtt.client as mqtt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


BROKER_IP = "140.112.18.2"
PORT = 11053
LAG_TIME = 600
TOPIC = "device"

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))

def on_publish(client, userdata, mid):
    print("A new message is published!")

def on_message(client, userdata, msg):
    # Do something
    from .models import DeviceInfo, DeviceTemperature, DeviceHumidity, DeviceLight
    topic_r = str(msg.topic)
    msg_r = str(msg.payload)
    msg_r = msg_r[2:-1]
    info_set = msg_r.split(",")
    uuid = info_set[0]
    device_exist = DeviceInfo.objects.filter(uuid=uuid)

    if topic_r == "device/connect/info":
        if not device_exist:
            device = DeviceInfo()
            device.uuid = uuid
            device.host = info_set[2]
            device.os_name = info_set[3]
            device.save()
        else:
            device_exist = device_exist[0]
            device_exist.online = True
            device_exist.save()
            print ("Connect!")
    elif topic_r == "device/disconnect/uuid":
        if device_exist:
            device_exist = device_exist[0]
            device_exist.online = False
            device_exist.save()
    elif topic_r == "device/connect/sensor/DHT":
        if device_exist:
            temperature = DeviceTemperature()
            temperature.uuid = uuid
            temperature.value = float(info_set[2])
            temperature.timestamp = info_set[3]

            humidity = DeviceHumidity()
            humidity.uuid = uuid
            humidity.value = float(info_set[1])
            humidity.timestamp = info_set[3]

            temperature.save()
            humidity.save()
            print ("success dht")
    elif topic_r == "device/connect/sensor/light":
        if device_exist:
            light = DeviceLight()
            light.uuid = uuid
            light.value = float(info_set[1])
            light.timestamp = info_set[2]
            light.save()
            print ("success light")
    elif topic_r == "device/search/info":
        print (msg_r)
        find_device = True
        if device_exist:
            device_exist = device_exist[0]
            if device_exist.online:
                find_device = False
        if find_device:
            room_group_name = 'display_search'
            channel_layer = get_channel_layer()
            info_dict = dict()
            info_dict['message'] = "Find Device"
            info_dict['uuid'] = uuid
            info_dict['host'] = info_set[2]
            info_dict['os_name'] = info_set[3]
            info_json = json.dumps(info_dict)
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'find_device',
                    'message': info_json
                }
            )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, PORT, LAG_TIME)
client.subscribe(TOPIC+'/#')

pub_client = mqtt.Client()
pub_client.on_connect = on_connect
pub_client.on_publish = on_publish
pub_client.connect(BROKER_IP, PORT, LAG_TIME)