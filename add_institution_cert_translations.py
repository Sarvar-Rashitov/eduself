import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# New translations for institution detail, certificate test result, and take certificate test
new_translations = {
    # Institution detail page
    "Ta'lim yo'nalishlari": {
        "en": "Educational Directions",
        "ru": "Направления обучения",
        "kk": "Білім беру бағыттары",
        "kaa": "Билим бериў йўналыслары",
        "tg": "Самтҳои таҳсилӣ",
        "ky": "Билим берүү багыттары"
    },
    "To'liq ma'lumot": {
        "en": "Full Information",
        "ru": "Полная информация",
        "kk": "Толық ақпарат",
        "kaa": "Толық мағлыўмат",
        "tg": "Маълумоти пурра",
        "ky": "Толук маалымат"
    },
    "Aloqa ma'lumotlari": {
        "en": "Contact Information",
        "ru": "Контактная информация",
        "kk": "Байланыс ақпараты",
        "kaa": "Байланыс мағлыўматлары",
        "tg": "Маълумоти тамос",
        "ky": "Байланыш маалыматы"
    },
    "Manzil xaritasi": {
        "en": "Location Map",
        "ru": "Карта местоположения",
        "kk": "Орналасқан жер картасы",
        "kaa": "Мекен картасы",
        "tg": "Харитаи мавқеъ",
        "ky": "Жайгашкан жер картасы"
    },
    "Vebsayt": {
        "en": "Website",
        "ru": "Веб-сайт",
        "kk": "Веб-сайт",
        "kaa": "Веб-сайт",
        "tg": "Вебсайт",
        "ky": "Веб-сайт"
    },
    "Manzil": {
        "en": "Address",
        "ru": "Адрес",
        "kk": "Мекенжай",
        "kaa": "Мекен",
        "tg": "Суроға",
        "ky": "Дарек"
    },
    "Batafsil": {
        "en": "Details",
        "ru": "Подробнее",
        "kk": "Толығырақ",
        "kaa": "Батафсил",
        "tg": "Муфассал",
        "ky": "Кененирээк"
    },
    "Imtihon topshirish": {
        "en": "Take Exam",
        "ru": "Сдать экзамен",
        "kk": "Емтихан тапсыру",
        "kaa": "Имтихан топсырыў",
        "tg": "Имтиҳон додан",
        "ky": "Экзамен тапшыруу"
    },
    
    # Certificate test pages
    "Tabriklaymiz": {
        "en": "Congratulations",
        "ru": "Поздравляем",
        "kk": "Құттықтаймыз",
        "kaa": "Қутлықлаймыз",
        "tg": "Табрик мекунем",
        "ky": "Куттуктайбыз"
    },
    "Afsuski": {
        "en": "Unfortunately",
        "ru": "К сожалению",
        "kk": "Өкінішке орай",
        "kaa": "Өкиниш",
        "tg": "Мутаассифона",
        "ky": "Тилекке каршы"
    },
    "to'g'ri javob": {
        "en": "correct answers",
        "ru": "правильных ответов",
        "kk": "дұрыс жауап",
        "kaa": "дурыс жуўап",
        "tg": "ҷавобҳои дуруст",
        "ky": "туура жооп"
    },
    "Qayta urinish": {
        "en": "Try Again",
        "ru": "Попробовать снова",
        "kk": "Қайта көріңіз",
        "kaa": "Қайта көриңиз",
        "tg": "Аз нав кӯшиш кунед",
        "ky": "Кайра аракет кылыңыз"
    },
    "Keyingi test": {
        "en": "Next test",
        "ru": "Следующий тест",
        "kk": "Келесі тест",
        "kaa": "Келеси тест",
        "tg": "Тести навбатӣ",
        "ky": "Кийинки тест"
    },
    "Testni boshlash": {
        "en": "Start Test",
        "ru": "Начать тест",
        "kk": "Тестті бастау",
        "kaa": "Тестти баслаў",
        "tg": "Оғози тест",
        "ky": "Тестти баштоо"
    },
    "Matn": {
        "en": "Text",
        "ru": "Текст",
        "kk": "Мәтін",
        "kaa": "Мәтин",
        "tg": "Матн",
        "ky": "Текст"
    },
    "Ogohlantirish": {
        "en": "Warning",
        "ru": "Предупреждение",
        "kk": "Ескерту",
        "kaa": "Ескертиў",
        "tg": "Огоҳӣ",
        "ky": "Эскертүү"
    },
    "Testni tugatish": {
        "en": "Finish test",
        "ru": "Завершить тест",
        "kk": "Тестті аяқтау",
        "kaa": "Тестти аяқтаў",
        "tg": "Хотима додани тест",
        "ky": "Тестти аяктоо"
    },
    "Davom etish": {
        "en": "Continue",
        "ru": "Продолжить",
        "kk": "Жалғастыру",
        "kaa": "Даўам етиў",
        "tg": "Давом додан",
        "ky": "Улантуу"
    },
    "Tugatish": {
        "en": "Finish",
        "ru": "Завершить",
        "kk": "Аяқтау",
        "kaa": "Аяқтаў",
        "tg": "Хотима додан",
        "ky": "Аяктоо"
    },
    "ta savolga javob berdingiz": {
        "en": "questions answered",
        "ru": "вопросов отвечено",
        "kk": "сұраққа жауап бердіңіз",
        "kaa": "сораққа жуўап бердиңиз",
        "tg": "савол ҷавоб додед",
        "ky": "суроого жооп бердиңиз"
    },
    "Joriy ballingiz": {
        "en": "Current score",
        "ru": "Текущий балл",
        "kk": "Ағымдағы ұпай",
        "kaa": "Ағымдағы балл",
        "tg": "Холи ҷорӣ",
        "ky": "Учурдагы упай"
    },
}

# Merge with existing translations
translations.update(new_translations)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translations)} new translations")
print(f"📊 Total translations: {len(translations)}")
