"""
SQL DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_sql():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='SQL', defaults={'category': cat, 'description': 'SQL - Ma\'lumotlar bazasi bilan ishlash tili', 'icon': 'bi-database', 'order': 10, 'is_active': True})
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

# 30 TA MAVZU
T = [
    {'n': 'SQL ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'SQL nima?', 'a': [{'t': 'Structured Query Language - ma\'lumotlar bazasi bilan ishlash tili', 'c': True}, {'t': 'Simple Query Language', 'c': False}, {'t': 'System Quality Language', 'c': False}, {'t': 'Standard Question Language', 'c': False}]},
        {'t': 'SQL ning asosiy vazifasi nima?', 'a': [{'t': 'Ma\'lumotlar bazasidan ma\'lumot olish va boshqarish', 'c': True}, {'t': 'Veb sahifa yaratish', 'c': False}, {'t': 'Grafik dizayn qilish', 'c': False}, {'t': 'Tarmoq sozlash', 'c': False}]},
        {'t': 'SQL qaysi turdagi til hisoblanadi?', 'a': [{'t': 'Deklarativ til', 'c': True}, {'t': 'Imperativ til', 'c': False}, {'t': 'Funksional til', 'c': False}, {'t': 'Ob\'ektga yo\'naltirilgan til', 'c': False}]},
        {'t': 'SQL standartini kim boshqaradi?', 'a': [{'t': 'ANSI va ISO', 'c': True}, {'t': 'Microsoft', 'c': False}, {'t': 'Oracle', 'c': False}, {'t': 'Google', 'c': False}]},
        {'t': 'SQL qaysi yilda standartlashtirilgan?', 'a': [{'t': '1986 yilda', 'c': True}, {'t': '1990 yilda', 'c': False}, {'t': '1995 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}]},
        {'t': 'SQL buyruqlari qanday yoziladi?', 'a': [{'t': 'Katta yoki kichik harflarda, farqi yo\'q', 'c': True}, {'t': 'Faqat katta harflarda', 'c': False}, {'t': 'Faqat kichik harflarda', 'c': False}, {'t': 'Aralash holda', 'c': False}]},
    ]},
    
    {'n': 'Ma\'lumotlar bazasi asoslari', 't': 25, 'o': 2, 'q': [
        {'t': 'Ma\'lumotlar bazasi nima?', 'a': [{'t': 'Tizimli tashkil etilgan ma\'lumotlar to\'plami', 'c': True}, {'t': 'Oddiy fayl', 'c': False}, {'t': 'Dasturiy ta\'minot', 'c': False}, {'t': 'Operatsion tizim', 'c': False}]},
        {'t': 'DBMS nima?', 'a': [{'t': 'Database Management System - ma\'lumotlar bazasini boshqarish tizimi', 'c': True}, {'t': 'Data Backup Management System', 'c': False}, {'t': 'Digital Business Management System', 'c': False}, {'t': 'Database Monitoring System', 'c': False}]},
        {'t': 'Relatsion ma\'lumotlar bazasida ma\'lumotlar qanday saqlanadi?', 'a': [{'t': 'Jadvallar (tables) ko\'rinishida', 'c': True}, {'t': 'Fayllarda', 'c': False}, {'t': 'Graflarda', 'c': False}, {'t': 'Daraxtlarda', 'c': False}]},
        {'t': 'Jadvalning ustuni (column) nima deb ataladi?', 'a': [{'t': 'Field yoki Attribute', 'c': True}, {'t': 'Row', 'c': False}, {'t': 'Record', 'c': False}, {'t': 'Index', 'c': False}]},
        {'t': 'Jadvalning qatori (row) nima deb ataladi?', 'a': [{'t': 'Record yoki Tuple', 'c': True}, {'t': 'Column', 'c': False}, {'t': 'Field', 'c': False}, {'t': 'Attribute', 'c': False}]},
        {'t': 'Primary Key nima?', 'a': [{'t': 'Jadvalda har bir yozuvni noyob aniqlash uchun kalit', 'c': True}, {'t': 'Parol', 'c': False}, {'t': 'Foydalanuvchi nomi', 'c': False}, {'t': 'Jadval nomi', 'c': False}]},
        {'t': 'Mashhur DBMS lardan biri qaysi?', 'a': [{'t': 'MySQL', 'c': True}, {'t': 'HTML', 'c': False}, {'t': 'CSS', 'c': False}, {'t': 'JavaScript', 'c': False}]},
    ]},

    {'n': 'SELECT - Ma\'lumot olish', 't': 25, 'o': 3, 'q': [
        {'t': 'SELECT buyrug\'i nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlar bazasidan ma\'lumot olish uchun', 'c': True}, {'t': 'Ma\'lumot o\'chirish uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Ma\'lumot yangilash uchun', 'c': False}]},
        {'t': 'Barcha ustunlarni tanlash uchun qanday yoziladi?', 'a': [{'t': 'SELECT * FROM jadval_nomi', 'c': True}, {'t': 'SELECT ALL FROM jadval_nomi', 'c': False}, {'t': 'GET * FROM jadval_nomi', 'c': False}, {'t': 'FETCH * FROM jadval_nomi', 'c': False}]},
        {'t': 'Muayyan ustunlarni tanlash uchun?', 'a': [{'t': 'SELECT ustun1, ustun2 FROM jadval', 'c': True}, {'t': 'SELECT (ustun1, ustun2) FROM jadval', 'c': False}, {'t': 'GET ustun1, ustun2 FROM jadval', 'c': False}, {'t': 'FETCH ustun1, ustun2 FROM jadval', 'c': False}]},
        {'t': 'FROM kalit so\'zi nima uchun ishlatiladi?', 'a': [{'t': 'Qaysi jadvaldan ma\'lumot olishni ko\'rsatish uchun', 'c': True}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}]},
        {'t': 'SELECT so\'rovi natijasi nima deb ataladi?', 'a': [{'t': 'Result set yoki natija to\'plami', 'c': True}, {'t': 'Database', 'c': False}, {'t': 'Table', 'c': False}, {'t': 'Schema', 'c': False}]},
        {'t': 'SELECT buyrug\'i ma\'lumotlar bazasini o\'zgartiradi?', 'a': [{'t': 'Yo\'q, faqat ma\'lumot o\'qiydi', 'c': True}, {'t': 'Ha, o\'zgartiradi', 'c': False}, {'t': 'Ba\'zan o\'zgartiradi', 'c': False}, {'t': 'Faqat yangilaydi', 'c': False}]},
    ]},

    {'n': 'WHERE - Filtrlash', 't': 30, 'o': 4, 'q': [
        {'t': 'WHERE kalit so\'zi nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlarni shartga ko\'ra filtrlash uchun', 'c': True}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}, {'t': 'Ma\'lumotni guruhlash uchun', 'c': False}]},
        {'t': 'Tenglik shartini qanday yoziladi?', 'a': [{'t': 'WHERE ustun = qiymat', 'c': True}, {'t': 'WHERE ustun == qiymat', 'c': False}, {'t': 'WHERE ustun := qiymat', 'c': False}, {'t': 'WHERE ustun EQUALS qiymat', 'c': False}]},
        {'t': 'Matnli qiymatlar qanday yoziladi?', 'a': [{'t': 'Bitta qo\'shtirnoq ichida: \'matn\'', 'c': True}, {'t': 'Qo\'sh qo\'shtirnoq ichida: "matn"', 'c': False}, {'t': 'Qo\'shtirnoqsiz: matn', 'c': False}, {'t': 'Kvadrat qavs ichida: [matn]', 'c': False}]},
        {'t': 'Bir nechta shartni birlashtirish uchun qaysi operator ishlatiladi?', 'a': [{'t': 'AND va OR', 'c': True}, {'t': 'PLUS va MINUS', 'c': False}, {'t': 'WITH va WITHOUT', 'c': False}, {'t': 'IF va ELSE', 'c': False}]},
        {'t': 'Katta yoki teng shartini qanday yoziladi?', 'a': [{'t': 'WHERE yosh >= 18', 'c': True}, {'t': 'WHERE yosh => 18', 'c': False}, {'t': 'WHERE yosh >== 18', 'c': False}, {'t': 'WHERE yosh GREATER 18', 'c': False}]},
        {'t': 'Teng emas shartini qanday yoziladi?', 'a': [{'t': 'WHERE ustun <> qiymat yoki ustun != qiymat', 'c': True}, {'t': 'WHERE ustun NOT qiymat', 'c': False}, {'t': 'WHERE ustun !== qiymat', 'c': False}, {'t': 'WHERE ustun NOTEQUAL qiymat', 'c': False}]},
        {'t': 'AND operatori qachon TRUE qaytaradi?', 'a': [{'t': 'Ikkala shart ham to\'g\'ri bo\'lganda', 'c': True}, {'t': 'Bitta shart to\'g\'ri bo\'lganda', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'OR operatori qachon TRUE qaytaradi?', 'a': [{'t': 'Kamida bitta shart to\'g\'ri bo\'lganda', 'c': True}, {'t': 'Ikkala shart ham to\'g\'ri bo\'lganda', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Ikkala shart ham noto\'g\'ri bo\'lganda', 'c': False}]},
    ]},

    {'n': 'ORDER BY - Saralash', 't': 25, 'o': 5, 'q': [
        {'t': 'ORDER BY nima uchun ishlatiladi?', 'a': [{'t': 'Natijalarni saralash uchun', 'c': True}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}]},
        {'t': 'O\'sish tartibida saralash uchun?', 'a': [{'t': 'ORDER BY ustun ASC (yoki faqat ORDER BY ustun)', 'c': True}, {'t': 'ORDER BY ustun UP', 'c': False}, {'t': 'ORDER BY ustun INCREASE', 'c': False}, {'t': 'SORT BY ustun ASC', 'c': False}]},
        {'t': 'Kamayish tartibida saralash uchun?', 'a': [{'t': 'ORDER BY ustun DESC', 'c': True}, {'t': 'ORDER BY ustun DOWN', 'c': False}, {'t': 'ORDER BY ustun DECREASE', 'c': False}, {'t': 'SORT BY ustun DESC', 'c': False}]},
        {'t': 'Bir nechta ustun bo\'yicha saralash mumkinmi?', 'a': [{'t': 'Ha, ORDER BY ustun1, ustun2', 'c': True}, {'t': 'Yo\'q, faqat bitta ustun', 'c': False}, {'t': 'Faqat 2 ta ustun', 'c': False}, {'t': 'Faqat 3 ta ustun', 'c': False}]},
        {'t': 'ORDER BY ning standart tartibi qanday?', 'a': [{'t': 'ASC (o\'sish tartibi)', 'c': True}, {'t': 'DESC (kamayish tartibi)', 'c': False}, {'t': 'Tasodifiy', 'c': False}, {'t': 'Tartibsiz', 'c': False}]},
        {'t': 'ORDER BY qayerda yoziladi?', 'a': [{'t': 'SELECT so\'rovining oxirida', 'c': True}, {'t': 'SELECT so\'rovining boshida', 'c': False}, {'t': 'WHERE dan oldin', 'c': False}, {'t': 'FROM dan oldin', 'c': False}]},
    ]},

    {'n': 'LIMIT - Natijalarni cheklash', 't': 20, 'o': 6, 'q': [
        {'t': 'LIMIT nima uchun ishlatiladi?', 'a': [{'t': 'Qaytariladigan qatorlar sonini cheklash uchun', 'c': True}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Jadval o\'lchamini cheklash uchun', 'c': False}, {'t': 'Foydalanuvchi huquqlarini cheklash uchun', 'c': False}]},
        {'t': 'Birinchi 10 ta yozuvni olish uchun?', 'a': [{'t': 'SELECT * FROM jadval LIMIT 10', 'c': True}, {'t': 'SELECT * FROM jadval TOP 10', 'c': False}, {'t': 'SELECT * FROM jadval FIRST 10', 'c': False}, {'t': 'SELECT * FROM jadval MAX 10', 'c': False}]},
        {'t': 'LIMIT qayerda yoziladi?', 'a': [{'t': 'So\'rovning oxirida', 'c': True}, {'t': 'SELECT dan keyin', 'c': False}, {'t': 'FROM dan oldin', 'c': False}, {'t': 'WHERE dan oldin', 'c': False}]},
        {'t': 'OFFSET nima uchun ishlatiladi?', 'a': [{'t': 'Qaysi qatordan boshlab olishni ko\'rsatish uchun', 'c': True}, {'t': 'Qatorlarni saralash uchun', 'c': False}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'LIMIT va OFFSET birgalikda qanday ishlatiladi?', 'a': [{'t': 'LIMIT 10 OFFSET 5', 'c': True}, {'t': 'OFFSET 5 LIMIT 10', 'c': False}, {'t': 'LIMIT(10, 5)', 'c': False}, {'t': 'OFFSET(5) LIMIT(10)', 'c': False}]},
    ]},

    {'n': 'DISTINCT - Noyob qiymatlar', 't': 20, 'o': 7, 'q': [
        {'t': 'DISTINCT nima uchun ishlatiladi?', 'a': [{'t': 'Takrorlanuvchi qiymatlarni olib tashlash uchun', 'c': True}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'DISTINCT qanday yoziladi?', 'a': [{'t': 'SELECT DISTINCT ustun FROM jadval', 'c': True}, {'t': 'SELECT ustun DISTINCT FROM jadval', 'c': False}, {'t': 'SELECT UNIQUE ustun FROM jadval', 'c': False}, {'t': 'SELECT ustun UNIQUE FROM jadval', 'c': False}]},
        {'t': 'DISTINCT bir nechta ustun bilan ishlaydi?', 'a': [{'t': 'Ha, SELECT DISTINCT ustun1, ustun2', 'c': True}, {'t': 'Yo\'q, faqat bitta ustun', 'c': False}, {'t': 'Faqat 2 ta ustun bilan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'DISTINCT qayerda yoziladi?', 'a': [{'t': 'SELECT dan keyin, ustun nomidan oldin', 'c': True}, {'t': 'FROM dan keyin', 'c': False}, {'t': 'WHERE dan keyin', 'c': False}, {'t': 'So\'rov oxirida', 'c': False}]},
        {'t': 'DISTINCT COUNT bilan qanday ishlatiladi?', 'a': [{'t': 'SELECT COUNT(DISTINCT ustun) FROM jadval', 'c': True}, {'t': 'SELECT DISTINCT COUNT(ustun) FROM jadval', 'c': False}, {'t': 'SELECT COUNT DISTINCT ustun FROM jadval', 'c': False}, {'t': 'SELECT ustun COUNT DISTINCT FROM jadval', 'c': False}]},
    ]},

    {'n': 'Agregat funksiyalar - COUNT, SUM, AVG', 't': 30, 'o': 8, 'q': [
        {'t': 'COUNT() funksiyasi nima qiladi?', 'a': [{'t': 'Qatorlar sonini sanaydi', 'c': True}, {'t': 'Qiymatlarni qo\'shadi', 'c': False}, {'t': 'O\'rtacha qiymatni hisoblaydi', 'c': False}, {'t': 'Maksimal qiymatni topadi', 'c': False}]},
        {'t': 'Barcha qatorlarni sanash uchun?', 'a': [{'t': 'SELECT COUNT(*) FROM jadval', 'c': True}, {'t': 'SELECT SUM(*) FROM jadval', 'c': False}, {'t': 'SELECT ALL(*) FROM jadval', 'c': False}, {'t': 'SELECT TOTAL(*) FROM jadval', 'c': False}]},
        {'t': 'SUM() funksiyasi nima qiladi?', 'a': [{'t': 'Raqamli qiymatlarni qo\'shadi', 'c': True}, {'t': 'Qatorlarni sanaydi', 'c': False}, {'t': 'O\'rtacha qiymatni hisoblaydi', 'c': False}, {'t': 'Minimal qiymatni topadi', 'c': False}]},
        {'t': 'AVG() funksiyasi nima qiladi?', 'a': [{'t': 'O\'rtacha qiymatni hisoblaydi', 'c': True}, {'t': 'Qatorlarni sanaydi', 'c': False}, {'t': 'Qiymatlarni qo\'shadi', 'c': False}, {'t': 'Maksimal qiymatni topadi', 'c': False}]},
        {'t': 'MIN() funksiyasi nima qiladi?', 'a': [{'t': 'Eng kichik qiymatni topadi', 'c': True}, {'t': 'Eng katta qiymatni topadi', 'c': False}, {'t': 'O\'rtacha qiymatni hisoblaydi', 'c': False}, {'t': 'Qatorlarni sanaydi', 'c': False}]},
        {'t': 'MAX() funksiyasi nima qiladi?', 'a': [{'t': 'Eng katta qiymatni topadi', 'c': True}, {'t': 'Eng kichik qiymatni topadi', 'c': False}, {'t': 'O\'rtacha qiymatni hisoblaydi', 'c': False}, {'t': 'Qiymatlarni qo\'shadi', 'c': False}]},
        {'t': 'Agregat funksiyalar NULL qiymatlarni hisobga oladimi?', 'a': [{'t': 'Yo\'q, NULL qiymatlar e\'tiborga olinmaydi', 'c': True}, {'t': 'Ha, NULL qiymatlar ham hisoblanadi', 'c': False}, {'t': 'Faqat COUNT() da hisoblanadi', 'c': False}, {'t': 'Faqat SUM() da hisoblanadi', 'c': False}]},
        {'t': 'COUNT(ustun) va COUNT(*) orasidagi farq?', 'a': [{'t': 'COUNT(ustun) NULL larni hisoblamaydi, COUNT(*) barcha qatorlarni sanaydi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'COUNT(*) tezroq ishlaydi', 'c': False}, {'t': 'COUNT(ustun) tezroq ishlaydi', 'c': False}]},
    ]},

    {'n': 'GROUP BY - Guruhlash', 't': 30, 'o': 9, 'q': [
        {'t': 'GROUP BY nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlarni guruhlash va agregat funksiyalar bilan ishlash uchun', 'c': True}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'GROUP BY qanday yoziladi?', 'a': [{'t': 'SELECT ustun, COUNT(*) FROM jadval GROUP BY ustun', 'c': True}, {'t': 'SELECT ustun FROM jadval GROUP ustun', 'c': False}, {'t': 'SELECT GROUP ustun FROM jadval', 'c': False}, {'t': 'GROUP BY ustun SELECT * FROM jadval', 'c': False}]},
        {'t': 'GROUP BY qayerda yoziladi?', 'a': [{'t': 'WHERE dan keyin, ORDER BY dan oldin', 'c': True}, {'t': 'SELECT dan keyin', 'c': False}, {'t': 'FROM dan oldin', 'c': False}, {'t': 'So\'rov boshida', 'c': False}]},
        {'t': 'GROUP BY da SELECT qismida qanday ustunlar bo\'lishi mumkin?', 'a': [{'t': 'Faqat GROUP BY dagi ustunlar yoki agregat funksiyalar', 'c': True}, {'t': 'Istalgan ustunlar', 'c': False}, {'t': 'Faqat agregat funksiyalar', 'c': False}, {'t': 'Faqat PRIMARY KEY ustunlar', 'c': False}]},
        {'t': 'Bir nechta ustun bo\'yicha guruhlash mumkinmi?', 'a': [{'t': 'Ha, GROUP BY ustun1, ustun2', 'c': True}, {'t': 'Yo\'q, faqat bitta ustun', 'c': False}, {'t': 'Faqat 2 ta ustun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'GROUP BY va ORDER BY birgalikda ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, GROUP BY dan keyin ORDER BY yoziladi', 'c': True}, {'t': 'Yo\'q, faqat bittasi ishlatiladi', 'c': False}, {'t': 'Ha, lekin ORDER BY birinchi', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'HAVING - Guruh filtrlash', 't': 25, 'o': 10, 'q': [
        {'t': 'HAVING nima uchun ishlatiladi?', 'a': [{'t': 'GROUP BY natijalarini filtrlash uchun', 'c': True}, {'t': 'Oddiy qatorlarni filtrlash uchun', 'c': False}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'WHERE va HAVING orasidagi farq?', 'a': [{'t': 'WHERE guruhlashdan oldin, HAVING guruhlashdan keyin ishlaydi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'HAVING tezroq ishlaydi', 'c': False}, {'t': 'WHERE agregat funksiyalar bilan ishlaydi', 'c': False}]},
        {'t': 'HAVING qayerda yoziladi?', 'a': [{'t': 'GROUP BY dan keyin', 'c': True}, {'t': 'WHERE dan oldin', 'c': False}, {'t': 'SELECT dan keyin', 'c': False}, {'t': 'FROM dan oldin', 'c': False}]},
        {'t': 'HAVING agregat funksiyalar bilan ishlaydi?', 'a': [{'t': 'Ha, HAVING COUNT(*) > 5', 'c': True}, {'t': 'Yo\'q, faqat oddiy ustunlar bilan', 'c': False}, {'t': 'Faqat ba\'zi funksiyalar bilan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'WHERE va HAVING birgalikda ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, WHERE birinchi, keyin GROUP BY, keyin HAVING', 'c': True}, {'t': 'Yo\'q, faqat bittasi', 'c': False}, {'t': 'Ha, lekin HAVING birinchi', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'INSERT - Ma\'lumot qo\'shish', 't': 25, 'o': 11, 'q': [
        {'t': 'INSERT buyrug\'i nima uchun ishlatiladi?', 'a': [{'t': 'Jadvalga yangi qator qo\'shish uchun', 'c': True}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'INSERT buyrug\'i qanday yoziladi?', 'a': [{'t': 'INSERT INTO jadval (ustun1, ustun2) VALUES (qiymat1, qiymat2)', 'c': True}, {'t': 'INSERT jadval VALUES (qiymat1, qiymat2)', 'c': False}, {'t': 'ADD INTO jadval VALUES (qiymat1, qiymat2)', 'c': False}, {'t': 'CREATE INTO jadval VALUES (qiymat1, qiymat2)', 'c': False}]},
        {'t': 'Barcha ustunlarga qiymat qo\'shishda ustun nomlarini yozish shart?', 'a': [{'t': 'Yo\'q, lekin tartib to\'g\'ri bo\'lishi kerak', 'c': True}, {'t': 'Ha, har doim yozish kerak', 'c': False}, {'t': 'Faqat PRIMARY KEY da', 'c': False}, {'t': 'Hech qachon yozilmaydi', 'c': False}]},
        {'t': 'Bir nechta qator qo\'shish mumkinmi?', 'a': [{'t': 'Ha, VALUES (qiymat1, qiymat2), (qiymat3, qiymat4)', 'c': True}, {'t': 'Yo\'q, faqat bitta qator', 'c': False}, {'t': 'Faqat 2 ta qator', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Matnli qiymatlar qanday yoziladi?', 'a': [{'t': 'Bitta qo\'shtirnoq ichida: \'matn\'', 'c': True}, {'t': 'Qo\'shtirnoqsiz', 'c': False}, {'t': 'Kvadrat qavs ichida', 'c': False}, {'t': 'Jingalak qavs ichida', 'c': False}]},
        {'t': 'Raqamli qiymatlar qanday yoziladi?', 'a': [{'t': 'Qo\'shtirnoqsiz: 123', 'c': True}, {'t': 'Qo\'shtirnoq ichida: \'123\'', 'c': False}, {'t': 'Kvadrat qavs ichida: [123]', 'c': False}, {'t': 'Jingalak qavs ichida: {123}', 'c': False}]},
    ]},

    {'n': 'UPDATE - Ma\'lumot yangilash', 't': 25, 'o': 12, 'q': [
        {'t': 'UPDATE buyrug\'i nima uchun ishlatiladi?', 'a': [{'t': 'Mavjud ma\'lumotlarni yangilash uchun', 'c': True}, {'t': 'Yangi ma\'lumot qo\'shish uchun', 'c': False}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'UPDATE buyrug\'i qanday yoziladi?', 'a': [{'t': 'UPDATE jadval SET ustun = qiymat WHERE shart', 'c': True}, {'t': 'UPDATE jadval WHERE shart SET ustun = qiymat', 'c': False}, {'t': 'CHANGE jadval SET ustun = qiymat WHERE shart', 'c': False}, {'t': 'MODIFY jadval SET ustun = qiymat WHERE shart', 'c': False}]},
        {'t': 'WHERE ni yozmasangiz nima bo\'ladi?', 'a': [{'t': 'Barcha qatorlar yangilanadi', 'c': True}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa bo\'lmaydi', 'c': False}, {'t': 'Faqat birinchi qator yangilanadi', 'c': False}]},
        {'t': 'Bir nechta ustunni yangilash mumkinmi?', 'a': [{'t': 'Ha, SET ustun1 = qiymat1, ustun2 = qiymat2', 'c': True}, {'t': 'Yo\'q, faqat bitta ustun', 'c': False}, {'t': 'Faqat 2 ta ustun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'UPDATE da SET kalit so\'zi nima uchun ishlatiladi?', 'a': [{'t': 'Qaysi ustunlarni yangilashni ko\'rsatish uchun', 'c': True}, {'t': 'Shartni belgilash uchun', 'c': False}, {'t': 'Jadval nomini ko\'rsatish uchun', 'c': False}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}]},
    ]},

    {'n': 'DELETE - Ma\'lumot o\'chirish', 't': 25, 'o': 13, 'q': [
        {'t': 'DELETE buyrug\'i nima uchun ishlatiladi?', 'a': [{'t': 'Jadvaldan qatorlarni o\'chirish uchun', 'c': True}, {'t': 'Jadvalning o\'zini o\'chirish uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}, {'t': 'Yangi ma\'lumot qo\'shish uchun', 'c': False}]},
        {'t': 'DELETE buyrug\'i qanday yoziladi?', 'a': [{'t': 'DELETE FROM jadval WHERE shart', 'c': True}, {'t': 'DELETE jadval WHERE shart', 'c': False}, {'t': 'REMOVE FROM jadval WHERE shart', 'c': False}, {'t': 'DROP FROM jadval WHERE shart', 'c': False}]},
        {'t': 'WHERE ni yozmasangiz nima bo\'ladi?', 'a': [{'t': 'Barcha qatorlar o\'chiriladi', 'c': True}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa bo\'lmaydi', 'c': False}, {'t': 'Faqat birinchi qator o\'chiriladi', 'c': False}]},
        {'t': 'DELETE va DROP orasidagi farq?', 'a': [{'t': 'DELETE qatorlarni, DROP jadvalning o\'zini o\'chiradi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'DROP tezroq ishlaydi', 'c': False}, {'t': 'DELETE jadvalning o\'zini o\'chiradi', 'c': False}]},
        {'t': 'DELETE va TRUNCATE orasidagi farq?', 'a': [{'t': 'DELETE WHERE bilan ishlaydi, TRUNCATE barcha qatorlarni tezda o\'chiradi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'TRUNCATE WHERE bilan ishlaydi', 'c': False}, {'t': 'DELETE tezroq ishlaydi', 'c': False}]},
    ]},

    {'n': 'CREATE TABLE - Jadval yaratish', 't': 30, 'o': 14, 'q': [
        {'t': 'CREATE TABLE nima uchun ishlatiladi?', 'a': [{'t': 'Yangi jadval yaratish uchun', 'c': True}, {'t': 'Ma\'lumot qo\'shish uchun', 'c': False}, {'t': 'Jadval o\'chirish uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}]},
        {'t': 'CREATE TABLE qanday yoziladi?', 'a': [{'t': 'CREATE TABLE jadval_nomi (ustun1 tip, ustun2 tip)', 'c': True}, {'t': 'CREATE jadval_nomi (ustun1 tip, ustun2 tip)', 'c': False}, {'t': 'NEW TABLE jadval_nomi (ustun1 tip, ustun2 tip)', 'c': False}, {'t': 'MAKE TABLE jadval_nomi (ustun1 tip, ustun2 tip)', 'c': False}]},
        {'t': 'INT ma\'lumot turi nima uchun?', 'a': [{'t': 'Butun sonlar uchun', 'c': True}, {'t': 'Matn uchun', 'c': False}, {'t': 'Sana uchun', 'c': False}, {'t': 'Haqiqiy sonlar uchun', 'c': False}]},
        {'t': 'VARCHAR ma\'lumot turi nima uchun?', 'a': [{'t': 'O\'zgaruvchan uzunlikdagi matn uchun', 'c': True}, {'t': 'Butun sonlar uchun', 'c': False}, {'t': 'Sana uchun', 'c': False}, {'t': 'Mantiqiy qiymatlar uchun', 'c': False}]},
        {'t': 'DATE ma\'lumot turi nima uchun?', 'a': [{'t': 'Sana saqlash uchun', 'c': True}, {'t': 'Matn uchun', 'c': False}, {'t': 'Butun sonlar uchun', 'c': False}, {'t': 'Vaqt uchun', 'c': False}]},
        {'t': 'PRIMARY KEY nima?', 'a': [{'t': 'Har bir qatorni noyob aniqlash uchun kalit', 'c': True}, {'t': 'Parol', 'c': False}, {'t': 'Foydalanuvchi nomi', 'c': False}, {'t': 'Jadval nomi', 'c': False}]},
        {'t': 'NOT NULL nima degani?', 'a': [{'t': 'Ustun bo\'sh bo\'lishi mumkin emas', 'c': True}, {'t': 'Ustun bo\'sh bo\'lishi mumkin', 'c': False}, {'t': 'Ustun noyob bo\'lishi kerak', 'c': False}, {'t': 'Ustun raqam bo\'lishi kerak', 'c': False}]},
        {'t': 'AUTO_INCREMENT nima qiladi?', 'a': [{'t': 'Har bir yangi qatorda avtomatik oshadi', 'c': True}, {'t': 'Qiymatni kamaytiradi', 'c': False}, {'t': 'Tasodifiy raqam beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'ALTER TABLE - Jadval o\'zgartirish', 't': 30, 'o': 15, 'q': [
        {'t': 'ALTER TABLE nima uchun ishlatiladi?', 'a': [{'t': 'Mavjud jadval strukturasini o\'zgartirish uchun', 'c': True}, {'t': 'Yangi jadval yaratish uchun', 'c': False}, {'t': 'Ma\'lumot qo\'shish uchun', 'c': False}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}]},
        {'t': 'Yangi ustun qo\'shish uchun?', 'a': [{'t': 'ALTER TABLE jadval ADD ustun tip', 'c': True}, {'t': 'ALTER TABLE jadval INSERT ustun tip', 'c': False}, {'t': 'ALTER TABLE jadval CREATE ustun tip', 'c': False}, {'t': 'ALTER TABLE jadval NEW ustun tip', 'c': False}]},
        {'t': 'Ustunni o\'chirish uchun?', 'a': [{'t': 'ALTER TABLE jadval DROP COLUMN ustun', 'c': True}, {'t': 'ALTER TABLE jadval DELETE ustun', 'c': False}, {'t': 'ALTER TABLE jadval REMOVE ustun', 'c': False}, {'t': 'ALTER TABLE jadval DROP ustun', 'c': False}]},
        {'t': 'Ustun tipini o\'zgartirish uchun?', 'a': [{'t': 'ALTER TABLE jadval MODIFY COLUMN ustun yangi_tip', 'c': True}, {'t': 'ALTER TABLE jadval CHANGE ustun yangi_tip', 'c': False}, {'t': 'ALTER TABLE jadval UPDATE ustun yangi_tip', 'c': False}, {'t': 'ALTER TABLE jadval SET ustun yangi_tip', 'c': False}]},
        {'t': 'Ustun nomini o\'zgartirish uchun?', 'a': [{'t': 'ALTER TABLE jadval RENAME COLUMN eski TO yangi', 'c': True}, {'t': 'ALTER TABLE jadval CHANGE eski yangi', 'c': False}, {'t': 'ALTER TABLE jadval UPDATE eski TO yangi', 'c': False}, {'t': 'ALTER TABLE jadval MODIFY eski TO yangi', 'c': False}]},
        {'t': 'ALTER TABLE ma\'lumotlarni o\'chiradi?', 'a': [{'t': 'Yo\'q, faqat strukturani o\'zgartiradi', 'c': True}, {'t': 'Ha, barcha ma\'lumotlarni o\'chiradi', 'c': False}, {'t': 'Ba\'zi ma\'lumotlarni o\'chiradi', 'c': False}, {'t': 'Faqat yangi ustun qo\'shganda', 'c': False}]},
    ]},

    {'n': 'DROP TABLE - Jadval o\'chirish', 't': 20, 'o': 16, 'q': [
        {'t': 'DROP TABLE nima uchun ishlatiladi?', 'a': [{'t': 'Jadvalni butunlay o\'chirish uchun', 'c': True}, {'t': 'Faqat ma\'lumotlarni o\'chirish uchun', 'c': False}, {'t': 'Jadval strukturasini o\'zgartirish uchun', 'c': False}, {'t': 'Yangi jadval yaratish uchun', 'c': False}]},
        {'t': 'DROP TABLE qanday yoziladi?', 'a': [{'t': 'DROP TABLE jadval_nomi', 'c': True}, {'t': 'DELETE TABLE jadval_nomi', 'c': False}, {'t': 'REMOVE TABLE jadval_nomi', 'c': False}, {'t': 'DESTROY TABLE jadval_nomi', 'c': False}]},
        {'t': 'DROP TABLE ma\'lumotlarni ham o\'chiradi?', 'a': [{'t': 'Ha, jadval va barcha ma\'lumotlar o\'chiriladi', 'c': True}, {'t': 'Yo\'q, faqat strukturani o\'chiradi', 'c': False}, {'t': 'Faqat ma\'lumotlarni o\'chiradi', 'c': False}, {'t': 'Hech narsani o\'chirmaydi', 'c': False}]},
        {'t': 'DROP TABLE IF EXISTS nima uchun ishlatiladi?', 'a': [{'t': 'Jadval mavjud bo\'lsa o\'chiradi, aks holda xatolik bermaydi', 'c': True}, {'t': 'Faqat bo\'sh jadvallarni o\'chiradi', 'c': False}, {'t': 'Jadval mavjudligini tekshiradi', 'c': False}, {'t': 'Jadval yaratadi', 'c': False}]},
        {'t': 'DROP va DELETE orasidagi farq?', 'a': [{'t': 'DROP jadvalning o\'zini, DELETE faqat qatorlarni o\'chiradi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'DELETE tezroq ishlaydi', 'c': False}, {'t': 'DROP faqat qatorlarni o\'chiradi', 'c': False}]},
    ]},

    {'n': 'LIKE - Naqsh bo\'yicha qidirish', 't': 25, 'o': 17, 'q': [
        {'t': 'LIKE operatori nima uchun ishlatiladi?', 'a': [{'t': 'Matnda naqsh bo\'yicha qidirish uchun', 'c': True}, {'t': 'Raqamlarni solishtirish uchun', 'c': False}, {'t': 'Sanalarni solishtirish uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}]},
        {'t': '% belgisi nima bildiradi?', 'a': [{'t': 'Istalgan miqdordagi istalgan belgilar', 'c': True}, {'t': 'Bitta istalgan belgi', 'c': False}, {'t': 'Bo\'sh joy', 'c': False}, {'t': 'Raqam', 'c': False}]},
        {'t': '_ belgisi nima bildiradi?', 'a': [{'t': 'Bitta istalgan belgi', 'c': True}, {'t': 'Istalgan miqdordagi belgilar', 'c': False}, {'t': 'Bo\'sh joy', 'c': False}, {'t': 'Harf', 'c': False}]},
        {'t': '"A" harfi bilan boshlanadigan qiymatlarni topish?', 'a': [{'t': 'WHERE ustun LIKE \'A%\'', 'c': True}, {'t': 'WHERE ustun LIKE \'%A\'', 'c': False}, {'t': 'WHERE ustun LIKE \'_A%\'', 'c': False}, {'t': 'WHERE ustun = \'A%\'', 'c': False}]},
        {'t': '"a" harfi bilan tugaydigan qiymatlarni topish?', 'a': [{'t': 'WHERE ustun LIKE \'%a\'', 'c': True}, {'t': 'WHERE ustun LIKE \'a%\'', 'c': False}, {'t': 'WHERE ustun LIKE \'%a_\'', 'c': False}, {'t': 'WHERE ustun = \'%a\'', 'c': False}]},
        {'t': 'Ichida "test" so\'zi bo\'lgan qiymatlarni topish?', 'a': [{'t': 'WHERE ustun LIKE \'%test%\'', 'c': True}, {'t': 'WHERE ustun LIKE \'test%\'', 'c': False}, {'t': 'WHERE ustun LIKE \'%test\'', 'c': False}, {'t': 'WHERE ustun = \'test\'', 'c': False}]},
    ]},

    {'n': 'IN - Ro\'yxatda qidirish', 't': 20, 'o': 18, 'q': [
        {'t': 'IN operatori nima uchun ishlatiladi?', 'a': [{'t': 'Bir nechta qiymatlar ro\'yxatida qidirish uchun', 'c': True}, {'t': 'Matnda qidirish uchun', 'c': False}, {'t': 'Raqamlarni qo\'shish uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}]},
        {'t': 'IN operatori qanday yoziladi?', 'a': [{'t': 'WHERE ustun IN (qiymat1, qiymat2, qiymat3)', 'c': True}, {'t': 'WHERE ustun = (qiymat1, qiymat2, qiymat3)', 'c': False}, {'t': 'WHERE ustun CONTAINS (qiymat1, qiymat2)', 'c': False}, {'t': 'WHERE ustun HAS (qiymat1, qiymat2)', 'c': False}]},
        {'t': 'IN operatori nechta OR operatorini almashtiradi?', 'a': [{'t': 'Ko\'p sonli OR larni qisqartiradi', 'c': True}, {'t': 'Faqat 2 ta OR', 'c': False}, {'t': 'Faqat 3 ta OR', 'c': False}, {'t': 'Hech qaysini almashtirmaydi', 'c': False}]},
        {'t': 'NOT IN nima qiladi?', 'a': [{'t': 'Ro\'yxatda yo\'q qiymatlarni tanlaydi', 'c': True}, {'t': 'Ro\'yxatdagi qiymatlarni tanlaydi', 'c': False}, {'t': 'Barcha qiymatlarni tanlaydi', 'c': False}, {'t': 'Hech narsani tanlamaydi', 'c': False}]},
        {'t': 'IN operatori subquery bilan ishlaydi?', 'a': [{'t': 'Ha, WHERE ustun IN (SELECT ...)', 'c': True}, {'t': 'Yo\'q, faqat qiymatlar ro\'yxati bilan', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'BETWEEN - Oraliq qidirish', 't': 20, 'o': 19, 'q': [
        {'t': 'BETWEEN operatori nima uchun ishlatiladi?', 'a': [{'t': 'Ikki qiymat oralig\'idagi ma\'lumotlarni tanlash uchun', 'c': True}, {'t': 'Matnda qidirish uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'BETWEEN qanday yoziladi?', 'a': [{'t': 'WHERE ustun BETWEEN qiymat1 AND qiymat2', 'c': True}, {'t': 'WHERE ustun BETWEEN qiymat1 TO qiymat2', 'c': False}, {'t': 'WHERE ustun FROM qiymat1 TO qiymat2', 'c': False}, {'t': 'WHERE ustun IN qiymat1 AND qiymat2', 'c': False}]},
        {'t': 'BETWEEN chegaraviy qiymatlarni o\'z ichiga oladimi?', 'a': [{'t': 'Ha, ikkala chegarani ham o\'z ichiga oladi', 'c': True}, {'t': 'Yo\'q, faqat oradagi qiymatlar', 'c': False}, {'t': 'Faqat birinchi chegarani', 'c': False}, {'t': 'Faqat ikkinchi chegarani', 'c': False}]},
        {'t': 'BETWEEN sanalar bilan ishlaydi?', 'a': [{'t': 'Ha, WHERE sana BETWEEN \'2024-01-01\' AND \'2024-12-31\'', 'c': True}, {'t': 'Yo\'q, faqat raqamlar bilan', 'c': False}, {'t': 'Faqat matn bilan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'NOT BETWEEN nima qiladi?', 'a': [{'t': 'Oraliqdan tashqaridagi qiymatlarni tanlaydi', 'c': True}, {'t': 'Oraliqdagi qiymatlarni tanlaydi', 'c': False}, {'t': 'Barcha qiymatlarni tanlaydi', 'c': False}, {'t': 'Hech narsani tanlamaydi', 'c': False}]},
    ]},

    {'n': 'NULL qiymatlar bilan ishlash', 't': 25, 'o': 20, 'q': [
        {'t': 'NULL nima?', 'a': [{'t': 'Qiymat yo\'qligi yoki noma\'lumligini bildiradi', 'c': True}, {'t': 'Nol raqami', 'c': False}, {'t': 'Bo\'sh matn', 'c': False}, {'t': 'False qiymati', 'c': False}]},
        {'t': 'NULL va 0 orasidagi farq?', 'a': [{'t': 'NULL qiymat yo\'q, 0 raqam', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': '0 qiymat yo\'q', 'c': False}, {'t': 'NULL raqam', 'c': False}]},
        {'t': 'NULL qiymatlarni qanday tekshiriladi?', 'a': [{'t': 'WHERE ustun IS NULL', 'c': True}, {'t': 'WHERE ustun = NULL', 'c': False}, {'t': 'WHERE ustun == NULL', 'c': False}, {'t': 'WHERE ustun EQUALS NULL', 'c': False}]},
        {'t': 'NULL bo\'lmagan qiymatlarni qanday tekshiriladi?', 'a': [{'t': 'WHERE ustun IS NOT NULL', 'c': True}, {'t': 'WHERE ustun != NULL', 'c': False}, {'t': 'WHERE ustun <> NULL', 'c': False}, {'t': 'WHERE ustun NOT EQUALS NULL', 'c': False}]},
        {'t': 'NULL bilan arifmetik amallar natijasi?', 'a': [{'t': 'NULL qaytaradi', 'c': True}, {'t': '0 qaytaradi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Qiymatning o\'zini qaytaradi', 'c': False}]},
        {'t': 'COALESCE funksiyasi nima qiladi?', 'a': [{'t': 'NULL bo\'lmagan birinchi qiymatni qaytaradi', 'c': True}, {'t': 'NULL qiymatlarni sanaydi', 'c': False}, {'t': 'NULL qiymatlarni o\'chiradi', 'c': False}, {'t': 'Barcha qiymatlarni NULL qiladi', 'c': False}]},
    ]},

    {'n': 'JOIN - Jadvallarni birlashtirish', 't': 30, 'o': 21, 'q': [
        {'t': 'JOIN nima uchun ishlatiladi?', 'a': [{'t': 'Bir nechta jadvallardan ma\'lumotlarni birlashtirish uchun', 'c': True}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Ma\'lumotni o\'chirish uchun', 'c': False}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}]},
        {'t': 'INNER JOIN nima qiladi?', 'a': [{'t': 'Ikkala jadvalda ham mos keladigan qatorlarni qaytaradi', 'c': True}, {'t': 'Barcha qatorlarni qaytaradi', 'c': False}, {'t': 'Faqat birinchi jadval qatorlarini qaytaradi', 'c': False}, {'t': 'Faqat ikkinchi jadval qatorlarini qaytaradi', 'c': False}]},
        {'t': 'JOIN qanday yoziladi?', 'a': [{'t': 'SELECT * FROM jadval1 JOIN jadval2 ON jadval1.id = jadval2.id', 'c': True}, {'t': 'SELECT * FROM jadval1, jadval2 WHERE id = id', 'c': False}, {'t': 'SELECT * JOIN jadval1 WITH jadval2', 'c': False}, {'t': 'JOIN jadval1 AND jadval2', 'c': False}]},
        {'t': 'ON kalit so\'zi nima uchun ishlatiladi?', 'a': [{'t': 'Jadvallarni qaysi ustun bo\'yicha birlashtirishni ko\'rsatish uchun', 'c': True}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Ma\'lumotni saralash uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}]},
        {'t': 'Bir nechta jadval bilan JOIN qilish mumkinmi?', 'a': [{'t': 'Ha, ketma-ket JOIN lar yozish mumkin', 'c': True}, {'t': 'Yo\'q, faqat 2 ta jadval', 'c': False}, {'t': 'Faqat 3 ta jadval', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'JOIN va WHERE birgalikda ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, JOIN dan keyin WHERE yoziladi', 'c': True}, {'t': 'Yo\'q, faqat bittasi', 'c': False}, {'t': 'Ha, lekin WHERE birinchi', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'LEFT JOIN - Chap birlashtirish', 't': 25, 'o': 22, 'q': [
        {'t': 'LEFT JOIN nima qiladi?', 'a': [{'t': 'Chap jadvaldagi barcha va o\'ng jadvaldagi mos qatorlarni qaytaradi', 'c': True}, {'t': 'Faqat mos keladigan qatorlarni qaytaradi', 'c': False}, {'t': 'O\'ng jadvaldagi barcha qatorlarni qaytaradi', 'c': False}, {'t': 'Hech qanday qator qaytarmaydi', 'c': False}]},
        {'t': 'LEFT JOIN da o\'ng jadvalda mos qator bo\'lmasa?', 'a': [{'t': 'O\'ng jadval ustunlari NULL bo\'ladi', 'c': True}, {'t': 'Qator ko\'rsatilmaydi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': '0 qiymati bo\'ladi', 'c': False}]},
        {'t': 'LEFT JOIN va LEFT OUTER JOIN orasidagi farq?', 'a': [{'t': 'Farqi yo\'q, bir xil', 'c': True}, {'t': 'LEFT JOIN tezroq ishlaydi', 'c': False}, {'t': 'LEFT OUTER JOIN ko\'proq qator qaytaradi', 'c': False}, {'t': 'Butunlay boshqacha', 'c': False}]},
        {'t': 'LEFT JOIN qanday yoziladi?', 'a': [{'t': 'SELECT * FROM jadval1 LEFT JOIN jadval2 ON jadval1.id = jadval2.id', 'c': True}, {'t': 'SELECT * FROM jadval1 JOIN LEFT jadval2 ON id = id', 'c': False}, {'t': 'LEFT JOIN jadval1, jadval2 WHERE id = id', 'c': False}, {'t': 'SELECT LEFT * FROM jadval1, jadval2', 'c': False}]},
        {'t': 'LEFT JOIN da qaysi jadval to\'liq ko\'rsatiladi?', 'a': [{'t': 'Chap jadval (FROM dan keyingi)', 'c': True}, {'t': 'O\'ng jadval (JOIN dan keyingi)', 'c': False}, {'t': 'Ikkala jadval ham', 'c': False}, {'t': 'Hech qaysi jadval', 'c': False}]},
    ]},

    {'n': 'RIGHT JOIN - O\'ng birlashtirish', 't': 25, 'o': 23, 'q': [
        {'t': 'RIGHT JOIN nima qiladi?', 'a': [{'t': 'O\'ng jadvaldagi barcha va chap jadvaldagi mos qatorlarni qaytaradi', 'c': True}, {'t': 'Faqat mos keladigan qatorlarni qaytaradi', 'c': False}, {'t': 'Chap jadvaldagi barcha qatorlarni qaytaradi', 'c': False}, {'t': 'Hech qanday qator qaytarmaydi', 'c': False}]},
        {'t': 'RIGHT JOIN da chap jadvalda mos qator bo\'lmasa?', 'a': [{'t': 'Chap jadval ustunlari NULL bo\'ladi', 'c': True}, {'t': 'Qator ko\'rsatilmaydi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': '0 qiymati bo\'ladi', 'c': False}]},
        {'t': 'RIGHT JOIN va RIGHT OUTER JOIN orasidagi farq?', 'a': [{'t': 'Farqi yo\'q, bir xil', 'c': True}, {'t': 'RIGHT JOIN tezroq ishlaydi', 'c': False}, {'t': 'RIGHT OUTER JOIN ko\'proq qator qaytaradi', 'c': False}, {'t': 'Butunlay boshqacha', 'c': False}]},
        {'t': 'RIGHT JOIN qanday yoziladi?', 'a': [{'t': 'SELECT * FROM jadval1 RIGHT JOIN jadval2 ON jadval1.id = jadval2.id', 'c': True}, {'t': 'SELECT * FROM jadval1 JOIN RIGHT jadval2 ON id = id', 'c': False}, {'t': 'RIGHT JOIN jadval1, jadval2 WHERE id = id', 'c': False}, {'t': 'SELECT RIGHT * FROM jadval1, jadval2', 'c': False}]},
        {'t': 'LEFT JOIN va RIGHT JOIN orasidagi farq?', 'a': [{'t': 'LEFT chap jadvalni, RIGHT o\'ng jadvalni to\'liq ko\'rsatadi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'LEFT tezroq ishlaydi', 'c': False}, {'t': 'RIGHT ko\'proq qator qaytaradi', 'c': False}]},
    ]},

    {'n': 'FULL JOIN - To\'liq birlashtirish', 't': 25, 'o': 24, 'q': [
        {'t': 'FULL JOIN nima qiladi?', 'a': [{'t': 'Ikkala jadvaldagi barcha qatorlarni qaytaradi', 'c': True}, {'t': 'Faqat mos keladigan qatorlarni qaytaradi', 'c': False}, {'t': 'Faqat chap jadval qatorlarini qaytaradi', 'c': False}, {'t': 'Faqat o\'ng jadval qatorlarini qaytaradi', 'c': False}]},
        {'t': 'FULL JOIN da mos qator bo\'lmasa?', 'a': [{'t': 'Mos bo\'lmagan ustunlar NULL bo\'ladi', 'c': True}, {'t': 'Qator ko\'rsatilmaydi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': '0 qiymati bo\'ladi', 'c': False}]},
        {'t': 'FULL JOIN va FULL OUTER JOIN orasidagi farq?', 'a': [{'t': 'Farqi yo\'q, bir xil', 'c': True}, {'t': 'FULL JOIN tezroq ishlaydi', 'c': False}, {'t': 'FULL OUTER JOIN ko\'proq qator qaytaradi', 'c': False}, {'t': 'Butunlay boshqacha', 'c': False}]},
        {'t': 'FULL JOIN qanday yoziladi?', 'a': [{'t': 'SELECT * FROM jadval1 FULL JOIN jadval2 ON jadval1.id = jadval2.id', 'c': True}, {'t': 'SELECT * FROM jadval1 JOIN FULL jadval2 ON id = id', 'c': False}, {'t': 'FULL JOIN jadval1, jadval2 WHERE id = id', 'c': False}, {'t': 'SELECT FULL * FROM jadval1, jadval2', 'c': False}]},
        {'t': 'FULL JOIN LEFT va RIGHT JOIN ning kombinatsiyasi?', 'a': [{'t': 'Ha, ikkala jadvalning barcha qatorlarini oladi', 'c': True}, {'t': 'Yo\'q, butunlay boshqacha', 'c': False}, {'t': 'Faqat LEFT JOIN ga o\'xshaydi', 'c': False}, {'t': 'Faqat RIGHT JOIN ga o\'xshaydi', 'c': False}]},
    ]},

    {'n': 'UNION - Natijalarni birlashtirish', 't': 25, 'o': 25, 'q': [
        {'t': 'UNION nima uchun ishlatiladi?', 'a': [{'t': 'Ikki yoki undan ortiq SELECT natijalarini birlashtirish uchun', 'c': True}, {'t': 'Jadvallarni birlashtirish uchun', 'c': False}, {'t': 'Ma\'lumotni filtrlash uchun', 'c': False}, {'t': 'Ma\'lumotni yangilash uchun', 'c': False}]},
        {'t': 'UNION qanday yoziladi?', 'a': [{'t': 'SELECT ustun FROM jadval1 UNION SELECT ustun FROM jadval2', 'c': True}, {'t': 'SELECT ustun FROM jadval1 AND jadval2', 'c': False}, {'t': 'UNION jadval1, jadval2', 'c': False}, {'t': 'SELECT UNION ustun FROM jadval1, jadval2', 'c': False}]},
        {'t': 'UNION takrorlanuvchi qatorlarni ko\'rsatadimi?', 'a': [{'t': 'Yo\'q, faqat noyob qatorlarni ko\'rsatadi', 'c': True}, {'t': 'Ha, barcha qatorlarni ko\'rsatadi', 'c': False}, {'t': 'Ba\'zan ko\'rsatadi', 'c': False}, {'t': 'Hech qachon qator ko\'rsatmaydi', 'c': False}]},
        {'t': 'UNION ALL nima qiladi?', 'a': [{'t': 'Takrorlanuvchi qatorlarni ham ko\'rsatadi', 'c': True}, {'t': 'Faqat noyob qatorlarni ko\'rsatadi', 'c': False}, {'t': 'Hech qanday qator ko\'rsatmaydi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}]},
        {'t': 'UNION da SELECT lardagi ustunlar soni bir xil bo\'lishi kerakmi?', 'a': [{'t': 'Ha, ustunlar soni va tiplari mos bo\'lishi kerak', 'c': True}, {'t': 'Yo\'q, farqi yo\'q', 'c': False}, {'t': 'Faqat ustunlar soni mos bo\'lishi kerak', 'c': False}, {'t': 'Faqat ustun tiplari mos bo\'lishi kerak', 'c': False}]},
        {'t': 'UNION va JOIN orasidagi farq?', 'a': [{'t': 'UNION qatorlarni, JOIN ustunlarni birlashtiradi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'UNION tezroq ishlaydi', 'c': False}, {'t': 'JOIN qatorlarni birlashtiradi', 'c': False}]},
    ]},

    {'n': 'Subquery - Ichki so\'rovlar', 't': 30, 'o': 26, 'q': [
        {'t': 'Subquery nima?', 'a': [{'t': 'Boshqa so\'rov ichidagi so\'rov', 'c': True}, {'t': 'Jadval nomi', 'c': False}, {'t': 'Ustun nomi', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
        {'t': 'Subquery qanday yoziladi?', 'a': [{'t': 'SELECT * FROM jadval WHERE ustun = (SELECT ...)', 'c': True}, {'t': 'SELECT * FROM (jadval WHERE ustun = SELECT)', 'c': False}, {'t': 'SELECT SUBQUERY * FROM jadval', 'c': False}, {'t': 'SUBQUERY SELECT * FROM jadval', 'c': False}]},
        {'t': 'Subquery qavs ichida yozilishi kerakmi?', 'a': [{'t': 'Ha, doim qavs ichida yoziladi', 'c': True}, {'t': 'Yo\'q, qavs shart emas', 'c': False}, {'t': 'Ba\'zan qavs kerak', 'c': False}, {'t': 'Hech qachon qavs ishlatilmaydi', 'c': False}]},
        {'t': 'Subquery WHERE da ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, WHERE ustun = (SELECT ...)', 'c': True}, {'t': 'Yo\'q, faqat FROM da', 'c': False}, {'t': 'Yo\'q, faqat SELECT da', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Subquery FROM da ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, FROM (SELECT ...) AS nom', 'c': True}, {'t': 'Yo\'q, faqat WHERE da', 'c': False}, {'t': 'Yo\'q, faqat SELECT da', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Subquery SELECT da ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, SELECT ustun, (SELECT ...) FROM jadval', 'c': True}, {'t': 'Yo\'q, faqat WHERE da', 'c': False}, {'t': 'Yo\'q, faqat FROM da', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Subquery bir nechta qator qaytarishi mumkinmi?', 'a': [{'t': 'Ha, lekin IN, ANY, ALL operatorlari bilan', 'c': True}, {'t': 'Yo\'q, faqat bitta qator', 'c': False}, {'t': 'Faqat 2 ta qator', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'INDEX - Indekslar', 't': 25, 'o': 27, 'q': [
        {'t': 'INDEX nima?', 'a': [{'t': 'Ma\'lumotlarni tezroq qidirish uchun maxsus struktura', 'c': True}, {'t': 'Jadval nomi', 'c': False}, {'t': 'Ustun nomi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}]},
        {'t': 'INDEX ning asosiy maqsadi nima?', 'a': [{'t': 'SELECT so\'rovlarini tezlashtirish', 'c': True}, {'t': 'INSERT ni tezlashtirish', 'c': False}, {'t': 'UPDATE ni tezlashtirish', 'c': False}, {'t': 'DELETE ni tezlashtirish', 'c': False}]},
        {'t': 'INDEX qanday yaratiladi?', 'a': [{'t': 'CREATE INDEX indeks_nomi ON jadval(ustun)', 'c': True}, {'t': 'CREATE INDEX jadval(ustun)', 'c': False}, {'t': 'INDEX CREATE ON jadval(ustun)', 'c': False}, {'t': 'NEW INDEX jadval(ustun)', 'c': False}]},
        {'t': 'INDEX qanday o\'chiriladi?', 'a': [{'t': 'DROP INDEX indeks_nomi', 'c': True}, {'t': 'DELETE INDEX indeks_nomi', 'c': False}, {'t': 'REMOVE INDEX indeks_nomi', 'c': False}, {'t': 'DESTROY INDEX indeks_nomi', 'c': False}]},
        {'t': 'INDEX ning kamchiligi nima?', 'a': [{'t': 'INSERT, UPDATE, DELETE sekinlashadi', 'c': True}, {'t': 'SELECT sekinlashadi', 'c': False}, {'t': 'Hech qanday kamchilik yo\'q', 'c': False}, {'t': 'Jadval o\'chiriladi', 'c': False}]},
        {'t': 'Bir nechta ustun bo\'yicha INDEX yaratish mumkinmi?', 'a': [{'t': 'Ha, CREATE INDEX indeks ON jadval(ustun1, ustun2)', 'c': True}, {'t': 'Yo\'q, faqat bitta ustun', 'c': False}, {'t': 'Faqat 2 ta ustun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'VIEW - Ko\'rinishlar', 't': 25, 'o': 28, 'q': [
        {'t': 'VIEW nima?', 'a': [{'t': 'Virtual jadval, SELECT so\'rovi asosida yaratiladi', 'c': True}, {'t': 'Oddiy jadval', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'VIEW qanday yaratiladi?', 'a': [{'t': 'CREATE VIEW view_nomi AS SELECT ...', 'c': True}, {'t': 'CREATE VIEW SELECT ...', 'c': False}, {'t': 'NEW VIEW AS SELECT ...', 'c': False}, {'t': 'VIEW CREATE SELECT ...', 'c': False}]},
        {'t': 'VIEW ma\'lumot saqlaydi?', 'a': [{'t': 'Yo\'q, faqat so\'rovni saqlaydi', 'c': True}, {'t': 'Ha, ma\'lumot saqlaydi', 'c': False}, {'t': 'Ba\'zan saqlaydi', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'VIEW qanday ishlatiladi?', 'a': [{'t': 'Oddiy jadval kabi: SELECT * FROM view_nomi', 'c': True}, {'t': 'VIEW view_nomi', 'c': False}, {'t': 'GET VIEW view_nomi', 'c': False}, {'t': 'SHOW VIEW view_nomi', 'c': False}]},
        {'t': 'VIEW qanday o\'chiriladi?', 'a': [{'t': 'DROP VIEW view_nomi', 'c': True}, {'t': 'DELETE VIEW view_nomi', 'c': False}, {'t': 'REMOVE VIEW view_nomi', 'c': False}, {'t': 'DESTROY VIEW view_nomi', 'c': False}]},
        {'t': 'VIEW ning afzalligi nima?', 'a': [{'t': 'Murakkab so\'rovlarni soddalashtirib, xavfsizlikni oshiradi', 'c': True}, {'t': 'Ma\'lumotni tezroq saqlaydi', 'c': False}, {'t': 'Disk joyini tejaydi', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},

    {'n': 'Transaksiyalar - BEGIN, COMMIT, ROLLBACK', 't': 30, 'o': 29, 'q': [
        {'t': 'Transaksiya nima?', 'a': [{'t': 'Bir nechta SQL buyruqlarini bitta mantiqiy birlik sifatida bajarish', 'c': True}, {'t': 'Oddiy SELECT so\'rovi', 'c': False}, {'t': 'Jadval yaratish', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}]},
        {'t': 'Transaksiya qanday boshlanadi?', 'a': [{'t': 'BEGIN yoki START TRANSACTION', 'c': True}, {'t': 'START', 'c': False}, {'t': 'OPEN TRANSACTION', 'c': False}, {'t': 'NEW TRANSACTION', 'c': False}]},
        {'t': 'COMMIT nima qiladi?', 'a': [{'t': 'Transaksiya o\'zgarishlarini saqlaydi', 'c': True}, {'t': 'Transaksiyani bekor qiladi', 'c': False}, {'t': 'Transaksiyani boshlaydi', 'c': False}, {'t': 'Transaksiyani to\'xtatadi', 'c': False}]},
        {'t': 'ROLLBACK nima qiladi?', 'a': [{'t': 'Transaksiya o\'zgarishlarini bekor qiladi', 'c': True}, {'t': 'Transaksiyani saqlaydi', 'c': False}, {'t': 'Transaksiyani boshlaydi', 'c': False}, {'t': 'Transaksiyani davom ettiradi', 'c': False}]},
        {'t': 'Transaksiyaning ACID xususiyatlari nima?', 'a': [{'t': 'Atomicity, Consistency, Isolation, Durability', 'c': True}, {'t': 'Add, Create, Insert, Delete', 'c': False}, {'t': 'All, Complete, Isolated, Done', 'c': False}, {'t': 'Auto, Commit, Insert, Drop', 'c': False}]},
        {'t': 'Transaksiya ichida xatolik bo\'lsa nima qilish kerak?', 'a': [{'t': 'ROLLBACK qilish kerak', 'c': True}, {'t': 'COMMIT qilish kerak', 'c': False}, {'t': 'Hech narsa qilmaslik kerak', 'c': False}, {'t': 'Transaksiyani qayta boshlash kerak', 'c': False}]},
        {'t': 'Transaksiya ichida bir nechta buyruq bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, istalgan miqdorda', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Faqat 3 ta', 'c': False}]},
    ]},

    {'n': 'SQL xavfsizligi va eng yaxshi amaliyotlar', 't': 30, 'o': 30, 'q': [
        {'t': 'SQL Injection nima?', 'a': [{'t': 'Zararli SQL kodini kiritish orqali hujum', 'c': True}, {'t': 'Ma\'lumot bazasini tezlashtirish usuli', 'c': False}, {'t': 'Yangi jadval yaratish', 'c': False}, {'t': 'Ma\'lumotni saqlash usuli', 'c': False}]},
        {'t': 'SQL Injection dan qanday himoyalanish mumkin?', 'a': [{'t': 'Prepared statements va parametrlangan so\'rovlar ishlatish', 'c': True}, {'t': 'Faqat SELECT ishlatish', 'c': False}, {'t': 'Parolsiz ishlash', 'c': False}, {'t': 'Hech qanday himoya kerak emas', 'c': False}]},
        {'t': 'Foydalanuvchi kiritgan ma\'lumotni to\'g\'ridan-to\'g\'ri SQL ga qo\'shish xavfli?', 'a': [{'t': 'Ha, juda xavfli', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Ba\'zan xavfli', 'c': False}, {'t': 'Hech qachon xavfli emas', 'c': False}]},
        {'t': 'SELECT * ishlatish yaxshi amaliyotmi?', 'a': [{'t': 'Yo\'q, faqat kerakli ustunlarni tanlash yaxshi', 'c': True}, {'t': 'Ha, har doim ishlatish kerak', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Faqat katta jadvallarda', 'c': False}]},
        {'t': 'INDEX qachon yaratish kerak?', 'a': [{'t': 'Tez-tez qidiriluvchi ustunlarda', 'c': True}, {'t': 'Barcha ustunlarda', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat PRIMARY KEY da', 'c': False}]},
        {'t': 'WHERE siz UPDATE yoki DELETE ishlatish xavfli?', 'a': [{'t': 'Ha, barcha qatorlar o\'zgaradi/o\'chiriladi', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Ba\'zan xavfli', 'c': False}, {'t': 'Hech qachon xavfli emas', 'c': False}]},
        {'t': 'Ma\'lumotlar bazasini zaxiralash (backup) kerakmi?', 'a': [{'t': 'Ha, muntazam zaxiralash juda muhim', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Faqat katta bazalarda', 'c': False}, {'t': 'Faqat yiliga bir marta', 'c': False}]},
        {'t': 'Parollarni ma\'lumotlar bazasida qanday saqlash kerak?', 'a': [{'t': 'Hash qilingan holda (masalan, bcrypt)', 'c': True}, {'t': 'Oddiy matn sifatida', 'c': False}, {'t': 'Base64 kodlangan holda', 'c': False}, {'t': 'Teskari tartibda', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_sql()
    add_topics(subj, T)
    print(f"\n✅ SQL - {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
