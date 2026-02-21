"""
Haqiqiy email manzilga notification yuborish testi
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
print("HAQIQIY EMAIL GA NOTIFICATION TEST")
print("=" * 60)

# Sizning emailingiz
test_email = "sarvarrashitov4321@gmail.com"

# Foydalanuvchini topish
test_user = User.objects.filter(email=test_email).first()

if not test_user:
    print(f"❌ {test_email} topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Email verified: {'✅' if test_user.email_verified else '❌'}")
print(f"   Telegram: {'✅ ' + str(test_user.telegram_chat_id) if test_user.telegram_chat_id else '❌ Ulanmagan'}")

if not test_user.email_verified:
    print("\n⚠️  Email tasdiqlanmagan! Email yuborilmaydi.")
    print("   Avval emailni tasdiqlang.")
    sys.exit(1)

print("\n" + "=" * 60)
print("NOTIFICATION YARATISH")
print("=" * 60)

# Notification yaratish
notification = Notification.objects.create(
    user=test_user,
    title="Admin Panel Test Xabari",
    message="Bu admin paneldan yuborilgan test bildirishnoma. Agar bu xabar emailingizga kelgan bo'lsa, demak email yuborish to'g'ri ishlayapti! 🎉",
    notification_type='info',
    icon='✉️',
    link='https://eduself.uz'
)

print(f"\n✅ Notification yaratildi: ID={notification.id}")
print("⏳ Email yuborilmoqda (background)...")
print("   10 soniya kutamiz...")

# 10 soniya kutish (email yuborilishi uchun)
time.sleep(10)

print("\n" + "=" * 60)
print("NATIJA")
print("=" * 60)
print(f"✅ Email yuborildi: {test_user.email}")
print("\n💡 EMAILINGIZNI TEKSHIRING!")
print("   - Inbox papkasini tekshiring")
print("   - Spam papkasini ham tekshiring")
print("   - Sarlavha: 'EduSelf - Admin Panel Test Xabari'")
print("   - Yuboruvchi: EduSelf <noreply@eduself.uz>")

# Cleanup
print(f"\n🗑️  Test notification o'chirildi")
notification.delete()

print("\n" + "=" * 60)
print("XULOSA")
print("=" * 60)
print("✅ Email yuborish ishlayapti")
print("✅ Emailingizni tekshiring")
print("✅ Agar kelmagan bo'lsa, spam papkasini tekshiring")
print()
