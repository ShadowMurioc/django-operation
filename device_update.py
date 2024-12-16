import os
import sys
import django
from pathlib import Path
# from pandas.core.methods.to_dict import to_dict

BASE_DIR = Path(__file__).parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "operation_platform.settings")
django.setup()


if __name__  ==  "__main__":
    from network_cmdb.models import Device
    import pandas as pd
    device_info = pd.read_excel('device_info.xlsx')
    fetch_device = pd.DataFrame(device_info.to_dict(orient='records'))
    for row in fetch_device.itertuples():
        # 判断IP是否已经存在，若存在则跳过，若不存在则导入
        dev_ip = Device.objects.filter(ip=row[2])
        if dev_ip:
            pass
        else:
            if row[1] =='':
                print(row[1])
                dev = Device(
                    name = row[1],
                    ip = row[2],
                    protocol = row[3],
                    platform = row[4],
                    username = row[5],
                    password = row[6],
                    enable_pass = row[7],
                    port = row[8],
                    vendor = row[9],
                    model = row[10],
                    series = row[11],
                )
                dev.save()
            else:
                dev = Device(
                    name = row[2],
                    ip = row[2],
                    protocol = row[3],
                    platform = row[4],
                    username = row[5],
                    password = row[6],
                    enable_pass = row[7],
                    port = row[8],
                    vendor = row[9],
                    model = row[10],
                    series = row[11],
                )
                dev.save()

    devs = Device.objects.all()
    for dev in devs:
        print(dev)


'''
# 简单导入可以使用get or create

dev = Device.objects.get_or_create(
name = row[1],
ip = row[2],
protocol = row[3],
platform = row[4],
username = row[5],
password = row[6],
enable_pass = row[7],
port = row[8],
vendor = row[9],
model = row[10],
series = row[11],
)
'''

