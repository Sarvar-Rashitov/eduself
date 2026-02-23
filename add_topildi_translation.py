import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add the missing translation
new_translation = {
    "topildi": {
        "en": "found",
        "ru": "найдено",
        "kk": "табылды",
        "kaa": "табылды",
        "tg": "ёфт шуд",
        "ky": "табылды"
    },
    "Qidiruv bo'yicha muassasa topilmadi": {
        "en": "No institutions found by search",
        "ru": "По поиску учреждения не найдены",
        "kk": "Іздеу бойынша мекемелер табылмады",
        "kaa": "Излеў бойынша муассасалар табылмады",
        "tg": "Аз рӯи ҷустуҷӯ муассисаҳо ёфт нашуданд",
        "ky": "Издөө боюнча мекемелер табылган жок"
    }
}

# Merge with existing translations
translations.update(new_translation)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translation)} new translations")
print(f"📊 Total translations: {len(translations)}")
