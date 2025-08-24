# HomeSer/wsgi.py

import os

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HomeSer.settings')

# Get the WSGI application
from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()