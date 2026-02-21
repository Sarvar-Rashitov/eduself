"""
Barcha foydalanuvchilarga texnik ish haqida bildirishnoma yuborish
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Notification
from accounts.models import User

print("=" * 70)
print("TEXNIK ISH HAQIDA BILDIRISHNOMA YUBORISH")
print("=" * 70)

# Statistika
email_users = User.objects.filter(
    is_active=True,
    email_verified=True
).exclude(email='').count()

telegram_users = User.objects.filter(
    is_active=True,
    telegram_chat_id__isnull=False
).exclude(telegram_chat_id='').count()

print(f"\n📊 Statistika:")
print(f"   📧 Email tasdiqlangan: {email_users} foydalanuvchi")
print(f"   📱 Telegram ulangan: {telegram_users} foydalanuvchi")

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

confirm = input(f"\n⚠️  {email_users} email va {telegram_users} telegram yuboriladi. Davom etamizmi? (ha/yo'q): ")

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
print("   Bu jarayon 1-2 daqiqa davom etishi mumkin")

print("\n" + "=" * 70)
print("NATIJA")
print("=" * 70)

print(f"\n✅ Muvaffaqiyatli!")
print(f"   📧 {email_users} ta email yuborilmoqda")
print(f"   📱 {telegram_users} ta telegram yuborilmoqda")
print(f"   🔔 {email_users + telegram_users} ta browser notification ko'rinadi")

print("\n💡 Keyingi qadamlar:")
print("   1. 2-3 daqiqa kuting (yuborish tugashi uchun)")
print("   2. Emailingizni tekshiring")
print("   3. Telegram botni tekshiring")
print("   4. Log'larni kuzating")

print("\n📊 Log'larni kuzatish:")
print("   - ✅ Email yuborildi: user@example.com")
print("   - ✅ Telegram yuborildi: username")
print("   - 📊 Jami yuborildi: X email, Y telegram")

print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)

print("\n✅ Barcha foydalanuvchilarga bildirishnoma yuborildi!")
print("✅ Email va Telegram orqali xabar yetkazilmoqda")
print("✅ Browser notification ham ko'rinadi")
print()
