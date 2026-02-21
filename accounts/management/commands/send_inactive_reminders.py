"""
Faol bo'lmagan foydalanuvchilarga eslatma email yuborish
Usage: python manage.py send_inactive_reminders
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
from accounts.models import User


class Command(BaseCommand):
    help = '3 kun faol bo\'lmagan foydalanuvchilarga eslatma email yuboradi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Necha kun faol bo\'lmagan foydalanuvchilarga yuborish (default: 3)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Faqat ko\'rsatish, email yubormaslik'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 70}'))
        self.stdout.write(self.style.SUCCESS(f'FAOL BO\'LMAGAN FOYDALANUVCHILARGA ESLATMA'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 70}\n'))
        
        # N kun oldingi vaqt
        inactive_date = timezone.now() - timedelta(days=days)
        
        self.stdout.write(f'📅 Faol bo\'lmaganlik muddati: {days} kun')
        self.stdout.write(f'📅 Oxirgi faollik: {inactive_date.strftime("%d.%m.%Y %H:%M")}\n')
        
        # Faol bo'lmagan foydalanuvchilarni topish
        inactive_users = User.objects.filter(
            is_active=True,
            email__isnull=False,
            email_verified=True,
            last_login__lt=inactive_date
        ).exclude(email='')
        
        total_users = inactive_users.count()
        self.stdout.write(f'👥 Jami faol bo\'lmagan foydalanuvchilar: {total_users}\n')
        
        if total_users == 0:
            self.stdout.write(self.style.WARNING('❌ Faol bo\'lmagan foydalanuvchilar topilmadi.'))
            return
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN - Email yuborilmaydi\n'))
        
        sent_count = 0
        failed_count = 0
        
        for user in inactive_users:
            try:
                # Foydalanuvchi statistikasi
                total_tests = user.get_total_tests_taken()
                passed_tests = user.get_passed_tests()
                total_points = user.total_points
                progress = user.get_progress_percentage()
                
                # Oxirgi faollik
                if user.last_login:
                    days_inactive = (timezone.now() - user.last_login).days
                else:
                    days_inactive = days
                
                self.stdout.write(f'📧 {user.email} ({user.first_name}) - {days_inactive} kun faol emas')
                
                if not dry_run:
                    # HTML email yaratish
                    html_content = render_to_string('emails/inactive_reminder.html', {
                        'user_name': user.first_name,
                        'days_inactive': days_inactive,
                        'site_url': settings.SITE_URL,
                        'total_tests': total_tests,
                        'passed_tests': passed_tests,
                        'total_points': total_points,
                        'progress': progress,
                    })
                    
                    # Text fallback
                    text_content = f'''Assalomu alaykum, {user.first_name}!

Sizni sog'indik! Siz EduSelf platformasida {days_inactive} kun faol bo'lmadingiz.

Sizning natijalaringiz:
- Jami testlar: {total_tests}
- O'tgan testlar: {passed_tests}
- Umumiy ball: {total_points}
- Progress: {progress}%

Qaytib kelib, o'qishni davom ettiring: {settings.SITE_URL}

Hurmat bilan,
EduSelf jamoasi'''
                    
                    # Email yuborish
                    email = EmailMultiAlternatives(
                        subject='EduSelf - Sizni sog\'indik!',
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email]
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send(fail_silently=False)
                    
                    # Telegram notification yuborish
                    if user.telegram_chat_id:
                        try:
                            from telegram_bot.notification_sender import send_telegram_notification
                            send_telegram_notification(
                                user_id=user.id,
                                title="📚 Sizni sog'indik!",
                                message=f"Assalomu alaykum, {user.first_name}!\n\n"
                                        f"Siz {days_inactive} kun faol bo'lmadingiz.\n\n"
                                        f"📊 Natijalaringiz:\n"
                                        f"• Jami testlar: {total_tests}\n"
                                        f"• O'tgan testlar: {passed_tests}\n"
                                        f"• Umumiy ball: {total_points}\n"
                                        f"• Progress: {progress}%\n\n"
                                        f"Qaytib kelib, o'qishni davom ettiring!",
                                link=settings.SITE_URL
                            )
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'   ⚠️  Telegram notification xatolik: {e}'))
                    
                    sent_count += 1
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Yuborildi'))
                else:
                    self.stdout.write(self.style.WARNING(f'   🔍 Dry run - yuborilmadi'))
                    sent_count += 1
                
            except Exception as e:
                failed_count += 1
                self.stdout.write(self.style.ERROR(f'   ❌ Xatolik: {str(e)}'))
        
        # Natija
        self.stdout.write(f'\n{"=" * 70}')
        self.stdout.write(self.style.SUCCESS(f'✅ YAKUNLANDI'))
        self.stdout.write(f'{"=" * 70}\n')
        self.stdout.write(f'📊 Jami: {total_users}')
        self.stdout.write(self.style.SUCCESS(f'✅ Yuborildi: {sent_count}'))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f'❌ Xatolik: {failed_count}'))
        self.stdout.write('')
