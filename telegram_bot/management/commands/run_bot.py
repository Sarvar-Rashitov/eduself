"""Telegram bot ishga tushirish command"""
import os
import sys
import logging
from django.core.management.base import BaseCommand
from telegram.ext import Application
from dotenv import load_dotenv

# .env yuklash
load_dotenv()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Telegram bot ishga tushirish (polling rejimida)'

    def handle(self, *args, **options):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            self.stdout.write(self.style.ERROR('TELEGRAM_BOT_TOKEN topilmadi!'))
            return

        self.stdout.write("🤖 EduSelf Telegram Bot")
        self.stdout.write("=" * 50)
        self.stdout.write("Bot ishga tushmoqda...")
        self.stdout.write("To'xtatish uchun Ctrl+C bosing")

        # Application yaratish
        app = Application.builder().token(bot_token).build()

        try:
            # Handlerlarni import qilish va ro'yxatdan o'tkazish
            from telegram_bot.handlers.start import register_handlers as start_handlers
            from telegram_bot.handlers.subjects import register_handlers as subject_handlers
            from telegram_bot.handlers.tests import register_handlers as test_handlers
            from telegram_bot.handlers.certificates import register_handlers as cert_handlers
            from telegram_bot.handlers.mock_exams import register_handlers as mock_handlers
            from telegram_bot.handlers.institutions import register_handlers as inst_handlers
            from telegram_bot.handlers.profile import register_handlers as profile_handlers
            from telegram_bot.handlers.ai_chat import register_handlers as ai_handlers
            from telegram_bot.handlers.common import register_handlers as common_handlers

            # Handlerlarni qo'shish
            start_handlers(app)
            subject_handlers(app)
            test_handlers(app)
            cert_handlers(app)
            mock_handlers(app)
            inst_handlers(app)
            profile_handlers(app)
            ai_handlers(app)
            common_handlers(app)

            logger.info("Barcha handlerlar ro'yxatdan o'tkazildi")
        except Exception as e:
            logger.error(f"Handler import xatoligi: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        logger.info("Bot polling rejimida ishga tushdi...")

        try:
            # Botni ishga tushirish
            app.run_polling(allowed_updates=['message', 'callback_query'])
        except KeyboardInterrupt:
            self.stdout.write("\n✅ Bot to'xtatildi.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Xatolik: {e}"))