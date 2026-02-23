import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add the missing translation
new_translation = {
    "Fanlar": {
        "en": "Subjects",
        "ru": "Предметы",
        "kk": "Пәндер",
        "kaa": "Фанлар",
        "tg": "Фанҳо",
        "ky": "Предметтер"
    }
}

# Merge with existing translations
translations.update(new_translation)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translation)} new translation")
print(f"📊 Total translations: {len(translations)}")
