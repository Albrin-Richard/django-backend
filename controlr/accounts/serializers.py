from rest_framework import serializers
from .models import User
from allauth.account.adapter import get_adapter


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'password']

    def save(self, request):
        data = request.data
        user = User.objects.create_user(
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password=data.get('password')
        )

        return user
