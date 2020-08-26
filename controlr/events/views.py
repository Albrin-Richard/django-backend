from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from django_filters.rest_framework import DjangoFilterBackend


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('device_id', 'type',)

    def list(self, request, *args, **kwargs):
        # device_id = request.query_params.get('device_id', None)
        # start_date = request.query_params['start_date'] or None
        # end_date = request.query_params['end_date'] or None

        queryset = Event.objects.filter(
            building_id=kwargs['id']).order_by('timestamp')

        # if device_id:
        #     queryset = queryset.filter(object_id=device_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
