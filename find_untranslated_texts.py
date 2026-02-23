"""
Barcha template'larda tarjima qilinmagan matnlarni topish
"""
import os
import re
from collections import defaultdict

templates_dir = 'templates/core'
templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

# Tarjima qilinmagan matnlarni saqlash
untranslated = defaultdict(list)

# Tarjima teglarini tekshirish
translation_pattern = re.compile(r'{%\s*t\s+"([^"]+)"\s+request\.LANGUAGE_CODE\s*%}')
filter_pattern = re.compile(r'\|\s*trans:request\.LANGUAGE_CODE')

# Oddiy matnlarni topish (HTML teglar ichida)
text_patterns = [
    re.compile(r'<h[1-6][^>]*>([^<{]+)</h[1-6]>'),  # Headers
    re.compile(r'<p[^>]*>([^<{]+)</p>'),  # Paragraphs
    re.compile(r'<span[^>]*>([^<{]+)</span>'),  # Spans
    re.compile(r'<button[^>]*>([^<{]+)</button>'),  # Buttons
    re.compile(r'<a[^>]*>([^<{]+)</a>'),  # Links
    re.compile(r'<label[^>]*>([^<{]+)</label>'),  # Labels
    re.compile(r'<div[^>]*class="[^"]*label[^"]*"[^>]*>([^<{]+)</div>'),  # Divs with label class
]

print("=" * 70)
print("TARJIMA QILINMAGAN MATNLARNI TOPISH")
print("=" * 70)
print()

for template in sorted(templates):
    file_path = os.path.join(templates_dir, template)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tarjima qilingan matnlarni topish
        translated_texts = set(translation_pattern.findall(content))
        
        # Barcha matnlarni topish
        all_texts = set()
        for pattern in text_patterns:
            matches = pattern.findall(content)
            for match in matches:
                text = match.strip()
                # Faqat o'zbek harflari bo'lgan matnlarni olish
                if text and len(text) > 2 and not text.startswith('{{') and not text.startswith('{%'):
                    # Raqamlar va belgilarni olib tashlash
                    if any(c.isalpha() for c in text):
                        all_texts.add(text)
        
        # Tarjima qilinmagan matnlarni topish
        not_translated = all_texts - translated_texts
        
        if not_translated:
            untranslated[template] = sorted(not_translated)
            print(f"\n📄 {template}")
            print(f"   Tarjima qilinmagan: {len(not_translated)} ta")
            for text in sorted(not_translated)[:10]:  # Faqat birinchi 10 tasini ko'rsatish
                print(f"   - {text[:60]}...")
            if len(not_translated) > 10:
                print(f"   ... va yana {len(not_translated) - 10} ta")
    
    except Exception as e:
        print(f"✗ {template} - xato: {str(e)}")

print()
print("=" * 70)
print("XULOSA")
print("=" * 70)
print(f"Tekshirilgan fayllar: {len(templates)}")
print(f"Tarjima kerak bo'lgan fayllar: {len(untranslated)}")

total_untranslated = sum(len(texts) for texts in untranslated.values())
print(f"Jami tarjima qilinmagan matnlar: {total_untranslated}")
print()

# Eng ko'p tarjima kerak bo'lgan fayllar
if untranslated:
    print("Eng ko'p tarjima kerak bo'lgan fayllar:")
    sorted_files = sorted(untranslated.items(), key=lambda x: len(x[1]), reverse=True)
    for filename, texts in sorted_files[:10]:
        print(f"  {filename}: {len(texts)} ta")
