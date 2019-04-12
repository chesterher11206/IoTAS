import paho.mqtt.client as mqtt


BROKER_IP = "140.112.18.2"
PORT = 11053
LAG_TIME = 600
TOPIC = "device"

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    # Do something
    from .models import DeviceInfo
    topic_r = str(msg.topic)
    msg_r = str(msg.payload)
    info_set = msg_r.split(",")
    for d in info_set:
        print (d)

    info = DeviceInfo()
    info.host = info_set[0]
    info.lan_ip = info_set[1]
    info.uuid = info_set[2]
    info.os_name = info_set[3]
    info.save()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, PORT, LAG_TIME)
client.subscribe(TOPIC+'/#')