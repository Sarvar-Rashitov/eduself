"""Telegram bot webhook'ni o'chirish"""
import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def delete_webhook():
    """Webhook'ni o'chirish"""
    bot = Bot(token=BOT_TOKEN)
    
    print("Webhook o'chirilmoqda...")
    result = await bot.delete_webhook(drop_pending_updates=True)
    
    if result:
        print("✅ Webhook muvaffaqiyatli o'chirildi!")
        print("Endi botni polling rejimida ishga tushirishingiz mumkin.")
    else:
        print("❌ Webhook o'chirishda xatolik yuz berdi.")
    
    # Bot ma'lumotlarini ko'rsatish
    me = await bot.get_me()
    print(f"\nBot: @{me.username}")
    print(f"ID: {me.id}")

if __name__ == '__main__':
    asyncio.run(delete_webhook())
