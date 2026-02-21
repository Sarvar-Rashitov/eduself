"""
Auth provider bo'yicha notification yuborish testi
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from django.db.models import Q

print("=" * 70)
print("AUTH PROVIDER BO'YICHA FOYDALANUVCHILAR")
print("=" * 70)

# Email bilan login qilganlar
email_users = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True,
    auth_provider='email'
).exclude(email='')

# Google ID bor foydalanuvchilar
google_users = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True,
    google_id__isnull=False
).exclude(email='')

# Telegram ID bor foydalanuvchilar
telegram_users = User.objects.filter(
    is_active=True,
    telegram_chat_id__isnull=False,
    telegram_id__isnull=False
).exclude(telegram_chat_id='')

# Email yuborilishi kerak bo'lganlar (Google yoki Email)
email_notification_users = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).filter(
    Q(google_id__isnull=False) | Q(auth_provider='email')
).exclude(email='')

print(f"\n📊 Statistika:")
print(f"   📧 Email bilan login: {email_users.count()}")
print(f"   🔵 Google ID bor: {google_users.count()}")
print(f"   📱 Telegram ID bor: {telegram_users.count()}")
print(f"   ✉️  Email yuborilishi kerak: {email_notification_users.count()}")

print(f"\n📋 Birinchi 10 ta foydalanuvchi:")
print(f"\n{'#':<3} {'Ism':<15} {'Auth Provider':<15} {'Google ID':<10} {'Telegram ID':<12} {'Yuborish':<10}")
print("-" * 70)

all_users = User.objects.filter(is_active=True)[:10]
for i, user in enumerate(all_users, 1):
    google = "✅" if user.google_id else "❌"
    telegram = "✅" if user.telegram_id else "❌"
    
    # Qaysi usul bilan yuboriladi
    send_method = []
    if user.google_id or user.auth_provider == 'email':
        if user.email_verified:
            send_method.append("📧")
    if user.telegram_id and user.telegram_chat_id:
        send_method.append("📱")
    
    send_str = " ".join(send_method) if send_method else "❌"
    
    print(f"{i:<3} {user.first_name[:15]:<15} {user.auth_provider:<15} {google:<10} {telegram:<12} {send_str:<10}")

print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)

print(f"\n✅ Email yuboriladi: {email_notification_users.count()} foydalanuvchi")
print(f"   - Google ID bor: {google_users.count()}")
print(f"   - Email bilan login: {email_users.count()}")

print(f"\n✅ Telegram yuboriladi: {telegram_users.count()} foydalanuvchi")
print(f"   - Telegram ID bor: {telegram_users.count()}")

print(f"\n📊 Jami: {email_notification_users.count() + telegram_users.count()} notification yuboriladi")

print()
