# settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
env_path = BASE_DIR.parent / '.env'
load_dotenv(env_path, override=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY environment variable is not set.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Hosts allowed to access the application
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF Trusted Origins for production
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF Trusted Origins for production
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')

# CORS Allowed Origins for production
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')

# CORS Allowed Origins for production
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')
if not DEBUG and not CORS_ALLOWED_ORIGINS:
    raise ImproperlyConfigured("CORS_ALLOWED_ORIGINS must be set in production.")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "cloudinary",
    "cloudinary_storage",
    "django_celery_results",
    "HomeSer",
]

if DEBUG:
    INSTALLED_APPS += ["whitenoise.runserver_nostatic"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "HomeSer.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "HomeSer.wsgi.application"

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# Supabase PostgreSQL configuration (no fallback to SQLite)

# Get database configuration from environment variables using python-dotenv
DB_USER = os.getenv('user', '').strip()
DB_PASSWORD = os.getenv('password', '').strip()
DB_HOST = os.getenv('host', '').strip()
DB_PORT = os.getenv('port', '').strip()
DB_NAME = os.getenv('dbname', '').strip()

# Always use Supabase PostgreSQL configuration
# Always use Supabase PostgreSQL configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    db_config = dj_database_url.parse(DATABASE_URL)
    # Add SSL options for Supabase
    db_config['OPTIONS'] = {
        'sslmode': 'require',
        'connect_timeout': 10,
    }
    DATABASES = {
        'default': db_config
    }
else:
    # Default to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR.parent / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "HomeSer.User"

# DRF Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/hour", "user": "1000/hour"},
}

# SimpleJWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", 60))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", 1))),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", 60))),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", 1))),
}

import ssl

# Cache configuration
# https://docs.djangoproject.com/en/stable/topics/cache/
if os.getenv("REDIS_URL"):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "TIMEOUT": int(os.getenv("CACHE_TTL", 900)),  # 15 minutes default
        }
    }
else:
    # Default to local memory cache for development
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }

CACHE_TTL = int(os.getenv("CACHE_TTL", 900))  # 15 minutes default

# Session configuration
# https://docs.djangoproject.com/en/stable/topics/http/sessions/
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = int(os.getenv("SESSION_COOKIE_AGE", 1209600))  # 2 weeks default
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Email configuration
# https://docs.djangoproject.com/en/stable/topics/email/
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 25))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "webmaster@localhost")

# Cloudinary configuration
# https://cloudinary.com/documentation/django_integration
if os.getenv("CLOUDINARY_URL"):
    # Using single environment variable approach
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
elif os.getenv("CLOUDINARY_CLOUD_NAME") and os.getenv("CLOUDINARY_API_KEY") and os.getenv("CLOUDINARY_API_SECRET"):
    # Using individual environment variables approach
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Celery configuration
# https://docs.celeryproject.org/en/stable/django/
if os.getenv("REDIS_URL"):
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_REDIS_USE_SSL = os.getenv("CELERY_REDIS_USE_SSL", "True").lower() == "true"
    CELERY_BROKER_USE_SSL = os.getenv("CELERY_BROKER_USE_SSL", "True").lower() == "true"
    CELERY_BEAT_SCHEDULER = os.getenv("CELERY_BEAT_SCHEDULER", "django_celery_beat.schedulers:DatabaseScheduler")
    CELERY_BROKER_RETRY_ON_STARTUP = os.getenv("CELERY_BROKER_RETRY_ON_STARTUP", "True").lower() == "true"

    # Additional Celery settings
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
else:
    # Default to local memory for development (eager mode)
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

# DRF Spectacular Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'HomeSer API',
    'DESCRIPTION': 'A modern Household Service Providing Platform - API Documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Detailed descriptions for better understanding
    'DESCRIPTION': '''
    Welcome to the HomeSer API documentation!
    
    This API allows you to interact with our household service platform programmatically.
    
    ## Getting Started
    1. Register a new user account using the authentication endpoints
    2. Log in to receive authentication tokens
    3. Use the tokens to access protected endpoints
    
    ## Authentication
    Most endpoints require authentication via JWT tokens. Include your token in the Authorization header:
    `Authorization: Bearer <your-token-here>`
    
    ## Common Response Formats
    - Success responses typically return JSON objects with your requested data
    - Error responses follow standard HTTP status codes with descriptive messages
    
    ## Key Resources
    - **Users**: Manage user accounts and roles
    - **Services**: Browse available household services
    - **Cart**: Manage your service selections before checkout
    - **Orders**: View and track your service orders
    - **Reviews**: Leave feedback on completed services
    
    For any questions, please refer to our main documentation or contact support.
    ''',
    'TAGS': [
        {'name': 'Users', 'description': 'User account management'},
        {'name': 'Services', 'description': 'Household services available on the platform'},
        {'name': 'Cart', 'description': 'Shopping cart functionality'},
        {'name': 'Orders', 'description': 'Service order management'},
        {'name': 'Reviews', 'description': 'Service reviews and ratings'},
    ],
    # Disable browser cache for better development experience
    'SERVE_PUBLIC': True,
}