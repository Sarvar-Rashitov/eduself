"""
INFORMATIKA - 100 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_informatics():
    cat, _ = SubjectCategory.objects.get_or_create(slug='aniq-fanlar', defaults={'name': 'Aniq fanlar', 'icon': 'bi-calculator', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Informatika', defaults={'category': cat, 'description': 'Informatika fani - asoslardan murakkabgacha', 'icon': 'bi-laptop', 'order': 4, 'is_active': True})
    return subj

def add_topics(subject, topics_data):
    for td in topics_data:
        topic, created = Topic.objects.get_or_create(subject=subject, name=td['n'], defaults={'time_limit': td['t'], 'passing_score': 60, 'order': td['o'], 'is_active': True})
        print(f"{'✅' if created else 'ℹ️'} §{td['o']}: {td['n']} ({len(td['q'])} test)")
        for i, qd in enumerate(td['q']):
            q, qc = Question.objects.get_or_create(topic=topic, text=qd['t'], defaults={'points': 10, 'order': i + 1})
            if qc:
                for ad in qd['a']:
                    Answer.objects.create(question=q, text=ad['t'], is_correct=ad['c'])

# 100 TA MAVZU (5-11 sinf materiallari, ketma-ket)
T = [
    # ASOSLAR (1-15)
    {'n': 'Informatika faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Informatika fani nimani o\'rganadi?', 'a': [{'t': 'Axborot va uni qayta ishlashni', 'c': True}, {'t': 'Faqat kompyuterni', 'c': False}, {'t': 'Faqat internetni', 'c': False}, {'t': 'Faqat dasturlashni', 'c': False}]},
        {'t': 'Axborot nima?', 'a': [{'t': 'Ma\'lumot, xabar, bilim', 'c': True}, {'t': 'Faqat raqamlar', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
        {'t': 'Informatika qayerda qo\'llaniladi?', 'a': [{'t': 'Barcha sohalarda', 'c': True}, {'t': 'Faqat maktabda', 'c': False}, {'t': 'Faqat ofisda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Kompyuter nima?', 'a': [{'t': 'Axborotni qayta ishlovchi elektron qurilma', 'c': True}, {'t': 'Faqat o\'yin o\'ynaydigan qurilma', 'c': False}, {'t': 'Faqat hisoblash mashinasi', 'c': False}, {'t': 'Faqat matn yozish uchun', 'c': False}]},
        {'t': 'Informatikaning asosiy yo\'nalishlari?', 'a': [{'t': 'Dasturlash, tarmoqlar, ma\'lumotlar bazasi, sun\'iy intellekt', 'c': True}, {'t': 'Faqat dasturlash', 'c': False}, {'t': 'Faqat o\'yinlar', 'c': False}, {'t': 'Hech qanday yo\'nalish yo\'q', 'c': False}]},
    ]},
    {'n': 'Kompyuter tarixi', 't': 20, 'o': 2, 'q': [
        {'t': 'Birinchi mexanik hisoblash mashinasini kim yaratgan?', 'a': [{'t': 'Bleyz Paskal', 'c': True}, {'t': 'Bill Geyts', 'c': False}, {'t': 'Stiv Jobs', 'c': False}, {'t': 'Mark Tsukerberg', 'c': False}]},
        {'t': 'Birinchi elektron kompyuter?', 'a': [{'t': 'ENIAC', 'c': True}, {'t': 'IBM PC', 'c': False}, {'t': 'Macintosh', 'c': False}, {'t': 'iPhone', 'c': False}]},
        {'t': 'Kompyuter avlodlari nechta?', 'a': [{'t': '5 ta', 'c': True}, {'t': '3 ta', 'c': False}, {'t': '10 ta', 'c': False}, {'t': '2 ta', 'c': False}]},
        {'t': 'Birinchi avlod kompyuterlarda nima ishlatilgan?', 'a': [{'t': 'Elektron lampalar', 'c': True}, {'t': 'Tranzistorlar', 'c': False}, {'t': 'Mikrochiplar', 'c': False}, {'t': 'Kvant protsessorlari', 'c': False}]},
        {'t': 'Shaxsiy kompyuter (PC) qachon paydo bo\'lgan?', 'a': [{'t': '1970-1980 yillarda', 'c': True}, {'t': '1950 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}, {'t': '1900 yilda', 'c': False}]},
        {'t': 'IBM PC qachon chiqarilgan?', 'a': [{'t': '1981 yilda', 'c': True}, {'t': '1990 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}, {'t': '1970 yilda', 'c': False}]},
    ]},
    {'n': 'Kompyuter tuzilishi', 't': 20, 'o': 3, 'q': [
        {'t': 'Kompyuterning asosiy qismlari?', 'a': [{'t': 'Protsessor, xotira, kiritish/chiqarish qurilmalari', 'c': True}, {'t': 'Faqat monitor', 'c': False}, {'t': 'Faqat klaviatura', 'c': False}, {'t': 'Faqat sichqoncha', 'c': False}]},
        {'t': 'Protsessor nima?', 'a': [{'t': 'Kompyuterning miyasi, hisoblash qiladi', 'c': True}, {'t': 'Xotira qurilmasi', 'c': False}, {'t': 'Kiritish qurilmasi', 'c': False}, {'t': 'Chiqarish qurilmasi', 'c': False}]},
        {'t': 'Operativ xotira (RAM) nima?', 'a': [{'t': 'Vaqtinchalik ma\'lumot saqlash joyi', 'c': True}, {'t': 'Doimiy xotira', 'c': False}, {'t': 'Protsessor', 'c': False}, {'t': 'Monitor', 'c': False}]},
        {'t': 'Qattiq disk (HDD) nima?', 'a': [{'t': 'Doimiy ma\'lumot saqlash qurilmasi', 'c': True}, {'t': 'Vaqtinchalik xotira', 'c': False}, {'t': 'Protsessor', 'c': False}, {'t': 'Kiritish qurilmasi', 'c': False}]},
        {'t': 'Kiritish qurilmalari qaysilar?', 'a': [{'t': 'Klaviatura, sichqoncha, mikrofon, kamera', 'c': True}, {'t': 'Faqat monitor', 'c': False}, {'t': 'Faqat printer', 'c': False}, {'t': 'Faqat dinamik', 'c': False}]},
        {'t': 'Chiqarish qurilmalari qaysilar?', 'a': [{'t': 'Monitor, printer, dinamik', 'c': True}, {'t': 'Faqat klaviatura', 'c': False}, {'t': 'Faqat sichqoncha', 'c': False}, {'t': 'Faqat mikrofon', 'c': False}]},
        {'t': 'Materik plata (motherboard) nima?', 'a': [{'t': 'Barcha qismlarni birlashtiruvchi asosiy plata', 'c': True}, {'t': 'Faqat protsessor', 'c': False}, {'t': 'Faqat xotira', 'c': False}, {'t': 'Faqat qattiq disk', 'c': False}]},
    ]},
    {'n': 'Operatsion tizimlar', 't': 20, 'o': 4, 'q': [
        {'t': 'Operatsion tizim nima?', 'a': [{'t': 'Kompyuter resurslarini boshqaruvchi dastur', 'c': True}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat matn muharriri', 'c': False}, {'t': 'Faqat brauzer', 'c': False}]},
        {'t': 'Mashhur operatsion tizimlar?', 'a': [{'t': 'Windows, Linux, macOS, Android, iOS', 'c': True}, {'t': 'Faqat Windows', 'c': False}, {'t': 'Faqat Linux', 'c': False}, {'t': 'Hech qanday tizim yo\'q', 'c': False}]},
        {'t': 'Windows operatsion tizimini kim yaratgan?', 'a': [{'t': 'Microsoft kompaniyasi', 'c': True}, {'t': 'Apple', 'c': False}, {'t': 'Google', 'c': False}, {'t': 'IBM', 'c': False}]},
        {'t': 'Linux operatsion tizimi qanday?', 'a': [{'t': 'Ochiq kodli, bepul', 'c': True}, {'t': 'Faqat pullik', 'c': False}, {'t': 'Faqat telefon uchun', 'c': False}, {'t': 'Ishlamaydi', 'c': False}]},
        {'t': 'macOS qaysi kompaniya mahsuloti?', 'a': [{'t': 'Apple', 'c': True}, {'t': 'Microsoft', 'c': False}, {'t': 'Google', 'c': False}, {'t': 'Samsung', 'c': False}]},
        {'t': 'Android operatsion tizimi qayerda ishlatiladi?', 'a': [{'t': 'Smartfonlar va planshetlarda', 'c': True}, {'t': 'Faqat kompyuterlarda', 'c': False}, {'t': 'Faqat serverlarda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},
    {'n': 'Fayl va papkalar', 't': 20, 'o': 5, 'q': [
        {'t': 'Fayl nima?', 'a': [{'t': 'Ma\'lumotlar to\'plami', 'c': True}, {'t': 'Faqat papka', 'c': False}, {'t': 'Faqat dastur', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
        {'t': 'Papka (katalog) nima?', 'a': [{'t': 'Fayllarni saqlash joyi', 'c': True}, {'t': 'Faqat fayl', 'c': False}, {'t': 'Faqat dastur', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
        {'t': 'Fayl kengaytmasi nima?', 'a': [{'t': 'Fayl turini ko\'rsatuvchi qo\'shimcha (.txt, .jpg, .exe)', 'c': True}, {'t': 'Fayl nomi', 'c': False}, {'t': 'Fayl hajmi', 'c': False}, {'t': 'Fayl sanasi', 'c': False}]},
        {'t': '.txt fayl nima?', 'a': [{'t': 'Matnli fayl', 'c': True}, {'t': 'Rasm fayli', 'c': False}, {'t': 'Video fayl', 'c': False}, {'t': 'Dastur fayli', 'c': False}]},
        {'t': '.jpg yoki .png fayl nima?', 'a': [{'t': 'Rasm fayli', 'c': True}, {'t': 'Matnli fayl', 'c': False}, {'t': 'Video fayl', 'c': False}, {'t': 'Audio fayl', 'c': False}]},
        {'t': '.exe fayl nima?', 'a': [{'t': 'Dastur fayli (Windows)', 'c': True}, {'t': 'Matnli fayl', 'c': False}, {'t': 'Rasm fayli', 'c': False}, {'t': 'Video fayl', 'c': False}]},
        {'t': 'Fayl hajmi qanday o\'lchanadi?', 'a': [{'t': 'Bayt, kilobayt, megabayt, gigabayt', 'c': True}, {'t': 'Metr, kilometr', 'c': False}, {'t': 'Gramm, kilogramm', 'c': False}, {'t': 'Sekund, minut', 'c': False}]},
    ]},
    {'n': 'Matn muharrirlari', 't': 20, 'o': 6, 'q': [
        {'t': 'Matn muharriri nima?', 'a': [{'t': 'Matn yozish va tahrirlash dasturi', 'c': True}, {'t': 'Faqat rasm chizish dasturi', 'c': False}, {'t': 'Faqat video tahrirlash dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Microsoft Word nima?', 'a': [{'t': 'Matn muharriri', 'c': True}, {'t': 'Elektron jadval', 'c': False}, {'t': 'Taqdimot dasturi', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Notepad nima?', 'a': [{'t': 'Oddiy matn muharriri', 'c': True}, {'t': 'Murakkab grafik muharriri', 'c': False}, {'t': 'Video muharriri', 'c': False}, {'t': 'O\'yin', 'c': False}]},
        {'t': 'Matn formatlash nima?', 'a': [{'t': 'Matnni bezash (shrift, rang, o\'lcham)', 'c': True}, {'t': 'Matnni o\'chirish', 'c': False}, {'t': 'Matnni saqlash', 'c': False}, {'t': 'Matnni chop etish', 'c': False}]},
        {'t': 'Shrift nima?', 'a': [{'t': 'Matn ko\'rinishi (Times New Roman, Arial)', 'c': True}, {'t': 'Matn rangi', 'c': False}, {'t': 'Matn hajmi', 'c': False}, {'t': 'Matn tili', 'c': False}]},
        {'t': 'Ctrl+C klavish birikmasining vazifasi?', 'a': [{'t': 'Nusxa olish (copy)', 'c': True}, {'t': 'Qo\'yish (paste)', 'c': False}, {'t': 'Kesish (cut)', 'c': False}, {'t': 'Saqlash (save)', 'c': False}]},
        {'t': 'Ctrl+V klavish birikmasining vazifasi?', 'a': [{'t': 'Qo\'yish (paste)', 'c': True}, {'t': 'Nusxa olish (copy)', 'c': False}, {'t': 'Kesish (cut)', 'c': False}, {'t': 'Saqlash (save)', 'c': False}]},
    ]},
    {'n': 'Elektron jadvallar', 't': 20, 'o': 7, 'q': [
        {'t': 'Elektron jadval nima?', 'a': [{'t': 'Hisob-kitob va ma\'lumotlarni jadval ko\'rinishida qayta ishlash dasturi', 'c': True}, {'t': 'Faqat matn yozish dasturi', 'c': False}, {'t': 'Faqat rasm chizish dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Microsoft Excel nima?', 'a': [{'t': 'Elektron jadval dasturi', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Taqdimot dasturi', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Elektron jadvaldagi katak nima?', 'a': [{'t': 'Qator va ustun kesishgan joy', 'c': True}, {'t': 'Faqat qator', 'c': False}, {'t': 'Faqat ustun', 'c': False}, {'t': 'Faqat raqam', 'c': False}]},
        {'t': 'Katak manzili qanday ko\'rinishda?', 'a': [{'t': 'Ustun harfi + qator raqami (A1, B2)', 'c': True}, {'t': 'Faqat raqam', 'c': False}, {'t': 'Faqat harf', 'c': False}, {'t': 'Faqat belgi', 'c': False}]},
        {'t': 'Formula nima?', 'a': [{'t': 'Hisob-kitob uchun ifoda (=A1+B1)', 'c': True}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat raqam', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
        {'t': 'SUM funksiyasi nima qiladi?', 'a': [{'t': 'Yig\'indi hisoblab beradi', 'c': True}, {'t': 'Ko\'paytiradi', 'c': False}, {'t': 'Bo\'ladi', 'c': False}, {'t': 'Ayiradi', 'c': False}]},
        {'t': 'Diagramma nima?', 'a': [{'t': 'Ma\'lumotlarni grafik ko\'rinishda tasvirlash', 'c': True}, {'t': 'Faqat jadval', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasm', 'c': False}]},
    ]},
    {'n': 'Taqdimot dasturlari', 't': 20, 'o': 8, 'q': [
        {'t': 'Taqdimot dasturi nima?', 'a': [{'t': 'Slaydlar yaratish va ko\'rsatish dasturi', 'c': True}, {'t': 'Faqat matn yozish dasturi', 'c': False}, {'t': 'Faqat hisob-kitob dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Microsoft PowerPoint nima?', 'a': [{'t': 'Taqdimot dasturi', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Elektron jadval', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Slayd nima?', 'a': [{'t': 'Taqdimotning bitta sahifasi', 'c': True}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Taqdimotda nima bo\'lishi mumkin?', 'a': [{'t': 'Matn, rasm, video, audio, animatsiya', 'c': True}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Animatsiya nima?', 'a': [{'t': 'Ob\'ektlarning harakati', 'c': True}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Taqdimot qayerda ishlatiladi?', 'a': [{'t': 'Dars, ma\'ruza, taqdimot, konferensiya', 'c': True}, {'t': 'Faqat maktabda', 'c': False}, {'t': 'Faqat ofisda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},
    {'n': 'Grafik muharrirlar', 't': 20, 'o': 9, 'q': [
        {'t': 'Grafik muharriri nima?', 'a': [{'t': 'Rasm chizish va tahrirlash dasturi', 'c': True}, {'t': 'Faqat matn yozish dasturi', 'c': False}, {'t': 'Faqat hisob-kitob dasturi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Paint dasturi nima?', 'a': [{'t': 'Oddiy grafik muharriri', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Elektron jadval', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Adobe Photoshop nima?', 'a': [{'t': 'Professional grafik muharriri', 'c': True}, {'t': 'Oddiy matn muharriri', 'c': False}, {'t': 'Elektron jadval', 'c': False}, {'t': 'O\'yin', 'c': False}]},
        {'t': 'Rastrli grafika nima?', 'a': [{'t': 'Piksellardan tashkil topgan rasm', 'c': True}, {'t': 'Vektorli rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Vektorli grafika nima?', 'a': [{'t': 'Matematik formulalar asosida chizilgan rasm', 'c': True}, {'t': 'Piksellardan tashkil topgan rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Piksel nima?', 'a': [{'t': 'Rasmning eng kichik nuqtasi', 'c': True}, {'t': 'Rasm hajmi', 'c': False}, {'t': 'Rasm rangi', 'c': False}, {'t': 'Rasm nomi', 'c': False}]},
    ]},
    {'n': 'Internet va World Wide Web', 't': 20, 'o': 10, 'q': [
        {'t': 'Internet nima?', 'a': [{'t': 'Butun dunyo bo\'ylab kompyuterlar tarmog\'i', 'c': True}, {'t': 'Faqat bitta kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat televizor', 'c': False}]},
        {'t': 'WWW (World Wide Web) nima?', 'a': [{'t': 'Internetdagi veb-sahifalar tizimi', 'c': True}, {'t': 'Faqat elektron pochta', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat dastur', 'c': False}]},
        {'t': 'Veb-sahifa nima?', 'a': [{'t': 'Internetdagi hujjat', 'c': True}, {'t': 'Faqat kompyuterdagi fayl', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Veb-sayt nima?', 'a': [{'t': 'Bir nechta veb-sahifalar to\'plami', 'c': True}, {'t': 'Faqat bitta sahifa', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'URL nima?', 'a': [{'t': 'Veb-sahifa manzili (https://example.com)', 'c': True}, {'t': 'Faqat domen nomi', 'c': False}, {'t': 'Faqat IP manzil', 'c': False}, {'t': 'Faqat fayl nomi', 'c': False}]},
        {'t': 'Brauzer nima?', 'a': [{'t': 'Veb-sahifalarni ko\'rish dasturi', 'c': True}, {'t': 'Faqat matn muharriri', 'c': False}, {'t': 'Faqat elektron jadval', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Mashhur brauzerlar?', 'a': [{'t': 'Chrome, Firefox, Safari, Edge', 'c': True}, {'t': 'Faqat Word', 'c': False}, {'t': 'Faqat Excel', 'c': False}, {'t': 'Hech qanday brauzer yo\'q', 'c': False}]},
    ]},
    {'n': 'Elektron pochta', 't': 20, 'o': 11, 'q': [
        {'t': 'Elektron pochta (email) nima?', 'a': [{'t': 'Internet orqali xabar yuborish xizmati', 'c': True}, {'t': 'Faqat oddiy pochta', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat SMS', 'c': False}]},
        {'t': 'Email manzili qanday ko\'rinishda?', 'a': [{'t': 'user@example.com', 'c': True}, {'t': 'Faqat user', 'c': False}, {'t': 'Faqat example.com', 'c': False}, {'t': 'Faqat @', 'c': False}]},
        {'t': 'Mashhur email xizmatlari?', 'a': [{'t': 'Gmail, Yahoo, Outlook, Mail.ru', 'c': True}, {'t': 'Faqat Facebook', 'c': False}, {'t': 'Faqat Instagram', 'c': False}, {'t': 'Hech qanday xizmat yo\'q', 'c': False}]},
        {'t': 'Email yuborishda nima kerak?', 'a': [{'t': 'Qabul qiluvchi manzili, mavzu, xabar matni', 'c': True}, {'t': 'Faqat manzil', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Hech narsa kerak emas', 'c': False}]},
        {'t': 'Email ga fayl biriktirish mumkinmi?', 'a': [{'t': 'Ha, attachment orqali', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}]},
    ]},
    {'n': 'Qidiruv tizimlari', 't': 20, 'o': 12, 'q': [
        {'t': 'Qidiruv tizimi nima?', 'a': [{'t': 'Internetda ma\'lumot qidirish xizmati', 'c': True}, {'t': 'Faqat brauzer', 'c': False}, {'t': 'Faqat email', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Eng mashhur qidiruv tizimi?', 'a': [{'t': 'Google', 'c': True}, {'t': 'Word', 'c': False}, {'t': 'Excel', 'c': False}, {'t': 'Paint', 'c': False}]},
        {'t': 'Boshqa qidiruv tizimlari?', 'a': [{'t': 'Bing, Yahoo, Yandex, DuckDuckGo', 'c': True}, {'t': 'Faqat Google', 'c': False}, {'t': 'Hech qanday tizim yo\'q', 'c': False}, {'t': 'Faqat Facebook', 'c': False}]},
        {'t': 'Qidiruv so\'rovini qanday yozish kerak?', 'a': [{'t': 'Kalit so\'zlarni yozish', 'c': True}, {'t': 'Faqat bitta harf', 'c': False}, {'t': 'Faqat raqam', 'c': False}, {'t': 'Hech narsa yozmaslik', 'c': False}]},
        {'t': 'Qo\'shtirnoq ("") nima uchun ishlatiladi?', 'a': [{'t': 'Aniq iborani qidirish uchun', 'c': True}, {'t': 'Faqat bezash uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}, {'t': 'Xato ko\'rsatish uchun', 'c': False}]},
    ]},
    {'n': 'Ijtimoiy tarmoqlar', 't': 20, 'o': 13, 'q': [
        {'t': 'Ijtimoiy tarmoq nima?', 'a': [{'t': 'Odamlar muloqot qiladigan veb-sayt', 'c': True}, {'t': 'Faqat email', 'c': False}, {'t': 'Faqat qidiruv tizimi', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}]},
        {'t': 'Mashhur ijtimoiy tarmoqlar?', 'a': [{'t': 'Facebook, Instagram, Twitter, TikTok, Telegram', 'c': True}, {'t': 'Faqat Google', 'c': False}, {'t': 'Faqat Word', 'c': False}, {'t': 'Hech qanday tarmoq yo\'q', 'c': False}]},
        {'t': 'Ijtimoiy tarmoqlarda nima qilish mumkin?', 'a': [{'t': 'Xabar yuborish, rasm/video ulashish, do\'stlar topish', 'c': True}, {'t': 'Faqat o\'qish', 'c': False}, {'t': 'Hech narsa qilish mumkin emas', 'c': False}, {'t': 'Faqat yuklab olish', 'c': False}]},
        {'t': 'Profil nima?', 'a': [{'t': 'Foydalanuvchi sahifasi', 'c': True}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat matn', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Ijtimoiy tarmoqlarda xavfsizlik qoidalari?', 'a': [{'t': 'Shaxsiy ma\'lumotlarni oshkor qilmaslik, notanish odamlarga ishonmaslik', 'c': True}, {'t': 'Hamma narsani ulashish', 'c': False}, {'t': 'Parolni barchaga aytish', 'c': False}, {'t': 'Hech qanday qoida yo\'q', 'c': False}]},
    ]},
    {'n': 'Axborot xavfsizligi', 't': 20, 'o': 14, 'q': [
        {'t': 'Axborot xavfsizligi nima?', 'a': [{'t': 'Ma\'lumotlarni himoya qilish', 'c': True}, {'t': 'Faqat kompyuterni o\'chirish', 'c': False}, {'t': 'Faqat internetni o\'chirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Parol nima?', 'a': [{'t': 'Maxfiy kalit so\'z', 'c': True}, {'t': 'Faqat ism', 'c': False}, {'t': 'Faqat raqam', 'c': False}, {'t': 'Faqat harf', 'c': False}]},
        {'t': 'Kuchli parol qanday bo\'lishi kerak?', 'a': [{'t': 'Uzun, harflar, raqamlar, belgilar aralash', 'c': True}, {'t': 'Faqat 123', 'c': False}, {'t': 'Faqat ism', 'c': False}, {'t': 'Faqat bitta harf', 'c': False}]},
        {'t': 'Virus nima?', 'a': [{'t': 'Zararli dastur', 'c': True}, {'t': 'Foydali dastur', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat fayl', 'c': False}]},
        {'t': 'Antivirus nima?', 'a': [{'t': 'Viruslardan himoya qiluvchi dastur', 'c': True}, {'t': 'Virus yaratuvchi dastur', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat brauzer', 'c': False}]},
        {'t': 'Spam nima?', 'a': [{'t': 'Keraksiz xabarlar', 'c': True}, {'t': 'Foydali xabarlar', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Faqat video', 'c': False}]},
        {'t': 'Phishing nima?', 'a': [{'t': 'Shaxsiy ma\'lumotlarni o\'g\'irlash urinishi', 'c': True}, {'t': 'Foydali xizmat', 'c': False}, {'t': 'Faqat o\'yin', 'c': False}, {'t': 'Faqat email', 'c': False}]},
    ]},
    {'n': 'Kompyuter tarmoqlari', 't': 20, 'o': 15, 'q': [
        {'t': 'Kompyuter tarmog\'i nima?', 'a': [{'t': 'Bir nechta kompyuterlarning birlashmasi', 'c': True}, {'t': 'Faqat bitta kompyuter', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat telefon', 'c': False}]},
        {'t': 'LAN nima?', 'a': [{'t': 'Lokal tarmoq (Local Area Network)', 'c': True}, {'t': 'Global tarmoq', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat telefon tarmog\'i', 'c': False}]},
        {'t': 'WAN nima?', 'a': [{'t': 'Keng hudud tarmog\'i (Wide Area Network)', 'c': True}, {'t': 'Lokal tarmoq', 'c': False}, {'t': 'Faqat bitta xona', 'c': False}, {'t': 'Faqat bitta bino', 'c': False}]},
        {'t': 'IP manzil nima?', 'a': [{'t': 'Tarmoqdagi kompyuter manzili', 'c': True}, {'t': 'Faqat veb-sayt manzili', 'c': False}, {'t': 'Faqat email manzili', 'c': False}, {'t': 'Faqat telefon raqami', 'c': False}]},
        {'t': 'Router nima?', 'a': [{'t': 'Tarmoqlarni birlashtiruvchi qurilma', 'c': True}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'Faqat telefon', 'c': False}, {'t': 'Faqat printer', 'c': False}]},
    ]},
