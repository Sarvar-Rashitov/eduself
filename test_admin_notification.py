#!/usr/bin/env python
"""Admin notification email test"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Notification, NotificationType
from accounts.models import User

print("=" * 70)
print("ADMIN NOTIFICATION EMAIL TEST")
print("=" * 70)

# Email tasdiqlangan foydalanuvchilarni topish
users_with_email = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).exclude(email='')

print(f"\n📧 Email tasdiqlangan foydalanuvchilar: {users_with_email.count()}")

if users_with_email.count() == 0:
    print("\n❌ Email tasdiqlangan foydalanuvchilar topilmadi!")
    exit(1)

# Birinchi foydalanuvchiga test notification
test_user = users_with_email.first()

print(f"\n{'=' * 70}")
print(f"TEST NOTIFICATION YARATISH")
print(f"{'=' * 70}")
print(f"Foydalanuvchi: {test_user.first_name} ({test_user.email})")
print(f"{'=' * 70}\n")

# 1. Shaxsiy notification
print("1️⃣  Shaxsiy notification yaratish...")
try:
    notification = Notification.objects.create(
        user=test_user,
        notification_type=NotificationType.SYSTEM,
        title="Test Bildirishnoma",
        message="Bu admin paneldan yuborilgan test bildirishnoma.\n\nEmail va Telegram orqali yuboriladi.",
        link="https://eduself.uz",
        icon="bi-bell",
        is_global=False
    )
    print(f"   ✅ Yaratildi! ID: {notification.id}")
    print(f"   📧 Email yuborilmoqda: {test_user.email}")
    if test_user.telegram_chat_id:
        print(f"   📱 Telegram yuborilmoqda: {test_user.telegram_chat_id}")
except Exception as e:
    print(f"   ❌ Xatolik: {e}")

import time
time.sleep(3)

# 2. Global notification (faqat 5 ta foydalanuvchiga test uchun)
print("\n2️⃣  Global notification yaratish (test)...")
print("   ⚠️  Bu haqiqiy global notification yaratadi!")
print("   ⚠️  Barcha foydalanuvchilarga email yuboriladi!")

response = input("\n   Davom ettirasizmi? (yes/no): ")

if response.lower() == 'yes':
    try:
        notification = Notification.objects.create(
            notification_type=NotificationType.NEWS,
            title="Yangi Xususiyat!",
            message="EduSelf platformasida yangi xususiyatlar qo'shildi:\n\n"
                    "• Professional email notification'lar\n"
                    "• Telegram notification'lar\n"
                    "• Yangi qurilma xavfsizligi\n"
                    "• Faol bo'lmaganlik eslatmalari\n\n"
                    "Platformaga kirib, yangi imkoniyatlardan foydalaning!",
            link="https://eduself.uz",
            icon="bi-star",
            is_global=True
        )
        print(f"   ✅ Yaratildi! ID: {notification.id}")
        print(f"   📧 Email yuborilmoqda: {users_with_email.count()} ta foydalanuvchiga")
        
        telegram_count = User.objects.filter(
            is_active=True,
            telegram_chat_id__isnull=False
        ).exclude(telegram_chat_id='').count()
        print(f"   📱 Telegram yuborilmoqda: {telegram_count} ta foydalanuvchiga")
    except Exception as e:
        print(f"   ❌ Xatolik: {e}")
else:
    print("   ⏭️  O'tkazib yuborildi")

print(f"\n{'=' * 70}")
print("✅ TEST YAKUNLANDI!")
print(f"{'=' * 70}\n")

print("📧 Email inbox'ni tekshiring:")
print(f"   {test_user.email}")
print("\n💡 Nima ko'rishingiz kerak:")
print("   • Admin notification email")
print("   • Logo, tugma va chiroyli dizayn")
print("   • Notification title va message")
print("\n🔍 Agar email kelmasa:")
print("   1. Email sozlamalarini tekshiring")
print("   2. Spam papkani tekshiring")
print("   3. core/signals.py log'larini ko'ring")
print("   4. Django server log'larini tekshiring")
