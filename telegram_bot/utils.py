"""Telegram bot yordamchi funksiyalari"""
import os
import hashlib
import time
from asgiref.sync import sync_to_async
from telegram import Bot, User as TelegramUser
from telegram.error import TelegramError
from accounts.models import User


# Login tokenlarni saqlash uchun (xotirada - production uchun Redis ishlatish kerak)
_login_tokens = {}


def get_channel_username():
    """Kanal username ni olish"""
    return os.getenv('TELEGRAM_CHANNEL_USERNAME', '@eduself_channel')


async def check_channel_subscription(bot: Bot, user_id: int) -> bool:
    """Foydalanuvchi kanalga obuna bo'lganligini tekshirish"""
    try:
        channel = get_channel_username()
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except TelegramError as e:
        print(f"Kanal obunasini tekshirishda xatolik: {e}")
        return False


@sync_to_async
def get_user_or_none(telegram_id: int) -> User | None:
    """Telegram ID bo'yicha foydalanuvchini olish"""
    try:
        return User.objects.get(telegram_id=str(telegram_id))
    except User.DoesNotExist:
        return None


@sync_to_async
def create_user_from_telegram(tg_user: TelegramUser) -> User:
    """Telegram foydalanuvchisidan avtomatik ro'yxatdan o'tkazish"""
    telegram_id = str(tg_user.id)
    
    # Avval mavjud foydalanuvchini tekshirish
    existing_user = User.objects.filter(telegram_id=telegram_id).first()
    if existing_user:
        return existing_user
    
    # Username yaratish - telegram username'ni to'liq saqlash (pastki chiziq bilan)
    base_username = tg_user.username or f"user{telegram_id}"
    username = base_username
    counter = 1
    
    # Unique username topish
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    
    # Foydalanuvchi yaratish - email NULL (unique constraint uchun)
    user = User(
        username=username,
        email=None,  # NULL - unique constraint muammosini hal qiladi
        telegram_id=telegram_id,
        first_name=tg_user.first_name or '',
        last_name=tg_user.last_name or '',
        auth_provider='telegram',
        email_verified=False
    )
    user.set_unusable_password()
    user.save()
    
    return user


@sync_to_async
def generate_login_token(telegram_id: str) -> str:
    """Xavfsiz login token yaratish - 5 daqiqa amal qiladi"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    timestamp = str(int(time.time()))
    
    # Token yaratish
    token_data = f"{telegram_id}:{bot_token}:{timestamp}"
    token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
    
    # Tokenni saqlash (timestamp bilan)
    _login_tokens[f"{telegram_id}:{token}"] = int(timestamp)
    
    # Eski tokenlarni tozalash (5 daqiqadan eski)
    current_time = int(time.time())
    expired_keys = [k for k, v in _login_tokens.items() if current_time - v > 300]
    for key in expired_keys:
        del _login_tokens[key]
    
    return token


def verify_login_token(telegram_id: str, token: str) -> bool:
    """Login tokenni tekshirish"""
    key = f"{telegram_id}:{token}"
    
    if key not in _login_tokens:
        return False
    
    # Vaqtni tekshirish (5 daqiqa)
    token_time = _login_tokens[key]
    if int(time.time()) - token_time > 300:
        del _login_tokens[key]
        return False
    
    # Token ishlatildi - o'chirish
    del _login_tokens[key]
    return True


@sync_to_async
def get_user_by_id(user_id: int) -> User | None:
    """ID bo'yicha foydalanuvchini olish"""
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


@sync_to_async
def user_exists_by_telegram_id(telegram_id: int) -> bool:
    """Telegram ID bo'yicha foydalanuvchi mavjudligini tekshirish"""
    return User.objects.filter(telegram_id=str(telegram_id)).exists()


@sync_to_async
def user_exists_by_username(username: str) -> bool:
    """Username bo'yicha foydalanuvchi mavjudligini tekshirish"""
    return User.objects.filter(username=username).exists()


@sync_to_async
def user_exists_by_email(email: str) -> bool:
    """Email bo'yicha foydalanuvchi mavjudligini tekshirish"""
    return User.objects.filter(email=email.lower()).exists()


@sync_to_async
def get_user_by_username(username: str) -> User | None:
    """Username bo'yicha foydalanuvchini olish"""
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


@sync_to_async
def get_user_by_email(email: str) -> User | None:
    """Email bo'yicha foydalanuvchini olish"""
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


@sync_to_async
def update_user_telegram_id(user: User, telegram_id: str) -> User:
    """Foydalanuvchi telegram_id ni yangilash"""
    user.telegram_id = telegram_id
    user.save()
    return user


def format_time(seconds: int) -> str:
    """Sekundlarni formatlash"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Matnni qisqartirish"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
