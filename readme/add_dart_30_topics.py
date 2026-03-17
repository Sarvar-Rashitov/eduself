"""
DART DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_dart():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Dart', defaults={'category': cat, 'description': 'Dart dasturlash tili - Flutter uchun zamonaviy dasturlash', 'icon': 'bi-phone-fill', 'order': 8, 'is_active': True})
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
    {'n': 'Dart dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Dart dasturlash tili qachon yaratilgan?', 'a': [{'t': '2011 yilda', 'c': True}, {'t': '2015 yilda', 'c': False}, {'t': '2008 yilda', 'c': False}, {'t': '2020 yilda', 'c': False}]},
        {'t': 'Dart tilini kim yaratgan?', 'a': [{'t': 'Microsoft', 'c': False}, {'t': 'Google kompaniyasi', 'c': True}, {'t': 'Apple', 'c': False}, {'t': 'Facebook', 'c': False}]},
        {'t': 'Dart ning asosiy qo\'llanilish sohasi?', 'a': [{'t': 'Faqat web dasturlash', 'c': False}, {'t': 'Faqat server dasturlash', 'c': False}, {'t': 'Flutter mobil ilovalar', 'c': True}, {'t': 'O\'yin dasturlash', 'c': False}]},
        {'t': 'Dart fayl kengaytmasi?', 'a': [{'t': '.dt', 'c': False}, {'t': '.dart', 'c': True}, {'t': '.d', 'c': False}, {'t': '.drt', 'c': False}]},
        {'t': 'Dart qanday til?', 'a': [{'t': 'Faqat dinamik tipli', 'c': False}, {'t': 'Ob\'ektga yo\'naltirilgan, statik tipli', 'c': True}, {'t': 'Faqat funktsional', 'c': False}, {'t': 'Mashina tili', 'c': False}]},
        {'t': 'Dart da garbage collection bormi?', 'a': [{'t': 'Ha, avtomatik xotira boshqaruvi bor', 'c': True}, {'t': 'Yo\'q, qo\'lda boshqarish kerak', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Dart dasturini qanday ishga tushirish mumkin?', 'a': [{'t': 'run dart filename', 'c': False}, {'t': 'dart filename.dart', 'c': True}, {'t': 'execute filename.dart', 'c': False}, {'t': 'start filename', 'c': False}]},
    ]},
    
    {'n': 'Birinchi Dart dasturi va print', 't': 15, 'o': 2, 'q': [
        {'t': 'Dart dasturining asosiy funksiyasi?', 'a': [{'t': 'function main() {}', 'c': False}, {'t': 'void main() {}', 'c': True}, {'t': 'start() {}', 'c': False}, {'t': 'begin() {}', 'c': False}]},
        {'t': 'Ekranga matn chiqarish uchun qaysi funksiya ishlatiladi?', 'a': [{'t': 'echo()', 'c': False}, {'t': 'console.log()', 'c': False}, {'t': 'print()', 'c': True}, {'t': 'write()', 'c': False}]},
        {'t': 'print("Salom"); natijasi?', 'a': [{'t': '"Salom"', 'c': False}, {'t': 'Salom', 'c': True}, {'t': 'print Salom', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Dart da qator oxirida ; belgisi majburiymi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': False}, {'t': 'Ha, majburiy', 'c': True}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'Dart da izoh qanday yoziladi?', 'a': [{'t': 'Faqat #', 'c': False}, {'t': '// yoki /* */', 'c': True}, {'t': 'Faqat <!-- -->', 'c': False}, {'t': '-- izoh', 'c': False}]},
        {'t': 'void main() { print(5 + 3); } natijasi?', 'a': [{'t': '53', 'c': False}, {'t': '5 + 3', 'c': False}, {'t': '8', 'c': True}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'O\'zgaruvchilar va var', 't': 20, 'o': 3, 'q': [
        {'t': 'Dart da o\'zgaruvchi e\'lon qilish uchun?', 'a': [{'t': 'Faqat let', 'c': False}, {'t': 'var, int, String va boshqalar', 'c': True}, {'t': 'Faqat dim', 'c': False}, {'t': 'declare', 'c': False}]},
        {'t': 'var x = 10; bu qanday tip?', 'a': [{'t': 'String', 'c': False}, {'t': 'double', 'c': False}, {'t': 'int', 'c': True}, {'t': 'var', 'c': False}]},
        {'t': 'var nomi = "Ali"; bu qanday tip?', 'a': [{'t': 'int', 'c': False}, {'t': 'String', 'c': True}, {'t': 'char', 'c': False}, {'t': 'text', 'c': False}]},
        {'t': 'O\'zgaruvchi nomida raqam bilan boshlanishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': False}, {'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Faqat 0 bilan', 'c': False}, {'t': 'Faqat 1 bilan', 'c': False}]},
        {'t': 'var x = 5; x = "text"; bu to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': False}, {'t': 'Yo\'q, xato', 'c': True}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Faqat debug rejimida', 'c': False}]},
        {'t': 'O\'zgaruvchi nomida _ belgisi ishlatilishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ha, mumkin', 'c': True}, {'t': 'Faqat boshida', 'c': False}, {'t': 'Faqat oxirida', 'c': False}]},
        {'t': 'var son = 10; print(son); natijasi?', 'a': [{'t': 'son', 'c': False}, {'t': '10', 'c': True}, {'t': 'var son', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'Ma\'lumot turlari: int, double, String', 't': 20, 'o': 4, 'q': [
        {'t': 'int x = 5; bu qanday ma\'lumot turi?', 'a': [{'t': 'Butun son', 'c': True}, {'t': 'O\'nlik son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Boolean', 'c': False}]},
        {'t': 'double y = 3.14; bu qanday ma\'lumot turi?', 'a': [{'t': 'Butun son', 'c': False}, {'t': 'O\'nlik son', 'c': True}, {'t': 'Matn', 'c': False}, {'t': 'Kasr', 'c': False}]},
        {'t': 'String matn = "Salom"; bu qanday ma\'lumot turi?', 'a': [{'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': True}, {'t': 'Belgi', 'c': False}, {'t': 'Array', 'c': False}]},
        {'t': 'int x = 5.5; bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': False}, {'t': 'Yo\'q, xato', 'c': True}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Faqat debug rejimida', 'c': False}]},
        {'t': 'String matn = \'Salom\'; bu to\'g\'rimi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Faqat " ishlatish kerak', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'int a = 10; double b = a; bu to\'g\'rimi?', 'a': [{'t': 'Ha, avtomatik konvertatsiya', 'c': False}, {'t': 'Yo\'q, aniq konvertatsiya kerak', 'c': True}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Har doim xato', 'c': False}]},
        {'t': 'String va int qo\'shish mumkinmi?', 'a': [{'t': 'Ha, avtomatik', 'c': False}, {'t': 'Yo\'q, konvertatsiya kerak', 'c': True}, {'t': 'Faqat + operatori bilan', 'c': False}, {'t': 'Har doim mumkin', 'c': False}]},
    ]},
    
    {'n': 'bool va null', 't': 15, 'o': 5, 'q': [
        {'t': 'bool tipida qanday qiymatlar bo\'ladi?', 'a': [{'t': 'true va false', 'c': True}, {'t': '0 va 1', 'c': False}, {'t': 'yes va no', 'c': False}, {'t': 'on va off', 'c': False}]},
        {'t': 'bool x = true; bu to\'g\'rimi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat false bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'null nima?', 'a': [{'t': '0 qiymati', 'c': False}, {'t': 'Qiymat yo\'qligi', 'c': True}, {'t': 'Bo\'sh string', 'c': False}, {'t': 'False', 'c': False}]},
        {'t': 'int? x = null; bu to\'g\'rimi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha, nullable tip', 'c': True}, {'t': 'Faqat String bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'int x = null; bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': False}, {'t': 'Yo\'q, xato', 'c': True}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Faqat debug rejimida', 'c': False}]},
        {'t': '? belgisi nima uchun ishlatiladi?', 'a': [{'t': 'Savol berish', 'c': False}, {'t': 'Nullable tip yaratish', 'c': True}, {'t': 'Shartli operator', 'c': False}, {'t': 'Izoh yozish', 'c': False}]},
    ]},
    
    {'n': 'Arifmetik operatorlar', 't': 20, 'o': 6, 'q': [
        {'t': '5 + 3 natijasi?', 'a': [{'t': '8', 'c': True}, {'t': '53', 'c': False}, {'t': '2', 'c': False}, {'t': '15', 'c': False}]},
        {'t': '10 - 4 natijasi?', 'a': [{'t': '14', 'c': False}, {'t': '6', 'c': True}, {'t': '40', 'c': False}, {'t': '2.5', 'c': False}]},
        {'t': '6 * 7 natijasi?', 'a': [{'t': '13', 'c': False}, {'t': '42', 'c': True}, {'t': '67', 'c': False}, {'t': '1', 'c': False}]},
        {'t': '20 / 4 natijasi qanday tip?', 'a': [{'t': 'int', 'c': False}, {'t': 'double', 'c': True}, {'t': 'String', 'c': False}, {'t': 'num', 'c': False}]},
        {'t': '20 ~/ 3 natijasi? (butun bo\'lish)', 'a': [{'t': '6.67', 'c': False}, {'t': '6', 'c': True}, {'t': '7', 'c': False}, {'t': '2', 'c': False}]},
        {'t': '17 % 5 natijasi? (qoldiq)', 'a': [{'t': '3', 'c': False}, {'t': '2', 'c': True}, {'t': '12', 'c': False}, {'t': '3.4', 'c': False}]},
        {'t': 'x++ operatori nima qiladi?', 'a': [{'t': 'x ni 2 ga ko\'paytiradi', 'c': False}, {'t': 'x ni 1 ga oshiradi', 'c': True}, {'t': 'x ni 1 ga kamaytiradi', 'c': False}, {'t': 'x ni o\'chiradi', 'c': False}]},
        {'t': '--y operatori nima qiladi?', 'a': [{'t': 'y ni 1 ga oshiradi', 'c': False}, {'t': 'y ni 1 ga kamaytiradi', 'c': True}, {'t': 'y ni 0 ga tenglashtiradi', 'c': False}, {'t': 'y ni o\'chiradi', 'c': False}]},
    ]},
    
    {'n': 'Taqqoslash operatorlari', 't': 15, 'o': 7, 'q': [
        {'t': '5 == 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '10', 'c': False}, {'t': 'null', 'c': False}]},
        {'t': '5 != 3 natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '2', 'c': False}, {'t': 'null', 'c': False}]},
        {'t': '10 > 5 natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '5', 'c': False}, {'t': '15', 'c': False}]},
        {'t': '3 < 7 natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '4', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '5 >= 5 natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '0', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '4 <= 3 natijasi?', 'a': [{'t': 'true', 'c': False}, {'t': 'false', 'c': True}, {'t': '1', 'c': False}, {'t': '7', 'c': False}]},
    ]},
    
    {'n': 'Mantiqiy operatorlar', 't': 15, 'o': 8, 'q': [
        {'t': 'true && true natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': 'null', 'c': False}, {'t': 'xato', 'c': False}]},
        {'t': 'true && false natijasi?', 'a': [{'t': 'true', 'c': False}, {'t': 'false', 'c': True}, {'t': 'null', 'c': False}, {'t': 'xato', 'c': False}]},
        {'t': 'false || true natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': 'null', 'c': False}, {'t': 'xato', 'c': False}]},
        {'t': 'false || false natijasi?', 'a': [{'t': 'true', 'c': False}, {'t': 'false', 'c': True}, {'t': 'null', 'c': False}, {'t': 'xato', 'c': False}]},
        {'t': '!true natijasi?', 'a': [{'t': 'true', 'c': False}, {'t': 'false', 'c': True}, {'t': 'null', 'c': False}, {'t': '1', 'c': False}]},
        {'t': '!false natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': 'null', 'c': False}, {'t': '0', 'c': False}]},
    ]},
    
    {'n': 'if shartli operatori', 't': 20, 'o': 9, 'q': [
        {'t': 'if operatori sintaksisi?', 'a': [{'t': 'if (shart) {}', 'c': True}, {'t': 'if shart then', 'c': False}, {'t': 'if [shart]', 'c': False}, {'t': 'if: shart', 'c': False}]},
        {'t': 'if (5 > 3) { print("Ha"); } natijasi?', 'a': [{'t': 'Hech narsa', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'false', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'if (false) { print("A"); } natijasi?', 'a': [{'t': 'A', 'c': False}, {'t': 'Hech narsa chiqmaydi', 'c': True}, {'t': 'false', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'if da {} qavslar majburiymi?', 'a': [{'t': 'Yo\'q, lekin tavsiya etiladi', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Faqat bir qator bo\'lsa', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'if (x == 5) bu to\'g\'ri sintaksismi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat = ishlatish kerak', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'if ichida if ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha, nested if', 'c': True}, {'t': 'Faqat 2 marta', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'else va else if', 't': 20, 'o': 10, 'q': [
        {'t': 'else qachon ishlaydi?', 'a': [{'t': 'if shart false bo\'lsa', 'c': True}, {'t': 'if shart true bo\'lsa', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'if (false) {print("A");} else {print("B");} natijasi?', 'a': [{'t': 'A', 'c': False}, {'t': 'B', 'c': True}, {'t': 'AB', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'else if nima uchun ishlatiladi?', 'a': [{'t': 'Birinchi shart false bo\'lsa, boshqa shartni tekshirish', 'c': True}, {'t': 'Ikki shartni bir vaqtda tekshirish', 'c': False}, {'t': 'Faqat dekoratsiya uchun', 'c': False}, {'t': 'Xato oldini olish', 'c': False}]},
        {'t': 'Nechta else if bo\'lishi mumkin?', 'a': [{'t': 'Faqat 1 ta', 'c': False}, {'t': 'Cheksiz', 'c': True}, {'t': 'Maksimum 5 ta', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}]},
        {'t': 'if-else if-else da nechta else bo\'lishi mumkin?', 'a': [{'t': 'Faqat 1 ta', 'c': True}, {'t': 'Cheksiz', 'c': False}, {'t': '2 ta', 'c': False}, {'t': '0 yoki ko\'p', 'c': False}]},
        {'t': 'else if dan keyin else majburiymi?', 'a': [{'t': 'Ha', 'c': False}, {'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Har doim kerak', 'c': False}]},
    ]},
    
    {'n': 'switch-case operatori', 't': 20, 'o': 11, 'q': [
        {'t': 'switch operatori nima uchun ishlatiladi?', 'a': [{'t': 'Ko\'p shartlarni tekshirish', 'c': True}, {'t': 'Faqat 2 ta shartni tekshirish', 'c': False}, {'t': 'Loop yaratish', 'c': False}, {'t': 'Funksiya chaqirish', 'c': False}]},
        {'t': 'switch da default nima?', 'a': [{'t': 'Hech bir case mos kelmasa ishlaydigan qism', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'case oxirida break kerakmi?', 'a': [{'t': 'Ha, odatda kerak', 'c': True}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Faqat oxirgi case da', 'c': False}, {'t': 'Faqat birinchi case da', 'c': False}]},
        {'t': 'switch (x) { case 1: print("Bir"); break; } bu to\'g\'rimi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat default bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'switch da String ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat int', 'c': False}, {'t': 'Faqat bool', 'c': False}]},
        {'t': 'default majburiymi?', 'a': [{'t': 'Ha', 'c': False}, {'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Har doim kerak', 'c': False}, {'t': 'Faqat String bilan', 'c': False}]},
        {'t': 'switch ichida if ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat case ichida', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'for loop (takrorlanish)', 't': 20, 'o': 12, 'q': [
        {'t': 'for loop sintaksisi?', 'a': [{'t': 'for (boshlang\'ich; shart; o\'zgarish) {}', 'c': True}, {'t': 'for (shart) {}', 'c': False}, {'t': 'for [i in range]', 'c': False}, {'t': 'for: i to 10', 'c': False}]},
        {'t': 'for (int i = 0; i < 5; i++) {} necha marta ishlaydi?', 'a': [{'t': '4 marta', 'c': False}, {'t': '5 marta', 'c': True}, {'t': '6 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'for (int i = 1; i <= 10; i++) {} necha marta ishlaydi?', 'a': [{'t': '9 marta', 'c': False}, {'t': '10 marta', 'c': True}, {'t': '11 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'i++ nima qiladi?', 'a': [{'t': 'i ni 1 ga oshiradi', 'c': True}, {'t': 'i ni 1 ga kamaytiradi', 'c': False}, {'t': 'i ni 2 ga ko\'paytiradi', 'c': False}, {'t': 'i ni o\'chiradi', 'c': False}]},
        {'t': 'for loop ichida break nima qiladi?', 'a': [{'t': 'Loop dan chiqadi', 'c': True}, {'t': 'Loop ni davom ettiradi', 'c': False}, {'t': 'Loop ni qayta boshlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'for loop ichida continue nima qiladi?', 'a': [{'t': 'Loop dan chiqadi', 'c': False}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Loop ni to\'xtatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'for (int i = 0; i < 3; i++) { print(i); } natijasi?', 'a': [{'t': '0 1 2', 'c': True}, {'t': '1 2 3', 'c': False}, {'t': '0 1 2 3', 'c': False}, {'t': '1 2', 'c': False}]},
    ]},
    
    {'n': 'while loop', 't': 15, 'o': 13, 'q': [
        {'t': 'while loop sintaksisi?', 'a': [{'t': 'while (shart) {}', 'c': True}, {'t': 'while [shart]', 'c': False}, {'t': 'while: shart', 'c': False}, {'t': 'while shart do', 'c': False}]},
        {'t': 'while (true) {} nima qiladi?', 'a': [{'t': 'Cheksiz loop', 'c': True}, {'t': '1 marta ishlaydi', 'c': False}, {'t': 'Hech qachon ishlamaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'while (false) {} necha marta ishlaydi?', 'a': [{'t': '0 marta', 'c': True}, {'t': '1 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'int i = 0; while (i < 3) { print(i); i++; } natijasi?', 'a': [{'t': '0 1 2', 'c': True}, {'t': '1 2 3', 'c': False}, {'t': '0 1 2 3', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'while da break ishlatish mumkinmi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat for da', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'while da continue ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat do-while da', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'do-while loop', 't': 15, 'o': 14, 'q': [
        {'t': 'do-while sintaksisi?', 'a': [{'t': 'do {} while (shart);', 'c': True}, {'t': 'while (shart) do {}', 'c': False}, {'t': 'do while (shart) {}', 'c': False}, {'t': 'while do (shart) {}', 'c': False}]},
        {'t': 'do-while va while orasidagi farq?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'while kamida 1 marta ishlaydi', 'c': False}, {'t': 'do-while tezroq', 'c': False}]},
        {'t': 'do { print("A"); } while (false); natijasi?', 'a': [{'t': 'A (1 marta)', 'c': True}, {'t': 'Hech narsa', 'c': False}, {'t': 'Cheksiz A', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'do-while oxirida ; kerakmi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Ixtiyoriy', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}]},
        {'t': 'do-while da break ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': False}, {'t': 'Ha', 'c': True}, {'t': 'Faqat while da', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'List (ro\'yxat)', 't': 25, 'o': 15, 'q': [
        {'t': 'List qanday e\'lon qilinadi?', 'a': [{'t': 'List<int> sonlar = [1, 2, 3];', 'c': True}, {'t': 'Array sonlar = [1, 2, 3];', 'c': False}, {'t': 'int[] sonlar = [1, 2, 3];', 'c': False}, {'t': 'list sonlar = [1, 2, 3];', 'c': False}]},
        {'t': 'var list = [1, 2, 3]; bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat List<int> bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'List elementiga qanday murojaat qilinadi?', 'a': [{'t': 'list[0]', 'c': True}, {'t': 'list(0)', 'c': False}, {'t': 'list.0', 'c': False}, {'t': 'list{0}', 'c': False}]},
        {'t': 'List ga element qo\'shish?', 'a': [{'t': 'list.add(element)', 'c': True}, {'t': 'list.push(element)', 'c': False}, {'t': 'list.insert(element)', 'c': False}, {'t': 'list += element', 'c': False}]},
        {'t': 'List dan element o\'chirish?', 'a': [{'t': 'list.remove(element)', 'c': True}, {'t': 'list.delete(element)', 'c': False}, {'t': 'list.pop(element)', 'c': False}, {'t': 'list -= element', 'c': False}]},
        {'t': 'List uzunligini olish?', 'a': [{'t': 'list.length', 'c': True}, {'t': 'list.size', 'c': False}, {'t': 'list.count', 'c': False}, {'t': 'list.len()', 'c': False}]},
        {'t': 'Bo\'sh list yaratish?', 'a': [{'t': 'var list = [];', 'c': True}, {'t': 'var list = List();', 'c': False}, {'t': 'var list = new List();', 'c': False}, {'t': 'var list;', 'c': False}]},
        {'t': 'List da birinchi element indeksi?', 'a': [{'t': '0', 'c': True}, {'t': '1', 'c': False}, {'t': '-1', 'c': False}, {'t': 'first', 'c': False}]},
    ]},
    
    {'n': 'Set (to\'plam)', 't': 20, 'o': 16, 'q': [
        {'t': 'Set nima?', 'a': [{'t': 'Takrorlanmaydigan elementlar to\'plami', 'c': True}, {'t': 'Oddiy ro\'yxat', 'c': False}, {'t': 'Kalit-qiymat juftligi', 'c': False}, {'t': 'String', 'c': False}]},
        {'t': 'Set qanday yaratiladi?', 'a': [{'t': 'var set = {1, 2, 3};', 'c': True}, {'t': 'var set = [1, 2, 3];', 'c': False}, {'t': 'var set = (1, 2, 3);', 'c': False}, {'t': 'var set = <1, 2, 3>;', 'c': False}]},
        {'t': 'Set<int> sonlar = {1, 2, 2, 3}; nechta element?', 'a': [{'t': '3 ta (takrorlanmas)', 'c': True}, {'t': '4 ta', 'c': False}, {'t': '2 ta', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Set ga element qo\'shish?', 'a': [{'t': 'set.add(element)', 'c': True}, {'t': 'set.push(element)', 'c': False}, {'t': 'set.insert(element)', 'c': False}, {'t': 'set += element', 'c': False}]},
        {'t': 'Set dan element o\'chirish?', 'a': [{'t': 'set.remove(element)', 'c': True}, {'t': 'set.delete(element)', 'c': False}, {'t': 'set.pop(element)', 'c': False}, {'t': 'set -= element', 'c': False}]},
        {'t': 'Set da indeks bilan murojaat mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha', 'c': False}, {'t': 'Faqat birinchi elementga', 'c': False}, {'t': 'Faqat oxirgi elementga', 'c': False}]},
        {'t': 'Bo\'sh Set yaratish?', 'a': [{'t': 'var set = <int>{};', 'c': True}, {'t': 'var set = {};', 'c': False}, {'t': 'var set = [];', 'c': False}, {'t': 'var set = Set();', 'c': False}]},
    ]},
    
    {'n': 'Map (lug\'at)', 't': 25, 'o': 17, 'q': [
        {'t': 'Map nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Oddiy ro\'yxat', 'c': False}, {'t': 'Takrorlanmaydigan to\'plam', 'c': False}, {'t': 'String', 'c': False}]},
        {'t': 'Map qanday yaratiladi?', 'a': [{'t': 'var map = {"kalit": "qiymat"};', 'c': True}, {'t': 'var map = ["kalit", "qiymat"];', 'c': False}, {'t': 'var map = ("kalit": "qiymat");', 'c': False}, {'t': 'var map = <"kalit", "qiymat">;', 'c': False}]},
        {'t': 'Map dan qiymat olish?', 'a': [{'t': 'map["kalit"]', 'c': True}, {'t': 'map.kalit', 'c': False}, {'t': 'map(kalit)', 'c': False}, {'t': 'map.get(kalit)', 'c': False}]},
        {'t': 'Map ga element qo\'shish?', 'a': [{'t': 'map["kalit"] = qiymat;', 'c': True}, {'t': 'map.add("kalit", qiymat);', 'c': False}, {'t': 'map.push("kalit", qiymat);', 'c': False}, {'t': 'map.insert("kalit", qiymat);', 'c': False}]},
        {'t': 'Map dan element o\'chirish?', 'a': [{'t': 'map.remove("kalit");', 'c': True}, {'t': 'map.delete("kalit");', 'c': False}, {'t': 'map.pop("kalit");', 'c': False}, {'t': 'delete map["kalit"];', 'c': False}]},
        {'t': 'Map uzunligini olish?', 'a': [{'t': 'map.length', 'c': True}, {'t': 'map.size', 'c': False}, {'t': 'map.count', 'c': False}, {'t': 'map.len()', 'c': False}]},
        {'t': 'Bo\'sh Map yaratish?', 'a': [{'t': 'var map = {};', 'c': True}, {'t': 'var map = [];', 'c': False}, {'t': 'var map = Map();', 'c': False}, {'t': 'var map = <>{};', 'c': False}]},
        {'t': 'Map da kalit mavjudligini tekshirish?', 'a': [{'t': 'map.containsKey("kalit")', 'c': True}, {'t': 'map.hasKey("kalit")', 'c': False}, {'t': 'map.exists("kalit")', 'c': False}, {'t': 'map.has("kalit")', 'c': False}]},
    ]},
    
    {'n': 'Funksiyalar (asosiy)', 't': 20, 'o': 18, 'q': [
        {'t': 'Funksiya qanday e\'lon qilinadi?', 'a': [{'t': 'void funksiya() {}', 'c': True}, {'t': 'function funksiya() {}', 'c': False}, {'t': 'def funksiya() {}', 'c': False}, {'t': 'func funksiya() {}', 'c': False}]},
        {'t': 'void nima degani?', 'a': [{'t': 'Funksiya hech narsa qaytarmaydi', 'c': True}, {'t': 'Funksiya int qaytaradi', 'c': False}, {'t': 'Funksiya String qaytaradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'int yig\'indi(int a, int b) { return a + b; } bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat void bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Funksiyani qanday chaqirish mumkin?', 'a': [{'t': 'funksiya();', 'c': True}, {'t': 'call funksiya();', 'c': False}, {'t': 'run funksiya();', 'c': False}, {'t': 'execute funksiya();', 'c': False}]},
        {'t': 'return nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi va funksiyadan chiqadi', 'c': True}, {'t': 'Faqat qiymat qaytaradi', 'c': False}, {'t': 'Funksiyani to\'xtatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Funksiya parametrsiz bo\'lishi mumkinmi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat void bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Funksiya ichida funksiya e\'lon qilish mumkinmi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat main da', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'Funksiya parametrlari', 't': 20, 'o': 19, 'q': [
        {'t': 'Positional parametrlar nima?', 'a': [{'t': 'Tartib bo\'yicha beriladigan parametrlar', 'c': True}, {'t': 'Nom bilan beriladigan parametrlar', 'c': False}, {'t': 'Ixtiyoriy parametrlar', 'c': False}, {'t': 'Default qiymatli parametrlar', 'c': False}]},
        {'t': 'void salom(String ism) {} - bu qanday parametr?', 'a': [{'t': 'Positional', 'c': True}, {'t': 'Named', 'c': False}, {'t': 'Optional', 'c': False}, {'t': 'Default', 'c': False}]},
        {'t': 'Named parametrlar qanday e\'lon qilinadi?', 'a': [{'t': 'void func({int? x}) {}', 'c': True}, {'t': 'void func(int x) {}', 'c': False}, {'t': 'void func([int x]) {}', 'c': False}, {'t': 'void func(int? x) {}', 'c': False}]},
        {'t': 'Named parametrlarni qanday chaqirish kerak?', 'a': [{'t': 'func(x: 5)', 'c': True}, {'t': 'func(5)', 'c': False}, {'t': 'func[x: 5]', 'c': False}, {'t': 'func{x: 5}', 'c': False}]},
        {'t': 'Optional positional parametrlar qanday?', 'a': [{'t': 'void func([int? x]) {}', 'c': True}, {'t': 'void func({int? x}) {}', 'c': False}, {'t': 'void func(int? x) {}', 'c': False}, {'t': 'void func(int x?) {}', 'c': False}]},
        {'t': 'Default qiymat qanday beriladi?', 'a': [{'t': 'void func({int x = 5}) {}', 'c': True}, {'t': 'void func(int x = 5) {}', 'c': False}, {'t': 'void func([int x = 5]) {}', 'c': False}, {'t': 'void func(int x := 5) {}', 'c': False}]},
        {'t': 'required kalit so\'zi nima uchun?', 'a': [{'t': 'Named parametrni majburiy qilish', 'c': True}, {'t': 'Positional parametrni majburiy qilish', 'c': False}, {'t': 'Default qiymat berish', 'c': False}, {'t': 'Xato oldini olish', 'c': False}]},
    ]},
    
    {'n': 'Arrow funksiyalar', 't': 15, 'o': 20, 'q': [
        {'t': 'Arrow funksiya sintaksisi?', 'a': [{'t': 'int yig\'indi(int a, int b) => a + b;', 'c': True}, {'t': 'int yig\'indi(int a, int b) -> a + b;', 'c': False}, {'t': 'int yig\'indi(int a, int b) := a + b;', 'c': False}, {'t': 'int yig\'indi(int a, int b) = a + b;', 'c': False}]},
        {'t': 'Arrow funksiya qachon ishlatiladi?', 'a': [{'t': 'Bir qatorli funksiyalar uchun', 'c': True}, {'t': 'Ko\'p qatorli funksiyalar uchun', 'c': False}, {'t': 'Faqat void funksiyalar uchun', 'c': False}, {'t': 'Faqat main funksiya uchun', 'c': False}]},
        {'t': 'void salom() => print("Salom"); bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat int bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Arrow funksiyada return kerakmi?', 'a': [{'t': 'Yo\'q, avtomatik qaytaradi', 'c': True}, {'t': 'Ha, har doim kerak', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Faqat int uchun', 'c': False}]},
        {'t': 'Arrow funksiyada {} kerakmi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha', 'c': False}, {'t': 'Ixtiyoriy', 'c': False}, {'t': 'Faqat void uchun', 'c': False}]},
        {'t': 'int kvadrat(int x) => x * x; bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat double uchun', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'String metodlari', 't': 25, 'o': 21, 'q': [
        {'t': 'String uzunligini olish?', 'a': [{'t': 'str.length', 'c': True}, {'t': 'str.size', 'c': False}, {'t': 'str.count', 'c': False}, {'t': 'str.len()', 'c': False}]},
        {'t': 'String ni katta harflarga o\'zgartirish?', 'a': [{'t': 'str.toUpperCase()', 'c': True}, {'t': 'str.upper()', 'c': False}, {'t': 'str.uppercase()', 'c': False}, {'t': 'str.toUpper()', 'c': False}]},
        {'t': 'String ni kichik harflarga o\'zgartirish?', 'a': [{'t': 'str.toLowerCase()', 'c': True}, {'t': 'str.lower()', 'c': False}, {'t': 'str.lowercase()', 'c': False}, {'t': 'str.toLower()', 'c': False}]},
        {'t': 'String da qidirish?', 'a': [{'t': 'str.contains("matn")', 'c': True}, {'t': 'str.search("matn")', 'c': False}, {'t': 'str.find("matn")', 'c': False}, {'t': 'str.has("matn")', 'c': False}]},
        {'t': 'String ni almashtirish?', 'a': [{'t': 'str.replaceAll("eski", "yangi")', 'c': True}, {'t': 'str.replace("eski", "yangi")', 'c': False}, {'t': 'str.change("eski", "yangi")', 'c': False}, {'t': 'str.swap("eski", "yangi")', 'c': False}]},
        {'t': 'String ni bo\'laklarga ajratish?', 'a': [{'t': 'str.split(" ")', 'c': True}, {'t': 'str.divide(" ")', 'c': False}, {'t': 'str.separate(" ")', 'c': False}, {'t': 'str.cut(" ")', 'c': False}]},
        {'t': 'String boshidagi va oxiridagi bo\'shliqlarni olib tashlash?', 'a': [{'t': 'str.trim()', 'c': True}, {'t': 'str.strip()', 'c': False}, {'t': 'str.clean()', 'c': False}, {'t': 'str.remove()', 'c': False}]},
        {'t': 'String qismini olish?', 'a': [{'t': 'str.substring(0, 5)', 'c': True}, {'t': 'str.substr(0, 5)', 'c': False}, {'t': 'str.slice(0, 5)', 'c': False}, {'t': 'str.cut(0, 5)', 'c': False}]},
    ]},
    
    {'n': 'Class (sinf) asoslari', 't': 25, 'o': 22, 'q': [
        {'t': 'Class qanday e\'lon qilinadi?', 'a': [{'t': 'class Odam {}', 'c': True}, {'t': 'Class Odam {}', 'c': False}, {'t': 'class odam {}', 'c': False}, {'t': 'def class Odam {}', 'c': False}]},
        {'t': 'Class dan ob\'ekt qanday yaratiladi?', 'a': [{'t': 'var odam = Odam();', 'c': True}, {'t': 'var odam = new Odam();', 'c': False}, {'t': 'var odam = Odam[];', 'c': False}, {'t': 'var odam = create Odam();', 'c': False}]},
        {'t': 'Class ichidagi o\'zgaruvchilar nima deyiladi?', 'a': [{'t': 'Xususiyatlar (properties)', 'c': True}, {'t': 'Metodlar', 'c': False}, {'t': 'Funksiyalar', 'c': False}, {'t': 'Parametrlar', 'c': False}]},
        {'t': 'Class ichidagi funksiyalar nima deyiladi?', 'a': [{'t': 'Metodlar', 'c': True}, {'t': 'Xususiyatlar', 'c': False}, {'t': 'Konstruktorlar', 'c': False}, {'t': 'Parametrlar', 'c': False}]},
        {'t': 'Constructor nima?', 'a': [{'t': 'Ob\'ekt yaratishda chaqiriladigan maxsus metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xususiyat', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Constructor qanday e\'lon qilinadi?', 'a': [{'t': 'Odam(this.ism);', 'c': True}, {'t': 'constructor Odam(this.ism);', 'c': False}, {'t': 'new Odam(this.ism);', 'c': False}, {'t': 'init Odam(this.ism);', 'c': False}]},
        {'t': 'this kalit so\'zi nima?', 'a': [{'t': 'Joriy ob\'ektga murojaat', 'c': True}, {'t': 'Yangi ob\'ekt yaratish', 'c': False}, {'t': 'Class nomi', 'c': False}, {'t': 'Metod nomi', 'c': False}]},
        {'t': 'Class xususiyatiga qanday murojaat qilinadi?', 'a': [{'t': 'odam.ism', 'c': True}, {'t': 'odam->ism', 'c': False}, {'t': 'odam::ism', 'c': False}, {'t': 'odam[ism]', 'c': False}]},
    ]},
    
    {'n': 'Class metodlari va getter/setter', 't': 20, 'o': 23, 'q': [
        {'t': 'Metod qanday chaqiriladi?', 'a': [{'t': 'odam.salom();', 'c': True}, {'t': 'odam->salom();', 'c': False}, {'t': 'odam::salom();', 'c': False}, {'t': 'odam[salom]();', 'c': False}]},
        {'t': 'Getter nima?', 'a': [{'t': 'Xususiyat qiymatini olish uchun metod', 'c': True}, {'t': 'Xususiyat qiymatini o\'zgartirish uchun metod', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Constructor', 'c': False}]},
        {'t': 'Getter qanday e\'lon qilinadi?', 'a': [{'t': 'int get yosh => _yosh;', 'c': True}, {'t': 'int getter yosh => _yosh;', 'c': False}, {'t': 'get int yosh => _yosh;', 'c': False}, {'t': 'int yosh() => _yosh;', 'c': False}]},
        {'t': 'Setter nima?', 'a': [{'t': 'Xususiyat qiymatini o\'zgartirish uchun metod', 'c': True}, {'t': 'Xususiyat qiymatini olish uchun metod', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Constructor', 'c': False}]},
        {'t': 'Setter qanday e\'lon qilinadi?', 'a': [{'t': 'set yosh(int qiymat) { _yosh = qiymat; }', 'c': True}, {'t': 'setter yosh(int qiymat) { _yosh = qiymat; }', 'c': False}, {'t': 'void yosh(int qiymat) { _yosh = qiymat; }', 'c': False}, {'t': 'int yosh = qiymat;', 'c': False}]},
        {'t': 'Private xususiyat qanday belgilanadi?', 'a': [{'t': '_ bilan boshlanadi: _ism', 'c': True}, {'t': 'private kalit so\'zi bilan', 'c': False}, {'t': '# bilan boshlanadi', 'c': False}, {'t': 'Maxsus belgi yo\'q', 'c': False}]},
        {'t': 'Getter chaqirishda () kerakmi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha', 'c': False}, {'t': 'Ixtiyoriy', 'c': False}, {'t': 'Ba\'zan', 'c': False}]},
    ]},
    
    {'n': 'Inheritance (meros olish)', 't': 20, 'o': 24, 'q': [
        {'t': 'Inheritance nima?', 'a': [{'t': 'Bir class boshqa class dan xususiyat va metodlarni meros olishi', 'c': True}, {'t': 'Yangi class yaratish', 'c': False}, {'t': 'Ob\'ekt yaratish', 'c': False}, {'t': 'Metod chaqirish', 'c': False}]},
        {'t': 'Inheritance qanday amalga oshiriladi?', 'a': [{'t': 'class Talaba extends Odam {}', 'c': True}, {'t': 'class Talaba inherits Odam {}', 'c': False}, {'t': 'class Talaba : Odam {}', 'c': False}, {'t': 'class Talaba from Odam {}', 'c': False}]},
        {'t': 'Parent class nima?', 'a': [{'t': 'Meros beriladigan class', 'c': True}, {'t': 'Meros oladigan class', 'c': False}, {'t': 'Asosiy class', 'c': False}, {'t': 'Yangi class', 'c': False}]},
        {'t': 'Child class nima?', 'a': [{'t': 'Meros oladigan class', 'c': True}, {'t': 'Meros beriladigan class', 'c': False}, {'t': 'Parent class', 'c': False}, {'t': 'Asosiy class', 'c': False}]},
        {'t': 'super kalit so\'zi nima?', 'a': [{'t': 'Parent class ga murojaat', 'c': True}, {'t': 'Child class ga murojaat', 'c': False}, {'t': 'Joriy class ga murojaat', 'c': False}, {'t': 'Yangi ob\'ekt yaratish', 'c': False}]},
        {'t': 'Dart da bir nechta class dan meros olish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat bitta', 'c': True}, {'t': 'Ha, cheksiz', 'c': False}, {'t': 'Maksimum 2 ta', 'c': False}, {'t': 'Faqat interface bilan', 'c': False}]},
        {'t': '@override nima uchun ishlatiladi?', 'a': [{'t': 'Parent class metodini qayta yozish', 'c': True}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Metodni o\'chirish', 'c': False}, {'t': 'Metodni yashirish', 'c': False}]},
    ]},
    
    {'n': 'Abstract class va interface', 't': 20, 'o': 25, 'q': [
        {'t': 'Abstract class nima?', 'a': [{'t': 'Ob\'ekt yaratib bo\'lmaydigan, faqat meros olish uchun class', 'c': True}, {'t': 'Oddiy class', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Mixin', 'c': False}]},
        {'t': 'Abstract class qanday e\'lon qilinadi?', 'a': [{'t': 'abstract class Shakl {}', 'c': True}, {'t': 'class abstract Shakl {}', 'c': False}, {'t': 'interface Shakl {}', 'c': False}, {'t': 'abstract Shakl {}', 'c': False}]},
        {'t': 'Abstract metod nima?', 'a': [{'t': 'Tanasi bo\'lmagan metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Private metod', 'c': False}, {'t': 'Static metod', 'c': False}]},
        {'t': 'Abstract class dan ob\'ekt yaratish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Faqat child class orqali', 'c': False}]},
        {'t': 'Interface qanday yaratiladi?', 'a': [{'t': 'Dart da har qanday class interface bo\'lishi mumkin', 'c': True}, {'t': 'interface kalit so\'zi bilan', 'c': False}, {'t': 'abstract interface bilan', 'c': False}, {'t': 'Maxsus sintaksis kerak', 'c': False}]},
        {'t': 'Interface qanday implement qilinadi?', 'a': [{'t': 'class A implements B {}', 'c': True}, {'t': 'class A extends B {}', 'c': False}, {'t': 'class A uses B {}', 'c': False}, {'t': 'class A from B {}', 'c': False}]},
        {'t': 'Bir nechta interface implement qilish mumkinmi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Faqat abstract class bilan', 'c': False}]},
    ]},
    
    {'n': 'Mixin', 't': 15, 'o': 26, 'q': [
        {'t': 'Mixin nima?', 'a': [{'t': 'Bir nechta class ga kod qo\'shish usuli', 'c': True}, {'t': 'Oddiy class', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Abstract class', 'c': False}]},
        {'t': 'Mixin qanday e\'lon qilinadi?', 'a': [{'t': 'mixin Uchuvchi {}', 'c': True}, {'t': 'class Uchuvchi {}', 'c': False}, {'t': 'abstract Uchuvchi {}', 'c': False}, {'t': 'interface Uchuvchi {}', 'c': False}]},
        {'t': 'Mixin qanday ishlatiladi?', 'a': [{'t': 'class Qush with Uchuvchi {}', 'c': True}, {'t': 'class Qush extends Uchuvchi {}', 'c': False}, {'t': 'class Qush implements Uchuvchi {}', 'c': False}, {'t': 'class Qush uses Uchuvchi {}', 'c': False}]},
        {'t': 'Bir nechta mixin ishlatish mumkinmi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Faqat abstract class bilan', 'c': False}]},
        {'t': 'Mixin dan ob\'ekt yaratish mumkinmi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Faqat with bilan', 'c': False}]},
        {'t': 'Mixin va inheritance farqi?', 'a': [{'t': 'Mixin da bir nechta qo\'shish mumkin', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Mixin tezroq', 'c': False}, {'t': 'Inheritance yaxshiroq', 'c': False}]},
    ]},
    
    {'n': 'Exception handling (xatolarni boshqarish)', 't': 20, 'o': 27, 'q': [
        {'t': 'Exception nima?', 'a': [{'t': 'Dastur ishlashida yuzaga keladigan xato', 'c': True}, {'t': 'Sintaksis xatosi', 'c': False}, {'t': 'Mantiqiy xato', 'c': False}, {'t': 'Kompilyatsiya xatosi', 'c': False}]},
        {'t': 'try-catch nima uchun ishlatiladi?', 'a': [{'t': 'Xatolarni ushlash va boshqarish', 'c': True}, {'t': 'Xatolarni yaratish', 'c': False}, {'t': 'Xatolarni e\'tiborsiz qoldirish', 'c': False}, {'t': 'Dasturni to\'xtatish', 'c': False}]},
        {'t': 'try-catch sintaksisi?', 'a': [{'t': 'try {} catch (e) {}', 'c': True}, {'t': 'try {} except (e) {}', 'c': False}, {'t': 'try {} error (e) {}', 'c': False}, {'t': 'try {} handle (e) {}', 'c': False}]},
        {'t': 'finally bloki nima?', 'a': [{'t': 'Har doim bajariladigan blok', 'c': True}, {'t': 'Faqat xato bo\'lsa bajariladigan blok', 'c': False}, {'t': 'Faqat xato bo\'lmasa bajariladigan blok', 'c': False}, {'t': 'Ixtiyoriy blok', 'c': False}]},
        {'t': 'throw nima qiladi?', 'a': [{'t': 'Xato tashlaydi', 'c': True}, {'t': 'Xatoni ushlaydi', 'c': False}, {'t': 'Xatoni bartaraf qiladi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}]},
        {'t': 'on kalit so\'zi nima uchun?', 'a': [{'t': 'Muayyan xato turini ushlash', 'c': True}, {'t': 'Xato yaratish', 'c': False}, {'t': 'Xatoni e\'tiborsiz qoldirish', 'c': False}, {'t': 'Dasturni davom ettirish', 'c': False}]},
        {'t': 'try {} on FormatException {} catch (e) {} bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat on yoki catch', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},
    
    {'n': 'Async va Future', 't': 25, 'o': 28, 'q': [
        {'t': 'Async nima?', 'a': [{'t': 'Asinxron dasturlash - kutmasdan ishlash', 'c': True}, {'t': 'Sinxron dasturlash', 'c': False}, {'t': 'Parallel dasturlash', 'c': False}, {'t': 'Ketma-ket dasturlash', 'c': False}]},
        {'t': 'Future nima?', 'a': [{'t': 'Kelajakda qiymat qaytaradigan ob\'ekt', 'c': True}, {'t': 'O\'tmishdagi qiymat', 'c': False}, {'t': 'Hozirgi qiymat', 'c': False}, {'t': 'Doimiy qiymat', 'c': False}]},
        {'t': 'async kalit so\'zi qayerda ishlatiladi?', 'a': [{'t': 'Funksiya e\'lonida', 'c': True}, {'t': 'O\'zgaruvchi e\'lonida', 'c': False}, {'t': 'Class e\'lonida', 'c': False}, {'t': 'Loop da', 'c': False}]},
        {'t': 'await nima qiladi?', 'a': [{'t': 'Future natijasini kutadi', 'c': True}, {'t': 'Darhol natija beradi', 'c': False}, {'t': 'Xato tashlaydi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}]},
        {'t': 'await qayerda ishlatiladi?', 'a': [{'t': 'Faqat async funksiya ichida', 'c': True}, {'t': 'Har qanday joyda', 'c': False}, {'t': 'Faqat main da', 'c': False}, {'t': 'Faqat class ichida', 'c': False}]},
        {'t': 'Future<int> func() async { return 5; } bu to\'g\'rimi?', 'a': [{'t': 'Ha', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat void bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Future.delayed nima qiladi?', 'a': [{'t': 'Kechiktirib bajaradi', 'c': True}, {'t': 'Darhol bajaradi', 'c': False}, {'t': 'Xato tashlaydi', 'c': False}, {'t': 'Bekor qiladi', 'c': False}]},
        {'t': 'then() metodi nima uchun?', 'a': [{'t': 'Future tugagach ishlaydigan kod', 'c': True}, {'t': 'Future boshlanishida ishlaydigan kod', 'c': False}, {'t': 'Xato bo\'lganda ishlaydigan kod', 'c': False}, {'t': 'Har doim ishlaydigan kod', 'c': False}]},
    ]},
    
    {'n': 'Stream', 't': 20, 'o': 29, 'q': [
        {'t': 'Stream nima?', 'a': [{'t': 'Asinxron ma\'lumotlar oqimi', 'c': True}, {'t': 'Sinxron ma\'lumotlar', 'c': False}, {'t': 'Oddiy o\'zgaruvchi', 'c': False}, {'t': 'List', 'c': False}]},
        {'t': 'Stream va Future farqi?', 'a': [{'t': 'Stream ko\'p qiymat, Future bitta qiymat', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Stream tezroq', 'c': False}, {'t': 'Future yaxshiroq', 'c': False}]},
        {'t': 'Stream qanday yaratiladi?', 'a': [{'t': 'Stream.fromIterable([1, 2, 3])', 'c': True}, {'t': 'new Stream([1, 2, 3])', 'c': False}, {'t': 'Stream([1, 2, 3])', 'c': False}, {'t': 'createStream([1, 2, 3])', 'c': False}]},
        {'t': 'Stream ni qanday tinglash mumkin?', 'a': [{'t': 'stream.listen((data) {})', 'c': True}, {'t': 'stream.watch((data) {})', 'c': False}, {'t': 'stream.observe((data) {})', 'c': False}, {'t': 'stream.on((data) {})', 'c': False}]},
        {'t': 'await for nima uchun?', 'a': [{'t': 'Stream dan ma\'lumot olish', 'c': True}, {'t': 'Future dan ma\'lumot olish', 'c': False}, {'t': 'List dan ma\'lumot olish', 'c': False}, {'t': 'Map dan ma\'lumot olish', 'c': False}]},
        {'t': 'await for (var i in stream) {} bu to\'g\'rimi?', 'a': [{'t': 'Ha, async funksiyada', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat main da', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'StreamController nima?', 'a': [{'t': 'Stream yaratish va boshqarish vositasi', 'c': True}, {'t': 'Future yaratish vositasi', 'c': False}, {'t': 'List yaratish vositasi', 'c': False}, {'t': 'Map yaratish vositasi', 'c': False}]},
    ]},
    
    {'n': 'Null safety', 't': 20, 'o': 30, 'q': [
        {'t': 'Null safety nima?', 'a': [{'t': 'Null xatolaridan himoya qilish tizimi', 'c': True}, {'t': 'Xotira boshqaruvi', 'c': False}, {'t': 'Xavfsizlik tizimi', 'c': False}, {'t': 'Shifrlash tizimi', 'c': False}]},
        {'t': 'Nullable tip qanday belgilanadi?', 'a': [{'t': 'int? x;', 'c': True}, {'t': 'int x?;', 'c': False}, {'t': 'nullable int x;', 'c': False}, {'t': 'int null x;', 'c': False}]},
        {'t': 'Non-nullable tip qanday?', 'a': [{'t': 'int x; (? belgisisiz)', 'c': True}, {'t': 'int! x;', 'c': False}, {'t': 'nonnull int x;', 'c': False}, {'t': 'int x!;', 'c': False}]},
        {'t': '! operatori nima qiladi?', 'a': [{'t': 'Null emasligini ta\'kidlaydi', 'c': True}, {'t': 'Null qiladi', 'c': False}, {'t': 'Tekshiradi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
        {'t': '?? operatori nima?', 'a': [{'t': 'Null bo\'lsa, boshqa qiymat beradi', 'c': True}, {'t': 'Null qiladi', 'c': False}, {'t': 'Tekshiradi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
        {'t': 'int x = y ?? 0; bu nima degani?', 'a': [{'t': 'y null bo\'lsa, x = 0', 'c': True}, {'t': 'y null bo\'lmasa, x = 0', 'c': False}, {'t': 'x va y ni solishtiradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '?. operatori nima?', 'a': [{'t': 'Null bo\'lmasa, xususiyatga murojaat', 'c': True}, {'t': 'Har doim murojaat qiladi', 'c': False}, {'t': 'Null qiladi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
        {'t': 'late kalit so\'zi nima uchun?', 'a': [{'t': 'Keyinroq qiymat berilishini bildiradi', 'c': True}, {'t': 'Darhol qiymat beradi', 'c': False}, {'t': 'Null qiladi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_dart()
    add_topics(subj, T)
    print(f"\n✅ {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
