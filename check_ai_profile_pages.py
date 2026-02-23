#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

# Pages to check
pages_to_check = [
    'templates/ai_assistant/chat.html',
    'templates/ai_assistant/help_center.html',
    'templates/accounts/profile.html',
    'templates/core/global_leaderboard.html',
]

# Pattern to find text that might need translation
pattern = r'>[^<{%]*[А-Яа-яЎўҚқҒғҲҳЁё\u04E8\u04E9\u0492\u0493\u049A\u049B\u04A2\u04A3\u04AE\u04AF\u04B0\u04B1\u04D8\u04D9\u04E8\u04E9][^<{%]*<'

print("=" * 70)
print("AI HAMROH VA PROFIL SAHIFALARI TAHLILI")
print("=" * 70)

for page in pages_to_check:
    if not os.path.exists(page):
        print(f"\nSahifa topilmadi: {page}")
        continue
    
    print(f"\n{page}")
    print("-" * 70)
    
    try:
        with open(page, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        untranslated_lines = []
        for i, line in enumerate(lines, 1):
            # Skip lines with translation tags
            if '{% t ' in line or '|translate' in line or '|trans' in line:
                continue
            
            # Find Cyrillic text
            matches = re.findall(pattern, line)
            for match in matches:
                text = match.strip('>< \n\t')
                # Skip template tags and variables
                if '{' in text or '%' in text or not text:
                    continue
                # Skip numbers only
                if re.match(r'^[\d\s\.,!?:;()\[\]{}«»"\']+$', text):
                    continue
                
                if text and len(text) > 2:
                    untranslated_lines.append((i, text[:80]))
        
        if untranslated_lines:
            print(f"Tarjima kerak: {len(untranslated_lines)} ta qator")
            for line_num, text in untranslated_lines[:15]:
                print(f"  Qator {line_num}: {text}")
            if len(untranslated_lines) > 15:
                print(f"  ... va yana {len(untranslated_lines) - 15} ta")
        else:
            print("Barcha matnlar tarjima qilingan!")
    
    except Exception as e:
        print(f"Xato: {str(e)}")

print("\n" + "=" * 70)
