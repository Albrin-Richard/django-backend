from django.urls import path, include
from .views import TimerViewSet, ScheduleViewSet

urlpatterns = [
    path('timers/', TimerViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('timers/<int:pk>/', TimerViewSet.as_view({
        'delete': 'destroy'
    })),
    path('schedules/', ScheduleViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'delete': 'destroy'
    })),
    path('schedules/<int:pk>/', ScheduleViewSet.as_view({
        'delete': 'destroy'
    })),
    path('schedules/<int:pk>/switch/', ScheduleViewSet.as_view({
        'put': 'switch'
    })),
]
