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
    from .models import DeviceInfo, DeviceTemperature, DeviceHumidity, DeviceLight, DeviceLocation
    topic = msg.topic
    message = json.loads(msg.payload.decode("utf-8"))
    print(message)
    uuid = message.get('uuid', '')
    device_exist = DeviceInfo.objects.filter(uuid=uuid)

    if topic == "device/connect/info":
        if not device_exist:
            device = DeviceInfo()
            device.conti = message['conti']
            device.freq_dht = message['freq_dht']
            device.freq_light = message['freq_light']
        else:
            device = device_exist[0]
            device.online = True
            device.connected = True
        
        device.uuid = uuid
        device.host = message['host']
        device.os_name = message['os_name']
        device.public_ip = message['public_ip']
        device.private_ip = message['private_ip']
        device.version = message['version']
        device.save()
    elif topic == "device/disconnect/uuid":
        print("Disconnect!")
        if device_exist:
            device_exist = device_exist[0]
            device_exist.online = False
            device_exist.connected = False
            device_exist.save()
    elif topic == "device/connect/sensor/DHT":
        if device_exist:
            print("DHT")
            temperature = DeviceTemperature()
            temperature.uuid = uuid
            temperature.value = float(message['temperature'])
            temperature.timestamp = message['time']

            humidity = DeviceHumidity()
            humidity.uuid = uuid
            humidity.value = float(message['humidity'])
            humidity.timestamp = message['time']

            temperature.save()
            humidity.save()
    elif topic == "device/connect/sensor/light":
        if device_exist:
            print("Light")
            light = DeviceLight()
            light.uuid = uuid
            light.value = float(message['light'])
            light.timestamp = message['time']
            light.save()
    elif topic == "device/search/info":
        find_device = True
        if device_exist:
            device_exist = device_exist[0]
            if device_exist.connected:
                find_device = False
            else:
                device_exist.online = True
                device_exist.save()
        if find_device:
            room_group_name = 'display_search'
            channel_layer = get_channel_layer()
            info_dict = dict()
            info_dict['message'] = "Find Device"
            info_dict['uuid'] = uuid
            info_dict['host'] = message['host']
            info_dict['os_name'] = message['os_name']
            info_json = json.dumps(info_dict)
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'find_device',
                    'message': info_json
                }
            )
    elif topic == "device/set/success":
        if device_exist:
            device_exist = device_exist[0]
            device_exist.conti = message['conti']
            device_exist.freq_dht = message['freq_dht']
            device_exist.freq_light = message['freq_light']
            device_exist.save()
            print("Set Success!")
    elif topic == "device/locate/info":
        if device_exist:
            print("Location")
            location = DeviceLocation()
            location.uuid = uuid
            location.location_x = float(message['locationX'])
            location.location_y = float(message['locationY'])
            location.location_z = float(message['locationZ'])
            location.timestamp = message['time']
            location.save()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, PORT, LAG_TIME)
client.subscribe(TOPIC+'/#')

pub_client = mqtt.Client()
pub_client.on_connect = on_connect
pub_client.on_publish = on_publish
pub_client.connect(BROKER_IP, PORT, LAG_TIME)