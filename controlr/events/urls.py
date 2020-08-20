from django.urls import path, include
from .views import EventViewSet

urlpatterns = [
    path('events/', EventViewSet.as_view({
        'get': 'list'
    }))
]
