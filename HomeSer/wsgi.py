# HomeSer/wsgi.py

import os
import sys

# Add your project's root directory to the Python path
# This is often needed if your Django project is nested
# For example, if your wsgi.py is at my_repo/backend/my_project_name/wsgi.py
# you might need to add 'my_repo/backend' to the path.
# Adjust the path based on your actual project structure.
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

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

# Vercel requires an 'app' variable that exposes the WSGI callable
# This needs to be a callable, not the result of calling get_wsgi_application()
def app(environ, start_response):
    return application(environ, start_response)

# Also provide handler for compatibility
handler = app