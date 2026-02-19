#!/usr/bin/env python
"""
SQL orqali duplicate phone raqamlarni tuzatish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.db import connection

# Duplicate phone raqamlarni topish va tuzatish
with connection.cursor() as cursor:
    # Duplicate phone raqamlarni topish
    cursor.execute("""
        SELECT phone, COUNT(*) as count
        FROM accounts_user
        WHERE phone IS NOT NULL AND phone != ''
        GROUP BY phone
        HAVING COUNT(*) > 1
    """)
    
    duplicates = cursor.fetchall()
    print(f"Topilgan duplicate phone raqamlar: {len(duplicates)}")
    
    for phone, count in duplicates:
        print(f"\nPhone: {phone} - {count} ta foydalanuvchi")
        
        # Eng eski foydalanuvchidan boshqa barcha foydalanuvchilarning phone ni NULL qilish
        cursor.execute("""
            UPDATE accounts_user
            SET phone = NULL
            WHERE phone = %s
            AND id NOT IN (
                SELECT id FROM accounts_user
                WHERE phone = %s
                ORDER BY date_joined ASC
                LIMIT 1
            )
        """, [phone, phone])
        
        print(f"  ✅ {cursor.rowcount} ta foydalanuvchining phone ni NULL qilindi")

print("\n✅ Barcha duplicate phone raqamlar tuzatildi!")
print("Endi 'python manage.py makemigrations' va 'python manage.py migrate' ni ishga tushiring")
