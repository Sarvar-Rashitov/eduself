import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Missing translations from the pages mentioned
new_translations = {
    "Oxirgi ishlangan test": {
        "en": "Last test taken",
        "ru": "Последний пройденный тест",
        "kk": "Соңғы тапсырылған тест",
        "kaa": "Соңғы тапсырылған тест",
        "tg": "Тести охирин гузаронидашуда",
        "ky": "Акыркы тапшырылган тест"
    },
    "Barcha fanlar": {
        "en": "All subjects",
        "ru": "Все предметы",
        "kk": "Барлық пәндер",
        "kaa": "Барлық пәндер",
        "tg": "Ҳамаи фанҳо",
        "ky": "Бардык предметтер"
    },
    "Barcha Mock Imtihonlar": {
        "en": "All Mock Exams",
        "ru": "Все пробные экзамены",
        "kk": "Барлық сынақ емтихандар",
        "kaa": "Барлық сынақ имтихан лар",
        "tg": "Ҳамаи имтиҳонҳои санҷишӣ",
        "ky": "Бардык сыноо экзамендер"
    },
    "Barcha muassasalar": {
        "en": "All institutions",
        "ru": "Все учреждения",
        "kk": "Барлық мекемелер",
        "kaa": "Барлық муассасалар",
        "tg": "Ҳамаи муассисаҳо",
        "ky": "Бардык мекемелер"
    },
    "Barcha ta'lim muassasalari": {
        "en": "All educational institutions",
        "ru": "Все образовательные учреждения",
        "kk": "Барлық білім беру мекемелері",
        "kaa": "Барлық білім беру муассасалары",
        "tg": "Ҳамаи муассисаҳои таҳсилӣ",
        "ky": "Бардык билим берүү мекемелери"
    },
    "Yo'nalishlar": {
        "en": "Directions",
        "ru": "Направления",
        "kk": "Бағыттар",
        "kaa": "Бағыттар",
        "tg": "Самтҳо",
        "ky": "Багыттар"
    },
    "Kontrakt narxi": {
        "en": "Contract price",
        "ru": "Цена контракта",
        "kk": "Контракт бағасы",
        "kaa": "Контракт бағасы",
        "tg": "Нархи шартнома",
        "ky": "Контракт баасы"
    },
    "Grant o'rinlari": {
        "en": "Grant places",
        "ru": "Грантовые места",
        "kk": "Грант орындары",
        "kaa": "Грант орындары",
        "tg": "Ҷойҳои грант",
        "ky": "Грант орундары"
    },
    "Batafsil": {
        "en": "Details",
        "ru": "Подробнее",
        "kk": "Толығырақ",
        "kaa": "Толығырақ",
        "tg": "Муфассал",
        "ky": "Кененирээк"
    },
    "Manzil": {
        "en": "Address",
        "ru": "Адрес",
        "kk": "Мекенжай",
        "kaa": "Мекенжай",
        "tg": "Суроға",
        "ky": "Дарек"
    },
    "Telefon": {
        "en": "Phone",
        "ru": "Телефон",
        "kk": "Телефон",
        "kaa": "Телефон",
        "tg": "Телефон",
        "ky": "Телефон"
    },
    "Veb-sayt": {
        "en": "Website",
        "ru": "Веб-сайт",
        "kk": "Веб-сайт",
        "kaa": "Веб-сайт",
        "tg": "Вебсайт",
        "ky": "Веб-сайт"
    },
    "Umumiy ma'lumot": {
        "en": "General information",
        "ru": "Общая информация",
        "kk": "Жалпы ақпарат",
        "kaa": "Жалпы ақпарат",
        "tg": "Маълумоти умумӣ",
        "ky": "Жалпы маалымат"
    },
    "Global Reyting": {
        "en": "Global Leaderboard",
        "ru": "Глобальный рейтинг",
        "kk": "Жаһандық рейтинг",
        "kaa": "Жаһандық рейтинг",
        "tg": "Рейтинги ҷаҳонӣ",
        "ky": "Глобалдык рейтинг"
    },
    "Eng yaxshi natijalar": {
        "en": "Best results",
        "ru": "Лучшие результаты",
        "kk": "Ең жақсы нәтижелер",
        "kaa": "Ең жақсы нәтижелер",
        "tg": "Натиҷаҳои беҳтарин",
        "ky": "Эң жакшы натыйжалар"
    },
    "Ball": {
        "en": "Points",
        "ru": "Баллы",
        "kk": "Ұпай",
        "kaa": "Ұпай",
        "tg": "Балл",
        "ky": "Упай"
    },
    "O'rin": {
        "en": "Place",
        "ru": "Место",
        "kk": "Орын",
        "kaa": "Орын",
        "tg": "Ҷой",
        "ky": "Орун"
    }
}

# Add new translations
added_count = 0
for key, value in new_translations.items():
    if key not in translations:
        translations[key] = value
        added_count += 1
        print(f"✅ Qo'shildi: {key}")
    else:
        print(f"⏭️  Mavjud: {key}")

# Save
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"\n✅ Jami {added_count} ta yangi tarjima qo'shildi!")
print(f"📊 Umumiy: {len(translations)}")
