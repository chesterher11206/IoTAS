from django.shortcuts import render
from .models import DeviceInfo


def dashboard(request):
    info = DeviceInfo.objects.all()

    context = {
        "info": info
    }
    return render(request, "dashboard/post.html", context=context)

# Create your views here.
