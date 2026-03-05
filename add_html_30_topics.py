"""
HTML DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_html():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='HTML', defaults={'category': cat, 'description': 'HTML - Veb sahifalar yaratish tili', 'icon': 'bi-filetype-html', 'order': 11, 'is_active': True})
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
    {'n': 'HTML ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'HTML nima?', 'a': [{'t': 'HyperText Markup Language - veb sahifalar yaratish tili', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Operatsion tizim', 'c': False}]},
        {'t': 'HTML faylining kengaytmasi qanday?', 'a': [{'t': '.html yoki .htm', 'c': True}, {'t': '.txt', 'c': False}, {'t': '.doc', 'c': False}, {'t': '.web', 'c': False}]},
        {'t': 'HTML teglar qanday yoziladi?', 'a': [{'t': 'Burchakli qavslar ichida: <tag>', 'c': True}, {'t': 'Kvadrat qavslar ichida: [tag]', 'c': False}, {'t': 'Jingalak qavslar ichida: {tag}', 'c': False}, {'t': 'Oddiy qavslar ichida: (tag)', 'c': False}]},
        {'t': 'HTML dasturlash tili hisoblanadimi?', 'a': [{'t': 'Yo\'q, markup (belgilash) tili', 'c': True}, {'t': 'Ha, dasturlash tili', 'c': False}, {'t': 'Ha, skript tili', 'c': False}, {'t': 'Ha, kompilatsiya tili', 'c': False}]},
        {'t': 'HTML ning asosiy vazifasi nima?', 'a': [{'t': 'Veb sahifa strukturasini yaratish', 'c': True}, {'t': 'Dizayn qilish', 'c': False}, {'t': 'Animatsiya yaratish', 'c': False}, {'t': 'Ma\'lumotlar bazasi bilan ishlash', 'c': False}]},
        {'t': 'HTML qaysi yilda yaratilgan?', 'a': [{'t': '1991 yilda', 'c': True}, {'t': '2000 yilda', 'c': False}, {'t': '1985 yilda', 'c': False}, {'t': '2010 yilda', 'c': False}]},
    ]},
    
    {'n': 'HTML hujjat strukturasi', 't': 25, 'o': 2, 'q': [
        {'t': 'HTML hujjatning asosiy strukturasi qanday?', 'a': [{'t': '<!DOCTYPE html>, <html>, <head>, <body>', 'c': True}, {'t': 'Faqat <html> va <body>', 'c': False}, {'t': 'Faqat <body>', 'c': False}, {'t': 'Struktura kerak emas', 'c': False}]},
        {'t': '<!DOCTYPE html> nima uchun ishlatiladi?', 'a': [{'t': 'HTML versiyasini bildirish uchun', 'c': True}, {'t': 'Sahifa sarlavhasini yozish uchun', 'c': False}, {'t': 'Matn yozish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}]},
        {'t': '<head> tegi ichida nima bo\'ladi?', 'a': [{'t': 'Meta ma\'lumotlar, sarlavha, CSS havolalar', 'c': True}, {'t': 'Sahifa kontenti', 'c': False}, {'t': 'Rasmlar', 'c': False}, {'t': 'Videolar', 'c': False}]},
        {'t': '<body> tegi ichida nima bo\'ladi?', 'a': [{'t': 'Sahifada ko\'rinadigan barcha kontent', 'c': True}, {'t': 'Faqat meta ma\'lumotlar', 'c': False}, {'t': 'Faqat sarlavha', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': '<title> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Brauzer yorlig\'ida ko\'rinadigan sarlavha', 'c': True}, {'t': 'Sahifadagi asosiy sarlavha', 'c': False}, {'t': 'Rasm nomi', 'c': False}, {'t': 'Havola matni', 'c': False}]},
        {'t': '<html> tegida qaysi atribut ko\'rsatiladi?', 'a': [{'t': 'lang="uz" - til ko\'rsatish uchun', 'c': True}, {'t': 'size - o\'lcham uchun', 'c': False}, {'t': 'color - rang uchun', 'c': False}, {'t': 'width - kenglik uchun', 'c': False}]},
        {'t': 'HTML teglar katta-kichik harfga sezgirmi?', 'a': [{'t': 'Yo\'q, lekin kichik harf tavsiya etiladi', 'c': True}, {'t': 'Ha, faqat kichik harf', 'c': False}, {'t': 'Ha, faqat katta harf', 'c': False}, {'t': 'Ha, aralash bo\'lishi kerak', 'c': False}]},
    ]},

    {'n': 'Sarlavha teglari (Headings)', 't': 20, 'o': 3, 'q': [
        {'t': 'HTML da nechta sarlavha tegi bor?', 'a': [{'t': '6 ta: <h1> dan <h6> gacha', 'c': True}, {'t': '5 ta', 'c': False}, {'t': '10 ta', 'c': False}, {'t': '3 ta', 'c': False}]},
        {'t': 'Eng katta sarlavha qaysi?', 'a': [{'t': '<h1>', 'c': True}, {'t': '<h6>', 'c': False}, {'t': '<h3>', 'c': False}, {'t': '<header>', 'c': False}]},
        {'t': 'Eng kichik sarlavha qaysi?', 'a': [{'t': '<h6>', 'c': True}, {'t': '<h1>', 'c': False}, {'t': '<h3>', 'c': False}, {'t': '<small>', 'c': False}]},
        {'t': '<h1>Salom</h1> nima qiladi?', 'a': [{'t': 'Eng katta sarlavha yaratadi', 'c': True}, {'t': 'Oddiy matn yaratadi', 'c': False}, {'t': 'Havola yaratadi', 'c': False}, {'t': 'Rasm qo\'yadi', 'c': False}]},
        {'t': 'Sarlavha teglari SEO uchun muhimmi?', 'a': [{'t': 'Ha, juda muhim', 'c': True}, {'t': 'Yo\'q, ahamiyati yo\'q', 'c': False}, {'t': 'Faqat <h1> muhim', 'c': False}, {'t': 'Faqat dizayn uchun', 'c': False}]},
        {'t': 'Bir sahifada nechta <h1> bo\'lishi kerak?', 'a': [{'t': 'Odatda bitta', 'c': True}, {'t': 'Istalgancha', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Kamida 5 ta', 'c': False}]},
    ]},

    {'n': 'Paragraf va matn teglari', 't': 25, 'o': 4, 'q': [
        {'t': '<p> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Paragraf yaratish uchun', 'c': True}, {'t': 'Sarlavha yaratish uchun', 'c': False}, {'t': 'Havola yaratish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}]},
        {'t': '<br> tegi nima qiladi?', 'a': [{'t': 'Yangi qatorga o\'tkazadi', 'c': True}, {'t': 'Paragraf yaratadi', 'c': False}, {'t': 'Bo\'sh joy qo\'shadi', 'c': False}, {'t': 'Matnni o\'chiradi', 'c': False}]},
        {'t': '<br> tegi yopilishi kerakmi?', 'a': [{'t': 'Yo\'q, o\'z-o\'zidan yopiladigan teg', 'c': True}, {'t': 'Ha, </br> bilan yopiladi', 'c': False}, {'t': 'Ha, <br></br> ko\'rinishida', 'c': False}, {'t': 'Har doim yopilishi kerak', 'c': False}]},
        {'t': '<hr> tegi nima qiladi?', 'a': [{'t': 'Gorizontal chiziq chizadi', 'c': True}, {'t': 'Vertikal chiziq chizadi', 'c': False}, {'t': 'Paragraf yaratadi', 'c': False}, {'t': 'Sarlavha yaratadi', 'c': False}]},
        {'t': '<strong> tegi nima qiladi?', 'a': [{'t': 'Matnni qalin (bold) qiladi', 'c': True}, {'t': 'Matnni qiyshiq qiladi', 'c': False}, {'t': 'Matnni tagiga chiziq chizadi', 'c': False}, {'t': 'Matnni o\'chiradi', 'c': False}]},
        {'t': '<em> tegi nima qiladi?', 'a': [{'t': 'Matnni qiyshiq (italic) qiladi', 'c': True}, {'t': 'Matnni qalin qiladi', 'c': False}, {'t': 'Matnni tagiga chiziq chizadi', 'c': False}, {'t': 'Matnni katta qiladi', 'c': False}]},
        {'t': '<b> va <strong> orasidagi farq?', 'a': [{'t': '<strong> semantik ahamiyatga ega', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<b> yangi standart', 'c': False}, {'t': '<strong> eskirgan', 'c': False}]},
        {'t': '<i> va <em> orasidagi farq?', 'a': [{'t': '<em> semantik ahamiyatga ega', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<i> yangi standart', 'c': False}, {'t': '<em> eskirgan', 'c': False}]},
    ]},

    {'n': 'Matn formatlash teglari', 't': 25, 'o': 5, 'q': [
        {'t': '<u> tegi nima qiladi?', 'a': [{'t': 'Matn tagiga chiziq chizadi', 'c': True}, {'t': 'Matnni qalin qiladi', 'c': False}, {'t': 'Matnni qiyshiq qiladi', 'c': False}, {'t': 'Matnni o\'chiradi', 'c': False}]},
        {'t': '<mark> tegi nima qiladi?', 'a': [{'t': 'Matnni belgilaydi (highlight)', 'c': True}, {'t': 'Matnni o\'chiradi', 'c': False}, {'t': 'Matnni yashiradi', 'c': False}, {'t': 'Matnni kichiklashtiradi', 'c': False}]},
        {'t': '<small> tegi nima qiladi?', 'a': [{'t': 'Matnni kichikroq qiladi', 'c': True}, {'t': 'Matnni kattalashtiradi', 'c': False}, {'t': 'Matnni o\'chiradi', 'c': False}, {'t': 'Matnni yashiradi', 'c': False}]},
        {'t': '<del> tegi nima qiladi?', 'a': [{'t': 'Matn ustidan chiziq chizadi (o\'chirilgan)', 'c': True}, {'t': 'Matnni o\'chiradi', 'c': False}, {'t': 'Matn tagiga chiziq chizadi', 'c': False}, {'t': 'Matnni yashiradi', 'c': False}]},
        {'t': '<ins> tegi nima qiladi?', 'a': [{'t': 'Matn tagiga chiziq chizadi (qo\'shilgan)', 'c': True}, {'t': 'Matnni qo\'shadi', 'c': False}, {'t': 'Matnni o\'chiradi', 'c': False}, {'t': 'Matnni yashiradi', 'c': False}]},
        {'t': '<sub> tegi nima qiladi?', 'a': [{'t': 'Pastki indeks yaratadi (H₂O)', 'c': True}, {'t': 'Yuqori indeks yaratadi', 'c': False}, {'t': 'Matnni kichiklashtiradi', 'c': False}, {'t': 'Matnni pastga tushiradi', 'c': False}]},
        {'t': '<sup> tegi nima qiladi?', 'a': [{'t': 'Yuqori indeks yaratadi (x²)', 'c': True}, {'t': 'Pastki indeks yaratadi', 'c': False}, {'t': 'Matnni kattalashtiradi', 'c': False}, {'t': 'Matnni yuqoriga ko\'taradi', 'c': False}]},
    ]},

    {'n': 'Havolalar (Links)', 't': 25, 'o': 6, 'q': [
        {'t': '<a> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Havola (link) yaratish uchun', 'c': True}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Paragraf yaratish uchun', 'c': False}, {'t': 'Sarlavha yaratish uchun', 'c': False}]},
        {'t': 'href atributi nima uchun?', 'a': [{'t': 'Havola manzilini ko\'rsatish uchun', 'c': True}, {'t': 'Havola matnini yozish uchun', 'c': False}, {'t': 'Havola rangini belgilash uchun', 'c': False}, {'t': 'Havola o\'lchamini belgilash uchun', 'c': False}]},
        {'t': '<a href="https://google.com">Google</a> - bu to\'g\'ri havolami?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Faqat HTTP uchun', 'c': False}, {'t': 'Faqat lokal fayllar uchun', 'c': False}]},
        {'t': 'target="_blank" nima qiladi?', 'a': [{'t': 'Havolani yangi oynada ochadi', 'c': True}, {'t': 'Havolani o\'chiradi', 'c': False}, {'t': 'Havolani yashiradi', 'c': False}, {'t': 'Havolani kattalashtiradi', 'c': False}]},
        {'t': 'Sahifa ichidagi bo\'limga havola qanday yaratiladi?', 'a': [{'t': 'href="#bolim_id" orqali', 'c': True}, {'t': 'href="bolim" orqali', 'c': False}, {'t': 'href="/bolim" orqali', 'c': False}, {'t': 'Yaratib bo\'lmaydi', 'c': False}]},
        {'t': 'Email havolasi qanday yaratiladi?', 'a': [{'t': 'href="mailto:email@example.com"', 'c': True}, {'t': 'href="email:email@example.com"', 'c': False}, {'t': 'href="mail:email@example.com"', 'c': False}, {'t': 'href="@email@example.com"', 'c': False}]},
        {'t': 'Telefon raqamiga havola qanday yaratiladi?', 'a': [{'t': 'href="tel:+998901234567"', 'c': True}, {'t': 'href="phone:+998901234567"', 'c': False}, {'t': 'href="call:+998901234567"', 'c': False}, {'t': 'href="number:+998901234567"', 'c': False}]},
    ]},

    {'n': 'Rasmlar (Images)', 't': 25, 'o': 7, 'q': [
        {'t': '<img> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Rasm qo\'yish uchun', 'c': True}, {'t': 'Havola yaratish uchun', 'c': False}, {'t': 'Matn yozish uchun', 'c': False}, {'t': 'Video qo\'yish uchun', 'c': False}]},
        {'t': 'src atributi nima uchun?', 'a': [{'t': 'Rasm manzilini ko\'rsatish uchun', 'c': True}, {'t': 'Rasm o\'lchamini belgilash uchun', 'c': False}, {'t': 'Rasm nomini yozish uchun', 'c': False}, {'t': 'Rasm rangini belgilash uchun', 'c': False}]},
        {'t': 'alt atributi nima uchun?', 'a': [{'t': 'Rasm yuklanmasa ko\'rinadigan matn', 'c': True}, {'t': 'Rasm o\'lchamini belgilash', 'c': False}, {'t': 'Rasm rangini belgilash', 'c': False}, {'t': 'Rasm nomini yozish', 'c': False}]},
        {'t': '<img> tegi yopilishi kerakmi?', 'a': [{'t': 'Yo\'q, o\'z-o\'zidan yopiladigan teg', 'c': True}, {'t': 'Ha, </img> bilan yopiladi', 'c': False}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}]},
        {'t': 'width va height atributlari nima uchun?', 'a': [{'t': 'Rasm o\'lchamini belgilash uchun', 'c': True}, {'t': 'Rasm manzilini ko\'rsatish uchun', 'c': False}, {'t': 'Rasm rangini belgilash uchun', 'c': False}, {'t': 'Rasm nomini yozish uchun', 'c': False}]},
        {'t': 'Rasmni havola qilish mumkinmi?', 'a': [{'t': 'Ha, <a> ichiga <img> qo\'yish orqali', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat CSS orqali', 'c': False}, {'t': 'Faqat JavaScript orqali', 'c': False}]},
    ]},

    {'n': 'Ro\'yxatlar - Tartibsiz (Unordered Lists)', 't': 20, 'o': 8, 'q': [
        {'t': '<ul> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Tartibsiz ro\'yxat yaratish uchun', 'c': True}, {'t': 'Tartiblangan ro\'yxat yaratish uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Havola yaratish uchun', 'c': False}]},
        {'t': '<li> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Ro\'yxat elementi yaratish uchun', 'c': True}, {'t': 'Havola yaratish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Paragraf yaratish uchun', 'c': False}]},
        {'t': '<ul> ichida qanday teglar bo\'lishi mumkin?', 'a': [{'t': 'Faqat <li> teglari', 'c': True}, {'t': 'Har qanday teglar', 'c': False}, {'t': 'Faqat <p> teglari', 'c': False}, {'t': 'Faqat <a> teglari', 'c': False}]},
        {'t': 'Tartibsiz ro\'yxatda qanday belgilar ko\'rinadi?', 'a': [{'t': 'Nuqta, doira yoki kvadrat', 'c': True}, {'t': 'Raqamlar', 'c': False}, {'t': 'Harflar', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Ichma-ich ro\'yxat yaratish mumkinmi?', 'a': [{'t': 'Ha, <li> ichiga yangi <ul> qo\'yish orqali', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat 2 darajagacha', 'c': False}, {'t': 'Faqat CSS orqali', 'c': False}]},
    ]},

    {'n': 'Ro\'yxatlar - Tartiblangan (Ordered Lists)', 't': 20, 'o': 9, 'q': [
        {'t': '<ol> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Tartiblangan ro\'yxat yaratish uchun', 'c': True}, {'t': 'Tartibsiz ro\'yxat yaratish uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Havola yaratish uchun', 'c': False}]},
        {'t': 'Tartiblangan ro\'yxatda qanday belgilar ko\'rinadi?', 'a': [{'t': 'Raqamlar (1, 2, 3...)', 'c': True}, {'t': 'Nuqtalar', 'c': False}, {'t': 'Yulduzchalar', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'type atributi nima uchun ishlatiladi?', 'a': [{'t': 'Raqamlash turini o\'zgartirish uchun', 'c': True}, {'t': 'Ro\'yxat rangini o\'zgartirish uchun', 'c': False}, {'t': 'Ro\'yxat o\'lchamini belgilash uchun', 'c': False}, {'t': 'Ro\'yxatni yashirish uchun', 'c': False}]},
        {'t': 'type="A" nima beradi?', 'a': [{'t': 'Katta harflar (A, B, C...)', 'c': True}, {'t': 'Kichik harflar', 'c': False}, {'t': 'Rim raqamlari', 'c': False}, {'t': 'Oddiy raqamlar', 'c': False}]},
        {'t': 'start atributi nima qiladi?', 'a': [{'t': 'Boshlanish raqamini belgilaydi', 'c': True}, {'t': 'Ro\'yxatni boshlaydi', 'c': False}, {'t': 'Ro\'yxatni to\'xtatadi', 'c': False}, {'t': 'Ro\'yxatni o\'chiradi', 'c': False}]},
        {'t': '<ol> va <ul> orasidagi asosiy farq?', 'a': [{'t': '<ol> raqamlangan, <ul> belgilangan', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<ul> raqamlangan', 'c': False}, {'t': '<ol> eskirgan', 'c': False}]},
    ]},

    {'n': 'Jadvallar (Tables) - Asoslar', 't': 30, 'o': 10, 'q': [
        {'t': '<table> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Jadval yaratish uchun', 'c': True}, {'t': 'Ro\'yxat yaratish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Havola yaratish uchun', 'c': False}]},
        {'t': '<tr> tegi nima uchun?', 'a': [{'t': 'Jadval qatori (table row)', 'c': True}, {'t': 'Jadval ustuni', 'c': False}, {'t': 'Jadval sarlavhasi', 'c': False}, {'t': 'Jadval katakchasi', 'c': False}]},
        {'t': '<td> tegi nima uchun?', 'a': [{'t': 'Jadval katakchasi (table data)', 'c': True}, {'t': 'Jadval qatori', 'c': False}, {'t': 'Jadval sarlavhasi', 'c': False}, {'t': 'Jadval nomi', 'c': False}]},
        {'t': '<th> tegi nima uchun?', 'a': [{'t': 'Jadval sarlavha katakchasi (table header)', 'c': True}, {'t': 'Oddiy katakcha', 'c': False}, {'t': 'Jadval qatori', 'c': False}, {'t': 'Jadval nomi', 'c': False}]},
        {'t': '<th> va <td> orasidagi farq?', 'a': [{'t': '<th> qalin va markazlashgan', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<td> qalin', 'c': False}, {'t': '<th> eskirgan', 'c': False}]},
        {'t': 'Jadval strukturasi qanday?', 'a': [{'t': '<table> > <tr> > <td>', 'c': True}, {'t': '<table> > <td> > <tr>', 'c': False}, {'t': '<tr> > <table> > <td>', 'c': False}, {'t': '<td> > <tr> > <table>', 'c': False}]},
        {'t': 'border atributi nima qiladi?', 'a': [{'t': 'Jadval chegarasini ko\'rsatadi', 'c': True}, {'t': 'Jadval rangini o\'zgartiradi', 'c': False}, {'t': 'Jadval o\'lchamini belgilaydi', 'c': False}, {'t': 'Jadvalni yashiradi', 'c': False}]},
    ]},

    {'n': 'Jadval atributlari', 't': 25, 'o': 11, 'q': [
        {'t': 'colspan atributi nima qiladi?', 'a': [{'t': 'Katakchan bir necha ustunni egallaydi', 'c': True}, {'t': 'Katakcha bir necha qatorni egallaydi', 'c': False}, {'t': 'Katakcha rangini o\'zgartiradi', 'c': False}, {'t': 'Katakchani yashiradi', 'c': False}]},
        {'t': 'rowspan atributi nima qiladi?', 'a': [{'t': 'Katakcha bir necha qatorni egallaydi', 'c': True}, {'t': 'Katakcha bir necha ustunni egallaydi', 'c': False}, {'t': 'Katakcha o\'lchamini belgilaydi', 'c': False}, {'t': 'Katakchani o\'chiradi', 'c': False}]},
        {'t': '<caption> tegi nima uchun?', 'a': [{'t': 'Jadval sarlavhasini yozish uchun', 'c': True}, {'t': 'Jadval katakchasi uchun', 'c': False}, {'t': 'Jadval qatori uchun', 'c': False}, {'t': 'Jadval chegarasi uchun', 'c': False}]},
        {'t': '<thead> tegi nima uchun?', 'a': [{'t': 'Jadval bosh qismi uchun', 'c': True}, {'t': 'Jadval tanasi uchun', 'c': False}, {'t': 'Jadval oxiri uchun', 'c': False}, {'t': 'Jadval nomi uchun', 'c': False}]},
        {'t': '<tbody> tegi nima uchun?', 'a': [{'t': 'Jadval asosiy qismi uchun', 'c': True}, {'t': 'Jadval boshi uchun', 'c': False}, {'t': 'Jadval oxiri uchun', 'c': False}, {'t': 'Jadval nomi uchun', 'c': False}]},
        {'t': '<tfoot> tegi nima uchun?', 'a': [{'t': 'Jadval oxirgi qismi uchun', 'c': True}, {'t': 'Jadval boshi uchun', 'c': False}, {'t': 'Jadval tanasi uchun', 'c': False}, {'t': 'Jadval nomi uchun', 'c': False}]},
    ]},

    {'n': 'Formalar (Forms) - Asoslar', 't': 30, 'o': 12, 'q': [
        {'t': '<form> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Foydalanuvchidan ma\'lumot olish uchun', 'c': True}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Havola yaratish uchun', 'c': False}]},
        {'t': 'action atributi nima uchun?', 'a': [{'t': 'Ma\'lumot qayerga yuborilishini ko\'rsatadi', 'c': True}, {'t': 'Forma rangini belgilaydi', 'c': False}, {'t': 'Forma o\'lchamini belgilaydi', 'c': False}, {'t': 'Formani yashiradi', 'c': False}]},
        {'t': 'method atributi qanday qiymatlar oladi?', 'a': [{'t': 'GET yoki POST', 'c': True}, {'t': 'SEND yoki RECEIVE', 'c': False}, {'t': 'PUT yoki DELETE', 'c': False}, {'t': 'UPLOAD yoki DOWNLOAD', 'c': False}]},
        {'t': 'GET va POST orasidagi farq?', 'a': [{'t': 'GET URL da, POST yashirin yuboradi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'POST tezroq', 'c': False}, {'t': 'GET xavfsizroq', 'c': False}]},
        {'t': '<input> tegi nima uchun?', 'a': [{'t': 'Foydalanuvchi kiritish maydoni yaratish', 'c': True}, {'t': 'Matn ko\'rsatish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Havola yaratish uchun', 'c': False}]},
        {'t': 'type atributi nima uchun ishlatiladi?', 'a': [{'t': 'Input turini belgilash uchun', 'c': True}, {'t': 'Input rangini belgilash uchun', 'c': False}, {'t': 'Input o\'lchamini belgilash uchun', 'c': False}, {'t': 'Inputni yashirish uchun', 'c': False}]},
        {'t': 'name atributi nima uchun muhim?', 'a': [{'t': 'Ma\'lumotni serverga yuborishda identifikator', 'c': True}, {'t': 'Foydalanuvchiga ko\'rsatish uchun', 'c': False}, {'t': 'Dizayn uchun', 'c': False}, {'t': 'Muhim emas', 'c': False}]},
    ]},

    {'n': 'Input turlari - Matn', 't': 25, 'o': 13, 'q': [
        {'t': 'type="text" nima yaratadi?', 'a': [{'t': 'Oddiy matn kiritish maydoni', 'c': True}, {'t': 'Parol maydoni', 'c': False}, {'t': 'Email maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}]},
        {'t': 'type="password" nima qiladi?', 'a': [{'t': 'Kiritilgan matnni yashiradi', 'c': True}, {'t': 'Parolni tekshiradi', 'c': False}, {'t': 'Parolni saqlaydi', 'c': False}, {'t': 'Parolni yaratadi', 'c': False}]},
        {'t': 'type="email" nima beradi?', 'a': [{'t': 'Email formatini tekshiradi', 'c': True}, {'t': 'Email yuboradi', 'c': False}, {'t': 'Email qabul qiladi', 'c': False}, {'t': 'Oddiy matn maydoni', 'c': False}]},
        {'t': 'placeholder atributi nima qiladi?', 'a': [{'t': 'Maydon bo\'sh bo\'lganda ko\'rsatiladigan matn', 'c': True}, {'t': 'Maydon qiymatini belgilaydi', 'c': False}, {'t': 'Maydon nomini yozadi', 'c': False}, {'t': 'Maydonni to\'ldiradi', 'c': False}]},
        {'t': 'required atributi nima qiladi?', 'a': [{'t': 'Maydonni to\'ldirish majburiy qiladi', 'c': True}, {'t': 'Maydonni yashiradi', 'c': False}, {'t': 'Maydonni o\'chiradi', 'c': False}, {'t': 'Maydonni kattalashtiradi', 'c': False}]},
        {'t': 'maxlength atributi nima uchun?', 'a': [{'t': 'Maksimal belgilar sonini cheklaydi', 'c': True}, {'t': 'Minimal belgilar sonini belgilaydi', 'c': False}, {'t': 'Maydon kengligini belgilaydi', 'c': False}, {'t': 'Maydon balandligini belgilaydi', 'c': False}]},
    ]},

    {'n': 'Input turlari - Raqam va sana', 't': 25, 'o': 14, 'q': [
        {'t': 'type="number" nima qiladi?', 'a': [{'t': 'Faqat raqam kiritish imkonini beradi', 'c': True}, {'t': 'Raqamni hisoblaydi', 'c': False}, {'t': 'Raqamni ko\'rsatadi', 'c': False}, {'t': 'Raqamni saqlaydi', 'c': False}]},
        {'t': 'min va max atributlari nima uchun?', 'a': [{'t': 'Raqam oralig\'ini cheklash uchun', 'c': True}, {'t': 'Maydon o\'lchamini belgilash uchun', 'c': False}, {'t': 'Matn uzunligini cheklash uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'type="date" nima yaratadi?', 'a': [{'t': 'Sana tanlash maydoni', 'c': True}, {'t': 'Vaqt tanlash maydoni', 'c': False}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}]},
        {'t': 'type="time" nima yaratadi?', 'a': [{'t': 'Vaqt tanlash maydoni', 'c': True}, {'t': 'Sana tanlash maydoni', 'c': False}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}]},
        {'t': 'type="datetime-local" nima yaratadi?', 'a': [{'t': 'Sana va vaqt tanlash maydoni', 'c': True}, {'t': 'Faqat sana', 'c': False}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Matn maydoni', 'c': False}]},
        {'t': 'type="range" nima yaratadi?', 'a': [{'t': 'Slayder (range slider)', 'c': True}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}, {'t': 'Sana maydoni', 'c': False}]},
    ]},

    {'n': 'Input turlari - Tanlash', 't': 25, 'o': 15, 'q': [
        {'t': 'type="checkbox" nima yaratadi?', 'a': [{'t': 'Bir nechta tanlov uchun katakcha', 'c': True}, {'t': 'Bitta tanlov uchun tugma', 'c': False}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}]},
        {'t': 'type="radio" nima yaratadi?', 'a': [{'t': 'Bitta tanlov uchun tugma', 'c': True}, {'t': 'Bir nechta tanlov uchun', 'c': False}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}]},
        {'t': 'Radio tugmalarni guruhlash uchun nima kerak?', 'a': [{'t': 'Bir xil name atributi', 'c': True}, {'t': 'Bir xil id atributi', 'c': False}, {'t': 'Bir xil class atributi', 'c': False}, {'t': 'Hech narsa kerak emas', 'c': False}]},
        {'t': 'checked atributi nima qiladi?', 'a': [{'t': 'Standart tanlangan qiladi', 'c': True}, {'t': 'Tekshiradi', 'c': False}, {'t': 'Yashiradi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
        {'t': 'type="file" nima yaratadi?', 'a': [{'t': 'Fayl yuklash maydoni', 'c': True}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}, {'t': 'Sana maydoni', 'c': False}]},
        {'t': 'type="color" nima yaratadi?', 'a': [{'t': 'Rang tanlash maydoni', 'c': True}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}, {'t': 'Sana maydoni', 'c': False}]},
    ]},

    {'n': 'Forma elementlari - Select va Textarea', 't': 25, 'o': 16, 'q': [
        {'t': '<select> tegi nima yaratadi?', 'a': [{'t': 'Ochiladigan ro\'yxat (dropdown)', 'c': True}, {'t': 'Matn maydoni', 'c': False}, {'t': 'Tugma', 'c': False}, {'t': 'Checkbox', 'c': False}]},
        {'t': '<option> tegi nima uchun?', 'a': [{'t': 'Select ichidagi tanlov variantlari', 'c': True}, {'t': 'Matn yozish uchun', 'c': False}, {'t': 'Tugma yaratish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}]},
        {'t': 'selected atributi nima qiladi?', 'a': [{'t': 'Standart tanlangan qiladi', 'c': True}, {'t': 'Tanlovni o\'chiradi', 'c': False}, {'t': 'Tanlovni yashiradi', 'c': False}, {'t': 'Tanlovni kattalashtiradi', 'c': False}]},
        {'t': '<textarea> tegi nima yaratadi?', 'a': [{'t': 'Ko\'p qatorli matn maydoni', 'c': True}, {'t': 'Bir qatorli matn maydoni', 'c': False}, {'t': 'Raqam maydoni', 'c': False}, {'t': 'Sana maydoni', 'c': False}]},
        {'t': 'rows va cols atributlari nima uchun?', 'a': [{'t': 'Textarea o\'lchamini belgilash', 'c': True}, {'t': 'Matn rangini belgilash', 'c': False}, {'t': 'Matn shriftini belgilash', 'c': False}, {'t': 'Matnni yashirish', 'c': False}]},
        {'t': '<optgroup> tegi nima uchun?', 'a': [{'t': 'Option larni guruhlash uchun', 'c': True}, {'t': 'Yangi select yaratish uchun', 'c': False}, {'t': 'Tugma yaratish uchun', 'c': False}, {'t': 'Matn yozish uchun', 'c': False}]},
    ]},

    {'n': 'Forma tugmalari', 't': 20, 'o': 17, 'q': [
        {'t': 'type="submit" nima qiladi?', 'a': [{'t': 'Formani yuboradi', 'c': True}, {'t': 'Formani tozalaydi', 'c': False}, {'t': 'Formani yopadi', 'c': False}, {'t': 'Formani ochadi', 'c': False}]},
        {'t': 'type="reset" nima qiladi?', 'a': [{'t': 'Forma maydonlarini tozalaydi', 'c': True}, {'t': 'Formani yuboradi', 'c': False}, {'t': 'Formani yopadi', 'c': False}, {'t': 'Formani saqlaydi', 'c': False}]},
        {'t': 'type="button" nima yaratadi?', 'a': [{'t': 'Oddiy tugma (JavaScript uchun)', 'c': True}, {'t': 'Submit tugma', 'c': False}, {'t': 'Reset tugma', 'c': False}, {'t': 'Havola', 'c': False}]},
        {'t': '<button> va <input type="button"> orasidagi farq?', 'a': [{'t': '<button> ichiga HTML qo\'yish mumkin', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<input> yangi standart', 'c': False}, {'t': '<button> eskirgan', 'c': False}]},
        {'t': 'value atributi tugmada nima qiladi?', 'a': [{'t': 'Tugma matnini belgilaydi', 'c': True}, {'t': 'Tugma rangini belgilaydi', 'c': False}, {'t': 'Tugma o\'lchamini belgilaydi', 'c': False}, {'t': 'Tugmani yashiradi', 'c': False}]},
    ]},

    {'n': 'Label va Fieldset', 't': 20, 'o': 18, 'q': [
        {'t': '<label> tegi nima uchun ishlatiladi?', 'a': [{'t': 'Input maydoniga yorliq qo\'yish', 'c': True}, {'t': 'Tugma yaratish', 'c': False}, {'t': 'Matn yozish', 'c': False}, {'t': 'Rasm qo\'yish', 'c': False}]},
        {'t': 'for atributi nima uchun?', 'a': [{'t': 'Qaysi input bilan bog\'lanishini ko\'rsatadi', 'c': True}, {'t': 'Label rangini belgilaydi', 'c': False}, {'t': 'Label o\'lchamini belgilaydi', 'c': False}, {'t': 'Labelni yashiradi', 'c': False}]},
        {'t': 'Label dan foyda nima?', 'a': [{'t': 'Labelni bosish input ni faollashtiradi', 'c': True}, {'t': 'Faqat dizayn uchun', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat matn ko\'rsatish', 'c': False}]},
        {'t': '<fieldset> tegi nima uchun?', 'a': [{'t': 'Forma elementlarini guruhlash', 'c': True}, {'t': 'Yangi forma yaratish', 'c': False}, {'t': 'Tugma yaratish', 'c': False}, {'t': 'Matn yozish', 'c': False}]},
        {'t': '<legend> tegi nima uchun?', 'a': [{'t': 'Fieldset sarlavhasi', 'c': True}, {'t': 'Forma sarlavhasi', 'c': False}, {'t': 'Sahifa sarlavhasi', 'c': False}, {'t': 'Input sarlavhasi', 'c': False}]},
    ]},

    {'n': 'Semantik teglar - Header, Nav, Main', 't': 25, 'o': 19, 'q': [
        {'t': 'Semantik teglar nima?', 'a': [{'t': 'Ma\'noga ega, maqsadini bildiruvchi teglar', 'c': True}, {'t': 'Oddiy teglar', 'c': False}, {'t': 'Eskirgan teglar', 'c': False}, {'t': 'Yangi teglar', 'c': False}]},
        {'t': '<header> tegi nima uchun?', 'a': [{'t': 'Sahifa yoki bo\'lim bosh qismi', 'c': True}, {'t': 'Faqat sahifa yuqori qismi', 'c': False}, {'t': 'Sarlavha yaratish', 'c': False}, {'t': 'Havola yaratish', 'c': False}]},
        {'t': '<nav> tegi nima uchun?', 'a': [{'t': 'Navigatsiya havolalari uchun', 'c': True}, {'t': 'Barcha havolalar uchun', 'c': False}, {'t': 'Faqat menyu uchun', 'c': False}, {'t': 'Rasm uchun', 'c': False}]},
        {'t': '<main> tegi nima uchun?', 'a': [{'t': 'Sahifaning asosiy kontenti', 'c': True}, {'t': 'Sahifa boshi', 'c': False}, {'t': 'Sahifa oxiri', 'c': False}, {'t': 'Yon panel', 'c': False}]},
        {'t': 'Bir sahifada nechta <main> bo\'lishi kerak?', 'a': [{'t': 'Faqat bitta', 'c': True}, {'t': 'Istalgancha', 'c': False}, {'t': 'Kamida ikkita', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'Semantik teglarning afzalligi nima?', 'a': [{'t': 'SEO va accessibility uchun yaxshi', 'c': True}, {'t': 'Faqat dizayn uchun', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},

    {'n': 'Semantik teglar - Section, Article, Aside', 't': 25, 'o': 20, 'q': [
        {'t': '<section> tegi nima uchun?', 'a': [{'t': 'Tematik guruh yoki bo\'lim', 'c': True}, {'t': 'Faqat dizayn uchun', 'c': False}, {'t': 'Paragraf yaratish', 'c': False}, {'t': 'Havola yaratish', 'c': False}]},
        {'t': '<article> tegi nima uchun?', 'a': [{'t': 'Mustaqil, qayta ishlatish mumkin kontent', 'c': True}, {'t': 'Faqat maqolalar uchun', 'c': False}, {'t': 'Faqat yangiliklar uchun', 'c': False}, {'t': 'Paragraf yaratish', 'c': False}]},
        {'t': '<aside> tegi nima uchun?', 'a': [{'t': 'Yon panel yoki qo\'shimcha ma\'lumot', 'c': True}, {'t': 'Asosiy kontent', 'c': False}, {'t': 'Sahifa boshi', 'c': False}, {'t': 'Sahifa oxiri', 'c': False}]},
        {'t': '<section> va <article> orasidagi farq?', 'a': [{'t': '<article> mustaqil, <section> guruh', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<section> eskirgan', 'c': False}, {'t': '<article> faqat maqolalar uchun', 'c': False}]},
        {'t': '<div> va <section> orasidagi farq?', 'a': [{'t': '<section> semantik ma\'noga ega', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '<div> yangi standart', 'c': False}, {'t': '<section> eskirgan', 'c': False}]},
    ]},

    {'n': 'Semantik teglar - Footer va Figure', 't': 20, 'o': 21, 'q': [
        {'t': '<footer> tegi nima uchun?', 'a': [{'t': 'Sahifa yoki bo\'lim oxiri', 'c': True}, {'t': 'Faqat sahifa pastki qismi', 'c': False}, {'t': 'Havola yaratish', 'c': False}, {'t': 'Paragraf yaratish', 'c': False}]},
        {'t': '<figure> tegi nima uchun?', 'a': [{'t': 'Rasm, diagramma kabi kontent uchun', 'c': True}, {'t': 'Faqat rasm uchun', 'c': False}, {'t': 'Faqat video uchun', 'c': False}, {'t': 'Matn uchun', 'c': False}]},
        {'t': '<figcaption> tegi nima uchun?', 'a': [{'t': 'Figure uchun izoh yoki sarlavha', 'c': True}, {'t': 'Rasm manzili', 'c': False}, {'t': 'Rasm o\'lchami', 'c': False}, {'t': 'Rasm nomi', 'c': False}]},
        {'t': '<figure> ichida nima bo\'lishi mumkin?', 'a': [{'t': 'Rasm, video, kod, diagramma', 'c': True}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Bir sahifada nechta <footer> bo\'lishi mumkin?', 'a': [{'t': 'Bir nechta (har bir section uchun)', 'c': True}, {'t': 'Faqat bitta', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Faqat ikkita', 'c': False}]},
    ]},

    {'n': 'Audio va Video', 't': 25, 'o': 22, 'q': [
        {'t': '<audio> tegi nima uchun?', 'a': [{'t': 'Audio fayl qo\'yish uchun', 'c': True}, {'t': 'Video qo\'yish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Matn yozish uchun', 'c': False}]},
        {'t': '<video> tegi nima uchun?', 'a': [{'t': 'Video fayl qo\'yish uchun', 'c': True}, {'t': 'Audio qo\'yish uchun', 'c': False}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Matn yozish uchun', 'c': False}]},
        {'t': 'controls atributi nima qiladi?', 'a': [{'t': 'Ijro tugmalarini ko\'rsatadi', 'c': True}, {'t': 'Videoni boshqaradi', 'c': False}, {'t': 'Videoni to\'xtatadi', 'c': False}, {'t': 'Videoni o\'chiradi', 'c': False}]},
        {'t': 'autoplay atributi nima qiladi?', 'a': [{'t': 'Avtomatik ijro boshlaydi', 'c': True}, {'t': 'Videoni to\'xtatadi', 'c': False}, {'t': 'Videoni takrorlaydi', 'c': False}, {'t': 'Videoni o\'chiradi', 'c': False}]},
        {'t': 'loop atributi nima qiladi?', 'a': [{'t': 'Videoni takrorlab ijro qiladi', 'c': True}, {'t': 'Videoni bir marta ijro qiladi', 'c': False}, {'t': 'Videoni to\'xtatadi', 'c': False}, {'t': 'Videoni o\'chiradi', 'c': False}]},
        {'t': 'muted atributi nima qiladi?', 'a': [{'t': 'Ovozni o\'chiradi', 'c': True}, {'t': 'Ovozni kuchaytiradi', 'c': False}, {'t': 'Videoni to\'xtatadi', 'c': False}, {'t': 'Videoni yashiradi', 'c': False}]},
        {'t': '<source> tegi nima uchun?', 'a': [{'t': 'Turli formatdagi fayllar uchun', 'c': True}, {'t': 'Faqat bitta format uchun', 'c': False}, {'t': 'Matn uchun', 'c': False}, {'t': 'Rasm uchun', 'c': False}]},
    ]},

    {'n': 'Iframe', 't': 20, 'o': 23, 'q': [
        {'t': '<iframe> tegi nima uchun?', 'a': [{'t': 'Boshqa sahifani ichiga joylashtirish', 'c': True}, {'t': 'Rasm qo\'yish uchun', 'c': False}, {'t': 'Video qo\'yish uchun', 'c': False}, {'t': 'Matn yozish uchun', 'c': False}]},
        {'t': 'src atributi iframe da nima uchun?', 'a': [{'t': 'Joylashtiriladigan sahifa manzili', 'c': True}, {'t': 'Iframe o\'lchami', 'c': False}, {'t': 'Iframe rangi', 'c': False}, {'t': 'Iframe nomi', 'c': False}]},
        {'t': 'width va height atributlari nima uchun?', 'a': [{'t': 'Iframe o\'lchamini belgilash', 'c': True}, {'t': 'Iframe rangini belgilash', 'c': False}, {'t': 'Iframe manzilini ko\'rsatish', 'c': False}, {'t': 'Iframe nomini yozish', 'c': False}]},
        {'t': 'YouTube videoni qanday joylashtirish mumkin?', 'a': [{'t': 'iframe orqali embed kodi bilan', 'c': True}, {'t': 'Faqat <video> tegi bilan', 'c': False}, {'t': 'Faqat <audio> tegi bilan', 'c': False}, {'t': 'Joylashtirish mumkin emas', 'c': False}]},
        {'t': 'frameborder atributi nima qiladi?', 'a': [{'t': 'Iframe chegarasini ko\'rsatadi/yashiradi', 'c': True}, {'t': 'Iframe o\'lchamini belgilaydi', 'c': False}, {'t': 'Iframe rangini o\'zgartiradi', 'c': False}, {'t': 'Iframe manzilini ko\'rsatadi', 'c': False}]},
    ]},

    {'n': 'Meta teglar', 't': 25, 'o': 24, 'q': [
        {'t': '<meta> tegi nima uchun?', 'a': [{'t': 'Sahifa haqida meta ma\'lumotlar', 'c': True}, {'t': 'Sahifa kontenti', 'c': False}, {'t': 'Rasm qo\'yish', 'c': False}, {'t': 'Havola yaratish', 'c': False}]},
        {'t': 'charset atributi nima uchun?', 'a': [{'t': 'Belgilar kodlashini belgilash', 'c': True}, {'t': 'Sahifa tilini belgilash', 'c': False}, {'t': 'Sahifa rangini belgilash', 'c': False}, {'t': 'Sahifa o\'lchamini belgilash', 'c': False}]},
        {'t': 'UTF-8 nima?', 'a': [{'t': 'Universal belgilar kodlash formati', 'c': True}, {'t': 'Sahifa tili', 'c': False}, {'t': 'Sahifa rangi', 'c': False}, {'t': 'Sahifa o\'lchami', 'c': False}]},
        {'t': 'viewport meta tegi nima uchun?', 'a': [{'t': 'Mobil qurilmalarda ko\'rinish sozlash', 'c': True}, {'t': 'Sahifa rangini belgilash', 'c': False}, {'t': 'Sahifa tilini belgilash', 'c': False}, {'t': 'Sahifa o\'lchamini belgilash', 'c': False}]},
        {'t': 'description meta tegi nima uchun?', 'a': [{'t': 'Sahifa tavsifi (SEO uchun)', 'c': True}, {'t': 'Sahifa sarlavhasi', 'c': False}, {'t': 'Sahifa kontenti', 'c': False}, {'t': 'Sahifa rangi', 'c': False}]},
        {'t': 'keywords meta tegi nima uchun?', 'a': [{'t': 'Sahifa kalit so\'zlari (SEO uchun)', 'c': True}, {'t': 'Sahifa sarlavhasi', 'c': False}, {'t': 'Sahifa kontenti', 'c': False}, {'t': 'Sahifa rangi', 'c': False}]},
    ]},

    {'n': 'Link va Script teglari', 't': 20, 'o': 25, 'q': [
        {'t': '<link> tegi nima uchun?', 'a': [{'t': 'Tashqi fayllarni ulash (CSS, favicon)', 'c': True}, {'t': 'Havola yaratish', 'c': False}, {'t': 'Rasm qo\'yish', 'c': False}, {'t': 'Matn yozish', 'c': False}]},
        {'t': 'CSS faylni qanday ulash mumkin?', 'a': [{'t': '<link rel="stylesheet" href="style.css">', 'c': True}, {'t': '<css src="style.css">', 'c': False}, {'t': '<style src="style.css">', 'c': False}, {'t': '<import href="style.css">', 'c': False}]},
        {'t': '<script> tegi nima uchun?', 'a': [{'t': 'JavaScript kodi yozish yoki ulash', 'c': True}, {'t': 'CSS yozish', 'c': False}, {'t': 'HTML yozish', 'c': False}, {'t': 'Rasm qo\'yish', 'c': False}]},
        {'t': 'JavaScript faylni qanday ulash mumkin?', 'a': [{'t': '<script src="script.js"></script>', 'c': True}, {'t': '<js src="script.js">', 'c': False}, {'t': '<javascript src="script.js">', 'c': False}, {'t': '<code src="script.js">', 'c': False}]},
        {'t': '<script> tegini qayerga joylashtirish yaxshi?', 'a': [{'t': '</body> dan oldin', 'c': True}, {'t': '<head> ichida', 'c': False}, {'t': '<body> boshida', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
    ]},

    {'n': 'HTML atributlari - id va class', 't': 25, 'o': 26, 'q': [
        {'t': 'id atributi nima uchun?', 'a': [{'t': 'Elementga noyob identifikator berish', 'c': True}, {'t': 'Element rangini belgilash', 'c': False}, {'t': 'Element o\'lchamini belgilash', 'c': False}, {'t': 'Element nomini yozish', 'c': False}]},
        {'t': 'Bir sahifada bir xil id bo\'lishi mumkinmi?', 'a': [{'t': 'Yo\'q, id noyob bo\'lishi kerak', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Istalgancha', 'c': False}]},
        {'t': 'class atributi nima uchun?', 'a': [{'t': 'Elementlarni guruhlash va CSS qo\'llash', 'c': True}, {'t': 'Element rangini belgilash', 'c': False}, {'t': 'Element o\'lchamini belgilash', 'c': False}, {'t': 'Element nomini yozish', 'c': False}]},
        {'t': 'Bir elementda bir nechta class bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, bo\'sh joy bilan ajratiladi', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'id va class orasidagi asosiy farq?', 'a': [{'t': 'id noyob, class takrorlanishi mumkin', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'class noyob', 'c': False}, {'t': 'id eskirgan', 'c': False}]},
        {'t': 'CSS da id qanday tanlanadi?', 'a': [{'t': '#id_nomi', 'c': True}, {'t': '.id_nomi', 'c': False}, {'t': 'id_nomi', 'c': False}, {'t': '@id_nomi', 'c': False}]},
        {'t': 'CSS da class qanday tanlanadi?', 'a': [{'t': '.class_nomi', 'c': True}, {'t': '#class_nomi', 'c': False}, {'t': 'class_nomi', 'c': False}, {'t': '@class_nomi', 'c': False}]},
    ]},

    {'n': 'HTML atributlari - style va title', 't': 20, 'o': 27, 'q': [
        {'t': 'style atributi nima uchun?', 'a': [{'t': 'Inline CSS yozish uchun', 'c': True}, {'t': 'Element nomini yozish', 'c': False}, {'t': 'Element o\'lchamini belgilash', 'c': False}, {'t': 'Element manzilini ko\'rsatish', 'c': False}]},
        {'t': 'style="color: red;" nima qiladi?', 'a': [{'t': 'Matn rangini qizil qiladi', 'c': True}, {'t': 'Fon rangini qizil qiladi', 'c': False}, {'t': 'Chegara rangini qizil qiladi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'title atributi nima uchun?', 'a': [{'t': 'Element ustiga kelganda ko\'rinadigan matn', 'c': True}, {'t': 'Element sarlavhasi', 'c': False}, {'t': 'Element nomi', 'c': False}, {'t': 'Element rangi', 'c': False}]},
        {'t': 'Inline CSS yaxshi amaliyotmi?', 'a': [{'t': 'Yo\'q, tashqi CSS fayllar yaxshiroq', 'c': True}, {'t': 'Ha, eng yaxshi usul', 'c': False}, {'t': 'Har doim ishlatish kerak', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'title atributi qaysi elementlarda ishlatiladi?', 'a': [{'t': 'Deyarli barcha elementlarda', 'c': True}, {'t': 'Faqat <a> da', 'c': False}, {'t': 'Faqat <img> da', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},

    {'n': 'HTML atributlari - data va aria', 't': 25, 'o': 28, 'q': [
        {'t': 'data-* atributlari nima uchun?', 'a': [{'t': 'Maxsus ma\'lumotlarni saqlash uchun', 'c': True}, {'t': 'Element rangini belgilash', 'c': False}, {'t': 'Element o\'lchamini belgilash', 'c': False}, {'t': 'Element nomini yozish', 'c': False}]},
        {'t': 'data-id="123" qanday ishlatiladi?', 'a': [{'t': 'JavaScript orqali o\'qiladi', 'c': True}, {'t': 'CSS orqali o\'qiladi', 'c': False}, {'t': 'Avtomatik ishlaydi', 'c': False}, {'t': 'Ishlatilmaydi', 'c': False}]},
        {'t': 'aria-* atributlari nima uchun?', 'a': [{'t': 'Accessibility (kirish imkoniyati) uchun', 'c': True}, {'t': 'Dizayn uchun', 'c': False}, {'t': 'SEO uchun', 'c': False}, {'t': 'Animatsiya uchun', 'c': False}]},
        {'t': 'aria-label nima qiladi?', 'a': [{'t': 'Ekran o\'quvchilar uchun yorliq beradi', 'c': True}, {'t': 'Element nomini yozadi', 'c': False}, {'t': 'Element rangini belgilaydi', 'c': False}, {'t': 'Element o\'lchamini belgilaydi', 'c': False}]},
        {'t': 'Accessibility nima?', 'a': [{'t': 'Nogironlar uchun kirish imkoniyati', 'c': True}, {'t': 'Sahifa tezligi', 'c': False}, {'t': 'Sahifa dizayni', 'c': False}, {'t': 'Sahifa xavfsizligi', 'c': False}]},
    ]},

    {'n': 'HTML5 yangi xususiyatlari', 't': 25, 'o': 29, 'q': [
        {'t': 'HTML5 nima?', 'a': [{'t': 'HTML ning eng yangi versiyasi', 'c': True}, {'t': 'Yangi dasturlash tili', 'c': False}, {'t': 'CSS versiyasi', 'c': False}, {'t': 'JavaScript versiyasi', 'c': False}]},
        {'t': 'HTML5 da qanday yangi teglar qo\'shilgan?', 'a': [{'t': 'Semantik teglar, audio, video, canvas', 'c': True}, {'t': 'Faqat <div> va <span>', 'c': False}, {'t': 'Hech qanday yangi teg yo\'q', 'c': False}, {'t': 'Faqat <table>', 'c': False}]},
        {'t': '<canvas> tegi nima uchun?', 'a': [{'t': 'JavaScript orqali grafika chizish', 'c': True}, {'t': 'Rasm qo\'yish', 'c': False}, {'t': 'Video qo\'yish', 'c': False}, {'t': 'Matn yozish', 'c': False}]},
        {'t': 'HTML5 da qanday yangi input turlari bor?', 'a': [{'t': 'email, date, number, range, color', 'c': True}, {'t': 'Faqat text va password', 'c': False}, {'t': 'Hech qanday yangi tur yo\'q', 'c': False}, {'t': 'Faqat checkbox', 'c': False}]},
        {'t': 'localStorage nima?', 'a': [{'t': 'Brauzerda ma\'lumot saqlash', 'c': True}, {'t': 'Serverda ma\'lumot saqlash', 'c': False}, {'t': 'Fayl saqlash', 'c': False}, {'t': 'Rasm saqlash', 'c': False}]},
        {'t': 'HTML5 da Flash kerakmi?', 'a': [{'t': 'Yo\'q, audio/video teglar bor', 'c': True}, {'t': 'Ha, har doim kerak', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Flash nima?', 'c': False}]},
    ]},

    {'n': 'HTML eng yaxshi amaliyotlar', 't': 30, 'o': 30, 'q': [
        {'t': 'HTML kodini qanday yozish kerak?', 'a': [{'t': 'Toza, o\'qilishi oson, indentatsiya bilan', 'c': True}, {'t': 'Bir qatorda', 'c': False}, {'t': 'Tasodifiy', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'Teglarni yopish kerakmi?', 'a': [{'t': 'Ha, barcha juft teglarni yopish kerak', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zilarini', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Alt atributini rasmga qo\'yish kerakmi?', 'a': [{'t': 'Ha, accessibility va SEO uchun', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Semantik teglarni ishlatish kerakmi?', 'a': [{'t': 'Ha, SEO va accessibility uchun', 'c': True}, {'t': 'Yo\'q, faqat <div> ishlatish kerak', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'HTML validatsiya nima?', 'a': [{'t': 'Kodning to\'g\'riligini tekshirish', 'c': True}, {'t': 'Dizaynni tekshirish', 'c': False}, {'t': 'Tezlikni tekshirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Inline CSS ishlatish yaxshimi?', 'a': [{'t': 'Yo\'q, tashqi CSS fayllar yaxshiroq', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Hech qachon CSS ishlatmaslik kerak', 'c': False}]},
        {'t': 'HTML kommentariya qanday yoziladi?', 'a': [{'t': '<!-- kommentariya -->', 'c': True}, {'t': '// kommentariya', 'c': False}, {'t': '/* kommentariya */', 'c': False}, {'t': '# kommentariya', 'c': False}]},
        {'t': 'Mobil uchun viewport meta tegi kerakmi?', 'a': [{'t': 'Ha, responsive dizayn uchun', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Faqat desktop uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'DOCTYPE e\'lon qilish kerakmi?', 'a': [{'t': 'Ha, har doim kerak', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'HTML faylni qanday nomlash kerak?', 'a': [{'t': 'Kichik harf, tire bilan: index.html', 'c': True}, {'t': 'Katta harf bilan', 'c': False}, {'t': 'Bo\'sh joy bilan', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("🚀 HTML mavzularini qo'shish boshlandi...")
    subject = get_or_create_html()
    add_topics(subject, T)
    print(f"\n✅ Jami {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
    print(f"📊 Jami testlar soni: {sum(len(t['q']) for t in T)}")
