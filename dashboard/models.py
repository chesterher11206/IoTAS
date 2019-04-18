from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            super(BaseModel, self).save(force_insert, force_update, using, update_fields)
        except IntegrityError as saveException:
            print ('Rolling back transaction due to an error while saving %s...' % self.__class__.__name__)


class DeviceInfo(BaseModel):
    host = models.CharField(verbose_name='host', default='', max_length=50)
    uuid = models.CharField(verbose_name='uuid', default='', max_length=50, unique=True)
    os_name = models.CharField(verbose_name='os_name', default='', max_length=50)
    online = models.BooleanField(default=True)
    published_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Device Information'
        verbose_name_plural = verbose_name

class DeviceTemperature(BaseModel):
    uuid = models.CharField(verbose_name='uuid', default='', max_length=50)
    value = models.FloatField(verbose_name='temperature', null=True, blank=True, default=None)
    timestamp = models.CharField(verbose_name='detected time', default='', max_length=10)
    published_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Temperature'
        verbose_name_plural = verbose_name

class DeviceHumidity(BaseModel):
    uuid = models.CharField(verbose_name='uuid', default='', max_length=50)
    value = models.FloatField(verbose_name='humidity', null=True, blank=True, default=None)
    timestamp = models.CharField(verbose_name='detected time', default='', max_length=10)
    published_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Humidity'
        verbose_name_plural = verbose_name

class DeviceLight(BaseModel):
    uuid = models.CharField(verbose_name='uuid', default='', max_length=50)
    value = models.FloatField(verbose_name='light', null=True, blank=True, default=None)
    timestamp = models.CharField(verbose_name='detected time', default='', max_length=10)
    published_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Light'
        verbose_name_plural = verbose_name

# Create your models here.
