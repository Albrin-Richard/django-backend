from rest_framework import viewsets, status, generics, mixins
from .models import Room, RoomGroup
from .serializers import RoomListSerializer, RoomDetailSerializer, RoomGroupSerializer
from controlr.utils.unique_id_generator import generate_unique_id
from rest_framework.response import Response
from controlr.buildings.models import Building


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return RoomListSerializer
        else:
            return RoomDetailSerializer
        # I dont' know what you want for create/destroy/update.

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
