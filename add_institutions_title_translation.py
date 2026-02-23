import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add the missing translation
new_translation = {
    "Barcha ta'lim muassasalari": {
        "en": "All Educational Institutions",
        "ru": "Все образовательные учреждения",
        "kk": "Барлық білім беру мекемелері",
        "kaa": "Барлық билим бериў муассасалары",
        "tg": "Ҳамаи муассисаҳои таҳсилӣ",
        "ky": "Бардык билим берүү мекемелери"
    }
}

# Merge with existing translations
translations.update(new_translation)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added 1 new translation")
print(f"📊 Total translations: {len(translations)}")
