"""
Google login email testlari
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User

print("=" * 80)
print("GOOGLE LOGIN EMAIL TESTLARI")
print("=" * 80)

# Test uchun Google foydalanuvchilarni ko'rsatish
google_users = User.objects.filter(google_id__isnull=False).order_by('-created_at')[:5]

print(f"\n📊 Jami Google foydalanuvchilar: {User.objects.filter(google_id__isnull=False).count()}")
print(f"\n📋 Oxirgi 5 ta Google foydalanuvchi:")

for user in google_users:
    print(f"\n   👤 {user.first_name} {user.last_name}")
    print(f"      Email: {user.email}")
    print(f"      Google ID: {user.google_id[:20]}...")
    print(f"      Email verified: {user.email_verified}")
    print(f"      Created: {user.created_at.strftime('%d.%m.%Y %H:%M')}")

print("\n" + "=" * 80)
print("TEST QILISH UCHUN:")
print("=" * 80)
print("\n1. Browserda Google bilan login qiling")
print("2. Yangi foydalanuvchi bo'lsa - Welcome email kelishi kerak")
print("3. Mavjud foydalanuvchi yangi qurilmadan kirsa - New device email kelishi kerak")
print("\n💡 Emaillar eduselfuz@gmail.com dan keladi")
print()
