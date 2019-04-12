from django.db import models


class DeviceInfo(models.Model):
    host = models.CharField(verbose_name='host', default='', max_length=50)
    lan_ip = models.CharField(verbose_name='lan_ip', default='', max_length=50)
    uuid = models.CharField(verbose_name='uuid', default='', max_length=50)
    os_name = models.CharField(verbose_name='os_name', default='', max_length=50)
    published_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Device Information'
        verbose_name_plural = verbose_name

# Create your models here.
