from django.apps import AppConfig
import threading


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        from . import signals
        t = threading.Thread(target=mqtt_thread, args=(), kwargs={})
        t.setDaemon(True)
        t.start()

def mqtt_thread():
    from .mqtt import client
    while True:
        client.loop_start()
