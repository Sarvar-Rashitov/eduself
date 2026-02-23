import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add the missing translation
new_translation = {
    "Barcha Mock Imtihonlar": {
        "en": "All Mock Exams",
        "ru": "Все пробные экзамены",
        "kk": "Барлық сынақ емтихандар",
        "kaa": "Барлық сынақ имтиханлар",
        "tg": "Ҳамаи имтиҳонҳои санҷишӣ",
        "ky": "Бардык сыноо экзамендер"
    },
    "ta imtihon": {
        "en": "exams",
        "ru": "экзаменов",
        "kk": "емтихан",
        "kaa": "имтихан",
        "tg": "имтиҳон",
        "ky": "экзамен"
    }
}

# Merge with existing translations
translations.update(new_translation)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translation)} new translations")
print(f"📊 Total translations: {len(translations)}")
