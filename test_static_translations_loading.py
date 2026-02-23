"""
Test script to verify static translations are loading correctly
"""
import json
import os

# Test loading static translations
print("Testing static translations loading...")
print("=" * 60)

# Try different paths
possible_paths = [
    'static_translations.json',
    os.path.join('..', 'static_translations.json'),
    os.path.join(os.path.dirname(__file__), 'static_translations.json'),
]

for path in possible_paths:
    print(f"\nTrying path: {path}")
    if os.path.exists(path):
        print(f"✅ File exists at: {os.path.abspath(path)}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
            print(f"✅ Loaded {len(translations)} translations")
            
            # Test some oferta translations
            test_keys = [
                "Ushbu hujjat EduSelf platformasidan foydalanish shartlarini belgilaydi",
                "Platformaga ro'yxatdan o'tish orqali siz ushbu Oferta shartlarini to'liq qabul qilasiz.",
                "Online testlar va imtihonlar",
                "Platforma quyidagi xizmatlarni taqdim etadi:",
            ]
            
            print("\nTesting oferta translations:")
            for key in test_keys:
                if key in translations:
                    print(f"✅ Found: {key[:50]}...")
                    print(f"   EN: {translations[key].get('en', 'N/A')[:50]}...")
                else:
                    print(f"❌ Missing: {key[:50]}...")
            
            break
        except Exception as e:
            print(f"❌ Error loading: {e}")
    else:
        print(f"❌ File not found")

print("\n" + "=" * 60)
print("Test complete!")
