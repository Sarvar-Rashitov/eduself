"""Telegram Bot Webhook Handler"""
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

# Global application instance
_application = None
_initialized = False
_lock = asyncio.Lock() if hasattr(asyncio, 'Lock') else None


def get_or_create_event_loop():
    """Event loop olish yoki yaratish"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


async def get_application():
    """Bot application olish yoki yaratish"""
    global _application, _initialized
    
    if _application is None:
        from dotenv import load_dotenv
        load_dotenv()
        
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        if not BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN topilmadi!")
        
        # Application yaratish
        _application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlerlarni ro'yxatdan o'tkazish
        register_all_handlers(_application)
        
        logger.info("Bot application yaratildi")
    
    if not _initialized:
        await _application.initialize()
        _initialized = True
        logger.info("Bot application initialized")
    
    return _application


def register_all_handlers(app):
    """Barcha handlerlarni ro'yxatdan o'tkazish"""
    from telegram.ext import MessageHandler, filters
    
    from telegram_bot.handlers.start import register_handlers as start_handlers
    from telegram_bot.handlers.subjects import register_handlers as subject_handlers
    from telegram_bot.handlers.tests import register_handlers as test_handlers
    from telegram_bot.handlers.certificates import register_handlers as cert_handlers
    from telegram_bot.handlers.mock_exams import register_handlers as mock_handlers
    from telegram_bot.handlers.institutions import register_handlers as inst_handlers
    from telegram_bot.handlers.profile import register_handlers as profile_handlers
    from telegram_bot.handlers.ai_chat import register_handlers as ai_handlers
    from telegram_bot.handlers.common import register_handlers as common_handlers
    
    start_handlers(app)
    subject_handlers(app)
    test_handlers(app)
    cert_handlers(app)
    mock_handlers(app)
    inst_handlers(app)
    profile_handlers(app)
    ai_handlers(app)
    common_handlers(app)
    
    # Test menyu handlerlari
    from telegram_bot.handlers.tests import handle_test_menu, handle_test_answer
    from telegram_bot.handlers.certificates import handle_cert_menu, handle_cert_answer
    from telegram_bot.handlers.mock_exams import handle_mock_menu, handle_mock_answer
    
    async def unified_test_menu_handler(update, context):
        session = context.user_data.get('test_session')
        if not session:
            return
        test_type = session.get('test_type')
        if test_type == 'regular':
            await handle_test_menu(update, context)
        elif test_type == 'certificate':
            await handle_cert_menu(update, context)
        elif test_type == 'mock':
            await handle_mock_menu(update, context)
    
    async def unified_answer_handler(update, context):
        session = context.user_data.get('test_session')
        if not session:
            return
        test_type = session.get('test_type')
        if test_type == 'regular':
            await handle_test_answer(update, context)
        elif test_type == 'certificate':
            await handle_cert_answer(update, context)
        elif test_type == 'mock':
            await handle_mock_answer(update, context)
    
    app.add_handler(MessageHandler(
        filters.Regex("^(⏭ Keyingisi|⏩ O'tkazib yuborish|🏁 Yakunlash)$"),
        unified_test_menu_handler
    ))
    app.add_handler(MessageHandler(filters.Regex("^[AaBbCcDd]$"), unified_answer_handler))
    
    logger.info("Barcha handlerlar ro'yxatdan o'tkazildi")


@csrf_exempt
@require_POST
def webhook_handler(request):
    """Telegram webhook endpoint"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        
        loop = get_or_create_event_loop()
        
        async def process():
            app = await get_application()
            update = Update.de_json(data, app.bot)
            await app.process_update(update)
        
        loop.run_until_complete(process())
        
        return HttpResponse('OK')
    except Exception as e:
        logger.error(f"Webhook xatoligi: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def set_webhook_view(request):
    """Webhook ni o'rnatish"""
    SITE_URL = os.getenv('SITE_URL', '').rstrip('/')
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not SITE_URL or not BOT_TOKEN:
        return JsonResponse({'error': 'SITE_URL yoki BOT_TOKEN topilmadi'}, status=400)
    
    webhook_url = f"{SITE_URL}/telegram/webhook/"
    
    loop = get_or_create_event_loop()
    
    async def set_webhook():
        app = await get_application()
        await app.bot.set_webhook(url=webhook_url)
        return await app.bot.get_webhook_info()
    
    try:
        info = loop.run_until_complete(set_webhook())
        return JsonResponse({
            'success': True,
            'webhook_url': info.url,
            'pending_update_count': info.pending_update_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def delete_webhook_view(request):
    """Webhook ni o'chirish"""
    loop = get_or_create_event_loop()
    
    async def delete_webhook():
        app = await get_application()
        await app.bot.delete_webhook()
        return True
    
    try:
        loop.run_until_complete(delete_webhook())
        return JsonResponse({'success': True, 'message': 'Webhook o\'chirildi'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
