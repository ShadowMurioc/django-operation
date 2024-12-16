from pathlib import Path
from nornir.core.task import Result
from nornir_scrapli.tasks import get_prompt
import re
from network_cmdb.models import Device
from tools.get_nornir_obj import get_nornir_by_django_queryset


def fetch_hostname(task_context):
    # result = '{}主机名称更新成功'.format(task_context.host.name)

    net_conn = task_context.host.get_connection('netmiko', task_context.nornir.config)

    # Cisco Device Hostname获取
    cisco_hostname_fetch  = net_conn.send_command('show run | inc hostname')
    cisco_hostname = re.findall('hostname (.*)', cisco_hostname_fetch)[0]



    dev = Device.objects.filter(name=task_context.host.name)[0]
    dev_ip = dev.ip
    hostname = Device.objects.filter(ip=dev_ip)
    hostname.update(name=cisco_hostname)

    # 操作完成之后关闭连接
    task_context.nornir.close_connections('netmiko')


def batch_fetch_hostname(queryset, num_workers=100):
    # 通过Device的queryset加载nornir对象
    nr = get_nornir_by_django_queryset(queryset, num_workers)
    # 批量执行收集并更新主机名称的task函数
    # result = nr.run(task=fetch_hostname)
    result = nr.run(task=fetch_hostname)
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