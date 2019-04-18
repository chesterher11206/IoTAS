from django.contrib import admin
from .models import DeviceInfo, DeviceTemperature, DeviceHumidity, DeviceLight

admin.site.register(DeviceInfo)
admin.site.register(DeviceTemperature)
admin.site.register(DeviceHumidity)
admin.site.register(DeviceLight)

# Register your models here.
