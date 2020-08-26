from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, GroupViewSet, CurrentStatsView

router = DefaultRouter()
router.register(r'', BuildingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/groups/', GroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<int:id>/groups/<int:pk>/', GroupViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<int:id>/current_stats/', CurrentStatsView.as_view())
]
