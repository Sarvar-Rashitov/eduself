from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import TopicResult, CertificateResult, MockExamResult, Notification
import logging

logger = logging.getLogger(__name__)


def calculate_user_total_points(user):
    """
    Foydalanuvchining barcha test turlaridan umumiy ballini hisoblash
    """
    # Mavzu testlaridan balllar (earned_points maydoni)
    topic_points = TopicResult.objects.filter(user=user).aggregate(
        total=Sum('earned_points')
    )['total'] or 0
    
    # Sertifikat testlaridan balllar (earned_points maydoni)
    cert_points = CertificateResult.objects.filter(user=user).aggregate(
        total=Sum('earned_points')
    )['total'] or 0
    
    # Mock exam testlaridan balllar (earned_points maydoni)
    mock_points = MockExamResult.objects.filter(user=user).aggregate(
        total=Sum('earned_points')
    )['total'] or 0
    
    return topic_points + cert_points + mock_points


@receiver(post_save, sender=TopicResult)
def update_user_total_points_on_topic_result(sender, instance, created, **kwargs):
    """
    TopicResult yaratilganda foydalanuvchining total_points ni yangilash
    """
    if created:  # Faqat yangi natija yaratilganda
        user = instance.user
        total_points = calculate_user_total_points(user)
        user.total_points = total_points
        user.save(update_fields=['total_points'])


@receiver(post_save, sender=CertificateResult)
def update_user_total_points_on_cert_result(sender, instance, created, **kwargs):
    """
    CertificateResult yaratilganda foydalanuvchining total_points ni yangilash
    """
    if created:  # Faqat yangi natija yaratilganda
        user = instance.user
        total_points = calculate_user_total_points(user)
        user.total_points = total_points
        user.save(update_fields=['total_points'])


@receiver(post_save, sender=MockExamResult)
def update_user_total_points_on_mock_result(sender, instance, created, **kwargs):
    """
    MockExamResult yaratilganda foydalanuvchining total_points ni yangilash
    """
    if created:  # Faqat yangi natija yaratilganda
        user = instance.user
        total_points = calculate_user_total_points(user)
        user.total_points = total_points
        user.save(update_fields=['total_points'])


@receiver(post_save, sender=Notification)
def send_telegram_notification_on_create(sender, instance, created, **kwargs):
    """
    Yangi bildirishnoma yaratilganda Telegram bot orqali yuborish
    """
    if created:  # Faqat yangi bildirishnoma yaratilganda
        try:
            from telegram_bot.notification_sender import send_telegram_notification
            
            # Sayt URL ni olish
            from django.conf import settings
            site_url = getattr(settings, 'SITE_URL', 'https://eduself.uz')
            
            # Havola tayyorlash
            link = None
            if instance.link:
                if instance.link.startswith('http'):
                    link = instance.link
                else:
                    link = f"{site_url}{instance.link}"
            
            # Telegram orqali yuborish
            success = send_telegram_notification(
                user_id=instance.user.id if instance.user else None,
                title=instance.title,
                message=instance.message,
                link=link,
                is_global=instance.is_global
            )
            
            if success:
                logger.info(f"Telegram bildirishnoma yuborildi: {instance.title}")
            else:
                logger.warning(f"Telegram bildirishnoma yuborilmadi: {instance.title}")
                
        except Exception as e:
            logger.error(f"Telegram bildirishnoma yuborishda xatolik: {e}")