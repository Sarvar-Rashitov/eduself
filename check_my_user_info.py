"""
Sizning foydalanuvchi ma'lumotlaringizni tekshirish
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("SIZNING FOYDALANUVCHI MA'LUMOTLARINGIZ")
print("=" * 70)

# Sizning emailingiz
test_email = "sarvarrashitov4321@gmail.com"

# Foydalanuvchini topish
user = User.objects.filter(email=test_email).first()

if not user:
    print(f"\n❌ {test_email} topilmadi!")
    
    # Barcha foydalanuvchilarni ko'rsatish
    print("\n📋 Barcha foydalanuvchilar:")
    for u in User.objects.all()[:10]:
        print(f"   - {u.first_name} ({u.email})")
    
    sys.exit(1)

print(f"\n✅ Foydalanuvchi topildi!")
print(f"\n📋 Ma'lumotlar:")
print(f"   ID: {user.id}")
print(f"   Ism: {user.first_name} {user.last_name}")
print(f"   Username: {user.username}")
print(f"   Email: {user.email}")
print(f"   Email verified: {user.email_verified}")
print(f"   Auth provider: {user.auth_provider}")
print(f"   Google ID: {user.google_id}")
print(f"   Telegram ID: {user.telegram_id}")
print(f"   Telegram username: {user.telegram_username}")
print(f"   Telegram chat_id: {user.telegram_chat_id}")
print(f"   Is active: {user.is_active}")

print("\n" + "=" * 70)
print("NOTIFICATION YUBORILISHI KERAKMI?")
print("=" * 70)

# Email yuborilishi kerakmi?
should_send_email = False
email_reason = ""

if user.google_id:
    should_send_email = True
    email_reason = "Google ID bor"
elif user.auth_provider == 'email':
    should_send_email = True
    email_reason = "Email bilan login qilgan"

if should_send_email and user.email_verified:
    print(f"\n✅ EMAIL YUBORILISHI KERAK")
    print(f"   Sabab: {email_reason}")
    print(f"   Email: {user.email}")
else:
    print(f"\n❌ EMAIL YUBORILMAYDI")
    if not should_send_email:
        print(f"   Sabab: Google ID yo'q va email bilan login qilmagan")
        print(f"   Auth provider: {user.auth_provider}")
    elif not user.email_verified:
        print(f"   Sabab: Email tasdiqlanmagan")

# Telegram yuborilishi kerakmi?
should_send_telegram = False
telegram_reason = ""

if user.telegram_id and user.telegram_chat_id:
    should_send_telegram = True
    telegram_reason = "Telegram ID va chat_id bor"

if should_send_telegram:
    print(f"\n✅ TELEGRAM YUBORILISHI KERAK")
    print(f"   Sabab: {telegram_reason}")
    print(f"   Telegram ID: {user.telegram_id}")
    print(f"   Chat ID: {user.telegram_chat_id}")
else:
    print(f"\n❌ TELEGRAM YUBORILMAYDI")
    if not user.telegram_id:
        print(f"   Sabab: Telegram ID yo'q")
    elif not user.telegram_chat_id:
        print(f"   Sabab: Telegram chat_id yo'q")

print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)

if should_send_email or should_send_telegram:
    print("\n✅ Sizga notification yuborilishi kerak!")
    if should_send_email:
        print(f"   📧 Email: {user.email}")
    if should_send_telegram:
        print(f"   📱 Telegram: {user.telegram_chat_id}")
else:
    print("\n❌ Sizga notification yuborilmaydi!")
    print("   Sabab: Google ID, Email login yoki Telegram ID yo'q")

print()
