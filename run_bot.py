#!/usr/bin/env python
"""EduSelf Telegram Bot - Ishga tushirish skripti"""
import os
import sys

# Django sozlamalari
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')

# Django ni ishga tushirish
import django
django.setup()

# Botni ishga tushirish
from telegram_bot.bot import main

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 EduSelf Telegram Bot")
    print("=" * 50)
    print()
    print("Bot ishga tushmoqda...")
    print("To'xtatish uchun Ctrl+C bosing")
    print()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Bot to'xtatildi.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Xatolik: {e}")
        sys.exit(1)
