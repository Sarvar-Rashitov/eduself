import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Additional translations
new_translations = {
    "Ma'lumotlar": {
        "en": "Data",
        "ru": "Данные",
        "kk": "Деректер",
        "kaa": "Мағлыўматлар",
        "tg": "Маълумот",
        "ky": "Маалымат"
    },
    "Ma'lumotlardan Foydalanish Maqsadlari": {
        "en": "Data Usage Purposes",
        "ru": "Цели использования данных",
        "kk": "Деректерді пайдалану мақсаттары",
        "kaa": "Мағлыўматлардан пайдаланыў мақсатлары",
        "tg": "Мақсадҳои истифодаи маълумот",
        "ky": "Маалыматты пайдалануу максаттары"
    }
}

# Merge with existing translations
translations.update(new_translations)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translations)} new translations")
print(f"📊 Total translations: {len(translations)}")
