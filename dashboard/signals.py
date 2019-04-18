import json
import datetime
from .models import DeviceInfo, DeviceTemperature, DeviceHumidity, DeviceLight
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync


@receiver(post_save, sender=DeviceInfo)
def device_status(sender, instance, **kwargs):
    room_group_name = 'display_info'
    channel_layer = get_channel_layer()
    info_dict = dict()
    for field in instance._meta.fields:
        field_value = getattr(instance, field.name)
        if isinstance(field_value, datetime.datetime):
            field_value = field_value.strftime('%Y-%m-%d %H:%M:%S')
        info_dict[field.name] = field_value
    info_dict['message'] = "Display Data"
    info_json = json.dumps(info_dict)
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'display_data',
            'message': info_json
        }
    )

@receiver(post_save, sender=DeviceTemperature)
def device_temperature(sender, instance, **kwargs):
    send_sensor(instance, "Temperature")

@receiver(post_save, sender=DeviceHumidity)
def device_humidity(sender, instance, **kwargs):
    send_sensor(instance, "Humidity")

@receiver(post_save, sender=DeviceLight)
def device_light(sender, instance, **kwargs):
    send_sensor(instance, "Light")

def send_sensor(instance, sensor_name):
    room_group_name = 'display_sensor'
    channel_layer = get_channel_layer()
    sensor_dict = dict()
    for field in instance._meta.fields:
        field_value = getattr(instance, field.name)
        if isinstance(field_value, datetime.datetime):
            field_value = field_value.strftime('%Y-%m-%d %H:%M:%S')
        sensor_dict[field.name] = field_value
    sensor_dict['message'] = "Display Sensor"
    sensor_dict["sensor_name"] = sensor_name
    sensor_json = json.dumps(sensor_dict)
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'display_data',
            'message': sensor_json
        }
    )
