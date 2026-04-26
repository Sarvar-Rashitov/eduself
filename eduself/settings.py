import os
from pathlib import Path
from environs import Env
import dj_database_url
from dotenv import load_dotenv

# Load .env file
load_dotenv()

env = Env()
env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SESSION_SECRET', 'django-insecure-dev-key-change-in-production')

# DEBUG mode
DEBUG = True

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Render.com handles SSL
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['eduself-bqc5.onrender.com', 'eduself.uz', 'www.eduself.uz', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'crispy_forms',
    'crispy_bootstrap5',
    'core',
    'accounts',
    'ai_assistant',
    'telegram_bot',
    'subscriptions',
]

# Jazzmin Admin Theme Configuration
JAZZMIN_SETTINGS = {
    # Title
    "site_title": "EduSelf Admin",
    "site_header": "EduSelf",
    "site_brand": "EduSelf",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "EduSelf Admin Paneliga xush kelibsiz",
    "copyright": "EduSelf © 2024",
    
    # Search
    "search_model": ["auth.User", "core.Institution", "core.Subject"],
    
    # User Menu
    "topmenu_links": [
        {"name": "Saytga o'tish", "url": "/", "new_window": True},
        {"model": "auth.user"},
    ],
    
    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Subject": "fas fa-book",
        "core.SubjectCategory": "fas fa-folder",
        "core.Topic": "fas fa-bookmark",
        "core.Test": "fas fa-clipboard-list",
        "core.Question": "fas fa-question-circle",
        "core.Answer": "fas fa-check-circle",
        "core.Certificate": "fas fa-award",
        "core.CertificateTopic": "fas fa-certificate",
        "core.CertificateTest": "fas fa-file-alt",
        "core.MockExam": "fas fa-file-signature",
        "core.MockExamCategory": "fas fa-layer-group",
        "core.Institution": "fas fa-university",
        "core.InstitutionCategory": "fas fa-building",
        "core.InstitutionDirection": "fas fa-graduation-cap",
        "core.Course": "fas fa-play-circle",
        "core.CourseCategory": "fas fa-th-large",
        "core.Lesson": "fas fa-video",
        "core.News": "fas fa-newspaper",
        "core.NewsCategory": "fas fa-tags",
        "core.UserTestResult": "fas fa-chart-bar",
        "core.SiteSettings": "fas fa-cog",
        "core.Partner": "fas fa-handshake",
        "accounts.Profile": "fas fa-id-card",
        "ai_assistant.AIConversation": "fas fa-robot",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    
    # Related Modal
    "related_modal_active": True,
    
    # Custom CSS/JS
    "custom_css": None,
    "custom_js": None,
    
    # UI Tweaks
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n uchun
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.UserLanguageMiddleware',  # User tilini avtomatik o'rnatish
    'accounts.onboarding_middleware.OnboardingMiddleware',  # Onboarding redirect
]

ROOT_URLCONF = 'eduself.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.notifications',
                'core.context_processors.auth_settings',
                'core.context_processors.language_context',  # Til context
                'accounts.onboarding_context.user_preferences',  # Onboarding preferences
            ],
        },
    },
]

WSGI_APPLICATION = 'eduself.wsgi.application'

# Database configuration
# SQLite yoki PostgreSQL (environment variable orqali)
DATABASES = {
    'default': dj_database_url.config(default=env("DATABASE_URL"))
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'uz'

# Internationalization (i18n) - 7 til qo'llab-quvvatlanadi
LANGUAGES = [
    ('uz', 'O\'zbekcha'),
    ('en', 'English'),
    ('ru', 'Русский'),
    ('kk', 'Қазақша'),
    ('kaa', 'Qaraqalpaqsha'),
    ('tg', 'Тоҷикӣ'),
    ('ky', 'Кыргызча'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# DeepSeek AI API for dynamic translation
# Multiple API keys for load balancing (worker timeout oldini olish uchun)
DEEPSEEK_API_KEY_1 = os.environ.get('DEEPSEEK_API_KEY_1', '')
DEEPSEEK_API_KEY_2 = os.environ.get('DEEPSEEK_API_KEY_2', '')
DEEPSEEK_API_KEY_3 = os.environ.get('DEEPSEEK_API_KEY_3', '')
DEEPSEEK_API_KEY_4 = os.environ.get('DEEPSEEK_API_KEY_4', '')
DEEPSEEK_API_KEY_5 = os.environ.get('DEEPSEEK_API_KEY_5', '')

# Legacy key (backward compatibility)
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Cloudflare R2 Storage Configuration
USE_S3 = os.environ.get('USE_S3', 'False') == 'True'

if USE_S3:
    # AWS S3 settings for Cloudflare R2
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'auto')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Media files only (not static files)
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/' if AWS_S3_CUSTOM_DOMAIN else f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/'
    
    # Django 4.2+ STORAGES setting
    STORAGES = {
        "default": {
            "BACKEND": "core.storage_backends.MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
else:
    # Local storage (development)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # Default STORAGES for local development
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0

# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True if os.environ.get('DEBUG', 'False') == 'True' else False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

AUTH_USER_MODEL = 'accounts.User'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailPhoneBackend',  # Email yoki telefon bilan login
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 hafta (sekundlarda)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False  # Development uchun False, production'da True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'EduSelf <noreply@eduself.uz>')

# Google OAuth
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_BOT_USERNAME = os.environ.get('TELEGRAM_BOT_USERNAME', '')

# Site URL
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

# Payment Integration Settings
# Click Payment
CLICK_MERCHANT_ID = os.environ.get('CLICK_MERCHANT_ID', '')
CLICK_SERVICE_ID = os.environ.get('CLICK_SERVICE_ID', '')
CLICK_SECRET_KEY = os.environ.get('CLICK_SECRET_KEY', '')
CLICK_MERCHANT_USER_ID = os.environ.get('CLICK_MERCHANT_USER_ID', '')

# Payme Payment
PAYME_MERCHANT_ID = os.environ.get('PAYME_MERCHANT_ID', '')
PAYME_SECRET_KEY = os.environ.get('PAYME_SECRET_KEY', '')
PAYME_ENDPOINT = os.environ.get('PAYME_ENDPOINT', 'https://checkout.paycom.uz')

CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.dev',
    'https://*.repl.co',
    'https://eduself.uz',
    'https://www.eduself.uz',
]

X_FRAME_OPTIONS = 'ALLOWALL'
