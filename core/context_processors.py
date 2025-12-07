from .models import SiteSettings, Notification

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    return {'site_settings': settings}


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
