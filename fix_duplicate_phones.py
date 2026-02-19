#!/usr/bin/env python
"""
Duplicate phone raqamlarni tuzatish scripti
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from django.db.models import Count

# Duplicate phone raqamlarni topish
duplicates = User.objects.values('phone').annotate(count=Count('phone')).filter(count__gt=1, phone__isnull=False)

print(f"Topilgan duplicate phone raqamlar: {duplicates.count()}")

for dup in duplicates:
    phone = dup['phone']
    users = User.objects.filter(phone=phone).order_by('date_joined')
    
    print(f"\nPhone: {phone}")
    print(f"Foydalanuvchilar soni: {users.count()}")
    
    # Birinchi foydalanuvchidan boshqa barcha foydalanuvchilarning phone ni NULL qilish
    for i, user in enumerate(users):
        if i > 0:  # Birinchisidan boshqa
            print(f"  - {user.username} ({user.email or 'no email'}) - phone ni NULL qilish")
            user.phone = None
            user.save()
        else:
            print(f"  - {user.username} ({user.email or 'no email'}) - saqlanadi")

print("\n✅ Duplicate phone raqamlar tuzatildi!")
print("Endi 'python manage.py migrate' ni ishga tushiring")
