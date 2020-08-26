from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomGroupList, CurrentStatsView

urlpatterns = [
    path('rooms/', RoomViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('rooms/<int:pk>/', RoomViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('rooms/<int:pk>/current_stats/', CurrentStatsView.as_view()),
    path('room_groups/', RoomGroupList.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('room_groups/<int:pk>/', RoomGroupList.as_view({
        'delete': 'destroy'
    })),
]
