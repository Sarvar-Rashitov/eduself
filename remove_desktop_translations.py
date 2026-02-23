#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

# Find all desktop templates
desktop_templates = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('_desktop.html'):
            desktop_templates.append(os.path.join(root, file))

print("=" * 70)
print("DESKTOP VERSIYALARDAN TARJIMA FUNKSIYASINI OLIB TASHLASH")
print("=" * 70)
print(f"\nTopilgan desktop shablonlar: {len(desktop_templates)}")

for template_path in desktop_templates:
    print(f"\nIshlanmoqda: {template_path}")
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Remove {% load translation_tags %}
        if '{% load translation_tags %}' in content:
            content = content.replace('{% load translation_tags %}', '')
            changes_made = True
            print("  - {% load translation_tags %} olib tashlandi")
        
        # Remove {% t "..." request.LANGUAGE_CODE %} and replace with original text
        pattern = r'{%\s*t\s+"([^"]+)"\s+request\.LANGUAGE_CODE\s*%}'
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                old_tag = f'{{% t "{match}" request.LANGUAGE_CODE %}}'
                content = content.replace(old_tag, match)
                changes_made = True
            print(f"  - {len(matches)} ta {{% t %}} tagi olib tashlandi")
        
        # Remove |translate:request.LANGUAGE_CODE filter
        pattern = r'\|\s*translate:request\.LANGUAGE_CODE'
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes_made = True
            print("  - |translate filtri olib tashlandi")
        
        # Remove |trans:request.LANGUAGE_CODE filter
        pattern = r'\|\s*trans:request\.LANGUAGE_CODE'
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes_made = True
            print("  - |trans filtri olib tashlandi")
        
        if changes_made:
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  ✓ Saqlandi")
        else:
            print("  - O'zgarishlar yo'q")
    
    except Exception as e:
        print(f"  ✗ Xato: {str(e)}")

print("\n" + "=" * 70)
print("TUGADI!")
print("=" * 70)
print("\nDesktop versiyalar endi faqat o'zbek tilida ishlaydi.")
