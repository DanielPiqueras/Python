import re

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int
from rest_framework import status, serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS


# Permission classes

class IsUserOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if (view.action == 'list' or request.method == 'POST') and \
                not request.user.is_staff:

            return False
        elif request.user.is_authenticated:

            return bool(request.user and request.user.is_authenticated)

        else:
            return False

    def check_object_permission(self, user, obj):
        return bool(user and user.is_authenticated and
                    bool(user.is_staff or obj == user))

    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request.user, obj)


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if (request.user.pk == view.kwargs['user_id']) or request.user.is_staff:
            return True
        else:
            return False


class IsAdminOrReadListBookOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsAdminOrOnlyRent(BasePermission):
    def has_permission(self, request, view):
        if (request.method != 'POST' and request.method != 'PUT') and \
                not request.user.is_staff:

            return False
        elif request.user.is_authenticated:

            return bool(request.user and request.user.is_authenticated)

        else:
            return False


# Check if data is valid

def check_is_empty(attrs):
    for attribute in attrs:
        if attrs[attribute] == 'Not found':
            raise serializers.ValidationError(
                'The {data} has not been sent'.format(data=attribute))

        if isinstance(attrs[attribute], str) is False:
            raise serializers.ValidationError(
                'The {data} need to be string'.format(data=attribute),
                code=status.HTTP_409_CONFLICT)

        if len(attrs[attribute]) == 0:
            raise serializers.ValidationError(
                'The {data} is empty'.format(data=attribute),
                code=status.HTTP_409_CONFLICT)

        if ' ' in attrs[attribute]:
            raise serializers.ValidationError(
                'The {data} should not contain spaces'.format(data=attribute))

    return True


def check_email(email):
    if isinstance(email, str) is False:
        raise serializers.ValidationError('The email need to be string')

    if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',
                email.lower()):
        return True
    else:
        raise serializers.ValidationError('Not valid email')


def check_is_in(param):
    response = {
        True: True,
        False: False,
        'true': True,
        'false': False,
    }

    if not isinstance(param, str) and not isinstance(param, bool):
        raise serializers.ValidationError('Only true or false in string')

    if isinstance(param, str):
        param = param.lower()

    if param not in response:
        raise serializers.ValidationError('Only true or false in string')

    return response[param]


def check_if_is_valid_post(request):
    field = ''
    if request.data.get('email', '') != '':
        check_email(request.data['email'])

        if len(User.objects.filter(email=request.data['email'])) != 0:
            raise serializers.ValidationError(
                'This email is being used by another user.')

    data_to_check = {
        'username': request.data.get('username', 'Not found'),
        'password': request.data.get('password', 'Not found'),
        'repeat_password': request.data.get('repeat_password', 'Not found')
    }

    check_is_empty(data_to_check)

    check_is_staff = request.data.get('is_staff', False)

    is_staff = check_is_in(check_is_staff)

    if isinstance(request.data.get('first_name', ''), str):
        first_name = request.data.get('first_name', '')

    else:
        field += 'First name, '

    if isinstance(request.data.get('last_name', ''), str):
        last_name = request.data.get('last_name', '')
    else:
        field += 'Last name'

    if request.data['password'] != request.data['repeat_password']:
        raise serializers.ValidationError(
            'The two password need to be identical')

    if field != "":
        raise serializers.ValidationError(
            'Invalid data for {fields}'.format(fields=field))

    user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
    )

    user.is_staff = is_staff

    user.first_name = first_name

    user.email = request.data.get('email', user.email)

    user.last_name = last_name

    user.save()

    return user


def check_if_is_valid_put(instance, request):
    field = ""
    if request.data.get('email', '') != '':
        check_email(request.data['email'])

        if len(User.objects.filter(email=request.data['email']).exclude(pk=instance.pk)) != 0:
            raise serializers.ValidationError(
                'This email is being used by another user.')

    check_is_staff = request.data.get('is_staff', False)
    check_is_active = request.data.get('is_active', True)

    is_staff = check_is_in(check_is_staff)
    is_active = check_is_in(check_is_active)

    if request.data.get('first_name') is not None and isinstance(
            request.data.get('first_name', ''), str):
        instance.first_name = request.data.get('first_name',
                                               instance.first_name)
    else:
        field += 'First name, '

    instance.email = request.data.get('email', instance.email)

    if request.data.get('last_name') is not None and isinstance(
            request.data.get('last_name', ''), str):
        instance.last_name = request.data.get('last_name',
                                              instance.last_name)
    else:
        field += 'Last name, '

    if request.data.get('username') is not None:
        check_is_empty({'username': request.data.get('username', 'Not found')})
        instance.username = request.data.get('username',
                                             instance.username)
    else:
        field += 'Username, '

    if request.data.get('password', 'notFound') is None or request.data.get(
            'repeat_password', 'notFound') is None:
        field += 'Password'

    if field != "":
        raise serializers.ValidationError(
            'Invalid data for {fields}'.format(fields=field))

    if request.data.get('password', '') != '' or request.data.get(
            'repeat_password', '') != '':

        check_is_empty({'password': request.data.get('password', 'Not found'),
                        'repeat_password': request.data.get('repeat_password',
                                                            'Not found')})

        if instance.check_password(request.data.get('old_password', '')) and \
                request.data['password'] == request.data['repeat_password']:
            instance.set_password(request.data['password'])

        elif request.data['password'] != request.data['repeat_password']:
            raise serializers.ValidationError(
                'The password need to be identical')

        else:
            raise serializers.ValidationError('Incorrect old passwords')

    instance.is_active = is_active
    instance.is_staff = is_staff
    instance.save()

    return instance


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)
                + six.text_type(timestamp)
                + six.text_type(user.is_active))

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts),
                                     token):
            return False

        if (self._num_days(self._today()) - ts) > 1:
            return False

        return True
