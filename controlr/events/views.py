from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('device',)
    ordering = ('-timestamp',)

    def list(self, request, *args, **kwargs):
        # device_id = request.query_params.get('device_id', None)
        # start_date = request.query_params['start_date'] or None
        # end_date = request.query_params['end_date'] or None

        queryset = Event.objects.filter(
            building_id=kwargs['id']).order_by('timestamp')
        filtered_queryset = self.filter_queryset(queryset)
        # if device_id:
        #     queryset = queryset.filter(object_id=device_id)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
