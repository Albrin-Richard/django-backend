from django.urls import path, include
from .views import DevicesUsageTotal, DevicesUsageList, DevicesUsageTimeseries, RoomsUsageList, RecentUsage

urlpatterns = [
    path('usage/recent/', RecentUsage.as_view()),
    path('usage/devices/total/', DevicesUsageTotal.as_view()),
    path('usage/devices/list/', DevicesUsageList.as_view()),
    path('usage/devices/timeseries/', DevicesUsageTimeseries.as_view()),
    path('usage/rooms/list/', RoomsUsageList.as_view())
]
