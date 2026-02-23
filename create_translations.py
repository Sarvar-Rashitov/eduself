"""
Statik matnlar uchun tarjima lug'ati yaratish
"""
import os
import json

# Statik matnlar va ularning tarjimalari
translations = {
    # Navigation
    "Bosh sahifa": {
        "en": "Home",
        "ru": "Главная",
        "kk": "Басты бет",
        "kaa": "Bas bet",
        "tg": "Саҳифаи асосӣ",
        "ky": "Башкы бет"
    },
    "Fanlar": {
        "en": "Subjects",
        "ru": "Предметы",
        "kk": "Пәндер",
        "kaa": "Fанлар",
        "tg": "Фанҳо",
        "ky": "Предметтер"
    },
    "Sertifikatlar": {
        "en": "Certificates",
        "ru": "Сертификаты",
        "kk": "Сертификаттар",
        "kaa": "Сертификатлар",
        "tg": "Сертификатҳо",
        "ky": "Сертификаттар"
    },
    "Imtihonlar": {
        "en": "Exams",
        "ru": "Экзамены",
        "kk": "Емтихандар",
        "kaa": "Имтиханлар",
        "tg": "Имтиҳонҳо",
        "ky": "Экзамендер"
    },
    "Muassasalar": {
        "en": "Institutions",
        "ru": "Учреждения",
        "kk": "Мекемелер",
        "kaa": "Муассасалар",
        "tg": "Муассисаҳо",
        "ky": "Мекемелер"
    },
    "Kurslar": {
        "en": "Courses",
        "ru": "Курсы",
        "kk": "Курстар",
        "kaa": "Курслар",
        "tg": "Курсҳо",
        "ky": "Курстар"
    },
    "Reyting": {
        "en": "Leaderboard",
        "ru": "Рейтинг",
        "kk": "Рейтинг",
        "kaa": "Рейтинг",
        "tg": "Рейтинг",
        "ky": "Рейтинг"
    },
    "Yangiliklar": {
        "en": "News",
        "ru": "Новости",
        "kk": "Жаңалықтар",
        "kaa": "Жаңалықлар",
        "tg": "Хабарҳо",
        "ky": "Жаңылыктар"
    },
    
    # Buttons
    "Kirish": {
        "en": "Login",
        "ru": "Войти",
        "kk": "Кіру",
        "kaa": "Кириў",
        "tg": "Ворид шудан",
        "ky": "Кирүү"
    },
    "Chiqish": {
        "en": "Logout",
        "ru": "Выйти",
        "kk": "Шығу",
        "kaa": "Шығыў",
        "tg": "Баромадан",
        "ky": "Чыгуу"
    },
    "Saqlash": {
        "en": "Save",
        "ru": "Сохранить",
        "kk": "Сақтау",
        "kaa": "Сақлаў",
        "tg": "Захира кардан",
        "ky": "Сактоо"
    },
    "Bekor qilish": {
        "en": "Cancel",
        "ru": "Отмена",
        "kk": "Болдырмау",
        "kaa": "Бийкар қылыў",
        "tg": "Бекор кардан",
        "ky": "Жокко чыгаруу"
    },
    "Ko'rish": {
        "en": "View",
        "ru": "Просмотр",
        "kk": "Көру",
        "kaa": "Көриў",
        "tg": "Дидан",
        "ky": "Көрүү"
    },
    "Batafsil": {
        "en": "Details",
        "ru": "Подробнее",
        "kk": "Толығырақ",
        "kaa": "Батафсил",
        "tg": "Муфассал",
        "ky": "Кененирээк"
    },
    "Boshlash": {
        "en": "Start",
        "ru": "Начать",
        "kk": "Бастау",
        "kaa": "Баслаў",
        "tg": "Оғоз кардан",
        "ky": "Баштоо"
    },
    "Davom etish": {
        "en": "Continue",
        "ru": "Продолжить",
        "kk": "Жалғастыру",
        "kaa": "Давам етиў",
        "tg": "Давом додан",
        "ky": "Улантуу"
    },
    "Yuborish": {
        "en": "Submit",
        "ru": "Отправить",
        "kk": "Жіберу",
        "kaa": "Жибериў",
        "tg": "Фиристодан",
        "ky": "Жөнөтүү"
    },
    "Qaytish": {
        "en": "Back",
        "ru": "Назад",
        "kk": "Артқа",
        "kaa": "Қайтыў",
        "tg": "Бозгашт",
        "ky": "Артка"
    },
    
    # Common words
    "Barchasi": {
        "en": "All",
        "ru": "Все",
        "kk": "Барлығы",
        "kaa": "Ҳәммеси",
        "tg": "Ҳама",
        "ky": "Баары"
    },
    "Qidirish": {
        "en": "Search",
        "ru": "Поиск",
        "kk": "Іздеу",
        "kaa": "Излеў",
        "tg": "Ҷустуҷӯ",
        "ky": "Издөө"
    },
    "Natija": {
        "en": "Result",
        "ru": "Результат",
        "kk": "Нәтиже",
        "kaa": "Нәтийже",
        "tg": "Натиҷа",
        "ky": "Натыйжа"
    },
    "Ball": {
        "en": "Score",
        "ru": "Балл",
        "kk": "Ұпай",
        "kaa": "Балл",
        "tg": "Холҳо",
        "ky": "Упай"
    },
    "Vaqt": {
        "en": "Time",
        "ru": "Время",
        "kk": "Уақыт",
        "kaa": "Ўақыт",
        "tg": "Вақт",
        "ky": "Убакыт"
    },
    "Savol": {
        "en": "Question",
        "ru": "Вопрос",
        "kk": "Сұрақ",
        "kaa": "Сорақ",
        "tg": "Савол",
        "ky": "Суроо"
    },
    "Javob": {
        "en": "Answer",
        "ru": "Ответ",
        "kk": "Жауап",
        "kaa": "Жуўап",
        "tg": "Ҷавоб",
        "ky": "Жооп"
    },
    "To'g'ri": {
        "en": "Correct",
        "ru": "Правильно",
        "kk": "Дұрыс",
        "kaa": "Дурыс",
        "tg": "Дуруст",
        "ky": "Туура"
    },
    "Noto'g'ri": {
        "en": "Incorrect",
        "ru": "Неправильно",
        "kk": "Қате",
        "kaa": "Қате",
        "tg": "Нодуруст",
        "ky": "Туура эмес"
    },
    "Profil": {
        "en": "Profile",
        "ru": "Профиль",
        "kk": "Профиль",
        "kaa": "Профиль",
        "tg": "Профил",
        "ky": "Профиль"
    },
    "Sozlamalar": {
        "en": "Settings",
        "ru": "Настройки",
        "kk": "Баптаулар",
        "kaa": "Созламалар",
        "tg": "Танзимот",
        "ky": "Жөндөөлөр"
    },
}

def save_translations():
    """Tarjimalarni JSON faylga saqlash"""
    output_file = 'static_translations.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Tarjimalar saqlandi: {output_file}")
    print(f"✓ Jami: {len(translations)} ta statik matn")
    print()
    print("Tillar:")
    for lang in ['en', 'ru', 'kk', 'kaa', 'tg', 'ky']:
        print(f"  - {lang}: {len(translations)} ta tarjima")

if __name__ == '__main__':
    save_translations()
