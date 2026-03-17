"""
C++ DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_cpp():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='C++', defaults={'category': cat, 'description': 'C++ dasturlash tili - asoslardan OOP gacha', 'icon': 'bi-code-square', 'order': 3, 'is_active': True})
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
    {'n': 'C++ dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'C++ qachon yaratilgan?', 'a': [{'t': '1983 yilda', 'c': True}, {'t': '1972 yilda', 'c': False}, {'t': '1990 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}]},
        {'t': 'C++ ni kim yaratgan?', 'a': [{'t': 'Bjarne Stroustrup', 'c': True}, {'t': 'Dennis Ritchie', 'c': False}, {'t': 'James Gosling', 'c': False}, {'t': 'Guido van Rossum', 'c': False}]},
        {'t': 'C++ faylining kengaytmasi?', 'a': [{'t': '.cpp', 'c': True}, {'t': '.c', 'c': False}, {'t': '.java', 'c': False}, {'t': '.py', 'c': False}]},
        {'t': 'C++ C tilidan qanday farq qiladi?', 'a': [{'t': 'OOP qo\'llab-quvvatlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Faqat tezroq', 'c': False}, {'t': 'Faqat yangi', 'c': False}]},
        {'t': 'C++ dasturini kompilyatsiya qilish?', 'a': [{'t': 'g++ file.cpp -o file', 'c': True}, {'t': 'gcc file.cpp', 'c': False}, {'t': 'python file.cpp', 'c': False}, {'t': 'javac file.cpp', 'c': False}]},
    ]},
    {'n': 'Birinchi C++ dasturi', 't': 20, 'o': 2, 'q': [
        {'t': 'C++ da asosiy funksiya?', 'a': [{'t': 'int main()', 'c': True}, {'t': 'void start()', 'c': False}, {'t': 'begin()', 'c': False}, {'t': 'program()', 'c': False}]},
        {'t': 'cout nima uchun ishlatiladi?', 'a': [{'t': 'Ekranga chiqarish', 'c': True}, {'t': 'Kiritish', 'c': False}, {'t': 'Hisoblash', 'c': False}, {'t': 'Saqlash', 'c': False}]},
        {'t': '#include <iostream> nima?', 'a': [{'t': 'Kiritish-chiqarish kutubxonasi', 'c': True}, {'t': 'Matematik kutubxona', 'c': False}, {'t': 'String kutubxona', 'c': False}, {'t': 'Fayl kutubxonasi', 'c': False}]},
        {'t': 'cout << "Hello"; natijasi?', 'a': [{'t': 'Hello', 'c': True}, {'t': '"Hello"', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'cout Hello', 'c': False}]},
        {'t': 'using namespace std; nima uchun?', 'a': [{'t': 'std:: yozmaslik uchun', 'c': True}, {'t': 'Dasturni tezlashtirish', 'c': False}, {'t': 'Xotirani tejash', 'c': False}, {'t': 'Majburiy', 'c': False}]},
        {'t': 'endl nima qiladi?', 'a': [{'t': 'Yangi qatorga o\'tadi', 'c': True}, {'t': 'Bo\'sh joy qo\'yadi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar va ma\'lumot turlari', 't': 25, 'o': 3, 'q': [
        {'t': 'int nima?', 'a': [{'t': 'Butun son turi', 'c': True}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy', 'c': False}]},
        {'t': 'double nima?', 'a': [{'t': 'Katta o\'nli kasr', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Belgi', 'c': False}, {'t': 'Matn', 'c': False}]},
        {'t': 'bool nima?', 'a': [{'t': 'Mantiqiy tur (true/false)', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Belgi', 'c': False}]},
        {'t': 'string nima?', 'a': [{'t': 'Matn turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Belgi', 'c': False}, {'t': 'Mantiqiy', 'c': False}]},
        {'t': 'char nima?', 'a': [{'t': 'Bitta belgi turi', 'c': True}, {'t': 'Matn', 'c': False}, {'t': 'Butun son', 'c': False}, {'t': 'O\'nli kasr', 'c': False}]},
        {'t': 'auto kalit so\'zi nima qiladi?', 'a': [{'t': 'Turni avtomatik aniqlaydi', 'c': True}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}, {'t': 'Funksiya yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'cin va cout', 't': 20, 'o': 4, 'q': [
        {'t': 'cin nima uchun?', 'a': [{'t': 'Foydalanuvchidan kiritish', 'c': True}, {'t': 'Ekranga chiqarish', 'c': False}, {'t': 'Hisoblash', 'c': False}, {'t': 'Saqlash', 'c': False}]},
        {'t': 'cin >> x; nima qiladi?', 'a': [{'t': 'x ga qiymat kiritadi', 'c': True}, {'t': 'x ni chiqaradi', 'c': False}, {'t': 'x ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'cout << x << y; nima qiladi?', 'a': [{'t': 'x va y ni ketma-ket chiqaradi', 'c': True}, {'t': 'x va y ni qo\'shadi', 'c': False}, {'t': 'Faqat x ni chiqaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '<< operatori nima?', 'a': [{'t': 'Chiqarish operatori', 'c': True}, {'t': 'Kiritish operatori', 'c': False}, {'t': 'Qo\'shish operatori', 'c': False}, {'t': 'Ko\'paytirish', 'c': False}]},
        {'t': '>> operatori nima?', 'a': [{'t': 'Kiritish operatori', 'c': True}, {'t': 'Chiqarish operatori', 'c': False}, {'t': 'Bo\'lish operatori', 'c': False}, {'t': 'Ayirish', 'c': False}]},
    ]},
    {'n': 'Operatorlar', 't': 25, 'o': 5, 'q': [
        {'t': '5 + 3 natijasi?', 'a': [{'t': '8', 'c': True}, {'t': '53', 'c': False}, {'t': '2', 'c': False}, {'t': '15', 'c': False}]},
        {'t': '10 / 3 natijasi (int)?', 'a': [{'t': '3', 'c': True}, {'t': '3.33', 'c': False}, {'t': '4', 'c': False}, {'t': '3.0', 'c': False}]},
        {'t': '10.0 / 3 natijasi?', 'a': [{'t': '3.33...', 'c': True}, {'t': '3', 'c': False}, {'t': '4', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '10 % 3 natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': '10', 'c': False}]},
        {'t': 'x++ va ++x farqi?', 'a': [{'t': 'x++ keyin oshiradi, ++x oldin', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'x++ tezroq', 'c': False}, {'t': '++x xato', 'c': False}]},
        {'t': '5 == 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '1', 'c': False}, {'t': '0', 'c': False}]},
        {'t': '5 != 3 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'if va else', 't': 25, 'o': 6, 'q': [
        {'t': 'if (x > 5) {...} qachon ishlaydi?', 'a': [{'t': 'x 5 dan katta bo\'lsa', 'c': True}, {'t': 'x 5 ga teng bo\'lsa', 'c': False}, {'t': 'x 5 dan kichik bo\'lsa', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'else if nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'if (x == 5) nima tekshiradi?', 'a': [{'t': 'x 5 ga tengmi', 'c': True}, {'t': 'x ga 5 ni beradi', 'c': False}, {'t': 'x 5 dan kattami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ternary operator: x > 5 ? a : b', 'a': [{'t': 'x>5 bo\'lsa a, aks holda b', 'c': True}, {'t': 'x va 5 ni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'a va b ni qo\'shadi', 'c': False}]},
    ]},
    {'n': 'switch-case', 't': 20, 'o': 7, 'q': [
        {'t': 'switch-case nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'case nima?', 'a': [{'t': 'Bir variant', 'c': True}, {'t': 'Shart', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'switch dan chiqadi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'switch da break qo\'ymasak?', 'a': [{'t': 'Keyingi case ham bajariladi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'To\'xtaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'while va do-while', 't': 25, 'o': 8, 'q': [
        {'t': 'while sikli nima uchun?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'while (true) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'do-while va while farqi?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'while tezroq', 'c': False}, {'t': 'do-while xato', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'Sikldan chiqadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Siklni qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Sikldan chiqadi', 'c': False}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'for sikli', 't': 25, 'o': 9, 'q': [
        {'t': 'for (int i=0; i<5; i++) necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for siklining 3 qismi?', 'a': [{'t': 'Boshlang\'ich, shart, o\'zgartirish', 'c': True}, {'t': 'Faqat shart', 'c': False}, {'t': 'Faqat boshlang\'ich', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for (;;) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Range-based for: for(int x : arr)', 'a': [{'t': 'arr ning har bir elementini oladi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'arr ni o\'chiradi', 'c': False}, {'t': 'arr ni saralaydi', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Massivlar', 't': 25, 'o': 10, 'q': [
        {'t': 'Massiv nima?', 'a': [{'t': 'Bir xil turdagi elementlar to\'plami', 'c': True}, {'t': 'Bitta qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'int arr[5]; nima yaratadi?', 'a': [{'t': '5 ta butun son uchun massiv', 'c': True}, {'t': '5 qiymatli massiv', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Bitta o\'zgaruvchi', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': 'int arr[] = {1,2,3,4,5}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'arr[0] nima?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Ikkinchi element', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sizeof(arr) nima qaytaradi?', 'a': [{'t': 'Massiv hajmini baytda', 'c': True}, {'t': 'Elementlar sonini', 'c': False}, {'t': 'Birinchi elementni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Funksiyalar', 't': 25, 'o': 11, 'q': [
        {'t': 'Funksiya nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'void nima?', 'a': [{'t': 'Hech narsa qaytarmaydi', 'c': True}, {'t': 'Butun son qaytaradi', 'c': False}, {'t': 'O\'nli kasr qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'return nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi va funksiyadan chiqadi', 'c': True}, {'t': 'Faqat qiymat qaytaradi', 'c': False}, {'t': 'Faqat funksiyadan chiqadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiya prototipi nima?', 'a': [{'t': 'Funksiya e\'loni', 'c': True}, {'t': 'Funksiya tanasi', 'c': False}, {'t': 'Funksiya chaqiruvi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Default parametr nima?', 'a': [{'t': 'Standart qiymatga ega parametr', 'c': True}, {'t': 'Majburiy parametr', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
    ]},
    {'n': 'Function overloading', 't': 20, 'o': 12, 'q': [
        {'t': 'Function overloading nima?', 'a': [{'t': 'Bir xil nomli, turli parametrli funksiyalar', 'c': True}, {'t': 'Funksiyani qayta yozish', 'c': False}, {'t': 'Funksiyani o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Overloading qanday farqlanadi?', 'a': [{'t': 'Parametrlar soni yoki turi bilan', 'c': True}, {'t': 'Faqat nom bilan', 'c': False}, {'t': 'Faqat qaytarish turi bilan', 'c': False}, {'t': 'Farqlanmaydi', 'c': False}]},
        {'t': 'int sum(int, int) va double sum(double, double) mumkinmi?', 'a': [{'t': 'Ha, overloading', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Faqat C da', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Overloading ning afzalligi?', 'a': [{'t': 'Bir xil nom, turli vazifalar', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'C da function overloading bormi?', 'a': [{'t': 'Yo\'q, faqat C++ da', 'c': True}, {'t': 'Ha, C da ham bor', 'c': False}, {'t': 'Faqat C da bor', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Pointerlar', 't': 30, 'o': 13, 'q': [
        {'t': 'Pointer nima?', 'a': [{'t': 'Xotira manzilini saqlovchi o\'zgaruvchi', 'c': True}, {'t': 'Oddiy o\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': '& operatori nima?', 'a': [{'t': 'Manzil operatori', 'c': True}, {'t': 'Qiymat operatori', 'c': False}, {'t': 'Ko\'paytirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '* operatori nima?', 'a': [{'t': 'Dereference (qiymatni olish)', 'c': True}, {'t': 'Manzil operatori', 'c': False}, {'t': 'Faqat ko\'paytirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int *p; nima yaratadi?', 'a': [{'t': 'int turidagi pointer', 'c': True}, {'t': 'int o\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Massiv', 'c': False}]},
        {'t': 'p = &x; nima qiladi?', 'a': [{'t': 'p ga x ning manzilini beradi', 'c': True}, {'t': 'p ga x ning qiymatini beradi', 'c': False}, {'t': 'x ga p ni beradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'nullptr nima?', 'a': [{'t': 'Bo\'sh pointer', 'c': True}, {'t': '0 qiymati', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
    ]},
    {'n': 'Referenclar', 't': 25, 'o': 14, 'q': [
        {'t': 'Reference nima?', 'a': [{'t': 'O\'zgaruvchining boshqa nomi', 'c': True}, {'t': 'Pointer', 'c': False}, {'t': 'Nusxa', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int &ref = x; nima?', 'a': [{'t': 'ref x ning referensi', 'c': True}, {'t': 'ref x ning nusxasi', 'c': False}, {'t': 'ref x ning pointeri', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Reference va pointer farqi?', 'a': [{'t': 'Reference o\'zgartirib bo\'lmaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Pointer o\'zgartirib bo\'lmaydi', 'c': False}, {'t': 'Reference tezroq', 'c': False}]},
        {'t': 'Reference null bo\'lishi mumkinmi?', 'a': [{'t': 'Yo\'q, har doim biror narsaga bog\'langan', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Funksiyaga reference uzatish afzalligi?', 'a': [{'t': 'Nusxa yaratilmaydi, tezroq', 'c': True}, {'t': 'Sekinroq', 'c': False}, {'t': 'Ko\'proq xotira', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
    ]},
    {'n': 'Dinamik xotira', 't': 30, 'o': 15, 'q': [
        {'t': 'new operatori nima qiladi?', 'a': [{'t': 'Dinamik xotira ajratadi', 'c': True}, {'t': 'Xotirani bo\'shatadi', 'c': False}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'delete nima qiladi?', 'a': [{'t': 'Xotirani bo\'shatadi', 'c': True}, {'t': 'Xotira ajratadi', 'c': False}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int *p = new int; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'delete[] nima uchun?', 'a': [{'t': 'Massivni bo\'shatish', 'c': True}, {'t': 'Bitta o\'zgaruvchini bo\'shatish', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Memory leak nima?', 'a': [{'t': 'Xotira oqishi (delete qilinmagan)', 'c': True}, {'t': 'Xotira tugashi', 'c': False}, {'t': 'Xotira xatosi', 'c': False}, {'t': 'Oddiy xato', 'c': False}]},
    ]},
    {'n': 'Klasslar - Asoslar', 't': 30, 'o': 16, 'q': [
        {'t': 'Klass nima?', 'a': [{'t': 'Obyektlar uchun shablon', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Obyekt nima?', 'a': [{'t': 'Klassdan yaratilgan nusxa', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'class Student {...}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Student s1; nima qiladi?', 'a': [{'t': 'Student obyekti yaratadi', 'c': True}, {'t': 'Student klassini yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya chaqiradi', 'c': False}]},
        {'t': 'Klass a\'zosiga qanday murojaat?', 'a': [{'t': 's1.name', 'c': True}, {'t': 's1->name', 'c': False}, {'t': 's1[name]', 'c': False}, {'t': 's1(name)', 'c': False}]},
        {'t': 'C++ da struct va class farqi?', 'a': [{'t': 'struct default public, class private', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'struct tezroq', 'c': False}, {'t': 'class kattaroq', 'c': False}]},
    ]},
    {'n': 'Konstruktor va Destruktor', 't': 30, 'o': 17, 'q': [
        {'t': 'Konstruktor nima?', 'a': [{'t': 'Obyekt yaratilganda chaqiriladigan funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Destruktor', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Konstruktor nomi qanday?', 'a': [{'t': 'Klass nomi bilan bir xil', 'c': True}, {'t': 'Istalgan nom', 'c': False}, {'t': 'constructor', 'c': False}, {'t': 'init', 'c': False}]},
        {'t': 'Destruktor nima?', 'a': [{'t': 'Obyekt yo\'q qilinganda chaqiriladi', 'c': True}, {'t': 'Obyekt yaratilganda chaqiriladi', 'c': False}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Destruktor belgisi?', 'a': [{'t': '~ClassName()', 'c': True}, {'t': 'delete ClassName()', 'c': False}, {'t': 'destroy ClassName()', 'c': False}, {'t': 'ClassName~()', 'c': False}]},
        {'t': 'Default konstruktor nima?', 'a': [{'t': 'Parametrsiz konstruktor', 'c': True}, {'t': 'Parametrli konstruktor', 'c': False}, {'t': 'Destruktor', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Konstruktor overloading mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Access modifiers', 't': 25, 'o': 18, 'q': [
        {'t': 'public nima?', 'a': [{'t': 'Hamma joydan kirish mumkin', 'c': True}, {'t': 'Faqat klass ichidan', 'c': False}, {'t': 'Faqat meros oluvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'private nima?', 'a': [{'t': 'Faqat klass ichidan kirish mumkin', 'c': True}, {'t': 'Hamma joydan kirish mumkin', 'c': False}, {'t': 'Faqat meros oluvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'protected nima?', 'a': [{'t': 'Klass va meros oluvchilar', 'c': True}, {'t': 'Faqat klass ichidan', 'c': False}, {'t': 'Hamma joydan', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Class da default access modifier?', 'a': [{'t': 'private', 'c': True}, {'t': 'public', 'c': False}, {'t': 'protected', 'c': False}, {'t': 'Yo\'q', 'c': False}]},
        {'t': 'Struct da default access modifier?', 'a': [{'t': 'public', 'c': True}, {'t': 'private', 'c': False}, {'t': 'protected', 'c': False}, {'t': 'Yo\'q', 'c': False}]},
    ]},
    {'n': 'Inheritance (Meros)', 't': 30, 'o': 19, 'q': [
        {'t': 'Inheritance nima?', 'a': [{'t': 'Bir klassdan boshqa klass yaratish', 'c': True}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'class Child : public Parent nima?', 'a': [{'t': 'Child Parent dan meros oladi', 'c': True}, {'t': 'Parent Child dan meros oladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Base class nima?', 'a': [{'t': 'Asosiy klass (meros beriladigan)', 'c': True}, {'t': 'Yangi klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Derived class nima?', 'a': [{'t': 'Meros oluvchi klass', 'c': True}, {'t': 'Asosiy klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'C++ da multiple inheritance bormi?', 'a': [{'t': 'Ha, bor', 'c': True}, {'t': 'Yo\'q, yo\'q', 'c': False}, {'t': 'Faqat Java da', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Inheritance ning afzalligi?', 'a': [{'t': 'Kodni qayta ishlatish', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
    ]},
    {'n': 'Polymorphism', 't': 30, 'o': 20, 'q': [
        {'t': 'Polymorphism nima?', 'a': [{'t': 'Bir xil nom, turli xil bajarilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Ma\'lumotlarni yashirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'Virtual funksiya nima?', 'a': [{'t': 'Child da qayta yozilishi mumkin bo\'lgan funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Static funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'virtual kalit so\'zi nima uchun?', 'a': [{'t': 'Polymorphism uchun', 'c': True}, {'t': 'Meros olish uchun', 'c': False}, {'t': 'Xotira tejash uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Pure virtual funksiya nima?', 'a': [{'t': 'virtual void func() = 0;', 'c': True}, {'t': 'virtual void func();', 'c': False}, {'t': 'void func() = 0;', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Abstract class nima?', 'a': [{'t': 'Pure virtual funksiyaga ega klass', 'c': True}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Final klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Abstract class dan obyekt yaratish mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Encapsulation', 't': 25, 'o': 21, 'q': [
        {'t': 'Encapsulation nima?', 'a': [{'t': 'Ma\'lumotlarni yashirish va himoya qilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Polimorfizm', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'Getter metod nima uchun?', 'a': [{'t': 'Private atributni o\'qish', 'c': True}, {'t': 'Private atributni o\'zgartirish', 'c': False}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Setter metod nima uchun?', 'a': [{'t': 'Private atributni o\'zgartirish', 'c': True}, {'t': 'Private atributni o\'qish', 'c': False}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Encapsulation ning afzalligi?', 'a': [{'t': 'Ma\'lumotlarni himoya qilish', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'Private atributga tashqaridan murojaat mumkinmi?', 'a': [{'t': 'Yo\'q, faqat getter/setter orqali', 'c': True}, {'t': 'Ha, erkin murojaat mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Operator overloading', 't': 30, 'o': 22, 'q': [
        {'t': 'Operator overloading nima?', 'a': [{'t': 'Operatorlarga yangi ma\'no berish', 'c': True}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Klass yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'operator+ nima?', 'a': [{'t': '+ operatorini qayta aniqlash', 'c': True}, {'t': 'Qo\'shish funksiyasi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Oddiy funksiya', 'c': False}]},
        {'t': 'Qaysi operatorlarni overload qilish mumkin?', 'a': [{'t': 'Ko\'pchilik operatorlar', 'c': True}, {'t': 'Hech qaysi', 'c': False}, {'t': 'Faqat +', 'c': False}, {'t': 'Faqat -', 'c': False}]},
        {'t': 'Qaysi operatorni overload qilib bo\'lmaydi?', 'a': [{'t': ':: (scope resolution)', 'c': True}, {'t': '+', 'c': False}, {'t': '-', 'c': False}, {'t': '*', 'c': False}]},
        {'t': 'Operator overloading ning afzalligi?', 'a': [{'t': 'Kodni tushunarli qiladi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
    ]},
    {'n': 'Friend funksiya', 't': 25, 'o': 23, 'q': [
        {'t': 'Friend funksiya nima?', 'a': [{'t': 'Klass private a\'zolariga kirish huquqi bor', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Klass metodi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'friend kalit so\'zi nima uchun?', 'a': [{'t': 'Friend funksiya e\'lon qilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Polimorfizm', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Friend funksiya klass a\'zosimi?', 'a': [{'t': 'Yo\'q, lekin private ga kirish mumkin', 'c': True}, {'t': 'Ha, klass a\'zosi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Friend class nima?', 'a': [{'t': 'Boshqa klass private a\'zolariga kirish mumkin', 'c': True}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Meros oluvchi klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Friend qachon ishlatiladi?', 'a': [{'t': 'Operator overloading, maxsus kirish kerak bo\'lsa', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
    ]},
    {'n': 'Static a\'zolar', 't': 25, 'o': 24, 'q': [
        {'t': 'Static a\'zo nima?', 'a': [{'t': 'Barcha obyektlar uchun umumiy', 'c': True}, {'t': 'Har bir obyektga xos', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Static funksiya nima?', 'a': [{'t': 'Obyektsiz chaqirish mumkin', 'c': True}, {'t': 'Faqat obyekt orqali', 'c': False}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Static funksiya non-static a\'zoga kirishi mumkinmi?', 'a': [{'t': 'Yo\'q, faqat static a\'zolarga', 'c': True}, {'t': 'Ha, kirishi mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Static o\'zgaruvchi qanday chaqiriladi?', 'a': [{'t': 'ClassName::variable', 'c': True}, {'t': 'object.variable', 'c': False}, {'t': 'variable()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Static a\'zoning afzalligi?', 'a': [{'t': 'Xotirani tejaydi, umumiy ma\'lumot', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Templates', 't': 30, 'o': 25, 'q': [
        {'t': 'Template nima?', 'a': [{'t': 'Umumiy dasturlash uchun shablon', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'template <typename T> nima?', 'a': [{'t': 'T - har qanday tur bo\'lishi mumkin', 'c': True}, {'t': 'T - faqat int', 'c': False}, {'t': 'T - faqat string', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Function template nima?', 'a': [{'t': 'Har xil turlar uchun funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Class template nima?', 'a': [{'t': 'Har xil turlar uchun klass', 'c': True}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Template ning afzalligi?', 'a': [{'t': 'Kodni qayta ishlatish, har xil turlar', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'STL nima?', 'a': [{'t': 'Standard Template Library', 'c': True}, {'t': 'String Template Library', 'c': False}, {'t': 'Static Template Library', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'STL - Vector', 't': 30, 'o': 26, 'q': [
        {'t': 'vector nima?', 'a': [{'t': 'Dinamik massiv', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'vector<int> v; nima yaratadi?', 'a': [{'t': 'Bo\'sh int vektori', 'c': True}, {'t': 'int massivi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'v.push_back(5) nima qiladi?', 'a': [{'t': 'Oxiriga 5 qo\'shadi', 'c': True}, {'t': 'Boshiga 5 qo\'shadi', 'c': False}, {'t': '5 ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v.pop_back() nima qiladi?', 'a': [{'t': 'Oxirgi elementni o\'chiradi', 'c': True}, {'t': 'Birinchi elementni o\'chiradi', 'c': False}, {'t': 'Element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v.size() nima qaytaradi?', 'a': [{'t': 'Elementlar sonini', 'c': True}, {'t': 'Hajmni baytda', 'c': False}, {'t': 'Birinchi elementni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v[i] va v.at(i) farqi?', 'a': [{'t': 'at() chegara tekshiradi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'v[i] tezroq', 'c': False}, {'t': 'at() xato', 'c': False}]},
    ]},
    {'n': 'STL - String', 't': 25, 'o': 27, 'q': [
        {'t': 'string nima?', 'a': [{'t': 'STL matn klassi', 'c': True}, {'t': 'char massivi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'string s = "Hello"; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 's1 + s2 nima qiladi?', 'a': [{'t': 'Satrlarni birlashtiradi', 'c': True}, {'t': 'Satrlarni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 's.length() nima qaytaradi?', 'a': [{'t': 'Satr uzunligini', 'c': True}, {'t': 'Satr hajmini', 'c': False}, {'t': 'Birinchi belgini', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.substr(0, 3) nima qiladi?', 'a': [{'t': '0 dan 3 ta belgi oladi', 'c': True}, {'t': '0 dan 3 gacha o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'STL - Map', 't': 30, 'o': 28, 'q': [
        {'t': 'map nima?', 'a': [{'t': 'Kalit-qiymat juftliklari', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'map<string, int> m; nima yaratadi?', 'a': [{'t': 'String kalitli, int qiymatli map', 'c': True}, {'t': 'int massivi', 'c': False}, {'t': 'string massivi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'm["key"] = 10; nima qiladi?', 'a': [{'t': '"key" ga 10 qiymatini beradi', 'c': True}, {'t': '"key" ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'm.find("key") nima qiladi?', 'a': [{'t': '"key" ni qidiradi', 'c': True}, {'t': '"key" ni o\'chiradi', 'c': False}, {'t': '"key" ga qiymat beradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'm.size() nima qaytaradi?', 'a': [{'t': 'Juftliklar sonini', 'c': True}, {'t': 'Hajmni baytda', 'c': False}, {'t': 'Birinchi elementni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Exception handling', 't': 30, 'o': 29, 'q': [
        {'t': 'try-catch nima uchun?', 'a': [{'t': 'Xatolarni ushlash va boshqarish', 'c': True}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Sikl yaratish', 'c': False}, {'t': 'Ma\'lumot saqlash', 'c': False}]},
        {'t': 'throw nima qiladi?', 'a': [{'t': 'Xato chiqaradi', 'c': True}, {'t': 'Xatoni ushlaydi', 'c': False}, {'t': 'Funksiya yaratadi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'catch (exception &e) nima?', 'a': [{'t': 'Xatoni ushlaydi', 'c': True}, {'t': 'Xato chiqaradi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'try blokida xato bo\'lsa?', 'a': [{'t': 'catch bloki ishlaydi', 'c': True}, {'t': 'Dastur to\'xtaydi', 'c': False}, {'t': 'Xato e\'tiborga olinmaydi', 'c': False}, {'t': 'Qayta urinadi', 'c': False}]},
        {'t': 'catch (...) nima?', 'a': [{'t': 'Har qanday xatoni ushlaydi', 'c': True}, {'t': 'Faqat bitta xato turini', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Fayl bilan ishlash', 't': 30, 'o': 30, 'q': [
        {'t': 'fstream nima?', 'a': [{'t': 'Fayl oqimi klassi', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'ifstream nima uchun?', 'a': [{'t': 'Fayldan o\'qish', 'c': True}, {'t': 'Faylga yozish', 'c': False}, {'t': 'Faylni o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'ofstream nima uchun?', 'a': [{'t': 'Faylga yozish', 'c': True}, {'t': 'Fayldan o\'qish', 'c': False}, {'t': 'Faylni o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'file.open("file.txt") nima qiladi?', 'a': [{'t': 'Faylni ochadi', 'c': True}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'file.close() nima qiladi?', 'a': [{'t': 'Faylni yopadi', 'c': True}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'file.is_open() nima tekshiradi?', 'a': [{'t': 'Fayl ochiqmi', 'c': True}, {'t': 'Fayl mavjudmi', 'c': False}, {'t': 'Fayl bo\'shmi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🔷 C++ DASTURLASH - 30 TA MAVZU")
    print("=" * 80)
    subject = get_or_create_cpp()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T)
    total = sum(len(t['q']) for t in T)
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! {len(T)} ta mavzu, {total} ta test qo'shildi!")
    print(f"📝 To'g'ri javoblar tasodifiy joylashtirildi")
    print("=" * 80)
