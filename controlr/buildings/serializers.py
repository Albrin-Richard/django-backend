from rest_framework import serializers
from .models import Building, Group
from controlr.devices.models import Device


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ['id', 'name']


class GroupSerializer(serializers.ModelSerializer):
    num_devices = serializers.ReadOnlyField()
    devices = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'devices', 'num_devices', 'building']
        read_only_fields = ['num_devices', 'building']

    # def create(self, validated_data):
    #     devices = validated_data.pop('devices')
    #     group = Group.objects.create(**validated_data)
    #     for device in devices:
    #         group.devices.add(device)
    #     return group
