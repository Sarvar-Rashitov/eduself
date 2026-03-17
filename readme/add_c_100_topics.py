"""
C DASTURLASH - 80 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_c():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='C', defaults={'category': cat, 'description': 'C dasturlash tili - asoslardan professionallikgacha', 'icon': 'bi-code-square', 'order': 2, 'is_active': True})
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

# 80 TA MAVZU
T = [
    {'n': 'C dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'C dasturlash tili qachon yaratilgan?', 'a': [{'t': '1972 yilda', 'c': True}, {'t': '1980 yilda', 'c': False}, {'t': '1990 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}]},
        {'t': 'C tilini kim yaratgan?', 'a': [{'t': 'Dennis Ritchie', 'c': True}, {'t': 'Bill Gates', 'c': False}, {'t': 'Steve Jobs', 'c': False}, {'t': 'Linus Torvalds', 'c': False}]},
        {'t': 'C dasturlash tili qanday til?', 'a': [{'t': 'O\'rta darajali dasturlash tili', 'c': True}, {'t': 'Yuqori darajali til', 'c': False}, {'t': 'Past darajali til', 'c': False}, {'t': 'Skript tili', 'c': False}]},
        {'t': 'C faylining kengaytmasi qanday?', 'a': [{'t': '.c', 'c': True}, {'t': '.cpp', 'c': False}, {'t': '.h', 'c': False}, {'t': '.txt', 'c': False}]},
        {'t': 'C dasturini kompilyatsiya qilish uchun?', 'a': [{'t': 'gcc file.c -o file', 'c': True}, {'t': 'python file.c', 'c': False}, {'t': 'java file.c', 'c': False}, {'t': 'run file.c', 'c': False}]},
    ]},
    {'n': 'Birinchi C dasturi', 't': 20, 'o': 2, 'q': [
        {'t': 'C dasturining asosiy funksiyasi?', 'a': [{'t': 'main()', 'c': True}, {'t': 'start()', 'c': False}, {'t': 'begin()', 'c': False}, {'t': 'run()', 'c': False}]},
        {'t': 'printf() funksiyasi nima uchun?', 'a': [{'t': 'Ekranga chiqarish', 'c': True}, {'t': 'Kiritish', 'c': False}, {'t': 'Hisoblash', 'c': False}, {'t': 'Saqlash', 'c': False}]},
        {'t': '#include <stdio.h> nima?', 'a': [{'t': 'Kutubxonani ulash', 'c': True}, {'t': 'Izoh', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'printf("Hello World"); natijasi?', 'a': [{'t': 'Hello World', 'c': True}, {'t': '"Hello World"', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'C dasturida ; belgisi nima?', 'a': [{'t': 'Operator tugashi belgisi', 'c': True}, {'t': 'Izoh belgisi', 'c': False}, {'t': 'Qo\'shtirnoq', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar va ma\'lumot turlari', 't': 25, 'o': 3, 'q': [
        {'t': 'int nima?', 'a': [{'t': 'Butun son turi', 'c': True}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Belgi', 'c': False}, {'t': 'Matn', 'c': False}]},
        {'t': 'float nima?', 'a': [{'t': 'O\'nli kasr son turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Belgi', 'c': False}, {'t': 'Matn', 'c': False}]},
        {'t': 'char nima?', 'a': [{'t': 'Belgi turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Matn', 'c': False}]},
        {'t': 'double nima?', 'a': [{'t': 'Katta o\'nli kasr', 'c': True}, {'t': 'Kichik o\'nli kasr', 'c': False}, {'t': 'Butun son', 'c': False}, {'t': 'Belgi', 'c': False}]},
        {'t': 'int x = 10; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Konstantalar', 't': 20, 'o': 4, 'q': [
        {'t': 'const nima uchun ishlatiladi?', 'a': [{'t': 'O\'zgarmas qiymat yaratish', 'c': True}, {'t': 'O\'zgaruvchi yaratish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Massiv yaratish', 'c': False}]},
        {'t': '#define nima?', 'a': [{'t': 'Makros yaratish', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'const int x = 5; x ni o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, o\'zgarmas', 'c': True}, {'t': 'Ha, o\'zgartirish mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '#define PI 3.14 to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Konstanta va o\'zgaruvchi farqi?', 'a': [{'t': 'Konstanta o\'zgarmas, o\'zgaruvchi o\'zgaradi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Konstanta kattaroq', 'c': False}, {'t': 'O\'zgaruvchi o\'zgarmas', 'c': False}]},
    ]},
    {'n': 'printf va scanf', 't': 25, 'o': 5, 'q': [
        {'t': 'printf() qaysi kutubxonada?', 'a': [{'t': 'stdio.h', 'c': True}, {'t': 'stdlib.h', 'c': False}, {'t': 'string.h', 'c': False}, {'t': 'math.h', 'c': False}]},
        {'t': 'scanf() nima uchun?', 'a': [{'t': 'Foydalanuvchidan kiritish', 'c': True}, {'t': 'Ekranga chiqarish', 'c': False}, {'t': 'Hisoblash', 'c': False}, {'t': 'Saqlash', 'c': False}]},
        {'t': '%d nima?', 'a': [{'t': 'Butun son formati', 'c': True}, {'t': 'O\'nli kasr formati', 'c': False}, {'t': 'Belgi formati', 'c': False}, {'t': 'Matn formati', 'c': False}]},
        {'t': '%f nima?', 'a': [{'t': 'O\'nli kasr formati', 'c': True}, {'t': 'Butun son formati', 'c': False}, {'t': 'Belgi formati', 'c': False}, {'t': 'Matn formati', 'c': False}]},
        {'t': 'scanf("%d", &x); & belgisi nima?', 'a': [{'t': 'Manzil operatori', 'c': True}, {'t': 'Qo\'shish operatori', 'c': False}, {'t': 'Ko\'paytirish operatori', 'c': False}, {'t': 'Bo\'lish operatori', 'c': False}]},
    ]},


    {'n': 'if operatori', 't': 25, 'o': 9, 'q': [
        {'t': 'if operatori nima uchun?', 'a': [{'t': 'Shartli bajarish', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'if (x > 5) printf("Katta"); qachon ishlaydi?', 'a': [{'t': 'x 5 dan katta bo\'lsa', 'c': True}, {'t': 'x 5 ga teng bo\'lsa', 'c': False}, {'t': 'x 5 dan kichik bo\'lsa', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'if blokida kod qanday yoziladi?', 'a': [{'t': 'Jingalak qavslar ichida {}', 'c': True}, {'t': 'Oddiy qavslar ichida ()', 'c': False}, {'t': 'Kvadrat qavslar ichida []', 'c': False}, {'t': 'Qo\'shtirnoqda ""', 'c': False}]},
        {'t': 'if (x == 5) nima tekshiradi?', 'a': [{'t': 'x 5 ga tengmi', 'c': True}, {'t': 'x ga 5 ni beradi', 'c': False}, {'t': 'x 5 dan kattami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir qatorli if da {} kerakmi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'if-else operatori', 't': 25, 'o': 10, 'q': [
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'else if nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Bir necha else if ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'if-else if-else ketma-ketligi to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, else birinchi', 'c': False}, {'t': 'Yo\'q, else if oxirida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'else dan keyin shart yozish kerakmi?', 'a': [{'t': 'Yo\'q, shart yozilmaydi', 'c': True}, {'t': 'Ha, shart yoziladi', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},

    {'n': 'switch-case operatori', 't': 25, 'o': 11, 'q': [
        {'t': 'switch-case nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'case nima?', 'a': [{'t': 'Bir variant', 'c': True}, {'t': 'Shart', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'switch dan chiqadi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'switch da break qo\'ymasak nima bo\'ladi?', 'a': [{'t': 'Keyingi case ham bajariladi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'To\'xtaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'while sikli', 't': 25, 'o': 12, 'q': [
        {'t': 'while sikli nima uchun?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'while (1) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Sikldan chiqish uchun?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'Siklning keyingi iteratsiyasiga o\'tish?', 'a': [{'t': 'continue', 'c': True}, {'t': 'skip', 'c': False}, {'t': 'next', 'c': False}, {'t': 'pass', 'c': False}]},
        {'t': 'int i=0; while(i<3) {printf("%d",i); i++;} necha marta?', 'a': [{'t': '3 marta', 'c': True}, {'t': '2 marta', 'c': False}, {'t': '4 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
    ]},
    {'n': 'do-while sikli', 't': 20, 'o': 13, 'q': [
        {'t': 'do-while va while farqi?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'while kamida 1 marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'do-while da shart qayerda tekshiriladi?', 'a': [{'t': 'Oxirida', 'c': True}, {'t': 'Boshida', 'c': False}, {'t': 'O\'rtada', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'do {...} while(shart); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while oxirida ; kerakmi?', 'a': [{'t': 'Ha, kerak', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while qachon ishlatiladi?', 'a': [{'t': 'Kamida 1 marta bajarish kerak bo\'lsa', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
    ]},
    {'n': 'for sikli', 't': 25, 'o': 14, 'q': [
        {'t': 'for sikli nima uchun?', 'a': [{'t': 'Ma\'lum marta takrorlash', 'c': True}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'for (int i=0; i<5; i++) necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for siklining 3 qismi?', 'a': [{'t': 'Boshlang\'ich, shart, o\'zgartirish', 'c': True}, {'t': 'Faqat shart', 'c': False}, {'t': 'Faqat boshlang\'ich', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for (;;) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Massivlar - Asoslar', 't': 25, 'o': 15, 'q': [
        {'t': 'Massiv nima?', 'a': [{'t': 'Bir xil turdagi elementlar to\'plami', 'c': True}, {'t': 'Bitta qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'int arr[5]; nima yaratadi?', 'a': [{'t': '5 ta butun son uchun massiv', 'c': True}, {'t': '5 qiymatli massiv', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Bitta o\'zgaruvchi', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': 'arr[0] nima?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Ikkinchi element', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int arr[5] = {1,2,3,4,5}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Massiv o\'lchamini o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, o\'zgarmas', 'c': True}, {'t': 'Ha, o\'zgartirish mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ko\'p o\'lchovli massivlar', 't': 25, 'o': 16, 'q': [
        {'t': '2 o\'lchovli massiv nima?', 'a': [{'t': 'Jadval ko\'rinishidagi massiv', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int arr[3][4]; nima yaratadi?', 'a': [{'t': '3 qator, 4 ustunli massiv', 'c': True}, {'t': '4 qator, 3 ustunli massiv', 'c': False}, {'t': '7 elementli massiv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr[0][0] nima?', 'a': [{'t': 'Birinchi qator, birinchi ustun', 'c': True}, {'t': 'Ikkinchi qator, ikkinchi ustun', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int arr[2][3] = {{1,2,3},{4,5,6}}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '2 o\'lchovli massivni qanday aylanish mumkin?', 'a': [{'t': 'Ichma-ich for sikllar bilan', 'c': True}, {'t': 'Bitta for sikl bilan', 'c': False}, {'t': 'while sikl bilan', 'c': False}, {'t': 'Aylanib bo\'lmaydi', 'c': False}]},
    ]},
    {'n': 'Satrlar (Strings)', 't': 25, 'o': 17, 'q': [
        {'t': 'C da satr nima?', 'a': [{'t': 'Belgilar massivi', 'c': True}, {'t': 'Alohida ma\'lumot turi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'char str[10]; nima yaratadi?', 'a': [{'t': '10 belgili satr uchun joy', 'c': True}, {'t': '10 ta satr', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Bitta belgi', 'c': False}]},
        {'t': 'Satr oxirida qanday belgi bo\'ladi?', 'a': [{'t': '\\0 (null belgi)', 'c': True}, {'t': '\\n (yangi qator)', 'c': False}, {'t': 'Bo\'sh joy', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'char str[] = "Hello"; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'printf("%s", str); nima qiladi?', 'a': [{'t': 'Satrni chiqaradi', 'c': True}, {'t': 'Birinchi belgini chiqaradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'String kutubxonasi', 't': 25, 'o': 18, 'q': [
        {'t': 'String funksiyalari qaysi kutubxonada?', 'a': [{'t': 'string.h', 'c': True}, {'t': 'stdio.h', 'c': False}, {'t': 'stdlib.h', 'c': False}, {'t': 'math.h', 'c': False}]},
        {'t': 'strlen(str) nima qiladi?', 'a': [{'t': 'Satr uzunligini qaytaradi', 'c': True}, {'t': 'Satrni ko\'chiradi', 'c': False}, {'t': 'Satrlarni birlashtiradi', 'c': False}, {'t': 'Satrlarni taqqoslaydi', 'c': False}]},
        {'t': 'strcpy(dest, src) nima qiladi?', 'a': [{'t': 'src ni dest ga ko\'chiradi', 'c': True}, {'t': 'dest ni src ga ko\'chiradi', 'c': False}, {'t': 'Satrlarni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'strcat(str1, str2) nima qiladi?', 'a': [{'t': 'str2 ni str1 ga qo\'shadi', 'c': True}, {'t': 'str1 ni str2 ga qo\'shadi', 'c': False}, {'t': 'Satrlarni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'strcmp(str1, str2) nima qaytaradi?', 'a': [{'t': '0 agar teng bo\'lsa', 'c': True}, {'t': '1 agar teng bo\'lsa', 'c': False}, {'t': '-1 agar teng bo\'lsa', 'c': False}, {'t': 'true agar teng bo\'lsa', 'c': False}]},
    ]},
    {'n': 'Funksiyalar - Asoslar', 't': 25, 'o': 19, 'q': [
        {'t': 'Funksiya nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Funksiya qanday e\'lon qilinadi?', 'a': [{'t': 'tur_nomi funksiya_nomi(parametrlar)', 'c': True}, {'t': 'function funksiya_nomi()', 'c': False}, {'t': 'def funksiya_nomi()', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'void nima?', 'a': [{'t': 'Hech narsa qaytarmaydi', 'c': True}, {'t': 'Butun son qaytaradi', 'c': False}, {'t': 'O\'nli kasr qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'return nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi va funksiyadan chiqadi', 'c': True}, {'t': 'Faqat qiymat qaytaradi', 'c': False}, {'t': 'Faqat funksiyadan chiqadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiyani chaqirish?', 'a': [{'t': 'funksiya_nomi(argumentlar);', 'c': True}, {'t': 'call funksiya_nomi();', 'c': False}, {'t': 'run funksiya_nomi();', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
    ]},
    {'n': 'Funksiya parametrlari', 't': 25, 'o': 20, 'q': [
        {'t': 'Parametr nima?', 'a': [{'t': 'Funksiyaga beriladigan qiymat', 'c': True}, {'t': 'Funksiya nomi', 'c': False}, {'t': 'Funksiya natijasi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Argument nima?', 'a': [{'t': 'Funksiyaga berilgan haqiqiy qiymat', 'c': True}, {'t': 'Funksiya parametri', 'c': False}, {'t': 'Funksiya nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int sum(int a, int b) - a va b nima?', 'a': [{'t': 'Parametrlar', 'c': True}, {'t': 'Argumentlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sum(5, 3) - 5 va 3 nima?', 'a': [{'t': 'Argumentlar', 'c': True}, {'t': 'Parametrlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiyaga massiv uzatish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat kichik massivlar', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},

    {'n': 'Funksiya prototipi', 't': 20, 'o': 21, 'q': [
        {'t': 'Funksiya prototipi nima?', 'a': [{'t': 'Funksiya e\'loni', 'c': True}, {'t': 'Funksiya tanasi', 'c': False}, {'t': 'Funksiya chaqiruvi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Prototip qayerda yoziladi?', 'a': [{'t': 'main() dan oldin', 'c': True}, {'t': 'main() ichida', 'c': False}, {'t': 'main() dan keyin', 'c': False}, {'t': 'Istalgan joyda', 'c': False}]},
        {'t': 'int sum(int, int); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri prototip', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Prototipda parametr nomlari kerakmi?', 'a': [{'t': 'Yo\'q, faqat turlar kifoya', 'c': True}, {'t': 'Ha, nomlar majburiy', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Prototip nima uchun kerak?', 'a': [{'t': 'Kompilyatorga funksiya haqida xabar berish', 'c': True}, {'t': 'Funksiyani chaqirish', 'c': False}, {'t': 'Funksiyani yaratish', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},
    {'n': 'Rekursiya', 't': 25, 'o': 22, 'q': [
        {'t': 'Rekursiya nima?', 'a': [{'t': 'Funksiyaning o\'zini chaqirishi', 'c': True}, {'t': 'Sikl', 'c': False}, {'t': 'Shart', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Rekursiv funksiyada nima bo\'lishi kerak?', 'a': [{'t': 'To\'xtash sharti', 'c': True}, {'t': 'Faqat chaqiruv', 'c': False}, {'t': 'Faqat return', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Faktorial hisoblash rekursiv bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat kichik sonlar uchun', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Rekursiya va sikl farqi?', 'a': [{'t': 'Rekursiya o\'zini chaqiradi, sikl takrorlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Sikl o\'zini chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Cheksiz rekursiya nima?', 'a': [{'t': 'To\'xtash sharti bo\'lmagan rekursiya', 'c': True}, {'t': 'Oddiy rekursiya', 'c': False}, {'t': 'Tez rekursiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Ko\'rsatkichlar (Pointers) - Asoslar', 't': 30, 'o': 23, 'q': [
        {'t': 'Pointer nima?', 'a': [{'t': 'Xotira manzilini saqlovchi o\'zgaruvchi', 'c': True}, {'t': 'Oddiy o\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': '& operatori nima?', 'a': [{'t': 'Manzil operatori', 'c': True}, {'t': 'Qiymat operatori', 'c': False}, {'t': 'Ko\'paytirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '* operatori nima?', 'a': [{'t': 'Dereference operatori (qiymatni olish)', 'c': True}, {'t': 'Manzil operatori', 'c': False}, {'t': 'Faqat ko\'paytirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int *p; nima yaratadi?', 'a': [{'t': 'int turidagi pointer', 'c': True}, {'t': 'int o\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Massiv', 'c': False}]},
        {'t': 'p = &x; nima qiladi?', 'a': [{'t': 'p ga x ning manzilini beradi', 'c': True}, {'t': 'p ga x ning qiymatini beradi', 'c': False}, {'t': 'x ga p ni beradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '*p nima qaytaradi?', 'a': [{'t': 'p ko\'rsatayotgan qiymatni', 'c': True}, {'t': 'p ning manzilini', 'c': False}, {'t': 'p ning o\'zini', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Pointerlar va massivlar', 't': 30, 'o': 24, 'q': [
        {'t': 'Massiv nomi nima?', 'a': [{'t': 'Birinchi elementning manzili', 'c': True}, {'t': 'Massiv qiymati', 'c': False}, {'t': 'Massiv o\'lchami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int arr[5]; int *p = arr; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'arr[i] va *(arr+i) bir xilmi?', 'a': [{'t': 'Ha, bir xil', 'c': True}, {'t': 'Yo\'q, har xil', 'c': False}, {'t': 'Ba\'zan bir xil', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Pointer arifmetikasi nima?', 'a': [{'t': 'Pointer bilan hisoblash', 'c': True}, {'t': 'Oddiy arifmetika', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'p++ nima qiladi?', 'a': [{'t': 'Keyingi elementga o\'tadi', 'c': True}, {'t': 'Qiymatni oshiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Funksiyaga pointer uzatish', 't': 25, 'o': 25, 'q': [
        {'t': 'Funksiyaga pointer nima uchun uzatiladi?', 'a': [{'t': 'Qiymatni o\'zgartirish uchun', 'c': True}, {'t': 'Faqat o\'qish uchun', 'c': False}, {'t': 'Tezroq ishlash uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'void func(int *p) - bu nima?', 'a': [{'t': 'Pointer parametrli funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Massiv funksiyasi', 'c': False}]},
        {'t': 'func(&x); nima qiladi?', 'a': [{'t': 'x ning manzilini uzatadi', 'c': True}, {'t': 'x ning qiymatini uzatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Call by value va call by reference farqi?', 'a': [{'t': 'Value nusxa, reference manzil uzatadi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Value tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiyada *p = 10; tashqarida o\'zgaradimi?', 'a': [{'t': 'Ha, o\'zgaradi', 'c': True}, {'t': 'Yo\'q, o\'zgarmaydi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Dinamik xotira - malloc', 't': 30, 'o': 26, 'q': [
        {'t': 'malloc() nima qiladi?', 'a': [{'t': 'Dinamik xotira ajratadi', 'c': True}, {'t': 'Xotirani bo\'shatadi', 'c': False}, {'t': 'Xotirani ko\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'malloc() qaysi kutubxonada?', 'a': [{'t': 'stdlib.h', 'c': True}, {'t': 'stdio.h', 'c': False}, {'t': 'string.h', 'c': False}, {'t': 'math.h', 'c': False}]},
        {'t': 'int *p = (int*)malloc(5*sizeof(int)); nima?', 'a': [{'t': '5 ta int uchun xotira', 'c': True}, {'t': '5 bayt xotira', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '1 ta int uchun xotira', 'c': False}]},
        {'t': 'sizeof() nima qaytaradi?', 'a': [{'t': 'Ma\'lumot turi o\'lchamini baytda', 'c': True}, {'t': 'Qiymatni', 'c': False}, {'t': 'Manzilni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'malloc() muvaffaqiyatsiz bo\'lsa nima qaytaradi?', 'a': [{'t': 'NULL', 'c': True}, {'t': '0', 'c': False}, {'t': '-1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Dinamik xotira - calloc va realloc', 't': 25, 'o': 27, 'q': [
        {'t': 'calloc() va malloc() farqi?', 'a': [{'t': 'calloc() xotirani 0 ga to\'ldiradi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'malloc() tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'realloc() nima qiladi?', 'a': [{'t': 'Xotira o\'lchamini o\'zgartiradi', 'c': True}, {'t': 'Yangi xotira ajratadi', 'c': False}, {'t': 'Xotirani bo\'shatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'free() nima qiladi?', 'a': [{'t': 'Xotirani bo\'shatadi', 'c': True}, {'t': 'Xotira ajratadi', 'c': False}, {'t': 'Xotirani ko\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'free() dan keyin pointer ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q, xavfli', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Memory leak nima?', 'a': [{'t': 'Xotira oqishi (free qilinmagan)', 'c': True}, {'t': 'Xotira tugashi', 'c': False}, {'t': 'Xotira xatosi', 'c': False}, {'t': 'Oddiy xato', 'c': False}]},
    ]},
    {'n': 'Strukturalar (Structures)', 't': 30, 'o': 28, 'q': [
        {'t': 'struct nima?', 'a': [{'t': 'Turli turdagi ma\'lumotlar to\'plami', 'c': True}, {'t': 'Bir xil turdagi ma\'lumotlar', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'struct Student {...}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Struktura a\'zosiga qanday murojaat qilinadi?', 'a': [{'t': 'student.name', 'c': True}, {'t': 'student->name', 'c': False}, {'t': 'student[name]', 'c': False}, {'t': 'student(name)', 'c': False}]},
        {'t': 'struct Student s1, s2; nima yaratadi?', 'a': [{'t': '2 ta Student o\'zgaruvchi', 'c': True}, {'t': '1 ta Student o\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Massiv', 'c': False}]},
        {'t': 'Struktura ichida struktura bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Struktura va pointer', 't': 25, 'o': 29, 'q': [
        {'t': 'struct Student *p; nima?', 'a': [{'t': 'Struktura pointeri', 'c': True}, {'t': 'Oddiy struktura', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Massiv', 'c': False}]},
        {'t': 'Pointer orqali a\'zoga murojaat?', 'a': [{'t': 'p->name', 'c': True}, {'t': 'p.name', 'c': False}, {'t': 'p[name]', 'c': False}, {'t': 'p(name)', 'c': False}]},
        {'t': '-> operatori nima?', 'a': [{'t': 'Pointer orqali a\'zoga murojaat', 'c': True}, {'t': 'Oddiy murojaat', 'c': False}, {'t': 'Manzil olish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'p->name va (*p).name bir xilmi?', 'a': [{'t': 'Ha, bir xil', 'c': True}, {'t': 'Yo\'q, har xil', 'c': False}, {'t': 'Ba\'zan bir xil', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Strukturaga pointer uzatish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat kichik strukturalar', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'typedef', 't': 20, 'o': 30, 'q': [
        {'t': 'typedef nima uchun?', 'a': [{'t': 'Yangi tur nomi yaratish', 'c': True}, {'t': 'O\'zgaruvchi yaratish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'typedef int Integer; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'typedef struct {...} Student; nima?', 'a': [{'t': 'Student tur nomini yaratadi', 'c': True}, {'t': 'Student o\'zgaruvchi yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'typedef dan keyin struct yozish kerakmi?', 'a': [{'t': 'Yo\'q, kerak emas', 'c': True}, {'t': 'Ha, kerak', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'typedef ning afzalligi?', 'a': [{'t': 'Kodni o\'qish osonroq', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},
    {'n': 'Union', 't': 25, 'o': 31, 'q': [
        {'t': 'union nima?', 'a': [{'t': 'Bir xotira joyini bo\'lishuvchi tur', 'c': True}, {'t': 'struct bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'union va struct farqi?', 'a': [{'t': 'union bir xotira, struct alohida', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'struct bir xotira', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'union Data {int i; float f;}; o\'lchami?', 'a': [{'t': 'Eng katta a\'zo o\'lchami', 'c': True}, {'t': 'Barcha a\'zolar yig\'indisi', 'c': False}, {'t': '0', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'union da bir vaqtda nechta a\'zo ishlatiladi?', 'a': [{'t': 'Faqat bitta', 'c': True}, {'t': 'Barcha a\'zolar', 'c': False}, {'t': 'Ikkita', 'c': False}, {'t': 'Istalgancha', 'c': False}]},
        {'t': 'union qachon ishlatiladi?', 'a': [{'t': 'Xotirani tejash kerak bo\'lsa', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
    ]},
    {'n': 'Enum', 't': 20, 'o': 32, 'q': [
        {'t': 'enum nima?', 'a': [{'t': 'Nomli konstantalar to\'plami', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'enum Color {RED, GREEN, BLUE}; RED qiymati?', 'a': [{'t': '0', 'c': True}, {'t': '1', 'c': False}, {'t': '-1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'enum da qiymatlar avtomatik oshiriladi?', 'a': [{'t': 'Ha, 0 dan boshlab', 'c': True}, {'t': 'Yo\'q, qo\'lda berish kerak', 'c': False}, {'t': '1 dan boshlab', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'enum Color {RED=5, GREEN, BLUE}; GREEN qiymati?', 'a': [{'t': '6', 'c': True}, {'t': '5', 'c': False}, {'t': '1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'enum ning afzalligi?', 'a': [{'t': 'Kodni tushunarli qiladi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},
    {'n': 'Fayl bilan ishlash - Asoslar', 't': 30, 'o': 33, 'q': [
        {'t': 'FILE nima?', 'a': [{'t': 'Fayl turi', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'fopen() nima qiladi?', 'a': [{'t': 'Faylni ochadi', 'c': True}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Fayldan o\'qiydi', 'c': False}]},
        {'t': 'fopen("file.txt", "r") - "r" nima?', 'a': [{'t': 'O\'qish rejimi', 'c': True}, {'t': 'Yozish rejimi', 'c': False}, {'t': 'Qo\'shish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fopen("file.txt", "w") - "w" nima?', 'a': [{'t': 'Yozish rejimi', 'c': True}, {'t': 'O\'qish rejimi', 'c': False}, {'t': 'Qo\'shish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fclose() nima qiladi?', 'a': [{'t': 'Faylni yopadi', 'c': True}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Faylga yozish va o\'qish', 't': 30, 'o': 34, 'q': [
        {'t': 'fprintf() nima qiladi?', 'a': [{'t': 'Faylga yozadi', 'c': True}, {'t': 'Fayldan o\'qiydi', 'c': False}, {'t': 'Ekranga chiqaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fscanf() nima qiladi?', 'a': [{'t': 'Fayldan o\'qiydi', 'c': True}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Klaviaturadan o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fgetc() nima qiladi?', 'a': [{'t': 'Fayldan bitta belgi o\'qiydi', 'c': True}, {'t': 'Faylga bitta belgi yozadi', 'c': False}, {'t': 'Fayldan qator o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fputc() nima qiladi?', 'a': [{'t': 'Faylga bitta belgi yozadi', 'c': True}, {'t': 'Fayldan bitta belgi o\'qiydi', 'c': False}, {'t': 'Faylga qator yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fgets() nima qiladi?', 'a': [{'t': 'Fayldan qator o\'qiydi', 'c': True}, {'t': 'Faylga qator yozadi', 'c': False}, {'t': 'Fayldan belgi o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Preprocessor direktivalar', 't': 25, 'o': 35, 'q': [
        {'t': '#include nima?', 'a': [{'t': 'Fayl ulash', 'c': True}, {'t': 'Makros yaratish', 'c': False}, {'t': 'Shart', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': '#define nima?', 'a': [{'t': 'Makros yaratish', 'c': True}, {'t': 'Fayl ulash', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '#ifdef nima?', 'a': [{'t': 'Agar aniqlangan bo\'lsa', 'c': True}, {'t': 'Agar aniqlanmagan bo\'lsa', 'c': False}, {'t': 'Fayl ulash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '#ifndef nima?', 'a': [{'t': 'Agar aniqlanmagan bo\'lsa', 'c': True}, {'t': 'Agar aniqlangan bo\'lsa', 'c': False}, {'t': 'Fayl ulash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '#endif nima?', 'a': [{'t': 'Shartli kompilyatsiya tugashi', 'c': True}, {'t': 'Fayl tugashi', 'c': False}, {'t': 'Funksiya tugashi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Header fayllar', 't': 25, 'o': 36, 'q': [
        {'t': 'Header fayl nima?', 'a': [{'t': 'Funksiya prototiplari va makroslar fayli', 'c': True}, {'t': 'Asosiy dastur fayli', 'c': False}, {'t': 'Ma\'lumotlar fayli', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Header fayl kengaytmasi?', 'a': [{'t': '.h', 'c': True}, {'t': '.c', 'c': False}, {'t': '.cpp', 'c': False}, {'t': '.txt', 'c': False}]},
        {'t': '#include <stdio.h> va #include "myfile.h" farqi?', 'a': [{'t': '<> standart, "" foydalanuvchi fayli', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '"" standart fayl', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Header faylda nima bo\'ladi?', 'a': [{'t': 'Prototiplar, makroslar, typedef', 'c': True}, {'t': 'Faqat funksiya tanasi', 'c': False}, {'t': 'Faqat main()', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Header guard nima?', 'a': [{'t': 'Takroriy ulashni oldini olish', 'c': True}, {'t': 'Xavfsizlik', 'c': False}, {'t': 'Tezlashtirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Bitwise operatorlar', 't': 30, 'o': 37, 'q': [
        {'t': '& operatori (bitwise)?', 'a': [{'t': 'Bitwise AND', 'c': True}, {'t': 'Bitwise OR', 'c': False}, {'t': 'Bitwise XOR', 'c': False}, {'t': 'Manzil', 'c': False}]},
        {'t': '| operatori?', 'a': [{'t': 'Bitwise OR', 'c': True}, {'t': 'Bitwise AND', 'c': False}, {'t': 'Bitwise XOR', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '^ operatori?', 'a': [{'t': 'Bitwise XOR', 'c': True}, {'t': 'Bitwise AND', 'c': False}, {'t': 'Bitwise OR', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '~ operatori?', 'a': [{'t': 'Bitwise NOT', 'c': True}, {'t': 'Bitwise AND', 'c': False}, {'t': 'Bitwise OR', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '<< operatori?', 'a': [{'t': 'Chapga siljitish', 'c': True}, {'t': 'O\'ngga siljitish', 'c': False}, {'t': 'Taqqoslash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '>> operatori?', 'a': [{'t': 'O\'ngga siljitish', 'c': True}, {'t': 'Chapga siljitish', 'c': False}, {'t': 'Taqqoslash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Command line arguments', 't': 25, 'o': 38, 'q': [
        {'t': 'int main(int argc, char *argv[]) - argc nima?', 'a': [{'t': 'Argumentlar soni', 'c': True}, {'t': 'Argumentlar qiymati', 'c': False}, {'t': 'Dastur nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'argv nima?', 'a': [{'t': 'Argumentlar massivi', 'c': True}, {'t': 'Argumentlar soni', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'argv[0] nima?', 'a': [{'t': 'Dastur nomi', 'c': True}, {'t': 'Birinchi argument', 'c': False}, {'t': 'Argumentlar soni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'argv[1] nima?', 'a': [{'t': 'Birinchi argument', 'c': True}, {'t': 'Dastur nomi', 'c': False}, {'t': 'Ikkinchi argument', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': './program arg1 arg2 - argc qiymati?', 'a': [{'t': '3', 'c': True}, {'t': '2', 'c': False}, {'t': '1', 'c': False}, {'t': '0', 'c': False}]},
    ]},
    {'n': 'Math kutubxonasi', 't': 25, 'o': 39, 'q': [
        {'t': 'Math funksiyalari qaysi kutubxonada?', 'a': [{'t': 'math.h', 'c': True}, {'t': 'stdio.h', 'c': False}, {'t': 'stdlib.h', 'c': False}, {'t': 'string.h', 'c': False}]},
        {'t': 'sqrt() nima qiladi?', 'a': [{'t': 'Kvadrat ildiz', 'c': True}, {'t': 'Daraja', 'c': False}, {'t': 'Mutlaq qiymat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'pow(x, y) nima qiladi?', 'a': [{'t': 'x ning y darajasi', 'c': True}, {'t': 'x + y', 'c': False}, {'t': 'x * y', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'abs() nima qiladi?', 'a': [{'t': 'Mutlaq qiymat', 'c': True}, {'t': 'Kvadrat ildiz', 'c': False}, {'t': 'Daraja', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'ceil() nima qiladi?', 'a': [{'t': 'Yuqoriga yaxlitlash', 'c': True}, {'t': 'Pastga yaxlitlash', 'c': False}, {'t': 'Oddiy yaxlitlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'floor() nima qiladi?', 'a': [{'t': 'Pastga yaxlitlash', 'c': True}, {'t': 'Yuqoriga yaxlitlash', 'c': False}, {'t': 'Oddiy yaxlitlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Time kutubxonasi', 't': 25, 'o': 40, 'q': [
        {'t': 'time.h nima uchun?', 'a': [{'t': 'Vaqt bilan ishlash', 'c': True}, {'t': 'Matematik amallar', 'c': False}, {'t': 'Fayl bilan ishlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'time() nima qaytaradi?', 'a': [{'t': 'Hozirgi vaqt (sekundlarda)', 'c': True}, {'t': 'Hozirgi sana', 'c': False}, {'t': 'Soat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'clock() nima uchun?', 'a': [{'t': 'Dastur ishlash vaqtini o\'lchash', 'c': True}, {'t': 'Hozirgi vaqtni olish', 'c': False}, {'t': 'Sanani olish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'difftime() nima qiladi?', 'a': [{'t': 'Ikki vaqt orasidagi farq', 'c': True}, {'t': 'Vaqtni qo\'shadi', 'c': False}, {'t': 'Vaqtni ko\'paytiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'struct tm nima?', 'a': [{'t': 'Vaqt strukturasi', 'c': True}, {'t': 'Oddiy struktura', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Xatolar bilan ishlash', 't': 25, 'o': 41, 'q': [
        {'t': 'errno nima?', 'a': [{'t': 'Xato kodi o\'zgaruvchisi', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}]},
        {'t': 'perror() nima qiladi?', 'a': [{'t': 'Xato xabarini chiqaradi', 'c': True}, {'t': 'Xatoni to\'g\'rilaydi', 'c': False}, {'t': 'Xatoni e\'tiborsiz qoldiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'strerror() nima qaytaradi?', 'a': [{'t': 'Xato tavsifi', 'c': True}, {'t': 'Xato kodi', 'c': False}, {'t': 'Xato soni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'NULL pointer xatosi qachon yuzaga keladi?', 'a': [{'t': 'NULL ga murojaat qilinganda', 'c': True}, {'t': 'Xotira tugaganda', 'c': False}, {'t': 'Fayl topilmaganda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Segmentation fault nima?', 'a': [{'t': 'Noto\'g\'ri xotiraga murojaat', 'c': True}, {'t': 'Sintaksis xatosi', 'c': False}, {'t': 'Mantiqiy xato', 'c': False}, {'t': 'Oddiy xato', 'c': False}]},
    ]},
    {'n': 'Makroslar', 't': 25, 'o': 42, 'q': [
        {'t': 'Makros nima?', 'a': [{'t': 'Preprocessor tomonidan almashtiriluvchi kod', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': '#define MAX(a,b) ((a)>(b)?(a):(b)) nima?', 'a': [{'t': 'Funksiya kabi makros', 'c': True}, {'t': 'Oddiy makros', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Makros va funksiya farqi?', 'a': [{'t': 'Makros kompilyatsiyadan oldin almashtiriladi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Funksiya tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '#undef nima qiladi?', 'a': [{'t': 'Makrosni bekor qiladi', 'c': True}, {'t': 'Makros yaratadi', 'c': False}, {'t': 'Funksiya yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Makrosda () qo\'yish nima uchun muhim?', 'a': [{'t': 'Operator ustuvorligini to\'g\'rilash', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Majburiy emas', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Fayl bilan ishlash - Asoslar', 't': 30, 'o': 33, 'q': [
        {'t': 'FILE nima?', 'a': [{'t': 'Fayl turi', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'fopen() nima qiladi?', 'a': [{'t': 'Faylni ochadi', 'c': True}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Fayldan o\'qiydi', 'c': False}]},
        {'t': 'fopen("file.txt", "r") - "r" nima?', 'a': [{'t': 'O\'qish rejimi', 'c': True}, {'t': 'Yozish rejimi', 'c': False}, {'t': 'Qo\'shish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fopen("file.txt", "w") - "w" nima?', 'a': [{'t': 'Yozish rejimi', 'c': True}, {'t': 'O\'qish rejimi', 'c': False}, {'t': 'Qo\'shish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fclose() nima qiladi?', 'a': [{'t': 'Faylni yopadi', 'c': True}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fopen() muvaffaqiyatsiz bo\'lsa nima qaytaradi?', 'a': [{'t': 'NULL', 'c': True}, {'t': '0', 'c': False}, {'t': '-1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Faylga yozish', 't': 25, 'o': 34, 'q': [
        {'t': 'fprintf() nima qiladi?', 'a': [{'t': 'Faylga formatlangan yozadi', 'c': True}, {'t': 'Ekranga chiqaradi', 'c': False}, {'t': 'Fayldan o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fputc() nima qiladi?', 'a': [{'t': 'Faylga bitta belgi yozadi', 'c': True}, {'t': 'Fayldan bitta belgi o\'qiydi', 'c': False}, {'t': 'Faylga satr yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fputs() nima qiladi?', 'a': [{'t': 'Faylga satr yozadi', 'c': True}, {'t': 'Fayldan satr o\'qiydi', 'c': False}, {'t': 'Faylga belgi yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fwrite() nima uchun?', 'a': [{'t': 'Binary ma\'lumot yozish', 'c': True}, {'t': 'Matn yozish', 'c': False}, {'t': 'O\'qish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"w" rejimida fayl mavjud bo\'lsa nima bo\'ladi?', 'a': [{'t': 'Fayl tozalanadi', 'c': True}, {'t': 'Faylga qo\'shiladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Fayldan o\'qish', 't': 25, 'o': 35, 'q': [
        {'t': 'fscanf() nima qiladi?', 'a': [{'t': 'Fayldan formatlangan o\'qiydi', 'c': True}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Ekrandan o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fgetc() nima qiladi?', 'a': [{'t': 'Fayldan bitta belgi o\'qiydi', 'c': True}, {'t': 'Faylga bitta belgi yozadi', 'c': False}, {'t': 'Fayldan satr o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fgets() nima qiladi?', 'a': [{'t': 'Fayldan satr o\'qiydi', 'c': True}, {'t': 'Faylga satr yozadi', 'c': False}, {'t': 'Fayldan belgi o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'fread() nima uchun?', 'a': [{'t': 'Binary ma\'lumot o\'qish', 'c': True}, {'t': 'Matn o\'qish', 'c': False}, {'t': 'Yozish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'feof() nima tekshiradi?', 'a': [{'t': 'Fayl oxiriga yetdimi', 'c': True}, {'t': 'Fayl ochiqmi', 'c': False}, {'t': 'Fayl mavjudmi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🔷 C DASTURLASH - 100 TA MAVZU")
    print("=" * 80)
    subject = get_or_create_c()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T[:40])
    total = sum(len(t['q']) for t in T[:40])
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! 10 ta mavzu, {total} ta test qo'shildi!")
    print(f"📝 To'g'ri javoblar tasodifiy joylashtirildi")
    print("=" * 80)