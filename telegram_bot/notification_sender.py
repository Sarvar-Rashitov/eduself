"""
Telegram bot orqali bildirishnoma yuborish moduli
"""
import os
import asyncio
import logging
import threading
from typing import List, Optional
from telegram import Bot
from telegram.error import TelegramError
from django.conf import settings
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


@sync_to_async
def get_users_with_telegram_chat_id():
    """Telegram chat_id si bor foydalanuvchilarni olish"""
    from accounts.models import User
    return list(User.objects.filter(telegram_chat_id__isnull=False).exclude(telegram_chat_id=''))


@sync_to_async
def get_user_by_id(user_id: int):
    """ID bo'yicha foydalanuvchini olish"""
    from accounts.models import User
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def get_notification_bot():
    """Bildirishnoma yuborish uchun alohida Bot instance"""
    bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN sozlamasi topilmadi!")
        return None
    
    return Bot(token=bot_token)


class TelegramNotificationSender:
    """Telegram bot orqali bildirishnoma yuborish klassi"""
    
    def __init__(self):
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        if not self.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN sozlamasi topilmadi!")
            return
    
    async def send_notification_to_user(self, user_id: int, title: str, message: str, link: str = None):
        """Bitta foydalanuvchiga bildirishnoma yuborish"""
        if not self.bot_token:
            return False
        
        # Har safar yangi Bot instance yaratish (webhook rejimi uchun)
        bot = get_notification_bot()
        if not bot:
            return False
        
        try:
            # Foydalanuvchining telegram_chat_id sini olish
            user = await get_user_by_id(user_id)
            if not user or not user.telegram_chat_id:
                logger.warning(f"Foydalanuvchi {user_id} uchun telegram_chat_id topilmadi")
                return False
            
            # Xabar matnini tayyorlash
            text = f"<b>{title}</b>\n\n{message}"
            
            if link:
                text += f"\n\n🔗 <a href='{link}'>Batafsil ko'rish</a>"
            
            # Xabarni yuborish
            await bot.send_message(
                chat_id=user.telegram_chat_id,
                text=text,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            
            logger.info(f"Bildirishnoma yuborildi: {user.username} ({user.telegram_chat_id})")
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram xatoligi: {e}")
            return False
        except Exception as e:
            logger.error(f"Bildirishnoma yuborishda xatolik: {e}")
            return False
    
    async def send_global_notification(self, title: str, message: str, link: str = None):
        """Barcha foydalanuvchilarga bildirishnoma yuborish"""
        if not self.bot_token:
            return 0
        
        # Har safar yangi Bot instance yaratish (webhook rejimi uchun)
        bot = get_notification_bot()
        if not bot:
            return 0
        
        # Telegram chat_id si bor foydalanuvchilarni olish
        users = await get_users_with_telegram_chat_id()
        
        success_count = 0
        
        for user in users:
            try:
                # Xabar matnini tayyorlash
                text = f"🔔 <b>{title}</b>\n\n{message}"
                
                if link:
                    text += f"\n\n🔗 <a href='{link}'>Batafsil ko'rish</a>"
                
                # Xabarni yuborish
                await bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text=text,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
                
                success_count += 1
                logger.info(f"Global bildirishnoma yuborildi: {user.username}")
                
                # Rate limiting uchun kichik kutish
                await asyncio.sleep(0.1)
                
            except TelegramError as e:
                logger.error(f"Telegram xatoligi ({user.username}): {e}")
                continue
            except Exception as e:
                logger.error(f"Bildirishnoma yuborishda xatolik ({user.username}): {e}")
                continue
        
        logger.info(f"Global bildirishnoma yuborish tugadi: {success_count}/{len(users)}")
        return success_count
    
    def send_notification_sync(self, user_id: int = None, title: str = "", message: str = "", link: str = None, is_global: bool = False):
        """Sinxron ravishda bildirishnoma yuborish (Django signallar uchun)"""
        if not self.bot_token:
            return False
        
        def run_async_in_thread():
            """Alohida thread da async funksiyani ishga tushirish"""
            try:
                # Yangi event loop yaratish
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    if is_global:
                        # Global bildirishnoma
                        result = loop.run_until_complete(
                            self.send_global_notification(title, message, link)
                        )
                        return result > 0
                    else:
                        # Shaxsiy bildirishnoma
                        result = loop.run_until_complete(
                            self.send_notification_to_user(user_id, title, message, link)
                        )
                        return result
                finally:
                    loop.close()
            except Exception as e:
                logger.error(f"Thread da async ishga tushirishda xatolik: {e}")
                return False
        
        try:
            # Thread da ishga tushirish
            thread = threading.Thread(target=run_async_in_thread)
            thread.daemon = True  # Daemon thread
            thread.start()
            thread.join(timeout=30)  # 30 soniya kutish
            
            logger.info(f"Bildirishnoma yuborish thread ishga tushdi: {title}")
            return True  # Thread muvaffaqiyatli ishga tushdi
                
        except Exception as e:
            logger.error(f"Sinxron bildirishnoma yuborishda xatolik: {e}")
            return False


# Global instance
notification_sender = TelegramNotificationSender()


def send_telegram_notification(user_id: int = None, title: str = "", message: str = "", link: str = None, is_global: bool = False):
    """
    Telegram bot orqali bildirishnoma yuborish uchun umumiy funksiya
    
    Args:
        user_id: Foydalanuvchi ID (shaxsiy bildirishnoma uchun)
        title: Bildirishnoma sarlavhasi
        message: Bildirishnoma matni
        link: Qo'shimcha havola (ixtiyoriy)
        is_global: Global bildirishnoma (barcha foydalanuvchilarga)
    
    Returns:
        bool: Muvaffaqiyatli yuborildi yoki yo'q
    """
    return notification_sender.send_notification_sync(
        user_id=user_id,
        title=title,
        message=message,
        link=link,
        is_global=is_global
    )