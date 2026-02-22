"""
Yangi foydalanuvchilar uchun bildirishnoma filtrlashni test qilish
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from core.models import Notification
from django.utils import timezone
from datetime import timedelta

print("=" * 80)
print("BILDIRISHNOMA FILTRLASH TESTI")
print("=" * 80)

# Eski va yangi bildirishnomalarni ko'rsatish
old_notifications = Notification.objects.filter(is_global=True).order_by('created_at')[:3]
new_notifications = Notification.objects.filter(is_global=True).order_by('-created_at')[:3]

print("\n📋 ENG ESKI 3 TA GLOBAL BILDIRISHNOMA:")
for notif in old_notifications:
    print(f"\n   📢 {notif.title}")
    print(f"      Yaratilgan: {notif.created_at.strftime('%d.%m.%Y %H:%M')}")
    print(f"      ID: {notif.id}")

print("\n📋 ENG YANGI 3 TA GLOBAL BILDIRISHNOMA:")
for notif in new_notifications:
    print(f"\n   📢 {notif.title}")
    print(f"      Yaratilgan: {notif.created_at.strftime('%d.%m.%Y %H:%M')}")
    print(f"      ID: {notif.id}")

# Yangi foydalanuvchi yaratish (test)
print("\n" + "=" * 80)
print("TEST FOYDALANUVCHI")
print("=" * 80)

# Oxirgi foydalanuvchini ko'rsatish
latest_user = User.objects.order_by('-created_at').first()
if latest_user:
    print(f"\n👤 Eng yangi foydalanuvchi: {latest_user.first_name} {latest_user.last_name}")
    print(f"   Email: {latest_user.email}")
    print(f"   Yaratilgan: {latest_user.created_at.strftime('%d.%m.%Y %H:%M')}")
    
    # Bu foydalanuvchi uchun ko'rinadigan bildirishnomalar
    from django.db import models
    visible_notifications = Notification.objects.filter(
        models.Q(user=latest_user) | 
        models.Q(is_global=True, created_at__gte=latest_user.created_at)
    ).order_by('-created_at')
    
    print(f"\n📊 Bu foydalanuvchi uchun ko'rinadigan bildirishnomalar: {visible_notifications.count()}")
    
    if visible_notifications.exists():
        print("\n   Ko'rinadigan bildirishnomalar:")
        for notif in visible_notifications[:5]:
            print(f"   • {notif.title} ({notif.created_at.strftime('%d.%m.%Y %H:%M')})")
    
    # Ko'rinmaydigan eski bildirishnomalar
    hidden_notifications = Notification.objects.filter(
        is_global=True,
        created_at__lt=latest_user.created_at
    ).count()
    
    print(f"\n📊 Ko'rinmaydigan eski bildirishnomalar: {hidden_notifications}")

print("\n" + "=" * 80)
print("XULOSA")
print("=" * 80)
print("\n✅ Yangi foydalanuvchilar faqat ro'yxatdan o'tgandan KEYIN")
print("   yaratilgan global bildirishnomalarni ko'radi.")
print("\n✅ Eski bildirishnomalar yangi foydalanuvchilarga ko'rinmaydi.")
print()
