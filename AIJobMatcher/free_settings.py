"""
Free platform optimized settings for AIJobMatcher project.

Optimized for free hosting platforms with resource limitations.
"""

from .production import *
import os

# Free platform optimizations
CONN_MAX_AGE = 60  # Database connection pooling

# Reduce resource usage - minimal logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',  # Only warnings and errors
    },
}

# Cache with file backend (no Redis needed for free tier)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

# Session with file backend (no Redis needed)
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/tmp/sessions'

# Performance optimizations for free platforms
MIDDLEWARE += ['django.middleware.gzip.GZipMiddleware']

# Optimize static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Database optimization
DATABASES['default']['CONN_MAX_AGE'] = 60

# Reduce session load
SESSION_SAVE_EVERY_REQUEST = False

# Media files optimization
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email backend for free platforms (use console for testing)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security settings for free platforms
SECURE_SSL_REDIRECT = False  # Let platform handle SSL
SESSION_COOKIE_SECURE = False  # Let platform handle SSL
CSRF_COOKIE_SECURE = False   # Let platform handle SSL
