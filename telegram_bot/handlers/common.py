"""Umumiy handlerlar"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram_bot.keyboards import main_menu_keyboard
from telegram_bot.utils import get_user_or_none, check_channel_subscription


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyuga qaytish (callback)"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)

    await query.edit_message_text(
        f"🏠 *Asosiy menyu*\n\n"
        f"Xush kelibsiz, {user.first_name if user else 'Foydalanuvchi'}!\n"
        f"Quyidagi bo'limlardan birini tanlang:",
        parse_mode='Markdown'
    )

    await query.message.reply_text(
        "Menyu:",
        reply_markup=main_menu_keyboard()
    )


async def main_menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyuga qaytish (text)"""
    user = await get_user_or_none(update.effective_user.id)

    await update.message.reply_text(
        f"🏠 *Asosiy menyu*\n\n"
        f"Xush kelibsiz, {user.first_name if user else 'Foydalanuvchi'}!",
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard()
    )


async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal obunasini tekshirish callback"""
    query = update.callback_query
    
    user_id = update.effective_user.id
    is_subscribed = await check_channel_subscription(context.bot, user_id)

    if is_subscribed:
        await query.answer("✅ Obuna tasdiqlandi!", show_alert=True)
        await query.edit_message_text(
            "✅ *Obuna tasdiqlandi!*\n\n"
            "Endi barcha funksiyalardan foydalanishingiz mumkin.\n"
            "Menyudan kerakli bo'limni tanlang 👇",
            parse_mode='Markdown'
        )
        await query.message.reply_text(
            "Menyu:",
            reply_markup=main_menu_keyboard()
        )
    else:
        await query.answer("❌ Siz hali kanalga obuna bo'lmagansiz!", show_alert=True)


async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message

    user = await get_user_or_none(update.effective_user.id)

    text = "⚙️ *Sozlamalar*\n\n"
    if user:
        text += f"👤 Username: @{user.username}\n"
        text += f"📧 Email: {user.email}\n"
        text += f"📱 Telegram ID: {user.telegram_id}\n\n"
    text += "Quyidagi amallarni bajarishingiz mumkin:"

    keyboard = [
        [InlineKeyboardButton("🔗 Saytda profilni tahrirlash", url="https://eduself.uz/accounts/profile/")],
        [InlineKeyboardButton("📊 Statistika", callback_data="profile_stats")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")]
    ]

    await message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_settings_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sozlamalar tugmasi"""
    if update.message.text == "⚙️ Sozlamalar":
        await settings_menu(update, context)


async def progress_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Progress info callback"""
    query = update.callback_query
    await query.answer("Bu test progressi", show_alert=False)


def register_handlers(app):
    """Umumiy handlerlarni ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(progress_info, pattern="^progress_info$"))
    app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^check_subscription$"))
    app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^retry_"))
    app.add_handler(MessageHandler(filters.Regex("^🏠 Asosiy menyu$"), main_menu_text))
    app.add_handler(MessageHandler(filters.Regex("^⚙️ Sozlamalar$"), handle_settings_text))
