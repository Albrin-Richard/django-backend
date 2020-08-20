from django.db import models
from controlr.buildings.models import Building
from controlr.devices.models import Device


class Event(models.Model):
    DEVICE_CREATED = 100
    ROOM_CREATED = 101
    GROUP_CREATED = 102
    ROOM_GROUP_CREATED = 103
    DEVICE_TIMER_CREATED = 104
    DEVICE_SCHEDULE_CREATED = 105
    DEVICE_ON_MANUAL = 200
    DEVICE_OFF_MANUAL = 201
    DEVICE_ON_TIMER = 202
    DEVICE_OFF_TIMER = 203
    DEVICE_ON_SCHEDULE = 204
    DEVICE_OFF_SCHEDULE = 205
    SCENE_TRIGGERED = 300

    # DEVICE = 'Device'
    # ROOM = 'Room'
    # BUILDING = 'Building'
    # SCENE = 'Scene'
    # GROUP = 'Group'

    EVENT_TYPES = [
        (DEVICE_CREATED, 'Device Created'),
        (ROOM_CREATED, 'Room Created'),
        (GROUP_CREATED, 'Group Created'),
        (ROOM_GROUP_CREATED, 'Room Group Created'),
        (DEVICE_TIMER_CREATED, 'Timer Created'),
        (DEVICE_SCHEDULE_CREATED, 'Schedule Created'),
        (DEVICE_ON_MANUAL, 'Device On'),
        (DEVICE_OFF_MANUAL, 'Device Off'),
        (DEVICE_ON_TIMER, 'Device On Timer'),
        (DEVICE_OFF_TIMER, 'Device Off Timer'),
        (DEVICE_ON_SCHEDULE, 'Device On Schedule'),
        (DEVICE_OFF_SCHEDULE, 'Device Off Schedule'),
        (SCENE_TRIGGERED, 'Scene Triggered'),
    ]

    # EVENT_OBJECT_TYPE = [
    #     (DEVICE, 'Device'),
    #     (ROOM, 'Room'),
    #     (BUILDING, 'Building'),
    #     (SCENE, 'Scene'),
    #     (GROUP, 'Group'),
    # ]

    device = models.ForeignKey(
        Device,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    # object_type = models.CharField(
    #     choices=EVENT_OBJECT_TYPE,
    #     max_length=15,
    #     blank=True,
    #     null=True
    # )

    timestamp = models.DateTimeField(auto_now_add=True)

    type = models.IntegerField(
        choices=EVENT_TYPES,
        blank=False,
        null=True
    )

    description = models.CharField(
        blank=True,
        max_length=100
    )

    # Device On: True; Device Off: False
    state_change = models.BooleanField(blank=True, null=True)

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=False
    )
