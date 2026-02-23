import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add missing translations for profile page
new_translations = {
    "Emailni tasdiqlash": {
        "en": "Verify email",
        "ru": "Подтвердить email",
        "kk": "Email растау",
        "kaa": "Email растау",
        "tg": "Email тасдиқ кардан",
        "ky": "Email тастыктоо"
    },
    "Hali test ishlanmagan": {
        "en": "No tests taken yet",
        "ru": "Тесты еще не пройдены",
        "kk": "Әлі тест өтілмеген",
        "kaa": "Әлі тест өтілмеген",
        "tg": "Ҳоло тест гузаронида нашудааст",
        "ky": "Али тест өтүлгөн жок"
    },
    "Fanlarni ko'rish": {
        "en": "View subjects",
        "ru": "Посмотреть предметы",
        "kk": "Пәндерді көру",
        "kaa": "Пәндерді көру",
        "tg": "Фанҳоро дидан",
        "ky": "Предметтерди көрүү"
    },
    "Sertifikatlarni ko'rish": {
        "en": "View certificates",
        "ru": "Посмотреть сертификаты",
        "kk": "Сертификаттарды көру",
        "kaa": "Сертификаттарды көру",
        "tg": "Сертификатҳоро дидан",
        "ky": "Сертификаттарды көрүү"
    },
    "Mock Exam": {
        "en": "Mock Exam",
        "ru": "Пробный экзамен",
        "kk": "Сынақ емтихан",
        "kaa": "Сынақ емтихан",
        "tg": "Имтиҳони санҷишӣ",
        "ky": "Сыноо экзамен"
    },
    "Mock Examlarni ko'rish": {
        "en": "View mock exams",
        "ru": "Посмотреть пробные экзамены",
        "kk": "Сынақ емтихандарды көру",
        "kaa": "Сынақ емтихандарды көру",
        "tg": "Имтиҳонҳои санҷиширо дидан",
        "ky": "Сыноо экзамендерди көрүү"
    },
    "ishlangan": {
        "en": "taken",
        "ru": "пройдено",
        "kk": "өтілген",
        "kaa": "өтілген",
        "tg": "гузаронида шуд",
        "ky": "өтүлгөн"
    },
    "Hali exam ishlanmagan": {
        "en": "No exams taken yet",
        "ru": "Экзамены еще не пройдены",
        "kk": "Әлі емтихан өтілмеген",
        "kaa": "Әлі емтихан өтілмеген",
        "tg": "Ҳоло имтиҳон гузаронида нашудааст",
        "ky": "Али экзамен өтүлгөн жок"
    },
    "Profilni tahrirlash": {
        "en": "Edit profile",
        "ru": "Редактировать профиль",
        "kk": "Профильді өңдеу",
        "kaa": "Профильді өңдеу",
        "tg": "Профилро таҳрир кардан",
        "ky": "Профилди түзөтүү"
    },
    "Ism": {
        "en": "First name",
        "ru": "Имя",
        "kk": "Аты",
        "kaa": "Аты",
        "tg": "Ном",
        "ky": "Аты"
    },
    "Familiya": {
        "en": "Last name",
        "ru": "Фамилия",
        "kk": "Тегі",
        "kaa": "Тегі",
        "tg": "Насаб",
        "ky": "Фамилиясы"
    },
    "Ismingiz": {
        "en": "Your first name",
        "ru": "Ваше имя",
        "kk": "Атыңыз",
        "kaa": "Атыңыз",
        "tg": "Номи шумо",
        "ky": "Атыңыз"
    },
    "Familiyangiz": {
        "en": "Your last name",
        "ru": "Ваша фамилия",
        "kk": "Тегіңіз",
        "kaa": "Тегіңіз",
        "tg": "Насаби шумо",
        "ky": "Фамилияңыз"
    },
    "Foydalanuvchi nomi": {
        "en": "Username",
        "ru": "Имя пользователя",
        "kk": "Пайдаланушы аты",
        "kaa": "Пайдаланушы аты",
        "tg": "Номи корбар",
        "ky": "Колдонуучу аты"
    },
    "Bio": {
        "en": "Bio",
        "ru": "О себе",
        "kk": "Өзім туралы",
        "kaa": "Өзім туралы",
        "tg": "Дар бораи худ",
        "ky": "Өзүм жөнүндө"
    },
    "Profil rasmi": {
        "en": "Profile picture",
        "ru": "Фото профиля",
        "kk": "Профиль суреті",
        "kaa": "Профиль суреті",
        "tg": "Расми профил",
        "ky": "Профиль сүрөтү"
    },
    "Parolni o'zgartirish": {
        "en": "Change password",
        "ru": "Изменить пароль",
        "kk": "Құпия сөзді өзгерту",
        "kaa": "Құпия сөзді өзгерту",
        "tg": "Рамзро иваз кардан",
        "ky": "Сыр сөздү өзгөртүү"
    },
    "Joriy parol": {
        "en": "Current password",
        "ru": "Текущий пароль",
        "kk": "Ағымдағы құпия сөз",
        "kaa": "Ағымдағы құпия сөз",
        "tg": "Рамзи ҷорӣ",
        "ky": "Учурдагы сыр сөз"
    },
    "Yangi parol": {
        "en": "New password",
        "ru": "Новый пароль",
        "kk": "Жаңа құпия сөз",
        "kaa": "Жаңа құпия сөз",
        "tg": "Рамзи нав",
        "ky": "Жаңы сыр сөз"
    },
    "Yangi parolni tasdiqlang": {
        "en": "Confirm new password",
        "ru": "Подтвердите новый пароль",
        "kk": "Жаңа құпия сөзді растаңыз",
        "kaa": "Жаңа құпия сөзді растаңыз",
        "tg": "Рамзи навро тасдиқ кунед",
        "ky": "Жаңы сыр сөздү тастыктаңыз"
    },
    "Xavfli zona": {
        "en": "Danger zone",
        "ru": "Опасная зона",
        "kk": "Қауіпті аймақ",
        "kaa": "Қауіпті аймақ",
        "tg": "Минтақаи хатарнок",
        "ky": "Коркунучтуу аймак"
    },
    "Hisobni o'chirish qaytarib bo'lmaydi.": {
        "en": "Account deletion cannot be undone.",
        "ru": "Удаление аккаунта нельзя отменить.",
        "kk": "Есептік жазбаны жоюды қайтару мүмкін емес.",
        "kaa": "Есептік жазбаны жоюды қайтару мүмкін емес.",
        "tg": "Нест кардани ҳисобро бозгардонидан ғайриимкон аст.",
        "ky": "Эсепти өчүрүүнү кайтаруу мүмкүн эмес."
    },
    "Hisobni o'chirish": {
        "en": "Delete account",
        "ru": "Удалить аккаунт",
        "kk": "Есептік жазбаны жою",
        "kaa": "Есептік жазбаны жою",
        "tg": "Ҳисобро нест кардан",
        "ky": "Эсепти өчүрүү"
    },
    "Oxirgi 30 kun": {
        "en": "Last 30 days",
        "ru": "Последние 30 дней",
        "kk": "Соңғы 30 күн",
        "kaa": "Соңғы 30 күн",
        "tg": "30 рӯзи охирин",
        "ky": "Акыркы 30 күн"
    },
    "Jami (oylik)": {
        "en": "Total (monthly)",
        "ru": "Всего (ежемесячно)",
        "kk": "Барлығы (айлық)",
        "kaa": "Барлығы (айлық)",
        "tg": "Ҳамаги (моҳона)",
        "ky": "Бардыгы (айлык)"
    }
}

# Add new translations
for key, value in new_translations.items():
    if key not in translations:
        translations[key] = value
        print(f"Added: {key}")
    else:
        print(f"Already exists: {key}")

# Save updated translations
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"\nTotal translations: {len(translations)}")
