from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def create_jwt_tokens_for_user(user):
    """
    Create JWT tokens for a user and return them
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def set_jwt_cookies(response, access_token, refresh_token=None):
    """
    Set JWT tokens in HTTP-only cookies
    """
    # Set access token cookie
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        expires=timezone.now() + timedelta(
            minutes=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].minutes
        )
    )
    
    # Set refresh token cookie if provided
    if refresh_token:
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            expires=timezone.now() + timedelta(
                days=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].days
            )
        )
    
    return response


def unset_jwt_cookies(response):
    """
    Remove JWT tokens from cookies
    """
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response