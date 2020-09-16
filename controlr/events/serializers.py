from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name')
    room_name = serializers.CharField(source='device.room.name')
    room_group_name = serializers.CharField(
        source='device.room.room_group.name')

    class Meta:
        model = Event
        fields = ['id', 'timestamp', 'type', 'description',
                  'state_change', 'device', 'device_name', 'room_name', 'room_group_name']
