"""
Global notification haqiqiy test (kichik guruhga)
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
import logging

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 70)
print("GLOBAL NOTIFICATION HAQIQIY TEST")
print("=" * 70)

# Statistika
email_users = User.objects.filter(
    is_active=True,
    email_verified=True
).exclude(email='')

telegram_users = User.objects.filter(
    is_active=True,
    telegram_chat_id__isnull=False
).exclude(telegram_chat_id='')

print(f"\n📊 Statistika:")
print(f"   📧 Email: {email_users.count()} foydalanuvchi")
print(f"   📱 Telegram: {telegram_users.count()} foydalanuvchi")

# Birinchi 5 ta foydalanuvchini ko'rsatish
print(f"\n📋 Birinchi 5 ta email foydalanuvchi:")
for i, user in enumerate(email_users[:5], 1):
    print(f"   {i}. {user.first_name} - {user.email}")

print("\n" + "=" * 70)
print("GLOBAL NOTIFICATION YARATISH")
print("=" * 70)

confirm = input(f"\n⚠️  {email_users.count()} email va {telegram_users.count()} telegram yuboriladi. Davom etamizmi? (ha/yo'q): ")

if confirm.lower() not in ['ha', 'yes', 'y']:
    print("\n❌ Bekor qilindi!")
    sys.exit(0)

# Global notification yaratish
print("\n📝 Global notification yaratilmoqda...")

notification = Notification.objects.create(
    title="Test: Global Notification",
    message="Bu global notification test xabari. Barcha foydalanuvchilarga yuborilmoqda.",
    notification_type='info',
    icon='🔔',
    link='https://eduself.uz',
    is_global=True
)

print(f"✅ Notification yaratildi: ID={notification.id}")
print("\n⏳ 30 soniya kutamiz (yuborish uchun)...")
print("   Log'larni kuzating...")

# 30 soniya kutish
time.sleep(30)

print("\n" + "=" * 70)
print("NATIJA")
print("=" * 70)

print("\n✅ Global notification yuborildi!")
print(f"   📧 {email_users.count()} ta email")
print(f"   📱 {telegram_users.count()} ta telegram")

print("\n💡 Emailingizni va Telegram botni tekshiring!")
print("   Sarlavha: 'EduSelf - Test: Global Notification'")

# Cleanup
print(f"\n🗑️  Test notification o'chirildi")
notification.delete()

print()
