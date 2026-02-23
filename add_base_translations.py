import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# New translations to add
new_translations = {
    "Bildirishnomalar": {
        "en": "Notifications",
        "ru": "Уведомления",
        "kk": "Хабарландырулар",
        "kaa": "Билдириснома лар",
        "tg": "Огоҳиҳо",
        "ky": "Билдирүүлөр"
    },
    "Bildirishnoma": {
        "en": "Notification",
        "ru": "Уведомление",
        "kk": "Хабарландыру",
        "kaa": "Билдириснома",
        "tg": "Огоҳӣ",
        "ky": "Билдирүү"
    },
    "Bildirishnomalar yo'q": {
        "en": "No notifications",
        "ru": "Нет уведомлений",
        "kk": "Хабарландырулар жоқ",
        "kaa": "Билдириснома лар жоқ",
        "tg": "Огоҳиҳо нест",
        "ky": "Билдирүүлөр жок"
    },
    "Yangi bildirishnomalar bu yerda ko'rinadi": {
        "en": "New notifications will appear here",
        "ru": "Новые уведомления появятся здесь",
        "kk": "Жаңа хабарландырулар осында көрінеді",
        "kaa": "Жаңа билдириснома лар бул жерде көринеди",
        "tg": "Огоҳиҳои нав дар ин ҷо пайдо мешаванд",
        "ky": "Жаңы билдирүүлөр бул жерде көрүнөт"
    },
    "Yopish": {
        "en": "Close",
        "ru": "Закрыть",
        "kk": "Жабу",
        "kaa": "Жабу",
        "tg": "Пӯшидан",
        "ky": "Жабуу"
    },
    "Sahifaga o'tish": {
        "en": "Go to page",
        "ru": "Перейти на страницу",
        "kk": "Бетке өту",
        "kaa": "Бетке өту",
        "tg": "Ба саҳифа гузаштан",
        "ky": "Бетке өтүү"
    },
    "Mehmon": {
        "en": "Guest",
        "ru": "Гость",
        "kk": "Қонақ",
        "kaa": "Қонақ",
        "tg": "Меҳмон",
        "ky": "Конок"
    },
    "Kirish talab qilinadi": {
        "en": "Login required",
        "ru": "Требуется вход",
        "kk": "Кіру қажет",
        "kaa": "Кіру қажет",
        "tg": "Воридшавӣ лозим аст",
        "ky": "Кирүү талап кылынат"
    },
    "Oq rejim": {
        "en": "Light mode",
        "ru": "Светлый режим",
        "kk": "Ашық режим",
        "kaa": "Ашық режим",
        "tg": "Реҷаи равшан",
        "ky": "Ачык режим"
    },
    "Qora rejim": {
        "en": "Dark mode",
        "ru": "Темный режим",
        "kk": "Қараңғы режим",
        "kaa": "Қараңғы режим",
        "tg": "Реҷаи торик",
        "ky": "Караңгы режим"
    },
    "Yangiliklar": {
        "en": "News",
        "ru": "Новости",
        "kk": "Жаңалықтар",
        "kaa": "Жаңалықлар",
        "tg": "Хабарҳо",
        "ky": "Жаңылыктар"
    },
    "Online Kurslar": {
        "en": "Online Courses",
        "ru": "Онлайн курсы",
        "kk": "Онлайн курстар",
        "kaa": "Онлайн курслар",
        "tg": "Курсҳои онлайн",
        "ky": "Онлайн курстар"
    },
    "AI Hamroh": {
        "en": "AI Assistant",
        "ru": "AI Помощник",
        "kk": "AI Көмекші",
        "kaa": "AI Көмекші",
        "tg": "Ёрдамчии AI",
        "ky": "AI Жардамчы"
    },
    "Ta'lim Muassasalari": {
        "en": "Educational Institutions",
        "ru": "Образовательные учреждения",
        "kk": "Білім беру мекемелері",
        "kaa": "Білім беру муассасалары",
        "tg": "Муассисаҳои таҳсилӣ",
        "ky": "Билим берүү мекемелери"
    },
    "Mening Profilim": {
        "en": "My Profile",
        "ru": "Мой профиль",
        "kk": "Менің профилім",
        "kaa": "Менің профилім",
        "tg": "Профили ман",
        "ky": "Менин профилим"
    },
    "Sozlamalar": {
        "en": "Settings",
        "ru": "Настройки",
        "kk": "Баптаулар",
        "kaa": "Баптаулар",
        "tg": "Танзимот",
        "ky": "Жөндөөлөр"
    },
    "Chiqish": {
        "en": "Logout",
        "ru": "Выход",
        "kk": "Шығу",
        "kaa": "Шығу",
        "tg": "Баромадан",
        "ky": "Чыгуу"
    },
    "Kirish": {
        "en": "Login",
        "ru": "Вход",
        "kk": "Кіру",
        "kaa": "Кіру",
        "tg": "Воридшавӣ",
        "ky": "Кирүү"
    },
    "Ro'yxatdan o'tish": {
        "en": "Register",
        "ru": "Регистрация",
        "kk": "Тіркелу",
        "kaa": "Тіркелу",
        "tg": "Бақайдгирӣ",
        "ky": "Катталуу"
    },
    "Mock Exam": {
        "en": "Mock Exam",
        "ru": "Пробный экзамен",
        "kk": "Сынақ емтихан",
        "kaa": "Сынақ имтихан",
        "tg": "Имтиҳони санҷишӣ",
        "ky": "Сыноо экзамен"
    }
}

# Add new translations (skip if already exists)
added_count = 0
for key, value in new_translations.items():
    if key not in translations:
        translations[key] = value
        added_count += 1
        print(f"✅ Qo'shildi: {key}")
    else:
        print(f"⏭️  Mavjud: {key}")

# Save updated translations
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"\n✅ Jami {added_count} ta yangi tarjima qo'shildi!")
print(f"📊 Umumiy tarjimalar soni: {len(translations)}")
