"""
Home sahifasi uchun qo'shimcha tarjimalar
"""
import json

# Qo'shimcha tarjimalar
additional_translations = {
    "O'zbekiston #1 Ta'lim Platformasi": {
        "en": "Uzbekistan's #1 Education Platform",
        "ru": "Образовательная платформа #1 в Узбекистане",
        "kk": "Өзбекстанның #1 білім беру платформасы",
        "kaa": "Өзбекстанның #1 билим бериў платформасы",
        "tg": "Платформаи таҳсилии №1 дар Ӯзбекистон",
        "ky": "Өзбекстандын #1 билим берүү платформасы"
    },
    "EduSelf bilan o'z kelajagingizni quring": {
        "en": "Build your future with EduSelf",
        "ru": "Постройте свое будущее с EduSelf",
        "kk": "EduSelf арқылы болашағыңызды құрыңыз",
        "kaa": "EduSelf пенен келешегиңизди қурыңыз",
        "tg": "Ояндаи худро бо EduSelf созед",
        "ky": "EduSelf менен келечегиңизди куруңуз"
    },
    "AI yordamchi, 10,000+ test savollari, sertifikatlar va eng yaxshi ta'lim muassasalari haqida to'liq ma'lumot": {
        "en": "AI assistant, 10,000+ test questions, certificates and complete information about the best educational institutions",
        "ru": "AI помощник, 10,000+ тестовых вопросов, сертификаты и полная информация о лучших учебных заведениях",
        "kk": "AI көмекші, 10,000+ тест сұрақтары, сертификаттар және үздік оқу орындары туралы толық ақпарат",
        "kaa": "AI жәрдемши, 10,000+ тест сорақлары, сертификатлар ҳәм ең жақсы билим бериў муассасалары ҳаққында толық мағлыўмат",
        "tg": "Ёрдамчии AI, 10,000+ саволҳои тест, сертификатҳо ва маълумоти пурра дар бораи муассисаҳои таҳсилии беҳтарин",
        "ky": "AI жардамчы, 10,000+ тест суроолору, сертификаттар жана эң мыкты билим берүү мекемелери жөнүндө толук маалымат"
    },
    "24/7 shaxsiy yordamchi": {
        "en": "24/7 personal assistant",
        "ru": "24/7 личный помощник",
        "kk": "24/7 жеке көмекші",
        "kaa": "24/7 жеке жәрдемши",
        "tg": "24/7 ёрдамчии шахсӣ",
        "ky": "24/7 жеке жардамчы"
    },
    "Gamefikatsiya": {
        "en": "Gamification",
        "ru": "Геймификация",
        "kk": "Геймификация",
        "kaa": "Геймификация",
        "tg": "Геймификатсия",
        "ky": "Геймификация"
    },
    "Ball to'plang, raqobatlashing": {
        "en": "Collect points, compete",
        "ru": "Собирайте баллы, соревнуйтесь",
        "kk": "Ұпай жинаңыз, бәсекелесіңіз",
        "kaa": "Балл жыйнаң, бәсекелесиң",
        "tg": "Холҳо ҷамъ кунед, рақобат кунед",
        "ky": "Упай чогултуңуз, атаандашыңыз"
    },
    "Progress Tracking": {
        "en": "Progress Tracking",
        "ru": "Отслеживание прогресса",
        "kk": "Прогресті бақылау",
        "kaa": "Прогрести бақылаў",
        "tg": "Пайгирии пешрафт",
        "ky": "Прогрессти көзөмөлдөө"
    },
    "Rivojlanishingizni kuzating": {
        "en": "Track your progress",
        "ru": "Отслеживайте свой прогресс",
        "kk": "Дамуыңызды қадағалаңыз",
        "kaa": "Раўажланыўыңызды қадағалаң",
        "tg": "Пешрафти худро пайгирӣ кунед",
        "ky": "Өнүгүүңүздү көзөмөлдөңүз"
    },
    "Bepul Boshlash": {
        "en": "Start Free",
        "ru": "Начать бесплатно",
        "kk": "Тегін бастау",
        "kaa": "Бепул баслаў",
        "tg": "Ройгон оғоз кунед",
        "ky": "Акысыз баштоо"
    },
    "Savollaringizga javob oling, tavsiyalar oling": {
        "en": "Get answers to your questions, get recommendations",
        "ru": "Получите ответы на свои вопросы, получите рекомендации",
        "kk": "Сұрақтарыңызға жауап алыңыз, ұсыныстар алыңыз",
        "kaa": "Сорақларыңызға жуўап алыңыз, усыныслар алыңыз",
        "tg": "Ба саволҳои худ ҷавоб гиред, тавсияҳо гиред",
        "ky": "Суроолоруңузга жооп алыңыз, сунуштарды алыңыз"
    },
    "O'zbekistonda ta'limni rivojlantirish platformasi": {
        "en": "Platform for developing education in Uzbekistan",
        "ru": "Платформа развития образования в Узбекистане",
        "kk": "Өзбекстанда білім беруді дамыту платформасы",
        "kaa": "Өзбекстанда билим бериўди раўажландырыў платформасы",
        "tg": "Платформаи рушди таҳсил дар Ӯзбекистон",
        "ky": "Өзбекстанда билим берүүнү өнүктүрүү платформасы"
    }
}

# Mavjud tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Yangi tarjimalarni qo'shish
translations.update(additional_translations)

# Saqlash
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✓ {len(additional_translations)} ta qo'shimcha tarjima qo'shildi!")
print(f"✓ Jami tarjimalar: {len(translations)}")
