from rest_framework import serializers
from .models import Building, Group
from controlr.devices.models import Device
from controlr.devices.serializers import DeviceShortSerializer


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ['id', 'name', 'owner']


class GroupDetailSerializer(serializers.ModelSerializer):
    devices = DeviceShortSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'devices', 'building']
        read_only_fields = ['building']


class GroupListSerializer(serializers.ModelSerializer):
    num_devices = serializers.ReadOnlyField()
    devices = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'devices', 'num_devices', 'building']
        read_only_fields = ['num_devices', 'building']


class CurrentStatsSerializer(serializers.Serializer):
    building_id = serializers.IntegerField()
    building_name = serializers.CharField()
    num_devices_on = serializers.IntegerField()
    num_devices_total = serializers.IntegerField()
    current_power_usage = serializers.DecimalField(
        max_digits=5, decimal_places=2)
    num_rooms_on = serializers.IntegerField()
    num_rooms_total = serializers.IntegerField()
    power_unit = serializers.CharField()
