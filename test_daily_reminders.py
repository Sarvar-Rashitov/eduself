"""
Kunlik eslatma tizimini test qilish
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from django.utils import timezone
from datetime import timedelta

print("=" * 80)
print("KUNLIK ESLATMA TIZIMI TEST")
print("=" * 80)

# Bugungi kun boshlanishi
today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

# Bugun kirmagan foydalanuvchilar
inactive_today = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).exclude(
    last_login__gte=today_start
).exclude(email='')

print(f"\n📊 STATISTIKA:")
print(f"   Jami faol foydalanuvchilar: {User.objects.filter(is_active=True).count()}")
print(f"   Email tasdiqlangan: {User.objects.filter(is_active=True, email_verified=True).count()}")
print(f"   Bugun kirmagan: {inactive_today.count()}")

# Bugun kirgan foydalanuvchilar
active_today = User.objects.filter(
    is_active=True,
    last_login__gte=today_start
)
print(f"   Bugun kirgan: {active_today.count()}")

print("\n📋 BUGUN KIRMAGAN FOYDALANUVCHILAR (oxirgi 5 ta):")
for user in inactive_today[:5]:
    last_login_str = user.last_login.strftime('%d.%m.%Y %H:%M') if user.last_login else 'Hech qachon'
    print(f"\n   👤 {user.first_name} {user.last_name}")
    print(f"      Email: {user.email}")
    print(f"      Oxirgi kirish: {last_login_str}")

print("\n" + "=" * 80)
print("COMMANDLARNI ISHGA TUSHIRISH")
print("=" * 80)

print("\n🌅 ERTALABKI ESLATMA (07:00):")
print("   python manage.py send_daily_reminders --time=morning")

print("\n☀️ TUSHDAN KEYINGI ESLATMA (14:00):")
print("   python manage.py send_daily_reminders --time=afternoon")

print("\n" + "=" * 80)
print("CRON SOZLAMALARI")
print("=" * 80)

print("\n📝 Render.com da cron job qo'shish:")
print("\n   1. Render Dashboard > Cron Jobs")
print("   2. Yangi cron job yaratish:")
print("\n      Name: Daily Morning Reminder")
print("      Command: python manage.py send_daily_reminders --time=morning")
print("      Schedule: 0 7 * * * (har kuni 07:00)")
print("\n      Name: Daily Afternoon Reminder")
print("      Command: python manage.py send_daily_reminders --time=afternoon")
print("      Schedule: 0 14 * * * (har kuni 14:00)")

print("\n💡 ESLATMA:")
print("   - Foydalanuvchi soat 07:00 gacha kirsa, eslatma yuborilmaydi")
print("   - Soat 07:00 da eslatma yuboriladi (agar kirmagan bo'lsa)")
print("   - Soat 14:00 da yana eslatma yuboriladi (agar hali ham kirmagan bo'lsa)")
print("   - Emaillar eduselfuz@gmail.com dan yuboriladi")
print()
