from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Building, Group
from .serializers import BuildingSerializer, GroupListSerializer, GroupDetailSerializer, CurrentStatsSerializer
from django.db.models import Count, Sum
from controlr.devices.models import Device, DeviceState
from controlr.rooms.models import Room


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer

    def get_queryset(self):
        user = self.request.user
        return Building.objects.filter(owner=user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return GroupListSerializer
        else:
            return GroupDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = Group.objects.filter(building=kwargs['id']).annotate(
            num_devices=Count('devices'))
        serializer = self.get_serializer(queryset, many=True)
        request.session['django_timezone'] = 'Asia/Kolkata'
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        serializer.save(building=building)
        print(serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CurrentStatsView(APIView):
    def get(self, request, *args, **kwargs):
        building_id = kwargs['id']

        building_name = Building.objects.get(id=building_id).name

        num_devices_total = DeviceState.objects.filter(
            device__building=building_id).count()

        num_devices_on = DeviceState.objects.filter(
            state=True, device__building=building_id).count()

        current_power_usage = Device.objects.filter(
            building=building_id, state__state=True).aggregate(Sum('power'))['power__sum']

        num_rooms_total = Room.objects.filter(building=building_id).count()

        num_rooms_on = 0

        for room in Room.objects.filter(building=building_id):
            on_devices = DeviceState.objects.filter(
                device__room=room.id, state=True).count()
            if on_devices > 0:
                num_rooms_on += 1

        serializer = CurrentStatsSerializer(
            data={
                'building_id': building_id,
                'building_name': building_name,
                'num_devices_on': num_devices_on,
                'num_devices_total': num_devices_total,
                'num_rooms_total': num_rooms_total,
                'num_rooms_on': num_rooms_on,
                'current_power_usage': current_power_usage
            }
        )

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
