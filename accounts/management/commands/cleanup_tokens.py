"""Eskirgan tokenlarni tozalash uchun management command"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import TelegramLoginToken, PasswordResetToken, EmailVerificationToken


class Command(BaseCommand):
    help = 'Eskirgan tokenlarni tozalash'

    def handle(self, *args, **options):
        # Eskirgan Telegram login tokenlarni o'chirish
        telegram_deleted = TelegramLoginToken.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        
        # Eskirgan parol tiklash tokenlarni o'chirish
        password_deleted = PasswordResetToken.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        
        # Eskirgan email tasdiqlash tokenlarni o'chirish
        email_deleted = EmailVerificationToken.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Tozalandi: {telegram_deleted} Telegram token, '
                f'{password_deleted} parol token, '
                f'{email_deleted} email token'
            )
        )