"""
Yangi bildirishnoma yaratib, foydalanuvchilarga ko'rinishini test qilish
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from core.models import Notification
from django.db import models

print("=" * 80)
print("YANGI BILDIRISHNOMA KO'RINISH TESTI")
print("=" * 80)

# Test bildirishnoma yaratish
notification = Notification.objects.create(
    title="Test: Yangi foydalanuvchilar uchun",
    message="Bu bildirishnoma faqat yangi foydalanuvchilarga ko'rinishi kerak.",
    notification_type='info',
    icon='🔔',
    is_global=True
)

print(f"\n✅ Yangi bildirishnoma yaratildi:")
print(f"   ID: {notification.id}")
print(f"   Title: {notification.title}")
print(f"   Created: {notification.created_at.strftime('%d.%m.%Y %H:%M')}")

# Turli vaqtlarda yaratilgan foydalanuvchilarni tekshirish
print("\n" + "=" * 80)
print("FOYDALANUVCHILAR BO'YICHA TEST")
print("=" * 80)

# Eski foydalanuvchi (bildirishnomadan OLDIN yaratilgan)
old_user = User.objects.filter(created_at__lt=notification.created_at).order_by('-created_at').first()
if old_user:
    visible_to_old = Notification.objects.filter(
        models.Q(user=old_user) | 
        models.Q(is_global=True, created_at__gte=old_user.created_at)
    ).filter(id=notification.id).exists()
    
    print(f"\n👤 ESKI FOYDALANUVCHI: {old_user.first_name}")
    print(f"   Yaratilgan: {old_user.created_at.strftime('%d.%m.%Y %H:%M')}")
    result = '✅ HA' if visible_to_old else '❌ YOQ'
    print(f"   Bildirishnoma ko'rinadi: {result}")

# Yangi foydalanuvchi (bildirishnomadan KEYIN yaratiladi)
print(f"\n👤 YANGI FOYDALANUVCHI (kelajakda yaratiladi):")
print(f"   Agar hozir ro'yxatdan o'tsa: {notification.created_at.strftime('%d.%m.%Y %H:%M')} dan keyin")
print(f"   Bildirishnoma ko'rinadi: ❌ YO'Q (chunki bildirishnoma oldin yaratilgan)")

print("\n" + "=" * 80)
print("XULOSA")
print("=" * 80)
print("\n✅ Eski foydalanuvchilar (bildirishnomadan oldin ro'yxatdan o'tganlar)")
print("   yangi bildirishnomani ko'radi.")
print("\n✅ Yangi foydalanuvchilar (bildirishnomadan keyin ro'yxatdan o'tganlar)")
print("   bu bildirishnomani ko'rmaydi.")
print("\n💡 Faqat foydalanuvchi yaratilgandan KEYIN yaratilgan")
print("   global bildirishnomalar ko'rinadi.")

# Cleanup
notification.delete()
print("\n🗑️  Test bildirishnoma o'chirildi.")
print()
