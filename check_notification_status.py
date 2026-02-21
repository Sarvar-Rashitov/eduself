"""
Notification yuborish holatini tekshirish
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Notification
from accounts.models import User
from django.db.models import Q

print("=" * 70)
print("NOTIFICATION YUBORISH HOLATI")
print("=" * 70)

# Oxirgi notification
last_notification = Notification.objects.filter(is_global=True).order_by('-created_at').first()

if not last_notification:
    print("\n❌ Global notification topilmadi!")
    sys.exit(1)

print(f"\n📝 Oxirgi global notification:")
print(f"   ID: {last_notification.id}")
print(f"   Sarlavha: {last_notification.title}")
print(f"   Yaratilgan: {last_notification.created_at}")

# Statistika
email_users = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).filter(
    Q(google_id__isnull=False) | Q(auth_provider='email')
).exclude(email='').count()

telegram_users = User.objects.filter(
    is_active=True,
    telegram_chat_id__isnull=False,
    telegram_id__isnull=False
).exclude(telegram_chat_id='').count()

print(f"\n📊 Yuborilishi kerak:")
print(f"   📧 Email: {email_users}")
print(f"   📱 Telegram: {telegram_users}")
print(f"   📊 Jami: {email_users + telegram_users}")

print("\n💡 Log'larda quyidagilar bo'lishi kerak:")
print("   - ✅ Email yuborildi: user@example.com (89 marta)")
print("   - ✅ Telegram yuborildi: username (260 marta)")
print("   - 📊 Jami yuborildi: 89 email, 260 telegram")

print("\n✅ Emailingizni va Telegram botni tekshiring!")
print()
