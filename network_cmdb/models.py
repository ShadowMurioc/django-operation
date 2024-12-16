from django.db import models

# Create your models here.

from pathlib import Path
from datetime import date

def config_backup_upload_to(instance, fielname):
    dev = instance.dev
    date_str = date.today().strftime('%Y%m%d')
    return str(Path('ConfigBackup', date_str, dev.name, fielname))

class Device(models.Model):
    data_chioces = (
        ('0', 'Cisco'),
        ('1', 'Huawei'),
        ('2', 'H3C')
    )
    # 登录设备需要
    ip = models.GenericIPAddressField(verbose_name='IP地址', unique=True)
    platform = models.CharField(verbose_name='平台', max_length=128,default="cisco_ios")
    username = models.CharField(verbose_name='用户名', max_length=128,default="admin")
    password = models.CharField(verbose_name='登录密码', max_length=128,default="<PASSWORD>")
    enable_pass = models.CharField(verbose_name='特权密码', max_length=128, default='enable_password')
    conn_timeout = models.IntegerField(verbose_name='连接超时时间', default=30)
    timeout = models.IntegerField(verbose_name='CLI执行超时时间', default=30)
    port = models.IntegerField(verbose_name='ssh端口', default=22)
    # 暂时仅支持SSH
    protocol = models.CharField(verbose_name='管理协议', max_length=32, default='ssh')
    # 可通过登录后进行回填该内容
    name = models.CharField(verbose_name='设备名', max_length=128, blank=True)
    vendor = models.CharField(verbose_name='厂商',choices=data_chioces, max_length=128, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, blank=True)
    series = models.CharField(verbose_name='系列', max_length=128, blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '<网络设备,IP:{},名称:{}>'.format(self.ip, self.name)

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = '设备'

class Command(models.Model):
    # 根据平台/厂商书写巡检命令
    vendor = models.CharField(verbose_name='厂商', max_length=128, blank=False)
    platform = models.CharField(verbose_name='平台', max_length=128,default="cisco_ios")
    cmd = models.TextField(verbose_name='命令', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return '<厂商:{} 的巡检命令已经添加>'.format(self.vendor)

    class Meta:
        verbose_name = '巡检命令'
        verbose_name_plural = '巡检命令'

class ConfigBackup(models.Model):
    dev = models.ForeignKey(verbose_name='关联设备', to='Device', on_delete=models.CASCADE)
    cmd = models.CharField(verbose_name='执行的命令', max_length=128)
    config_file = models.FileField(verbose_name='配置文件', upload_to=config_backup_upload_to)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        # 我们可以访问外键对象的属性，比如取所属设备名self.dev.name
        return '{}于{}的"{}"备份'.format(self.dev.name, self.created_time, self.cmd)

    class Meta:
        verbose_name = '配置备份'
        verbose_name_plural = '配置备份'