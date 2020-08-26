from django.shortcuts import render
from rest_framework.views import APIView

from .utils import get_devices_usage, get_device_usage_timeseries
from rest_framework.response import Response
from rest_framework import status
from controlr.buildings.models import Group
from controlr.rooms.models import Room
from controlr.devices.models import Device


class DeviceUsageTotal(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        group_id = request.data.get('group_id')
        start_ts = request.data.get('start_ts')
        end_ts = request.data.get('end_ts')

        if device_ids is None:
            if room_id is not None:
                device_ids = list(Room.objects.filter(
                    id=room_id).values_list('devices', flat=True))
            if group_id is not None:
                device_ids = list(Group.objects.filter(
                    id=group_id).values_list('devices', flat=True))

        devices_usage = get_devices_usage(
            building_id=kwargs['id'],
            device_ids=device_ids,
            start_ts=start_ts,
            end_ts=end_ts
        )

        total_usage = 0
        total_runtime = 0

        for usage in devices_usage.values():
            total_usage += usage['usage']
            total_runtime += usage['runtime']

        return Response({
            'total_usage': total_usage,
            'total_runtime': total_runtime
        }, status=status.HTTP_200_OK)


class DeviceUsageList(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        group_id = request.data.get('group_id')
        start_ts = request.data.get('start_ts')
        end_ts = request.data.get('end_ts')

        if device_ids is None:
            if room_id is not None:
                device_ids = list(Room.objects.filter(
                    id=room_id).values_list('devices', flat=True))
            if group_id is not None:
                device_ids = list(Group.objects.filter(
                    id=group_id).values_list('devices', flat=True))

        devices_usage = get_devices_usage(
            building_id=kwargs['id'],
            device_ids=device_ids,
            start_ts=start_ts,
            end_ts=end_ts
        )

        devices_usage_list = []

        for device_id, usage in devices_usage.items():
            devices_usage_list.append({
                'device_id': device_id,
                'device_name': Device.objects.get(id=device_id).name,
                'room_name': Device.objects.get(id=device_id).room.name,
                'room_group_name': Device.objects.get(id=device_id).room.room_group.name,
                'runtime': usage['runtime'],
                'usage': usage['usage']
            })

        return Response(devices_usage_list, status=status.HTTP_200_OK)


class DeviceUsageTimeseries(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        group_id = request.data.get('group_id')
        start_ts = request.data.get('start_ts')
        end_ts = request.data.get('end_ts')
        frequency = request.data.get('frequency')

        if device_ids is None:
            if room_id is not None:
                device_ids = list(Room.objects.filter(
                    id=room_id).values_list('devices', flat=True))
            if group_id is not None:
                device_ids = list(Group.objects.filter(
                    id=group_id).values_list('devices', flat=True))

        devices_usage = get_device_usage_timeseries(
            building_id=kwargs['id'],
            device_ids=device_ids,
            start_ts=start_ts,
            end_ts=end_ts,
            frequency=frequency
        )

        return Response(devices_usage, status=status.HTTP_200_OK)
