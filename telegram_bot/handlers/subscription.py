"""Obuna handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from asgiref.sync import sync_to_async
from telegram_bot.utils import get_user_or_none
from telegram_bot.decorators import require_subscription
import os

SITE_URL = os.getenv('SITE_URL', 'https://eduself.uz')


@sync_to_async
def get_subscription_plans():
    """Barcha faol obuna tariflarini olish"""
    from subscriptions.models import SubscriptionPlan
    return list(SubscriptionPlan.objects.filter(is_active=True).order_by('order', 'price'))


@sync_to_async
def get_user_subscription(user):
    """Foydalanuvchi obunasini olish"""
    return user.get_active_subscription()


@require_subscription("subscription")
async def subscription_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Obuna tariflari ro'yxati"""
    query = update.callback_query
    await query.answer()
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    plans = await get_subscription_plans()
    current_sub = await get_user_subscription(user)
    
    text = "💎 *Premium Obuna Tariflari*\n\n"
    
    if current_sub:
        end_date = current_sub.end_date.strftime('%d.%m.%Y')
        text += f"✅ Sizda faol obuna bor: *{current_sub.plan.name}*\n"
        text += f"📅 Tugash sanasi: {end_date}\n\n"
        text += "━━━━━━━━━━━━━━━\n\n"
    
    text += "*Premium imkoniyatlar:*\n\n"
    text += "♾️ Cheksiz yurakchalar\n"
    text += "🔓 Barcha mavzular ochiq\n"
    text += "🤖 AI tahlil va hamroh\n"
    text += "🏆 Universitet imtihonlari\n"
    text += "📝 Mock imtihonlar\n"
    text += "🎓 Sertifikat testlari\n\n"
    text += "Obuna sotib olish uchun saytga o'ting:"
    
    keyboard = [
        [InlineKeyboardButton("🌐 Saytda obuna bo'lish", url=f"{SITE_URL}/subscriptions/plans/")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="profile")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def register_handlers(app):
    """Subscription handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(subscription_plans, pattern="^subscription_plans$"))
