from nornir import InitNornir



def get_nornir_by_django_queryset(queryset, num_workers=100, ):
    """
    通过django Device数据对象集合queryset加载Nornir对象
    Args:
        queryset: Device的查询数据结合，QuerySet类型或者
        num_workers: 并发数，默认100 可以根据事情情况调整

    Returns:
        Nornir对象
    """
    data = []
    for device in queryset:
        dev_dict = {
            'name': device.name,
            'hostname': device.ip,
            'platform': device.platform,
            'username': device.username,
            'password': device.password,
            'port': device.port,
            'netmiko_secret': device.enable_pass,
            'netmiko_conn_timeout': device.conn_timeout,
            'netmiko_timeout': device.timeout,
        }
        data.append(dev_dict)

    runner = {
        "plugin": "threaded",
        "options": {
            "num_workers": num_workers,
        },
    }
    inventory = {
        "plugin": "FlatDataInventory",
        "options": {
            "data": data,
        },
    }
    nr = InitNornir(runner=runner, inventory=inventory)
    return nr