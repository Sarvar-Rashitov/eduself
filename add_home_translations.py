"""
Home sahifasi uchun yangi tarjimalar qo'shish
"""
import json

# Yangi tarjimalar
new_translations = {
    "Foydalanuvchilar": {
        "en": "Users",
        "ru": "Пользователи",
        "kk": "Пайдаланушылар",
        "kaa": "Пайдаланыўшылар",
        "tg": "Корбарон",
        "ky": "Колдонуучулар"
    },
    "Test Savollari": {
        "en": "Test Questions",
        "ru": "Тестовые вопросы",
        "kk": "Тест сұрақтары",
        "kaa": "Тест сорақлары",
        "tg": "Саволҳои тест",
        "ky": "Тест суроолору"
    },
    "Testlar": {
        "en": "Tests",
        "ru": "Тесты",
        "kk": "Тесттер",
        "kaa": "Тестлар",
        "tg": "Тестҳо",
        "ky": "Тесттер"
    },
    "Ballar": {
        "en": "Points",
        "ru": "Баллы",
        "kk": "Ұпайлар",
        "kaa": "Баллар",
        "tg": "Холҳо",
        "ky": "Упайлар"
    },
    "Oxirgi Test": {
        "en": "Last Test",
        "ru": "Последний тест",
        "kk": "Соңғы тест",
        "kaa": "Соңғы тест",
        "tg": "Тести охирин",
        "ky": "Акыркы тест"
    },
    "O'tdingiz": {
        "en": "Passed",
        "ru": "Пройдено",
        "kk": "Өттіңіз",
        "kaa": "Өттиңиз",
        "tg": "Гузаштед",
        "ky": "Өттүңүз"
    },
    "O'tmadingiz": {
        "en": "Failed",
        "ru": "Не пройдено",
        "kk": "Өтпедіңіз",
        "kaa": "Өтпедиңиз",
        "tg": "Нагузаштед",
        "ky": "Өтпөдүңүз"
    },
    "Tahlil Ko'rish": {
        "en": "View Analysis",
        "ru": "Посмотреть анализ",
        "kk": "Талдауды көру",
        "kaa": "Таҳлилди көриў",
        "tg": "Дидани таҳлил",
        "ky": "Талдоону көрүү"
    },
    "Keyingi Testni Boshlash": {
        "en": "Start Next Test",
        "ru": "Начать следующий тест",
        "kk": "Келесі тестті бастау",
        "kaa": "Келеси тестти баслаў",
        "tg": "Оғози тести навбатӣ",
        "ky": "Кийинки тестти баштоо"
    },
    "Qayta Urinish": {
        "en": "Try Again",
        "ru": "Попробовать снова",
        "kk": "Қайта көріңіз",
        "kaa": "Қайта көриңиз",
        "tg": "Аз нав кӯшиш кунед",
        "ky": "Кайра аракет кылыңыз"
    },
    "Oxirgi Sertifikat Testi": {
        "en": "Last Certificate Test",
        "ru": "Последний тест на сертификат",
        "kk": "Соңғы сертификат тесті",
        "kaa": "Соңғы сертификат тести",
        "tg": "Тести охирини сертификат",
        "ky": "Акыркы сертификат тести"
    },
    "AI Hamroh": {
        "en": "AI Assistant",
        "ru": "AI Помощник",
        "kk": "AI Көмекші",
        "kaa": "AI Жәрдемши",
        "tg": "Ёрдамчии AI",
        "ky": "AI Жардамчы"
    },
    "Suhbat Boshlash": {
        "en": "Start Chat",
        "ru": "Начать чат",
        "kk": "Сөйлесуді бастау",
        "kaa": "Сөйлесиўди баслаў",
        "tg": "Оғози сӯҳбат",
        "ky": "Маектешүүнү баштоо"
    },
    "Platformaning Imkoniyatlari": {
        "en": "Platform Features",
        "ru": "Возможности платформы",
        "kk": "Платформа мүмкіндіктері",
        "kaa": "Платформа мүмкиншиликлери",
        "tg": "Имкониятҳои платформа",
        "ky": "Платформанын мүмкүнчүлүктөрү"
    },
    "Online Kurslar": {
        "en": "Online Courses",
        "ru": "Онлайн курсы",
        "kk": "Онлайн курстар",
        "kaa": "Онлайн курслар",
        "tg": "Курсҳои онлайн",
        "ky": "Онлайн курстар"
    },
    "Video darslar": {
        "en": "Video lessons",
        "ru": "Видео уроки",
        "kk": "Бейне сабақтар",
        "kaa": "Видео дарслар",
        "tg": "Дарсҳои видео",
        "ky": "Видео сабактар"
    },
    "Barcha fanlar": {
        "en": "All subjects",
        "ru": "Все предметы",
        "kk": "Барлық пәндер",
        "kaa": "Барлық фанлар",
        "tg": "Ҳамаи фанҳо",
        "ky": "Бардык предметтер"
    },
    "Bilimingizni tasdiqlang": {
        "en": "Certify your knowledge",
        "ru": "Подтвердите свои знания",
        "kk": "Білімді растаңыз",
        "kaa": "Билимиңизди тастыйықлаң",
        "tg": "Донишатонро тасдиқ кунед",
        "ky": "Билимиңизди тастыктаңыз"
    },
    "Mock Imtihonlar": {
        "en": "Mock Exams",
        "ru": "Пробные экзамены",
        "kk": "Сынақ емтихандар",
        "kaa": "Сынақ имтиханлар",
        "tg": "Имтиҳонҳои санҷишӣ",
        "ky": "Сыноо экзамендер"
    },
    "Real tajriba": {
        "en": "Real experience",
        "ru": "Реальный опыт",
        "kk": "Нақты тәжірибе",
        "kaa": "Нақты тәжирийбе",
        "tg": "Таҷрибаи воқеӣ",
        "ky": "Чыныгы тажрыйба"
    },
    "Universitet va maktablar": {
        "en": "Universities and schools",
        "ru": "Университеты и школы",
        "kk": "Университеттер мен мектептер",
        "kaa": "Университетлер ҳәм мектеплер",
        "tg": "Донишгоҳҳо ва мактабҳо",
        "ky": "Университеттер жана мектептер"
    },
    "Top o'quvchilar": {
        "en": "Top students",
        "ru": "Лучшие ученики",
        "kk": "Үздік оқушылар",
        "kaa": "Үздик оқыўшылар",
        "tg": "Хонандагони беҳтарин",
        "ky": "Мыкты окуучулар"
    },
    "Tavsiya Etamiz": {
        "en": "We Recommend",
        "ru": "Рекомендуем",
        "kk": "Ұсынамыз",
        "kaa": "Усынамыз",
        "tg": "Тавсия мекунем",
        "ky": "Сунуштайбыз"
    },
    "Ta'lim Muassasalari": {
        "en": "Educational Institutions",
        "ru": "Образовательные учреждения",
        "kk": "Білім беру мекемелері",
        "kaa": "Билим бериў муассасалары",
        "tg": "Муассисаҳои таҳсилӣ",
        "ky": "Билим берүү мекемелери"
    },
    "Top Reyting": {
        "en": "Top Rating",
        "ru": "Топ рейтинг",
        "kk": "Топ рейтинг",
        "kaa": "Топ рейтинг",
        "tg": "Рейтинги болоӣ",
        "ky": "Топ рейтинг"
    },
    "Bizga Ishonadigan Hamkorlar": {
        "en": "Our Trusted Partners",
        "ru": "Наши надежные партнеры",
        "kk": "Бізге сенетін серіктестер",
        "kaa": "Бизге ишенетуғын ҳәмкорлар",
        "tg": "Шарикони боэътимоди мо",
        "ky": "Бизге ишенген өнөктөштөр"
    },
    "Platformamiz": {
        "en": "Our Platform",
        "ru": "Наша платформа",
        "kk": "Біздің платформа",
        "kaa": "Биздиң платформа",
        "tg": "Платформаи мо",
        "ky": "Биздин платформа"
    },
    "Bog'lanish": {
        "en": "Contact",
        "ru": "Контакты",
        "kk": "Байланыс",
        "kaa": "Байланыс",
        "tg": "Тамос",
        "ky": "Байланыш"
    },
    "Ijtimoiy tarmoqlar": {
        "en": "Social Networks",
        "ru": "Социальные сети",
        "kk": "Әлеуметтік желілер",
        "kaa": "Әлеўметлик желилер",
        "tg": "Шабакаҳои иҷтимоӣ",
        "ky": "Социалдык тармактар"
    },
    "Barcha huquqlar himoyalangan": {
        "en": "All rights reserved",
        "ru": "Все права защищены",
        "kk": "Барлық құқықтар қорғалған",
        "kaa": "Барлық ҳуқықлар қорғалған",
        "tg": "Ҳамаи ҳуқуқҳо ҳифз шудаанд",
        "ky": "Бардык укуктар корголгон"
    },
    "Salom": {
        "en": "Hello",
        "ru": "Привет",
        "kk": "Сәлем",
        "kaa": "Салам",
        "tg": "Салом",
        "ky": "Салам"
    },
    "ball": {
        "en": "points",
        "ru": "баллов",
        "kk": "ұпай",
        "kaa": "балл",
        "tg": "хол",
        "ky": "упай"
    },
    "test": {
        "en": "tests",
        "ru": "тестов",
        "kk": "тест",
        "kaa": "тест",
        "tg": "тест",
        "ky": "тест"
    },
    "yo'nalish": {
        "en": "directions",
        "ru": "направлений",
        "kk": "бағыт",
        "kaa": "йўналыс",
        "tg": "самт",
        "ky": "багыт"
    },
    "mavzu": {
        "en": "topics",
        "ru": "тем",
        "kk": "тақырып",
        "kaa": "мавзу",
        "tg": "мавзуъ",
        "ky": "тема"
    },
    "savol": {
        "en": "questions",
        "ru": "вопросов",
        "kk": "сұрақ",
        "kaa": "сорақ",
        "tg": "савол",
        "ky": "суроо"
    },
    "Sizning o'rningiz": {
        "en": "Your position",
        "ru": "Ваша позиция",
        "kk": "Сіздің орныңыз",
        "kaa": "Сиздиң орныңыз",
        "tg": "Мавқеи шумо",
        "ky": "Сиздин орунуңуз"
    }
}

# Mavjud tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Yangi tarjimalarni qo'shish
translations.update(new_translations)

# Saqlash
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✓ {len(new_translations)} ta yangi tarjima qo'shildi!")
print(f"✓ Jami tarjimalar: {len(translations)}")
