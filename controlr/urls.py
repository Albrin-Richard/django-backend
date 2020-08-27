"""controlr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/auth/', include('rest_auth.urls')),
    path('v1/auth/registration/', include('rest_auth.registration.urls')),
    path('v1/', include('controlr.accounts.urls')),
    path('v1/buildings/', include('controlr.buildings.urls')),
    path('v1/buildings/<int:id>/', include('controlr.rooms.urls')),
    path('v1/buildings/<int:id>/', include('controlr.devices.urls')),
    path('v1/buildings/<int:id>/', include('controlr.events.urls')),
    path('v1/buildings/<int:id>/', include('controlr.rules.urls')),
    path('v1/buildings/<int:id>/', include('controlr.usage.urls')),
]
