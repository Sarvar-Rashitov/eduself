"""
Context processors for adding global variables to templates
"""
from django.conf import settings
from django.db import models
from .models import SiteSettings, Notification, NotificationRead


def site_settings(request):
    """
    Site settings'ni barcha template'larga qo'shish
    """
    try:
        site_settings_obj = SiteSettings.objects.first()
    except:
        site_settings_obj = None
    
    return {
        'site_settings': site_settings_obj,
    }


def notifications(request):
    """
    Foydalanuvchi notificationlarini barcha template'larga qo'shish
    """
    if request.user.is_authenticated:
        # Global notificationlar (o'qilmaganlar)
        global_notifications = Notification.objects.filter(
            is_global=True
        ).exclude(
            reads__user=request.user
        )
        
        # Shaxsiy notificationlar (o'qilmaganlar)
        personal_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        
        # Jami o'qilmagan notificationlar soni
        unread_count = global_notifications.count() + personal_notifications.count()
        
        # Oxirgi 10 ta notification (global + personal)
        recent_notifications = Notification.objects.filter(
            models.Q(is_global=True) | models.Q(user=request.user)
        ).order_by('-created_at')[:10]
        
        return {
            'unread_notifications_count': unread_count,
            'recent_notifications': recent_notifications,
        }
    
    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }


def auth_settings(request):
    """
    Authentication settings'ni barcha template'larga qo'shish
    """
    return {
        'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
    }


def language_context(request):
    """
    Har bir template'ga til ma'lumotlarini qo'shish
    """
    # Get current language from request
    current_lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Prepare languages list with names
    languages_list = []
    language_names = {
        'uz': "O'zbek",
        'en': 'English',
        'ru': 'Русский',
        'kk': 'Қазақша',
        'kaa': 'Qaraqalpaqsha',
        'tg': 'Тоҷикӣ',
        'ky': 'Кыргызча',
    }
    
    for lang_code, lang_name in settings.LANGUAGES:
        languages_list.append((lang_code, language_names.get(lang_code, lang_name)))
    
    # Detect page name from URL path
    page_name = 'default'
    path = request.path.strip('/')
    
    if not path or path == '':
        page_name = 'home'
    elif 'institution' in path:
        page_name = 'institutions'
    elif 'course' in path or 'lesson' in path:
        page_name = 'courses'
    elif 'subject' in path or 'topic' in path:
        page_name = 'subjects'
    elif 'mock-exam' in path:
        page_name = 'mock_exams'
    elif 'certificate' in path:
        page_name = 'certificates'
    elif 'profile' in path:
        page_name = 'profile'
    elif 'leaderboard' in path:
        page_name = 'leaderboard'
    elif 'news' in path:
        page_name = 'news'
    elif 'ai-assistant' in path:
        page_name = 'ai_assistant'
    elif 'oferta' in path or 'privacy' in path:
        page_name = 'oferta'
    
    return {
        'CURRENT_LANGUAGE': current_lang,
        'AVAILABLE_LANGUAGES': settings.LANGUAGES,
        'current_language': current_lang,
        'languages': languages_list,
        'PAGE_NAME': page_name,  # Sahifa nomi
    }
