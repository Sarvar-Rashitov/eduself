"""
Core app signals - Notification yaratilganda email yuborish
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Notification
import logging
import threading

logger = logging.getLogger(__name__)


def send_emails_async(notification):
    """
    Email yuborishni background thread'da bajarish
    Bu admin panel darhol javob qaytarishi uchun
    """
    def _send_emails():
        try:
            # Email yuborish funksiyasi
            def send_email_to_user(user):
                """Bitta foydalanuvchiga email yuborish"""
                if not user.email or not user.email_verified:
                    return False
                
                try:
                    # HTML email yaratish
                    html_content = render_to_string('emails/notification.html', {
                        'user_name': user.first_name,
                        'title': notification.title,
                        'message': notification.message,
                        'link': notification.link,
                        'notification_type': notification.get_notification_type_display(),
                        'icon': notification.icon,
                        'site_url': settings.SITE_URL,
                    })
                    
                    # Text fallback
                    text_content = f'''Assalomu alaykum, {user.first_name}!

{notification.get_notification_type_display()}: {notification.title}

{notification.message}

{f"Havola: {notification.link}" if notification.link else ""}

Hurmat bilan,
EduSelf jamoasi'''
                    
                    # Email yuborish
                    email = EmailMultiAlternatives(
                        subject=f'EduSelf - {notification.title}',
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email]
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send(fail_silently=True)
                    
                    logger.info(f"Notification email yuborildi: {user.email}")
                    return True
                    
                except Exception as e:
                    logger.error(f"Notification email yuborishda xatolik ({user.email}): {e}")
                    return False
            
            # Global yoki shaxsiy notification
            if notification.is_global:
                # Barcha foydalanuvchilarga yuborish (email tasdiqlangan)
                from accounts.models import User
                users = User.objects.filter(
                    is_active=True,
                    email__isnull=False,
                    email_verified=True
                ).exclude(email='')
                
                logger.info(f"Global notification: {users.count()} ta foydalanuvchiga yuborilmoqda")
                
                sent_count = 0
                for user in users:
                    if send_email_to_user(user):
                        sent_count += 1
                
                logger.info(f"Global notification email yuborish tugadi: {sent_count}/{users.count()}")
                
            else:
                # Shaxsiy notification - faqat bitta foydalanuvchiga
                if notification.user:
                    send_email_to_user(notification.user)
                    logger.info(f"Shaxsiy notification email yuborildi: {notification.user.email}")
        
        except Exception as e:
            logger.error(f"Async email yuborishda xatolik: {e}")
    
    # Background thread'da ishga tushirish
    thread = threading.Thread(target=_send_emails)
    thread.daemon = True
    thread.start()
    logger.info("Email yuborish background thread'da boshlandi")


@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    """
    Yangi notification yaratilganda email yuborish (async)
    """
    if not created:
        return  # Faqat yangi notification uchun
    
    # Email yuborishni async qilish (admin panel timeout bo'lmasligi uchun)
    send_emails_async(instance)
