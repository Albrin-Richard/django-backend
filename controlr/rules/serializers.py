from rest_framework import serializers
from .models import Timer, Schedule


class TimerSerializer(serializers.ModelSerializer):
    time_delta = serializers.DurationField()
    room_name = serializers.CharField(
        source='device.room.name',
        read_only=True
    )
    room_group_name = serializers.CharField(
        source='device.room.room_group',
        read_only=True
    )
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = Timer
        fields = ['id', 'device', 'device_name', 'state_change', 'time_delta',
                  'building', 'room_name', 'room_group_name']
        read_only_fields = ['building', 'device.room',
                            'room_name', 'room_group_name']


class ScheduleSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(
        source='device.room.name',
        read_only=True
    )
    room_group_name = serializers.CharField(
        source='device.room.room_group',
        read_only=True
    )

    class Meta:
        model = Schedule
        fields = ['id', 'device', 'state', 'state_change',
                  'time', 'days_of_week', 'building', 'room_name', 'room_group_name']
        read_only_fields = ['building', 'room_name', 'room_group_name']
