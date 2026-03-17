"""EduSelf Telegram Bot - Asosiy fayl"""
import os
import sys
import logging

# Django sozlamalari
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')

import django
django.setup()

from telegram import Update
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

# Bot token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN topilmadi!")
    sys.exit(1)


def main():
    """Botni ishga tushirish"""
    logger.info("EduSelf Bot ishga tushmoqda...")

    # Application yaratish
    app = Application.builder().token(BOT_TOKEN).build()

    try:
        # Handlerlarni import qilish va ro'yxatdan o'tkazish
        from telegram_bot.handlers.start import register_handlers as start_handlers
        from telegram_bot.handlers.subjects import register_handlers as subject_handlers
        from telegram_bot.handlers.tests import register_handlers as test_handlers
        from telegram_bot.handlers.certificates import register_handlers as cert_handlers
        from telegram_bot.handlers.mock_exams import register_handlers as mock_handlers
        from telegram_bot.handlers.institutions import register_handlers as inst_handlers
        from telegram_bot.handlers.profile import register_handlers as profile_handlers
        from telegram_bot.handlers.subscription import register_handlers as subscription_handlers
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
        subscription_handlers(app)
        ai_handlers(app)
        common_handlers(app)
        
        # Test menyu tugmalari uchun umumiy handler - faqat mavjud handlerlar
        from telegram.ext import MessageHandler, filters

        logger.info("Barcha handlerlar ro'yxatdan o'tkazildi")
    except Exception as e:
        logger.error(f"Handler import xatoligi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    logger.info("Bot polling rejimida ishga tushdi...")

    # Botni ishga tushirish
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
