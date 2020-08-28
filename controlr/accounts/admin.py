from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'first_name', 'last_name',
              'is_active', 'is_superuser', 'is_staff', ]


admin.site.register(User, UserAdmin)
