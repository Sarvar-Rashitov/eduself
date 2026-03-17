"""Telegram Bot Webhook Handler - Soddalashtirilgan"""
import os
import json
import logging
import asyncio
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from telegram import Update, Bot
from telegram.ext import Application

logger = logging.getLogger(__name__)

# Global bot instance
_bot = None
_application = None


def get_bot():
    """Bot instance olish"""
    global _bot
    if _bot is None:
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        if not BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN topilmadi!")
        _bot = Bot(token=BOT_TOKEN)
    return _bot


def get_application():
    """Application instance olish"""
    global _application
    if _application is None:
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        if not BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN topilmadi!")
        
        _application = Application.builder().token(BOT_TOKEN).build()
        register_all_handlers(_application)
        logger.info("Bot application yaratildi")
    
    return _application


def register_all_handlers(app):
    """Barcha handlerlarni ro'yxatdan o'tkazish"""
    try:
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
        
        logger.info("Barcha handlerlar ro'yxatdan o'tkazildi")
    except Exception as e:
        logger.error(f"Handler ro'yxatdan o'tkazishda xatolik: {e}")
        raise


@csrf_exempt
@require_POST
def webhook_handler(request):
    """Telegram webhook endpoint - soddalashtirilgan"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        logger.info(f"Webhook qabul qilindi: {data.get('update_id', 'unknown')}")
        
        # Application olish
        app = get_application()
        
        # Update yaratish
        update = Update.de_json(data, app.bot)
        
        # Async funksiyani sync rejimda ishga tushirish
        import asyncio
        
        async def process_update():
            try:
                # Application initialize qilish
                if not app.running:
                    await app.initialize()
                    await app.start()
                
                # Update ni qayta ishlash
                await app.process_update(update)
                
            except Exception as e:
                logger.error(f"Update qayta ishlashda xatolik: {e}")
                raise
        
        # Event loop yaratish va ishga tushirish
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_running():
            # Agar loop allaqachon ishlayotgan bo'lsa, task yaratish
            asyncio.create_task(process_update())
        else:
            # Loop ishlamayotgan bo'lsa, to'g'ridan-to'g'ri ishga tushirish
            loop.run_until_complete(process_update())
        
        return HttpResponse('OK')
        
    except Exception as e:
        logger.error(f"Webhook xatoligi: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def set_webhook_view(request):
    """Webhook ni o'rnatish - soddalashtirilgan"""
    try:
        SITE_URL = os.getenv('SITE_URL', '').rstrip('/')
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not SITE_URL or not BOT_TOKEN:
            return JsonResponse({'error': 'SITE_URL yoki BOT_TOKEN topilmadi'}, status=400)
        
        webhook_url = f"{SITE_URL}/telegram/webhook/"
        
        # Bot yaratish
        bot = get_bot()
        
        # Sync rejimda webhook o'rnatish
        import asyncio
        
        async def set_webhook():
            await bot.set_webhook(url=webhook_url)
            return await bot.get_webhook_info()
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        info = loop.run_until_complete(set_webhook())
        
        return JsonResponse({
            'success': True,
            'webhook_url': info.url,
            'pending_update_count': info.pending_update_count,
            'message': f'Webhook muvaffaqiyatli o\'rnatildi: {webhook_url}'
        })
        
    except Exception as e:
        logger.error(f"Webhook o'rnatishda xatolik: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def webhook_info_view(request):
    """Webhook ma'lumotlarini olish"""
    try:
        bot = get_bot()
        
        import asyncio
        
        async def get_info():
            return await bot.get_webhook_info()
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        info = loop.run_until_complete(get_info())
        
        return JsonResponse({
            'webhook_url': info.url,
            'has_custom_certificate': info.has_custom_certificate,
            'pending_update_count': info.pending_update_count,
            'last_error_date': info.last_error_date.isoformat() if info.last_error_date else None,
            'last_error_message': info.last_error_message,
            'max_connections': info.max_connections,
            'allowed_updates': info.allowed_updates
        })
        
    except Exception as e:
        logger.error(f"Webhook info olishda xatolik: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def delete_webhook_view(request):
    """Webhook ni o'chirish"""
    try:
        bot = get_bot()
        
        import asyncio
        
        async def delete_webhook():
            await bot.delete_webhook()
            return True
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(delete_webhook())
        
        return JsonResponse({'success': True, 'message': 'Webhook o\'chirildi'})
        
    except Exception as e:
        logger.error(f"Webhook o'chirishda xatolik: {e}")
        return JsonResponse({'error': str(e)}, status=500)
