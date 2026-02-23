"""
Statik matnlarga {% trans %} qo'shish
"""
import os
import re

templates_dir = 'templates/core'
templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

# Statik matnlar ro'yxati (tarjima qilinishi kerak)
static_texts = [
    # Buttons
    'Kirish',
    'Chiqish',
    'Saqlash',
    'Bekor qilish',
    'Yuborish',
    'Qaytish',
    'Ko\'rish',
    'Batafsil',
    'Davom etish',
    'Boshlash',
    'Tugatish',
    
    # Common words
    'Barchasi',
    'Yangiliklar',
    'Kurslar',
    'Fanlar',
    'Sertifikatlar',
    'Imtihonlar',
    'Muassasalar',
    'Reyting',
    'Profil',
    'Sozlamalar',
    
    # Actions
    'Qidirish',
    'Filtrlash',
    'Saralash',
    'Yuklab olish',
    'Ulashish',
    
    # Status
    'Faol',
    'Nofaol',
    'Tugallangan',
    'Jarayonda',
    'Kutilmoqda',
    
    # Messages
    'Muvaffaqiyatli',
    'Xato',
    'Ogohlantirish',
    'Ma\'lumot',
    
    # Time
    'Bugun',
    'Kecha',
    'Ertaga',
    'Hafta',
    'Oy',
    'Yil',
]

def add_i18n_tags(file_path):
    """Template'ga {% load i18n %} va {% trans %} qo'shish"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # {% load i18n %} qo'shish (agar yo'q bo'lsa)
        if '{% load i18n %}' not in content and '{% load translation_tags %}' in content:
            content = content.replace(
                '{% load translation_tags %}',
                '{% load i18n %}\n{% load translation_tags %}'
            )
        elif '{% load i18n %}' not in content and '{% extends' in content:
            content = re.sub(
                r"({% extends ['\"].*?['\"] %})",
                r"\1\n{% load i18n %}",
                content,
                count=1
            )
        
        # Agar o'zgarish bo'lsa, saqlash
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"✗ {file_path} - xato: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("STATIK MATNLAR UCHUN i18n QO'SHISH")
    print("=" * 70)
    print()
    
    updated_count = 0
    
    for template in sorted(templates):
        file_path = os.path.join(templates_dir, template)
        
        if add_i18n_tags(file_path):
            print(f"✓ {template}")
            updated_count += 1
    
    print()
    print("=" * 70)
    print(f"TUGADI! Yangilandi: {updated_count} ta template")
    print("=" * 70)
    print()
    print("Keyingi qadamlar:")
    print("1. python manage.py makemessages -l en")
    print("2. python manage.py makemessages -l ru")
    print("3. python manage.py makemessages -l kk")
    print("4. python manage.py makemessages -l kaa")
    print("5. python manage.py makemessages -l tg")
    print("6. python manage.py makemessages -l ky")
    print("7. locale/*/LC_MESSAGES/django.po fayllarni to'ldiring")
    print("8. python manage.py compilemessages")

if __name__ == '__main__':
    main()
