"""
Test translation system
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.translation import translator

# Test matnlar
test_texts = {
    'uz': "Salom, bu test matni. Platformamizga xush kelibsiz!",
    'en': "Hello, this is a test text. Welcome to our platform!",
    'ru': "Привет, это тестовый текст. Добро пожаловать на нашу платформу!",
}

print("=" * 80)
print("TRANSLATION SYSTEM TEST")
print("=" * 80)

# O'zbek matnni boshqa tillarga tarjima qilish
print("\n1. O'zbek matnni tarjima qilish:")
print(f"Original (uz): {test_texts['uz']}")
print()

for target_lang in ['en', 'ru', 'kk', 'kaa', 'tg', 'ky']:
    translated = translator.translate(test_texts['uz'], 'uz', target_lang)
    print(f"→ {target_lang.upper()}: {translated}")

print("\n" + "=" * 80)
print("\n2. Ingliz matnni tarjima qilish:")
print(f"Original (en): {test_texts['en']}")
print()

for target_lang in ['uz', 'ru', 'kk']:
    translated = translator.translate(test_texts['en'], 'en', target_lang)
    print(f"→ {target_lang.upper()}: {translated}")

print("\n" + "=" * 80)
print("\n3. Cache test - bir xil matnni qayta tarjima qilish:")
import time

start = time.time()
result1 = translator.translate(test_texts['uz'], 'uz', 'en')
time1 = time.time() - start

start = time.time()
result2 = translator.translate(test_texts['uz'], 'uz', 'en')
time2 = time.time() - start

print(f"Birinchi tarjima: {time1:.3f}s")
print(f"Ikkinchi tarjima (cache): {time2:.3f}s")
print(f"Cache tezligi: {time1/time2:.1f}x tezroq")

print("\n" + "=" * 80)
print("TEST TUGADI!")
print("=" * 80)
