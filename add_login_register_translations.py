import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# New translations for login and register pages
new_translations = {
    "Kirish": {
        "en": "Login",
        "ru": "Войти",
        "kk": "Кіру",
        "kaa": "Кириў",
        "tg": "Ворид шудан",
        "ky": "Кирүү"
    },
    "Xush kelibsiz": {
        "en": "Welcome",
        "ru": "Добро пожаловать",
        "kk": "Қош келдіңіз",
        "kaa": "Хош келдиңиз",
        "tg": "Хуш омадед",
        "ky": "Кош келиңиз"
    },
    "Hisobingizga kiring": {
        "en": "Login to your account",
        "ru": "Войдите в свой аккаунт",
        "kk": "Есептік жазбаңызға кіріңіз",
        "kaa": "Есабыңызға кириң",
        "tg": "Ба ҳисоби худ ворид шавед",
        "ky": "Эсебиңизге кириңиз"
    },
    "Google bilan": {
        "en": "With Google",
        "ru": "С Google",
        "kk": "Google арқылы",
        "kaa": "Google пенен",
        "tg": "Бо Google",
        "ky": "Google менен"
    },
    "Telegram bilan": {
        "en": "With Telegram",
        "ru": "С Telegram",
        "kk": "Telegram арқылы",
        "kaa": "Telegram пенен",
        "tg": "Бо Telegram",
        "ky": "Telegram менен"
    },
    "yoki": {
        "en": "or",
        "ru": "или",
        "kk": "немесе",
        "kaa": "яки",
        "tg": "ё",
        "ky": "же"
    },
    "Telefon raqam": {
        "en": "Phone number",
        "ru": "Номер телефона",
        "kk": "Телефон нөмірі",
        "kaa": "Телефон номери",
        "tg": "Рақами телефон",
        "ky": "Телефон номери"
    },
    "Eslab qol": {
        "en": "Remember me",
        "ru": "Запомнить меня",
        "kk": "Мені есте сақта",
        "kaa": "Мени еслеп қал",
        "tg": "Маро дар хотир нигоҳ дор",
        "ky": "Мени эстеп кал"
    },
    "Parolni unutdingizmi": {
        "en": "Forgot password",
        "ru": "Забыли пароль",
        "kk": "Құпия сөзді ұмыттыңыз ба",
        "kaa": "Паролды унытыңыз ба",
        "tg": "Рамзро фаромӯш кардед",
        "ky": "Сыр сөздү унуттуңузбу"
    },
    "Hisobingiz yo'qmi": {
        "en": "Don't have an account",
        "ru": "Нет аккаунта",
        "kk": "Есептік жазбаңыз жоқ па",
        "kaa": "Есабыңыз жоқ па",
        "tg": "Ҳисоб надоред",
        "ky": "Эсебиңиз жокпу"
    },
    "Ro'yxatdan o'ting": {
        "en": "Register",
        "ru": "Зарегистрироваться",
        "kk": "Тіркелу",
        "kaa": "Тиркелиў",
        "tg": "Сабти ном",
        "ky": "Катталуу"
    },
    "Ro'yxatdan o'tish": {
        "en": "Registration",
        "ru": "Регистрация",
        "kk": "Тіркелу",
        "kaa": "Тиркелиў",
        "tg": "Сабти ном",
        "ky": "Катталуу"
    },
    "EduSelf ga qo'shiling": {
        "en": "Join EduSelf",
        "ru": "Присоединяйтесь к EduSelf",
        "kk": "EduSelf-ке қосылыңыз",
        "kaa": "EduSelf-ке қосылың",
        "tg": "Ба EduSelf ҳамроҳ шавед",
        "ky": "EduSelf-ке кошулуңуз"
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
        "kaa": "Фамилия",
        "tg": "Насаб",
        "ky": "Фамилия"
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
        "kaa": "Фамилияңыз",
        "tg": "Насаби шумо",
        "ky": "Фамилияңыз"
    },
    "Tasdiqlash": {
        "en": "Confirm",
        "ru": "Подтверждение",
        "kk": "Растау",
        "kaa": "Тастыйықлаў",
        "tg": "Тасдиқ",
        "ky": "Тастыктоо"
    },
    "Ommaviy oferta shartlari": {
        "en": "Public offer terms",
        "ru": "Условия публичной оферты",
        "kk": "Жария оферта шарттары",
        "kaa": "Жәрия оферта шартлары",
        "tg": "Шартҳои пешниҳоди умумӣ",
        "ky": "Жалпы сунуш шарттары"
    },
    "ni qabul qilaman": {
        "en": "I accept",
        "ru": "Я принимаю",
        "kk": "Қабылдаймын",
        "kaa": "Қабыл қыламан",
        "tg": "Қабул мекунам",
        "ky": "Кабыл алам"
    },
    "Hisobingiz bormi": {
        "en": "Already have an account",
        "ru": "Уже есть аккаунт",
        "kk": "Есептік жазбаңыз бар ма",
        "kaa": "Есабыңыз бар ма",
        "tg": "Ҳисоб доред",
        "ky": "Эсебиңиз барбы"
    }
}

# Merge with existing translations
translations.update(new_translations)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translations)} new translations")
print(f"📊 Total translations: {len(translations)}")
