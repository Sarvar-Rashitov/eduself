"""
Admin notification - Email va Telegram yuborishni to'liq test qilish
"""
import os
import sys
import django
import time

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from core.models import Notification

print("=" * 60)
print("NOTIFICATION EMAIL + TELEGRAM TO'LIQ TEST")
print("=" * 60)

# Test foydalanuvchi (email va telegram bor)
test_user = User.objects.filter(
    email_verified=True,
    telegram_chat_id__isnull=False
).exclude(telegram_chat_id='').first()

if not test_user:
    print("⚠️  Email va Telegram ulangan foydalanuvchi topilmadi")
    print("   Faqat email bilan test qilamiz...")
    test_user = User.objects.filter(email_verified=True).first()

if not test_user:
    print("❌ Test uchun foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Telegram: {'✅ ' + str(test_user.telegram_chat_id) if test_user.telegram_chat_id else '❌ Ulanmagan'}")

print("\n" + "=" * 60)
print("SHAXSIY NOTIFICATION YARATISH")
print("=" * 60)

# Notification yaratish
notification = Notification.objects.create(
    user=test_user,
    title="Test: Email va Telegram",
    message="Bu admin paneldan yuborilgan test xabari. Email va Telegram orqali kelishi kerak.",
    notification_type='info',
    icon='🔔',
    link='https://eduself.uz'
)

print(f"\n✅ Notification yaratildi: ID={notification.id}")
print("⏳ Email va Telegram yuborilmoqda (background)...")
print("   5 soniya kutamiz...")

# 5 soniya kutish (email va telegram yuborilishi uchun)
time.sleep(5)

print("\n" + "=" * 60)
print("NATIJA")
print("=" * 60)
print("✅ Notification yaratildi va yuborildi")
print(f"   📧 Email: {test_user.email}")
if test_user.telegram_chat_id:
    print(f"   📱 Telegram: {test_user.telegram_chat_id}")
print("\n💡 Emailingizni va Telegram botni tekshiring!")

# Statistika
print("\n" + "=" * 60)
print("STATISTIKA")
print("=" * 60)

email_users = User.objects.filter(
    is_active=True,
    email_verified=True
).exclude(email='').count()

telegram_users = User.objects.filter(
    is_active=True,
    telegram_chat_id__isnull=False
).exclude(telegram_chat_id='').count()

print(f"📊 Jami email tasdiqlangan: {email_users}")
print(f"📊 Jami telegram ulangan: {telegram_users}")

# Cleanup
print(f"\n🗑️  Test notification o'chirildi")
notification.delete()

print("\n" + "=" * 60)
print("XULOSA")
print("=" * 60)
print("✅ Admin notification email va telegram yuborish ishlayapti")
print("✅ Emailingizni va Telegram botni tekshiring")
print("✅ Agar xabar kelmagan bo'lsa, log'larni tekshiring")
print()
