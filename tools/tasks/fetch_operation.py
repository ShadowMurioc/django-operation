from pathlib import Path
from network_cmdb.models import Device, Command, ConfigBackup
from tools.get_nornir_obj import get_nornir_by_django_queryset
from django.core.files.base import ContentFile
import os
import django

# BASE_DIR = Path(__file__).parent
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "operation_platform.settings")
# django.setup()


def fetch_operation(task_context):
    result = '{} 巡检完成'.format(task_context.host.name)
    host_obj = task_context.host
    platform_device = host_obj.platform
    dev_obj = Device.objects.filter(name=task_context.host.name)[0]
    platform_diff = Command.objects.filter(platform=platform_device)

    if platform_diff:
        net_conn = task_context.host.get_connection('netmiko', task_context.nornir.config)
        # secret参数可以直接从Netmiko连接中获取
        # enable_pass = net_conn.enable_pass
        #         # if enable_pass:
        #         #     net_conn.enable()

        exec_cmd = platform_diff.values_list()[0][3]
        cmd_single_list = exec_cmd.split('\n')
        '''
        此处通过Netmiko 连接设备，遍历命令，发送到设备进行执行。
        '''
        for cmd_single in cmd_single_list:
            output = net_conn.send_command(cmd_single)
            file_name = '{}.config'.format(cmd_single)
            config_content = ContentFile(content=output, name=file_name)
            config_backup_obj = ConfigBackup(dev=dev_obj, cmd=cmd_single, config_file=config_content)
            config_backup_obj.save()

    else:
        print('【 ' + host_obj.ip + ' 】 暂不支持巡检, 请添加巡检命令')
        pass

def batch_fetch_operation(queryset, num_workers=100):
    # 通过Device的queryset加载nornir对象
    nr = get_nornir_by_django_queryset(queryset, num_workers)
    # 批量执行收集并更新软件版本的task函数
    result = nr.run(task=fetch_operation)
    # 初始化失败设备的列表
    fail_dev = []
    # 失败的设备会被Nornir捕获异常，将网络设备追加到Nornir Result的failed_hosts字段
    # 这是一个类似于字典的数据结构，可以进行for循环，key为Nornir网络对象的name属性，即设备名
    for fail_host_name in result.failed_hosts:
        fail_dev.append(fail_host_name)
    # 通过内置函数len计算失败网络设备的数量
    fail_num = len(fail_dev)
    # 通过本次执行任务设备总量减去失败的设备总量获取成功设备的总量
    success_num = len(queryset) - fail_num
    result_detail = {'success_num': success_num, 'fail_num': fail_num, 'fail_dev': fail_dev}
    return result_detail