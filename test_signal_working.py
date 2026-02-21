"""
Signal ishlab turganini tekshirish
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 70)
print("SIGNAL ISHLASHINI TEKSHIRISH")
print("=" * 70)

# Test foydalanuvchi
test_user = User.objects.filter(email_verified=True).first()

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")

print("\n" + "=" * 70)
print("NOTIFICATION YARATISH (Signal ishga tushishi kerak)")
print("=" * 70)

# Notification yaratish
print("\n📝 Notification yaratilmoqda...")

notification = Notification.objects.create(
    user=test_user,
    title="Signal Test",
    message="Bu signal test xabari. Agar signal ishlasa, email va telegram yuboriladi.",
    notification_type='info',
    icon='🔔',
    link='https://eduself.uz'
)

print(f"✅ Notification yaratildi: ID={notification.id}")
print("\n⏳ 15 soniya kutamiz (signal ishga tushishi va yuborish uchun)...")
print("   Log'larni kuzating...")

# 15 soniya kutish va log'larni kuzatish
time.sleep(15)

print("\n" + "=" * 70)
print("NATIJA")
print("=" * 70)

print("\n💡 Yuqoridagi log'larda quyidagilar bo'lishi kerak:")
print("   - 📤 Notification yuborish background thread'da boshlandi")
print("   - ✅ Email yuborildi: user@example.com")
print("   - ✅ Telegram yuborildi: username")
print("   - 📊 Jami yuborildi: X email, Y telegram")

print("\n⚠️  Agar log'lar ko'rinmasa:")
print("   1. Signal ishlamayapti")
print("   2. core/apps.py da signal import qilinmagan")
print("   3. INSTALLED_APPS da 'core' yo'q")

# Cleanup
print(f"\n🗑️  Test notification o'chirildi")
notification.delete()

print()
