from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

urlpatterns = [
    path('devices/', DeviceViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('devices/favorites/', DeviceViewSet.as_view({
        'get': 'favorites',
    })),

    path('devices/<int:pk>/', DeviceViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    path('devices/<int:pk>/switch/', DeviceViewSet.as_view({
        'put': 'switch',
    })),

    path('devices/<int:pk>/favorite/', DeviceViewSet.as_view({
        'put': 'favorite',
        'delete': 'favorite'
    })),
]
