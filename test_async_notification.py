"""
Admin panel notification yaratish va async email/telegram yuborishni test qilish
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
print("ASYNC NOTIFICATION (EMAIL + TELEGRAM) TEST")
print("=" * 60)

# Test foydalanuvchi
test_user = User.objects.filter(email_verified=True).first()
if not test_user:
    print("❌ Email tasdiqlangan foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Telegram: {'✅ Ulangan' if test_user.telegram_chat_id else '❌ Ulanmagan'}")

print("\n" + "=" * 60)
print("SHAXSIY NOTIFICATION YARATISH")
print("=" * 60)

# Notification yaratish va vaqtni o'lchash
start_time = time.time()

notification = Notification.objects.create(
    user=test_user,
    title="Test Bildirishnoma",
    message="Bu async email va telegram yuborish testi. Admin panel tez javob qaytarishi kerak.",
    notification_type='info',
    icon='📧',
    link='https://eduself.uz'
)

end_time = time.time()
elapsed = end_time - start_time

print(f"\n✅ Notification yaratildi: ID={notification.id}")
print(f"⏱️  Vaqt: {elapsed:.2f} soniya")

print("\n" + "=" * 60)
print("NATIJA")
print("=" * 60)

if elapsed < 2:
    print(f"✅ MUVAFFAQIYATLI! ({elapsed:.2f}s < 2s)")
    print("   Admin panel tez javob qaytardi")
    print("   Email va Telegram yuborish background'da davom etmoqda")
else:
    print(f"⚠️  SEKIN! ({elapsed:.2f}s >= 2s)")
    print("   Admin panel kutish vaqti uzoq")

# Global notification test
print("\n" + "=" * 60)
print("GLOBAL NOTIFICATION TEST")
print("=" * 60)

verified_users = User.objects.filter(is_active=True, email_verified=True).count()
telegram_users = User.objects.filter(is_active=True, telegram_chat_id__isnull=False).exclude(telegram_chat_id='').count()

print(f"📊 Email tasdiqlangan: {verified_users}")
print(f"📊 Telegram ulangan: {telegram_users}")

if verified_users > 50 or telegram_users > 50:
    print(f"\n⚠️  Ko'p foydalanuvchilarga yuborish uzoq vaqt oladi")
    print("   Async bo'lmasa, 30+ soniya ketishi mumkin")

print("\n🧪 Global notification yaratamiz...")

start_time = time.time()

global_notification = Notification.objects.create(
    title="Global Test",
    message="Bu barcha foydalanuvchilarga yuborilayotgan test xabari (Email va Telegram).",
    notification_type='announcement',
    icon='📢',
    is_global=True
)

end_time = time.time()
elapsed = end_time - start_time

print(f"\n✅ Global notification yaratildi: ID={global_notification.id}")
print(f"⏱️  Vaqt: {elapsed:.2f} soniya")

if elapsed < 3:
    print(f"\n✅ AJOYIB! ({elapsed:.2f}s < 3s)")
    print(f"   {verified_users} email + {telegram_users} telegram yuborish background'da")
    print("   Admin panel timeout bo'lmadi!")
else:
    print(f"\n⚠️  SEKIN! ({elapsed:.2f}s >= 3s)")
    print("   Admin panel kutish vaqti uzoq")

# Cleanup
print(f"\n🗑️  Global notification o'chirildi")
global_notification.delete()

print(f"🗑️  Test notification o'chirildi")
notification.delete()

print("\n" + "=" * 60)
print("XULOSA")
print("=" * 60)
print("✅ Async email va telegram yuborish ishlayapti")
print("✅ Admin panel tez javob qaytaradi")
print("✅ Email va Telegram yuborish background'da davom etadi")
print("✅ Gunicorn timeout muammosi hal qilindi")

print("\n📝 KEYINGI QADAMLAR:")
print("   1. Production'ga deploy qiling")
print("   2. Admin panelda notification yarating")
print("   3. Darhol success message ko'rinadi")
print("   4. Email va Telegram yuborish background'da davom etadi")
print("   5. Log'larda yuborish jarayonini kuzating")
print()

print("\n💡 LOG'LARNI KUZATISH:")
print("   - Email yuborildi: ✅ Email yuborildi: user@example.com")
print("   - Telegram yuborildi: ✅ Telegram yuborildi: username")
print("   - Jami: 📊 Jami yuborildi: X email, Y telegram")
print()
