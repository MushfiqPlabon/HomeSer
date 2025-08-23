from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def jwt_login_required(view_func):
    """
    Decorator that ensures the user is authenticated with JWT token.
    Works for both web views and API views.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Check if user is already authenticated (from session or JWT middleware)
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        
        # Try to authenticate with JWT token from cookies
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            # For AJAX requests, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Authentication required'}, status=401)
            # For regular requests, redirect to login
            return redirect('login')
            
        try:
            # Authenticate using JWT
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            
            # Set user in request
            request.user = user
            
            return view_func(request, *args, **kwargs)
        except (InvalidToken, TokenError):
            # Token is invalid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid token'}, status=401)
            return redirect('login')
        except Exception:
            # Any other error
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Authentication failed'}, status=401)
            return redirect('login')
            
    return wrapped_view