import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DeviceInfo, DeviceTemperature, DeviceHumidity, DeviceLight


def dashboard(request):
    infos = DeviceInfo.objects.all()

    temperature = dict();
    humidity = dict();
    light = dict();
    for info in infos:
        temp_t = [[t.timestamp, t.value] for t in DeviceTemperature.objects.filter(uuid=info.uuid).order_by('timestamp')]
        temp_h = [[h.timestamp, h.value] for h in DeviceHumidity.objects.filter(uuid=info.uuid).order_by('timestamp')]
        temp_l = [[l.timestamp, l.value] for l in DeviceLight.objects.filter(uuid=info.uuid).order_by('timestamp')]

        temperature[info.uuid] = temp_t[-10:]
        humidity[info.uuid] = temp_h[-10:]
        light[info.uuid] = temp_l[-10:]
    
    sensor_dataset = dict()
    sensor_dataset["Temperature"] = temperature
    sensor_dataset["Humidity"] = humidity
    sensor_dataset["Light"] = light
    sensor_list = ["Temperature", "Humidity", "Light"]

    context = {
        "infos": infos,
        "sensor_dataset": json.dumps(sensor_dataset),
        "sensor_list": sensor_list,
    }
    return render(request, "dashboard/post.html", context=context)

def home(request):
    if request.user.is_authenticated:
        response = HttpResponseRedirect(reverse("dashboard"))
        return response
    else:
        response = HttpResponseRedirect(reverse("log_in"))
        return response

# Create your views here.
