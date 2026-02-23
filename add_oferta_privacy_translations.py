import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# New translations for oferta and privacy pages
new_translations = {
    "Ommaviy Oferta": {
        "en": "Public Offer",
        "ru": "Публичная оферта",
        "kk": "Жария оферта",
        "kaa": "Жәрия оферта",
        "tg": "Пешниҳоди умумӣ",
        "ky": "Жалпы сунуш"
    },
    "Xizmat ko'rsatish shartlari": {
        "en": "Terms of Service",
        "ru": "Условия предоставления услуг",
        "kk": "Қызмет көрсету шарттары",
        "kaa": "Хызмет көрсетиў шартлары",
        "tg": "Шартҳои пешниҳоди хидмат",
        "ky": "Кызмат көрсөтүү шарттары"
    },
    "Maxfiylik siyosati": {
        "en": "Privacy Policy",
        "ru": "Политика конфиденциальности",
        "kk": "Құпиялылық саясаты",
        "kaa": "Құпиялылық саясаты",
        "tg": "Сиёсати махфият",
        "ky": "Купуялуулук саясаты"
    },
    "Umumiy qoidalar": {
        "en": "General Rules",
        "ru": "Общие правила",
        "kk": "Жалпы ережелер",
        "kaa": "Умумий қағыйдалар",
        "tg": "Қоидаҳои умумӣ",
        "ky": "Жалпы эрежелер"
    },
    "Xizmatlar": {
        "en": "Services",
        "ru": "Услуги",
        "kk": "Қызметтер",
        "kaa": "Хызметлер",
        "tg": "Хидматҳо",
        "ky": "Кызматтар"
    },
    "Foydalanuvchi majburiyatlari": {
        "en": "User Obligations",
        "ru": "Обязанности пользователя",
        "kk": "Пайдаланушы міндеттері",
        "kaa": "Пайдаланыўшы мәжбүриятлары",
        "tg": "Уҳдадориҳои корбар",
        "ky": "Колдонуучунун милдеттери"
    },
    "Shaxsiy ma'lumotlar": {
        "en": "Personal Information",
        "ru": "Личные данные",
        "kk": "Жеке ақпарат",
        "kaa": "Жеке мағлыўматлар",
        "tg": "Маълумоти шахсӣ",
        "ky": "Жеке маалымат"
    },
    "Ma'lumotlarni himoya qilish": {
        "en": "Data Protection",
        "ru": "Защита данных",
        "kk": "Деректерді қорғау",
        "kaa": "Мағлыўматларды қорғаў",
        "tg": "Ҳифзи маълумот",
        "ky": "Маалыматты коргоо"
    },
    "Aloqa": {
        "en": "Contact",
        "ru": "Контакты",
        "kk": "Байланыс",
        "kaa": "Байланыс",
        "tg": "Тамос",
        "ky": "Байланыш"
    }
}

# Merge with existing translations
translations.update(new_translations)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translations)} new translations")
print(f"📊 Total translations: {len(translations)}")
