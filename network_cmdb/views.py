from django.shortcuts import render
from django.shortcuts import HttpResponse
import pandas as pd
from network_cmdb.models import Device


def index(request):
    device_objs = Device.objects.all()
    data = {'devs': device_objs}
    return render(request, 'network_cmdb/index.html', context=data)