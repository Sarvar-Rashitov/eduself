"""
API views for notifications
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from .models import Notification
import json


@login_required
@require_http_methods(["GET"])
def get_unread_notifications(request):
    """O'qilmagan notification'larni olish"""
    try:
        # Oxirgi 5 daqiqadagi yangi notification'lar
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        
        # Shaxsiy notification'lar
        personal_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False,
            created_at__gte=five_minutes_ago
        )
        
        # Global notification'lar (o'qilmagan)
        from .models import NotificationRead
        read_global_ids = NotificationRead.objects.filter(
            user=request.user
        ).values_list('notification_id', flat=True)
        
        global_notifications = Notification.objects.filter(
            is_global=True,
            created_at__gte=five_minutes_ago
        ).exclude(id__in=read_global_ids)
        
        # Birlashtirib, eng yangisidan boshlab
        all_notifications = (personal_notifications | global_notifications).distinct().order_by('-created_at')[:5]
        
        # JSON formatga o'tkazish
        notifications_data = []
        for notif in all_notifications:
            notifications_data.append({
                'id': notif.id,
                'title': notif.title,
                'message': notif.message,
                'link': notif.link or '/',
                'type': notif.notification_type,
                'icon': notif.icon,
                'created_at': notif.created_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'notifications': notifications_data,
            'count': len(notifications_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_notification_permission(request):
    """Foydalanuvchi notification permission'ini saqlash"""
    try:
        data = json.loads(request.body)
        granted = data.get('granted', False)
        
        # User profile'da saqlash (kelajakda)
        # request.user.notification_permission = granted
        # request.user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Permission saqlandi'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Notification'ni o'qilgan deb belgilash"""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        if notification.is_global:
            # Global notification uchun NotificationRead yaratish
            from .models import NotificationRead
            NotificationRead.objects.get_or_create(
                notification=notification,
                user=request.user
            )
        else:
            # Shaxsiy notification uchun is_read = True
            if notification.user == request.user:
                notification.is_read = True
                notification.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Notification o\'qilgan deb belgilandi'
        })
        
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Notification topilmadi'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
