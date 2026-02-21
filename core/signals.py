"""
Core app signals - Notification yaratilganda email va Telegram yuborish
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db import models
from .models import Notification
import logging
import threading

logger = logging.getLogger(__name__)


def send_notifications_async(notification):
    """
    Email va Telegram yuborishni background thread'da bajarish
    Bu admin panel darhol javob qaytarishi uchun
    """
    def _send_notifications():
        email_sent = 0
        telegram_sent = 0
        
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
                    email.send(fail_silently=False)  # Xatoliklarni ko'rish uchun
                    
                    logger.info(f"✅ Email yuborildi: {user.email}")
                    return True
                    
                except Exception as e:
                    logger.error(f"❌ Email yuborishda xatolik ({user.email}): {e}")
                    return False
            
            # Telegram yuborish funksiyasi
            def send_telegram_to_user(user):
                """Bitta foydalanuvchiga Telegram yuborish"""
                if not user.telegram_chat_id:
                    return False
                
                try:
                    from telegram_bot.notification_sender import send_telegram_notification
                    
                    result = send_telegram_notification(
                        user_id=user.id,
                        title=notification.title,
                        message=notification.message,
                        link=notification.link,
                        is_global=False
                    )
                    
                    if result:
                        logger.info(f"✅ Telegram yuborildi: {user.username}")
                        return True
                    return False
                    
                except Exception as e:
                    logger.error(f"❌ Telegram yuborishda xatolik ({user.username}): {e}")
                    return False
            
            # Global yoki shaxsiy notification
            if notification.is_global:
                # Barcha foydalanuvchilarga yuborish
                from accounts.models import User
                
                # Email uchun foydalanuvchilar (BARCHA email tasdiqlangan)
                email_users = User.objects.filter(
                    is_active=True,
                    email__isnull=False,
                    email_verified=True
                ).exclude(email='')
                
                # Telegram uchun foydalanuvchilar (Telegram ID bor)
                telegram_users = User.objects.filter(
                    is_active=True,
                    telegram_chat_id__isnull=False,
                    telegram_id__isnull=False
                ).exclude(telegram_chat_id='')
                
                logger.info(f"📧 Global notification: {email_users.count()} email, {telegram_users.count()} telegram")
                
                # Email yuborish (BARCHA email tasdiqlanganlarga)
                for user in email_users:
                    if send_email_to_user(user):
                        email_sent += 1
                
                # Telegram yuborish (Telegram ID bor foydalanuvchilarga)
                for user in telegram_users:
                    if send_telegram_to_user(user):
                        telegram_sent += 1
                
                logger.info(f"✅ Global yuborish tugadi: {email_sent} email, {telegram_sent} telegram")
                
            else:
                # Shaxsiy notification - faqat bitta foydalanuvchiga
                if notification.user:
                    # Email yuborish (agar email tasdiqlangan bo'lsa)
                    if send_email_to_user(notification.user):
                        email_sent = 1
                    
                    # Telegram yuborish (agar Telegram ID bor bo'lsa)
                    if notification.user.telegram_id:
                        if send_telegram_to_user(notification.user):
                            telegram_sent = 1
                    
                    logger.info(f"✅ Shaxsiy notification: email={email_sent}, telegram={telegram_sent}")
        
        except Exception as e:
            logger.error(f"❌ Async notification yuborishda xatolik: {e}")
        
        logger.info(f"📊 Jami yuborildi: {email_sent} email, {telegram_sent} telegram")
    
    # Background thread'da ishga tushirish
    thread = threading.Thread(target=_send_notifications)
    thread.daemon = True
    thread.start()
    logger.info("📤 Notification yuborish background thread'da boshlandi")


@receiver(post_save, sender=Notification)
def send_notification_email_and_telegram(sender, instance, created, **kwargs):
    """
    Yangi notification yaratilganda email va Telegram yuborish (async)
    """
    if not created:
        return  # Faqat yangi notification uchun
    
    # Email va Telegram yuborishni async qilish (admin panel timeout bo'lmasligi uchun)
    send_notifications_async(instance)
