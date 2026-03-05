"""
TEXNOLOGIYA - 60 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_technology():
    cat, _ = SubjectCategory.objects.get_or_create(slug='umumiy-fanlar', defaults={'name': 'Umumiy fanlar', 'icon': 'bi-book', 'order': 1, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Texnologiya', defaults={'category': cat, 'description': 'Texnologiya fani - zamonaviy texnologiyalar va ularning hayotdagi qo\'llanilishi', 'icon': 'bi-gear', 'order': 15, 'is_active': True})
    return subj

def add_topics(subject, topics_data):
    for td in topics_data:
        topic, created = Topic.objects.get_or_create(subject=subject, name=td['n'], defaults={'time_limit': td['t'], 'passing_score': 60, 'order': td['o'], 'is_active': True})
        print(f"{'✅' if created else 'ℹ️'} §{td['o']}: {td['n']} ({len(td['q'])} test)")
        for i, qd in enumerate(td['q']):
            q, qc = Question.objects.get_or_create(topic=topic, text=qd['t'], defaults={'points': 10, 'order': i + 1})
            if qc:
                answers = qd['a'].copy()
                random.shuffle(answers)
                for ad in answers:
                    Answer.objects.create(question=q, text=ad['t'], is_correct=ad['c'])

# 60 TA MAVZU
T = [
    {'n': 'Texnologiya faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Texnologiya nima?', 'a': [{'t': 'Ilmiy bilimlarni amaliy maqsadlarda qo\'llash', 'c': True}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat telefonlar', 'c': False}]},
        {'t': 'Texnologiya hayotimizda qanday rol o\'ynaydi?', 'a': [{'t': 'Hayotni osonlashtiradi va samaradorlikni oshiradi', 'c': True}, {'t': 'Hech qanday rol o\'ynamaydi', 'c': False}, {'t': 'Faqat muammolar yaratadi', 'c': False}, {'t': 'Faqat o\'yin-kulgi uchun', 'c': False}]},
        {'t': 'Zamonaviy texnologiyalarga qaysilar kiradi?', 'a': [{'t': 'Kompyuter, internet, sun\'iy intellekt, robotlar', 'c': True}, {'t': 'Faqat telefonlar', 'c': False}, {'t': 'Faqat televizorlar', 'c': False}, {'t': 'Faqat kitoblar', 'c': False}]},
        {'t': 'Texnologiya rivojlanishi nimaga olib keladi?', 'a': [{'t': 'Yangi imkoniyatlar va innovatsiyalar paydo bo\'ladi', 'c': True}, {'t': 'Hech narsaga olib kelmaydi', 'c': False}, {'t': 'Faqat qimmatroq mahsulotlar', 'c': False}, {'t': 'Faqat muammolar', 'c': False}]},
        {'t': 'Texnologiya fanini o\'rganish nima uchun muhim?', 'a': [{'t': 'Zamonaviy dunyoda muvaffaqiyatli bo\'lish uchun', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat dasturchilar uchun', 'c': False}, {'t': 'Faqat o\'qituvchilar uchun', 'c': False}]},
    ]},

    {'n': 'Kompyuter asoslari', 't': 25, 'o': 2, 'q': [
        {'t': 'Kompyuter nima?', 'a': [{'t': 'Ma\'lumotlarni qayta ishlaydigan elektron qurilma', 'c': True}, {'t': 'Faqat o\'yin o\'ynaydigan qurilma', 'c': False}, {'t': 'Faqat internet uchun', 'c': False}, {'t': 'Faqat hisoblash uchun', 'c': False}]},
        {'t': 'Kompyuterning asosiy qismlari qaysilar?', 'a': [{'t': 'Protsessor, xotira, qattiq disk, monitor, klaviatura', 'c': True}, {'t': 'Faqat monitor', 'c': False}, {'t': 'Faqat klaviatura', 'c': False}, {'t': 'Faqat sichqoncha', 'c': False}]},
        {'t': 'Protsessor (CPU) nima vazifani bajaradi?', 'a': [{'t': 'Barcha hisob-kitoblarni amalga oshiradi', 'c': True}, {'t': 'Faqat ma\'lumot saqlaydi', 'c': False}, {'t': 'Faqat rasm ko\'rsatadi', 'c': False}, {'t': 'Faqat ovoz chiqaradi', 'c': False}]},
        {'t': 'RAM (operativ xotira) nima?', 'a': [{'t': 'Vaqtinchalik ma\'lumotlarni saqlaydigan tez xotira', 'c': True}, {'t': 'Doimiy ma\'lumot saqlash joyi', 'c': False}, {'t': 'Faqat rasmlar uchun', 'c': False}, {'t': 'Faqat musiqa uchun', 'c': False}]},
        {'t': 'Qattiq disk (HDD/SSD) nima uchun kerak?', 'a': [{'t': 'Ma\'lumotlarni doimiy saqlash uchun', 'c': True}, {'t': 'Faqat vaqtinchalik saqlash uchun', 'c': False}, {'t': 'Faqat hisoblash uchun', 'c': False}, {'t': 'Faqat internet uchun', 'c': False}]},
        {'t': 'Monitor nima vazifani bajaradi?', 'a': [{'t': 'Ma\'lumotlarni ekranda ko\'rsatadi', 'c': True}, {'t': 'Ma\'lumot kiritadi', 'c': False}, {'t': 'Hisoblash bajaradi', 'c': False}, {'t': 'Ovoz chiqaradi', 'c': False}]},
    ]},

    {'n': 'Operatsion tizimlar', 't': 25, 'o': 3, 'q': [
        {'t': 'Operatsion tizim nima?', 'a': [{'t': 'Kompyuter resurslarini boshqaradigan asosiy dastur', 'c': True}, {'t': 'Oddiy o\'yin', 'c': False}, {'t': 'Internet brauzer', 'c': False}, {'t': 'Matn muharriri', 'c': False}]},
        {'t': 'Mashhur operatsion tizimlar qaysilar?', 'a': [{'t': 'Windows, macOS, Linux, Android, iOS', 'c': True}, {'t': 'Faqat Windows', 'c': False}, {'t': 'Faqat Android', 'c': False}, {'t': 'Faqat iOS', 'c': False}]},
        {'t': 'Windows operatsion tizimi kim tomonidan yaratilgan?', 'a': [{'t': 'Microsoft kompaniyasi', 'c': True}, {'t': 'Apple kompaniyasi', 'c': False}, {'t': 'Google kompaniyasi', 'c': False}, {'t': 'Samsung kompaniyasi', 'c': False}]},
        {'t': 'Linux operatsion tizimining asosiy xususiyati nima?', 'a': [{'t': 'Ochiq kodli va bepul', 'c': True}, {'t': 'Juda qimmat', 'c': False}, {'t': 'Faqat telefonlar uchun', 'c': False}, {'t': 'Faqat o\'yinlar uchun', 'c': False}]},
        {'t': 'Android operatsion tizimi qaysi qurilmalar uchun?', 'a': [{'t': 'Smartfonlar va planshetlar uchun', 'c': True}, {'t': 'Faqat kompyuterlar uchun', 'c': False}, {'t': 'Faqat televizorlar uchun', 'c': False}, {'t': 'Faqat soatlar uchun', 'c': False}]},
    ]},

    {'n': 'Dasturiy ta\'minot turlari', 't': 25, 'o': 4, 'q': [
        {'t': 'Dasturiy ta\'minot nima?', 'a': [{'t': 'Kompyuterda bajariladigan dasturlar to\'plami', 'c': True}, {'t': 'Faqat kompyuter qismlari', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat klaviatura', 'c': False}]},
        {'t': 'Tizim dasturiy ta\'minoti nima?', 'a': [{'t': 'Operatsion tizim va drayverlarga', 'c': True}, {'t': 'Faqat o\'yinlar', 'c': False}, {'t': 'Faqat brauzerlar', 'c': False}, {'t': 'Faqat matn muharrirlari', 'c': False}]},
        {'t': 'Amaliy dasturiy ta\'minot nima?', 'a': [{'t': 'Foydalanuvchi vazifalarini bajaradigan dasturlar', 'c': True}, {'t': 'Faqat operatsion tizim', 'c': False}, {'t': 'Faqat drayverlarga', 'c': False}, {'t': 'Faqat viruslar', 'c': False}]},
        {'t': 'Qaysi dasturlar amaliy dasturlarga kiradi?', 'a': [{'t': 'Word, Excel, Photoshop, Chrome', 'c': True}, {'t': 'Faqat Windows', 'c': False}, {'t': 'Faqat Linux', 'c': False}, {'t': 'Faqat drayverlarga', 'c': False}]},
        {'t': 'Drayver nima?', 'a': [{'t': 'Qurilmalarni boshqaradigan maxsus dastur', 'c': True}, {'t': 'O\'yin dasturi', 'c': False}, {'t': 'Brauzer', 'c': False}, {'t': 'Matn muharriri', 'c': False}]},
        {'t': 'Ochiq kodli dastur nima?', 'a': [{'t': 'Manba kodi ochiq va bepul dastur', 'c': True}, {'t': 'Juda qimmat dastur', 'c': False}, {'t': 'Faqat Windows uchun', 'c': False}, {'t': 'Faqat o\'yinlar', 'c': False}]},
    ]},

    {'n': 'Internet asoslari', 't': 25, 'o': 5, 'q': [
        {'t': 'Internet nima?', 'a': [{'t': 'Butun dunyo bo\'ylab kompyuterlar tarmog\'i', 'c': True}, {'t': 'Faqat bitta kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat televizor', 'c': False}]},
        {'t': 'WWW (World Wide Web) nima?', 'a': [{'t': 'Internet orqali ma\'lumot almashish tizimi', 'c': True}, {'t': 'Faqat elektron pochta', 'c': False}, {'t': 'Faqat o\'yinlar', 'c': False}, {'t': 'Faqat musiqa', 'c': False}]},
        {'t': 'Brauzer nima?', 'a': [{'t': 'Veb-saytlarni ko\'rish uchun dastur', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'O\'yin dasturi', 'c': False}, {'t': 'Rasm muharriri', 'c': False}]},
        {'t': 'Mashhur brauzerlar qaysilar?', 'a': [{'t': 'Chrome, Firefox, Safari, Edge', 'c': True}, {'t': 'Faqat Word', 'c': False}, {'t': 'Faqat Excel', 'c': False}, {'t': 'Faqat PowerPoint', 'c': False}]},
        {'t': 'URL nima?', 'a': [{'t': 'Veb-sayt manzili', 'c': True}, {'t': 'Parol', 'c': False}, {'t': 'Foydalanuvchi nomi', 'c': False}, {'t': 'Elektron pochta', 'c': False}]},
        {'t': 'HTTP nima?', 'a': [{'t': 'Veb-sahifalarni uzatish protokoli', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Operatsion tizim', 'c': False}, {'t': 'Brauzer', 'c': False}]},
    ]},

    {'n': 'Elektron pochta', 't': 25, 'o': 6, 'q': [
        {'t': 'Elektron pochta (email) nima?', 'a': [{'t': 'Internet orqali xabar yuborish xizmati', 'c': True}, {'t': 'Oddiy pochta', 'c': False}, {'t': 'Telefon qo\'ng\'irog\'i', 'c': False}, {'t': 'SMS xabari', 'c': False}]},
        {'t': 'Email manzili qanday ko\'rinishda bo\'ladi?', 'a': [{'t': 'ism@domen.uz', 'c': True}, {'t': 'www.sayt.uz', 'c': False}, {'t': '+998901234567', 'c': False}, {'t': 'C:\\fayl.txt', 'c': False}]},
        {'t': 'Mashhur email xizmatlari qaysilar?', 'a': [{'t': 'Gmail, Outlook, Yahoo Mail', 'c': True}, {'t': 'Faqat Telegram', 'c': False}, {'t': 'Faqat WhatsApp', 'c': False}, {'t': 'Faqat Facebook', 'c': False}]},
        {'t': 'Email orqali nima yuborish mumkin?', 'a': [{'t': 'Matn, rasm, video, hujjatlar', 'c': True}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Spam nima?', 'a': [{'t': 'Keraksiz va zararli xabarlar', 'c': True}, {'t': 'Muhim xabarlar', 'c': False}, {'t': 'Do\'stlardan xabarlar', 'c': False}, {'t': 'Ish xabarlari', 'c': False}]},
    ]},

    {'n': 'Ijtimoiy tarmoqlar', 't': 25, 'o': 7, 'q': [
        {'t': 'Ijtimoiy tarmoq nima?', 'a': [{'t': 'Odamlar muloqot qiladigan onlayn platforma', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat email', 'c': False}, {'t': 'Faqat telefon', 'c': False}]},
        {'t': 'Mashhur ijtimoiy tarmoqlar qaysilar?', 'a': [{'t': 'Facebook, Instagram, Twitter, TikTok', 'c': True}, {'t': 'Faqat email', 'c': False}, {'t': 'Faqat SMS', 'c': False}, {'t': 'Faqat telefon', 'c': False}]},
        {'t': 'Ijtimoiy tarmoqlar nima uchun ishlatiladi?', 'a': [{'t': 'Muloqot, ma\'lumot almashish, do\'stlar topish', 'c': True}, {'t': 'Faqat o\'yin o\'ynash', 'c': False}, {'t': 'Faqat rasm ko\'rish', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Ijtimoiy tarmoqlarda xavfsizlik qoidalari?', 'a': [{'t': 'Shaxsiy ma\'lumotlarni oshkor qilmaslik', 'c': True}, {'t': 'Hamma narsani baham ko\'rish', 'c': False}, {'t': 'Parolni barchaga aytish', 'c': False}, {'t': 'Notanish odamlarni ishonish', 'c': False}]},
        {'t': 'Telegram nima?', 'a': [{'t': 'Xavfsiz messenger va ijtimoiy tarmoq', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat brauzer', 'c': False}, {'t': 'Operatsion tizim', 'c': False}]},
    ]},

    {'n': 'Kiberbezopaslik asoslari', 't': 30, 'o': 8, 'q': [
        {'t': 'Kiberbezopaslik nima?', 'a': [{'t': 'Kompyuter va ma\'lumotlarni himoya qilish', 'c': True}, {'t': 'Faqat antivirus', 'c': False}, {'t': 'Faqat parol', 'c': False}, {'t': 'Faqat internet', 'c': False}]},
        {'t': 'Virus nima?', 'a': [{'t': 'Kompyuterga zarar yetkazadigan zararli dastur', 'c': True}, {'t': 'Foydali dastur', 'c': False}, {'t': 'O\'yin', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Antivirus dastur nima qiladi?', 'a': [{'t': 'Viruslarni topadi va yo\'q qiladi', 'c': True}, {'t': 'Faqat internetni tezlashtiradi', 'c': False}, {'t': 'Faqat rasm ko\'rsatadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Kuchli parol qanday bo\'lishi kerak?', 'a': [{'t': 'Uzun, harflar, raqamlar va belgilar aralash', 'c': True}, {'t': 'Faqat 123456', 'c': False}, {'t': 'Faqat ismingiz', 'c': False}, {'t': 'Faqat tug\'ilgan kuningiz', 'c': False}]},
        {'t': 'Phishing nima?', 'a': [{'t': 'Shaxsiy ma\'lumotlarni o\'g\'irlash uchun aldash', 'c': True}, {'t': 'Baliq ovlash', 'c': False}, {'t': 'O\'yin o\'ynash', 'c': False}, {'t': 'Rasm chizish', 'c': False}]},
        {'t': 'Ikki bosqichli autentifikatsiya nima?', 'a': [{'t': 'Paroldan tashqari qo\'shimcha himoya', 'c': True}, {'t': 'Faqat parol', 'c': False}, {'t': 'Faqat foydalanuvchi nomi', 'c': False}, {'t': 'Hech qanday himoya', 'c': False}]},
    ]},

    {'n': 'Bulutli texnologiyalar', 't': 25, 'o': 9, 'q': [
        {'t': 'Bulutli texnologiya (Cloud) nima?', 'a': [{'t': 'Internet orqali ma\'lumot saqlash va xizmatlar', 'c': True}, {'t': 'Faqat ob-havo', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}]},
        {'t': 'Bulutli xizmatlarning afzalliklari?', 'a': [{'t': 'Har yerdan kirish, xavfsizlik, tejamkorlik', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat sekin', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Mashhur bulutli xizmatlar qaysilar?', 'a': [{'t': 'Google Drive, Dropbox, iCloud, OneDrive', 'c': True}, {'t': 'Faqat email', 'c': False}, {'t': 'Faqat brauzer', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Google Drive nima uchun ishlatiladi?', 'a': [{'t': 'Fayllarni saqlash va baham ko\'rish', 'c': True}, {'t': 'Faqat o\'yin o\'ynash', 'c': False}, {'t': 'Faqat musiqa tinglash', 'c': False}, {'t': 'Faqat video ko\'rish', 'c': False}]},
        {'t': 'Bulutda ma\'lumotlar xavfsizmi?', 'a': [{'t': 'Ha, shifrlangan va zaxira nusxalari bor', 'c': True}, {'t': 'Yo\'q, umuman xavfsiz emas', 'c': False}, {'t': 'Faqat ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Mobil qurilmalar', 't': 25, 'o': 10, 'q': [
        {'t': 'Smartfon nima?', 'a': [{'t': 'Ko\'p funksiyali aqlli telefon', 'c': True}, {'t': 'Oddiy telefon', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Faqat soat', 'c': False}]},
        {'t': 'Smartfonning asosiy funksiyalari?', 'a': [{'t': 'Qo\'ng\'iroq, internet, ilova, kamera, GPS', 'c': True}, {'t': 'Faqat qo\'ng\'iroq', 'c': False}, {'t': 'Faqat SMS', 'c': False}, {'t': 'Faqat soat', 'c': False}]},
        {'t': 'Planshet nima?', 'a': [{'t': 'Katta ekranli portativ kompyuter', 'c': True}, {'t': 'Kichik telefon', 'c': False}, {'t': 'Faqat kitob', 'c': False}, {'t': 'Faqat daftar', 'c': False}]},
        {'t': 'Mobil ilovalar qayerdan yuklab olinadi?', 'a': [{'t': 'App Store, Google Play kabi do\'konlardan', 'c': True}, {'t': 'Faqat kompyuterdan', 'c': False}, {'t': 'Faqat televizordan', 'c': False}, {'t': 'Yuklab bo\'lmaydi', 'c': False}]},
        {'t': 'GPS nima?', 'a': [{'t': 'Global joylashuvni aniqlash tizimi', 'c': True}, {'t': 'O\'yin', 'c': False}, {'t': 'Brauzer', 'c': False}, {'t': 'Messenger', 'c': False}]},
        {'t': 'Smartfonni qanday himoya qilish kerak?', 'a': [{'t': 'Parol, barmoq izi, yuz tanish', 'c': True}, {'t': 'Hech qanday himoya kerak emas', 'c': False}, {'t': 'Faqat qulfga qo\'yish', 'c': False}, {'t': 'Faqat yashirish', 'c': False}]},
    ]},

    {'n': 'Raqamli kamera va fotosurat', 't': 25, 'o': 11, 'q': [
        {'t': 'Raqamli kamera qanday ishlaydi?', 'a': [{'t': 'Yorug\'likni raqamli signalga aylantiradi', 'c': True}, {'t': 'Faqat plyonka ishlatadi', 'c': False}, {'t': 'Faqat qog\'ozga chizadi', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'Megapiksel nima?', 'a': [{'t': 'Rasm sifatini belgilovchi o\'lchov birligi', 'c': True}, {'t': 'Kamera og\'irligi', 'c': False}, {'t': 'Kamera narxi', 'c': False}, {'t': 'Kamera rangi', 'c': False}]},
        {'t': 'Smartfon kamerasi qanday rivojlandi?', 'a': [{'t': 'Sifat oshdi, ko\'p linzali bo\'ldi', 'c': True}, {'t': 'Hech qanday o\'zgarmadi', 'c': False}, {'t': 'Faqat yomonlashdi', 'c': False}, {'t': 'Butunlay yo\'qoldi', 'c': False}]},
        {'t': 'Raqamli rasmlar qaysi formatlarda saqlanadi?', 'a': [{'t': 'JPEG, PNG, RAW, HEIC', 'c': True}, {'t': 'Faqat TXT', 'c': False}, {'t': 'Faqat DOC', 'c': False}, {'t': 'Faqat PDF', 'c': False}]},
        {'t': 'Rasm tahrirlash dasturlari qaysilar?', 'a': [{'t': 'Photoshop, GIMP, Lightroom', 'c': True}, {'t': 'Faqat Word', 'c': False}, {'t': 'Faqat Excel', 'c': False}, {'t': 'Faqat PowerPoint', 'c': False}]},
    ]},

    {'n': 'Video texnologiyalari', 't': 25, 'o': 12, 'q': [
        {'t': 'Raqamli video qanday ishlaydi?', 'a': [{'t': 'Ketma-ket kadrlarni tez ko\'rsatish', 'c': True}, {'t': 'Faqat bitta rasm', 'c': False}, {'t': 'Faqat ovoz', 'c': False}, {'t': 'Hech qanday harakat yo\'q', 'c': False}]},
        {'t': 'Video sifatini nima belgilaydi?', 'a': [{'t': 'Ruxsat (resolution), kadr tezligi, bitrate', 'c': True}, {'t': 'Faqat fayl hajmi', 'c': False}, {'t': 'Faqat fayl nomi', 'c': False}, {'t': 'Faqat fayl formati', 'c': False}]},
        {'t': 'HD, Full HD, 4K nima?', 'a': [{'t': 'Video ruxsat (sifat) darajalari', 'c': True}, {'t': 'Video formatlari', 'c': False}, {'t': 'Video dasturlari', 'c': False}, {'t': 'Video kameralari', 'c': False}]},
        {'t': 'Mashhur video formatlar qaysilar?', 'a': [{'t': 'MP4, AVI, MOV, MKV', 'c': True}, {'t': 'Faqat JPG', 'c': False}, {'t': 'Faqat PNG', 'c': False}, {'t': 'Faqat TXT', 'c': False}]},
        {'t': 'Video tahrirlash dasturlari qaysilar?', 'a': [{'t': 'Adobe Premiere, Final Cut, DaVinci Resolve', 'c': True}, {'t': 'Faqat Word', 'c': False}, {'t': 'Faqat Excel', 'c': False}, {'t': 'Faqat Paint', 'c': False}]},
        {'t': 'YouTube nima?', 'a': [{'t': 'Video baham ko\'rish platformasi', 'c': True}, {'t': 'Faqat musiqa platformasi', 'c': False}, {'t': 'Faqat o\'yin platformasi', 'c': False}, {'t': 'Faqat kitob platformasi', 'c': False}]},
    ]},

    {'n': 'Audio texnologiyalari', 't': 25, 'o': 13, 'q': [
        {'t': 'Raqamli audio qanday ishlaydi?', 'a': [{'t': 'Analog ovozni raqamli signalga aylantiradi', 'c': True}, {'t': 'Faqat kasetada saqlaydi', 'c': False}, {'t': 'Faqat plastinkada saqlaydi', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'Mashhur audio formatlar qaysilar?', 'a': [{'t': 'MP3, WAV, FLAC, AAC', 'c': True}, {'t': 'Faqat MP4', 'c': False}, {'t': 'Faqat AVI', 'c': False}, {'t': 'Faqat JPG', 'c': False}]},
        {'t': 'MP3 nima?', 'a': [{'t': 'Siqilgan audio format', 'c': True}, {'t': 'Video format', 'c': False}, {'t': 'Rasm format', 'c': False}, {'t': 'Matn format', 'c': False}]},
        {'t': 'Audio tahrirlash dasturlari qaysilar?', 'a': [{'t': 'Audacity, Adobe Audition, FL Studio', 'c': True}, {'t': 'Faqat Word', 'c': False}, {'t': 'Faqat Excel', 'c': False}, {'t': 'Faqat Paint', 'c': False}]},
        {'t': 'Podcast nima?', 'a': [{'t': 'Audio yoki video ko\'rsatuvlar seriyasi', 'c': True}, {'t': 'Faqat musiqa', 'c': False}, {'t': 'Faqat kitob', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
    ]},

    {'n': 'Matn muharrirlari', 't': 25, 'o': 14, 'q': [
        {'t': 'Matn muharriri nima?', 'a': [{'t': 'Matn yozish va tahrirlash dasturi', 'c': True}, {'t': 'Faqat rasm chizish dasturi', 'c': False}, {'t': 'Faqat video tahrirlash dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Microsoft Word nima uchun ishlatiladi?', 'a': [{'t': 'Hujjatlar yaratish va formatlash', 'c': True}, {'t': 'Faqat hisob-kitob', 'c': False}, {'t': 'Faqat taqdimot', 'c': False}, {'t': 'Faqat rasm chizish', 'c': False}]},
        {'t': 'Word da qanday formatlar mavjud?', 'a': [{'t': 'Shrift, o\'lcham, rang, hizalash', 'c': True}, {'t': 'Faqat qora matn', 'c': False}, {'t': 'Hech qanday format yo\'q', 'c': False}, {'t': 'Faqat bitta shrift', 'c': False}]},
        {'t': 'Google Docs nima?', 'a': [{'t': 'Onlayn matn muharriri', 'c': True}, {'t': 'Faqat offline dastur', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat brauzer', 'c': False}]},
        {'t': 'Matn hujjatlarini qanday saqlash mumkin?', 'a': [{'t': 'DOCX, PDF, TXT, RTF formatlarida', 'c': True}, {'t': 'Faqat JPG', 'c': False}, {'t': 'Faqat MP3', 'c': False}, {'t': 'Faqat MP4', 'c': False}]},
    ]},

    {'n': 'Elektron jadvallar', 't': 25, 'o': 15, 'q': [
        {'t': 'Elektron jadval nima?', 'a': [{'t': 'Ma\'lumotlarni jadval ko\'rinishida qayta ishlovchi dastur', 'c': True}, {'t': 'Faqat matn muharriri', 'c': False}, {'t': 'Faqat rasm muharriri', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Microsoft Excel nima uchun ishlatiladi?', 'a': [{'t': 'Hisob-kitoblar, jadvallar, grafiklar yaratish', 'c': True}, {'t': 'Faqat matn yozish', 'c': False}, {'t': 'Faqat rasm chizish', 'c': False}, {'t': 'Faqat video tahrirlash', 'c': False}]},
        {'t': 'Excel da katak (cell) nima?', 'a': [{'t': 'Jadvalning bitta bo\'lagi', 'c': True}, {'t': 'Butun jadval', 'c': False}, {'t': 'Faqat raqam', 'c': False}, {'t': 'Faqat matn', 'c': False}]},
        {'t': 'Excel da formula nima?', 'a': [{'t': 'Avtomatik hisoblash uchun ifoda', 'c': True}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat rang', 'c': False}]},
        {'t': 'Excel da grafik nima uchun kerak?', 'a': [{'t': 'Ma\'lumotlarni vizual ko\'rsatish', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat chop etish uchun', 'c': False}]},
    ]},

    {'n': 'Taqdimot dasturlari', 't': 25, 'o': 16, 'q': [
        {'t': 'Taqdimot dasturi nima?', 'a': [{'t': 'Slaydlar yaratish va ko\'rsatish dasturi', 'c': True}, {'t': 'Faqat matn muharriri', 'c': False}, {'t': 'Faqat jadval dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Microsoft PowerPoint nima uchun ishlatiladi?', 'a': [{'t': 'Taqdimotlar yaratish va ko\'rsatish', 'c': True}, {'t': 'Faqat hisob-kitob', 'c': False}, {'t': 'Faqat matn yozish', 'c': False}, {'t': 'Faqat rasm chizish', 'c': False}]},
        {'t': 'Slayd nima?', 'a': [{'t': 'Taqdimotning bitta sahifasi', 'c': True}, {'t': 'Butun taqdimot', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
        {'t': 'Yaxshi taqdimot qanday bo\'lishi kerak?', 'a': [{'t': 'Qisqa, aniq, vizual, qiziqarli', 'c': True}, {'t': 'Juda uzun va murakkab', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasmlar', 'c': False}]},
        {'t': 'Google Slides nima?', 'a': [{'t': 'Onlayn taqdimot dasturi', 'c': True}, {'t': 'Faqat offline dastur', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat brauzer', 'c': False}]},
    ]},

    {'n': 'Grafik muharrirlar', 't': 25, 'o': 17, 'q': [
        {'t': 'Grafik muharriri nima?', 'a': [{'t': 'Rasm yaratish va tahrirlash dasturi', 'c': True}, {'t': 'Faqat matn muharriri', 'c': False}, {'t': 'Faqat jadval dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Raster va vektor grafikalar farqi nima?', 'a': [{'t': 'Raster piksellardan, vektor matematik formulalardan', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Raster yangi', 'c': False}, {'t': 'Vektor eskirgan', 'c': False}]},
        {'t': 'Adobe Photoshop nima uchun ishlatiladi?', 'a': [{'t': 'Raster rasmlarni tahrirlash', 'c': True}, {'t': 'Faqat matn yozish', 'c': False}, {'t': 'Faqat video tahrirlash', 'c': False}, {'t': 'Faqat musiqa yaratish', 'c': False}]},
        {'t': 'Adobe Illustrator nima uchun ishlatiladi?', 'a': [{'t': 'Vektor grafikalar yaratish', 'c': True}, {'t': 'Faqat foto tahrirlash', 'c': False}, {'t': 'Faqat matn yozish', 'c': False}, {'t': 'Faqat video tahrirlash', 'c': False}]},
        {'t': 'GIMP nima?', 'a': [{'t': 'Bepul ochiq kodli grafik muharriri', 'c': True}, {'t': 'Qimmat dastur', 'c': False}, {'t': 'Faqat Windows uchun', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
    ]},

    {'n': 'Ma\'lumotlar bazasi asoslari', 't': 30, 'o': 18, 'q': [
        {'t': 'Ma\'lumotlar bazasi nima?', 'a': [{'t': 'Tizimli tarzda saqlangan ma\'lumotlar to\'plami', 'c': True}, {'t': 'Faqat bitta fayl', 'c': False}, {'t': 'Faqat papka', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'Ma\'lumotlar bazasi nima uchun kerak?', 'a': [{'t': 'Katta hajmdagi ma\'lumotlarni samarali boshqarish', 'c': True}, {'t': 'Faqat o\'yin o\'ynash', 'c': False}, {'t': 'Faqat rasm saqlash', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Mashhur ma\'lumotlar bazalari qaysilar?', 'a': [{'t': 'MySQL, PostgreSQL, MongoDB, Oracle', 'c': True}, {'t': 'Faqat Word', 'c': False}, {'t': 'Faqat Excel', 'c': False}, {'t': 'Faqat PowerPoint', 'c': False}]},
        {'t': 'SQL nima?', 'a': [{'t': 'Ma\'lumotlar bazasi bilan ishlash tili', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Operatsion tizim', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Jadval (table) ma\'lumotlar bazasida nima?', 'a': [{'t': 'Ma\'lumotlarni saqlash strukturasi', 'c': True}, {'t': 'Faqat Excel fayli', 'c': False}, {'t': 'Faqat Word hujjati', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
        {'t': 'Ma\'lumotlar bazasi qayerlarda ishlatiladi?', 'a': [{'t': 'Veb-saytlar, ilovalar, banklar, do\'konlar', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat telefonlarda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},

    {'n': 'Dasturlash asoslari', 't': 30, 'o': 19, 'q': [
        {'t': 'Dasturlash nima?', 'a': [{'t': 'Kompyuterga buyruqlar yozish', 'c': True}, {'t': 'Faqat o\'yin o\'ynash', 'c': False}, {'t': 'Faqat internet ko\'rish', 'c': False}, {'t': 'Faqat matn yozish', 'c': False}]},
        {'t': 'Dasturlash tili nima?', 'a': [{'t': 'Kompyuter bilan muloqot qilish vositasi', 'c': True}, {'t': 'Oddiy til', 'c': False}, {'t': 'Faqat ingliz tili', 'c': False}, {'t': 'Faqat rus tili', 'c': False}]},
        {'t': 'Mashhur dasturlash tillari qaysilar?', 'a': [{'t': 'Python, JavaScript, Java, C++, C#', 'c': True}, {'t': 'Faqat ingliz tili', 'c': False}, {'t': 'Faqat o\'zbek tili', 'c': False}, {'t': 'Faqat rus tili', 'c': False}]},
        {'t': 'Python nima uchun mashhur?', 'a': [{'t': 'O\'rganish oson, ko\'p maqsadli', 'c': True}, {'t': 'Juda qiyin', 'c': False}, {'t': 'Faqat o\'yinlar uchun', 'c': False}, {'t': 'Eskirgan', 'c': False}]},
        {'t': 'Algoritm nima?', 'a': [{'t': 'Muammoni yechish uchun qadamlar ketma-ketligi', 'c': True}, {'t': 'Faqat dastur', 'c': False}, {'t': 'Faqat kod', 'c': False}, {'t': 'Faqat fayl', 'c': False}]},
        {'t': 'Dasturchi kim?', 'a': [{'t': 'Dasturlar yaratadigan mutaxassis', 'c': True}, {'t': 'Faqat o\'yin o\'ynaydigan odam', 'c': False}, {'t': 'Faqat internet ko\'radigan odam', 'c': False}, {'t': 'Faqat kompyuter sotadigan odam', 'c': False}]},
    ]},

    {'n': 'Veb-sayt yaratish asoslari', 't': 30, 'o': 20, 'q': [
        {'t': 'Veb-sayt nima?', 'a': [{'t': 'Internet orqali ko\'riladigan sahifalar to\'plami', 'c': True}, {'t': 'Faqat bitta sahifa', 'c': False}, {'t': 'Faqat dastur', 'c': False}, {'t': 'Faqat fayl', 'c': False}]},
        {'t': 'HTML nima?', 'a': [{'t': 'Veb-sahifa strukturasini yaratish tili', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Operatsion tizim', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'CSS nima uchun ishlatiladi?', 'a': [{'t': 'Veb-sahifa dizaynini yaratish', 'c': True}, {'t': 'Faqat matn yozish', 'c': False}, {'t': 'Faqat hisob-kitob', 'c': False}, {'t': 'Faqat rasm chizish', 'c': False}]},
        {'t': 'JavaScript nima qiladi?', 'a': [{'t': 'Veb-sahifani interaktiv qiladi', 'c': True}, {'t': 'Faqat dizayn yaratadi', 'c': False}, {'t': 'Faqat struktura yaratadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Domen nima?', 'a': [{'t': 'Veb-sayt manzili (masalan, google.com)', 'c': True}, {'t': 'Faqat parol', 'c': False}, {'t': 'Faqat foydalanuvchi nomi', 'c': False}, {'t': 'Faqat email', 'c': False}]},
        {'t': 'Hosting nima?', 'a': [{'t': 'Veb-sayt fayllarini saqlaydigan server', 'c': True}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat brauzer', 'c': False}]},
    ]},

    {'n': 'Sun\'iy intellekt (AI) asoslari', 't': 30, 'o': 21, 'q': [
        {'t': 'Sun\'iy intellekt nima?', 'a': [{'t': 'Kompyuterning inson kabi o\'ylash qobiliyati', 'c': True}, {'t': 'Faqat robot', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'AI qayerlarda ishlatiladi?', 'a': [{'t': 'Ovoz tanish, yuz tanish, chatbot, avtomobil', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat telefonlarda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Mashinali o\'rganish (Machine Learning) nima?', 'a': [{'t': 'Kompyuter ma\'lumotlardan o\'rganadi', 'c': True}, {'t': 'Faqat dastur o\'rnatish', 'c': False}, {'t': 'Faqat fayl ko\'chirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'ChatGPT nima?', 'a': [{'t': 'AI asosidagi suhbat roboti', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat brauzer', 'c': False}, {'t': 'Faqat operatsion tizim', 'c': False}]},
        {'t': 'AI ning afzalliklari?', 'a': [{'t': 'Tez, aniq, 24/7 ishlaydi', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat sekin', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'AI ning kamchiliklari?', 'a': [{'t': 'Xato qilishi, ishsizlik, etika muammolari', 'c': True}, {'t': 'Hech qanday kamchilik yo\'q', 'c': False}, {'t': 'Faqat afzalliklari bor', 'c': False}, {'t': 'Faqat yaxshi', 'c': False}]},
    ]},

    {'n': 'Robotlar va avtomatlashtirish', 't': 30, 'o': 22, 'q': [
        {'t': 'Robot nima?', 'a': [{'t': 'Dasturlashtirilgan avtomatik qurilma', 'c': True}, {'t': 'Faqat o\'yinchoq', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}]},
        {'t': 'Robotlar qayerlarda ishlatiladi?', 'a': [{'t': 'Zavod, tibbiyot, xizmat, qidiruv-qutqaruv', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat uyda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Sanoat roboti nima qiladi?', 'a': [{'t': 'Zavodlarda ishlab chiqarish vazifalarini bajaradi', 'c': True}, {'t': 'Faqat o\'ynaydi', 'c': False}, {'t': 'Faqat uxlaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Avtomatlashtirish nima?', 'a': [{'t': 'Jarayonlarni avtomatik bajarilishini ta\'minlash', 'c': True}, {'t': 'Faqat qo\'lda ishlash', 'c': False}, {'t': 'Faqat o\'chirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Dron nima?', 'a': [{'t': 'Uchuvchi robot (pilotsiz uchish apparati)', 'c': True}, {'t': 'Faqat o\'yinchoq', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}]},
    ]},

    {'n': 'Internet of Things (IoT)', 't': 30, 'o': 23, 'q': [
        {'t': 'IoT nima?', 'a': [{'t': 'Narsalarning interneti - qurilmalar tarmog\'i', 'c': True}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}]},
        {'t': 'IoT qurilmalarga misollar?', 'a': [{'t': 'Aqlli uy, fitnes bilaguzuk, aqlli soat', 'c': True}, {'t': 'Faqat oddiy telefon', 'c': False}, {'t': 'Faqat oddiy televizor', 'c': False}, {'t': 'Faqat oddiy chiroq', 'c': False}]},
        {'t': 'Aqlli uy nima?', 'a': [{'t': 'Internetga ulangan qurilmalar bilan boshqariladigan uy', 'c': True}, {'t': 'Oddiy uy', 'c': False}, {'t': 'Faqat katta uy', 'c': False}, {'t': 'Faqat yangi uy', 'c': False}]},
        {'t': 'IoT ning afzalliklari?', 'a': [{'t': 'Qulaylik, avtomatlashtirish, energiya tejash', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat murakkab', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'IoT xavfsizligi nima uchun muhim?', 'a': [{'t': 'Xakerlar qurilmalarni buzishi mumkin', 'c': True}, {'t': 'Hech qanday xavf yo\'q', 'c': False}, {'t': 'Faqat o\'yin uchun', 'c': False}, {'t': 'Ahamiyatsiz', 'c': False}]},
    ]},

    {'n': 'Virtual va kengaytirilgan haqiqat', 't': 30, 'o': 24, 'q': [
        {'t': 'Virtual haqiqat (VR) nima?', 'a': [{'t': 'Kompyuter yaratgan to\'liq virtual dunyo', 'c': True}, {'t': 'Oddiy o\'yin', 'c': False}, {'t': 'Oddiy video', 'c': False}, {'t': 'Oddiy rasm', 'c': False}]},
        {'t': 'Kengaytirilgan haqiqat (AR) nima?', 'a': [{'t': 'Haqiqiy dunyoga virtual elementlar qo\'shish', 'c': True}, {'t': 'Faqat virtual dunyo', 'c': False}, {'t': 'Oddiy kamera', 'c': False}, {'t': 'Oddiy o\'yin', 'c': False}]},
        {'t': 'VR va AR farqi nima?', 'a': [{'t': 'VR to\'liq virtual, AR haqiqiy + virtual', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'VR eskirgan', 'c': False}, {'t': 'AR eskirgan', 'c': False}]},
        {'t': 'VR ko\'zoynak nima uchun kerak?', 'a': [{'t': 'Virtual dunyoni ko\'rish uchun', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Faqat himoya uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'VR va AR qayerlarda ishlatiladi?', 'a': [{'t': 'O\'yin, ta\'lim, tibbiyot, arxitektura', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat kinoda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},

    {'n': 'Blockchain va kriptovalyuta', 't': 30, 'o': 25, 'q': [
        {'t': 'Blockchain nima?', 'a': [{'t': 'Tarqatilgan ma\'lumotlar bazasi texnologiyasi', 'c': True}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'Kriptovalyuta nima?', 'a': [{'t': 'Raqamli shifrlangan pul', 'c': True}, {'t': 'Oddiy pul', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'Bitcoin nima?', 'a': [{'t': 'Birinchi va eng mashhur kriptovalyuta', 'c': True}, {'t': 'Oddiy pul', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'Blockchain ning afzalliklari?', 'a': [{'t': 'Xavfsizlik, shaffoflik, markazsizlik', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat sekin', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Kriptovalyuta qayerda saqlanadi?', 'a': [{'t': 'Raqamli hamyonda (wallet)', 'c': True}, {'t': 'Oddiy hamyonda', 'c': False}, {'t': 'Bankda', 'c': False}, {'t': 'Uyda', 'c': False}]},
    ]},

    {'n': '3D bosib chiqarish', 't': 25, 'o': 26, 'q': [
        {'t': '3D printer nima?', 'a': [{'t': 'Uch o\'lchamli narsalarni chop etadigan qurilma', 'c': True}, {'t': 'Oddiy printer', 'c': False}, {'t': 'Faqat qog\'ozga chop etadi', 'c': False}, {'t': 'Faqat rasm chizadi', 'c': False}]},
        {'t': '3D printer qanday ishlaydi?', 'a': [{'t': 'Materiallarni qatlam-qatlam qo\'yib narsani yasaydi', 'c': True}, {'t': 'Faqat qog\'ozga chizadi', 'c': False}, {'t': 'Faqat rasm ko\'rsatadi', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': '3D printer qayerlarda ishlatiladi?', 'a': [{'t': 'Tibbiyot, arxitektura, sanoat, ta\'lim', 'c': True}, {'t': 'Faqat uyda', 'c': False}, {'t': 'Faqat maktabda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': '3D printer qanday materiallar ishlatadi?', 'a': [{'t': 'Plastik, metall, qatron, keramika', 'c': True}, {'t': 'Faqat qog\'oz', 'c': False}, {'t': 'Faqat suv', 'c': False}, {'t': 'Faqat havo', 'c': False}]},
        {'t': '3D modelni qanday yaratish mumkin?', 'a': [{'t': 'CAD dasturlari yoki 3D skanerlash', 'c': True}, {'t': 'Faqat qo\'lda chizish', 'c': False}, {'t': 'Faqat fotosurat', 'c': False}, {'t': 'Yaratish mumkin emas', 'c': False}]},
    ]},

    {'n': 'Kvant kompyuterlari', 't': 30, 'o': 27, 'q': [
        {'t': 'Kvant kompyuteri nima?', 'a': [{'t': 'Kvant mexanikasi asosida ishlaydigan kompyuter', 'c': True}, {'t': 'Oddiy kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat planshet', 'c': False}]},
        {'t': 'Kvant kompyuteri oddiy kompyuterdan qanday farq qiladi?', 'a': [{'t': 'Juda tezroq va murakkab hisob-kitoblar bajaradi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Faqat sekinroq', 'c': False}, {'t': 'Faqat kattaroq', 'c': False}]},
        {'t': 'Kvant bit (qubit) nima?', 'a': [{'t': 'Bir vaqtning o\'zida 0 va 1 bo\'lishi mumkin', 'c': True}, {'t': 'Faqat 0', 'c': False}, {'t': 'Faqat 1', 'c': False}, {'t': 'Oddiy bit', 'c': False}]},
        {'t': 'Kvant kompyuterlari qayerlarda foydali?', 'a': [{'t': 'Kriptografiya, dori yaratish, AI', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat internetda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Kvant kompyuterlari hozir mavjudmi?', 'a': [{'t': 'Ha, lekin juda qimmat va tajriba bosqichida', 'c': True}, {'t': 'Yo\'q, hali yaratilmagan', 'c': False}, {'t': 'Ha, hammada bor', 'c': False}, {'t': 'Hech qachon bo\'lmaydi', 'c': False}]},
    ]},

    {'n': '5G va aloqa texnologiyalari', 't': 25, 'o': 28, 'q': [
        {'t': '5G nima?', 'a': [{'t': 'Beshinchi avlod mobil aloqa texnologiyasi', 'c': True}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}]},
        {'t': '5G ning afzalliklari?', 'a': [{'t': 'Juda tez, kam kechikish, ko\'p qurilma', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat sekin', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': '5G 4G dan qancha tezroq?', 'a': [{'t': '10-100 marta tezroq', 'c': True}, {'t': 'Bir xil', 'c': False}, {'t': 'Sekinroq', 'c': False}, {'t': 'Faqat 2 marta', 'c': False}]},
        {'t': 'Wi-Fi nima?', 'a': [{'t': 'Simsiz internet aloqa texnologiyasi', 'c': True}, {'t': 'Faqat simli internet', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}]},
        {'t': 'Bluetooth nima uchun ishlatiladi?', 'a': [{'t': 'Qisqa masofada qurilmalarni ulash', 'c': True}, {'t': 'Faqat internet uchun', 'c': False}, {'t': 'Faqat qo\'ng\'iroq uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},

    {'n': 'Elektron tijorat (E-commerce)', 't': 25, 'o': 29, 'q': [
        {'t': 'Elektron tijorat nima?', 'a': [{'t': 'Internet orqali savdo-sotiq', 'c': True}, {'t': 'Faqat oddiy do\'kon', 'c': False}, {'t': 'Faqat bozor', 'c': False}, {'t': 'Faqat bank', 'c': False}]},
        {'t': 'Mashhur onlayn do\'konlar qaysilar?', 'a': [{'t': 'Amazon, AliExpress, eBay, Wildberries', 'c': True}, {'t': 'Faqat oddiy do\'konlar', 'c': False}, {'t': 'Faqat bozorlar', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'Onlayn xarid qilishning afzalliklari?', 'a': [{'t': 'Qulay, tez, keng tanlov, arzon', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat noqulay', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Onlayn to\'lov usullari qaysilar?', 'a': [{'t': 'Karta, PayPal, Click, Payme', 'c': True}, {'t': 'Faqat naqd pul', 'c': False}, {'t': 'Faqat almashinuv', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'Onlayn xarid qilishda xavfsizlik?', 'a': [{'t': 'Ishonchli saytlar, HTTPS, sharhlar o\'qish', 'c': True}, {'t': 'Hech qanday xavf yo\'q', 'c': False}, {'t': 'Hamma sayt xavfsiz', 'c': False}, {'t': 'Ahamiyatsiz', 'c': False}]},
    ]},

    {'n': 'Raqamli marketing', 't': 25, 'o': 30, 'q': [
        {'t': 'Raqamli marketing nima?', 'a': [{'t': 'Internet orqali mahsulot va xizmatlarni reklama qilish', 'c': True}, {'t': 'Faqat oddiy reklama', 'c': False}, {'t': 'Faqat gazeta', 'c': False}, {'t': 'Faqat televizor', 'c': False}]},
        {'t': 'Raqamli marketing turlari?', 'a': [{'t': 'SEO, SMM, email, kontentli, video marketing', 'c': True}, {'t': 'Faqat gazeta', 'c': False}, {'t': 'Faqat radio', 'c': False}, {'t': 'Faqat televizor', 'c': False}]},
        {'t': 'SEO nima?', 'a': [{'t': 'Qidiruv tizimlarida saytni yuqoriga chiqarish', 'c': True}, {'t': 'Faqat reklama', 'c': False}, {'t': 'Faqat dizayn', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'SMM nima?', 'a': [{'t': 'Ijtimoiy tarmoqlarda marketing', 'c': True}, {'t': 'Faqat email', 'c': False}, {'t': 'Faqat SMS', 'c': False}, {'t': 'Faqat qo\'ng\'iroq', 'c': False}]},
        {'t': 'Kontentli marketing nima?', 'a': [{'t': 'Foydali kontent orqali mijozlarni jalb qilish', 'c': True}, {'t': 'Faqat reklama', 'c': False}, {'t': 'Faqat spam', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Big Data - katta ma\'lumotlar', 't': 30, 'o': 31, 'q': [
        {'t': 'Big Data nima?', 'a': [{'t': 'Juda katta hajmdagi ma\'lumotlar to\'plami', 'c': True}, {'t': 'Oddiy fayl', 'c': False}, {'t': 'Faqat bitta ma\'lumot', 'c': False}, {'t': 'Faqat kichik ma\'lumot', 'c': False}]},
        {'t': 'Big Data qayerdan kelib chiqadi?', 'a': [{'t': 'Ijtimoiy tarmoqlar, sensorlar, tranzaksiyalar', 'c': True}, {'t': 'Faqat bitta manba', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Hech qayerdan', 'c': False}]},
        {'t': 'Big Data nima uchun muhim?', 'a': [{'t': 'Qarorlar qabul qilish, trend topish, bashorat', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat saqlash uchun', 'c': False}, {'t': 'Faqat o\'chirish uchun', 'c': False}]},
        {'t': 'Big Data tahlili qayerlarda ishlatiladi?', 'a': [{'t': 'Biznes, tibbiyot, transport, ta\'lim', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat uyda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Big Data ning 3V si nima?', 'a': [{'t': 'Volume (hajm), Velocity (tezlik), Variety (xilma-xillik)', 'c': True}, {'t': 'Faqat hajm', 'c': False}, {'t': 'Faqat tezlik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Kibersport va onlayn o\'yinlar', 't': 25, 'o': 32, 'q': [
        {'t': 'Kibersport nima?', 'a': [{'t': 'Professional video o\'yinlar musobaqasi', 'c': True}, {'t': 'Oddiy o\'yin', 'c': False}, {'t': 'Faqat mashg\'ulot', 'c': False}, {'t': 'Faqat o\'yin-kulgi', 'c': False}]},
        {'t': 'Mashhur kibersport o\'yinlari?', 'a': [{'t': 'Dota 2, CS:GO, League of Legends, Fortnite', 'c': True}, {'t': 'Faqat shaxmat', 'c': False}, {'t': 'Faqat futbol', 'c': False}, {'t': 'Faqat basketbol', 'c': False}]},
        {'t': 'Onlayn o\'yin nima?', 'a': [{'t': 'Internet orqali o\'ynaladigan o\'yin', 'c': True}, {'t': 'Faqat offline o\'yin', 'c': False}, {'t': 'Faqat bitta o\'yinchi uchun', 'c': False}, {'t': 'Hech qanday o\'yin emas', 'c': False}]},
        {'t': 'Streaming nima?', 'a': [{'t': 'O\'yinni jonli efirda ko\'rsatish', 'c': True}, {'t': 'Faqat yuklab olish', 'c': False}, {'t': 'Faqat saqlash', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Twitch va YouTube Gaming nima?', 'a': [{'t': 'O\'yin streaming platformalari', 'c': True}, {'t': 'Faqat o\'yin do\'konlari', 'c': False}, {'t': 'Faqat ijtimoiy tarmoqlar', 'c': False}, {'t': 'Faqat email xizmatlari', 'c': False}]},
    ]},

    {'n': 'Masofaviy ish va onlayn ta\'lim', 't': 25, 'o': 33, 'q': [
        {'t': 'Masofaviy ish nima?', 'a': [{'t': 'Uydan yoki istalgan joydan ishlash', 'c': True}, {'t': 'Faqat ofisda ishlash', 'c': False}, {'t': 'Faqat zavodda ishlash', 'c': False}, {'t': 'Hech qanday ish emas', 'c': False}]},
        {'t': 'Masofaviy ish uchun nima kerak?', 'a': [{'t': 'Kompyuter, internet, aloqa vositalari', 'c': True}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat qog\'oz', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Onlayn ta\'lim nima?', 'a': [{'t': 'Internet orqali o\'qish va o\'rganish', 'c': True}, {'t': 'Faqat maktabda o\'qish', 'c': False}, {'t': 'Faqat kitobdan o\'qish', 'c': False}, {'t': 'Hech qanday ta\'lim emas', 'c': False}]},
        {'t': 'Mashhur onlayn ta\'lim platformalari?', 'a': [{'t': 'Coursera, Udemy, Khan Academy, edX', 'c': True}, {'t': 'Faqat maktab', 'c': False}, {'t': 'Faqat universitet', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'Zoom, Google Meet nima?', 'a': [{'t': 'Video konferensiya platformalari', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat ijtimoiy tarmoq', 'c': False}, {'t': 'Faqat email', 'c': False}]},
    ]},

    {'n': 'Raqamli imzo va elektron hujjatlar', 't': 25, 'o': 34, 'q': [
        {'t': 'Raqamli imzo nima?', 'a': [{'t': 'Elektron hujjatni tasdiqlash usuli', 'c': True}, {'t': 'Oddiy qo\'l imzo', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}]},
        {'t': 'Raqamli imzo qanday ishlaydi?', 'a': [{'t': 'Kriptografik shifrlash orqali', 'c': True}, {'t': 'Faqat qo\'lda yozish', 'c': False}, {'t': 'Faqat rasm qo\'yish', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'Elektron hujjat nima?', 'a': [{'t': 'Raqamli formatdagi rasmiy hujjat', 'c': True}, {'t': 'Faqat qog\'oz hujjat', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Raqamli imzoning afzalliklari?', 'a': [{'t': 'Tez, xavfsiz, qulaylik, tejamkorlik', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat noqulay', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'PDF nima?', 'a': [{'t': 'Hujjatlarni saqlash uchun universal format', 'c': True}, {'t': 'Faqat rasm format', 'c': False}, {'t': 'Faqat video format', 'c': False}, {'t': 'Faqat audio format', 'c': False}]},
    ]},

    {'n': 'QR kod va NFC texnologiyalari', 't': 25, 'o': 35, 'q': [
        {'t': 'QR kod nima?', 'a': [{'t': 'Ma\'lumotni saqlaydigan 2D shtrix-kod', 'c': True}, {'t': 'Oddiy rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat raqam', 'c': False}]},
        {'t': 'QR kod qanday o\'qiladi?', 'a': [{'t': 'Smartfon kamerasi yoki maxsus skaner bilan', 'c': True}, {'t': 'Faqat ko\'z bilan', 'c': False}, {'t': 'Faqat qo\'l bilan', 'c': False}, {'t': 'O\'qib bo\'lmaydi', 'c': False}]},
        {'t': 'QR kod qayerlarda ishlatiladi?', 'a': [{'t': 'To\'lov, reklama, ma\'lumot, kirish', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qayerda', 'c': False}, {'t': 'Faqat o\'yinlarda', 'c': False}]},
        {'t': 'NFC nima?', 'a': [{'t': 'Juda qisqa masofada simsiz aloqa', 'c': True}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat Bluetooth', 'c': False}, {'t': 'Faqat Wi-Fi', 'c': False}]},
        {'t': 'NFC qayerlarda ishlatiladi?', 'a': [{'t': 'Kontaktsiz to\'lov, kirish kartalari', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat internetda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},

    {'n': 'Biometrik texnologiyalar', 't': 25, 'o': 36, 'q': [
        {'t': 'Biometrik texnologiya nima?', 'a': [{'t': 'Inson biologik xususiyatlarini tanish', 'c': True}, {'t': 'Faqat parol', 'c': False}, {'t': 'Faqat karta', 'c': False}, {'t': 'Faqat kalit', 'c': False}]},
        {'t': 'Biometrik tanish turlari?', 'a': [{'t': 'Barmoq izi, yuz, ko\'z, ovoz tanish', 'c': True}, {'t': 'Faqat parol', 'c': False}, {'t': 'Faqat karta', 'c': False}, {'t': 'Faqat kalit', 'c': False}]},
        {'t': 'Barmoq izi tanish qanday ishlaydi?', 'a': [{'t': 'Barmoq izining noyob naqshini taqqoslaydi', 'c': True}, {'t': 'Faqat rasm oladi', 'c': False}, {'t': 'Faqat o\'lchaydi', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'Yuz tanish qayerlarda ishlatiladi?', 'a': [{'t': 'Telefon qulfi, xavfsizlik, to\'lov', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat rasmda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Biometrik texnologiyaning afzalliklari?', 'a': [{'t': 'Xavfsiz, qulay, tez, unutib bo\'lmaydi', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat noqulay', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},

    {'n': 'Avtonomli transport', 't': 30, 'o': 37, 'q': [
        {'t': 'Avtonomli avtomobil nima?', 'a': [{'t': 'O\'zi haydaydigan mashina', 'c': True}, {'t': 'Oddiy mashina', 'c': False}, {'t': 'Faqat elektr mashina', 'c': False}, {'t': 'Faqat tez mashina', 'c': False}]},
        {'t': 'Avtonomli mashina qanday ishlaydi?', 'a': [{'t': 'Sensorlar, kameralar, AI yordamida', 'c': True}, {'t': 'Faqat haydovchi boshqaradi', 'c': False}, {'t': 'Faqat yo\'l bo\'ylab', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'Avtonomli transport darajalari?', 'a': [{'t': '0 dan 5 gacha (0-qo\'lda, 5-to\'liq avtonom)', 'c': True}, {'t': 'Faqat 2 daraja', 'c': False}, {'t': 'Faqat 1 daraja', 'c': False}, {'t': 'Hech qanday daraja yo\'q', 'c': False}]},
        {'t': 'Avtonomli transportning afzalliklari?', 'a': [{'t': 'Xavfsizlik, qulaylik, vaqt tejash', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat xavfli', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Tesla nima bilan mashhur?', 'a': [{'t': 'Elektr va yarim avtonomli avtomobillar', 'c': True}, {'t': 'Faqat oddiy mashinalar', 'c': False}, {'t': 'Faqat velosipedlar', 'c': False}, {'t': 'Faqat samolyotlar', 'c': False}]},
    ]},

    {'n': 'Aqlli shahar (Smart City)', 't': 30, 'o': 38, 'q': [
        {'t': 'Aqlli shahar nima?', 'a': [{'t': 'Texnologiya bilan boshqariladigan zamonaviy shahar', 'c': True}, {'t': 'Oddiy shahar', 'c': False}, {'t': 'Faqat katta shahar', 'c': False}, {'t': 'Faqat yangi shahar', 'c': False}]},
        {'t': 'Aqlli shahar elementlari?', 'a': [{'t': 'Aqlli transport, energiya, xavfsizlik, chiqindilar', 'c': True}, {'t': 'Faqat yo\'llar', 'c': False}, {'t': 'Faqat binolar', 'c': False}, {'t': 'Faqat parklar', 'c': False}]},
        {'t': 'Aqlli svetofor nima qiladi?', 'a': [{'t': 'Trafik oqimini tahlil qilib moslashadi', 'c': True}, {'t': 'Faqat yonadi va o\'chadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Faqat rang o\'zgartiradi', 'c': False}]},
        {'t': 'Aqlli shaharning afzalliklari?', 'a': [{'t': 'Samaradorlik, ekologiya, qulaylik, xavfsizlik', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat murakkab', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Aqlli shahar misollari?', 'a': [{'t': 'Singapur, Dubay, Barselona, Seul', 'c': True}, {'t': 'Faqat kichik qishloqlar', 'c': False}, {'t': 'Faqat eski shaharlar', 'c': False}, {'t': 'Hech qanday misol yo\'q', 'c': False}]},
    ]},

    {'n': 'Energiya tejash texnologiyalari', 't': 25, 'o': 39, 'q': [
        {'t': 'Qayta tiklanadigan energiya nima?', 'a': [{'t': 'Quyosh, shamol, suv energiyasi', 'c': True}, {'t': 'Faqat neft', 'c': False}, {'t': 'Faqat ko\'mir', 'c': False}, {'t': 'Faqat gaz', 'c': False}]},
        {'t': 'Quyosh paneli qanday ishlaydi?', 'a': [{'t': 'Quyosh nurini elektr energiyasiga aylantiradi', 'c': True}, {'t': 'Faqat issiqlik beradi', 'c': False}, {'t': 'Faqat yorug\'lik beradi', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'Shamol generatori nima?', 'a': [{'t': 'Shamol energiyasidan elektr ishlab chiqaradi', 'c': True}, {'t': 'Faqat shamol yaratadi', 'c': False}, {'t': 'Faqat havo tozalaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'LED lampochka nima uchun yaxshi?', 'a': [{'t': 'Kam energiya sarflaydi, uzoq xizmat qiladi', 'c': True}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat zaif yorug\'lik', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Aqlli termostat nima qiladi?', 'a': [{'t': 'Haroratni avtomatik boshqarib energiya tejaydi', 'c': True}, {'t': 'Faqat haroratni ko\'rsatadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Faqat ovoz chiqaradi', 'c': False}]},
    ]},

    {'n': 'Tibbiyotda texnologiya', 't': 30, 'o': 40, 'q': [
        {'t': 'Telemedicina nima?', 'a': [{'t': 'Masofadan tibbiy xizmat ko\'rsatish', 'c': True}, {'t': 'Faqat kasalxonada davolanish', 'c': False}, {'t': 'Faqat dori ichish', 'c': False}, {'t': 'Hech qanday xizmat emas', 'c': False}]},
        {'t': 'Tibbiy robot nima qiladi?', 'a': [{'t': 'Operatsiya, diagnostika, parvarishlash', 'c': True}, {'t': 'Faqat tozalaydi', 'c': False}, {'t': 'Faqat ovqat beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Fitnes bilaguzuk nima uchun?', 'a': [{'t': 'Sog\'liqni kuzatish (yurak, qadam, uyqu)', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Faqat vaqtni ko\'rsatish', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': '3D printer tibbiyotda qanday ishlatiladi?', 'a': [{'t': 'Protez, implant, organ modellari yaratish', 'c': True}, {'t': 'Faqat dori yaratish', 'c': False}, {'t': 'Faqat asbob yaratish', 'c': False}, {'t': 'Hech qanday ishlatilmaydi', 'c': False}]},
        {'t': 'AI tibbiyotda qanday yordam beradi?', 'a': [{'t': 'Diagnostika, davolash rejasi, dori yaratish', 'c': True}, {'t': 'Faqat hisob-kitob', 'c': False}, {'t': 'Faqat ma\'lumot saqlash', 'c': False}, {'t': 'Hech qanday yordam bermaydi', 'c': False}]},
    ]},

    {'n': 'Ta\'limda texnologiya', 't': 25, 'o': 41, 'q': [
        {'t': 'Elektron darslik nima?', 'a': [{'t': 'Raqamli formatdagi interaktiv darslik', 'c': True}, {'t': 'Oddiy qog\'oz kitob', 'c': False}, {'t': 'Faqat video', 'c': False}, {'t': 'Faqat audio', 'c': False}]},
        {'t': 'Interaktiv doska nima?', 'a': [{'t': 'Sensorli ekran bilan ishlash taxtasi', 'c': True}, {'t': 'Oddiy doska', 'c': False}, {'t': 'Faqat qog\'oz', 'c': False}, {'t': 'Faqat daftar', 'c': False}]},
        {'t': 'Virtual laboratoriya nima?', 'a': [{'t': 'Kompyuterda tajriba o\'tkazish dasturi', 'c': True}, {'t': 'Oddiy laboratoriya', 'c': False}, {'t': 'Faqat kitob', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Gamifikatsiya ta\'limda nima?', 'a': [{'t': 'O\'yin elementlarini darsga qo\'shish', 'c': True}, {'t': 'Faqat o\'yin o\'ynash', 'c': False}, {'t': 'Faqat dam olish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Adaptiv ta\'lim nima?', 'a': [{'t': 'Har bir o\'quvchiga moslashgan dastur', 'c': True}, {'t': 'Hammaga bir xil dastur', 'c': False}, {'t': 'Faqat qiyin dastur', 'c': False}, {'t': 'Faqat oson dastur', 'c': False}]},
    ]},

    {'n': 'Qishloq xo\'jaligida texnologiya', 't': 25, 'o': 42, 'q': [
        {'t': 'Aqlli ferma nima?', 'a': [{'t': 'Texnologiya bilan boshqariladigan ferma', 'c': True}, {'t': 'Oddiy ferma', 'c': False}, {'t': 'Faqat katta ferma', 'c': False}, {'t': 'Faqat kichik ferma', 'c': False}]},
        {'t': 'Dron qishloq xo\'jaligida nima uchun?', 'a': [{'t': 'Dalalarni kuzatish, sug\'orish, dori sepish', 'c': True}, {'t': 'Faqat o\'yin uchun', 'c': False}, {'t': 'Faqat rasm olish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Sensorlar dalada nima qiladi?', 'a': [{'t': 'Tuproq, havo, namlik holatini kuzatadi', 'c': True}, {'t': 'Faqat haroratni o\'lchaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Faqat ovoz chiqaradi', 'c': False}]},
        {'t': 'Vertikal ferma nima?', 'a': [{'t': 'Binolar ichida qatlamli ekin yetishtirish', 'c': True}, {'t': 'Oddiy dala', 'c': False}, {'t': 'Faqat tog\'da ferma', 'c': False}, {'t': 'Faqat suv ostida ferma', 'c': False}]},
        {'t': 'Aqlli sug\'orish tizimi nima?', 'a': [{'t': 'Kerakli joyga kerakli miqdorda suv beradi', 'c': True}, {'t': 'Faqat ko\'p suv beradi', 'c': False}, {'t': 'Faqat kam suv beradi', 'c': False}, {'t': 'Hech qanday suv bermaydi', 'c': False}]},
    ]},

    {'n': 'Ekologiya va texnologiya', 't': 25, 'o': 43, 'q': [
        {'t': 'Yashil texnologiya nima?', 'a': [{'t': 'Atrof-muhitga zarar bermaydigan texnologiya', 'c': True}, {'t': 'Faqat yashil rangdagi texnologiya', 'c': False}, {'t': 'Faqat o\'simliklar uchun', 'c': False}, {'t': 'Hech qanday texnologiya emas', 'c': False}]},
        {'t': 'Elektr avtomobil nima uchun ekologik?', 'a': [{'t': 'Zararli gaz chiqarmaydi', 'c': True}, {'t': 'Faqat tez', 'c': False}, {'t': 'Faqat arzon', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}]},
        {'t': 'Qayta ishlash (recycling) nima?', 'a': [{'t': 'Chiqindilardan yangi mahsulot yaratish', 'c': True}, {'t': 'Faqat tashlab yuborish', 'c': False}, {'t': 'Faqat yoqib yuborish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Aqlli chiqindi qutisi nima qiladi?', 'a': [{'t': 'Chiqindilarni avtomatik saralaydi', 'c': True}, {'t': 'Faqat saqlaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Faqat hidini olib tashlaydi', 'c': False}]},
        {'t': 'Karbon izini kamaytirish nima?', 'a': [{'t': 'CO2 chiqindilarini kamaytirishga harakat', 'c': True}, {'t': 'Faqat oyoq izini o\'chirish', 'c': False}, {'t': 'Faqat tozalash', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Kosmik texnologiyalar', 't': 30, 'o': 44, 'q': [
        {'t': 'Sun\'iy yo\'ldosh nima?', 'a': [{'t': 'Yer atrofida aylanadigan kosmik qurilma', 'c': True}, {'t': 'Oddiy samolyot', 'c': False}, {'t': 'Faqat yulduz', 'c': False}, {'t': 'Faqat planeta', 'c': False}]},
        {'t': 'GPS qanday ishlaydi?', 'a': [{'t': 'Sun\'iy yo\'ldoshlar orqali joylashuvni aniqlaydi', 'c': True}, {'t': 'Faqat internet orqali', 'c': False}, {'t': 'Faqat telefon orqali', 'c': False}, {'t': 'Hech qanday ishlash yo\'q', 'c': False}]},
        {'t': 'SpaceX kompaniyasi nima bilan shug\'ullanadi?', 'a': [{'t': 'Qayta ishlatiluvchi raketalar yaratadi', 'c': True}, {'t': 'Faqat samolyot yasaydi', 'c': False}, {'t': 'Faqat mashina yasaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Xalqaro kosmik stansiya (ISS) nima?', 'a': [{'t': 'Kosmosda tadqiqot o\'tkaziladigan laboratoriya', 'c': True}, {'t': 'Oddiy bino', 'c': False}, {'t': 'Faqat mehmonxona', 'c': False}, {'t': 'Faqat do\'kon', 'c': False}]},
        {'t': 'Mars ga uchish nima uchun qiyin?', 'a': [{'t': 'Juda uzoq, qimmat, xavfli', 'c': True}, {'t': 'Juda oson', 'c': False}, {'t': 'Hech qanday qiyinchilik yo\'q', 'c': False}, {'t': 'Faqat vaqt kerak', 'c': False}]},
    ]},

    {'n': 'Nanotexnologiya', 't': 30, 'o': 45, 'q': [
        {'t': 'Nanotexnologiya nima?', 'a': [{'t': 'Juda kichik (nanometr) o\'lchamdagi texnologiya', 'c': True}, {'t': 'Oddiy texnologiya', 'c': False}, {'t': 'Faqat katta texnologiya', 'c': False}, {'t': 'Hech qanday texnologiya emas', 'c': False}]},
        {'t': 'Nanometr qancha?', 'a': [{'t': 'Metrning milliarddan bir qismi', 'c': True}, {'t': 'Metrning mingdan bir qismi', 'c': False}, {'t': 'Metrning yuzdan bir qismi', 'c': False}, {'t': 'Bir metr', 'c': False}]},
        {'t': 'Nanotexnologiya qayerlarda ishlatiladi?', 'a': [{'t': 'Tibbiyot, elektronika, material, energiya', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat uyda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Nanomateriallar nima?', 'a': [{'t': 'Nano o\'lchamdagi zarralardan yasalgan materiallar', 'c': True}, {'t': 'Oddiy materiallar', 'c': False}, {'t': 'Faqat metall', 'c': False}, {'t': 'Faqat plastik', 'c': False}]},
        {'t': 'Nanotexnologiya kelajagi qanday?', 'a': [{'t': 'Tibbiyot, elektronika, energiyada inqilob', 'c': True}, {'t': 'Hech qanday kelajak yo\'q', 'c': False}, {'t': 'Faqat o\'yinlar uchun', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
    ]},

    {'n': 'Biotexnologiya', 't': 30, 'o': 46, 'q': [
        {'t': 'Biotexnologiya nima?', 'a': [{'t': 'Tirik organizmlardan foydalanib texnologiya yaratish', 'c': True}, {'t': 'Faqat kompyuter texnologiyasi', 'c': False}, {'t': 'Faqat mashina texnologiyasi', 'c': False}, {'t': 'Hech qanday texnologiya emas', 'c': False}]},
        {'t': 'Genetik muhandislik nima?', 'a': [{'t': 'Organizmlarning genlarini o\'zgartirish', 'c': True}, {'t': 'Faqat bino qurish', 'c': False}, {'t': 'Faqat yo\'l qurish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'GMO nima?', 'a': [{'t': 'Genetik jihatdan o\'zgartirilgan organizm', 'c': True}, {'t': 'Oddiy o\'simlik', 'c': False}, {'t': 'Faqat hayvon', 'c': False}, {'t': 'Faqat mikrob', 'c': False}]},
        {'t': 'Biotexnologiya qayerlarda ishlatiladi?', 'a': [{'t': 'Tibbiyot, qishloq xo\'jaligi, oziq-ovqat', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat sportda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Klonlash nima?', 'a': [{'t': 'Organizmning genetik nusxasini yaratish', 'c': True}, {'t': 'Faqat ko\'paytirish', 'c': False}, {'t': 'Faqat o\'stirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Axborot xavfsizligi', 't': 30, 'o': 47, 'q': [
        {'t': 'Axborot xavfsizligi nima?', 'a': [{'t': 'Ma\'lumotlarni himoya qilish va xavfsizligini ta\'minlash', 'c': True}, {'t': 'Faqat parol qo\'yish', 'c': False}, {'t': 'Faqat antivirus o\'rnatish', 'c': False}, {'t': 'Hech qanday himoya yo\'q', 'c': False}]},
        {'t': 'Shifrlash (encryption) nima?', 'a': [{'t': 'Ma\'lumotlarni maxfiy kodga aylantirish', 'c': True}, {'t': 'Faqat yashirish', 'c': False}, {'t': 'Faqat o\'chirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Firewall nima?', 'a': [{'t': 'Tarmoqni himoya qiluvchi dastur yoki qurilma', 'c': True}, {'t': 'Faqat o\'t o\'chirish', 'c': False}, {'t': 'Faqat devor', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'VPN nima uchun ishlatiladi?', 'a': [{'t': 'Xavfsiz va maxfiy internet aloqa', 'c': True}, {'t': 'Faqat tezlashtirish uchun', 'c': False}, {'t': 'Faqat o\'yin uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Zaxira nusxa (backup) nima uchun kerak?', 'a': [{'t': 'Ma\'lumotlar yo\'qolsa qayta tiklash uchun', 'c': True}, {'t': 'Faqat joy egallash uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}, {'t': 'Faqat o\'chirish uchun', 'c': False}]},
        {'t': 'Xaker kim?', 'a': [{'t': 'Tizimga noqonuniy kiradigan shaxs', 'c': True}, {'t': 'Oddiy foydalanuvchi', 'c': False}, {'t': 'Dasturchi', 'c': False}, {'t': 'O\'qituvchi', 'c': False}]},
    ]},

    {'n': 'Raqamli iqtisodiyot', 't': 25, 'o': 48, 'q': [
        {'t': 'Raqamli iqtisodiyot nima?', 'a': [{'t': 'Raqamli texnologiyalarga asoslangan iqtisodiyot', 'c': True}, {'t': 'Oddiy iqtisodiyot', 'c': False}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat savdo', 'c': False}]},
        {'t': 'Fintech nima?', 'a': [{'t': 'Moliya va texnologiya birlashmasi', 'c': True}, {'t': 'Faqat bank', 'c': False}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat karta', 'c': False}]},
        {'t': 'Mobil to\'lov nima?', 'a': [{'t': 'Telefon orqali to\'lov qilish', 'c': True}, {'t': 'Faqat naqd to\'lov', 'c': False}, {'t': 'Faqat karta bilan', 'c': False}, {'t': 'Hech qanday to\'lov emas', 'c': False}]},
        {'t': 'Click, Payme nima?', 'a': [{'t': 'O\'zbekistonda mobil to\'lov tizimlari', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat ijtimoiy tarmoq', 'c': False}, {'t': 'Faqat messenger', 'c': False}]},
        {'t': 'Raqamli bank nima?', 'a': [{'t': 'Faqat onlayn ishlaydigan bank', 'c': True}, {'t': 'Oddiy bank', 'c': False}, {'t': 'Faqat katta bank', 'c': False}, {'t': 'Faqat kichik bank', 'c': False}]},
    ]},

    {'n': 'Kiberport va professional o\'yinlar', 't': 25, 'o': 49, 'q': [
        {'t': 'Esport nima?', 'a': [{'t': 'Elektron sport - professional video o\'yinlar', 'c': True}, {'t': 'Oddiy sport', 'c': False}, {'t': 'Faqat mashg\'ulot', 'c': False}, {'t': 'Faqat o\'yin-kulgi', 'c': False}]},
        {'t': 'Esport turniri nima?', 'a': [{'t': 'Professional o\'yinchilar musobaqasi', 'c': True}, {'t': 'Oddiy o\'yin', 'c': False}, {'t': 'Faqat mashg\'ulot', 'c': False}, {'t': 'Faqat ko\'rgazma', 'c': False}]},
        {'t': 'Esport o\'yinchisi qanday tayyorlanadi?', 'a': [{'t': 'Kuniga ko\'p soat mashq qiladi, strategiya o\'rganadi', 'c': True}, {'t': 'Faqat o\'ynaydi', 'c': False}, {'t': 'Hech qanday tayyorlanmaydi', 'c': False}, {'t': 'Faqat dam oladi', 'c': False}]},
        {'t': 'Esport mukofotlari qanday?', 'a': [{'t': 'Millionlab dollar mukofotlar', 'c': True}, {'t': 'Faqat medal', 'c': False}, {'t': 'Faqat diplom', 'c': False}, {'t': 'Hech qanday mukofot yo\'q', 'c': False}]},
        {'t': 'Esport kelajagi qanday?', 'a': [{'t': 'Tez rivojlanmoqda, Olimpiadaga kiritilishi mumkin', 'c': True}, {'t': 'Hech qanday kelajak yo\'q', 'c': False}, {'t': 'Faqat kamaymoqda', 'c': False}, {'t': 'Faqat to\'xtab qolmoqda', 'c': False}]},
    ]},

    {'n': 'Raqamli san\'at va dizayn', 't': 25, 'o': 50, 'q': [
        {'t': 'Raqamli san\'at nima?', 'a': [{'t': 'Kompyuter yordamida yaratilgan san\'at', 'c': True}, {'t': 'Faqat rasm chizish', 'c': False}, {'t': 'Faqat haykaltaroshlik', 'c': False}, {'t': 'Faqat musiqa', 'c': False}]},
        {'t': 'Grafik dizayn nima?', 'a': [{'t': 'Vizual kontent yaratish san\'ati', 'c': True}, {'t': 'Faqat matn yozish', 'c': False}, {'t': 'Faqat rasm ko\'rish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'UI/UX dizayn nima?', 'a': [{'t': 'Foydalanuvchi interfeysi va tajribasi dizayni', 'c': True}, {'t': 'Faqat rang tanlash', 'c': False}, {'t': 'Faqat shrift tanlash', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'NFT nima?', 'a': [{'t': 'Raqamli san\'at asarining noyob tokeni', 'c': True}, {'t': 'Oddiy rasm', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Raqamli dizayn qayerlarda ishlatiladi?', 'a': [{'t': 'Veb-sayt, ilova, reklama, brending', 'c': True}, {'t': 'Faqat o\'yinlarda', 'c': False}, {'t': 'Faqat kitoblarda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},

    {'n': 'Musiqa va audio texnologiyalari', 't': 25, 'o': 51, 'q': [
        {'t': 'Raqamli audio ishlab chiqarish nima?', 'a': [{'t': 'Kompyuterda musiqa yaratish va tahrirlash', 'c': True}, {'t': 'Faqat tinglash', 'c': False}, {'t': 'Faqat yuklab olish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'DAW (Digital Audio Workstation) nima?', 'a': [{'t': 'Musiqa yaratish dasturi', 'c': True}, {'t': 'Faqat pleer', 'c': False}, {'t': 'Faqat brauzer', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Streaming musiqa xizmatlari qaysilar?', 'a': [{'t': 'Spotify, Apple Music, YouTube Music', 'c': True}, {'t': 'Faqat radio', 'c': False}, {'t': 'Faqat kasseta', 'c': False}, {'t': 'Faqat plastinka', 'c': False}]},
        {'t': 'MIDI nima?', 'a': [{'t': 'Musiqa asboblari uchun raqamli protokol', 'c': True}, {'t': 'Audio format', 'c': False}, {'t': 'Video format', 'c': False}, {'t': 'Rasm format', 'c': False}]},
        {'t': 'Auto-Tune nima qiladi?', 'a': [{'t': 'Ovozni avtomatik sozlaydi va to\'g\'rilaydi', 'c': True}, {'t': 'Faqat ovoz balandligini oshiradi', 'c': False}, {'t': 'Faqat ovozni o\'chiradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'Kino va video ishlab chiqarish', 't': 25, 'o': 52, 'q': [
        {'t': 'Raqamli kino nima?', 'a': [{'t': 'Raqamli kameralar bilan suratga olingan kino', 'c': True}, {'t': 'Faqat plyonkali kino', 'c': False}, {'t': 'Faqat qora-oq kino', 'c': False}, {'t': 'Hech qanday kino emas', 'c': False}]},
        {'t': 'CGI nima?', 'a': [{'t': 'Kompyuter grafik effektlari', 'c': True}, {'t': 'Faqat oddiy rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Green screen nima uchun ishlatiladi?', 'a': [{'t': 'Fon o\'rniga boshqa tasvirni qo\'yish uchun', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Faqat yorug\'lik uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Motion capture nima?', 'a': [{'t': 'Harakatlarni raqamli formatga o\'tkazish', 'c': True}, {'t': 'Faqat rasm olish', 'c': False}, {'t': 'Faqat video olish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Netflix, YouTube kabi platformalar nima?', 'a': [{'t': 'Video streaming xizmatlari', 'c': True}, {'t': 'Faqat o\'yin platformalari', 'c': False}, {'t': 'Faqat ijtimoiy tarmoqlar', 'c': False}, {'t': 'Faqat email xizmatlari', 'c': False}]},
    ]},

    {'n': 'Ovoz yozish va podcast', 't': 25, 'o': 53, 'q': [
        {'t': 'Podcast nima?', 'a': [{'t': 'Audio yoki video epizodlar seriyasi', 'c': True}, {'t': 'Faqat radio', 'c': False}, {'t': 'Faqat musiqa', 'c': False}, {'t': 'Faqat kitob', 'c': False}]},
        {'t': 'Podcast qanday yaratiladi?', 'a': [{'t': 'Mikrofon, dastur, tahrirlash, nashr qilish', 'c': True}, {'t': 'Faqat gapirish', 'c': False}, {'t': 'Faqat yozish', 'c': False}, {'t': 'Hech qanday jarayon yo\'q', 'c': False}]},
        {'t': 'Podcast qayerda tinglash mumkin?', 'a': [{'t': 'Spotify, Apple Podcasts, Google Podcasts', 'c': True}, {'t': 'Faqat radio', 'c': False}, {'t': 'Faqat televizor', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Podcast mavzulari qanday bo\'lishi mumkin?', 'a': [{'t': 'Ta\'lim, ko\'ngilochar, biznes, sport, san\'at', 'c': True}, {'t': 'Faqat yangiliklar', 'c': False}, {'t': 'Faqat musiqa', 'c': False}, {'t': 'Faqat reklama', 'c': False}]},
        {'t': 'Podcast yaratish uchun qimmat asbob kerakmi?', 'a': [{'t': 'Yo\'q, oddiy mikrofon va telefon yetarli', 'c': True}, {'t': 'Ha, juda qimmat', 'c': False}, {'t': 'Faqat professional studiya kerak', 'c': False}, {'t': 'Yaratish mumkin emas', 'c': False}]},
    ]},

    {'n': 'Loyiha boshqaruvi texnologiyalari', 't': 25, 'o': 54, 'q': [
        {'t': 'Loyiha boshqaruvi nima?', 'a': [{'t': 'Loyihani rejalashtirish va amalga oshirish', 'c': True}, {'t': 'Faqat ishlash', 'c': False}, {'t': 'Faqat dam olish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Trello, Asana nima?', 'a': [{'t': 'Loyiha boshqaruvi dasturlari', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat ijtimoiy tarmoq', 'c': False}, {'t': 'Faqat messenger', 'c': False}]},
        {'t': 'Kanban taxtasi nima?', 'a': [{'t': 'Vazifalarni vizual boshqarish usuli', 'c': True}, {'t': 'Oddiy doska', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Agile metodologiya nima?', 'a': [{'t': 'Moslashuvchan loyiha boshqaruvi usuli', 'c': True}, {'t': 'Faqat dasturlash tili', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Slack, Microsoft Teams nima?', 'a': [{'t': 'Jamoa uchun aloqa va hamkorlik platformalari', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat ijtimoiy tarmoq', 'c': False}, {'t': 'Faqat email', 'c': False}]},
    ]},

    {'n': 'Texnologiya va jamiyat', 't': 25, 'o': 55, 'q': [
        {'t': 'Texnologiya jamiyatga qanday ta\'sir qiladi?', 'a': [{'t': 'Muloqot, ish, ta\'lim, hayot tarzini o\'zgartiradi', 'c': True}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}, {'t': 'Faqat yomonlashadi', 'c': False}, {'t': 'Faqat qimmatlashadi', 'c': False}]},
        {'t': 'Raqamli bo\'linish nima?', 'a': [{'t': 'Texnologiyaga kirish imkoniyatidagi farq', 'c': True}, {'t': 'Faqat matematika', 'c': False}, {'t': 'Faqat geografiya', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Texnologiya bilan bog\'liq etika muammolari?', 'a': [{'t': 'Maxfiylik, ishsizlik, qaramlik, noto\'g\'ri ma\'lumot', 'c': True}, {'t': 'Hech qanday muammo yo\'q', 'c': False}, {'t': 'Faqat narx', 'c': False}, {'t': 'Faqat o\'lcham', 'c': False}]},
        {'t': 'Texnologiya qaramlik nima?', 'a': [{'t': 'Texnologiyadan haddan tashqari foydalanish', 'c': True}, {'t': 'Oddiy foydalanish', 'c': False}, {'t': 'Kam foydalanish', 'c': False}, {'t': 'Hech qachon foydalanmaslik', 'c': False}]},
        {'t': 'Texnologiyadan to\'g\'ri foydalanish qanday?', 'a': [{'t': 'Muvozanatli, maqsadli, xavfsiz', 'c': True}, {'t': 'Faqat ko\'p foydalanish', 'c': False}, {'t': 'Faqat kam foydalanish', 'c': False}, {'t': 'Hech qachon foydalanmaslik', 'c': False}]},
    ]},

    {'n': 'Texnologiya tarixi', 't': 25, 'o': 56, 'q': [
        {'t': 'Birinchi kompyuter qachon yaratilgan?', 'a': [{'t': '1940-yillarda', 'c': True}, {'t': '2000-yillarda', 'c': False}, {'t': '1800-yillarda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Internet qachon paydo bo\'lgan?', 'a': [{'t': '1960-1970-yillarda', 'c': True}, {'t': '2000-yillarda', 'c': False}, {'t': '1900-yillarda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Birinchi shaxsiy kompyuter qaysi?', 'a': [{'t': 'Apple II, IBM PC', 'c': True}, {'t': 'iPhone', 'c': False}, {'t': 'PlayStation', 'c': False}, {'t': 'Televizor', 'c': False}]},
        {'t': 'Steve Jobs va Bill Gates kim?', 'a': [{'t': 'Texnologiya sohasidagi mashhur tadbirkorlar', 'c': True}, {'t': 'Faqat o\'yinchilar', 'c': False}, {'t': 'Faqat sportchilar', 'c': False}, {'t': 'Faqat artistlar', 'c': False}]},
        {'t': 'Smartfon qachon mashhur bo\'ldi?', 'a': [{'t': '2007-yilda iPhone chiqishidan keyin', 'c': True}, {'t': '1990-yillarda', 'c': False}, {'t': '2020-yillarda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Texnologiya kelajagi', 't': 30, 'o': 57, 'q': [
        {'t': 'Kelajakda qanday texnologiyalar rivojlanadi?', 'a': [{'t': 'AI, kvant, nano, bio, kosmik texnologiyalar', 'c': True}, {'t': 'Hech qanday yangilik yo\'q', 'c': False}, {'t': 'Faqat eski texnologiyalar', 'c': False}, {'t': 'Faqat oddiy texnologiyalar', 'c': False}]},
        {'t': 'Umumiy sun\'iy intellekt (AGI) nima?', 'a': [{'t': 'Inson darajasidagi universal AI', 'c': True}, {'t': 'Oddiy dastur', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Singularity nima?', 'a': [{'t': 'AI inson intellektidan oshib ketadigan nuqta', 'c': True}, {'t': 'Oddiy hodisa', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Kelajakda ish joylari qanday o\'zgaradi?', 'a': [{'t': 'Ko\'p kasblar avtomatlashadi, yangi kasblar paydo bo\'ladi', 'c': True}, {'t': 'Hech narsa o\'zgarmaydi', 'c': False}, {'t': 'Faqat yo\'qoladi', 'c': False}, {'t': 'Faqat ko\'payadi', 'c': False}]},
        {'t': 'Texnologiya insoniyat kelajagini qanday o\'zgartiradi?', 'a': [{'t': 'Hayot davomiyligi, sog\'liq, bilim, kosmosga sayohat', 'c': True}, {'t': 'Hech qanday o\'zgarish yo\'q', 'c': False}, {'t': 'Faqat yomonlashadi', 'c': False}, {'t': 'Faqat qimmatlashadi', 'c': False}]},
    ]},

    {'n': 'Texnologiya kasblar', 't': 25, 'o': 58, 'q': [
        {'t': 'Dasturchi nima qiladi?', 'a': [{'t': 'Dasturiy ta\'minot yaratadi', 'c': True}, {'t': 'Faqat o\'yin o\'ynaydi', 'c': False}, {'t': 'Faqat internet ko\'radi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Data scientist nima qiladi?', 'a': [{'t': 'Katta ma\'lumotlarni tahlil qiladi', 'c': True}, {'t': 'Faqat kompyuter ta\'mirlaydi', 'c': False}, {'t': 'Faqat o\'yin yaratadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'UX/UI dizayner nima qiladi?', 'a': [{'t': 'Foydalanuvchi interfeysi va tajribasini loyihalaydi', 'c': True}, {'t': 'Faqat rasm chizadi', 'c': False}, {'t': 'Faqat matn yozadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'DevOps muhandisi nima qiladi?', 'a': [{'t': 'Dastur ishlab chiqish va operatsiyalarni birlashtiradi', 'c': True}, {'t': 'Faqat kompyuter ta\'mirlaydi', 'c': False}, {'t': 'Faqat o\'yin o\'ynaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Kiberbezopaslik mutaxassisi nima qiladi?', 'a': [{'t': 'Tizimlarni xakerlardan himoya qiladi', 'c': True}, {'t': 'Faqat antivirus o\'rnatadi', 'c': False}, {'t': 'Faqat parol yaratadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'Texnologiya o\'rganish', 't': 25, 'o': 59, 'q': [
        {'t': 'Texnologiyani qanday o\'rganish kerak?', 'a': [{'t': 'Amaliyot, loyihalar, onlayn kurslar, kitoblar', 'c': True}, {'t': 'Faqat kitob o\'qish', 'c': False}, {'t': 'Faqat video ko\'rish', 'c': False}, {'t': 'Hech qanday o\'rganish kerak emas', 'c': False}]},
        {'t': 'Dasturlashni qayerdan boshlash kerak?', 'a': [{'t': 'Python yoki JavaScript kabi oson tildan', 'c': True}, {'t': 'Faqat eng qiyin tildan', 'c': False}, {'t': 'Faqat eski tildan', 'c': False}, {'t': 'Hech qayerdan', 'c': False}]},
        {'t': 'Onlayn ta\'lim platformalari qaysilar?', 'a': [{'t': 'Coursera, Udemy, Khan Academy, freeCodeCamp', 'c': True}, {'t': 'Faqat maktab', 'c': False}, {'t': 'Faqat universitet', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'Texnologiya sohasida muvaffaqiyat uchun nima kerak?', 'a': [{'t': 'Doimiy o\'rganish, amaliyot, qiziqish', 'c': True}, {'t': 'Faqat diplom', 'c': False}, {'t': 'Faqat pul', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Loyiha yaratish nima uchun muhim?', 'a': [{'t': 'Amaliy tajriba va portfolio uchun', 'c': True}, {'t': 'Faqat vaqt o\'tkazish uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat o\'yin uchun', 'c': False}]},
    ]},

    {'n': 'Texnologiya va kelajak kasblar', 't': 30, 'o': 60, 'q': [
        {'t': 'Kelajakda qanday kasblar talab bo\'ladi?', 'a': [{'t': 'AI mutaxassisi, data scientist, kiberbezopaslik', 'c': True}, {'t': 'Faqat eski kasblar', 'c': False}, {'t': 'Hech qanday kasb yo\'q', 'c': False}, {'t': 'Faqat oddiy kasblar', 'c': False}]},
        {'t': 'Texnologiya qanday kasblarni yo\'qotadi?', 'a': [{'t': 'Takrorlanuvchi va oddiy ishlar avtomatlashadi', 'c': True}, {'t': 'Hech qanday kasb yo\'qolmaydi', 'c': False}, {'t': 'Barcha kasblar yo\'qoladi', 'c': False}, {'t': 'Faqat yangi kasblar yo\'qoladi', 'c': False}]},
        {'t': 'Kelajakda qanday ko\'nikmalar muhim?', 'a': [{'t': 'Ijodkorlik, muammolarni yechish, texnologiya bilimi', 'c': True}, {'t': 'Faqat yodlash', 'c': False}, {'t': 'Faqat takrorlash', 'c': False}, {'t': 'Hech qanday ko\'nikma kerak emas', 'c': False}]},
        {'t': 'Umr bo\'yi o\'rganish nima uchun kerak?', 'a': [{'t': 'Texnologiya tez o\'zgargani uchun', 'c': True}, {'t': 'Hech qanday sabab yo\'q', 'c': False}, {'t': 'Faqat maktabda o\'rganish yetarli', 'c': False}, {'t': 'Faqat universitetda o\'rganish yetarli', 'c': False}]},
        {'t': 'Texnologiya sohasida ishlash uchun universitet kerakmi?', 'a': [{'t': 'Yo\'q, ko\'nikma va tajriba muhimroq', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Faqat doktorlik kerak', 'c': False}, {'t': 'Hech qanday ta\'lim kerak emas', 'c': False}]},
        {'t': 'Texnologiya kelajagingizni qanday o\'zgartirishi mumkin?', 'a': [{'t': 'Yangi imkoniyatlar, yaxshi ish, global hamkorlik', 'c': True}, {'t': 'Hech qanday o\'zgarish yo\'q', 'c': False}, {'t': 'Faqat yomonlashadi', 'c': False}, {'t': 'Faqat qiyinlashadi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_technology()
    add_topics(subj, T)
    print(f"\n✅ Texnologiya: {len(T)} ta mavzu qo'shildi!")
