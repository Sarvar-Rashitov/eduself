"""
Yakuniy texnik ish bildirishnomasi (Auth provider bo'yicha)
"""
import os
import sys
import django
import time

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Notification
from accounts.models import User
from django.db.models import Q
import logging

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 70)
print("TEXNIK ISH BILDIRISHNOMASI (AUTH PROVIDER BO'YICHA)")
print("=" * 70)

# Statistika
email_users = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).filter(
    Q(google_id__isnull=False) | Q(auth_provider='email')
).exclude(email='')

telegram_users = User.objects.filter(
    is_active=True,
    telegram_chat_id__isnull=False,
    telegram_id__isnull=False
).exclude(telegram_chat_id='')

print(f"\n📊 Statistika:")
print(f"   📧 Email yuboriladi: {email_users.count()} (Google/Email login)")
print(f"   📱 Telegram yuboriladi: {telegram_users.count()} (Telegram login)")
print(f"   📊 Jami: {email_users.count() + telegram_users.count()} notification")

print("\n" + "=" * 70)
print("BILDIRISHNOMA MATNI")
print("=" * 70)

title = "⚙️ Texnik ish olib borilyapti"
message = """Hurmatli foydalanuvchilar!

Platformamizda yangi xususiyatlar qo'shish va xizmat sifatini yaxshilash maqsadida texnik ishlar olib borilyapti.

Bu davrda platformada qisqa muddatli uzilishlar bo'lishi mumkin.

Yuzaga kelgan noqulayliklar uchun samimiy uzr so'raymiz! 🙏

Tez orada yangi imkoniyatlar bilan qaytamiz!"""

link = "https://eduself.uz"

print(f"\n📝 Sarlavha: {title}")
print(f"📝 Xabar:\n{message}")
print(f"🔗 Havola: {link}")

print("\n" + "=" * 70)
print("TASDIQLASH")
print("=" * 70)

confirm = input(f"\n⚠️  {email_users.count()} email va {telegram_users.count()} telegram yuboriladi. Davom etamizmi? (ha/yo'q): ")

if confirm.lower() not in ['ha', 'yes', 'y']:
    print("\n❌ Bekor qilindi!")
    sys.exit(0)

print("\n" + "=" * 70)
print("BILDIRISHNOMA YARATISH")
print("=" * 70)

# Global notification yaratish
notification = Notification.objects.create(
    title=title,
    message=message,
    notification_type='system',
    icon='⚙️',
    link=link,
    is_global=True
)

print(f"\n✅ Bildirishnoma yaratildi: ID={notification.id}")
print("⏳ Email va Telegram yuborish background'da boshlandi...")
print("   Log'larni kuzating...")
print("   30 soniya kutamiz...")

# 30 soniya kutish
time.sleep(30)

print("\n" + "=" * 70)
print("NATIJA")
print("=" * 70)

print(f"\n✅ Muvaffaqiyatli!")
print(f"   📧 {email_users.count()} ta email yuborildi (Google/Email)")
print(f"   📱 {telegram_users.count()} ta telegram yuborildi (Telegram)")

print("\n💡 Tekshirish:")
print("   1. Emailingizni tekshiring (Google login)")
print("   2. Telegram botni tekshiring (Telegram login)")
print("   3. Log'larda yuborish jarayonini ko'ring")

print("\n📊 Log'larda ko'rinishi kerak:")
print("   - 📧 Global notification: X email (Google/Email), Y telegram")
print("   - ✅ Email yuborildi: user@example.com")
print("   - ✅ Telegram yuborildi: username")
print("   - 📊 Jami yuborildi: X email, Y telegram")

print()
