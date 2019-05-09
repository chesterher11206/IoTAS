import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DeviceInfo, DeviceTemperature, DeviceHumidity, DeviceLight


def dashboard(request):
    infos = DeviceInfo.objects.all()

    temperature = dict()
    humidity = dict()
    light = dict()

    t_ts = []
    for t in DeviceTemperature.objects.order_by('-timestamp'):
        if len(t_ts) > 10:
            break
        else:
            if t.timestamp not in t_ts:
                t_ts.append(t.timestamp)
            if t.uuid not in temperature.keys():
                temperature[t.uuid] = [[t.timestamp, t.value]]
            else:
                temperature[t.uuid].insert(0, [t.timestamp, t.value])

    h_ts = []
    for h in DeviceHumidity.objects.order_by('-timestamp'):
        if len(h_ts) > 10:
            break
        else:
            if h.timestamp not in h_ts:
                h_ts.append(h.timestamp)
            if h.uuid not in humidity.keys():
                humidity[h.uuid] = [[h.timestamp, h.value]]
            else:
                humidity[h.uuid].insert(0, [h.timestamp, h.value])

    l_ts = []
    for l in DeviceLight.objects.order_by('-timestamp'):
        if len(l_ts) > 10:
            break
        else:
            if l.timestamp not in l_ts:
                l_ts.append(l.timestamp)
            if l.uuid not in light.keys():
                light[h.uuid] = [[l.timestamp, l.value]]
            else:
                light[l.uuid].insert(0, [l.timestamp, l.value])

    # for info in infos:
        # temp_t = [[t.timestamp, t.value] for t in DeviceTemperature.objects.filter(uuid=info.uuid).order_by('timestamp')]
        # temp_h = [[h.timestamp, h.value] for h in DeviceHumidity.objects.filter(uuid=info.uuid).order_by('timestamp')]
        # temp_l = [[l.timestamp, l.value] for l in DeviceLight.objects.filter(uuid=info.uuid).order_by('timestamp')]

        # temperature[info.uuid].reverse()
        # humidity[info.uuid].reverse()
        # light[info.uuid].reverse()
    
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

def device(request):
    infos = DeviceInfo.objects.all()
    sensor_list = ["Temperature", "Humidity", "Light"]

    device_info = dict()
    for info in infos:
        if info.uuid not in device_info.keys():
            device_info[info.uuid] = dict()
        if 'info' not in device_info[info.uuid]:
            device_info[info.uuid]['info'] = dict()
        if 'sensor' not in device_info[info.uuid]:
            device_info[info.uuid]['sensor'] = dict()
        if 'setting' not in device_info[info.uuid]:
            device_info[info.uuid]['setting'] = dict()
        if 'ver' not in device_info[info.uuid]:
            device_info[info.uuid]['ver'] = dict()
        device_info[info.uuid]['info']['uuid'] = info.uuid
        device_info[info.uuid]['info']['host'] = info.host
        device_info[info.uuid]['info']['os_name'] = info.os_name
        device_info[info.uuid]['info']['public_ip'] = "None"
        device_info[info.uuid]['info']['private_ip'] = "None"
        device_info[info.uuid]['info']['connected'] = info.connected
        device_info[info.uuid]['ver']['version'] = info.version
        device_info[info.uuid]['setting']['continuous'] = info.conti
        device_info[info.uuid]['setting']['dht_frequence'] = info.freq_dht
        device_info[info.uuid]['setting']['light_frequence'] = info.freq_light
        device_info[info.uuid]['sensor']['temperature'] = "None"
        device_info[info.uuid]['sensor']['humidity'] = "None"
        device_info[info.uuid]['sensor']['light'] = "None"
        temp_t = DeviceTemperature.objects.filter(uuid=info.uuid).order_by('-timestamp').first()
        temp_h = DeviceHumidity.objects.filter(uuid=info.uuid).order_by('-timestamp').first()
        temp_l = DeviceLight.objects.filter(uuid=info.uuid).order_by('-timestamp').first()
        if info.connected:
            device_info[info.uuid]['info']['public_ip'] = info.public_ip
            device_info[info.uuid]['info']['private_ip'] = info.private_ip
            if temp_t:
                device_info[info.uuid]['sensor']['temperature'] = temp_t.value
            if temp_h:
                device_info[info.uuid]['sensor']['humidity'] = temp_h.value
            if temp_l:
                device_info[info.uuid]['sensor']['light'] = temp_l.value


    context = {
        "infos": infos,
        "device_info": device_info,
        "sensor_list": sensor_list,
    }
    return render(request, "dashboard/device.html", context=context)

# Create your views here.
