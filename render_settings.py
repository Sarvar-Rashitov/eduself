"""Render uchun maxsus Django settings"""
import os
from eduself.settings import *

# Render uchun maxsus sozlamalar
DEBUG = False

# Render'da ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'eduself-bqc5.onrender.com',
    'eduself.uz', 
    'www.eduself.uz',
    '127.0.0.1',
    'localhost'
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://eduself-bqc5.onrender.com',
    'https://eduself.uz',
    'https://www.eduself.uz',
]

# Render'da logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'telegram_bot': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Render'da static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Render'da security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Render'da database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

print("🚀 Render settings yuklandi")
print(f"📍 SITE_URL: {os.environ.get('SITE_URL', 'NOT_SET')}")
print(f"🤖 BOT_TOKEN: {'SET' if os.environ.get('TELEGRAM_BOT_TOKEN') else 'NOT_SET'}")
print(f"🔗 ALLOWED_HOSTS: {ALLOWED_HOSTS}")