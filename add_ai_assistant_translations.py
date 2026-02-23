import json

# Read existing translations
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Add missing translations for AI assistant pages
new_translations = {
    "AI Yordam Markazi": {
        "en": "AI Help Center",
        "ru": "Центр помощи AI",
        "kk": "AI Көмек орталығы",
        "kaa": "AI Көмек орталығы",
        "tg": "Маркази кӯмаки AI",
        "ky": "AI Жардам борбору"
    },
    "AI Yordam Markazi - EduSelf": {
        "en": "AI Help Center - EduSelf",
        "ru": "Центр помощи AI - EduSelf",
        "kk": "AI Көмек орталығы - EduSelf",
        "kaa": "AI Көмек орталығы - EduSelf",
        "tg": "Маркази кӯмаки AI - EduSelf",
        "ky": "AI Жардам борбору - EduSelf"
    },
    "AI Hamroh bilan tanishing va barcha imkoniyatlardan foydalaning. Sizning shaxsiy ta'lim yordamchingiz har doim yordamga tayyor!": {
        "en": "Get to know AI Assistant and use all features. Your personal education assistant is always ready to help!",
        "ru": "Познакомьтесь с AI Помощником и используйте все возможности. Ваш личный помощник по образованию всегда готов помочь!",
        "kk": "AI Көмекшімен танысыңыз және барлық мүмкіндіктерді пайдаланыңыз. Сіздің жеке білім көмекшіңіз әрқашан көмектесуге дайын!",
        "kaa": "AI Көмекши менен таныс болыңыз ҳәм барлық мүмкиншиликлерден пайдаланыңыз. Сиздиң жеке билим көмекшиңиз ҳәр дайым көмектесиўге тайяр!",
        "tg": "Бо Ёрдамчии AI шинос шавед ва аз ҳамаи имкониятҳо истифода баред. Ёрдамчии шахсии таҳсилии шумо ҳамеша омодаи кӯмак аст!",
        "ky": "AI Жардамчы менен таанышыңыз жана бардык мүмкүнчүлүктөрдү колдонуңуз. Сиздин жеке билим берүү жардамчыңыз ар дайым жардам берүүгө даяр!"
    },
    "Ta'lim muassasalari": {
        "en": "Educational institutions",
        "ru": "Образовательные учреждения",
        "kk": "Білім беру мекемелері",
        "kaa": "Билим бериў муассасалары",
        "tg": "Муассисаҳои таҳсилӣ",
        "ky": "Билим берүү мекемелери"
    },
    "Tezkor Savol": {
        "en": "Quick Question",
        "ru": "Быстрый вопрос",
        "kk": "Жылдам сұрақ",
        "kaa": "Тез сорақ",
        "tg": "Саволи зуд",
        "ky": "Тез суроо"
    },
    "AI Hamrohdan biror narsa so'rashni xohlaysizmi? Savolingizni yozing va darhol javob oling!": {
        "en": "Want to ask AI Assistant something? Write your question and get an instant answer!",
        "ru": "Хотите спросить что-то у AI Помощника? Напишите свой вопрос и получите мгновенный ответ!",
        "kk": "AI Көмекшіден бір нәрсе сұрағыңыз келе ме? Сұрағыңызды жазыңыз және дереу жауап алыңыз!",
        "kaa": "AI Көмекшиден бир нәрсе сорағыңыз келе ме? Сорағыңызды жазыңыз ҳәм дереу жуўап алыңыз!",
        "tg": "Мехоҳед аз Ёрдамчии AI чизе бипурсед? Саволатонро нависед ва дарҳол ҷавоб гиред!",
        "ky": "AI Жардамчыдан бир нерсе сурагыңыз келеби? Суроонузду жазыңыз жана дароо жооп алыңыз!"
    },
    "Savolingiz:": {
        "en": "Your question:",
        "ru": "Ваш вопрос:",
        "kk": "Сұрағыңыз:",
        "kaa": "Сорағыңыз:",
        "tg": "Саволи шумо:",
        "ky": "Суроонуз:"
    },
    "Masalan: Matematika fanini qanday o'rganish kerak?": {
        "en": "For example: How to study Mathematics?",
        "ru": "Например: Как изучать математику?",
        "kk": "Мысалы: Математиканы қалай оқу керек?",
        "kaa": "Мысалы: Математиканы қалай оқыў керек?",
        "tg": "Масалан: Чӣ тавр математикаро омӯхтан лозим аст?",
        "ky": "Мисалы: Математиканы кантип окуу керек?"
    },
    "Kategoriya:": {
        "en": "Category:",
        "ru": "Категория:",
        "kk": "Санат:",
        "kaa": "Категория:",
        "tg": "Категория:",
        "ky": "Категория:"
    },
    "Umumiy": {
        "en": "General",
        "ru": "Общее",
        "kk": "Жалпы",
        "kaa": "Жалпы",
        "tg": "Умумӣ",
        "ky": "Жалпы"
    },
    "Fan bo'yicha yordam": {
        "en": "Subject help",
        "ru": "Помощь по предмету",
        "kk": "Пән бойынша көмек",
        "kaa": "Фан бойынша көмек",
        "tg": "Кӯмак дар фан",
        "ky": "Предмет боюнча жардам"
    },
    "Muassasa tanlash": {
        "en": "Institution selection",
        "ru": "Выбор учреждения",
        "kk": "Мекеме таңдау",
        "kaa": "Муассаса таңлаў",
        "tg": "Интихоби муассиса",
        "ky": "Мекеме тандоо"
    },
    "Sertifikat yo'riqnomasi": {
        "en": "Certificate guide",
        "ru": "Руководство по сертификату",
        "kk": "Сертификат нұсқаулығы",
        "kaa": "Сертификат нусқаўлығы",
        "tg": "Дастури сертификат",
        "ky": "Сертификат колдонмосу"
    },
    "Savol yuborish": {
        "en": "Send question",
        "ru": "Отправить вопрос",
        "kk": "Сұрақ жіберу",
        "kaa": "Сорақ жибериў",
        "tg": "Фиристодани савол",
        "ky": "Суроо жөнөтүү"
    },
    "Fanlar bo'yicha yordam": {
        "en": "Subject help",
        "ru": "Помощь по предметам",
        "kk": "Пәндер бойынша көмек",
        "kaa": "Фанлар бойынша көмек",
        "tg": "Кӯмак дар фанҳо",
        "ky": "Предметтер боюнча жардам"
    },
    "Matematika, fizika, kimya va boshqa fanlar bo'yicha savollaringizga batafsil javoblar olish": {
        "en": "Get detailed answers to your questions on mathematics, physics, chemistry and other subjects",
        "ru": "Получите подробные ответы на ваши вопросы по математике, физике, химии и другим предметам",
        "kk": "Математика, физика, химия және басқа пәндер бойынша сұрақтарыңызға толық жауаптар алыңыз",
        "kaa": "Математика, физика, химия ҳәм басқа фанлар бойынша сорақларыңызға толық жуўаплар алыңыз",
        "tg": "Ба саволҳои худ дар бораи математика, физика, химия ва дигар фанҳо ҷавобҳои муфассал гиред",
        "ky": "Математика, физика, химия жана башка предметтер боюнча суроолоруңузга толук жоопторду алыңыз"
    },
    "Sizning ehtiyojlaringizga mos ta'lim muassasalarini topish va taqqoslash": {
        "en": "Find and compare educational institutions that suit your needs",
        "ru": "Найдите и сравните образовательные учреждения, соответствующие вашим потребностям",
        "kk": "Сіздің қажеттіліктеріңізге сәйкес келетін білім беру мекемелерін табыңыз және салыстырыңыз",
        "kaa": "Сиздиң қәжетликлериңизге сәйкес келетуғын билим бериў муассасаларын табыңыз ҳәм салыстырыңыз",
        "tg": "Муассисаҳои таҳсилиеро, ки ба эҳтиёҷоти шумо мувофиқанд, ёбед ва муқоиса кунед",
        "ky": "Сиздин керектөөлөрүңүзгө ылайыктуу билим берүү мекемелерин табыңыз жана салыштырыңыз"
    },
    "Turli sertifikatlar haqida ma'lumot va ularni qanday olish bo'yicha maslahatlar": {
        "en": "Information about various certificates and tips on how to get them",
        "ru": "Информация о различных сертификатах и советы по их получению",
        "kk": "Әртүрлі сертификаттар туралы ақпарат және оларды қалай алу туралы кеңестер",
        "kaa": "Түрли сертификатлар ҳаққында ақпарат ҳәм оларды қалай алыў бойынша кеңеслер",
        "tg": "Маълумот дар бораи сертификатҳои гуногун ва маслиҳатҳо оид ба гирифтани онҳо",
        "ky": "Ар кандай сертификаттар жөнүндө маалымат жана аларды кантип алуу боюнча кеңештер"
    },
    "Tez-tez so'raladigan savollar": {
        "en": "Frequently asked questions",
        "ru": "Часто задаваемые вопросы",
        "kk": "Жиі қойылатын сұрақтар",
        "kaa": "Жий қойылатуғын сорақлар",
        "tg": "Саволҳои зуд-зуд пурсида мешаванда",
        "ky": "Көп берилүүчү суроолор"
    },
    "AI Hamroh bilan suhbatni boshlang!": {
        "en": "Start a conversation with AI Assistant!",
        "ru": "Начните разговор с AI Помощником!",
        "kk": "AI Көмекшімен сөйлесуді бастаңыз!",
        "kaa": "AI Көмекши менен сөйлесиўди баслаңыз!",
        "tg": "Сӯҳбатро бо Ёрдамчии AI оғоз кунед!",
        "ky": "AI Жардамчы менен маектешүүнү баштаңыз!"
    },
    "Suhbatni boshlash": {
        "en": "Start chat",
        "ru": "Начать чат",
        "kk": "Сөйлесуді бастау",
        "kaa": "Сөйлесиўди баслаў",
        "tg": "Оғози сӯҳбат",
        "ky": "Маектешүүнү баштоо"
    },
    "AI Hamroh - EduSelf": {
        "en": "AI Assistant - EduSelf",
        "ru": "AI Помощник - EduSelf",
        "kk": "AI Көмекші - EduSelf",
        "kaa": "AI Көмекші - EduSelf",
        "tg": "Ёрдамчии AI - EduSelf",
        "ky": "AI Жардамчы - EduSelf"
    },
    "Online": {
        "en": "Online",
        "ru": "Онлайн",
        "kk": "Онлайн",
        "kaa": "Онлайн",
        "tg": "Онлайн",
        "ky": "Онлайн"
    },
    "Tozalash": {
        "en": "Clear",
        "ru": "Очистить",
        "kk": "Тазалау",
        "kaa": "Тазалаў",
        "tg": "Тоза кардан",
        "ky": "Тазалоо"
    },
    "Yangi suhbat": {
        "en": "New chat",
        "ru": "Новый чат",
        "kk": "Жаңа сөйлесу",
        "kaa": "Жаңа сөйлесиў",
        "tg": "Сӯҳбати нав",
        "ky": "Жаңы маек"
    },
    "Salom, {{ user.first_name|default:user.username }}! 👋": {
        "en": "Hello, {{ user.first_name|default:user.username }}! 👋",
        "ru": "Привет, {{ user.first_name|default:user.username }}! 👋",
        "kk": "Сәлем, {{ user.first_name|default:user.username }}! 👋",
        "kaa": "Салам, {{ user.first_name|default:user.username }}! 👋",
        "tg": "Салом, {{ user.first_name|default:user.username }}! 👋",
        "ky": "Салам, {{ user.first_name|default:user.username }}! 👋"
    },
    "Men sizning shaxsiy AI yordamchingizman": {
        "en": "I am your personal AI assistant",
        "ru": "Я ваш личный AI помощник",
        "kk": "Мен сіздің жеке AI көмекшіңізбін",
        "kaa": "Мен сиздиң жеке AI көмекшиңизбин",
        "tg": "Ман ёрдамчии шахсии AI-и шумо ҳастам",
        "ky": "Мен сиздин жеке AI жардамчыңызмын"
    },
    "Matematika bo'yicha qanday testlar bor?": {
        "en": "What tests are available in Mathematics?",
        "ru": "Какие тесты есть по математике?",
        "kk": "Математика бойынша қандай тесттер бар?",
        "kaa": "Математика бойынша қандай тестлер бар?",
        "tg": "Дар математика чӣ гуна тестҳо мавҷуданд?",
        "ky": "Математика боюнча кандай тесттер бар?"
    },
    "Matematika testlari": {
        "en": "Mathematics tests",
        "ru": "Тесты по математике",
        "kk": "Математика тесттері",
        "kaa": "Математика тестлери",
        "tg": "Тестҳои математика",
        "ky": "Математика тесттери"
    },
    "Qanday qilib sertifikat olish mumkin?": {
        "en": "How can I get a certificate?",
        "ru": "Как можно получить сертификат?",
        "kk": "Сертификатты қалай алуға болады?",
        "kaa": "Сертификатты қалай алыўға болады?",
        "tg": "Чӣ тавр сертификат гирифтан мумкин аст?",
        "ky": "Сертификатты кантип алса болот?"
    },
    "Sertifikat olish": {
        "en": "Get certificate",
        "ru": "Получить сертификат",
        "kk": "Сертификат алу",
        "kaa": "Сертификат алыў",
        "tg": "Гирифтани сертификат",
        "ky": "Сертификат алуу"
    },
    "Eng yaxshi universitetlar haqida ma'lumot bering": {
        "en": "Give information about the best universities",
        "ru": "Дайте информацию о лучших университетах",
        "kk": "Ең жақсы университеттер туралы ақпарат беріңіз",
        "kaa": "Ең жақсы университетлер ҳаққында ақпарат бериңиз",
        "tg": "Маълумот дар бораи беҳтарин донишгоҳҳо диҳед",
        "ky": "Эң мыкты университеттер жөнүндө маалымат бериңиз"
    },
    "Top universitetlar": {
        "en": "Top universities",
        "ru": "Топ университеты",
        "kk": "Топ университеттер",
        "kaa": "Топ университетлер",
        "tg": "Донишгоҳҳои болоӣ",
        "ky": "Топ университеттер"
    },
    "Xabar yozing...": {
        "en": "Write a message...",
        "ru": "Напишите сообщение...",
        "kk": "Хабар жазыңыз...",
        "kaa": "Хабар жазыңыз...",
        "tg": "Паём нависед...",
        "ky": "Билдирүү жазыңыз..."
    },
    "Suhbatni tozalash": {
        "en": "Clear chat",
        "ru": "Очистить чат",
        "kk": "Сөйлесуді тазалау",
        "kaa": "Сөйлесиўди тазалаў",
        "tg": "Тоза кардани сӯҳбат",
        "ky": "Маекти тазалоо"
    },
    "Suhbatni tozalashni xohlaysizmi?": {
        "en": "Do you want to clear the chat?",
        "ru": "Хотите очистить чат?",
        "kk": "Сөйлесуді тазалағыңыз келе ме?",
        "kaa": "Сөйлесиўди тазалағыңыз келе ме?",
        "tg": "Мехоҳед сӯҳбатро тоза кунед?",
        "ky": "Маекти тазалагыңыз келеби?"
    },
    "Ha, tozalash": {
        "en": "Yes, clear",
        "ru": "Да, очистить",
        "kk": "Иә, тазалау",
        "kaa": "Ия, тазалаў",
        "tg": "Бале, тоза кунед",
        "ky": "Ооба, тазалоо"
    },
    "Salom! 👋": {
        "en": "Hello! 👋",
        "ru": "Привет! 👋",
        "kk": "Сәлем! 👋",
        "kaa": "Салам! 👋",
        "tg": "Салом! 👋",
        "ky": "Салам! 👋"
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
