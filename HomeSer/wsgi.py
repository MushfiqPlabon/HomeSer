# HomeSer/wsgi.py

import os

# Optimize for serverless environments
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeSer.settings")

# Enable serverless mode optimizations
os.environ.setdefault("SERVERLESS", "1")

# Ensure staticfiles directory exists
static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
os.makedirs(static_root, exist_ok=True)

from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()

# Vercel requires an 'app' variable that exposes the WSGI application
app = application

# Also provide handler for compatibility
handler = application