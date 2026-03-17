#!/usr/bin/env python
"""
Test script for page-based load balancing translation system
"""
import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.translation import translator

def test_api_keys_loading():
    """Test 1: API keylarni yuklash"""
    print("=" * 60)
    print("TEST 1: API Keylarni Yuklash")
    print("=" * 60)
    
    print(f"✅ Yuklangan keylar soni: {len(translator.api_keys)}")
    
    if len(translator.api_keys) > 0:
        for i, key in enumerate(translator.api_keys, 1):
            print(f"   KEY_{i}: {key[:15]}...{key[-5:]}")
    else:
        print("❌ Hech qanday key topilmadi!")
    
    print()


def test_page_key_mapping():
    """Test 2: Har bir sahifa uchun key tanlash"""
    print("=" * 60)
    print("TEST 2: Sahifa → Key Mapping")
    print("=" * 60)
    
    pages = ['home', 'institutions', 'courses', 'subjects', 'mock_exams', 
             'certificates', 'profile', 'leaderboard', 'news', 'ai_assistant', 'oferta']
    
    for page in pages:
        key = translator._get_api_key_for_page(page)
        if key:
            key_display = f"{key[:15]}...{key[-5:]}"
        else:
            key_display = "None"
        
        # Find which key index this is
        key_index = translator.api_keys.index(key) + 1 if key in translator.api_keys else 0
        
        print(f"   {page:15} → KEY_{key_index} ({key_display})")
    
    print()


def test_translation_with_page():
    """Test 3: Sahifa bilan tarjima qilish"""
    print("=" * 60)
    print("TEST 3: Sahifa Bilan Tarjima")
    print("=" * 60)
    
    test_texts = [
        ("Salom", "home"),
        ("Matematika", "subjects"),
        ("TATU", "institutions"),
        ("IELTS", "certificates"),
    ]
    
    for text, page in test_texts:
        print(f"\n   Matn: '{text}'")
        print(f"   Sahifa: {page}")
        
        # Get key for this page
        key = translator._get_api_key_for_page(page)
        key_index = translator.api_keys.index(key) + 1 if key in translator.api_keys else 0
        print(f"   Ishlatilgan key: KEY_{key_index}")
        
        # Try translation (will use cache or API)
        try:
            result = translator.translate(text, 'uz', 'en', page_name=page)
            print(f"   ✅ Tarjima: '{result}'")
        except Exception as e:
            print(f"   ❌ Xatolik: {e}")
    
    print()


def test_cache():
    """Test 4: Cache ishlashini tekshirish"""
    print("=" * 60)
    print("TEST 4: Cache Ishlashi")
    print("=" * 60)
    
    from django.core.cache import cache
    
    # Test cache key generation
    test_text = "Test matn"
    cache_key = translator._get_cache_key(test_text, 'uz', 'en')
    print(f"   Cache key: {cache_key}")
    
    # Set test cache
    cache.set(cache_key, "Test translation", 60)
    cached_value = cache.get(cache_key)
    
    if cached_value:
        print(f"   ✅ Cache ishlayapti: '{cached_value}'")
    else:
        print(f"   ❌ Cache ishlamayapti")
    
    # Clean up
    cache.delete(cache_key)
    print()


def test_length_limits():
    """Test 5: Uzunlik limitlarini tekshirish"""
    print("=" * 60)
    print("TEST 5: Uzunlik Limitlari")
    print("=" * 60)
    
    short_text = "Qisqa matn"  # 10 chars
    medium_text = "Bu o'rtacha uzunlikdagi matn bo'lib, tarjima qilinishi kerak"  # ~60 chars
    long_text = "Bu juda uzun matn bo'lib, " * 10  # 200+ chars
    
    print(f"   Qisqa matn ({len(short_text)} chars): ", end="")
    result = translator.translate(short_text, 'uz', 'en', 'home')
    print(f"{'✅ Tarjima qilindi' if result != short_text else '⚠️ Original qaytarildi'}")
    
    print(f"   O'rtacha matn ({len(medium_text)} chars): ", end="")
    result = translator.translate(medium_text, 'uz', 'en', 'home')
    print(f"{'✅ Tarjima qilindi' if result != medium_text else '⚠️ Original qaytarildi'}")
    
    print(f"   Uzun matn ({len(long_text)} chars): ", end="")
    result = translator.translate(long_text, 'uz', 'en', 'home')
    print(f"{'✅ Tarjima qilindi' if result != long_text else '⚠️ Original qaytarildi (kutilgan)'}")
    
    print()


def main():
    """Barcha testlarni ishga tushirish"""
    print("\n" + "=" * 60)
    print("PAGE-BASED LOAD BALANCING TEST")
    print("=" * 60 + "\n")
    
    try:
        test_api_keys_loading()
        test_page_key_mapping()
        test_cache()
        test_length_limits()
        
        # Translation test (requires API key)
        if len(translator.api_keys) > 0:
            print("⚠️  Translation test API so'rov yuboradi va vaqt olishi mumkin...")
            response = input("Davom ettirishni xohlaysizmi? (yes/no): ")
            if response.lower() in ['yes', 'y', 'ha']:
                test_translation_with_page()
        
        print("=" * 60)
        print("✅ BARCHA TESTLAR TUGADI")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ XATOLIK: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
