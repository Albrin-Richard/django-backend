from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .models import Building, Group
from .serializers import BuildingSerializer, GroupSerializer
from django.db.models import Count
from controlr.devices.models import Device


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

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

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
