# Generated by Django 5.1.3 on 2024-12-16 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_cmdb', '0004_command_platform_alter_command_cmd'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='conn_timeout',
            field=models.IntegerField(default=30, verbose_name='连接超时时间'),
        ),
        migrations.AddField(
            model_name='device',
            name='timeout',
            field=models.IntegerField(default=30, verbose_name='CLI执行超时时间'),
        ),
    ]
