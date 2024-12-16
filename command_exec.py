import os
import sys
import django
from pathlib import Path


BASE_DIR = Path(__file__).parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "operation_platform.settings")
django.setup()


if __name__  ==  "__main__":
    from network_cmdb.models import Device, Command
    devices = Device.objects.all()
    for device in devices:
        platform_diff = Command.objects.filter(platform=device.platform)
        if platform_diff:
            exec_cmd = platform_diff.values_list()[0][3]
            cmd_single_list = exec_cmd.split('\n')
            '''
            此处通过Netmiko 连接设备，遍历命令，发送到设备进行执行。
            '''
            for cmd_single in cmd_single_list:
                print(cmd_single)

        else:
            print('【 '+ device.ip + ' 】 暂不支持巡检, 请添加巡检命令')
            pass

