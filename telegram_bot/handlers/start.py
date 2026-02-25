"""Start va help handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from telegram_bot.keyboards import main_menu_keyboard
from telegram_bot.utils import get_user_or_none, create_user_from_telegram, generate_login_token
import os

SITE_URL = os.getenv('SITE_URL', 'https://eduself.uz')


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda - avtomatik ro'yxatdan o'tkazish"""
    tg_user = update.effective_user
    
    # Foydalanuvchi mavjudligini tekshirish
    db_user = await get_user_or_none(tg_user.id)
    
    if not db_user:
        # Yangi foydalanuvchi - avtomatik ro'yxatdan o'tkazish
        db_user = await create_user_from_telegram(tg_user)
    else:
        # Mavjud foydalanuvchi uchun chat_id ni yangilash
        from telegram_bot.utils import update_user_telegram_chat_id
        await update_user_telegram_chat_id(db_user, tg_user.id)
    
    # start parametrini tekshirish (login yoki register)
    args = context.args
    if args and args[0] in ['login', 'register']:
        # Saytdan kelgan - xavfsiz login havolasini yaratish
        login_token = await generate_login_token(str(tg_user.id))
        login_url = f"{SITE_URL}/accounts/telegram-callback/?telegram_id={tg_user.id}&token={login_token}"
        
        # Foydalanuvchi ismini olish
        display_name = db_user.first_name or db_user.username
        
        text = f"""✅ Muvaffaqiyatli!

👤 Foydalanuvchi: {display_name}

🔐 Saytga kirish uchun quyidagi tugmani bosing 👇

⚠️ Havola 5 daqiqa ichida amal qiladi"""
        
        keyboard = [
            [InlineKeyboardButton("🌐 Saytga kirish", url=login_url)],
            [InlineKeyboardButton("📱 Botda davom etish", callback_data="main_menu")]
        ]
        
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Asosiy menyuni ham ko'rsatish
        await update.message.reply_text(
            "Yoki botdan foydalanishni davom eting:",
            reply_markup=main_menu_keyboard()
        )
        return
    
    # Oddiy start
    welcome_text = f"""🎓 *Assalomu alaykum, {db_user.first_name or db_user.username}!*

EduSelf ta'lim platformasiga xush kelibsiz!

📚 *Imkoniyatlar:*
• Fanlar bo'yicha testlar
• Sertifikat imtihonlari
• Mock DTM testlari
• Ta'lim muassasalari
• AI Hamroh yordamchisi

Quyidagi menyudan kerakli bo'limni tanlang 👇"""

    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard()
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam xabari"""
    help_text = """📖 *EduSelf Bot Yordam*

*Asosiy buyruqlar:*
/start - Botni ishga tushirish
/help - Yordam

*Qanday ishlaydi:*
1️⃣ Menyudan bo'lim tanlang
2️⃣ Kanalga obuna bo'ling
3️⃣ Test yeching
4️⃣ XP to'plang
5️⃣ Reytingda ko'taring!

Savollar bo'lsa: @eduself_support"""

    await update.message.reply_text(help_text, parse_mode='Markdown')


def register_handlers(app):
    """Start handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
