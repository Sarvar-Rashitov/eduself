"""
Test static translations implementation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.templatetags.translation_tags import trans, t
import json

# Load static translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    TRANSLATIONS = json.load(f)

print("=" * 70)
print("STATIC TRANSLATIONS TEST")
print("=" * 70)
print()

# Test languages
languages = ['uz', 'en', 'ru', 'kk', 'kaa', 'tg', 'ky']

# Test some common texts
test_texts = [
    "Bosh sahifa",
    "Fanlar",
    "Sertifikatlar",
    "Kirish",
    "Chiqish",
    "Barchasi",
    "Yangiliklar",
    "Kurslar",
    "Mashhur kurslar",
    "Barcha kurslar"
]

print("Testing static translations:")
print("-" * 70)

for text in test_texts:
    print(f"\n'{text}':")
    for lang in languages:
        translated = trans(text, lang)
        status = "✓" if translated != text or lang == 'uz' else "✗"
        print(f"  {status} {lang}: {translated}")

print()
print("=" * 70)
print("TRANSLATION STATISTICS")
print("=" * 70)
print(f"Total static translations: {len(TRANSLATIONS)}")
print(f"Languages supported: {len(languages)}")
print(f"Total translation entries: {len(TRANSLATIONS) * len(languages)}")
print()

# Check coverage
print("Translation coverage:")
for lang in languages:
    count = 0
    for text, translations in TRANSLATIONS.items():
        if lang in translations:
            count += 1
    coverage = (count / len(TRANSLATIONS)) * 100
    print(f"  {lang}: {count}/{len(TRANSLATIONS)} ({coverage:.1f}%)")

print()
print("=" * 70)
print("TEST COMPLETED!")
print("=" * 70)
