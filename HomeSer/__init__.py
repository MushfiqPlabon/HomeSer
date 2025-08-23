# HomeSer/__init__.py
try:
    from .celery import app as celery_app

    __all__ = ("celery_app",)
except ImportError:
    # Celery is not available (e.g., in Vercel deployment)
    pass
