#!/usr/bin/env python
"""Telegram notification'larni test qilish"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from telegram_bot.notification_sender import send_telegram_notification
from django.conf import settings

print("=" * 70)
print("TELEGRAM NOTIFICATION TEST")
print("=" * 70)

# Telegram chat_id si bor foydalanuvchilarni topish
users_with_telegram = User.objects.filter(
    telegram_chat_id__isnull=False
).exclude(telegram_chat_id='')

print(f"\n📱 Telegram bilan bog'langan foydalanuvchilar: {users_with_telegram.count()}")

if users_with_telegram.count() == 0:
    print("\n❌ Telegram bilan bog'langan foydalanuvchilar topilmadi!")
    print("\nYechim:")
    print("1. Telegram bot'ni oching: @edu_self_bot")
    print("2. /start ni bosing")
    print("3. Login qiling")
    print("4. Qayta test qiling")
    exit(1)

print("\nTelegram bilan bog'langan foydalanuvchilar:")
for user in users_with_telegram[:5]:  # Faqat birinchi 5 ta
    print(f"  • {user.first_name} ({user.username}) - Chat ID: {user.telegram_chat_id}")

# Birinchi foydalanuvchiga test notification yuborish
test_user = users_with_telegram.first()

print(f"\n{'=' * 70}")
print(f"TEST NOTIFICATION YUBORISH")
print(f"{'=' * 70}")
print(f"Foydalanuvchi: {test_user.first_name} ({test_user.username})")
print(f"Chat ID: {test_user.telegram_chat_id}")
print(f"{'=' * 70}\n")

# 1. Xush kelibsiz notification
print("1️⃣  Xush kelibsiz notification...")
try:
    result = send_telegram_notification(
        user_id=test_user.id,
        title="🎉 Xush kelibsiz!",
        message=f"Assalomu alaykum, {test_user.first_name}!\n\n"
                f"EduSelf platformasiga xush kelibsiz! "
                f"Endi siz platformaning barcha imkoniyatlaridan foydalanishingiz mumkin.",
        link=settings.SITE_URL
    )
    if result:
        print("   ✅ Yuborildi!")
    else:
        print("   ❌ Yuborilmadi!")
except Exception as e:
    print(f"   ❌ Xatolik: {e}")

import time
time.sleep(2)  # 2 soniya kutish

# 2. Qaytganingizdan xursandmiz notification
print("\n2️⃣  Qaytganingizdan xursandmiz notification...")
try:
    result = send_telegram_notification(
        user_id=test_user.id,
        title="👋 Qaytganingizdan xursandmiz!",
        message=f"Assalomu alaykum, {test_user.first_name}!\n\n"
                f"Siz EduSelf platformasiga qaytib keldingiz. "
                f"Davom eting va bilimingizni oshiring!",
        link=settings.SITE_URL
    )
    if result:
        print("   ✅ Yuborildi!")
    else:
        print("   ❌ Yuborilmadi!")
except Exception as e:
    print(f"   ❌ Xatolik: {e}")

time.sleep(2)

# 3. Yangi qurilmadan kirish notification
print("\n3️⃣  Yangi qurilmadan kirish notification...")
try:
    from django.utils import timezone
    result = send_telegram_notification(
        user_id=test_user.id,
        title="🔒 Yangi qurilmadan kirish",
        message=f"Sizning hisobingizga yangi qurilmadan kirish amalga oshirildi.\n\n"
                f"📅 Vaqt: {timezone.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"📱 Qurilma: Desktop\n"
                f"🌐 Brauzer: Google Chrome\n"
                f"💻 OS: Windows 10\n\n"
                f"Bu siz bo'lmasa, darhol parolingizni o'zgartiring!",
        link=f"{settings.SITE_URL}/accounts/forgot-password/"
    )
    if result:
        print("   ✅ Yuborildi!")
    else:
        print("   ❌ Yuborilmadi!")
except Exception as e:
    print(f"   ❌ Xatolik: {e}")

time.sleep(2)

# 4. Sizni sog'indik notification
print("\n4️⃣  Sizni sog'indik notification...")
try:
    result = send_telegram_notification(
        user_id=test_user.id,
        title="📚 Sizni sog'indik!",
        message=f"Assalomu alaykum, {test_user.first_name}!\n\n"
                f"Siz 5 kun faol bo'lmadingiz.\n\n"
                f"📊 Natijalaringiz:\n"
                f"• Jami testlar: {test_user.get_total_tests_taken()}\n"
                f"• O'tgan testlar: {test_user.get_passed_tests()}\n"
                f"• Umumiy ball: {test_user.total_points}\n"
                f"• Progress: {test_user.get_progress_percentage()}%\n\n"
                f"Qaytib kelib, o'qishni davom ettiring!",
        link=settings.SITE_URL
    )
    if result:
        print("   ✅ Yuborildi!")
    else:
        print("   ❌ Yuborilmadi!")
except Exception as e:
    print(f"   ❌ Xatolik: {e}")

print(f"\n{'=' * 70}")
print("✅ TEST YAKUNLANDI!")
print(f"{'=' * 70}\n")

print("📱 Telegram bot'ni tekshiring:")
print(f"   @{settings.TELEGRAM_BOT_USERNAME}")
print("\n💡 Nima ko'rishingiz kerak:")
print("   • 4 ta notification:")
print("     1. 🎉 Xush kelibsiz")
print("     2. 👋 Qaytganingizdan xursandmiz")
print("     3. 🔒 Yangi qurilmadan kirish")
print("     4. 📚 Sizni sog'indik")
print("   • Har birida emoji, matn va havola")
print("\n🔍 Agar notification kelmasa:")
print("   1. Telegram bot ishlab turganini tekshiring")
print("   2. TELEGRAM_BOT_TOKEN to'g'riligini tekshiring")
print("   3. telegram_chat_id to'g'riligini tekshiring")
print("   4. Bot'ni restart qiling")
