from pyexpat.errors import messages

from django.contrib import admin, messages

# Register your models here.
from network_cmdb.models import Device, Command, ConfigBackup
from tools.tasks.fetch_operation import batch_fetch_operation
from tools.tasks.fetch_hostname import batch_fetch_hostname

def fetch_operation(modeladmin, request, queryset):
    result = batch_fetch_operation(queryset)
    success_num = result['success_num']
    fail_num = result['fail_num']
    fail_dev = result['fail_dev']
    messages.info(request, '获取巡检文件成功{}台,失败{}台，失败名单如下：{}'.format(success_num, fail_num, fail_dev))
fetch_operation.short_description = '获取巡检文件'

def fetch_hostname(modeladmin, request, queryset):
    result = batch_fetch_hostname(queryset)
    success_num = result['success_num']
    fail_num = result['fail_num']
    fail_dev = result['fail_dev']
    messages.info(request, '获取主机名称{}台,失败{}台，失败名单如下：{}'.format(success_num, fail_num, fail_dev))
fetch_hostname.short_description = '获取设备主机名称'


# 创建Device的Admin管理类
class DeviceAdmin(admin.ModelAdmin):
    actions = [fetch_operation, fetch_hostname]

    list_display = ['id', 'name', 'ip', 'vendor', 'platform', 'username', 'protocol', 'update_time']
    list_per_page = 15
    search_fields = ['name', 'ip', 'vendor']
    list_display_links = ['name', 'ip']
    list_editable = ['vendor', 'platform', 'username']
    date_hierarchy = 'created_time'
    list_filter = ['vendor', 'platform']
    # exclude = ['password']
    readonly_fields = ['id', 'update_time', 'created_time']
    fieldsets = [
        ('基本信息', {'fields': ['id', 'ip', 'name']}),
        ('型号信息', {'fields': ['vendor',
                                ('series', 'model')]}),
        ('登录信息', {'fields': [('username', 'password', 'enable_pass','platform'),
                                ('protocol', 'port'),
                                ('timeout', 'conn_timeout')]}),
        ('其他信息', {'fields': [('created_time', 'update_time')]}),
    ]

# 将Device Admin管理类与Device Model绑定注册到Admin管理后台
admin.site.register(Device, DeviceAdmin)


class CommandAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'platform', 'cmd', 'created_time', 'update_time']
# 将Device Admin管理类与Device Model绑定注册到Admin管理后台
admin.site.register(Command, CommandAdmin)


class ConfigBackupAdmin(admin.ModelAdmin):
    list_display = ['dev', 'cmd', 'config_file', 'created_time']


admin.site.register(ConfigBackup, ConfigBackupAdmin)