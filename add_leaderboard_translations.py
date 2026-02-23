import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add missing translations for leaderboard page
new_translations = {
    "Global Leaderboard - EduSelf": {
        "en": "Global Leaderboard - EduSelf",
        "ru": "Глобальный рейтинг - EduSelf",
        "kk": "Жаһандық рейтинг - EduSelf",
        "kaa": "Жаһандық рейтинг - EduSelf",
        "tg": "Рейтинги ҷаҳонӣ - EduSelf",
        "ky": "Глобалдык рейтинг - EduSelf"
    },
    "Global Reyting": {
        "en": "Global Leaderboard",
        "ru": "Глобальный рейтинг",
        "kk": "Жаһандық рейтинг",
        "kaa": "Жаһандық рейтинг",
        "tg": "Рейтинги ҷаҳонӣ",
        "ky": "Глобалдык рейтинг"
    },
    "Sizning pozitsiyangiz": {
        "en": "Your position",
        "ru": "Ваша позиция",
        "kk": "Сіздің позицияңыз",
        "kaa": "Сиздиң позицияңыз",
        "tg": "Мавқеи шумо",
        "ky": "Сиздин позицияңыз"
    },
    "Top 100 Foydalanuvchilar": {
        "en": "Top 100 Users",
        "ru": "Топ 100 пользователей",
        "kk": "Топ 100 пайдаланушылар",
        "kaa": "Топ 100 пайдаланыўшылар",
        "tg": "100 корбари беҳтарин",
        "ky": "Топ 100 колдонуучулар"
    },
    "Foydalanuvchi": {
        "en": "User",
        "ru": "Пользователь",
        "kk": "Пайдаланушы",
        "kaa": "Пайдаланыўшы",
        "tg": "Корбар",
        "ky": "Колдонуучу"
    },
    "Testlar": {
        "en": "Tests",
        "ru": "Тесты",
        "kk": "Тесттер",
        "kaa": "Тестлар",
        "tg": "Тестҳо",
        "ky": "Тесттер"
    },
    "Hali hech kim ball to'plamagan": {
        "en": "No one has earned points yet",
        "ru": "Никто еще не набрал баллов",
        "kk": "Әлі ешкім ұпай жинамаған",
        "kaa": "Әли ҳеш ким балл жыйнамаған",
        "tg": "Ҳоло ҳеҷ кас холҳо ҷамъ накардааст",
        "ky": "Али эч ким упай чогултпаган"
    },
    "Birinchi bo'lib test yechib, leaderboardda o'z o'rningizni egallang!": {
        "en": "Be the first to take tests and claim your place on the leaderboard!",
        "ru": "Будьте первым, кто пройдет тесты и займет свое место в рейтинге!",
        "kk": "Тестті алғашқы болып тапсырып, рейтингте өз орныңызды алыңыз!",
        "kaa": "Тестти биринши болып тапсырып, рейтингте өз орныңызды алыңыз!",
        "tg": "Аввалин шахсе бошед, ки тестҳоро гузаронида, дар рейтинг ҷои худро ишғол кунед!",
        "ky": "Тестти биринчи болуп тапшырып, рейтингде өз орунуңузду ээлеңиз!"
    },
    "Testlarni boshlash": {
        "en": "Start tests",
        "ru": "Начать тесты",
        "kk": "Тесттерді бастау",
        "kaa": "Тестлерди баслаў",
        "tg": "Оғози тестҳо",
        "ky": "Тесттерди баштоо"
    },
    "Reytingda yuqoriga ko'tarilmoqchimisiz?": {
        "en": "Want to climb higher in the rankings?",
        "ru": "Хотите подняться выше в рейтинге?",
        "kk": "Рейтингте жоғары көтерілгіңіз келе ме?",
        "kaa": "Рейтингте жоқары көтерилгиңиз келе ме?",
        "tg": "Мехоҳед дар рейтинг боло баравед?",
        "ky": "Рейтингде жогору көтөрүлгүңүз келеби?"
    },
    "Ko'proq test yechib, ko'proq ball to'plang!": {
        "en": "Take more tests and earn more points!",
        "ru": "Решайте больше тестов и зарабатывайте больше баллов!",
        "kk": "Көбірек тест шешіп, көбірек ұпай жинаңыз!",
        "kaa": "Көбирек тест шешип, көбирек балл жыйнаңыз!",
        "tg": "Тестҳои бештар гузаронида, холҳои бештар ҷамъ кунед!",
        "ky": "Көбүрөөк тест чечип, көбүрөөк упай чогултуңуз!"
    },
    "Fanlar bo'yicha testlar": {
        "en": "Subject tests",
        "ru": "Тесты по предметам",
        "kk": "Пәндер бойынша тесттер",
        "kaa": "Фанлар бойынша тестлер",
        "tg": "Тестҳо аз рӯи фанҳо",
        "ky": "Предметтер боюнча тесттер"
    },
    "Sertifikat testlari": {
        "en": "Certificate tests",
        "ru": "Сертификационные тесты",
        "kk": "Сертификат тесттері",
        "kaa": "Сертификат тестлери",
        "tg": "Тестҳои сертификатӣ",
        "ky": "Сертификат тесттери"
    },
    "Mock imtihonlar": {
        "en": "Mock exams",
        "ru": "Пробные экзамены",
        "kk": "Сынақ емтихандар",
        "kaa": "Сынақ имтиханлар",
        "tg": "Имтиҳонҳои санҷишӣ",
        "ky": "Сыноо экзамендер"
    },
    "o'rin": {
        "en": "place",
        "ru": "место",
        "kk": "орын",
        "kaa": "орын",
        "tg": "ҷой",
        "ky": "орун"
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
