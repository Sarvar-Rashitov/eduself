#!/usr/bin/env python
"""
Bo'sh phone raqamlarni NULL qilish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.db import connection

# Bo'sh phone raqamlarni NULL qilish
with connection.cursor() as cursor:
    cursor.execute("""
        UPDATE accounts_user
        SET phone = NULL
        WHERE phone = '' OR phone IS NULL
    """)
    
    print(f"✅ {cursor.rowcount} ta foydalanuvchining bo'sh phone ni NULL qilindi")

print("\nEndi 'python manage.py migrate' ni ishga tushiring")
