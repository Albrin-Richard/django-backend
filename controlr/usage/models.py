from django.db import models
from controlr.devices.models import Device


class DeviceHourlyUsage(models.Model):

    timestamp = models.DateTimeField()

    device = models.IntegerField()

    usage = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    runtime = models.IntegerField()
