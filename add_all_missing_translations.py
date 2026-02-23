#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# All missing translations based on screenshots
new_translations = {
    "Jami testlar": {
        "en": "Total tests",
        "ru": "Всего тестов",
        "kk": "Барлық тесттер",
        "kaa": "Барлық тесттер",
        "tg": "Ҳамаи тестҳо",
        "ky": "Бардык тесттер"
    },
    "Muvaffaqiyatli": {
        "en": "Successful",
        "ru": "Успешно",
        "kk": "Табысты",
        "kaa": "Табысты",
        "tg": "Муваффақ",
        "ky": "Ийгиликтүү"
    },
    "Progress": {
        "en": "Progress",
        "ru": "Прогресс",
        "kk": "Прогресс",
        "kaa": "Прогресс",
        "tg": "Пешрафт",
        "ky": "Прогресс"
    },
    "Faollik diagrammasi": {
        "en": "Activity diagram",
        "ru": "Диаграмма активности",
        "kk": "Белсенділік диаграммасы",
        "kaa": "Белсенділік диаграммасы",
        "tg": "Диаграммаи фаъолият",
        "ky": "Активдүүлүк диаграммасы"
    },
    "Haftalik": {
        "en": "Weekly",
        "ru": "Еженедельно",
        "kk": "Апталық",
        "kaa": "Апталық",
        "tg": "Ҳафтавор",
        "ky": "Жумалык"
    },
    "Oylik": {
        "en": "Monthly",
        "ru": "Ежемесячно",
        "kk": "Айлық",
        "kaa": "Айлық",
        "tg": "Моҳона",
        "ky": "Айлык"
    },
    "Jami (haftalik)": {
        "en": "Total (weekly)",
        "ru": "Всего (еженедельно)",
        "kk": "Барлығы (апталық)",
        "kaa": "Барлығы (апталық)",
        "tg": "Ҳамаги (ҳафтавор)",
        "ky": "Бардыгы (жумалык)"
    },
    "O'rtacha": {
        "en": "Average",
        "ru": "Средний",
        "kk": "Орташа",
        "kaa": "Орташа",
        "tg": "Миёна",
        "ky": "Орточо"
    },
    "Eng faol": {
        "en": "Most active",
        "ru": "Самый активный",
        "kk": "Ең белсенді",
        "kaa": "Ең белсенді",
        "tg": "Фаъолтарин",
        "ky": "Эң активдүү"
    },
    "Tahrirlash": {
        "en": "Edit",
        "ru": "Редактировать",
        "kk": "Өңдеу",
        "kaa": "Өңдеу",
        "tg": "Таҳрир кардан",
        "ky": "Түзөтүү"
    },
    "Өтпедіңіз": {
        "en": "Failed",
        "ru": "Не пройдено",
        "kk": "Өтпедіңіз",
        "kaa": "Өтпедіңіз",
        "tg": "Нагузаштед",
        "ky": "Өтпөдүңүз"
    },
    "Қайта уринғиз": {
        "en": "Try again",
        "ru": "Попробуйте снова",
        "kk": "Қайта көріңіз",
        "kaa": "Қайта көріңіз",
        "tg": "Аз нав кӯшиш кунед",
        "ky": "Кайра аракет кылыңыз"
    },
    "Талдауды көру": {
        "en": "View analysis",
        "ru": "Посмотреть анализ",
        "kk": "Талдауды көру",
        "kaa": "Талдауды көру",
        "tg": "Таҳлилро дидан",
        "ky": "Талдоону көрүү"
    },
    "Қайта уринғиз": {
        "en": "Try again",
        "ru": "Попробуйте снова",
        "kk": "Қайта көріңіз",
        "kaa": "Қайта көріңіз",
        "tg": "Аз нав кӯшиш кунед",
        "ky": "Кайра аракет кылыңыз"
    },
    "Email qo'shish": {
        "en": "Add email",
        "ru": "Добавить email",
        "kk": "Email қосу",
        "kaa": "Email қосу",
        "tg": "Email илова кардан",
        "ky": "Email кошуу"
    },
    "Сейлесуді бастау": {
        "en": "Start chat",
        "ru": "Начать чат",
        "kk": "Сөйлесуді бастау",
        "kaa": "Сөйлесуді бастау",
        "tg": "Сӯҳбатро оғоз кардан",
        "ky": "Маекти баштоо"
    },
    "AI Көмекші": {
        "en": "AI Assistant",
        "ru": "AI Помощник",
        "kk": "AI Көмекші",
        "kaa": "AI Көмекші",
        "tg": "Ёрдамчии AI",
        "ky": "AI Жардамчы"
    },
    "Сұрақтарыңызға жауап алыңыз, усыныстар алыңыз": {
        "en": "Get answers to your questions, get recommendations",
        "ru": "Получите ответы на ваши вопросы, получите рекомендации",
        "kk": "Сұрақтарыңызға жауап алыңыз, ұсыныстар алыңыз",
        "kaa": "Сұрақтарыңызға жауап алыңыз, ұсыныстар алыңыз",
        "tg": "Ба саволҳои худ ҷавоб гиред, тавсияҳо гиред",
        "ky": "Суроолоруңузга жооп алыңыз, сунуштарды алыңыз"
    }
}

# Add new translations
added_count = 0
updated_count = 0

for key, value in new_translations.items():
    if key not in translations:
        translations[key] = value
        added_count += 1
        print(f"✅ Qo'shildi: {key}")
    else:
        # Update if needed
        for lang_code in ['en', 'ru', 'kk', 'kaa', 'tg', 'ky']:
            if lang_code not in translations[key]:
                translations[key][lang_code] = value[lang_code]
                updated_count += 1
        print(f"⏭️  Mavjud: {key}")

# Save
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"\n✅ Jami {added_count} ta yangi tarjima qo'shildi!")
print(f"🔄 Jami {updated_count} ta tarjima yangilandi!")
print(f"📊 Umumiy: {len(translations)}")
