from rest_framework import viewsets
from django.utils import timezone
from .models import Device, DeviceState
from .serializers import DeviceSerializer, DeviceStateSerializer, FavoriteSerializer
from controlr.rooms.models import Room
from controlr.buildings.models import Building
from rest_framework.response import Response
from rest_framework import status
from controlr.events.models import Event
from controlr.signals.signals import event_signal


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def list(self, request, *args, **kwargs):
        queryset = Device.objects.filter(building_id=kwargs['id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        device = serializer.save(building=building)

        event_signal.send(
            sender=self.__class__,
            timestamp=timezone.now(),
            type=Event.DEVICE_CREATED,
            description='Device has been created',
            device_id=device.id,
            building_id=kwargs['id']
        )

        # Initialize the state of the device as True
        state_object = DeviceState.objects.create(device=device, state=False)
        state_serializer = DeviceStateSerializer(data=state_object)
        if (state_serializer.is_valid()):
            state_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def switch(self, request, pk=None, id=None):
        state_object = DeviceState.objects.filter(
            device=pk).update(state=request.data['state'])

        event_signal.send(
            sender=self.__class__,
            timestamp=timezone.now(),
            type=Event.DEVICE_CREATED,
            description='Device Switched On',
            device_id=pk,
            state_change=request.data['state'],
            building_id=id
        )
        return Response({'message': 'success'}, status=status.HTTP_200_OK)

    def favorites(self, request, id=None):
        favorite_devices = Device.objects.filter(
            building_id=id).filter(is_favorite=True)
        serializer = FavoriteSerializer(favorite_devices, many=True)
        return Response(serializer.data)

    def favorite(self, request, pk=None, id=None):
        if request.method == 'PUT':
            Device.objects.filter(id=pk).update(is_favorite=True)
        if request.method == 'DELETE':
            Device.objects.filter(id=pk).update(is_favorite=False)
        return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
