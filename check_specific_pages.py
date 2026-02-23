#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json

# Load translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Pages to check
pages_to_check = [
    'templates/core/home.html',
    'templates/core/subjects.html',
    'templates/core/mock_exams.html',
    'templates/core/institutions.html',
    'templates/core/institution_detail.html',
    'templates/core/global_leaderboard.html',
]

# Pattern to find untranslated text
pattern = r'>[^<{%]*[А-Яа-яЎўҚқҒғҲҳЁё\u04E8\u04E9\u0492\u0493\u049A\u049B\u04A2\u04A3\u04AE\u04AF\u04B0\u04B1\u04D8\u04D9\u04E8\u04E9][^<{%]*<'

print("=" * 70)
print("ASOSIY SAHIFALAR TAHLILI")
print("=" * 70)

for page in pages_to_check:
    if not os.path.exists(page):
        print(f"\nSahifa topilmadi: {page}")
        continue
    
    print(f"\n{page}")
    print("-" * 70)
    
    try:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find untranslated texts
        matches = re.findall(pattern, content)
        
        untranslated = []
        for match in matches:
            text = match.strip('>< \n\t')
            # Skip if it's a template tag or variable
            if '{' in text or '%' in text or not text:
                continue
            # Skip if already translated
            if '{% t ' in match or '|translate' in match or '|trans' in match:
                continue
            # Skip numbers and symbols only
            if re.match(r'^[\d\s\.,!?:;()\[\]{}«»"\']+$', text):
                continue
            
            if text and len(text) > 2:
                untranslated.append(text[:80])
        
        if untranslated:
            print(f"Tarjima kerak: {len(untranslated)} ta")
            for i, text in enumerate(untranslated[:10], 1):
                print(f"  {i}. {text}")
            if len(untranslated) > 10:
                print(f"  ... va yana {len(untranslated) - 10} ta")
        else:
            print("Barcha matnlar tarjima qilingan!")
    
    except Exception as e:
        print(f"Xato: {str(e)}")

print("\n" + "=" * 70)
print("TAHLIL TUGADI")
print("=" * 70)
