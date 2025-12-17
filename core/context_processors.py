from .models import SiteSettings, Notification
from django.conf import settings as django_settings

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    # SEO uchun asosiy ma'lumotlar
    seo_data = {
        'site_name': 'EduSelf',
        'site_url': django_settings.SITE_URL,
        'site_description': 'O\'zbekiston uchun zamonaviy onlayn ta\'lim platformasi',
        'site_keywords': 'eduself, onlayn ta\'lim, test, sertifikat, mock imtihon, o\'zbekiston',
    }
    
    return {
        'site_settings': settings,
        'seo_data': seo_data
    }


def notifications(request):
    if request.user.is_authenticated:
        # Foydalanuvchiga tegishli o'qilmagan bildirishnomalar
        user_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        
        # Global o'qilmagan bildirishnomalar
        global_notifications = Notification.objects.filter(
            is_global=True,
            is_read=False
        )
        
        # Barcha o'qilmagan bildirishnomalar
        all_notifications = (user_notifications | global_notifications).distinct().order_by('-created_at')[:10]
        unread_count = all_notifications.count()
    else:
        all_notifications = []
        unread_count = 0
    
    return {
        'notifications': all_notifications,
        'unread_notifications_count': unread_count
    }
