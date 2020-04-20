from datetime import timedelta
from django.utils.timezone import now
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_409_CONFLICT


def expires_in(token):
    time_elapsed = now() - token.created
    left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


class CustomAuthToken(TokenAuthentication):
    keyword = 'Token'

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise ValidationError('Invalid token.', code=HTTP_409_CONFLICT)

        if not token.user.is_active:
            raise ValidationError('User inactive or deleted.', code=HTTP_409_CONFLICT)

        is_expired, token = token_expire_handler(token)

        if is_expired:
            raise ValidationError('The Token is expired', code=HTTP_409_CONFLICT)

        return token.user, token