from django.conf import settings as django_settings
from django.db import models
from .models import SiteSettings, Notification, NotificationRead

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
        # Barcha bildirishnomalarni olish
        # Global bildirishnomalar faqat foydalanuvchi yaratilgandan KEYIN yaratilganlarini ko'rsatish
        all_notifications = Notification.objects.filter(
            models.Q(user=request.user) | 
            models.Q(is_global=True, created_at__gte=request.user.created_at)
        ).select_related('user').order_by('-created_at')
        
        # Har bir bildirishnoma uchun o'qilganligini tekshirish
        notifications_with_read_status = []
        unread_count = 0
        
        for notification in all_notifications:
            is_read = notification.is_read_by_user(request.user)
            # Template da ishlatish uchun is_read attributini qo'shish
            notification.is_read = is_read
            notifications_with_read_status.append(notification)
            
            if not is_read:
                unread_count += 1
    else:
        notifications_with_read_status = []
        unread_count = 0
    
    return {
        'notifications': notifications_with_read_status,
        'unread_notifications_count': unread_count
    }
