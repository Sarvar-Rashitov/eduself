import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add the missing translation
new_translation = {
    "Barcha fanlar": {
        "en": "All Subjects",
        "ru": "Все предметы",
        "kk": "Барлық пәндер",
        "kaa": "Барлық фанлар",
        "tg": "Ҳамаи фанҳо",
        "ky": "Бардык предметтер"
    },
    "fan": {
        "en": "subject",
        "ru": "предмет",
        "kk": "пән",
        "kaa": "фан",
        "tg": "фан",
        "ky": "предмет"
    }
}

# Merge with existing translations
translations.update(new_translation)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translation)} new translations")
print(f"📊 Total translations: {len(translations)}")
