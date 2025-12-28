"""Telegram bot decoratorlari"""
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.utils import check_channel_subscription, get_user_or_none
from telegram_bot.keyboards import channel_subscription_keyboard


def require_subscription(action_name: str = "check_sub"):
    """Kanal obunasini tekshiruvchi decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            
            # Kanal obunasini tekshirish
            is_subscribed = await check_channel_subscription(context.bot, user_id)
            
            if not is_subscribed:
                # Callback yoki message ekanligini aniqlash
                if update.callback_query:
                    await update.callback_query.answer()
                    await update.callback_query.message.reply_text(
                        "📢 *Botdan foydalanish uchun kanalimizga obuna bo'ling!*\n\n"
                        "Kanalda foydali ma'lumotlar, yangiliklar va maxsus takliflar bor.\n\n"
                        "Obuna bo'lgandan so'ng \"✅ Obunani tekshirish\" tugmasini bosing.",
                        parse_mode='Markdown',
                        reply_markup=channel_subscription_keyboard(f"retry_{action_name}")
                    )
                    # Qaysi funksiyani qayta chaqirish kerakligini saqlash
                    context.user_data['pending_action'] = func.__name__
                    context.user_data['pending_data'] = update.callback_query.data if update.callback_query else None
                else:
                    await update.message.reply_text(
                        "📢 *Botdan foydalanish uchun kanalimizga obuna bo'ling!*\n\n"
                        "Kanalda foydali ma'lumotlar, yangiliklar va maxsus takliflar bor.\n\n"
                        "Obuna bo'lgandan so'ng \"✅ Obunani tekshirish\" tugmasini bosing.",
                        parse_mode='Markdown',
                        reply_markup=channel_subscription_keyboard(f"retry_{action_name}")
                    )
                    context.user_data['pending_action'] = func.__name__
                return
            
            # Obuna bor - funksiyani bajarish
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator
