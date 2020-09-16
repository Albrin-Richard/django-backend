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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils.dateparse import parse_datetime, parse_duration
from django.utils.timezone import is_aware, now
import pytz


class RecentUsage(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        group_id = request.data.get('group_id')
        durations = request.data.get('durations')

        if device_ids is None:
            if room_id is not None:
                device_ids = list(Room.objects.filter(
                    id=room_id).values_list('devices', flat=True))
            if group_id is not None:
                device_ids = list(Group.objects.filter(
                    id=group_id).values_list('devices', flat=True))

        if room_id is not None and device_ids == [None]:
            return Response([], status=status.HTTP_200_OK)

        if group_id is not None and device_ids == [None]:
            return Response([], status=status.HTTP_200_OK)

        recent_usage = []

        for duration in durations:
            devices_usage = get_devices_usage(
                building_id=kwargs['id'],
                device_ids=device_ids,
                start_ts=now() - parse_duration(duration),
                end_ts=now()
            )

            total_usage = 0
            total_runtime = 0

            for usage in devices_usage.values():
                total_usage += usage['usage']
                total_runtime += usage['runtime']

            recent_usage.append({
                'duration': duration,
                'usage': total_usage,
                'runtime': total_runtime
            })

        return Response(recent_usage, status=status.HTTP_200_OK)


class DevicesUsageTotal(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        group_id = request.data.get('group_id')
        start_ts = parse_datetime(request.data.get('start_ts'))
        end_ts = parse_datetime(request.data.get('end_ts'))

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


class DevicesUsageList(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        print(request.data.get('start_ts'))
        group_id = request.data.get('group_id')
        start_ts = parse_datetime(request.data.get('start_ts'))
        end_ts = parse_datetime(request.data.get('end_ts'))

        if device_ids is None:
            if room_id is not None:
                device_ids = list(Room.objects.filter(
                    id=room_id).values_list('devices', flat=True))
            if group_id is not None:
                device_ids = list(Group.objects.filter(
                    id=group_id).values_list('devices', flat=True))

        print(device_ids)
        if room_id is not None and device_ids == [None]:
            return Response([], status=status.HTTP_200_OK)

        if group_id is not None and device_ids == [None]:
            return Response([], status=status.HTTP_200_OK)

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

        devices_usage_list = sorted(
            devices_usage_list, key=lambda x: x['usage'], reverse=True)

        return Response(devices_usage_list, status=status.HTTP_200_OK)


class DevicesUsageTimeseries(APIView):
    def post(self, request, *args, **kwargs):
        device_ids = request.data.get('device_ids')
        room_id = request.data.get('room_id')
        group_id = request.data.get('group_id')
        start_ts = parse_datetime(request.data.get('start_ts'))
        end_ts = parse_datetime(request.data.get('end_ts'))
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

        serializer = DeviceUsageTimeseriesSerializer(
            data=devices_usage, many=True)

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomsUsageList(APIView):
    def post(self, request, *args, **kwargs):
        room_ids = request.data.get('room_ids')
        start_ts = parse_datetime(request.data.get('start_ts'))
        end_ts = parse_datetime(request.data.get('end_ts'))

        if room_ids is None:
            room_ids = list(Room.objects.filter(
                building_id=kwargs['id'],
            ).values_list('id', flat=True))

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

        rooms_usage_list = sorted(
            rooms_usage_list, key=lambda x: x['usage'], reverse=True)

        return Response(rooms_usage_list, status=status.HTTP_200_OK)
