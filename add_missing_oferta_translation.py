import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add the missing translation
missing_translation = {
    "Ushbu hujjat EduSelf platformasidan foydalanish shartlarini belgilaydi": {
        "en": "This document defines the terms of use of the EduSelf platform",
        "ru": "Данный документ определяет условия использования платформы EduSelf",
        "kk": "Бұл құжат EduSelf платформасын пайдалану шарттарын белгілейді",
        "kaa": "Бул ҳүжжет EduSelf платформасынан пайдаланыў шартларын белгилейди",
        "tg": "Ин ҳуҷҷат шартҳои истифодаи платформаи EduSelf-ро муайян мекунад",
        "ky": "Бул документ EduSelf платформасын пайдалануу шарттарын аныктайт"
    }
}

# Merge
translations.update(missing_translation)

# Write back
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added missing translation")
print(f"Total translations: {len(translations)}")
