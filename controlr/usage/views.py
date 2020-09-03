from django.shortcuts import render
from rest_framework.views import APIView
from datetime import datetime
from .utils import get_devices_usage, get_device_usage_timeseries, get_rooms_usage
from rest_framework.response import Response
from rest_framework import status
from controlr.buildings.models import Group
from controlr.rooms.models import Room
from controlr.devices.models import Device
from .serializers import DeviceUsageTimeseriesSerializer
import pytz


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

        start_ts = datetime.strptime(
            start_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)
        end_ts = datetime.strptime(
            end_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)

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

        start_ts = datetime.strptime(
            start_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)
        end_ts = datetime.strptime(
            end_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)

        devices_usage = get_devices_usage(
            building_id=kwargs['id'],
            device_ids=device_ids,
            start_ts=start_ts,
            end_ts=end_ts
        )

        devices_usage_list = []

        for device_id, value in devices_usage.items():
            devices_usage_list.append({
                'device_id': device_id,
                'device_name': Device.objects.get(id=device_id).name,
                'room_name': Device.objects.get(id=device_id).room.name,
                'room_group_name': Device.objects.get(id=device_id).room.room_group.name,
                'runtime': value['runtime'],
                'usage': value['usage']
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

        start_ts = datetime.strptime(
            start_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)
        end_ts = datetime.strptime(
            end_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)

        devices_usage = get_device_usage_timeseries(
            building_id=kwargs['id'],
            device_ids=device_ids,
            start_ts=start_ts,
            end_ts=end_ts,
            frequency=frequency
        )

        serializer = DeviceUsageTimeseriesSerializer(
            data=devices_usage, many=True)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomUsageList(APIView):
    def post(self, request, *args, **kwargs):
        room_ids = request.data.get('room_ids')
        start_ts = request.data.get('start_ts')
        end_ts = request.data.get('end_ts')

        if room_ids is None:
            room_ids = list(Room.objects.filter(
                building_id=kwargs['id'],
            ).values_list('id', flat=True))

        start_ts = datetime.strptime(
            start_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)
        end_ts = datetime.strptime(
            end_ts, '%Y-%m-%dT%H:%M:%S').astimezone(tz=pytz.utc)

        rooms_usage = get_rooms_usage(
            building_id=kwargs['id'],
            room_ids=room_ids,
            start_ts=start_ts,
            end_ts=end_ts
        )

        rooms_usage_list = []

        for room_id, value in rooms_usage.items():
            rooms_usage_list.append({
                'room_id': room_id,
                'room_name': Room.objects.get(id=room_id).name,
                'room_group_name': Room.objects.get(id=room_id).room_group.name,
                'runtime': value['runtime'],
                'usage': value['usage']
            })

        return Response(rooms_usage_list, status=status.HTTP_200_OK)
