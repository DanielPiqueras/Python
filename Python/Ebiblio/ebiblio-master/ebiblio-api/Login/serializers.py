import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('pk',)
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active'
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',
                        username.lower()):
                users = User.objects.filter(email=username)

                if len(users) != 1:
                    raise ValidationError(
                        'The user with that username or email not exist.')

                username = users[0].username

        user = authenticate(username=username,
                            password=password)

        if not user:

            user_aux = User.objects.filter(username=attrs['username'])

            if len(user_aux) != 0:
                if not user_aux[0].is_active:
                    raise ValidationError('User is disabled.')

            raise ValidationError('Incorrect username or password.')

        return {'user': user}
