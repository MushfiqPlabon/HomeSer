# HomeSer/wsgi.py

import os

# Optimize for serverless environments
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeSer.settings")

# Enable serverless mode optimizations
os.environ.setdefault("SERVERLESS", "1")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
