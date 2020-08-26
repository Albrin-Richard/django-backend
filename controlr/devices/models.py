from django.db import models
from controlr.settings import MAX_ITEM_NAME_LENGTH, UNIQUE_ID_LENGTH
from controlr.rooms.models import Room
from controlr.buildings.models import Building


class Device(models.Model):
    unique_id = models.SlugField(
        max_length=UNIQUE_ID_LENGTH,
        null=True,
        blank=False,
        unique=True
    )

    name = models.CharField(
        max_length=MAX_ITEM_NAME_LENGTH,
    )

    power = models.SmallIntegerField(
        blank=False,
        null=True
    )

    room = models.ForeignKey(
        Room,
        related_name='devices',
        on_delete=models.CASCADE
    )

    building = models.ForeignKey(
        Building,
        related_name='devices',
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )

    is_favorite = models.BooleanField(default=False)

    created_ts = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class DeviceState(models.Model):
    device = models.OneToOneField(
        Device,
        related_name='state',
        on_delete=models.CASCADE,
    )

    state = models.BooleanField(
        default=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.device}:{self.state}'
