#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

# Files that need translation_tags
files_to_fix = [
    'templates/accounts/profile.html',
    'templates/accounts/login.html',
    'templates/accounts/register.html',
    'templates/accounts/forgot_password.html',
    'templates/accounts/reset_password.html',
    'templates/ai_assistant/chat.html',
    'templates/ai_assistant/help_center.html',
    'templates/ai_assistant/institution_recommendations.html',
]

print("=" * 70)
print("BARCHA SAHIFALARGA {% load translation_tags %} QO'SHISH")
print("=" * 70)

for file_path in files_to_fix:
    if not os.path.exists(file_path):
        print(f"\n❌ Topilmadi: {file_path}")
        continue
    
    print(f"\n📄 Ishlanmoqda: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has translation_tags
        if '{% load translation_tags %}' in content:
            print("  ⏭️  {% load translation_tags %} allaqachon mavjud")
            continue
        
        # Find where to insert - after {% extends %} and {% load i18n %} and {% load static %}
        lines = content.split('\n')
        insert_index = 0
        
        for i, line in enumerate(lines):
            if '{% extends' in line:
                insert_index = i + 1
            elif '{% load i18n %}' in line:
                insert_index = i + 1
            elif '{% load static %}' in line:
                insert_index = i + 1
        
        # Insert the load tag
        lines.insert(insert_index, '{% load translation_tags %}')
        new_content = '\n'.join(lines)
        
        # Save
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("  ✅ {% load translation_tags %} qo'shildi")
    
    except Exception as e:
        print(f"  ❌ Xato: {str(e)}")

print("\n" + "=" * 70)
print("TUGADI!")
print("=" * 70)
