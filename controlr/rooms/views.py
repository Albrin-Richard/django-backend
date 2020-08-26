from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from .models import Room, RoomGroup
from .serializers import RoomListSerializer, RoomDetailSerializer, RoomGroupSerializer, CurrentStatsSerializer
from controlr.utils.unique_id_generator import generate_unique_id
from rest_framework.response import Response
from controlr.buildings.models import Building
from controlr.devices.models import DeviceState, Device
from django.db.models import Sum


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return RoomListSerializer
        else:
            return RoomDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = Room.objects.filter(building_id=kwargs['id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        serializer.save(building=building)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RoomGroupList(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin
):
    queryset = RoomGroup.objects.all()
    serializer_class = RoomGroupSerializer

    def list(self, request, *args, **kwargs):
        queryset = RoomGroup.objects.filter(building_id=kwargs['id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        serializer.save(building=building)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CurrentStatsView(APIView):
    def get(self, request, *args, **kwargs):
        room_id = kwargs['pk']
        room_name = Room.objects.get(id=room_id).name
        num_devices_on = DeviceState.objects.filter(
            device__room=room_id, state=True).count()
        num_devices_total = DeviceState.objects.filter(
            device__room=room_id).count()
        current_power_usage = Device.objects.filter(
            state=True, room=room_id).aggregate(Sum('power'))['power__sum']

        serializer = CurrentStatsSerializer(
            data={
                'room_id': room_id,
                'room_name': room_name,
                'num_devices_on': num_devices_on,
                'num_devices_total': num_devices_total,
                'current_power_usage': current_power_usage
            }
        )

        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
