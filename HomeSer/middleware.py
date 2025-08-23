from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.middleware import get_user


User = get_user_model()


class JWTAuthenticationMiddleware:
    """
    Middleware to authenticate users based on JWT tokens in cookies
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to authenticate user with JWT token from cookies
        if not hasattr(request, 'user') or request.user.is_anonymous:
            request.user = self.get_jwt_user(request)
            
        response = self.get_response(request)
        return response

    def get_jwt_user(self, request):
        """
        Get user from JWT token in cookies
        """
        # Get tokens from cookies
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return AnonymousUser()
            
        try:
            # Authenticate using JWT
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            return user
        except (InvalidToken, TokenError):
            # Token is invalid, return anonymous user
            return AnonymousUser()
        except Exception:
            # Any other error, return anonymous user
            return AnonymousUser()