# Generated by Django 2.2 on 2019-04-17 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_deviceinfo_allow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceinfo',
            name='allow',
        ),
    ]
