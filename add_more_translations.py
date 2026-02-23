"""
Ko'proq statik matnlar qo'shish
"""
import json

# Qo'shimcha statik matnlar
additional_translations = {
    # Subjects/Topics
    "Mavzular": {
        "en": "Topics",
        "ru": "Темы",
        "kk": "Тақырыптар",
        "kaa": "Мавзулар",
        "tg": "Мавзуъҳо",
        "ky": "Темалар"
    },
    "Test": {
        "en": "Test",
        "ru": "Тест",
        "kk": "Тест",
        "kaa": "Тест",
        "tg": "Тест",
        "ky": "Тест"
    },
    "Testni boshlash": {
        "en": "Start Test",
        "ru": "Начать тест",
        "kk": "Тестті бастау",
        "kaa": "Тестти баслаў",
        "tg": "Оғози тест",
        "ky": "Тестти баштоо"
    },
    "Tahlil": {
        "en": "Analysis",
        "ru": "Анализ",
        "kk": "Талдау",
        "kaa": "Таҳлил",
        "tg": "Таҳлил",
        "ky": "Талдоо"
    },
    
    # Institutions
    "Ta'lim muassasalari": {
        "en": "Educational Institutions",
        "ru": "Образовательные учреждения",
        "kk": "Білім беру мекемелері",
        "kaa": "Билим бериў муассасалары",
        "tg": "Муассисаҳои таҳсилӣ",
        "ky": "Билим берүү мекемелери"
    },
    "Yo'nalishlar": {
        "en": "Directions",
        "ru": "Направления",
        "kk": "Бағыттар",
        "kaa": "Йўналыслар",
        "tg": "Самтҳо",
        "ky": "Багыттар"
    },
    "Kontrakt": {
        "en": "Contract",
        "ru": "Контракт",
        "kk": "Келісімшарт",
        "kaa": "Контракт",
        "tg": "Шартнома",
        "ky": "Келишим"
    },
    "Qabul": {
        "en": "Admission",
        "ru": "Прием",
        "kk": "Қабылдау",
        "kaa": "Қабыл",
        "tg": "Қабул",
        "ky": "Кабыл алуу"
    },
    
    # Common actions
    "Yuklab olish": {
        "en": "Download",
        "ru": "Скачать",
        "kk": "Жүктеп алу",
        "kaa": "Жүклеп алыў",
        "tg": "Боргирӣ кардан",
        "ky": "Жүктөп алуу"
    },
    "Ulashish": {
        "en": "Share",
        "ru": "Поделиться",
        "kk": "Бөлісу",
        "kaa": "Улысыў",
        "tg": "Мубодила кардан",
        "ky": "Бөлүшүү"
    },
    "Tahrirlash": {
        "en": "Edit",
        "ru": "Редактировать",
        "kk": "Өңдеу",
        "kaa": "Таҳрирлеў",
        "tg": "Таҳрир кардан",
        "ky": "Түзөтүү"
    },
    "O'chirish": {
        "en": "Delete",
        "ru": "Удалить",
        "kk": "Жою",
        "kaa": "Өшириў",
        "tg": "Нест кардан",
        "ky": "Өчүрүү"
    },
    
    # Status/Results
    "Muvaffaqiyatli": {
        "en": "Success",
        "ru": "Успешно",
        "kk": "Сәтті",
        "kaa": "Муваффақиятли",
        "tg": "Муваффақ",
        "ky": "Ийгиликтүү"
    },
    "Xato": {
        "en": "Error",
        "ru": "Ошибка",
        "kk": "Қате",
        "kaa": "Қате",
        "tg": "Хато",
        "ky": "Ката"
    },
    "Yuklanyapti": {
        "en": "Loading",
        "ru": "Загрузка",
        "kk": "Жүктелуде",
        "kaa": "Жүкленип атыр",
        "tg": "Боргирӣ",
        "ky": "Жүктөлүүдө"
    },
    "Tugallandi": {
        "en": "Completed",
        "ru": "Завершено",
        "kk": "Аяқталды",
        "kaa": "Тугалланды",
        "tg": "Анҷом ёфт",
        "ky": "Аяктады"
    },
    
    # Time/Date
    "Bugun": {
        "en": "Today",
        "ru": "Сегодня",
        "kk": "Бүгін",
        "kaa": "Бүгин",
        "tg": "Имрӯз",
        "ky": "Бүгүн"
    },
    "Kecha": {
        "en": "Yesterday",
        "ru": "Вчера",
        "kk": "Кеше",
        "kaa": "Кеше",
        "tg": "Дирӯз",
        "ky": "Кечээ"
    },
    "Ertaga": {
        "en": "Tomorrow",
        "ru": "Завтра",
        "kk": "Ертең",
        "kaa": "Ертең",
        "tg": "Фардо",
        "ky": "Эртең"
    },
    
    # User/Profile
    "Mening profilim": {
        "en": "My Profile",
        "ru": "Мой профиль",
        "kk": "Менің профилім",
        "kaa": "Менің профилим",
        "tg": "Профили ман",
        "ky": "Менин профилим"
    },
    "Parol": {
        "en": "Password",
        "ru": "Пароль",
        "kk": "Құпия сөз",
        "kaa": "Парол",
        "tg": "Рамз",
        "ky": "Сыр сөз"
    },
    "Email": {
        "en": "Email",
        "ru": "Email",
        "kk": "Email",
        "kaa": "Email",
        "tg": "Email",
        "ky": "Email"
    },
    "Telefon": {
        "en": "Phone",
        "ru": "Телефон",
        "kk": "Телефон",
        "kaa": "Телефон",
        "tg": "Телефон",
        "ky": "Телефон"
    },
    
    # Misc
    "Ko'proq": {
        "en": "More",
        "ru": "Больше",
        "kk": "Көбірек",
        "kaa": "Көбирек",
        "tg": "Бештар",
        "ky": "Көбүрөөк"
    },
    "Kamroq": {
        "en": "Less",
        "ru": "Меньше",
        "kk": "Азырақ",
        "kaa": "Камирек",
        "tg": "Камтар",
        "ky": "Азыраак"
    },
    "Hammasi": {
        "en": "Everything",
        "ru": "Всё",
        "kk": "Бәрі",
        "kaa": "Ҳәммеси",
        "tg": "Ҳама чиз",
        "ky": "Баары"
    },
    "Hech narsa": {
        "en": "Nothing",
        "ru": "Ничего",
        "kk": "Ештеңе",
        "kaa": "Ҳеш нәрсе",
        "tg": "Ҳеҷ чиз",
        "ky": "Эч нерсе"
    },
}

def update_translations():
    """Mavjud tarjimalarga qo'shish"""
    # Mavjud tarjimalarni yuklash
    with open('static_translations.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    # Yangi tarjimalarni qo'shish
    translations.update(additional_translations)
    
    # Saqlash
    with open('static_translations.json', 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Tarjimalar yangilandi!")
    print(f"✓ Jami: {len(translations)} ta statik matn")
    print(f"✓ Qo'shildi: {len(additional_translations)} ta yangi matn")

if __name__ == '__main__':
    update_translations()
