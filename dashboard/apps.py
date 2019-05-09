from django.apps import AppConfig
import threading
import sys, json
import atexit


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        from . import signals
        atexit.register(exit_handler)
        t = threading.Thread(target=mqtt_thread, args=(), kwargs={})
        t.daemon = True
        t.start()

def mqtt_thread():
    from .mqtt import client
    while True:
        client.loop_start()

def exit_handler():
    from .mqtt import pub_client
    from .models import DeviceInfo
    msg_json = {"message": "Server Disconnect"}
    pub_client.publish("server/disconnect", payload=json.dumps(msg_json), qos=0)
    devices = DeviceInfo.objects.all()
    for device in devices:
        device.connected = False
        device.online = False
        device.save()
    print("System closing...")
