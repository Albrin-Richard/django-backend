from django.db import models
from controlr.settings import MAX_ITEM_NAME_LENGTH, UNIQUE_ID_LENGTH
from controlr.buildings.models import Building


class RoomGroup(models.Model):
    name = models.CharField(max_length=MAX_ITEM_NAME_LENGTH)

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='room_group'
    )

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(
        max_length=MAX_ITEM_NAME_LENGTH
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    room_group = models.ForeignKey(
        RoomGroup,
        on_delete=models.CASCADE,
        related_name='rooms',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
