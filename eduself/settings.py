import os
from pathlib import Path
from environs import Env
import dj_database_url

env = Env()
env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SESSION_SECRET', 'django-insecure-dev-key-change-in-production')

DEBUG = True

ALLOWED_HOSTS = ['eduself-bqc5.onrender.com', 'eduself.uz', 'www.eduself.uz', '127.0.0.1']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'crispy_forms',
    'crispy_bootstrap5',
    'core',
    'accounts',
    'ai_assistant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'eduself.wsgi.application'

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

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

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

CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.dev',
    'https://*.repl.co',
    'https://eduself.uz',
    'https://www.eduself.uz',
]

X_FRAME_OPTIONS = 'ALLOWALL'

# Jazzmin Admin Configuration
JAZZMIN_SETTINGS = {
    # Sarlavha
    "site_title": "EduSelf Admin",
    "site_header": "EduSelf",
    "site_brand": "EduSelf",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    
    # Xush kelibsiz matni
    "welcome_sign": "EduSelf Boshqaruv Paneliga Xush Kelibsiz",
    "copyright": "EduSelf © 2024",
    
    # Qidiruv modellari
    "search_model": ["accounts.User", "core.Subject", "core.Test"],
    
    # Foydalanuvchi avatar
    "user_avatar": None,
    
    # Yuqori menyu
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Saytga o'tish", "url": "/", "new_window": True},
        {"model": "accounts.User"},
    ],
    
    # Foydalanuvchi menyu
    "usermenu_links": [
        {"name": "Saytga o'tish", "url": "/", "new_window": True, "icon": "fas fa-globe"},
        {"model": "accounts.User"},
    ],
    
    # Yon menyu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Tartib
    "order_with_respect_to": [
        "accounts",
        "core",
        "ai_assistant",
    ],
    
    # Ikonkalar
    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.User": "fas fa-user",
        "core.Subject": "fas fa-book",
        "core.SubjectCategory": "fas fa-folder",
        "core.Topic": "fas fa-list",
        "core.Test": "fas fa-clipboard-check",
        "core.Question": "fas fa-question-circle",
        "core.Answer": "fas fa-check-circle",
        "core.TestResult": "fas fa-chart-bar",
        "core.Certificate": "fas fa-certificate",
        "core.CertificateTopic": "fas fa-list-alt",
        "core.CertificateTest": "fas fa-file-alt",
        "core.CertificateQuestion": "fas fa-question",
        "core.CertificateResult": "fas fa-trophy",
        "core.MockExamCategory": "fas fa-folder-open",
        "core.MockExam": "fas fa-graduation-cap",
        "core.MockExamQuestion": "fas fa-question",
        "core.MockExamResult": "fas fa-medal",
        "core.Institution": "fas fa-university",
        "core.InstitutionCategory": "fas fa-building",
        "core.InstitutionDirection": "fas fa-directions",
        "core.Advertisement": "fas fa-ad",
        "core.Statistic": "fas fa-chart-line",
        "core.News": "fas fa-newspaper",
        "core.NewsCategory": "fas fa-tags",
        "core.Course": "fas fa-play-circle",
        "core.CourseCategory": "fas fa-layer-group",
        "core.Lesson": "fas fa-video",
        "core.CourseEnrollment": "fas fa-user-graduate",
        "core.Notification": "fas fa-bell",
        "core.SiteSettings": "fas fa-cog",
        "ai_assistant": "fas fa-robot",
        "ai_assistant.ChatSession": "fas fa-comments",
        "ai_assistant.ChatMessage": "fas fa-comment",
    },
    
    # Default ikonka
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related modal
    "related_modal_active": True,
    
    # Custom CSS/JS
    "custom_css": None,
    "custom_js": None,
    
    # UI Tweaks
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "accounts.User": "collapsible",
        "core.Test": "horizontal_tabs",
        "core.MockExam": "horizontal_tabs",
    },
}

# Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-primary",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-indigo",
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
