"""
Kunlik eslatma yuborish - soat 07:00 va 14:00 da
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.models import User
from core.models import Notification
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Kunlik eslatma yuborish - bugun kirmagan foydalanuvchilarga'

    def add_arguments(self, parser):
        parser.add_argument(
            '--time',
            type=str,
            default='morning',
            help='Qaysi vaqt: morning (07:00) yoki afternoon (14:00)'
        )

    def handle(self, *args, **options):
        time_slot = options['time']
        
        self.stdout.write("=" * 80)
        self.stdout.write(f"KUNLIK ESLATMA - {time_slot.upper()}")
        self.stdout.write("=" * 80)
        
        # Bugungi kun boshlanishi
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Bugun kirmagan foydalanuvchilarni topish
        inactive_today = User.objects.filter(
            is_active=True,
            email__isnull=False,
            email_verified=True
        ).exclude(
            last_login__gte=today_start
        ).exclude(email='')
        
        self.stdout.write(f"\n📊 Bugun kirmagan foydalanuvchilar: {inactive_today.count()}")
        
        if time_slot == 'morning':
            # Ertalabki eslatma (07:00)
            self.send_morning_reminders(inactive_today)
        elif time_slot == 'afternoon':
            # Tushdan keyingi eslatma (14:00)
            # Faqat ertalab eslatma yuborilgan va hali ham kirmagan foydalanuvchilarga
            self.send_afternoon_reminders(inactive_today)
        else:
            self.stdout.write(self.style.ERROR("❌ Noto'g'ri vaqt: morning yoki afternoon"))
            return
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✅ Kunlik eslatma yuborish tugadi!"))
        self.stdout.write("=" * 80)

    def send_morning_reminders(self, users):
        """Ertalabki eslatma (07:00)"""
        self.stdout.write("\n🌅 ERTALABKI ESLATMA (07:00)")
        self.stdout.write("-" * 80)
        
        email_sent = 0
        telegram_sent = 0
        notification_created = 0
        
        for user in users:
            try:
                # Email yuborish
                if user.email and user.email_verified:
                    try:
                        html_content = render_to_string('emails/daily_reminder.html', {
                            'user_name': user.first_name,
                            'time': 'ertalab',
                            'site_url': settings.SITE_URL,
                        })
                        
                        text_content = f'''Assalomu alaykum, {user.first_name}!

🌅 Xayrli tong! Bugun EduSelf platformasida o'qishni boshlaganingiz yo'qmi?

Har kuni 15-20 daqiqa o'qish sizning bilimingizni oshiradi va maqsadlaringizga yaqinlashtiradi.

📚 Bugun nima o'rganamiz?

{settings.SITE_URL}

Hurmat bilan,
EduSelf jamoasi'''
                        
                        email = EmailMultiAlternatives(
                            subject='EduSelf - Bugun o\'qishni boshlaymizmi? 📚',
                            body=text_content,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[user.email]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send(fail_silently=False)
                        email_sent += 1
                        logger.info(f"✅ Morning email: {user.email}")
                    except Exception as e:
                        logger.error(f"❌ Email xatolik ({user.email}): {e}")
                
                # Telegram yuborish
                if user.telegram_chat_id and user.telegram_id:
                    try:
                        from telegram_bot.notification_sender import send_telegram_notification
                        
                        result = send_telegram_notification(
                            user_id=user.id,
                            title="🌅 Xayrli tong!",
                            message=f"Bugun EduSelf platformasida o'qishni boshlaganingiz yo'qmi?\n\nHar kuni 15-20 daqiqa o'qish bilimingizni oshiradi! 📚",
                            link=settings.SITE_URL,
                            is_global=False
                        )
                        
                        if result:
                            telegram_sent += 1
                            logger.info(f"✅ Morning telegram: {user.username}")
                    except Exception as e:
                        logger.error(f"❌ Telegram xatolik ({user.username}): {e}")
                
                # Platformada bildirishnoma yaratish
                try:
                    Notification.objects.create(
                        user=user,
                        title="🌅 Bugun o'qishni boshlaymizmi?",
                        message="Har kuni 15-20 daqiqa o'qish sizning bilimingizni oshiradi va maqsadlaringizga yaqinlashtiradi.",
                        notification_type='reminder',
                        icon='📚',
                        link='/'
                    )
                    notification_created += 1
                except Exception as e:
                    logger.error(f"❌ Notification xatolik ({user.username}): {e}")
                    
            except Exception as e:
                logger.error(f"❌ Umumiy xatolik ({user.username}): {e}")
        
        self.stdout.write(f"\n📊 Natijalar:")
        self.stdout.write(f"   📧 Email yuborildi: {email_sent}")
        self.stdout.write(f"   💬 Telegram yuborildi: {telegram_sent}")
        self.stdout.write(f"   🔔 Bildirishnoma yaratildi: {notification_created}")

    def send_afternoon_reminders(self, users):
        """Tushdan keyingi eslatma (14:00)"""
        self.stdout.write("\n☀️ TUSHDAN KEYINGI ESLATMA (14:00)")
        self.stdout.write("-" * 80)
        
        # Bugungi kun boshlanishi
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Bugun ertalab eslatma yuborilgan foydalanuvchilarni topish
        # (bugun yaratilgan reminder tipidagi bildirishnomalar bor foydalanuvchilar)
        morning_notified_users = Notification.objects.filter(
            notification_type='reminder',
            created_at__gte=today_start,
            user__isnull=False
        ).values_list('user_id', flat=True).distinct()
        
        # Faqat ertalab eslatma yuborilgan va hali ham kirmagan foydalanuvchilarga
        users_to_remind = users.filter(id__in=morning_notified_users)
        
        self.stdout.write(f"\n📊 Ertalab eslatma yuborilgan va hali kirmagan: {users_to_remind.count()}")
        
        email_sent = 0
        telegram_sent = 0
        notification_created = 0
        
        for user in users_to_remind:
            try:
                # Email yuborish
                if user.email and user.email_verified:
                    try:
                        html_content = render_to_string('emails/daily_reminder.html', {
                            'user_name': user.first_name,
                            'time': 'tushdan keyin',
                            'site_url': settings.SITE_URL,
                        })
                        
                        text_content = f'''Assalomu alaykum, {user.first_name}!

☀️ Bugun hali EduSelf platformasiga kirmaganingizni ko'rdik.

Faqat 10-15 daqiqa vaqt ajrating va bilimingizni oshiring!

📚 Keling, bugun biror narsa o'rganamiz?

{settings.SITE_URL}

Hurmat bilan,
EduSelf jamoasi'''
                        
                        email = EmailMultiAlternatives(
                            subject='EduSelf - Bugun hali o\'qimadingiz 📖',
                            body=text_content,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[user.email]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send(fail_silently=False)
                        email_sent += 1
                        logger.info(f"✅ Afternoon email: {user.email}")
                    except Exception as e:
                        logger.error(f"❌ Email xatolik ({user.email}): {e}")
                
                # Telegram yuborish
                if user.telegram_chat_id and user.telegram_id:
                    try:
                        from telegram_bot.notification_sender import send_telegram_notification
                        
                        result = send_telegram_notification(
                            user_id=user.id,
                            title="☀️ Bugun hali o'qimadingiz",
                            message=f"Faqat 10-15 daqiqa vaqt ajrating va bilimingizni oshiring!\n\nKeling, bugun biror narsa o'rganamiz? 📖",
                            link=settings.SITE_URL,
                            is_global=False
                        )
                        
                        if result:
                            telegram_sent += 1
                            logger.info(f"✅ Afternoon telegram: {user.username}")
                    except Exception as e:
                        logger.error(f"❌ Telegram xatolik ({user.username}): {e}")
                
                # Platformada bildirishnoma yaratish
                try:
                    Notification.objects.create(
                        user=user,
                        title="☀️ Bugun hali o'qimadingiz",
                        message="Faqat 10-15 daqiqa vaqt ajrating va bilimingizni oshiring! Keling, bugun biror narsa o'rganamiz?",
                        notification_type='reminder',
                        icon='📖',
                        link='/'
                    )
                    notification_created += 1
                except Exception as e:
                    logger.error(f"❌ Notification xatolik ({user.username}): {e}")
                    
            except Exception as e:
                logger.error(f"❌ Umumiy xatolik ({user.username}): {e}")
        
        self.stdout.write(f"\n📊 Natijalar:")
        self.stdout.write(f"   📧 Email yuborildi: {email_sent}")
        self.stdout.write(f"   💬 Telegram yuborildi: {telegram_sent}")
        self.stdout.write(f"   🔔 Bildirishnoma yaratildi: {notification_created}")
