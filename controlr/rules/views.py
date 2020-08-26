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


class TimerViewSet(viewsets.ModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

    def list(self, request, *args, **kwargs):
        queryset = Timer.objects.filter(building_id=kwargs['id'])
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        building = Building.objects.get(id=kwargs['id'])
        timer = serializer.save(building=building)

        time_delta = serializer.validated_data['time_delta']
        # timer_id = serializer.data['id']
        timer_schedule.add_timer(
            timer_id=timer.id,
            device_id=data['device'],
            state_change=data['state_change'],
            time_delta=time_delta
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        timer_schedule.remove_schedule(kwargs['pk'])

        return Response(status=status.HTTP_204_NO_CONTENT)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def list(self, request, *args, **kwargs):
        queryset = Schedule.objects.filter(building_id=kwargs['id'])
        serializer = self.get_serializer(queryset, many=True)

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
        Schedule.objects.filter(id=pk).update(state=request.data['state'])

        schedule_schedule.switch_schedule_state(
            schedule_id=pk, state_change=request.data['state'])

        return Response({'message': 'success'}, status=status.HTTP_200_OK)
