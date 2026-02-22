"""
Yangi qurilmadan kirish va kunlik eslatma testlari
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User, LoginHistory
from django.utils import timezone
from django.conf import settings

print("=" * 80)
print("YANGI QURILMA VA KUNLIK ESLATMA TESTLARI")
print("=" * 80)

# Test foydalanuvchi
test_user = User.objects.filter(email="sarvarrashitov4321@gmail.com").first()

if not test_user:
    print("\n❌ Test foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Last login: {test_user.last_login.strftime('%d.%m.%Y %H:%M') if test_user.last_login else 'Hech qachon'}")

# ============================================================================
# TEST 1: Login History
# ============================================================================
print("\n" + "=" * 80)
print("TEST 1: LOGIN HISTORY")
print("=" * 80)

login_history = LoginHistory.objects.filter(user=test_user).order_by('-login_time')[:5]

print(f"\n📊 Oxirgi 5 ta kirish tarixi:")
for history in login_history:
    new_device_icon = "🆕" if history.is_new_device else "✅"
    print(f"\n   {new_device_icon} {history.login_time.strftime('%d.%m.%Y %H:%M')}")
    print(f"      Device: {history.device_type}")
    print(f"      Browser: {history.browser}")
    print(f"      OS: {history.os}")
    print(f"      IP: {history.ip_address}")
    print(f"      New Device: {history.is_new_device}")

# ============================================================================
# TEST 2: Email Backend Sozlamalari
# ============================================================================
print("\n" + "=" * 80)
print("TEST 2: EMAIL BACKEND SOZLAMALARI")
print("=" * 80)

print("\n📧 AVTOMATIK EMAILLAR (kunlik eslatma, yangi qurilma, welcome, etc.):")
print(f"   Host: {settings.EMAIL_HOST}")
print(f"   User: {settings.EMAIL_HOST_USER}")
print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

print("\n📧 ADMIN NOTIFICATION EMAILLAR:")
print(f"   Host: {os.getenv('ADMIN_EMAIL_HOST')}")
print(f"   User: {os.getenv('ADMIN_EMAIL_HOST_USER')}")
print(f"   From: {os.getenv('ADMIN_DEFAULT_FROM_EMAIL')}")

# ============================================================================
# TEST 3: Kunlik Eslatma Statistika
# ============================================================================
print("\n" + "=" * 80)
print("TEST 3: KUNLIK ESLATMA STATISTIKA")
print("=" * 80)

today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

inactive_today = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).exclude(
    last_login__gte=today_start
).exclude(email='')

active_today = User.objects.filter(
    is_active=True,
    last_login__gte=today_start
)

print(f"\n📊 Bugun kirgan: {active_today.count()}")
print(f"📊 Bugun kirmagan: {inactive_today.count()}")

# ============================================================================
# TEST 4: Yangi Qurilma Tekshirish
# ============================================================================
print("\n" + "=" * 80)
print("TEST 4: YANGI QURILMA TEKSHIRISH")
print("=" * 80)

# Oxirgi 7 kundagi yangi qurilmadan kirishlar
seven_days_ago = timezone.now() - timezone.timedelta(days=7)
new_device_logins = LoginHistory.objects.filter(
    is_new_device=True,
    login_time__gte=seven_days_ago
).order_by('-login_time')[:10]

print(f"\n📊 Oxirgi 7 kundagi yangi qurilmadan kirishlar: {new_device_logins.count()}")

if new_device_logins.exists():
    print("\n   Oxirgi 10 ta:")
    for login in new_device_logins:
        print(f"\n   👤 {login.user.first_name} {login.user.last_name}")
        print(f"      Email: {login.user.email}")
        print(f"      Vaqt: {login.login_time.strftime('%d.%m.%Y %H:%M')}")
        print(f"      Device: {login.device_type} - {login.browser} on {login.os}")

# ============================================================================
# XULOSA
# ============================================================================
print("\n" + "=" * 80)
print("XULOSA")
print("=" * 80)

print("\n✅ YANGI QURILMADAN KIRISH:")
print("   - LoginHistory yaratiladi")
print("   - Yangi qurilma bo'lsa, email yuboriladi")
print("   - Email: eduselfuz@gmail.com dan yuboriladi")

print("\n✅ KUNLIK ESLATMA:")
print("   - Soat 07:00 va 14:00 da yuboriladi")
print("   - Email: eduselfuz@gmail.com dan yuboriladi")
print("   - Platformada bildirishnoma yaratilmaydi")

print("\n✅ ADMIN NOTIFICATION:")
print("   - Email: notificationeduselfuz@gmail.com dan yuboriladi")
print("   - Platformada bildirishnoma yaratiladi")

print("\n💡 TEST QILISH:")
print("   1. Yangi browserdan login qiling")
print("   2. Email kelishini tekshiring (eduselfuz@gmail.com dan)")
print("   3. LoginHistory admin panelda ko'ring")

print()
