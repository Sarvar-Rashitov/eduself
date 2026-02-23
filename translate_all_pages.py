"""
Barcha sahifalardagi tarjima qilinmagan matnlarni avtomatik tarjima qilish
"""
import json
import os
import re

# Yangi tarjimalar ro'yxati
all_new_translations = {
    # Common messages
    "Hozircha": {
        "en": "Not yet",
        "ru": "Пока нет",
        "kk": "Әзірше",
        "kaa": "Ҳәзирше",
        "tg": "Ҳоло",
        "ky": "Азырынча"
    },
    "mavjud emas": {
        "en": "not available",
        "ru": "недоступно",
        "kk": "қолжетімді емес",
        "kaa": "қолжетимли емес",
        "tg": "дастрас нест",
        "ky": "жеткиликтүү эмес"
    },
    "topilmadi": {
        "en": "not found",
        "ru": "не найдено",
        "kk": "табылмады",
        "kaa": "табылмады",
        "tg": "ёфт нашуд",
        "ky": "табылган жок"
    },
    "Yopish": {
        "en": "Close",
        "ru": "Закрыть",
        "kk": "Жабу",
        "kaa": "Жабыў",
        "tg": "Пӯшидан",
        "ky": "Жабуу"
    },
    "Ortga": {
        "en": "Back",
        "ru": "Назад",
        "kk": "Артқа",
        "kaa": "Артқа",
        "tg": "Бозгашт",
        "ky": "Артка"
    },
    "Keyingi": {
        "en": "Next",
        "ru": "Следующий",
        "kk": "Келесі",
        "kaa": "Келеси",
        "tg": "Навбатӣ",
        "ky": "Кийинки"
    },
    "Hali hech kim": {
        "en": "No one yet",
        "ru": "Пока никто",
        "kk": "Әлі ешкім",
        "kaa": "Әли ҳеш ким",
        "tg": "Ҳоло ҳеҷ кас",
        "ky": "Али эч ким"
    },
    "Siz": {
        "en": "You",
        "ru": "Вы",
        "kk": "Сіз",
        "kaa": "Сиз",
        "tg": "Шумо",
        "ky": "Сиз"
    },
    "Kurs haqida": {
        "en": "About course",
        "ru": "О курсе",
        "kk": "Курс туралы",
        "kaa": "Курс ҳаққында",
        "tg": "Дар бораи курс",
        "ky": "Курс жөнүндө"
    },
    "Dars matni": {
        "en": "Lesson text",
        "ru": "Текст урока",
        "kk": "Сабақ мәтіні",
        "kaa": "Дарс мәтини",
        "tg": "Матни дарс",
        "ky": "Сабак тексти"
    },
    "Ulashish": {
        "en": "Share",
        "ru": "Поделиться",
        "kk": "Бөлісу",
        "kaa": "Улысыў",
        "tg": "Мубодила",
        "ky": "Бөлүшүү"
    },
    "Yashirish": {
        "en": "Hide",
        "ru": "Скрыть",
        "kk": "Жасыру",
        "kaa": "Жасырыў",
        "tg": "Пинҳон кардан",
        "ky": "Жашыруу"
    },
    "Mashhur": {
        "en": "Popular",
        "ru": "Популярный",
        "kk": "Танымал",
        "kaa": "Машҳур",
        "tg": "Машҳур",
        "ky": "Популярдуу"
    },
    "Narx": {
        "en": "Price",
        "ru": "Цена",
        "kk": "Баға",
        "kaa": "Баға",
        "tg": "Нарх",
        "ky": "Баа"
    },
    "so'm": {
        "en": "sum",
        "ru": "сум",
        "kk": "сом",
        "kaa": "сом",
        "tg": "сом",
        "ky": "сом"
    },
    "Tugallangan": {
        "en": "Completed",
        "ru": "Завершено",
        "kk": "Аяқталды",
        "kaa": "Тугалланды",
        "tg": "Анҷом ёфт",
        "ky": "Аяктады"
    },
    "Yopiq": {
        "en": "Closed",
        "ru": "Закрыто",
        "kk": "Жабық",
        "kaa": "Жабық",
        "tg": "Пӯшида",
        "ky": "Жабык"
    },
    "Savollar": {
        "en": "Questions",
        "ru": "Вопросы",
        "kk": "Сұрақтар",
        "kaa": "Сорақлар",
        "tg": "Саволҳо",
        "ky": "Суроолор"
    },
    "Javobni tekshirish": {
        "en": "Check answer",
        "ru": "Проверить ответ",
        "kk": "Жауапты тексеру",
        "kaa": "Жуўапты тексериў",
        "tg": "Санҷиши ҷавоб",
        "ky": "Жоопту текшерүү"
    },
    "Keyingi savol": {
        "en": "Next question",
        "ru": "Следующий вопрос",
        "kk": "Келесі сұрақ",
        "kaa": "Келеси сорақ",
        "tg": "Саволи навбатӣ",
        "ky": "Кийинки суроо"
    },
    "Testni yakunlash": {
        "en": "Finish test",
        "ru": "Завершить тест",
        "kk": "Тестті аяқтау",
        "kaa": "Тестти аяқтаў",
        "tg": "Хотима додани тест",
        "ky": "Тестти аяктоо"
    },
    "Testni tugatmoqchimisiz": {
        "en": "Do you want to finish the test",
        "ru": "Хотите завершить тест",
        "kk": "Тестті аяқтағыңыз келе ме",
        "kaa": "Тестти аяқтағыңыз келе ме",
        "tg": "Мехоҳед тестро хотима диҳед",
        "ky": "Тестти аяктагыңыз келеби"
    },
    "Tugatilgandan so'ng qaytib bo'lmaydi": {
        "en": "Cannot be undone after completion",
        "ru": "После завершения нельзя отменить",
        "kk": "Аяқтағаннан кейін қайтарып болмайды",
        "kaa": "Аяқтағаннан кейин қайтарып болмайды",
        "tg": "Пас аз хотима бозгашт ғайриимкон аст",
        "ky": "Аяктагандан кийин кайтарып болбойт"
    },
    "Natija topilmadi": {
        "en": "Result not found",
        "ru": "Результат не найден",
        "kk": "Нәтиже табылмады",
        "kaa": "Нәтийже табылмады",
        "tg": "Натиҷа ёфт нашуд",
        "ky": "Натыйжа табылган жок"
    },
    "AI Tahlil": {
        "en": "AI Analysis",
        "ru": "AI Анализ",
        "kk": "AI Талдау",
        "kaa": "AI Таҳлил",
        "tg": "Таҳлили AI",
        "ky": "AI Талдоо"
    },
    "Tahlil qilinmoqda": {
        "en": "Analyzing",
        "ru": "Анализируется",
        "kk": "Талданып жатыр",
        "kaa": "Таҳлил қылынып атыр",
        "tg": "Таҳлил мешавад",
        "ky": "Талдоо жүрүүдө"
    },
    "AI Hamroh Tavsiyalari": {
        "en": "AI Assistant Recommendations",
        "ru": "Рекомендации AI помощника",
        "kk": "AI көмекшінің ұсыныстары",
        "kaa": "AI жәрдемшиниң усыныслары",
        "tg": "Тавсияҳои ёрдамчии AI",
        "ky": "AI жардамчынын сунуштары"
    },
    "AI Hamroh sizning natijangizni tahlil qilmoqda": {
        "en": "AI Assistant is analyzing your result",
        "ru": "AI помощник анализирует ваш результат",
        "kk": "AI көмекші нәтижеңізді талдап жатыр",
        "kaa": "AI жәрдемши нәтийжеңизди таҳлил қылып атыр",
        "tg": "Ёрдамчии AI натиҷаи шуморо таҳлил мекунад",
        "ky": "AI жардамчы натыйжаңызды талдап жатат"
    },
    "qoldi": {
        "en": "remaining",
        "ru": "осталось",
        "kk": "қалды",
        "kaa": "қалды",
        "tg": "боқӣ монд",
        "ky": "калды"
    },
    "javob berildi": {
        "en": "answered",
        "ru": "отвечено",
        "kk": "жауап берілді",
        "kaa": "жуўап берилди",
        "tg": "ҷавоб дода шуд",
        "ky": "жооп берилди"
    },
    "javobsiz": {
        "en": "unanswered",
        "ru": "без ответа",
        "kk": "жауапсыз",
        "kaa": "жуўапсыз",
        "tg": "бе ҷавоб",
        "ky": "жоопсуз"
    },
    "Hozircha reklamalar yo'q": {
        "en": "No ads yet",
        "ru": "Пока нет рекламы",
        "kk": "Әзірше жарнама жоқ",
        "kaa": "Ҳәзирше жарнама жоқ",
        "tg": "Ҳоло реклама нест",
        "ky": "Азырынча жарнама жок"
    }
}

# Mavjud tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Yangi tarjimalarni qo'shish
count_before = len(translations)
translations.update(all_new_translations)
count_after = len(translations)

# Saqlash
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✓ {count_after - count_before} ta yangi tarjima qo'shildi!")
print(f"✓ Jami tarjimalar: {count_after}")
