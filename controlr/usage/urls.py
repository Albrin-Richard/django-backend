from django.urls import path, include
from .views import DeviceUsageTotal, DeviceUsageList, DeviceUsageTimeseries, RoomUsageList

urlpatterns = [
    path('usage/devices/total/', DeviceUsageTotal.as_view()),
    path('usage/devices/list/', DeviceUsageList.as_view()),
    path('usage/devices/timeseries/', DeviceUsageTimeseries.as_view()),
    path('usage/rooms/list/', RoomUsageList.as_view())
]
