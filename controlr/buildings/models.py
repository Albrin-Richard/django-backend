from django.db import models
from controlr.settings import MAX_ITEM_NAME_LENGTH, UNIQUE_ID_LENGTH
# from controlr.devices.models import Device
from controlr.accounts.models import User


class Building(models.Model):
    name = models.CharField(max_length=MAX_ITEM_NAME_LENGTH)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(
        max_length=MAX_ITEM_NAME_LENGTH
    )

    devices = models.ManyToManyField(
        'devices.device', related_name='groups', blank=False)

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='groups',
        null=True,
        blank=False
    )

    def __str__(self):
        return self.name
