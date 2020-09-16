from django.db import models
from controlr.devices.models import Device
from controlr.buildings.models import Building
from django.contrib.postgres.fields import ArrayField


class Timer(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='timers',
        null=True,
    )

    state_change = models.BooleanField(default=True)

    trigger_time = models.DateTimeField(null=True)

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='timers',
        null=True
    )


class Schedule(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='schedules',
        null=True
    )

    state = models.BooleanField(default=True)

    state_change = models.BooleanField(default=True)

    time = models.TimeField()

    days_of_week = ArrayField(
        models.IntegerField(),
        size=7
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='schedules',
        null=True
    )
