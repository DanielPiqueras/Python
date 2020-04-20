import re

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status as httpcodes
from rest_framework import viewsets, authentication, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json

from DjangoLibraryRest.authentication import token_expire_handler
from DjangoLibraryRest.pagination import StandardResultsSetPagination
from .models import IsUserOwnerOrAdmin, check_if_is_valid_post, \
    check_if_is_valid_put, TokenGenerator, check_is_empty
from .serializers import UserSerializer, LoginSerializer


class CsrfExemptSession(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsUserOwnerOrAdmin,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('pk',
                       'username',
                       'email',
                       'first_name',
                       'last_name',
                       'is_staff',
                       'is_active')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Redundant because only is_staff can see the list
        if request.user.is_staff is False:
            queryset = queryset.exclude(is_active=False)

        if self.paginate_queryset(queryset) is not None \
                and self.request.query_params.get('page_size', False):
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_active is True or request.user.is_staff:
            serializer = self.get_serializer(instance)
            response = serializer.data
            status = httpcodes.HTTP_200_OK
        else:
            status = httpcodes.HTTP_404_NOT_FOUND
            response = 'Not found'

        return Response(response, status=status)

    def create(self, request, *args, **kwargs):
        try:
            users = User.objects.filter(username=request.data.get('username'))

            if len(users) != 0:
                raise ValidationError('The user already exist.')

            user = check_if_is_valid_post(request)

            serializer = UserSerializer(user)

            status = httpcodes.HTTP_201_CREATED
            response = serializer.data

        except Exception as error:
            status = httpcodes.HTTP_409_CONFLICT
            response = error.args[0]

        return Response(response, status=status)

    def update(self, request, *args, **kwargs):
        try:
            instance = check_if_is_valid_put(self.get_object(), request)
            serializer = UserSerializer(instance)
            token, created = Token.objects.get_or_create(user=instance)
            is_expired, token = token_expire_handler(token)
            data = serializer.data
            data['token'] = token.key
            response = data
            status = httpcodes.HTTP_200_OK
        except Exception as error:
            status = httpcodes.HTTP_409_CONFLICT
            response = error.args[0]

        return Response(response, status=status)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        status = httpcodes.HTTP_200_OK

        return Response(status=status)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_for_recovery_password(request):
    username = request.data.get('username', '')

    if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',
                username.lower()):
        users = User.objects.filter(email=username, is_active=True)

    else:
        users = User.objects.filter(username=username, is_active=True)

    try:

        if len(users) != 1:
            raise ValidationError(
                'The user with that email or username not exist.')

        token_generator = TokenGenerator()
        token = token_generator.make_token(users[0])

        uid = urlsafe_base64_encode(force_bytes(users[0].pk))

        response = {
            'uid': uid,
            'token': token
        }
        status = httpcodes.HTTP_200_OK
    except Exception as error:
        response = error.args[0]
        status = httpcodes.HTTP_409_CONFLICT

        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',
                    username.lower()):
            users = User.objects.filter(email=username, is_active=False)
        else:
            users = User.objects.filter(username=username, is_active=False)

        if len(users) != 0:
            response = 'The user is disabled.'

    return Response(response, status=status)


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request, uidb64, token):
    try:
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except:
            user = None

        token_generator = TokenGenerator()

        if user is not None and token_generator.check_token(user, token):
            password = request.data.get('password', 'Not found')

            data_to_check = {
                'password': password
            }

            check_is_empty(data_to_check)

            user.set_password(password)
            user.save()
            data = UserSerializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            is_expired, token = token_expire_handler(token)
            data['token'] = token.key
            response = data
            status = httpcodes.HTTP_200_OK
        else:
            raise ValidationError('Not valid change password url')

    except Exception as error:
        response = error.args[0]
        status = httpcodes.HTTP_409_CONFLICT

    return Response(response, status=status)


@api_view(['GET'])
def get_data_token(request):
    try:
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        is_expired, token = token_expire_handler(token)
        status = httpcodes.HTTP_200_OK
        data = UserSerializer(user).data
        data['token'] = token.key
        response = data

    except Exception as error:
        status = httpcodes.HTTP_409_CONFLICT
        response = error.args[0]
        if not isinstance(response, str) and response.get('non_field_errors',
                                                          False):
            response = str(response['non_field_errors'][0])

    return Response(response, status=status)


class CustomAuth(views.APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSession,)

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            is_expired, token = token_expire_handler(token)
            status = httpcodes.HTTP_200_OK
            data = UserSerializer(user).data
            data['token'] = token.key
            response = data

        except Exception as error:
            status = httpcodes.HTTP_409_CONFLICT
            response = error.args[0]
            if not isinstance(response, str) and response.get(
                    'non_field_errors', False):
                response = str(response['non_field_errors'][0])

        return Response(response, status=status)


class CustomLogOut(views.APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSession,)

    def post(self, request):
        try:
            logout(request)
            status = httpcodes.HTTP_200_OK
        except Exception as error:
            status = httpcodes.HTTP_409_CONFLICT

        return Response(status=status)


def server_error(request, *args, **kwargs):
    data = 'Server Error (500)'

    return HttpResponse(json.dumps(data),
                        status=httpcodes.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json')


def bad_request(request, exception, *args, **kwargs):
    data = 'Bad Request (400)'

    return Response(json.dumps(data), status=httpcodes.HTTP_400_BAD_REQUEST,
                    content_type='application/json')
