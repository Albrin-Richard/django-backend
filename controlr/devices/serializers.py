from rest_framework import serializers
from .models import Device, DeviceState
from controlr.buildings.models import Building


class DeviceStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceState
        fields = ['id', 'device', 'state']


class DeviceSerializer(serializers.ModelSerializer):
    state = serializers.BooleanField(read_only=True, source='state.state')
    building_name = serializers.CharField(
        source='building.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    room_group_name = serializers.CharField(
        source='room.room_group', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'room',
                  'unique_id', 'power', 'state', 'building', 'building_name', 'room_name', 'room_group_name', 'is_favorite', 'created_ts']
        read_only_fields = ['building', 'is_favorite', 'created_ts']


class DeviceShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['id', 'name', 'state']


class FavoriteSerializer(serializers.ModelSerializer):
    room_group = serializers.CharField(
        source='room.room_group', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'room', 'state', 'room_group']
