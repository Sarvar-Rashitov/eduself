"""
Qolgan barcha tarjimalarni qo'shish
"""
import json

# Qolgan tarjimalar
final_translations = {
    "Hozircha kurslar mavjud emas": {
        "en": "No courses available yet",
        "ru": "Пока нет курсов",
        "kk": "Әзірше курстар жоқ",
        "kaa": "Ҳәзирше курслар жоқ",
        "tg": "Ҳоло курсҳо нестанд",
        "ky": "Азырынча курстар жок"
    },
    "Qidiruv bo'yicha kurs topilmadi": {
        "en": "No courses found by search",
        "ru": "По поиску курсы не найдены",
        "kk": "Іздеу бойынша курстар табылмады",
        "kaa": "Излеў бойынша курслар табылмады",
        "tg": "Аз рӯи ҷустуҷӯ курсҳо ёфт нашуданд",
        "ky": "Издөө боюнча курстар табылган жок"
    },
    "Boshqa kalit so'zlar bilan qidirib ko'ring": {
        "en": "Try searching with other keywords",
        "ru": "Попробуйте поискать с другими ключевыми словами",
        "kk": "Басқа кілт сөздермен іздеп көріңіз",
        "kaa": "Басқа кілт сөзлермен излеп көриңиз",
        "tg": "Бо калимаҳои калидии дигар ҷустуҷӯ кунед",
        "ky": "Башка ачкыч сөздөр менен издеп көрүңүз"
    },
    "To'lov URL manzili mavjud emas. Admin bilan bog'laning.": {
        "en": "Payment URL not available. Contact admin.",
        "ru": "URL оплаты недоступен. Свяжитесь с администратором.",
        "kk": "Төлем URL мекенжайы қолжетімді емес. Әкімшімен байланысыңыз.",
        "kaa": "Төлем URL мекенжайы қолжетимли емес. Әкимши пенен байланысыңыз.",
        "tg": "URL-и пардохт дастрас нест. Бо маъмур тамос гиред.",
        "ky": "Төлөм URL дареги жеткиликтүү эмес. Администратор менен байланышыңыз."
    },
    "Hozircha yangiliklar mavjud emas": {
        "en": "No news available yet",
        "ru": "Пока нет новостей",
        "kk": "Әзірше жаңалықтар жоқ",
        "kaa": "Ҳәзирше жаңалықлар жоқ",
        "tg": "Ҳоло хабарҳо нестанд",
        "ky": "Азырынча жаңылыктар жок"
    },
    "Hozircha fanlar mavjud emas": {
        "en": "No subjects available yet",
        "ru": "Пока нет предметов",
        "kk": "Әзірше пәндер жоқ",
        "kaa": "Ҳәзирше фанлар жоқ",
        "tg": "Ҳоло фанҳо нестанд",
        "ky": "Азырынча предметтер жок"
    },
    "Hozircha ta'lim muassasalari mavjud emas": {
        "en": "No educational institutions available yet",
        "ru": "Пока нет учебных заведений",
        "kk": "Әзірше білім беру мекемелері жоқ",
        "kaa": "Ҳәзирше билим бериў муассасалары жоқ",
        "tg": "Ҳоло муассисаҳои таҳсилӣ нестанд",
        "ky": "Азырынча билим берүү мекемелери жок"
    },
    "Hozircha mock imtihonlar mavjud emas": {
        "en": "No mock exams available yet",
        "ru": "Пока нет пробных экзаменов",
        "kk": "Әзірше сынақ емтихандар жоқ",
        "kaa": "Ҳәзирше сынақ имтиханлар жоқ",
        "tg": "Ҳоло имтиҳонҳои санҷишӣ нестанд",
        "ky": "Азырынча сыноо экзамендер жок"
    },
    "Hozircha sertifikatlar mavjud emas": {
        "en": "No certificates available yet",
        "ru": "Пока нет сертификатов",
        "kk": "Әзірше сертификаттар жоқ",
        "kaa": "Ҳәзирше сертификатлар жоқ",
        "tg": "Ҳоло сертификатҳо нестанд",
        "ky": "Азырынча сертификаттар жок"
    },
    "Qidiruv bo'yicha natija topilmadi": {
        "en": "No results found by search",
        "ru": "По поиску ничего не найдено",
        "kk": "Іздеу бойынша нәтиже табылмады",
        "kaa": "Излеў бойынша нәтийже табылмады",
        "tg": "Аз рӯи ҷустуҷӯ натиҷа ёфт нашуд",
        "ky": "Издөө боюнча натыйжа табылган жок"
    },
    "Kurslarni qidiring": {
        "en": "Search courses",
        "ru": "Поиск курсов",
        "kk": "Курстарды іздеу",
        "kaa": "Курсларды излеў",
        "tg": "Ҷустуҷӯи курсҳо",
        "ky": "Курстарды издөө"
    },
    "Fanlarni qidiring": {
        "en": "Search subjects",
        "ru": "Поиск предметов",
        "kk": "Пәндерді іздеу",
        "kaa": "Фанларды излеў",
        "tg": "Ҷустуҷӯи фанҳо",
        "ky": "Предметтерди издөө"
    },
    "Barcha kurslarni ko'rsatish": {
        "en": "Show all courses",
        "ru": "Показать все курсы",
        "kk": "Барлық курстарды көрсету",
        "kaa": "Барлық курсларды көрсетиў",
        "tg": "Ҳамаи курсҳоро нишон додан",
        "ky": "Бардык курстарды көрсөтүү"
    },
    "Barcha fanlarni ko'rsatish": {
        "en": "Show all subjects",
        "ru": "Показать все предметы",
        "kk": "Барлық пәндерді көрсету",
        "kaa": "Барлық фанларды көрсетиў",
        "tg": "Ҳамаи фанҳоро нишон додан",
        "ky": "Бардык предметтерди көрсөтүү"
    },
    "Barcha muassasalarni ko'rsatish": {
        "en": "Show all institutions",
        "ru": "Показать все учреждения",
        "kk": "Барлық мекемелерді көрсету",
        "kaa": "Барлық муассасаларды көрсетиў",
        "tg": "Ҳамаи муассисаҳоро нишон додан",
        "ky": "Бардык мекемелерди көрсөтүү"
    },
    "Barcha imtihonlarni ko'rsatish": {
        "en": "Show all exams",
        "ru": "Показать все экзамены",
        "kk": "Барлық емтихандарды көрсету",
        "kaa": "Барлық имтиханларды көрсетиў",
        "tg": "Ҳамаи имтиҳонҳоро нишон додан",
        "ky": "Бардык экзамендерди көрсөтүү"
    },
    "Barcha sertifikatlarni ko'rsatish": {
        "en": "Show all certificates",
        "ru": "Показать все сертификаты",
        "kk": "Барлық сертификаттарды көрсету",
        "kaa": "Барлық сертификатларды көрсетиў",
        "tg": "Ҳамаи сертификатҳоро нишон додан",
        "ky": "Бардык сертификаттарды көрсөтүү"
    },
    "Barcha mavzularni ko'rsatish": {
        "en": "Show all topics",
        "ru": "Показать все темы",
        "kk": "Барлық тақырыптарды көрсету",
        "kaa": "Барлық мавзуларды көрсетиў",
        "tg": "Ҳамаи мавзуъҳоро нишон додан",
        "ky": "Бардык темаларды көрсөтүү"
    },
    "dars": {
        "en": "lessons",
        "ru": "уроков",
        "kk": "сабақ",
        "kaa": "дарс",
        "tg": "дарс",
        "ky": "сабак"
    }
}

# Mavjud tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Yangi tarjimalarni qo'shish
count_before = len(translations)
translations.update(final_translations)
count_after = len(translations)

# Saqlash
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✓ {count_after - count_before} ta yangi tarjima qo'shildi!")
print(f"✓ Jami tarjimalar: {count_after}")
