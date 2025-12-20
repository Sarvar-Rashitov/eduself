from django.conf import settings as django_settings
from django.db import models
from .models import SiteSettings, Notification

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    return {'site_settings': settings}


def auth_settings(request):
    """Google va Telegram auth sozlamalari"""
    return {
        'google_client_id': getattr(django_settings, 'GOOGLE_CLIENT_ID', ''),
        'telegram_bot_username': getattr(django_settings, 'TELEGRAM_BOT_USERNAME', ''),
    }


def notifications(request):
    if request.user.is_authenticated:
        # Bitta so'rov bilan barcha bildirishnomalarni olish
        all_notifications = Notification.objects.filter(
            is_read=False
        ).filter(
            models.Q(user=request.user) | models.Q(is_global=True)
        ).select_related('user').order_by('-created_at')[:10]
        
        unread_count = all_notifications.count()
    else:
        all_notifications = []
        unread_count = 0
    
    return {
        'notifications': all_notifications,
        'unread_notifications_count': unread_count
    }
