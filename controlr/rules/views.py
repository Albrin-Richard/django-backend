from rest_framework import viewsets
from .models import Timer, Schedule
from .serializers import TimerSerializer, ScheduleSerializer
from rest_framework.response import Response
from datetime import timedelta
from rest_framework import status
from datetime import datetime
from .schedules import timer_schedule
from .schedules import schedule_schedule
from controlr.buildings.models import Building
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class TimerViewSet(viewsets.ModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('device',)

    def list(self, request, *args, **kwargs):
        queryset = Timer.objects.filter(building_id=kwargs['id'])
        filtered_queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(filtered_queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        timer = serializer.save(building=building)

        trigger_time = serializer.validated_data['trigger_time']
        # timer_id = serializer.data['id']
        timer_schedule.add_timer(
            timer_id=timer.id,
            device_id=data['device'],
            state_change=data['state_change'],
            trigger_time=trigger_time
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        timer_schedule.remove_timer(kwargs['pk'])

        return Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('device',)

    def list(self, request, *args, **kwargs):
        queryset = Schedule.objects.filter(building_id=kwargs['id'])
        filtered_queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(filtered_queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        schedule = serializer.save(building=building)

        data = serializer.validated_data

        time = data['time']

        schedule_schedule.add_schedule(
            schedule_id=schedule.id,
            device_id=schedule.device_id,
            state_change=data['state_change'],
            hour=time.hour,
            minute=time.minute,
            days_of_week=data['days_of_week']
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        schedule_schedule.remove_schedule(kwargs['pk'])

        return Response(status=status.HTTP_204_NO_CONTENT)

    def switch(self, request, pk=None, id=None):
        current_state = Schedule.objects.get(id=pk).state
        state_change = request.data['state_change']

        if current_state == state_change:
            return Response({'message': 'failure'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Schedule.objects.filter(id=pk).update(state=state_change)

        schedule_schedule.switch_schedule_state(
            schedule_id=pk, state_change=state_change)

        return Response({'message': 'success'}, status=status.HTTP_200_OK)
