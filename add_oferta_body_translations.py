import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add oferta body text translations
new_translations = {
    "Ushbu Ommaviy Oferta (keyingi o'rinlarda \"Oferta\") EduSelf platformasi (keyingi o'rinlarda \"Platforma\") tomonidan taqdim etiladigan xizmatlardan foydalanish shartlarini belgilaydi.": {
        "en": "This Public Offer (hereinafter \"Offer\") defines the terms of use of services provided by the EduSelf platform (hereinafter \"Platform\").",
        "ru": "Данная Публичная Оферта (далее \"Оферта\") определяет условия использования услуг, предоставляемых платформой EduSelf (далее \"Платформа\").",
        "kk": "Бұл Жария Оферта (бұдан әрі \"Оферта\") EduSelf платформасы (бұдан әрі \"Платформа\") ұсынатын қызметтерді пайдалану шарттарын белгілейді.",
        "kaa": "Бул Жәрия Оферта (бундан әри \"Оферта\") EduSelf платформасы (бундан әри \"Платформа\") усынатуғын қызметлерди пайдаланыў шартларын белгилейди.",
        "tg": "Ин Пешниҳоди Умумӣ (минбаъд \"Пешниҳод\") шартҳои истифодаи хидматҳои пешниҳодшудаи платформаи EduSelf (минбаъд \"Платформа\") муайян мекунад.",
        "ky": "Бул Жалпы Сунуш (мындан ары \"Сунуш\") EduSelf платформасы (мындан ары \"Платформа\") сунуштаган кызматтарды пайдалануу шарттарын аныктайт."
    },
    "Platformaga ro'yxatdan o'tish orqali siz ushbu Oferta shartlarini to'liq qabul qilasiz.": {
        "en": "By registering on the Platform, you fully accept the terms of this Offer.",
        "ru": "Регистрируясь на Платформе, вы полностью принимаете условия данной Оферты.",
        "kk": "Платформаға тіркелу арқылы сіз осы Оферта шарттарын толық қабылдайсыз.",
        "kaa": "Платформаға тиркелиў арқылы сиз бул Оферта шартларын толық қабыл қыласыз.",
        "tg": "Бо сабти ном дар Платформа, шумо шартҳои ин Пешниҳодро пурра қабул мекунед.",
        "ky": "Платформага катталуу аркылуу сиз бул Сунуштун шарттарын толук кабыл аласыз."
    },
    "Platforma quyidagi xizmatlarni taqdim etadi:": {
        "en": "The Platform provides the following services:",
        "ru": "Платформа предоставляет следующие услуги:",
        "kk": "Платформа келесі қызметтерді ұсынады:",
        "kaa": "Платформа төмендеги қызметлерди усынады:",
        "tg": "Платформа хидматҳои зеринро пешниҳод мекунад:",
        "ky": "Платформа төмөнкү кызматтарды сунуштайт:"
    },
    "Online testlar va imtihonlar": {
        "en": "Online tests and exams",
        "ru": "Онлайн тесты и экзамены",
        "kk": "Онлайн тесттер мен емтихандар",
        "kaa": "Онлайн тестлер ҳәм имтиханлар",
        "tg": "Тестҳо ва имтиҳонҳои онлайн",
        "ky": "Онлайн тесттер жана экзамендер"
    },
    "Ta'lim materiallari": {
        "en": "Educational materials",
        "ru": "Учебные материалы",
        "kk": "Оқу материалдары",
        "kaa": "Оқыў материаллары",
        "tg": "Маводҳои таҳсилӣ",
        "ky": "Окуу материалдары"
    },
    "AI yordamchi": {
        "en": "AI assistant",
        "ru": "AI помощник",
        "kk": "AI көмекші",
        "kaa": "AI жәрдемши",
        "tg": "Ёрдамчии AI",
        "ky": "AI жардамчы"
    },
    "Progress monitoring": {
        "en": "Progress monitoring",
        "ru": "Мониторинг прогресса",
        "kk": "Прогресті бақылау",
        "kaa": "Прогрести бақылаў",
        "tg": "Пайгирии пешрафт",
        "ky": "Прогрессти көзөмөлдөө"
    },
    "Foydalanuvchi quyidagilarga majbur:": {
        "en": "The user is obliged to:",
        "ru": "Пользователь обязан:",
        "kk": "Пайдаланушы міндетті:",
        "kaa": "Пайдаланыўшы мәжбүр:",
        "tg": "Корбар вазифадор аст:",
        "ky": "Колдонуучу милдеттүү:"
    },
    "To'g'ri ma'lumotlar berish": {
        "en": "Provide accurate information",
        "ru": "Предоставлять точную информацию",
        "kk": "Дұрыс ақпарат беру",
        "kaa": "Дурыс мағлыўмат бериў",
        "tg": "Маълумоти дақиқ пешниҳод кардан",
        "ky": "Так маалымат берүү"
    },
    "Parolni maxfiy saqlash": {
        "en": "Keep password confidential",
        "ru": "Хранить пароль в секрете",
        "kk": "Құпия сөзді құпия сақтау",
        "kaa": "Паролды құпия сақлаў",
        "tg": "Рамзро махфӣ нигоҳ доштан",
        "ky": "Сыр сөздү купуя сактоо"
    },
    "Platformadan to'g'ri foydalanish": {
        "en": "Use the Platform correctly",
        "ru": "Правильно использовать Платформу",
        "kk": "Платформаны дұрыс пайдалану",
        "kaa": "Платформадан дурыс пайдаланыў",
        "tg": "Истифодаи дурусти Платформа",
        "ky": "Платформаны туура пайдалануу"
    },
    "Boshqa foydalanuvchilarni hurmat qilish": {
        "en": "Respect other users",
        "ru": "Уважать других пользователей",
        "kk": "Басқа пайдаланушыларды құрметтеу",
        "kaa": "Басқа пайдаланыўшыларды ҳүрмет қылыў",
        "tg": "Корбарони дигарро эҳтиром кардан",
        "ky": "Башка колдонуучуларды урматтоо"
    },
    "Mualliflik huquqlarini hurmat qilish": {
        "en": "Respect copyright",
        "ru": "Уважать авторские права",
        "kk": "Авторлық құқықтарды құрметтеу",
        "kaa": "Авторлық ҳуқықларды ҳүрмет қылыў",
        "tg": "Ҳуқуқи муаллифро эҳтиром кардан",
        "ky": "Автордук укукту урматтоо"
    },
    "Platformaning asosiy xizmatlari bepul. Premium xizmatlar uchun to'lov talab qilinadi.": {
        "en": "The Platform's basic services are free. Payment is required for premium services.",
        "ru": "Основные услуги Платформы бесплатны. Для премиум-услуг требуется оплата.",
        "kk": "Платформаның негізгі қызметтері тегін. Премиум қызметтер үшін төлем қажет.",
        "kaa": "Платформаның негизги қызметлери бепул. Премиум қызметлер ушын төлем талап қылынады.",
        "tg": "Хидматҳои асосии Платформа ройгон аст. Барои хидматҳои премиум пардохт лозим аст.",
        "ky": "Платформанын негизги кызматтары акысыз. Премиум кызматтар үчүн төлөм талап кылынат."
    },
    "To'lovlar Click, Payme va boshqa to'lov tizimlari orqali amalga oshiriladi.": {
        "en": "Payments are made through Click, Payme and other payment systems.",
        "ru": "Платежи осуществляются через Click, Payme и другие платежные системы.",
        "kk": "Төлемдер Click, Payme және басқа төлем жүйелері арқылы жүзеге асырылады.",
        "kaa": "Төлемлер Click, Payme ҳәм басқа төлем жүйелери арқылы амалға асырылады.",
        "tg": "Пардохтҳо тавассути Click, Payme ва дигар системаҳои пардохт анҷом дода мешаванд.",
        "ky": "Төлөмдөр Click, Payme жана башка төлөм системалары аркылуу жүргүзүлөт."
    },
    "Platforma test natijalari va ta'lim materiallarining to'g'riligi uchun mas'uliyat oladi, lekin foydalanuvchining shaxsiy natijalari uchun mas'ul emas.": {
        "en": "The Platform is responsible for the accuracy of test results and educational materials, but is not responsible for the user's personal results.",
        "ru": "Платформа несет ответственность за точность результатов тестов и учебных материалов, но не несет ответственности за личные результаты пользователя.",
        "kk": "Платформа тест нәтижелері мен оқу материалдарының дұрыстығы үшін жауапты, бірақ пайдаланушының жеке нәтижелері үшін жауапты емес.",
        "kaa": "Платформа тест нәтийжелери ҳәм оқыў материалларының дурыслығы ушын жуўапты, бирақ пайдаланыўшының жеке нәтийжелери ушын жуўапты емес.",
        "tg": "Платформа барои дақиқии натиҷаҳои тест ва маводҳои таҳсилӣ масъул аст, аммо барои натиҷаҳои шахсии корбар масъул нест.",
        "ky": "Платформа тест натыйжаларынын жана окуу материалдарынын тактыгы үчүн жооптуу, бирок колдонуучунун жеке натыйжалары үчүн жооптуу эмес."
    },
    "Foydalanuvchi istalgan vaqtda hisobini o'chirish orqali shartnomani bekor qilishi mumkin.": {
        "en": "The user can cancel the contract at any time by deleting their account.",
        "ru": "Пользователь может расторгнуть договор в любое время, удалив свой аккаунт.",
        "kk": "Пайдаланушы кез келген уақытта есептік жазбасын жою арқылы шартты бұза алады.",
        "kaa": "Пайдаланыўшы исталған ўақытта есабын өшириў арқылы шартноманы бийкар қыла алады.",
        "tg": "Корбар метавонад дар ҳар вақт бо нест кардани ҳисоби худ шартномаро бекор кунад.",
        "ky": "Колдонуучу каалаган убакта эсебин өчүрүү аркылуу келишимди жокко чыгара алат."
    },
    "Platforma Oferta shartlarini buzgan foydalanuvchilarning hisobini bloklash huquqiga ega.": {
        "en": "The Platform has the right to block accounts of users who violate the Offer terms.",
        "ru": "Платформа имеет право блокировать аккаунты пользователей, нарушивших условия Оферты.",
        "kk": "Платформа Оферта шарттарын бұзған пайдаланушылардың есептік жазбаларын бұғаттау құқығына ие.",
        "kaa": "Платформа Оферта шартларын бузған пайдаланыўшылардың есабын блоклаў ҳуқықына ийе.",
        "tg": "Платформа ҳуқуқи блок кардани ҳисобҳои корбаронеро дорад, ки шартҳои Пешниҳодро вайрон кардаанд.",
        "ky": "Платформа Сунуш шарттарын бузган колдонуучулардын эсептерин блоктоо укугуна ээ."
    },
    "Platforma Oferta shartlarini o'zgartirish huquqiga ega. O'zgarishlar Platformada e'lon qilinadi.": {
        "en": "The Platform has the right to change the Offer terms. Changes will be announced on the Platform.",
        "ru": "Платформа имеет право изменять условия Оферты. Изменения будут объявлены на Платформе.",
        "kk": "Платформа Оферта шарттарын өзгерту құқығына ие. Өзгерістер Платформада жарияланады.",
        "kaa": "Платформа Оферта шартларын өзгертиў ҳуқықына ийе. Өзгерислер Платформада жәрияланады.",
        "tg": "Платформа ҳуқуқи тағйир додани шартҳои Пешниҳодро дорад. Тағйирот дар Платформа эълон мешаванд.",
        "ky": "Платформа Сунуш шарттарын өзгөртүү укугуна ээ. Өзгөртүүлөр Платформада жарыяланат."
    },
    "Savollar bo'lsa, biz bilan bog'laning:": {
        "en": "If you have questions, contact us:",
        "ru": "Если у вас есть вопросы, свяжитесь с нами:",
        "kk": "Сұрақтарыңыз болса, бізбен байланысыңыз:",
        "kaa": "Сорақларыңыз болса, биз пенен байланысыңыз:",
        "tg": "Агар саволҳо дошта бошед, бо мо тамос гиред:",
        "ky": "Суроолоруңуз болсо, биз менен байланышыңыз:"
    }
}

# Merge new translations
translations.update(new_translations)

# Write back to file
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_translations)} oferta body text translations")
print("Total translations:", len(translations))
