"""Django management command - Telegram botni ishga tushirish"""
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'EduSelf Telegram botni ishga tushirish'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('EduSelf Telegram Bot ishga tushmoqda...'))
        
        try:
            from telegram_bot.bot import main
            main()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Bot to\'xtatildi.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Xatolik: {e}'))
            raise
