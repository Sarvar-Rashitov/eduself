"""
Qolgan barcha tarjimalarni qo'shish
"""
import json

# Qolgan tarjimalar
remaining_translations = {
    # Home page specific
    "Gamefikatsiya": {
        "en": "Gamification",
        "ru": "Геймификация",
        "kk": "Геймификация",
        "kaa": "Геймификация",
        "tg": "Геймификатсия",
        "ky": "Геймификация"
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
    "Kurs nomi": {
        "en": "Course name",
        "ru": "Название курса",
        "kk": "Курс атауы",
        "kaa": "Курс аты",
        "tg": "Номи курс",
        "ky": "Курстун аталышы"
    },
    "Kursga yozilish": {
        "en": "Enroll in course",
        "ru": "Записаться на курс",
        "kk": "Курсқа жазылу",
        "kaa": "Курсқа жазылыў",
        "tg": "Сабти ном ба курс",
        "ky": "Курска жазылуу"
    },
    "To'lov qilish": {
        "en": "Make payment",
        "ru": "Оплатить",
        "kk": "Төлем жасау",
        "kaa": "Төлем жасаў",
        "tg": "Пардохт кардан",
        "ky": "Төлөм жасоо"
    },
    "Qidiruv bo'yicha": {
        "en": "By search",
        "ru": "По поиску",
        "kk": "Іздеу бойынша",
        "kaa": "Излеў бойынша",
        "tg": "Аз рӯи ҷустуҷӯ",
        "ky": "Издөө боюнча"
    },
    "Muassasa haqida": {
        "en": "About institution",
        "ru": "Об учреждении",
        "kk": "Мекеме туралы",
        "kaa": "Муассаса ҳаққында",
        "tg": "Дар бораи муассиса",
        "ky": "Мекеме жөнүндө"
    },
    "Yo'nalish haqida": {
        "en": "About direction",
        "ru": "О направлении",
        "kk": "Бағыт туралы",
        "kaa": "Йўналыс ҳаққында",
        "tg": "Дар бораи самт",
        "ky": "Багыт жөнүндө"
    },
    "Kontrakt to'lovi": {
        "en": "Contract payment",
        "ru": "Оплата контракта",
        "kk": "Келісімшарт төлемі",
        "kaa": "Контракт төлеми",
        "tg": "Пардохти шартнома",
        "ky": "Келишим төлөмү"
    },
    "Qabul muddati": {
        "en": "Admission period",
        "ru": "Срок приема",
        "kk": "Қабылдау мерзімі",
        "kaa": "Қабыл муддети",
        "tg": "Мӯҳлати қабул",
        "ky": "Кабыл алуу мөөнөтү"
    },
    "Muassasa litsenziyasi": {
        "en": "Institution license",
        "ru": "Лицензия учреждения",
        "kk": "Мекеме лицензиясы",
        "kaa": "Муассаса лицензиясы",
        "tg": "Литсензияи муассиса",
        "ky": "Мекеменин лицензиясы"
    },
    "Aloqa": {
        "en": "Contact",
        "ru": "Контакт",
        "kk": "Байланыс",
        "kaa": "Байланыс",
        "tg": "Тамос",
        "ky": "Байланыш"
    },
    "Ijtimoiy tarmoqlar": {
        "en": "Social networks",
        "ru": "Социальные сети",
        "kk": "Әлеуметтік желілер",
        "kaa": "Әлеўметлик желилер",
        "tg": "Шабакаҳои иҷтимоӣ",
        "ky": "Социалдык тармактар"
    },
    "O'tish balli": {
        "en": "Passing score",
        "ru": "Проходной балл",
        "kk": "Өту ұпайы",
        "kaa": "Өтиў баллы",
        "tg": "Холи гузариш",
        "ky": "Өтүү упайы"
    },
    "Savollar soni": {
        "en": "Number of questions",
        "ru": "Количество вопросов",
        "kk": "Сұрақтар саны",
        "kaa": "Сорақлар саны",
        "tg": "Шумораи саволҳо",
        "ky": "Суроолордун саны"
    },
    "Vaqt limiti": {
        "en": "Time limit",
        "ru": "Ограничение времени",
        "kk": "Уақыт шегі",
        "kaa": "Ўақыт шеги",
        "tg": "Маҳдудияти вақт",
        "ky": "Убакыт чеги"
    },
    "Barcha darslar": {
        "en": "All lessons",
        "ru": "Все уроки",
        "kk": "Барлық сабақтар",
        "kaa": "Барлық дарслар",
        "tg": "Ҳамаи дарсҳо",
        "ky": "Бардык сабактар"
    },
    "O'qituvchi": {
        "en": "Teacher",
        "ru": "Преподаватель",
        "kk": "Оқытушы",
        "kaa": "Оқытыўшы",
        "tg": "Муаллим",
        "ky": "Мугалим"
    },
    "Cheksiz kirish": {
        "en": "Unlimited access",
        "ru": "Неограниченный доступ",
        "kk": "Шексіз кіру",
        "kaa": "Шексиз кириў",
        "tg": "Дастрасии номаҳдуд",
        "ky": "Чексиз кирүү"
    },
    "Sertifikat beriladi": {
        "en": "Certificate provided",
        "ru": "Выдается сертификат",
        "kk": "Сертификат беріледі",
        "kaa": "Сертификат бериледи",
        "tg": "Сертификат дода мешавад",
        "ky": "Сертификат берилет"
    },
    "Kurs ma'lumotlari": {
        "en": "Course information",
        "ru": "Информация о курсе",
        "kk": "Курс ақпараты",
        "kaa": "Курс мағлыўматлары",
        "tg": "Маълумоти курс",
        "ky": "Курс маалыматы"
    },
    "Muassasa ma'lumotlari": {
        "en": "Institution information",
        "ru": "Информация об учреждении",
        "kk": "Мекеме ақпараты",
        "kaa": "Муассаса мағлыўматлары",
        "tg": "Маълумоти муассиса",
        "ky": "Мекеме маалыматы"
    },
    "Foydalanuvchi": {
        "en": "User",
        "ru": "Пользователь",
        "kk": "Пайдаланушы",
        "kaa": "Пайдаланыўшы",
        "tg": "Корбар",
        "ky": "Колдонуучу"
    },
    "Sizning pozitsiyangiz": {
        "en": "Your position",
        "ru": "Ваша позиция",
        "kk": "Сіздің позицияңыз",
        "kaa": "Сиздиң позицияңыз",
        "tg": "Мавқеи шумо",
        "ky": "Сиздин позицияңыз"
    },
    "Global Reyting": {
        "en": "Global Rating",
        "ru": "Глобальный рейтинг",
        "kk": "Жаһандық рейтинг",
        "kaa": "Глобал рейтинг",
        "tg": "Рейтинги ҷаҳонӣ",
        "ky": "Глобалдык рейтинг"
    },
    "Yakunlash": {
        "en": "Finish",
        "ru": "Завершить",
        "kk": "Аяқтау",
        "kaa": "Аяқтаў",
        "tg": "Хотима додан",
        "ky": "Аяктоо"
    },
    "Imtihonni yakunlash": {
        "en": "Finish exam",
        "ru": "Завершить экзамен",
        "kk": "Емтиханды аяқтау",
        "kaa": "Имтиханды аяқтаў",
        "tg": "Хотима додани имтиҳон",
        "ky": "Экзаменди аяктоо"
    },
    "natija": {
        "en": "result",
        "ru": "результат",
        "kk": "нәтиже",
        "kaa": "нәтийже",
        "tg": "натиҷа",
        "ky": "натыйжа"
    },
    "Ball to'plandi": {
        "en": "Points earned",
        "ru": "Набрано баллов",
        "kk": "Ұпай жиналды",
        "kaa": "Балл жыйналды",
        "tg": "Холҳо ҷамъ шуд",
        "ky": "Упай чогулду"
    },
    "To'g'ri javob": {
        "en": "Correct answer",
        "ru": "Правильный ответ",
        "kk": "Дұрыс жауап",
        "kaa": "Дурыс жуўап",
        "tg": "Ҷавоби дуруст",
        "ky": "Туура жооп"
    },
    "Noto'g'ri javob": {
        "en": "Wrong answer",
        "ru": "Неправильный ответ",
        "kk": "Қате жауап",
        "kaa": "Қате жуўап",
        "tg": "Ҷавоби нодуруст",
        "ky": "Туура эмес жооп"
    },
    "Sarflangan vaqt": {
        "en": "Time spent",
        "ru": "Затраченное время",
        "kk": "Жұмсалған уақыт",
        "kaa": "Жұмсалған ўақыт",
        "tg": "Вақти сарфшуда",
        "ky": "Сарпталган убакыт"
    }
}

# Mavjud tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Yangi tarjimalarni qo'shish
count_before = len(translations)
translations.update(remaining_translations)
count_after = len(translations)

# Saqlash
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✓ {count_after - count_before} ta yangi tarjima qo'shildi!")
print(f"✓ Jami tarjimalar: {count_after}")
