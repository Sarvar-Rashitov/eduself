"""
JAVA DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_java():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Java', defaults={'category': cat, 'description': 'Java dasturlash tili - ob\'ekt-yo\'naltirilgan dasturlash', 'icon': 'bi-cup-hot', 'order': 5, 'is_active': True})
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
    {'n': 'Java dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Java dasturlash tili qachon yaratilgan?', 'a': [{'t': '1995 yilda', 'c': True}, {'t': '2000 yilda', 'c': False}, {'t': '1990 yilda', 'c': False}, {'t': '2010 yilda', 'c': False}]},
        {'t': 'Java tilini kim yaratgan?', 'a': [{'t': 'James Gosling', 'c': True}, {'t': 'Bill Gates', 'c': False}, {'t': 'Steve Jobs', 'c': False}, {'t': 'Mark Zuckerberg', 'c': False}]},
        {'t': 'Java ning asosiy xususiyati?', 'a': [{'t': 'Platform mustaqil (Write Once, Run Anywhere)', 'c': True}, {'t': 'Faqat Windows da ishlaydi', 'c': False}, {'t': 'Faqat Linux da ishlaydi', 'c': False}, {'t': 'Faqat Mac da ishlaydi', 'c': False}]},
        {'t': 'Java dasturi qanday fayl kengaytmasiga ega?', 'a': [{'t': '.java', 'c': True}, {'t': '.class', 'c': False}, {'t': '.exe', 'c': False}, {'t': '.jar', 'c': False}]},
        {'t': 'Java bytecode qanday fayl kengaytmasiga ega?', 'a': [{'t': '.class', 'c': True}, {'t': '.java', 'c': False}, {'t': '.exe', 'c': False}, {'t': '.jar', 'c': False}]},
        {'t': 'JVM nima?', 'a': [{'t': 'Java Virtual Machine - Java dasturlarini ishga tushiruvchi muhit', 'c': True}, {'t': 'Java kompilyatori', 'c': False}, {'t': 'Java muharriri', 'c': False}, {'t': 'Java kutubxonasi', 'c': False}]},
    ]},
    {'n': 'Birinchi Java dasturi', 't': 20, 'o': 2, 'q': [
        {'t': 'Java dasturining asosiy metodi?', 'a': [{'t': 'public static void main(String[] args)', 'c': True}, {'t': 'void main()', 'c': False}, {'t': 'public void start()', 'c': False}, {'t': 'static void run()', 'c': False}]},
        {'t': 'System.out.println() nima qiladi?', 'a': [{'t': 'Ekranga chiqaradi va yangi qatorga o\'tadi', 'c': True}, {'t': 'Faqat ekranga chiqaradi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Kiritish qiladi', 'c': False}]},
        {'t': 'System.out.print() va println() farqi?', 'a': [{'t': 'println() yangi qatorga o\'tadi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'print() tezroq', 'c': False}, {'t': 'println() xato', 'c': False}]},
        {'t': 'Java da izoh qanday yoziladi?', 'a': [{'t': '// yoki /* */ yoki /** */', 'c': True}, {'t': 'Faqat //', 'c': False}, {'t': '# belgisi bilan', 'c': False}, {'t': '\'\'\' bilan', 'c': False}]},
        {'t': 'Java dasturini kompilyatsiya qilish buyrug\'i?', 'a': [{'t': 'javac FileName.java', 'c': True}, {'t': 'java FileName.java', 'c': False}, {'t': 'compile FileName.java', 'c': False}, {'t': 'run FileName.java', 'c': False}]},
        {'t': 'Java dasturini ishga tushirish buyrug\'i?', 'a': [{'t': 'java FileName', 'c': True}, {'t': 'java FileName.java', 'c': False}, {'t': 'run FileName', 'c': False}, {'t': 'execute FileName', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar va ma\'lumot turlari', 't': 25, 'o': 3, 'q': [
        {'t': 'Java da o\'zgaruvchi e\'lon qilish?', 'a': [{'t': 'int x = 5;', 'c': True}, {'t': 'x = 5;', 'c': False}, {'t': 'var x = 5;', 'c': False}, {'t': '$x = 5;', 'c': False}]},
        {'t': 'int nima?', 'a': [{'t': 'Butun son turi', 'c': True}, {'t': 'O\'nli kasr turi', 'c': False}, {'t': 'Matn turi', 'c': False}, {'t': 'Mantiqiy turi', 'c': False}]},
        {'t': 'double nima?', 'a': [{'t': 'O\'nli kasr son turi', 'c': True}, {'t': 'Butun son turi', 'c': False}, {'t': 'Matn turi', 'c': False}, {'t': 'Mantiqiy turi', 'c': False}]},
        {'t': 'boolean qanday qiymatlar oladi?', 'a': [{'t': 'true yoki false', 'c': True}, {'t': '0 yoki 1', 'c': False}, {'t': 'yes yoki no', 'c': False}, {'t': 'on yoki off', 'c': False}]},
        {'t': 'char nima?', 'a': [{'t': 'Bitta belgi turi', 'c': True}, {'t': 'Matn turi', 'c': False}, {'t': 'Butun son turi', 'c': False}, {'t': 'O\'nli kasr turi', 'c': False}]},
        {'t': 'String nima?', 'a': [{'t': 'Matn turi', 'c': True}, {'t': 'Butun son turi', 'c': False}, {'t': 'Bitta belgi turi', 'c': False}, {'t': 'Mantiqiy turi', 'c': False}]},
        {'t': 'Java da o\'zgaruvchi nomi raqam bilan boshlanishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Primitiv ma\'lumot turlari', 't': 25, 'o': 4, 'q': [
        {'t': 'Java da nechta primitiv tur bor?', 'a': [{'t': '8 ta', 'c': True}, {'t': '4 ta', 'c': False}, {'t': '10 ta', 'c': False}, {'t': '6 ta', 'c': False}]},
        {'t': 'byte turi qancha xotira oladi?', 'a': [{'t': '1 bayt', 'c': True}, {'t': '2 bayt', 'c': False}, {'t': '4 bayt', 'c': False}, {'t': '8 bayt', 'c': False}]},
        {'t': 'int turi qancha xotira oladi?', 'a': [{'t': '4 bayt', 'c': True}, {'t': '2 bayt', 'c': False}, {'t': '8 bayt', 'c': False}, {'t': '1 bayt', 'c': False}]},
        {'t': 'long turi qancha xotira oladi?', 'a': [{'t': '8 bayt', 'c': True}, {'t': '4 bayt', 'c': False}, {'t': '2 bayt', 'c': False}, {'t': '16 bayt', 'c': False}]},
        {'t': 'float va double farqi?', 'a': [{'t': 'double aniqroq (8 bayt), float 4 bayt', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'float aniqroq', 'c': False}, {'t': 'Ikkalasi ham bir xil', 'c': False}]},
        {'t': 'char turi qancha xotira oladi?', 'a': [{'t': '2 bayt', 'c': True}, {'t': '1 bayt', 'c': False}, {'t': '4 bayt', 'c': False}, {'t': '8 bayt', 'c': False}]},
    ]},
    {'n': 'Operatorlar', 't': 25, 'o': 5, 'q': [
        {'t': '10 + 5 natijasi?', 'a': [{'t': '15', 'c': True}, {'t': '105', 'c': False}, {'t': '5', 'c': False}, {'t': '50', 'c': False}]},
        {'t': '10 / 3 natijasi (int)?', 'a': [{'t': '3', 'c': True}, {'t': '3.333', 'c': False}, {'t': '4', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '10.0 / 3 natijasi?', 'a': [{'t': '3.333...', 'c': True}, {'t': '3', 'c': False}, {'t': '4', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '10 % 3 natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '++ operatori nima qiladi?', 'a': [{'t': '1 ga oshiradi', 'c': True}, {'t': '1 ga kamaytiradi', 'c': False}, {'t': '2 ga ko\'paytiradi', 'c': False}, {'t': 'Qo\'shadi', 'c': False}]},
        {'t': '-- operatori nima qiladi?', 'a': [{'t': '1 ga kamaytiradi', 'c': True}, {'t': '1 ga oshiradi', 'c': False}, {'t': '2 ga bo\'ladi', 'c': False}, {'t': 'Ayiradi', 'c': False}]},
        {'t': '&& operatori nima?', 'a': [{'t': 'Mantiqiy VA (AND)', 'c': True}, {'t': 'Mantiqiy YOKI (OR)', 'c': False}, {'t': 'Mantiqiy EMAS (NOT)', 'c': False}, {'t': 'Qo\'shish', 'c': False}]},
    ]},
    {'n': 'Taqqoslash operatorlari', 't': 20, 'o': 6, 'q': [
        {'t': '5 == 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 != 3 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 > 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 >= 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '0', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '3 < 10 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '7', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'if operatori', 't': 25, 'o': 7, 'q': [
        {'t': 'if operatori nima uchun?', 'a': [{'t': 'Shartli bajarish', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'if (x > 5) nima tekshiradi?', 'a': [{'t': 'x 5 dan kattami', 'c': True}, {'t': 'x 5 ga tengmi', 'c': False}, {'t': 'x 5 dan kichikmi', 'c': False}, {'t': 'x ga 5 ni beradi', 'c': False}]},
        {'t': 'if blokida kod qanday yoziladi?', 'a': [{'t': 'Jingalak qavslar ichida {}', 'c': True}, {'t': 'Oddiy qavslar ichida ()', 'c': False}, {'t': 'Kvadrat qavslar ichida []', 'c': False}, {'t': 'Qo\'shtirnoqda ""', 'c': False}]},
        {'t': 'if (x == 5) nima tekshiradi?', 'a': [{'t': 'x 5 ga tengmi', 'c': True}, {'t': 'x ga 5 ni beradi', 'c': False}, {'t': 'x 5 dan kattami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir qatorli if da {} kerakmi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'if-else operatori', 't': 25, 'o': 8, 'q': [
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'else if nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'Bir necha else if ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'if-else if-else ketma-ketligi to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, else birinchi', 'c': False}, {'t': 'Yo\'q, else if oxirida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ternary operator: x > 5 ? "Katta" : "Kichik"', 'a': [{'t': 'x>5 bo\'lsa "Katta", aks holda "Kichik"', 'c': True}, {'t': 'x va 5 ni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Stringlarni qo\'shadi', 'c': False}]},
    ]},
    {'n': 'switch-case operatori', 't': 25, 'o': 9, 'q': [
        {'t': 'switch-case nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'case nima?', 'a': [{'t': 'Bir variant', 'c': True}, {'t': 'Shart', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'switch dan chiqadi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'switch da break qo\'ymasak?', 'a': [{'t': 'Keyingi case ham bajariladi (fall-through)', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'To\'xtaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'switch qanday turlar bilan ishlaydi?', 'a': [{'t': 'byte, short, int, char, String, enum', 'c': True}, {'t': 'Faqat int', 'c': False}, {'t': 'Faqat String', 'c': False}, {'t': 'Barcha turlar', 'c': False}]},
    ]},
    {'n': 'while sikli', 't': 25, 'o': 10, 'q': [
        {'t': 'while sikli nima uchun?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'while (true) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Sikldan chiqish uchun?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'Siklning keyingi iteratsiyasiga o\'tish?', 'a': [{'t': 'continue', 'c': True}, {'t': 'skip', 'c': False}, {'t': 'next', 'c': False}, {'t': 'pass', 'c': False}]},
        {'t': 'int i=0; while(i<3) {System.out.print(i); i++;} necha marta?', 'a': [{'t': '3 marta', 'c': True}, {'t': '2 marta', 'c': False}, {'t': '4 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
    ]},
    {'n': 'do-while sikli', 't': 20, 'o': 11, 'q': [
        {'t': 'do-while va while farqi?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'while kamida 1 marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'do-while da shart qayerda tekshiriladi?', 'a': [{'t': 'Oxirida', 'c': True}, {'t': 'Boshida', 'c': False}, {'t': 'O\'rtada', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'do {...} while(shart); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while oxirida ; kerakmi?', 'a': [{'t': 'Ha, kerak', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while qachon ishlatiladi?', 'a': [{'t': 'Kamida 1 marta bajarish kerak bo\'lsa', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
    ]},
    {'n': 'for sikli', 't': 25, 'o': 12, 'q': [
        {'t': 'for sikli nima uchun?', 'a': [{'t': 'Ma\'lum marta takrorlash', 'c': True}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'for (int i=0; i<5; i++) necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for siklining 3 qismi?', 'a': [{'t': 'Boshlang\'ich, shart, o\'zgartirish', 'c': True}, {'t': 'Faqat shart', 'c': False}, {'t': 'Faqat boshlang\'ich', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for (;;) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Enhanced for (for-each) sikli', 't': 25, 'o': 13, 'q': [
        {'t': 'Enhanced for nima uchun?', 'a': [{'t': 'Massiv va kolleksiyalarni aylanish', 'c': True}, {'t': 'Oddiy takrorlash', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Metod yaratish', 'c': False}]},
        {'t': 'for (int x : arr) nima qiladi?', 'a': [{'t': 'arr massivini aylanadi', 'c': True}, {'t': 'arr ni yaratadi', 'c': False}, {'t': 'arr ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Enhanced for da indeksga kirishish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat qiymatga', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Enhanced for da elementni o\'zgartirish mumkinmi?', 'a': [{'t': 'Primitiv turlarda yo\'q, ob\'ektlarda ha', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Enhanced for va oddiy for farqi?', 'a': [{'t': 'Enhanced for soddaroq, indeks yo\'q', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Oddiy for tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Massivlar - Asoslar', 't': 25, 'o': 14, 'q': [
        {'t': 'Massiv nima?', 'a': [{'t': 'Bir xil turdagi elementlar to\'plami', 'c': True}, {'t': 'Bitta qiymat', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'int[] arr = new int[5]; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'int[] arr = {1,2,3}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': 'arr[0] nima?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Ikkinchi element', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.length nima qaytaradi?', 'a': [{'t': 'Massiv uzunligi', 'c': True}, {'t': 'Massiv qiymati', 'c': False}, {'t': 'Massiv turi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Massiv o\'lchamini o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, o\'zgarmas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ko\'p o\'lchovli massivlar', 't': 25, 'o': 15, 'q': [
        {'t': 'Ko\'p o\'lchovli massiv nima?', 'a': [{'t': 'Massivlar massivi', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int[][] arr = new int[3][4]; nima?', 'a': [{'t': '3 qator, 4 ustunli massiv', 'c': True}, {'t': '4 qator, 3 ustunli massiv', 'c': False}, {'t': '7 elementli massiv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr[0][0] nima?', 'a': [{'t': 'Birinchi qator, birinchi ustun', 'c': True}, {'t': 'Ikkinchi qator, ikkinchi ustun', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '2D massivni aylanish uchun?', 'a': [{'t': 'Ichma-ich for sikllar', 'c': True}, {'t': 'Bitta for sikl', 'c': False}, {'t': 'while sikl', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'int[][] arr = {{1,2},{3,4,5}}; to\'g\'rimi?', 'a': [{'t': 'Ha, jagged array (turli uzunlikdagi)', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Faqat kvadrat massiv bo\'lishi kerak', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'String sinfi', 't': 25, 'o': 16, 'q': [
        {'t': 'String nima?', 'a': [{'t': 'Ob\'ekt turi (class)', 'c': True}, {'t': 'Primitiv tur', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'String s = "Hello"; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'String o\'zgarmasmi (immutable)?', 'a': [{'t': 'Ha, o\'zgarmas', 'c': True}, {'t': 'Yo\'q, o\'zgaruvchan', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Stringlarni birlashtirish operatori?', 'a': [{'t': '+ (plyus)', 'c': True}, {'t': '. (nuqta)', 'c': False}, {'t': '& (ampersand)', 'c': False}, {'t': ', (vergul)', 'c': False}]},
        {'t': '"Hello" + " World" natijasi?', 'a': [{'t': 'Hello World', 'c': True}, {'t': 'HelloWorld', 'c': False}, {'t': 'Hello+World', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.length() nima qiladi?', 'a': [{'t': 'String uzunligini qaytaradi', 'c': True}, {'t': 'Stringni o\'chiradi', 'c': False}, {'t': 'Stringni teskari qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'String metodlari', 't': 25, 'o': 17, 'q': [
        {'t': 's.charAt(0) nima qiladi?', 'a': [{'t': 'Birinchi belgini qaytaradi', 'c': True}, {'t': 'Oxirgi belgini qaytaradi', 'c': False}, {'t': 'Barcha belgilarni qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.toUpperCase() nima qiladi?', 'a': [{'t': 'Katta harflarga o\'tkazadi', 'c': True}, {'t': 'Kichik harflarga o\'tkazadi', 'c': False}, {'t': 'Birinchi harfni katta qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.toLowerCase() nima qiladi?', 'a': [{'t': 'Kichik harflarga o\'tkazadi', 'c': True}, {'t': 'Katta harflarga o\'tkazadi', 'c': False}, {'t': 'Birinchi harfni kichik qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.substring(0, 3) nima qiladi?', 'a': [{'t': '0 dan 3 gacha (3 kirmaydi) qismini oladi', 'c': True}, {'t': '0 dan 3 gacha (3 kiradi) qismini oladi', 'c': False}, {'t': '3 ta belgini o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.indexOf("a") nima qiladi?', 'a': [{'t': '"a" ning birinchi pozitsiyasini topadi', 'c': True}, {'t': '"a" ning oxirgi pozitsiyasini topadi', 'c': False}, {'t': '"a" ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.replace("a", "b") nima qiladi?', 'a': [{'t': 'Barcha "a" ni "b" ga almashtiradi', 'c': True}, {'t': 'Birinchi "a" ni "b" ga almashtiradi', 'c': False}, {'t': '"a" ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.equals("Hello") nima qiladi?', 'a': [{'t': 'Stringlarni taqqoslaydi', 'c': True}, {'t': 's ga "Hello" ni beradi', 'c': False}, {'t': 'Stringlarni birlashtiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Metodlar - Asoslar', 't': 25, 'o': 18, 'q': [
        {'t': 'Metod nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Sikl', 'c': False}]},
        {'t': 'public static void myMethod() {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'void nima degani?', 'a': [{'t': 'Hech narsa qaytarmaydi', 'c': True}, {'t': 'int qaytaradi', 'c': False}, {'t': 'String qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Metoddan qiymat qaytarish uchun?', 'a': [{'t': 'return kalit so\'zi', 'c': True}, {'t': 'send kalit so\'zi', 'c': False}, {'t': 'give kalit so\'zi', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'Metodni chaqirish?', 'a': [{'t': 'myMethod();', 'c': True}, {'t': 'call myMethod();', 'c': False}, {'t': 'run myMethod();', 'c': False}, {'t': 'execute myMethod();', 'c': False}]},
    ]},
    {'n': 'Metod parametrlari', 't': 25, 'o': 19, 'q': [
        {'t': 'Parametr nima?', 'a': [{'t': 'Metodga beriladigan qiymat', 'c': True}, {'t': 'Metoddan qaytadigan qiymat', 'c': False}, {'t': 'Metod nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'void myMethod(int x) {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Bir necha parametr qo\'shish mumkinmi?', 'a': [{'t': 'Ha, vergul bilan ajratib', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'void myMethod(int x, String y) {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Parametr va argument farqi?', 'a': [{'t': 'Parametr - e\'londa, argument - chaqirishda', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Argument - e\'londa, parametr - chaqirishda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Metod overloading', 't': 25, 'o': 20, 'q': [
        {'t': 'Method overloading nima?', 'a': [{'t': 'Bir xil nomli, turli parametrli metodlar', 'c': True}, {'t': 'Turli nomli metodlar', 'c': False}, {'t': 'Bir xil metodlar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Overloading uchun nima farq qilishi kerak?', 'a': [{'t': 'Parametrlar soni yoki turi', 'c': True}, {'t': 'Faqat metod nomi', 'c': False}, {'t': 'Faqat qaytish turi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'int sum(int a, int b) va int sum(int a, int b, int c) overloadingmi?', 'a': [{'t': 'Ha, parametrlar soni farq qiladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'int sum(int a, int b) va double sum(int a, int b) overloadingmi?', 'a': [{'t': 'Yo\'q, faqat qaytish turi farq qiladi', 'c': True}, {'t': 'Ha, to\'g\'ri', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Overloading nima uchun foydali?', 'a': [{'t': 'Bir xil vazifani turli parametrlar bilan bajarish', 'c': True}, {'t': 'Kod hajmini oshirish', 'c': False}, {'t': 'Xatolik yaratish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Rekursiya', 't': 25, 'o': 21, 'q': [
        {'t': 'Rekursiya nima?', 'a': [{'t': 'Metod o\'zini chaqirishi', 'c': True}, {'t': 'Metod boshqa metodlarni chaqirishi', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Rekursiyada nima muhim?', 'a': [{'t': 'Base case (to\'xtash sharti)', 'c': True}, {'t': 'Faqat chaqirish', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Base case bo\'lmasa nima bo\'ladi?', 'a': [{'t': 'Cheksiz rekursiya (StackOverflowError)', 'c': True}, {'t': 'Hech narsa', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Tez ishlaydi', 'c': False}]},
        {'t': 'Faktorial hisoblash rekursiyaga misolmi?', 'a': [{'t': 'Ha, klassik misol', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Rekursiya va sikl farqi?', 'a': [{'t': 'Rekursiya o\'zini chaqiradi, sikl takrorlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Sikl tezroq', 'c': False}, {'t': 'Rekursiya har doim yaxshi', 'c': False}]},
    ]},
    {'n': 'OOP - Sinflar va ob\'ektlar', 't': 25, 'o': 22, 'q': [
        {'t': 'OOP nima?', 'a': [{'t': 'Object-Oriented Programming', 'c': True}, {'t': 'Online Programming', 'c': False}, {'t': 'Open Programming', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Sinf (class) nima?', 'a': [{'t': 'Ob\'ektlar uchun shablon', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Ob\'ekt (object) nima?', 'a': [{'t': 'Sinfning namunasi (instance)', 'c': True}, {'t': 'Sinf', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'class Car {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Car myCar = new Car(); nima qiladi?', 'a': [{'t': 'Ob\'ekt yaratadi', 'c': True}, {'t': 'Sinf yaratadi', 'c': False}, {'t': 'Metod chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'new kalit so\'zi nima qiladi?', 'a': [{'t': 'Yangi ob\'ekt yaratadi', 'c': True}, {'t': 'Sinf yaratadi', 'c': False}, {'t': 'Metod yaratadi', 'c': False}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}]},
    ]},
    {'n': 'OOP - Konstruktorlar', 't': 25, 'o': 23, 'q': [
        {'t': 'Konstruktor nima?', 'a': [{'t': 'Ob\'ekt yaratilganda chaqiriladigan maxsus metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Konstruktor nomi qanday bo\'lishi kerak?', 'a': [{'t': 'Sinf nomi bilan bir xil', 'c': True}, {'t': 'Istalgan nom', 'c': False}, {'t': 'constructor', 'c': False}, {'t': 'init', 'c': False}]},
        {'t': 'Konstruktor qaytish turiga egami?', 'a': [{'t': 'Yo\'q, qaytish turi yo\'q', 'c': True}, {'t': 'Ha, void', 'c': False}, {'t': 'Ha, int', 'c': False}, {'t': 'Ha, String', 'c': False}]},
        {'t': 'Default konstruktor nima?', 'a': [{'t': 'Parametrsiz avtomatik yaratilgan konstruktor', 'c': True}, {'t': 'Parametrli konstruktor', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir necha konstruktor bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, overloading orqali', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'this kalit so\'zi nima?', 'a': [{'t': 'Joriy ob\'ektga havola', 'c': True}, {'t': 'Boshqa ob\'ektga havola', 'c': False}, {'t': 'Sinfga havola', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OOP - Inkapsulyatsiya', 't': 25, 'o': 24, 'q': [
        {'t': 'Inkapsulyatsiya nima?', 'a': [{'t': 'Ma\'lumotlarni yashirish va himoya qilish', 'c': True}, {'t': 'Ma\'lumotlarni ochiq qilish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'private nima degani?', 'a': [{'t': 'Faqat o\'sha sinfda ko\'rinadi', 'c': True}, {'t': 'Hamma joyda ko\'rinadi', 'c': False}, {'t': 'Faqat paket ichida ko\'rinadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'public nima degani?', 'a': [{'t': 'Hamma joyda ko\'rinadi', 'c': True}, {'t': 'Faqat o\'sha sinfda ko\'rinadi', 'c': False}, {'t': 'Faqat paket ichida ko\'rinadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Getter metod nima?', 'a': [{'t': 'Private o\'zgaruvchini o\'qish uchun', 'c': True}, {'t': 'Private o\'zgaruvchini yozish uchun', 'c': False}, {'t': 'Ob\'ekt yaratish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Setter metod nima?', 'a': [{'t': 'Private o\'zgaruvchiga qiymat berish uchun', 'c': True}, {'t': 'Private o\'zgaruvchini o\'qish uchun', 'c': False}, {'t': 'Ob\'ekt yaratish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'protected nima degani?', 'a': [{'t': 'Paket va subclass larda ko\'rinadi', 'c': True}, {'t': 'Faqat o\'sha sinfda ko\'rinadi', 'c': False}, {'t': 'Hamma joyda ko\'rinadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OOP - Meros olish (Inheritance)', 't': 25, 'o': 25, 'q': [
        {'t': 'Inheritance nima?', 'a': [{'t': 'Bir sinf boshqa sinfdan xususiyatlarni olishi', 'c': True}, {'t': 'Yangi sinf yaratish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'extends kalit so\'zi nima qiladi?', 'a': [{'t': 'Meros olish uchun ishlatiladi', 'c': True}, {'t': 'Ob\'ekt yaratadi', 'c': False}, {'t': 'Metod yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'class Dog extends Animal {} to\'g\'rimi?', 'a': [{'t': 'Ha, Dog Animal dan meros oladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Superclass nima?', 'a': [{'t': 'Ota sinf (parent class)', 'c': True}, {'t': 'Bola sinf (child class)', 'c': False}, {'t': 'Oddiy sinf', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Subclass nima?', 'a': [{'t': 'Bola sinf (child class)', 'c': True}, {'t': 'Ota sinf (parent class)', 'c': False}, {'t': 'Oddiy sinf', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'super kalit so\'zi nima?', 'a': [{'t': 'Ota sinfga havola', 'c': True}, {'t': 'Joriy sinfga havola', 'c': False}, {'t': 'Bola sinfga havola', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Java da bir sinfdan nechta sinf meros olish mumkin?', 'a': [{'t': 'Faqat bitta (single inheritance)', 'c': True}, {'t': 'Istalgancha', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'OOP - Polimorfizm', 't': 25, 'o': 26, 'q': [
        {'t': 'Polimorfizm nima?', 'a': [{'t': 'Bir ob\'ektning ko\'p shaklda bo\'lishi', 'c': True}, {'t': 'Bir sinf yaratish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Method overriding nima?', 'a': [{'t': 'Subclass da superclass metodini qayta yozish', 'c': True}, {'t': 'Bir xil nomli metodlar yaratish', 'c': False}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '@Override annotatsiyasi nima uchun?', 'a': [{'t': 'Metodning override ekanligini ko\'rsatish', 'c': True}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Metodni o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Overloading va overriding farqi?', 'a': [{'t': 'Overloading - bir sinfda, overriding - meros olishda', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Overriding - bir sinfda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Animal a = new Dog(); to\'g\'rimi?', 'a': [{'t': 'Ha, polimorfizm (upcasting)', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'OOP - Abstraktlik', 't': 25, 'o': 27, 'q': [
        {'t': 'Abstract class nima?', 'a': [{'t': 'Ob\'ekt yaratib bo\'lmaydigan sinf', 'c': True}, {'t': 'Oddiy sinf', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'abstract kalit so\'zi nima uchun?', 'a': [{'t': 'Abstract sinf yoki metod yaratish', 'c': True}, {'t': 'Oddiy sinf yaratish', 'c': False}, {'t': 'Ob\'ekt yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Abstract metod nima?', 'a': [{'t': 'Tanasi yo\'q metod (faqat imzo)', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Static metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Abstract sinfdan ob\'ekt yaratish mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Abstract sinfdan meros olish mumkinmi?', 'a': [{'t': 'Ha, subclass abstract metodlarni implement qilishi kerak', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Abstract sinfda oddiy metod bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, faqat abstract metodlar', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Interface', 't': 25, 'o': 28, 'q': [
        {'t': 'Interface nima?', 'a': [{'t': 'Faqat abstract metodlar to\'plami (Java 8 gacha)', 'c': True}, {'t': 'Oddiy sinf', 'c': False}, {'t': 'Abstract sinf', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'interface kalit so\'zi nima uchun?', 'a': [{'t': 'Interface yaratish', 'c': True}, {'t': 'Sinf yaratish', 'c': False}, {'t': 'Ob\'ekt yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'implements kalit so\'zi nima qiladi?', 'a': [{'t': 'Interface ni implement qilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Ob\'ekt yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'class Dog implements Animal {} to\'g\'rimi?', 'a': [{'t': 'Ha, Dog Animal interface ni implement qiladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Bir sinf nechta interface implement qilishi mumkin?', 'a': [{'t': 'Istalgancha (multiple inheritance)', 'c': True}, {'t': 'Faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Interface dan ob\'ekt yaratish mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Interface metodlari qanday?', 'a': [{'t': 'Default public abstract', 'c': True}, {'t': 'Private', 'c': False}, {'t': 'Protected', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Exception Handling - Asoslar', 't': 25, 'o': 29, 'q': [
        {'t': 'Exception nima?', 'a': [{'t': 'Dastur ishlashida yuzaga keladigan xatolik', 'c': True}, {'t': 'Oddiy xato', 'c': False}, {'t': 'Sintaksis xatosi', 'c': False}, {'t': 'Ogohlantirish', 'c': False}]},
        {'t': 'try-catch nima uchun?', 'a': [{'t': 'Xatoliklarni ushlash va boshqarish', 'c': True}, {'t': 'Kod yozish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Ob\'ekt yaratish', 'c': False}]},
        {'t': 'try bloki nima?', 'a': [{'t': 'Xatolik yuz berishi mumkin bo\'lgan kod', 'c': True}, {'t': 'Xatolikni ushlash kodi', 'c': False}, {'t': 'Har doim bajariladigan kod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'catch bloki nima?', 'a': [{'t': 'Xatolikni ushlash va qayta ishlash kodi', 'c': True}, {'t': 'Xatolik yuz berishi mumkin bo\'lgan kod', 'c': False}, {'t': 'Har doim bajariladigan kod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'finally bloki nima?', 'a': [{'t': 'Har doim bajariladigan kod', 'c': True}, {'t': 'Xatolik yuz bersa bajariladigan kod', 'c': False}, {'t': 'Xatolik bo\'lmasa bajariladigan kod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir necha catch blok bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, turli xatoliklar uchun', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'Exception Handling - Davomi', 't': 25, 'o': 30, 'q': [
        {'t': 'throw kalit so\'zi nima qiladi?', 'a': [{'t': 'Xatolik tashlaydi', 'c': True}, {'t': 'Xatolikni ushlaydi', 'c': False}, {'t': 'Xatolikni bartaraf qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'throws kalit so\'zi nima qiladi?', 'a': [{'t': 'Metod xatolik tashlashi mumkinligini e\'lon qiladi', 'c': True}, {'t': 'Xatolik tashlaydi', 'c': False}, {'t': 'Xatolikni ushlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'throw va throws farqi?', 'a': [{'t': 'throw - xatolik tashlash, throws - e\'lon qilish', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'throws - xatolik tashlash', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Checked exception nima?', 'a': [{'t': 'Kompilyatsiya vaqtida tekshiriladigan xatolik', 'c': True}, {'t': 'Runtime da yuz beradigan xatolik', 'c': False}, {'t': 'Oddiy xatolik', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Unchecked exception nima?', 'a': [{'t': 'Runtime da yuz beradigan xatolik', 'c': True}, {'t': 'Kompilyatsiya vaqtida tekshiriladigan xatolik', 'c': False}, {'t': 'Oddiy xatolik', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'NullPointerException qanday xatolik?', 'a': [{'t': 'Unchecked (RuntimeException)', 'c': True}, {'t': 'Checked', 'c': False}, {'t': 'Sintaksis xatosi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'O\'z exception sinfingizni yaratish mumkinmi?', 'a': [{'t': 'Ha, Exception yoki RuntimeException dan meros olib', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("🚀 Java dasturlash - 30 ta mavzu qo'shilmoqda...")
    subject = get_or_create_java()
    add_topics(subject, T)
    print(f"\n✅ Jami {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
    print("📊 Har bir mavzuda 5-10 ta test savoli mavjud")
    print("🎯 To'g'ri javoblar har xil pozitsiyalarda joylashtirilgan")
