"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

# Email
DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL',
    default='APP_NAME_HERE <noreply@app_name_here.com>'
)

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# COOKIE DOMAIN
COOKIE_DOMAIN = env('COOKIE_DOMAIN', default='127.0.0.1')

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405

# Celery
# This vars is for not do async tasks in development
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
