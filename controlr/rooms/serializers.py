from rest_framework import serializers
from .models import Room, RoomGroup
from controlr.devices.serializers import DeviceShortSerializer
from controlr.devices.models import DeviceState


class RoomDetailSerializer(serializers.ModelSerializer):
    devices = DeviceShortSerializer(read_only=True, many=True)
    room_group_name = serializers.CharField(
        source='room_group.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name',
                  'building', 'devices', 'room_group', 'room_group_name']
        read_only_fields = ['id', 'devices']


class RoomListSerializer(serializers.ModelSerializer):
    num_devices_total = serializers.SerializerMethodField()
    num_devices_on = serializers.SerializerMethodField()
    room_group_name = serializers.CharField(
        source='room_group.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'room_group',
                  'num_devices_total', 'num_devices_on', 'room_group_name']
        read_only_fields = ['room_group_name']

    def get_num_devices_total(self, obj):
        return obj.devices.count()

    def get_num_devices_on(self, obj):
        return obj.devices.filter(state__state=True).count()


class RoomGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomGroup
        fields = ['id', 'name', 'building']
        read_only_fields = ['building']


class CurrentStatsSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    room_name = serializers.CharField()
    num_devices_on = serializers.IntegerField()
    num_devices_total = serializers.IntegerField()
    current_power_usage = serializers.FloatField()
