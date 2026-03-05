"""
PYTHON DASTURLASH - 100 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_python():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Python', defaults={'category': cat, 'description': 'Python dasturlash tili - asoslardan professionallikgacha', 'icon': 'bi-file-code', 'order': 1, 'is_active': True})
    return subj

def add_topics(subject, topics_data):
    for td in topics_data:
        topic, created = Topic.objects.get_or_create(subject=subject, name=td['n'], defaults={'time_limit': td['t'], 'passing_score': 60, 'order': td['o'], 'is_active': True})
        print(f"{'✅' if created else 'ℹ️'} §{td['o']}: {td['n']} ({len(td['q'])} test)")
        for i, qd in enumerate(td['q']):
            q, qc = Question.objects.get_or_create(topic=topic, text=qd['t'], defaults={'points': 10, 'order': i + 1})
            if qc:
                # Javoblarni tasodifiy aralashtiramiz
                answers = qd['a'].copy()
                random.shuffle(answers)
                for ad in answers:
                    Answer.objects.create(question=q, text=ad['t'], is_correct=ad['c'])

# 100 TA MAVZU (boshlang'ichdan murakkabgacha)
T = [
    # ASOSLAR (1-15)
    {'n': 'Python dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Python qanday dasturlash tili?', 'a': [{'t': 'Yuqori darajali, talqin qilinadigan til', 'c': True}, {'t': 'Past darajali til', 'c': False}, {'t': 'Faqat veb uchun til', 'c': False}, {'t': 'Kompilatsiya qilinadigan til', 'c': False}]},
        {'t': 'Python dasturini qanday ishga tushirish mumkin?', 'a': [{'t': 'python fayl.py buyrug\'i orqali', 'c': True}, {'t': 'Faqat brauzerda', 'c': False}, {'t': 'Faqat kompilatsiya qilib', 'c': False}, {'t': 'Ishga tushirib bo\'lmaydi', 'c': False}]},
        {'t': 'Python faylining kengaytmasi qanday?', 'a': [{'t': '.py', 'c': True}, {'t': '.python', 'c': False}, {'t': '.txt', 'c': False}, {'t': '.exe', 'c': False}]},
        {'t': 'Python tilining yaratuvchisi kim?', 'a': [{'t': 'Guido van Rossum', 'c': True}, {'t': 'Bill Gates', 'c': False}, {'t': 'Steve Jobs', 'c': False}, {'t': 'Mark Zuckerberg', 'c': False}]},
        {'t': 'Python qaysi sohalarda ishlatiladi?', 'a': [{'t': 'Veb, AI, Data Science, avtomatlashtirish', 'c': True}, {'t': 'Faqat veb dasturlash', 'c': False}, {'t': 'Faqat o\'yinlar', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},
    {'n': 'Birinchi dastur - Hello World', 't': 15, 'o': 2, 'q': [
        {'t': 'Ekranga matn chiqarish uchun qaysi funksiya ishlatiladi?', 'a': [{'t': 'print()', 'c': True}, {'t': 'echo()', 'c': False}, {'t': 'write()', 'c': False}, {'t': 'display()', 'c': False}]},
        {'t': 'print("Hello") natijasi nima?', 'a': [{'t': 'Hello', 'c': True}, {'t': '"Hello"', 'c': False}, {'t': 'print("Hello")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir necha qatorga chiqarish uchun?', 'a': [{'t': 'print() ni bir necha marta yozish', 'c': True}, {'t': 'Faqat bitta print() ishlatish mumkin', 'c': False}, {'t': 'Buning imkoni yo\'q', 'c': False}, {'t': 'echo() ishlatish kerak', 'c': False}]},
        {'t': 'print(5 + 3) natijasi nima?', 'a': [{'t': '8', 'c': True}, {'t': '5 + 3', 'c': False}, {'t': '53', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Python da izoh qanday yoziladi?', 'a': [{'t': '# belgisi bilan', 'c': True}, {'t': '// belgisi bilan', 'c': False}, {'t': '/* */ bilan', 'c': False}, {'t': 'Izoh yozib bo\'lmaydi', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar (Variables)', 't': 20, 'o': 3, 'q': [
        {'t': 'O\'zgaruvchi nima?', 'a': [{'t': 'Ma\'lumot saqlaydigan joy', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Dastur', 'c': False}]},
        {'t': 'To\'g\'ri o\'zgaruvchi nomi qaysi?', 'a': [{'t': 'ism', 'c': True}, {'t': '1ism', 'c': False}, {'t': 'ism-familiya', 'c': False}, {'t': 'ism familiya', 'c': False}]},
        {'t': 'x = 10 nima qiladi?', 'a': [{'t': 'x ga 10 qiymatini beradi', 'c': True}, {'t': 'x ni 10 ga tenglashtiradi', 'c': False}, {'t': 'x dan 10 ni ayiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'O\'zgaruvchi nomida qaysi belgilardan foydalanish mumkin?', 'a': [{'t': 'Harflar, raqamlar, _ belgisi', 'c': True}, {'t': 'Faqat harflar', 'c': False}, {'t': 'Faqat raqamlar', 'c': False}, {'t': 'Har qanday belgi', 'c': False}]},
        {'t': 'Python da o\'zgaruvchi turini e\'lon qilish kerakmi?', 'a': [{'t': 'Yo\'q, avtomatik aniqlanadi', 'c': True}, {'t': 'Ha, har doim kerak', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Bir necha o\'zgaruvchiga qiymat berish: a = b = 5 to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari - Sonlar', 't': 20, 'o': 4, 'q': [
        {'t': 'Python da qanday son turlari bor?', 'a': [{'t': 'int, float, complex', 'c': True}, {'t': 'Faqat int', 'c': False}, {'t': 'Faqat float', 'c': False}, {'t': 'number', 'c': False}]},
        {'t': 'int nima?', 'a': [{'t': 'Butun son', 'c': True}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'float nima?', 'a': [{'t': 'O\'nli kasr son', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'type(10) natijasi nima?', 'a': [{'t': '<class \'int\'>', 'c': True}, {'t': '<class \'float\'>', 'c': False}, {'t': '<class \'str\'>', 'c': False}, {'t': '10', 'c': False}]},
        {'t': 'type(10.5) natijasi nima?', 'a': [{'t': '<class \'float\'>', 'c': True}, {'t': '<class \'int\'>', 'c': False}, {'t': '<class \'str\'>', 'c': False}, {'t': '10.5', 'c': False}]},
        {'t': '5 / 2 natijasi nima?', 'a': [{'t': '2.5', 'c': True}, {'t': '2', 'c': False}, {'t': '3', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 // 2 natijasi nima?', 'a': [{'t': '2', 'c': True}, {'t': '2.5', 'c': False}, {'t': '3', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari - Matnlar (Strings)', 't': 25, 'o': 5, 'q': [
        {'t': 'Matn (string) qanday yaratiladi?', 'a': [{'t': 'Qo\'shtirnoq yoki birtirnoq ichida', 'c': True}, {'t': 'Faqat qo\'shtirnoqda', 'c': False}, {'t': 'Faqat birtirnoqda', 'c': False}, {'t': 'Qavslar ichida', 'c': False}]},
        {'t': '"Salom" + " " + "Dunyo" natijasi?', 'a': [{'t': 'Salom Dunyo', 'c': True}, {'t': 'SalomDunyo', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Salom + Dunyo', 'c': False}]},
        {'t': '"Python" * 3 natijasi?', 'a': [{'t': 'PythonPythonPython', 'c': True}, {'t': 'Python3', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Python Python Python', 'c': False}]},
        {'t': 'len("Salom") natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '4', 'c': False}, {'t': '6', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"Python"[0] natijasi?', 'a': [{'t': 'P', 'c': True}, {'t': 'y', 'c': False}, {'t': 'Python', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"Python"[-1] natijasi?', 'a': [{'t': 'n', 'c': True}, {'t': 'P', 'c': False}, {'t': 'o', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"Python"[0:3] natijasi?', 'a': [{'t': 'Pyt', 'c': True}, {'t': 'Pyth', 'c': False}, {'t': 'Python', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Matn metodlari', 't': 20, 'o': 6, 'q': [
        {'t': '"python".upper() natijasi?', 'a': [{'t': 'PYTHON', 'c': True}, {'t': 'python', 'c': False}, {'t': 'Python', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"PYTHON".lower() natijasi?', 'a': [{'t': 'python', 'c': True}, {'t': 'PYTHON', 'c': False}, {'t': 'Python', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"  salom  ".strip() natijasi?', 'a': [{'t': 'salom', 'c': True}, {'t': '  salom  ', 'c': False}, {'t': 'salom  ', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"Python dasturlash".split() natijasi?', 'a': [{'t': '["Python", "dasturlash"]', 'c': True}, {'t': '"Python dasturlash"', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '["Pythondasturlash"]', 'c': False}]},
        {'t': '"Python".replace("P", "J") natijasi?', 'a': [{'t': 'Jython', 'c': True}, {'t': 'Python', 'c': False}, {'t': 'JPython', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"Python" in "Python dasturlash" natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '1', 'c': False}]},
    ]},
    {'n': 'Arifmetik operatorlar', 't': 20, 'o': 7, 'q': [
        {'t': '10 + 5 natijasi?', 'a': [{'t': '15', 'c': True}, {'t': '105', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 - 5 natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '15', 'c': False}, {'t': '-5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 * 5 natijasi?', 'a': [{'t': '50', 'c': True}, {'t': '15', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 / 5 natijasi?', 'a': [{'t': '2.0', 'c': True}, {'t': '2', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 % 3 natijasi (qoldiq)?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '2 ** 3 natijasi (daraja)?', 'a': [{'t': '8', 'c': True}, {'t': '6', 'c': False}, {'t': '9', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 // 3 natijasi (butun bo\'lish)?', 'a': [{'t': '3', 'c': True}, {'t': '3.33', 'c': False}, {'t': '4', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Taqqoslash operatorlari', 't': 20, 'o': 8, 'q': [
        {'t': '5 == 5 natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 != 3 natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 > 3 natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 < 3 natijasi?', 'a': [{'t': 'False', 'c': True}, {'t': 'True', 'c': False}, {'t': '-2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 >= 5 natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': '0', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 <= 3 natijasi?', 'a': [{'t': 'False', 'c': True}, {'t': 'True', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Mantiqiy operatorlar', 't': 20, 'o': 9, 'q': [
        {'t': 'True and True natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'True and False natijasi?', 'a': [{'t': 'False', 'c': True}, {'t': 'True', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'True or False natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'False or False natijasi?', 'a': [{'t': 'False', 'c': True}, {'t': 'True', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'not True natijasi?', 'a': [{'t': 'False', 'c': True}, {'t': 'True', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'not False natijasi?', 'a': [{'t': 'True', 'c': True}, {'t': 'False', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
    ]},
    {'n': 'Foydalanuvchidan ma\'lumot olish', 't': 20, 'o': 10, 'q': [
        {'t': 'Foydalanuvchidan ma\'lumot olish uchun qaysi funksiya ishlatiladi?', 'a': [{'t': 'input()', 'c': True}, {'t': 'get()', 'c': False}, {'t': 'read()', 'c': False}, {'t': 'scan()', 'c': False}]},
        {'t': 'input() funksiyasi qanday ma\'lumot qaytaradi?', 'a': [{'t': 'String (matn)', 'c': True}, {'t': 'Integer (butun son)', 'c': False}, {'t': 'Float (o\'nli kasr)', 'c': False}, {'t': 'Boolean', 'c': False}]},
        {'t': 'Foydalanuvchidan son olish uchun?', 'a': [{'t': 'int(input())', 'c': True}, {'t': 'input()', 'c': False}, {'t': 'number(input())', 'c': False}, {'t': 'get_number()', 'c': False}]},
        {'t': 'input("Ismingiz: ") nima qiladi?', 'a': [{'t': 'Savolni ko\'rsatib, javobni oladi', 'c': True}, {'t': 'Faqat savolni chiqaradi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'float(input()) nima uchun ishlatiladi?', 'a': [{'t': 'O\'nli kasr son olish uchun', 'c': True}, {'t': 'Butun son olish uchun', 'c': False}, {'t': 'Matn olish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'If shartli operatori', 't': 25, 'o': 11, 'q': [
        {'t': 'if operatori nima uchun ishlatiladi?', 'a': [{'t': 'Shartli ravishda kod bajarish uchun', 'c': True}, {'t': 'Takrorlash uchun', 'c': False}, {'t': 'Funksiya yaratish uchun', 'c': False}, {'t': 'Ma\'lumot saqlash uchun', 'c': False}]},
        {'t': 'if x > 5: print("Katta") - bu kod qachon ishlaydi?', 'a': [{'t': 'x 5 dan katta bo\'lsa', 'c': True}, {'t': 'x 5 ga teng bo\'lsa', 'c': False}, {'t': 'x 5 dan kichik bo\'lsa', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'if blokida kod qanday yoziladi?', 'a': [{'t': 'Ichkariga surib (indent)', 'c': True}, {'t': 'Oddiy yoziladi', 'c': False}, {'t': 'Qavslar ichida', 'c': False}, {'t': 'Qo\'shtirnoqda', 'c': False}]},
        {'t': 'Python da indent nima?', 'a': [{'t': 'Kod blokini ko\'rsatuvchi bo\'sh joy', 'c': True}, {'t': 'Operator', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'if x == 5: nima tekshiradi?', 'a': [{'t': 'x 5 ga tengmi', 'c': True}, {'t': 'x ga 5 ni beradi', 'c': False}, {'t': 'x 5 dan kattami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'else va elif', 't': 25, 'o': 12, 'q': [
        {'t': 'else nima uchun ishlatiladi?', 'a': [{'t': 'if sharti bajarilmasa ishlaydigan kod', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash uchun', 'c': False}, {'t': 'Funksiya yaratish uchun', 'c': False}]},
        {'t': 'elif nima?', 'a': [{'t': 'Qo\'shimcha shart (else if)', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Bir necha elif ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'elif ishlatib bo\'lmaydi', 'c': False}]},
        {'t': 'if-elif-else ketma-ketligi to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, else birinchi bo\'lishi kerak', 'c': False}, {'t': 'Yo\'q, elif oxirida bo\'lishi kerak', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'else dan keyin shart yozish kerakmi?', 'a': [{'t': 'Yo\'q, shart yozilmaydi', 'c': True}, {'t': 'Ha, shart yoziladi', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'While sikli', 't': 25, 'o': 13, 'q': [
        {'t': 'while sikli nima uchun ishlatiladi?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash uchun', 'c': True}, {'t': 'Faqat bir marta bajarish uchun', 'c': False}, {'t': 'Funksiya yaratish uchun', 'c': False}, {'t': 'Ma\'lumot saqlash uchun', 'c': False}]},
        {'t': 'while True: nima qiladi?', 'a': [{'t': 'Cheksiz sikl yaratadi', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Sikldan chiqish uchun qaysi operator ishlatiladi?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'Siklning keyingi iteratsiyasiga o\'tish uchun?', 'a': [{'t': 'continue', 'c': True}, {'t': 'skip', 'c': False}, {'t': 'next', 'c': False}, {'t': 'pass', 'c': False}]},
        {'t': 'i = 0; while i < 3: print(i); i += 1 - necha marta ishlaydi?', 'a': [{'t': '3 marta', 'c': True}, {'t': '2 marta', 'c': False}, {'t': '4 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
    ]},
    {'n': 'For sikli', 't': 25, 'o': 14, 'q': [
        {'t': 'for sikli nima uchun ishlatiladi?', 'a': [{'t': 'Ketma-ketlik bo\'ylab takrorlash uchun', 'c': True}, {'t': 'Shart tekshirish uchun', 'c': False}, {'t': 'Funksiya yaratish uchun', 'c': False}, {'t': 'Ma\'lumot saqlash uchun', 'c': False}]},
        {'t': 'for i in range(5): necha marta ishlaydi?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'range(1, 5) qanday sonlar beradi?', 'a': [{'t': '1, 2, 3, 4', 'c': True}, {'t': '1, 2, 3, 4, 5', 'c': False}, {'t': '0, 1, 2, 3, 4', 'c': False}, {'t': '5, 4, 3, 2, 1', 'c': False}]},
        {'t': 'range(0, 10, 2) nima beradi?', 'a': [{'t': '0, 2, 4, 6, 8', 'c': True}, {'t': '0, 1, 2, 3, 4, 5, 6, 7, 8, 9', 'c': False}, {'t': '2, 4, 6, 8, 10', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for x in "Python": nima qiladi?', 'a': [{'t': 'Har bir harfni takrorlaydi', 'c': True}, {'t': 'Faqat birinchi harfni oladi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'for siklida break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},
    {'n': 'Ro\'yxatlar (Lists) - Asoslar', 't': 25, 'o': 15, 'q': [
        {'t': 'Ro\'yxat (list) nima?', 'a': [{'t': 'Bir necha qiymatlarni saqlaydigan ma\'lumot turi', 'c': True}, {'t': 'Faqat bitta qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Ro\'yxat qanday yaratiladi?', 'a': [{'t': 'Kvadrat qavslar ichida: [1, 2, 3]', 'c': True}, {'t': 'Oddiy qavslar ichida: (1, 2, 3)', 'c': False}, {'t': 'Jingalak qavslar ichida: {1, 2, 3}', 'c': False}, {'t': 'Qo\'shtirnoqda: "1, 2, 3"', 'c': False}]},
        {'t': 'my_list = [1, 2, 3]; my_list[0] natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '0', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'my_list = [1, 2, 3]; my_list[-1] natijasi?', 'a': [{'t': '3', 'c': True}, {'t': '1', 'c': False}, {'t': '-1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'len([1, 2, 3, 4, 5]) natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '4', 'c': False}, {'t': '15', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ro\'yxatda turli xil ma\'lumot turlari bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin: [1, "salom", True]', 'c': True}, {'t': 'Yo\'q, faqat bir xil tur', 'c': False}, {'t': 'Faqat sonlar', 'c': False}, {'t': 'Faqat matnlar', 'c': False}]},
    ]},
    {'n': 'Ro\'yxat metodlari', 't': 25, 'o': 16, 'q': [
        {'t': 'Ro\'yxatga element qo\'shish uchun qaysi metod?', 'a': [{'t': 'append()', 'c': True}, {'t': 'add()', 'c': False}, {'t': 'insert_end()', 'c': False}, {'t': 'push()', 'c': False}]},
        {'t': 'my_list = [1, 2]; my_list.append(3) natijasi?', 'a': [{'t': '[1, 2, 3]', 'c': True}, {'t': '[1, 2]', 'c': False}, {'t': '[3, 1, 2]', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ro\'yxatdan element o\'chirish uchun?', 'a': [{'t': 'remove() yoki pop()', 'c': True}, {'t': 'delete()', 'c': False}, {'t': 'clear_one()', 'c': False}, {'t': 'erase()', 'c': False}]},
        {'t': 'my_list = [1, 2, 3]; my_list.pop() natijasi?', 'a': [{'t': '3 qaytaradi va ro\'yxatdan o\'chiradi', 'c': True}, {'t': 'Faqat 3 qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Ro\'yxatni saralash uchun?', 'a': [{'t': 'sort()', 'c': True}, {'t': 'order()', 'c': False}, {'t': 'arrange()', 'c': False}, {'t': 'organize()', 'c': False}]},
        {'t': 'Ro\'yxatni teskari aylantirish uchun?', 'a': [{'t': 'reverse()', 'c': True}, {'t': 'flip()', 'c': False}, {'t': 'backward()', 'c': False}, {'t': 'invert()', 'c': False}]},
    ]},
    {'n': 'Tuple (O\'zgarmas ro\'yxat)', 't': 20, 'o': 17, 'q': [
        {'t': 'Tuple nima?', 'a': [{'t': 'O\'zgarmas ro\'yxat', 'c': True}, {'t': 'O\'zgaruvchan ro\'yxat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Tuple qanday yaratiladi?', 'a': [{'t': 'Oddiy qavslar ichida: (1, 2, 3)', 'c': True}, {'t': 'Kvadrat qavslar ichida: [1, 2, 3]', 'c': False}, {'t': 'Jingalak qavslar ichida: {1, 2, 3}', 'c': False}, {'t': 'Qo\'shtirnoqda', 'c': False}]},
        {'t': 'my_tuple = (1, 2, 3); my_tuple[0] natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '0', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '(1)', 'c': False}]},
        {'t': 'Tuple elementini o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, o\'zgarmas', 'c': True}, {'t': 'Ha, o\'zgartirish mumkin', 'c': False}, {'t': 'Faqat ba\'zi elementlarni', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Tuple va list orasidagi asosiy farq?', 'a': [{'t': 'Tuple o\'zgarmas, list o\'zgaruvchan', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Tuple kattaroq', 'c': False}, {'t': 'List o\'zgarmas', 'c': False}]},
    ]},
    {'n': 'Set (To\'plam)', 't': 20, 'o': 18, 'q': [
        {'t': 'Set nima?', 'a': [{'t': 'Takrorlanmaydigan elementlar to\'plami', 'c': True}, {'t': 'Oddiy ro\'yxat', 'c': False}, {'t': 'O\'zgarmas ro\'yxat', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Set qanday yaratiladi?', 'a': [{'t': 'Jingalak qavslar ichida: {1, 2, 3}', 'c': True}, {'t': 'Kvadrat qavslar ichida: [1, 2, 3]', 'c': False}, {'t': 'Oddiy qavslar ichida: (1, 2, 3)', 'c': False}, {'t': 'Qo\'shtirnoqda', 'c': False}]},
        {'t': 'my_set = {1, 2, 2, 3}; print(my_set) natijasi?', 'a': [{'t': '{1, 2, 3}', 'c': True}, {'t': '{1, 2, 2, 3}', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '{3, 2, 1}', 'c': False}]},
        {'t': 'Set da indeks orqali element olish mumkinmi?', 'a': [{'t': 'Yo\'q, tartibsiz', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Faqat birinchi element', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Set ga element qo\'shish uchun?', 'a': [{'t': 'add()', 'c': True}, {'t': 'append()', 'c': False}, {'t': 'insert()', 'c': False}, {'t': 'push()', 'c': False}]},
    ]},
    {'n': 'Dictionary (Lug\'at)', 't': 25, 'o': 19, 'q': [
        {'t': 'Dictionary nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Oddiy ro\'yxat', 'c': False}, {'t': 'O\'zgarmas ro\'yxat', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Dictionary qanday yaratiladi?', 'a': [{'t': '{"kalit": "qiymat"}', 'c': True}, {'t': '["kalit", "qiymat"]', 'c': False}, {'t': '("kalit", "qiymat")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'my_dict = {"ism": "Ali"}; my_dict["ism"] natijasi?', 'a': [{'t': 'Ali', 'c': True}, {'t': 'ism', 'c': False}, {'t': '{"ism": "Ali"}', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Dictionary ga yangi element qo\'shish?', 'a': [{'t': 'my_dict["yangi"] = "qiymat"', 'c': True}, {'t': 'my_dict.add("yangi", "qiymat")', 'c': False}, {'t': 'my_dict.append("yangi")', 'c': False}, {'t': 'Qo\'shib bo\'lmaydi', 'c': False}]},
        {'t': 'Dictionary kalitlari qanday bo\'lishi kerak?', 'a': [{'t': 'O\'zgarmas (string, number, tuple)', 'c': True}, {'t': 'Har qanday tur', 'c': False}, {'t': 'Faqat string', 'c': False}, {'t': 'Faqat number', 'c': False}]},
        {'t': 'my_dict.keys() nima qaytaradi?', 'a': [{'t': 'Barcha kalitlarni', 'c': True}, {'t': 'Barcha qiymatlarni', 'c': False}, {'t': 'Birinchi kalitni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Funksiyalar - Asoslar', 't': 25, 'o': 20, 'q': [
        {'t': 'Funksiya nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Funksiya qanday yaratiladi?', 'a': [{'t': 'def kalit so\'zi bilan', 'c': True}, {'t': 'function kalit so\'zi bilan', 'c': False}, {'t': 'func kalit so\'zi bilan', 'c': False}, {'t': 'Avtomatik yaratiladi', 'c': False}]},
        {'t': 'def salom(): print("Salom") - bu funksiyani chaqirish?', 'a': [{'t': 'salom()', 'c': True}, {'t': 'salom', 'c': False}, {'t': 'call salom()', 'c': False}, {'t': 'run salom()', 'c': False}]},
        {'t': 'Funksiya parametri nima?', 'a': [{'t': 'Funksiyaga beriladigan qiymat', 'c': True}, {'t': 'Funksiya nomi', 'c': False}, {'t': 'Funksiya natijasi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'def qosh(a, b): return a + b - return nima qiladi?', 'a': [{'t': 'Natijani qaytaradi', 'c': True}, {'t': 'Natijani chiqaradi', 'c': False}, {'t': 'Funksiyani to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Funksiya parametrlari', 't': 25, 'o': 21, 'q': [
        {'t': 'Default parametr nima?', 'a': [{'t': 'Standart qiymatga ega parametr', 'c': True}, {'t': 'Majburiy parametr', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
        {'t': 'def salom(ism="Mehmon"): - "Mehmon" nima?', 'a': [{'t': 'Default qiymat', 'c': True}, {'t': 'Majburiy qiymat', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
        {'t': '*args nima uchun ishlatiladi?', 'a': [{'t': 'Istalgancha parametr qabul qilish uchun', 'c': True}, {'t': 'Faqat bitta parametr uchun', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
        {'t': '**kwargs nima uchun ishlatiladi?', 'a': [{'t': 'Kalit-qiymat parametrlar uchun', 'c': True}, {'t': 'Oddiy parametrlar uchun', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
        {'t': 'def func(a, b=5): func(3) - b ning qiymati?', 'a': [{'t': '5', 'c': True}, {'t': '3', 'c': False}, {'t': 'None', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Lambda funksiyalar', 't': 20, 'o': 22, 'q': [
        {'t': 'Lambda funksiya nima?', 'a': [{'t': 'Bir qatorli anonim funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Katta funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'lambda x: x * 2 - bu nima qiladi?', 'a': [{'t': 'x ni 2 ga ko\'paytiradi', 'c': True}, {'t': 'x ga 2 qo\'shadi', 'c': False}, {'t': 'x dan 2 ayiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Lambda funksiya nechta ifoda bo\'lishi mumkin?', 'a': [{'t': 'Faqat bitta', 'c': True}, {'t': 'Istalgancha', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qanday', 'c': False}]},
        {'t': 'f = lambda x, y: x + y; f(2, 3) natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '23', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'Lambda funksiya qachon ishlatiladi?', 'a': [{'t': 'Qisqa, bir martalik funksiyalar uchun', 'c': True}, {'t': 'Katta funksiyalar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}]},
    ]},
    {'n': 'Map, Filter, Reduce', 't': 25, 'o': 23, 'q': [
        {'t': 'map() funksiyasi nima qiladi?', 'a': [{'t': 'Har bir elementga funksiya qo\'llaydi', 'c': True}, {'t': 'Elementlarni filtrlaydi', 'c': False}, {'t': 'Elementlarni birlashtiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'list(map(lambda x: x*2, [1,2,3])) natijasi?', 'a': [{'t': '[2, 4, 6]', 'c': True}, {'t': '[1, 2, 3]', 'c': False}, {'t': '[3, 6, 9]', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'filter() funksiyasi nima qiladi?', 'a': [{'t': 'Shartga mos elementlarni tanlaydi', 'c': True}, {'t': 'Har bir elementga funksiya qo\'llaydi', 'c': False}, {'t': 'Elementlarni birlashtiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'list(filter(lambda x: x>2, [1,2,3,4])) natijasi?', 'a': [{'t': '[3, 4]', 'c': True}, {'t': '[1, 2]', 'c': False}, {'t': '[1, 2, 3, 4]', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'reduce() qaysi moduldan import qilinadi?', 'a': [{'t': 'functools', 'c': True}, {'t': 'math', 'c': False}, {'t': 'random', 'c': False}, {'t': 'os', 'c': False}]},
    ]},
    {'n': 'List Comprehension', 't': 25, 'o': 24, 'q': [
        {'t': 'List comprehension nima?', 'a': [{'t': 'Ro\'yxat yaratishning qisqa usuli', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': '[x*2 for x in range(3)] natijasi?', 'a': [{'t': '[0, 2, 4]', 'c': True}, {'t': '[0, 1, 2]', 'c': False}, {'t': '[2, 4, 6]', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '[x for x in range(5) if x%2==0] natijasi?', 'a': [{'t': '[0, 2, 4]', 'c': True}, {'t': '[1, 3]', 'c': False}, {'t': '[0, 1, 2, 3, 4]', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'List comprehension da if-else ishlatish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, faqat if', 'c': False}, {'t': 'Yo\'q, hech qanday shart yo\'q', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '[x if x>0 else 0 for x in [-1,2,-3,4]] natijasi?', 'a': [{'t': '[0, 2, 0, 4]', 'c': True}, {'t': '[-1, 2, -3, 4]', 'c': False}, {'t': '[2, 4]', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Modullar va import', 't': 20, 'o': 25, 'q': [
        {'t': 'Modul nima?', 'a': [{'t': 'Python kod fayli', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Modulni import qilish uchun?', 'a': [{'t': 'import modul_nomi', 'c': True}, {'t': 'include modul_nomi', 'c': False}, {'t': 'require modul_nomi', 'c': False}, {'t': 'use modul_nomi', 'c': False}]},
        {'t': 'import math; math.sqrt(16) natijasi?', 'a': [{'t': '4.0', 'c': True}, {'t': '16', 'c': False}, {'t': '256', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'from math import sqrt - bu nima?', 'a': [{'t': 'Faqat sqrt funksiyasini import qilish', 'c': True}, {'t': 'Butun math modulini import qilish', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'import math as m - "as" nima uchun?', 'a': [{'t': 'Qisqa nom berish uchun', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Math moduli', 't': 20, 'o': 26, 'q': [
        {'t': 'math.sqrt(25) natijasi?', 'a': [{'t': '5.0', 'c': True}, {'t': '25', 'c': False}, {'t': '625', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'math.pow(2, 3) natijasi?', 'a': [{'t': '8.0', 'c': True}, {'t': '6', 'c': False}, {'t': '9', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'math.ceil(4.3) natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '4', 'c': False}, {'t': '4.3', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'math.floor(4.7) natijasi?', 'a': [{'t': '4', 'c': True}, {'t': '5', 'c': False}, {'t': '4.7', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'math.pi nima?', 'a': [{'t': 'Pi soni (3.14159...)', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Operator', 'c': False}]},
    ]},
    {'n': 'Random moduli', 't': 20, 'o': 27, 'q': [
        {'t': 'random.randint(1, 10) nima qiladi?', 'a': [{'t': '1 dan 10 gacha tasodifiy butun son', 'c': True}, {'t': '1 dan 9 gacha tasodifiy son', 'c': False}, {'t': 'Har doim 1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'random.choice([1,2,3,4,5]) nima qiladi?', 'a': [{'t': 'Ro\'yxatdan tasodifiy element tanlaydi', 'c': True}, {'t': 'Birinchi elementni qaytaradi', 'c': False}, {'t': 'Oxirgi elementni qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'random.random() nima qaytaradi?', 'a': [{'t': '0 va 1 orasida tasodifiy son', 'c': True}, {'t': '0 dan 100 gacha tasodifiy son', 'c': False}, {'t': 'Har doim 0.5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'random.shuffle(my_list) nima qiladi?', 'a': [{'t': 'Ro\'yxatni aralashtirib yuboradi', 'c': True}, {'t': 'Ro\'yxatni saralaydi', 'c': False}, {'t': 'Ro\'yxatni teskari aylantiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'random modulini import qilish?', 'a': [{'t': 'import random', 'c': True}, {'t': 'include random', 'c': False}, {'t': 'using random', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
    ]},
    {'n': 'Datetime moduli', 't': 20, 'o': 28, 'q': [
        {'t': 'datetime.datetime.now() nima qaytaradi?', 'a': [{'t': 'Hozirgi sana va vaqt', 'c': True}, {'t': 'Faqat sana', 'c': False}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'datetime.date.today() nima qaytaradi?', 'a': [{'t': 'Bugungi sana', 'c': True}, {'t': 'Hozirgi vaqt', 'c': False}, {'t': 'Kecha sanasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'datetime modulini import qilish?', 'a': [{'t': 'import datetime', 'c': True}, {'t': 'include datetime', 'c': False}, {'t': 'using datetime', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'datetime.timedelta nima uchun ishlatiladi?', 'a': [{'t': 'Vaqt farqini hisoblash uchun', 'c': True}, {'t': 'Faqat sana olish uchun', 'c': False}, {'t': 'Faqat vaqt olish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Sanani formatlash uchun qaysi metod?', 'a': [{'t': 'strftime()', 'c': True}, {'t': 'format()', 'c': False}, {'t': 'toString()', 'c': False}, {'t': 'print()', 'c': False}]},
    ]},
    {'n': 'Fayl bilan ishlash - O\'qish', 't': 25, 'o': 29, 'q': [
        {'t': 'Faylni ochish uchun qaysi funksiya?', 'a': [{'t': 'open()', 'c': True}, {'t': 'read()', 'c': False}, {'t': 'file()', 'c': False}, {'t': 'load()', 'c': False}]},
        {'t': 'open("file.txt", "r") - "r" nima?', 'a': [{'t': 'O\'qish rejimi (read)', 'c': True}, {'t': 'Yozish rejimi', 'c': False}, {'t': 'Qo\'shish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Faylni o\'qish uchun qaysi metod?', 'a': [{'t': 'read()', 'c': True}, {'t': 'open()', 'c': False}, {'t': 'get()', 'c': False}, {'t': 'load()', 'c': False}]},
        {'t': 'Faylni qator-qator o\'qish uchun?', 'a': [{'t': 'readlines() yoki for loop', 'c': True}, {'t': 'Faqat read()', 'c': False}, {'t': 'Faqat readline()', 'c': False}, {'t': 'Buning imkoni yo\'q', 'c': False}]},
        {'t': 'Faylni yopish uchun?', 'a': [{'t': 'close()', 'c': True}, {'t': 'end()', 'c': False}, {'t': 'stop()', 'c': False}, {'t': 'Avtomatik yopiladi', 'c': False}]},
    ]},
    {'n': 'Fayl bilan ishlash - Yozish', 't': 25, 'o': 30, 'q': [
        {'t': 'open("file.txt", "w") - "w" nima?', 'a': [{'t': 'Yozish rejimi (write)', 'c': True}, {'t': 'O\'qish rejimi', 'c': False}, {'t': 'Qo\'shish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"w" rejimida fayl mavjud bo\'lsa nima bo\'ladi?', 'a': [{'t': 'Fayl tozalanadi va qayta yoziladi', 'c': True}, {'t': 'Faylga qo\'shiladi', 'c': False}, {'t': 'Xatolik beradi', 'c': False}, {'t': 'Hech narsa bo\'lmaydi', 'c': False}]},
        {'t': 'open("file.txt", "a") - "a" nima?', 'a': [{'t': 'Qo\'shish rejimi (append)', 'c': True}, {'t': 'Yozish rejimi', 'c': False}, {'t': 'O\'qish rejimi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Faylga yozish uchun qaysi metod?', 'a': [{'t': 'write()', 'c': True}, {'t': 'print()', 'c': False}, {'t': 'save()', 'c': False}, {'t': 'put()', 'c': False}]},
        {'t': 'with open("file.txt") as f: ning afzalligi?', 'a': [{'t': 'Avtomatik yopiladi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xatolik bermaydi', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
    ]},
    {'n': 'Xatolar bilan ishlash - Try/Except', 't': 25, 'o': 31, 'q': [
        {'t': 'try-except nima uchun ishlatiladi?', 'a': [{'t': 'Xatolarni ushlash va boshqarish uchun', 'c': True}, {'t': 'Funksiya yaratish uchun', 'c': False}, {'t': 'Sikl yaratish uchun', 'c': False}, {'t': 'Ma\'lumot saqlash uchun', 'c': False}]},
        {'t': 'try blokida xato bo\'lsa nima bo\'ladi?', 'a': [{'t': 'except bloki ishlaydi', 'c': True}, {'t': 'Dastur to\'xtaydi', 'c': False}, {'t': 'Xato e\'tiborga olinmaydi', 'c': False}, {'t': 'Qayta urinadi', 'c': False}]},
        {'t': 'except Exception as e: - "e" nima?', 'a': [{'t': 'Xato haqida ma\'lumot', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'finally bloki qachon ishlaydi?', 'a': [{'t': 'Har doim (xato bo\'lsa ham, bo\'lmasa ham)', 'c': True}, {'t': 'Faqat xato bo\'lsa', 'c': False}, {'t': 'Faqat xato bo\'lmasa', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'raise nima uchun ishlatiladi?', 'a': [{'t': 'Xato chiqarish uchun', 'c': True}, {'t': 'Xatoni ushlash uchun', 'c': False}, {'t': 'Funksiya yaratish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},
    {'n': 'Xato turlari', 't': 20, 'o': 32, 'q': [
        {'t': 'SyntaxError qachon yuzaga keladi?', 'a': [{'t': 'Kod sintaksisi noto\'g\'ri bo\'lsa', 'c': True}, {'t': 'O\'zgaruvchi topilmasa', 'c': False}, {'t': 'Nolga bo\'lishda', 'c': False}, {'t': 'Fayl topilmasa', 'c': False}]},
        {'t': 'NameError qachon yuzaga keladi?', 'a': [{'t': 'O\'zgaruvchi yoki funksiya topilmasa', 'c': True}, {'t': 'Sintaksis xato bo\'lsa', 'c': False}, {'t': 'Nolga bo\'lishda', 'c': False}, {'t': 'Fayl topilmasa', 'c': False}]},
        {'t': 'ZeroDivisionError qachon yuzaga keladi?', 'a': [{'t': 'Nolga bo\'lishda', 'c': True}, {'t': 'O\'zgaruvchi topilmasa', 'c': False}, {'t': 'Sintaksis xato bo\'lsa', 'c': False}, {'t': 'Fayl topilmasa', 'c': False}]},
        {'t': 'FileNotFoundError qachon yuzaga keladi?', 'a': [{'t': 'Fayl topilmasa', 'c': True}, {'t': 'Nolga bo\'lishda', 'c': False}, {'t': 'O\'zgaruvchi topilmasa', 'c': False}, {'t': 'Sintaksis xato bo\'lsa', 'c': False}]},
        {'t': 'TypeError qachon yuzaga keladi?', 'a': [{'t': 'Noto\'g\'ri ma\'lumot turi ishlatilsa', 'c': True}, {'t': 'Fayl topilmasa', 'c': False}, {'t': 'Nolga bo\'lishda', 'c': False}, {'t': 'O\'zgaruvchi topilmasa', 'c': False}]},
    ]},
    {'n': 'OOP - Klasslar va Obyektlar', 't': 30, 'o': 33, 'q': [
        {'t': 'Klass nima?', 'a': [{'t': 'Obyektlar uchun shablon', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Obyekt nima?', 'a': [{'t': 'Klassdan yaratilgan nusxa', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Klass qanday yaratiladi?', 'a': [{'t': 'class kalit so\'zi bilan', 'c': True}, {'t': 'def kalit so\'zi bilan', 'c': False}, {'t': 'function kalit so\'zi bilan', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': '__init__ metodi nima?', 'a': [{'t': 'Konstruktor (obyekt yaratilganda chaqiriladi)', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Destruktor', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'self nima?', 'a': [{'t': 'Obyektning o\'ziga havola', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Kalit so\'z', 'c': False}]},
        {'t': 'Obyekt qanday yaratiladi?', 'a': [{'t': 'obj = ClassName()', 'c': True}, {'t': 'obj = new ClassName()', 'c': False}, {'t': 'obj = create ClassName()', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
    ]},
    {'n': 'OOP - Atributlar va Metodlar', 't': 25, 'o': 34, 'q': [
        {'t': 'Atribut nima?', 'a': [{'t': 'Klass yoki obyekt o\'zgaruvchisi', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Metod nima?', 'a': [{'t': 'Klass ichidagi funksiya', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Modul', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Instance atribut nima?', 'a': [{'t': 'Har bir obyektga xos atribut', 'c': True}, {'t': 'Barcha obyektlar uchun umumiy', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Class atribut nima?', 'a': [{'t': 'Barcha obyektlar uchun umumiy atribut', 'c': True}, {'t': 'Har bir obyektga xos', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Obyekt atributiga qanday murojaat qilinadi?', 'a': [{'t': 'obj.atribut', 'c': True}, {'t': 'obj->atribut', 'c': False}, {'t': 'obj[atribut]', 'c': False}, {'t': 'obj(atribut)', 'c': False}]},
    ]},
    {'n': 'OOP - Inheritance (Meros)', 't': 25, 'o': 35, 'q': [
        {'t': 'Inheritance nima?', 'a': [{'t': 'Bir klassdan boshqa klass yaratish', 'c': True}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Modul yaratish', 'c': False}]},
        {'t': 'Parent class nima?', 'a': [{'t': 'Asosiy klass (meros beriladigan)', 'c': True}, {'t': 'Yangi klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Child class nima?', 'a': [{'t': 'Meros oluvchi klass', 'c': True}, {'t': 'Asosiy klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'class Child(Parent): - bu nima?', 'a': [{'t': 'Child klassi Parent dan meros oladi', 'c': True}, {'t': 'Parent klassi Child dan meros oladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'super() nima uchun ishlatiladi?', 'a': [{'t': 'Parent klass metodlariga murojaat qilish', 'c': True}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OOP - Encapsulation', 't': 25, 'o': 36, 'q': [
        {'t': 'Encapsulation nima?', 'a': [{'t': 'Ma\'lumotlarni yashirish va himoya qilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Polimorfizm', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'Private atribut qanday yaratiladi?', 'a': [{'t': 'Ikki pastki chiziq bilan: __atribut', 'c': True}, {'t': 'Bir pastki chiziq bilan: _atribut', 'c': False}, {'t': 'Oddiy: atribut', 'c': False}, {'t': 'Yaratib bo\'lmaydi', 'c': False}]},
        {'t': '__atribut ga tashqaridan murojaat qilish mumkinmi?', 'a': [{'t': 'Yo\'q, private', 'c': True}, {'t': 'Ha, erkin murojaat qilish mumkin', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Getter metod nima uchun?', 'a': [{'t': 'Private atributni o\'qish uchun', 'c': True}, {'t': 'Private atributni o\'zgartirish uchun', 'c': False}, {'t': 'Obyekt yaratish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Setter metod nima uchun?', 'a': [{'t': 'Private atributni o\'zgartirish uchun', 'c': True}, {'t': 'Private atributni o\'qish uchun', 'c': False}, {'t': 'Obyekt yaratish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OOP - Polymorphism', 't': 25, 'o': 37, 'q': [
        {'t': 'Polymorphism nima?', 'a': [{'t': 'Bir xil nom, turli xil bajarilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Ma\'lumotlarni yashirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'Method overriding nima?', 'a': [{'t': 'Parent metodni child da qayta yozish', 'c': True}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Metodni o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir xil nomli metodlar turli klasslarda bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, polymorphism', 'c': True}, {'t': 'Yo\'q, xatolik', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Duck typing nima?', 'a': [{'t': 'Obyekt turi emas, xatti-harakati muhim', 'c': True}, {'t': 'Obyekt turi muhim', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Polymorphism ning afzalligi?', 'a': [{'t': 'Kodni qayta ishlatish va moslashuvchanlik', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},
    {'n': 'Dekoratorlar', 't': 25, 'o': 38, 'q': [
        {'t': 'Dekorator nima?', 'a': [{'t': 'Funksiyani o\'zgartiruvchi funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': '@decorator sintaksisi nima uchun?', 'a': [{'t': 'Dekoratorni qo\'llash uchun', 'c': True}, {'t': 'Izoh yozish uchun', 'c': False}, {'t': 'Funksiya yaratish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '@staticmethod nima?', 'a': [{'t': 'self ni talab qilmaydigan metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Private metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '@classmethod nima?', 'a': [{'t': 'cls parametri oladigan metod', 'c': True}, {'t': 'self parametri oladigan metod', 'c': False}, {'t': 'Parametrsiz metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '@property nima uchun?', 'a': [{'t': 'Metodga atribut kabi murojaat qilish', 'c': True}, {'t': 'Private qilish uchun', 'c': False}, {'t': 'Static qilish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Generatorlar', 't': 25, 'o': 39, 'q': [
        {'t': 'Generator nima?', 'a': [{'t': 'Qiymatlarni ketma-ket ishlab chiqaruvchi funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'yield kalit so\'zi nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi va to\'xtaydi', 'c': True}, {'t': 'return bilan bir xil', 'c': False}, {'t': 'Funksiyani to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Generator va oddiy funksiya farqi?', 'a': [{'t': 'Generator yield ishlatadi, funksiya return', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Generator tezroq', 'c': False}, {'t': 'Funksiya tezroq', 'c': False}]},
        {'t': 'Generator ning afzalligi?', 'a': [{'t': 'Kam xotira ishlatadi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Oson yoziladi', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'next() funksiyasi nima qiladi?', 'a': [{'t': 'Generatordan keyingi qiymatni oladi', 'c': True}, {'t': 'Generatorni to\'xtatadi', 'c': False}, {'t': 'Generatorni qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Iteratorlar', 't': 20, 'o': 40, 'q': [
        {'t': 'Iterator nima?', 'a': [{'t': 'Ketma-ketlik bo\'ylab harakatlanish imkonini beruvchi obyekt', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': '__iter__() metodi nima qaytaradi?', 'a': [{'t': 'Iterator obyektini', 'c': True}, {'t': 'Qiymat', 'c': False}, {'t': 'None', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '__next__() metodi nima qiladi?', 'a': [{'t': 'Keyingi qiymatni qaytaradi', 'c': True}, {'t': 'Birinchi qiymatni qaytaradi', 'c': False}, {'t': 'Oxirgi qiymatni qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'iter() funksiyasi nima qiladi?', 'a': [{'t': 'Obyektdan iterator yaratadi', 'c': True}, {'t': 'Obyektni o\'chiradi', 'c': False}, {'t': 'Obyektni ko\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'StopIteration nima?', 'a': [{'t': 'Iterator tugaganda chiqadigan xato', 'c': True}, {'t': 'Oddiy xato', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}]},
    ]},
    {'n': 'Regular Expressions (Regex)', 't': 30, 'o': 41, 'q': [
        {'t': 'Regex nima?', 'a': [{'t': 'Matnlarni qidirish va tekshirish uchun shablon', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'Regex uchun qaysi modul ishlatiladi?', 'a': [{'t': 're', 'c': True}, {'t': 'regex', 'c': False}, {'t': 'pattern', 'c': False}, {'t': 'search', 'c': False}]},
        {'t': 're.search() nima qiladi?', 'a': [{'t': 'Matnda shablon qidiradi', 'c': True}, {'t': 'Matnni o\'zgartiradi', 'c': False}, {'t': 'Matnni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 're.match() nima qiladi?', 'a': [{'t': 'Matn boshidan shablon qidiradi', 'c': True}, {'t': 'Matn oxiridan qidiradi', 'c': False}, {'t': 'Butun matnda qidiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 're.findall() nima qaytaradi?', 'a': [{'t': 'Barcha mos kelishlarni ro\'yxat sifatida', 'c': True}, {'t': 'Faqat birinchi mos kelishni', 'c': False}, {'t': 'True yoki False', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'JSON bilan ishlash', 't': 25, 'o': 42, 'q': [
        {'t': 'JSON nima?', 'a': [{'t': 'Ma\'lumot almashinuv formati', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Fayl turi', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'JSON uchun qaysi modul ishlatiladi?', 'a': [{'t': 'json', 'c': True}, {'t': 'data', 'c': False}, {'t': 'file', 'c': False}, {'t': 'parse', 'c': False}]},
        {'t': 'json.dumps() nima qiladi?', 'a': [{'t': 'Python obyektini JSON stringga aylantiradi', 'c': True}, {'t': 'JSON ni Python obyektiga aylantiradi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'json.loads() nima qiladi?', 'a': [{'t': 'JSON stringni Python obyektiga aylantiradi', 'c': True}, {'t': 'Python obyektini JSON ga aylantiradi', 'c': False}, {'t': 'Fayldan o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'json.dump() va json.dumps() farqi?', 'a': [{'t': 'dump() faylga yozadi, dumps() string qaytaradi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'dumps() faylga yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OS moduli', 't': 25, 'o': 43, 'q': [
        {'t': 'os moduli nima uchun?', 'a': [{'t': 'Operatsion tizim bilan ishlash uchun', 'c': True}, {'t': 'Faqat fayllar bilan ishlash', 'c': False}, {'t': 'Faqat papkalar bilan ishlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'os.getcwd() nima qaytaradi?', 'a': [{'t': 'Joriy ishchi papka yo\'lini', 'c': True}, {'t': 'Uy papka yo\'lini', 'c': False}, {'t': 'Fayl nomini', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'os.listdir() nima qiladi?', 'a': [{'t': 'Papkadagi fayllar ro\'yxatini qaytaradi', 'c': True}, {'t': 'Yangi papka yaratadi', 'c': False}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'os.mkdir() nima qiladi?', 'a': [{'t': 'Yangi papka yaratadi', 'c': True}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Papka nomini o\'zgartiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'os.remove() nima qiladi?', 'a': [{'t': 'Faylni o\'chiradi', 'c': True}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Sys moduli', 't': 20, 'o': 44, 'q': [
        {'t': 'sys moduli nima uchun?', 'a': [{'t': 'Python interpretatori bilan ishlash', 'c': True}, {'t': 'Faqat fayllar bilan ishlash', 'c': False}, {'t': 'Faqat matematik amallar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sys.argv nima?', 'a': [{'t': 'Buyruq qatori argumentlari ro\'yxati', 'c': True}, {'t': 'Python versiyasi', 'c': False}, {'t': 'Fayl yo\'li', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sys.exit() nima qiladi?', 'a': [{'t': 'Dasturni to\'xtatadi', 'c': True}, {'t': 'Dasturni qayta boshlaydi', 'c': False}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sys.version nima?', 'a': [{'t': 'Python versiyasi haqida ma\'lumot', 'c': True}, {'t': 'Modul versiyasi', 'c': False}, {'t': 'Fayl versiyasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sys.path nima?', 'a': [{'t': 'Modullar qidiriladi gan yo\'llar ro\'yxati', 'c': True}, {'t': 'Joriy fayl yo\'li', 'c': False}, {'t': 'Uy papka yo\'li', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Collections moduli', 't': 25, 'o': 45, 'q': [
        {'t': 'collections moduli nima uchun?', 'a': [{'t': 'Maxsus ma\'lumot tuzilmalari uchun', 'c': True}, {'t': 'Faqat ro\'yxatlar uchun', 'c': False}, {'t': 'Faqat lug\'atlar uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Counter nima qiladi?', 'a': [{'t': 'Elementlarni sanaydi', 'c': True}, {'t': 'Elementlarni saralaydi', 'c': False}, {'t': 'Elementlarni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'defaultdict nima?', 'a': [{'t': 'Default qiymatli lug\'at', 'c': True}, {'t': 'Oddiy lug\'at', 'c': False}, {'t': 'Ro\'yxat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'OrderedDict nima?', 'a': [{'t': 'Tartibli lug\'at', 'c': True}, {'t': 'Tartibsiz lug\'at', 'c': False}, {'t': 'Ro\'yxat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'deque nima?', 'a': [{'t': 'Ikki tomonlama navbat', 'c': True}, {'t': 'Oddiy ro\'yxat', 'c': False}, {'t': 'Lug\'at', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Itertools moduli', 't': 25, 'o': 46, 'q': [
        {'t': 'itertools moduli nima uchun?', 'a': [{'t': 'Iterator yaratish va boshqarish', 'c': True}, {'t': 'Faqat ro\'yxatlar uchun', 'c': False}, {'t': 'Faqat lug\'atlar uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'itertools.count() nima qiladi?', 'a': [{'t': 'Cheksiz sanash', 'c': True}, {'t': 'Elementlarni sanaydi', 'c': False}, {'t': 'Ro\'yxat yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'itertools.cycle() nima qiladi?', 'a': [{'t': 'Ketma-ketlikni cheksiz takrorlaydi', 'c': True}, {'t': 'Bir marta takrorlaydi', 'c': False}, {'t': 'Takrorlamaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'itertools.chain() nima qiladi?', 'a': [{'t': 'Bir necha iteratorni birlashtiradi', 'c': True}, {'t': 'Iteratorni bo\'ladi', 'c': False}, {'t': 'Iteratorni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'itertools.combinations() nima qiladi?', 'a': [{'t': 'Kombinatsiyalar yaratadi', 'c': True}, {'t': 'Permutatsiyalar yaratadi', 'c': False}, {'t': 'Ro\'yxat yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Multithreading', 't': 30, 'o': 47, 'q': [
        {'t': 'Thread nima?', 'a': [{'t': 'Parallel bajariluvchi kod oqimi', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'threading moduli nima uchun?', 'a': [{'t': 'Ko\'p oqimli dasturlash uchun', 'c': True}, {'t': 'Faqat bir oqimli dasturlash', 'c': False}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Thread qanday yaratiladi?', 'a': [{'t': 'threading.Thread(target=func)', 'c': True}, {'t': 'thread.create(func)', 'c': False}, {'t': 'new Thread(func)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'thread.start() nima qiladi?', 'a': [{'t': 'Thread ni ishga tushiradi', 'c': True}, {'t': 'Thread ni to\'xtatadi', 'c': False}, {'t': 'Thread ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'thread.join() nima qiladi?', 'a': [{'t': 'Thread tugashini kutadi', 'c': True}, {'t': 'Thread ni to\'xtatadi', 'c': False}, {'t': 'Thread ni boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Multiprocessing', 't': 30, 'o': 48, 'q': [
        {'t': 'Process nima?', 'a': [{'t': 'Alohida xotiraga ega bajariluvchi dastur', 'c': True}, {'t': 'Thread bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}]},
        {'t': 'multiprocessing moduli nima uchun?', 'a': [{'t': 'Ko\'p jarayonli dasturlash uchun', 'c': True}, {'t': 'Faqat bir jarayonli dasturlash', 'c': False}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Process va Thread farqi?', 'a': [{'t': 'Process alohida xotiraga ega, Thread umumiy', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Thread alohida xotiraga ega', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Process qanday yaratiladi?', 'a': [{'t': 'multiprocessing.Process(target=func)', 'c': True}, {'t': 'process.create(func)', 'c': False}, {'t': 'new Process(func)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Multiprocessing ning afzalligi?', 'a': [{'t': 'Haqiqiy parallel bajarilish', 'c': True}, {'t': 'Kam xotira', 'c': False}, {'t': 'Oson yoziladi', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},
    {'n': 'Async/Await', 't': 30, 'o': 49, 'q': [
        {'t': 'Async dasturlash nima?', 'a': [{'t': 'Asinxron (kutmasdan) bajarilish', 'c': True}, {'t': 'Sinxron bajarilish', 'c': False}, {'t': 'Parallel bajarilish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'async def nima?', 'a': [{'t': 'Asinxron funksiya yaratish', 'c': True}, {'t': 'Oddiy funksiya yaratish', 'c': False}, {'t': 'Klass yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'await nima qiladi?', 'a': [{'t': 'Asinxron operatsiya tugashini kutadi', 'c': True}, {'t': 'Operatsiyani to\'xtatadi', 'c': False}, {'t': 'Operatsiyani boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'asyncio moduli nima uchun?', 'a': [{'t': 'Asinxron dasturlash uchun', 'c': True}, {'t': 'Sinxron dasturlash uchun', 'c': False}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'asyncio.run() nima qiladi?', 'a': [{'t': 'Asinxron funksiyani ishga tushiradi', 'c': True}, {'t': 'Oddiy funksiyani ishga tushiradi', 'c': False}, {'t': 'Funksiyani to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Virtual Environment', 't': 25, 'o': 50, 'q': [
        {'t': 'Virtual environment nima?', 'a': [{'t': 'Izolyatsiya qilingan Python muhiti', 'c': True}, {'t': 'Oddiy papka', 'c': False}, {'t': 'Modul', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Virtual environment nima uchun kerak?', 'a': [{'t': 'Loyihalar uchun alohida kutubxonalar', 'c': True}, {'t': 'Tezroq ishlash uchun', 'c': False}, {'t': 'Kam xotira uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Virtual environment yaratish (Python 3)?', 'a': [{'t': 'python -m venv myenv', 'c': True}, {'t': 'create venv myenv', 'c': False}, {'t': 'new venv myenv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Virtual environment faollashtirish (Windows)?', 'a': [{'t': 'myenv\\Scripts\\activate', 'c': True}, {'t': 'source myenv/bin/activate', 'c': False}, {'t': 'activate myenv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Virtual environment faollashtirish (Linux/Mac)?', 'a': [{'t': 'source myenv/bin/activate', 'c': True}, {'t': 'myenv\\Scripts\\activate', 'c': False}, {'t': 'activate myenv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Pip - Paket menejeri', 't': 25, 'o': 51, 'q': [
        {'t': 'pip nima?', 'a': [{'t': 'Python paketlarini o\'rnatish vositasi', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Modul', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Paket o\'rnatish buyrug\'i?', 'a': [{'t': 'pip install paket_nomi', 'c': True}, {'t': 'pip get paket_nomi', 'c': False}, {'t': 'pip download paket_nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Paketni o\'chirish buyrug\'i?', 'a': [{'t': 'pip uninstall paket_nomi', 'c': True}, {'t': 'pip remove paket_nomi', 'c': False}, {'t': 'pip delete paket_nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'O\'rnatilgan paketlar ro\'yxati?', 'a': [{'t': 'pip list', 'c': True}, {'t': 'pip show', 'c': False}, {'t': 'pip packages', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'requirements.txt nima uchun?', 'a': [{'t': 'Loyiha bog\'liqliklarini saqlash', 'c': True}, {'t': 'Kod yozish uchun', 'c': False}, {'t': 'Test yozish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Requests kutubxonasi', 't': 25, 'o': 52, 'q': [
        {'t': 'requests kutubxonasi nima uchun?', 'a': [{'t': 'HTTP so\'rovlar yuborish uchun', 'c': True}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'GET so\'rov yuborish?', 'a': [{'t': 'requests.get(url)', 'c': True}, {'t': 'requests.send(url)', 'c': False}, {'t': 'requests.fetch(url)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'POST so\'rov yuborish?', 'a': [{'t': 'requests.post(url, data=data)', 'c': True}, {'t': 'requests.send(url, data)', 'c': False}, {'t': 'requests.put(url, data)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'response.status_code nima?', 'a': [{'t': 'HTTP javob kodi (200, 404, ...)', 'c': True}, {'t': 'Javob matni', 'c': False}, {'t': 'Javob vaqti', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'response.json() nima qiladi?', 'a': [{'t': 'JSON javobni Python obyektiga aylantiradi', 'c': True}, {'t': 'Javobni matn sifatida qaytaradi', 'c': False}, {'t': 'Javobni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'BeautifulSoup - Web Scraping', 't': 30, 'o': 53, 'q': [
        {'t': 'BeautifulSoup nima uchun?', 'a': [{'t': 'HTML/XML dan ma\'lumot olish', 'c': True}, {'t': 'HTTP so\'rovlar yuborish', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'BeautifulSoup obyekti yaratish?', 'a': [{'t': 'BeautifulSoup(html, "html.parser")', 'c': True}, {'t': 'BeautifulSoup.parse(html)', 'c': False}, {'t': 'parse(html)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'soup.find() nima qiladi?', 'a': [{'t': 'Birinchi mos elementni topadi', 'c': True}, {'t': 'Barcha mos elementlarni topadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'soup.find_all() nima qiladi?', 'a': [{'t': 'Barcha mos elementlarni topadi', 'c': True}, {'t': 'Faqat birinchi elementni topadi', 'c': False}, {'t': 'Elementlarni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'element.text nima qaytaradi?', 'a': [{'t': 'Element ichidagi matnni', 'c': True}, {'t': 'Element nomini', 'c': False}, {'t': 'Element atributlarini', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Pandas - Ma\'lumotlar tahlili', 't': 30, 'o': 54, 'q': [
        {'t': 'Pandas nima uchun?', 'a': [{'t': 'Ma\'lumotlar tahlili va ishlov berish', 'c': True}, {'t': 'Web scraping', 'c': False}, {'t': 'HTTP so\'rovlar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'DataFrame nima?', 'a': [{'t': 'Jadval ko\'rinishidagi ma\'lumot tuzilmasi', 'c': True}, {'t': 'Oddiy ro\'yxat', 'c': False}, {'t': 'Lug\'at', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'CSV faylni o\'qish?', 'a': [{'t': 'pd.read_csv("file.csv")', 'c': True}, {'t': 'pd.open("file.csv")', 'c': False}, {'t': 'pd.load("file.csv")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'df.head() nima qiladi?', 'a': [{'t': 'Birinchi 5 qatorni ko\'rsatadi', 'c': True}, {'t': 'Oxirgi 5 qatorni ko\'rsatadi', 'c': False}, {'t': 'Barcha qatorlarni ko\'rsatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'df.describe() nima qiladi?', 'a': [{'t': 'Statistik ma\'lumotlarni ko\'rsatadi', 'c': True}, {'t': 'Faqat birinchi qatorni ko\'rsatadi', 'c': False}, {'t': 'Ma\'lumotlarni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'NumPy - Raqamli hisoblashlar', 't': 30, 'o': 55, 'q': [
        {'t': 'NumPy nima uchun?', 'a': [{'t': 'Raqamli hisoblashlar va massivlar', 'c': True}, {'t': 'Web scraping', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'NumPy array yaratish?', 'a': [{'t': 'np.array([1, 2, 3])', 'c': True}, {'t': 'np.list([1, 2, 3])', 'c': False}, {'t': 'np.create([1, 2, 3])', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'np.zeros(5) nima yaratadi?', 'a': [{'t': '5 ta noldan iborat massiv', 'c': True}, {'t': '5 ta birdan iborat massiv', 'c': False}, {'t': 'Bo\'sh massiv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'np.ones(3) nima yaratadi?', 'a': [{'t': '3 ta birdan iborat massiv', 'c': True}, {'t': '3 ta noldan iborat massiv', 'c': False}, {'t': 'Bo\'sh massiv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'NumPy array va Python list farqi?', 'a': [{'t': 'NumPy tezroq va ko\'proq funksiyalar', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'List tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Matplotlib - Grafiklar', 't': 30, 'o': 56, 'q': [
        {'t': 'Matplotlib nima uchun?', 'a': [{'t': 'Grafiklar va diagrammalar chizish', 'c': True}, {'t': 'Ma\'lumotlar tahlili', 'c': False}, {'t': 'Web scraping', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Oddiy chiziq grafigi chizish?', 'a': [{'t': 'plt.plot(x, y)', 'c': True}, {'t': 'plt.draw(x, y)', 'c': False}, {'t': 'plt.line(x, y)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Grafikni ko\'rsatish?', 'a': [{'t': 'plt.show()', 'c': True}, {'t': 'plt.display()', 'c': False}, {'t': 'plt.view()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Grafik sarlavhasi qo\'shish?', 'a': [{'t': 'plt.title("Sarlavha")', 'c': True}, {'t': 'plt.header("Sarlavha")', 'c': False}, {'t': 'plt.name("Sarlavha")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Stolbchali diagramma chizish?', 'a': [{'t': 'plt.bar(x, y)', 'c': True}, {'t': 'plt.column(x, y)', 'c': False}, {'t': 'plt.histogram(x, y)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Flask - Web Framework', 't': 30, 'o': 57, 'q': [
        {'t': 'Flask nima?', 'a': [{'t': 'Python web framework', 'c': True}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Grafik kutubxona', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Flask ilovasi yaratish?', 'a': [{'t': 'app = Flask(__name__)', 'c': True}, {'t': 'app = Flask.create()', 'c': False}, {'t': 'app = new Flask()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '@app.route("/") nima?', 'a': [{'t': 'URL yo\'lini belgilash', 'c': True}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Sahifa yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Flask ilovasini ishga tushirish?', 'a': [{'t': 'app.run()', 'c': True}, {'t': 'app.start()', 'c': False}, {'t': 'app.execute()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Flask da shablon qaytarish?', 'a': [{'t': 'return render_template("file.html")', 'c': True}, {'t': 'return template("file.html")', 'c': False}, {'t': 'return html("file.html")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Django - Web Framework', 't': 30, 'o': 58, 'q': [
        {'t': 'Django nima?', 'a': [{'t': 'To\'liq funksional Python web framework', 'c': True}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Grafik kutubxona', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Django loyihasi yaratish?', 'a': [{'t': 'django-admin startproject myproject', 'c': True}, {'t': 'django create myproject', 'c': False}, {'t': 'django new myproject', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Django ilovasini ishga tushirish?', 'a': [{'t': 'python manage.py runserver', 'c': True}, {'t': 'django run', 'c': False}, {'t': 'python start.py', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Django da model nima?', 'a': [{'t': 'Ma\'lumotlar bazasi jadvali', 'c': True}, {'t': 'HTML shablon', 'c': False}, {'t': 'URL yo\'l', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Migratsiya yaratish?', 'a': [{'t': 'python manage.py makemigrations', 'c': True}, {'t': 'python manage.py migrate', 'c': False}, {'t': 'django migrate', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'SQLite - Ma\'lumotlar bazasi', 't': 30, 'o': 59, 'q': [
        {'t': 'SQLite nima?', 'a': [{'t': 'Yengil ma\'lumotlar bazasi', 'c': True}, {'t': 'Web framework', 'c': False}, {'t': 'Grafik kutubxona', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'SQLite ga ulanish?', 'a': [{'t': 'sqlite3.connect("db.db")', 'c': True}, {'t': 'sqlite3.open("db.db")', 'c': False}, {'t': 'sqlite3.create("db.db")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'SQL so\'rov bajarish?', 'a': [{'t': 'cursor.execute("SELECT * FROM table")', 'c': True}, {'t': 'cursor.query("SELECT * FROM table")', 'c': False}, {'t': 'cursor.run("SELECT * FROM table")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'O\'zgarishlarni saqlash?', 'a': [{'t': 'conn.commit()', 'c': True}, {'t': 'conn.save()', 'c': False}, {'t': 'conn.write()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ulanishni yopish?', 'a': [{'t': 'conn.close()', 'c': True}, {'t': 'conn.end()', 'c': False}, {'t': 'conn.stop()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Pytest - Test yozish', 't': 30, 'o': 60, 'q': [
        {'t': 'Pytest nima uchun?', 'a': [{'t': 'Avtomatik testlar yozish', 'c': True}, {'t': 'Web dasturlash', 'c': False}, {'t': 'Ma\'lumotlar tahlili', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Test funksiyasi qanday nomlanadi?', 'a': [{'t': 'test_ bilan boshlanadi', 'c': True}, {'t': 'func_ bilan boshlanadi', 'c': False}, {'t': 'check_ bilan boshlanadi', 'c': False}, {'t': 'Istalgan nom', 'c': False}]},
        {'t': 'assert nima qiladi?', 'a': [{'t': 'Shartni tekshiradi', 'c': True}, {'t': 'Funksiya yaratadi', 'c': False}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Testlarni ishga tushirish?', 'a': [{'t': 'pytest', 'c': True}, {'t': 'python test', 'c': False}, {'t': 'run tests', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'assert 2 + 2 == 4 natijasi?', 'a': [{'t': 'Test o\'tadi', 'c': True}, {'t': 'Test muvaffaqiyatsiz', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Logging - Loglar bilan ishlash', 't': 25, 'o': 61, 'q': [
        {'t': 'Logging nima uchun?', 'a': [{'t': 'Dastur ishlashi haqida ma\'lumot yozish', 'c': True}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Oddiy log yozish?', 'a': [{'t': 'logging.info("Xabar")', 'c': True}, {'t': 'print("Xabar")', 'c': False}, {'t': 'write("Xabar")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Log darajalari qaysilar?', 'a': [{'t': 'DEBUG, INFO, WARNING, ERROR, CRITICAL', 'c': True}, {'t': 'Faqat ERROR', 'c': False}, {'t': 'Faqat INFO', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'logging.error() qachon ishlatiladi?', 'a': [{'t': 'Xatolar haqida ma\'lumot berish', 'c': True}, {'t': 'Oddiy ma\'lumot berish', 'c': False}, {'t': 'Debug qilish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Logni faylga yozish?', 'a': [{'t': 'logging.basicConfig(filename="app.log")', 'c': True}, {'t': 'logging.write("app.log")', 'c': False}, {'t': 'logging.save("app.log")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Argparse - Buyruq qatori argumentlari', 't': 25, 'o': 62, 'q': [
        {'t': 'argparse nima uchun?', 'a': [{'t': 'Buyruq qatori argumentlarini boshqarish', 'c': True}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'ArgumentParser yaratish?', 'a': [{'t': 'parser = argparse.ArgumentParser()', 'c': True}, {'t': 'parser = argparse.create()', 'c': False}, {'t': 'parser = new ArgumentParser()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Argument qo\'shish?', 'a': [{'t': 'parser.add_argument("--name")', 'c': True}, {'t': 'parser.add("--name")', 'c': False}, {'t': 'parser.argument("--name")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Argumentlarni olish?', 'a': [{'t': 'args = parser.parse_args()', 'c': True}, {'t': 'args = parser.get_args()', 'c': False}, {'t': 'args = parser.read()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Majburiy argument yaratish?', 'a': [{'t': 'parser.add_argument("name", required=True)', 'c': True}, {'t': 'parser.add_argument("--name")', 'c': False}, {'t': 'parser.required("name")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Pickle - Obyektlarni saqlash', 't': 25, 'o': 63, 'q': [
        {'t': 'pickle nima uchun?', 'a': [{'t': 'Python obyektlarini faylga saqlash', 'c': True}, {'t': 'Faqat matn saqlash', 'c': False}, {'t': 'Faqat sonlar saqlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Obyektni saqlash?', 'a': [{'t': 'pickle.dump(obj, file)', 'c': True}, {'t': 'pickle.save(obj, file)', 'c': False}, {'t': 'pickle.write(obj, file)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Obyektni yuklash?', 'a': [{'t': 'obj = pickle.load(file)', 'c': True}, {'t': 'obj = pickle.read(file)', 'c': False}, {'t': 'obj = pickle.get(file)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Pickle faylini qanday ochish kerak?', 'a': [{'t': 'Binary rejimda ("rb" yoki "wb")', 'c': True}, {'t': 'Matn rejimda ("r" yoki "w")', 'c': False}, {'t': 'Istalgan rejimda', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'pickle.dumps() nima qiladi?', 'a': [{'t': 'Obyektni bytes ga aylantiradi', 'c': True}, {'t': 'Obyektni faylga yozadi', 'c': False}, {'t': 'Obyektni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'CSV bilan ishlash', 't': 25, 'o': 64, 'q': [
        {'t': 'CSV nima?', 'a': [{'t': 'Comma-Separated Values (vergul bilan ajratilgan)', 'c': True}, {'t': 'Python moduli', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'CSV faylni o\'qish?', 'a': [{'t': 'csv.reader(file)', 'c': True}, {'t': 'csv.read(file)', 'c': False}, {'t': 'csv.load(file)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'CSV faylga yozish?', 'a': [{'t': 'csv.writer(file)', 'c': True}, {'t': 'csv.write(file)', 'c': False}, {'t': 'csv.save(file)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'writer.writerow() nima qiladi?', 'a': [{'t': 'Bir qator yozadi', 'c': True}, {'t': 'Bir ustun yozadi', 'c': False}, {'t': 'Butun faylni yozadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'DictReader nima uchun?', 'a': [{'t': 'CSV ni lug\'at sifatida o\'qish', 'c': True}, {'t': 'CSV ni ro\'yxat sifatida o\'qish', 'c': False}, {'t': 'CSV ni yozish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'XML bilan ishlash', 't': 25, 'o': 65, 'q': [
        {'t': 'XML nima?', 'a': [{'t': 'Extensible Markup Language', 'c': True}, {'t': 'Python moduli', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'XML uchun qaysi modul?', 'a': [{'t': 'xml.etree.ElementTree', 'c': True}, {'t': 'xmlparser', 'c': False}, {'t': 'xml.reader', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'XML faylni o\'qish?', 'a': [{'t': 'ET.parse("file.xml")', 'c': True}, {'t': 'ET.read("file.xml")', 'c': False}, {'t': 'ET.load("file.xml")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'XML elementini topish?', 'a': [{'t': 'root.find("tag")', 'c': True}, {'t': 'root.get("tag")', 'c': False}, {'t': 'root.search("tag")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Barcha elementlarni topish?', 'a': [{'t': 'root.findall("tag")', 'c': True}, {'t': 'root.getall("tag")', 'c': False}, {'t': 'root.searchall("tag")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Email yuborish', 't': 25, 'o': 66, 'q': [
        {'t': 'Email yuborish uchun qaysi modul?', 'a': [{'t': 'smtplib', 'c': True}, {'t': 'email', 'c': False}, {'t': 'mail', 'c': False}, {'t': 'send', 'c': False}]},
        {'t': 'SMTP serverga ulanish?', 'a': [{'t': 'smtplib.SMTP("smtp.gmail.com", 587)', 'c': True}, {'t': 'smtplib.connect("smtp.gmail.com")', 'c': False}, {'t': 'smtplib.open("smtp.gmail.com")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Email yuborish?', 'a': [{'t': 'server.sendmail(from, to, msg)', 'c': True}, {'t': 'server.send(from, to, msg)', 'c': False}, {'t': 'server.mail(from, to, msg)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'TLS shifrlashni yoqish?', 'a': [{'t': 'server.starttls()', 'c': True}, {'t': 'server.tls()', 'c': False}, {'t': 'server.secure()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Serverga login qilish?', 'a': [{'t': 'server.login(email, password)', 'c': True}, {'t': 'server.auth(email, password)', 'c': False}, {'t': 'server.signin(email, password)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Tkinter - GUI dasturlash', 't': 30, 'o': 67, 'q': [
        {'t': 'Tkinter nima?', 'a': [{'t': 'Python GUI kutubxonasi', 'c': True}, {'t': 'Web framework', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Asosiy oyna yaratish?', 'a': [{'t': 'root = tk.Tk()', 'c': True}, {'t': 'root = tk.Window()', 'c': False}, {'t': 'root = tk.create()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Tugma yaratish?', 'a': [{'t': 'tk.Button(root, text="OK")', 'c': True}, {'t': 'tk.button(root, "OK")', 'c': False}, {'t': 'tk.createButton(root, "OK")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Matn kiritish maydoni?', 'a': [{'t': 'tk.Entry(root)', 'c': True}, {'t': 'tk.Input(root)', 'c': False}, {'t': 'tk.TextField(root)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Oynani ishga tushirish?', 'a': [{'t': 'root.mainloop()', 'c': True}, {'t': 'root.run()', 'c': False}, {'t': 'root.start()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Pygame - O\'yin dasturlash', 't': 30, 'o': 68, 'q': [
        {'t': 'Pygame nima?', 'a': [{'t': 'O\'yin yaratish kutubxonasi', 'c': True}, {'t': 'Web framework', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Pygame ni ishga tushirish?', 'a': [{'t': 'pygame.init()', 'c': True}, {'t': 'pygame.start()', 'c': False}, {'t': 'pygame.run()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Oyna yaratish?', 'a': [{'t': 'pygame.display.set_mode((800, 600))', 'c': True}, {'t': 'pygame.window(800, 600)', 'c': False}, {'t': 'pygame.create(800, 600)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Rangni belgilash (RGB)?', 'a': [{'t': '(255, 0, 0) - qizil', 'c': True}, {'t': '"red"', 'c': False}, {'t': '#FF0000', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'To\'rtburchak chizish?', 'a': [{'t': 'pygame.draw.rect(screen, color, rect)', 'c': True}, {'t': 'pygame.rectangle(screen, color, rect)', 'c': False}, {'t': 'pygame.draw.square(screen, color, rect)', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Selenium - Brauzer avtomatlashtirish', 't': 30, 'o': 69, 'q': [
        {'t': 'Selenium nima uchun?', 'a': [{'t': 'Brauzer avtomatlashtirish va testing', 'c': True}, {'t': 'Web scraping', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'WebDriver yaratish?', 'a': [{'t': 'driver = webdriver.Chrome()', 'c': True}, {'t': 'driver = selenium.Chrome()', 'c': False}, {'t': 'driver = browser.Chrome()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Sahifani ochish?', 'a': [{'t': 'driver.get("https://example.com")', 'c': True}, {'t': 'driver.open("https://example.com")', 'c': False}, {'t': 'driver.load("https://example.com")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Elementni topish (ID bo\'yicha)?', 'a': [{'t': 'driver.find_element(By.ID, "myid")', 'c': True}, {'t': 'driver.get_element("myid")', 'c': False}, {'t': 'driver.find("myid")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Brauzerni yopish?', 'a': [{'t': 'driver.quit()', 'c': True}, {'t': 'driver.close()', 'c': False}, {'t': 'driver.exit()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Type Hints - Tur belgilash', 't': 25, 'o': 70, 'q': [
        {'t': 'Type hints nima?', 'a': [{'t': 'O\'zgaruvchi va funksiya turlarini belgilash', 'c': True}, {'t': 'Xatolarni aniqlash', 'c': False}, {'t': 'Kodni tezlashtirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'O\'zgaruvchi turini belgilash?', 'a': [{'t': 'name: str = "Ali"', 'c': True}, {'t': 'name = str("Ali")', 'c': False}, {'t': 'str name = "Ali"', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiya parametri turini belgilash?', 'a': [{'t': 'def func(x: int):', 'c': True}, {'t': 'def func(int x):', 'c': False}, {'t': 'def func(x) -> int:', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiya qaytarish turini belgilash?', 'a': [{'t': 'def func() -> int:', 'c': True}, {'t': 'def func(): int', 'c': False}, {'t': 'def int func():', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Type hints majburiyatmi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan majburiy', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Context Managers - with operatori', 't': 25, 'o': 71, 'q': [
        {'t': 'Context manager nima?', 'a': [{'t': 'Resurslarni avtomatik boshqarish', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'with operatori nima uchun?', 'a': [{'t': 'Resurslarni avtomatik yopish', 'c': True}, {'t': 'Sikl yaratish', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'with open("file.txt") as f: ning afzalligi?', 'a': [{'t': 'Fayl avtomatik yopiladi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
        {'t': '__enter__ metodi qachon chaqiriladi?', 'a': [{'t': 'with bloki boshlanishida', 'c': True}, {'t': 'with bloki tugashida', 'c': False}, {'t': 'Xato yuz berganda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': '__exit__ metodi qachon chaqiriladi?', 'a': [{'t': 'with bloki tugashida', 'c': True}, {'t': 'with bloki boshlanishida', 'c': False}, {'t': 'Faqat xato bo\'lsa', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'Metaclasses', 't': 30, 'o': 72, 'q': [
        {'t': 'Metaclass nima?', 'a': [{'t': 'Klass yaratuvchi klass', 'c': True}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'type() funksiyasi nima qiladi?', 'a': [{'t': 'Obyekt turini qaytaradi yoki klass yaratadi', 'c': True}, {'t': 'Faqat tur qaytaradi', 'c': False}, {'t': 'Faqat klass yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Metaclass qanday belgilanadi?', 'a': [{'t': 'class MyClass(metaclass=MyMeta):', 'c': True}, {'t': 'class MyClass(MyMeta):', 'c': False}, {'t': 'class MyClass: metaclass=MyMeta', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Metaclass qachon ishlatiladi?', 'a': [{'t': 'Klass yaratilish jarayonini boshqarish kerak bo\'lsa', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat murakkab dasturlarda', 'c': False}]},
        {'t': '__new__ va __init__ farqi?', 'a': [{'t': '__new__ obyekt yaratadi, __init__ sozlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '__init__ obyekt yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Descriptors', 't': 30, 'o': 73, 'q': [
        {'t': 'Descriptor nima?', 'a': [{'t': 'Atribut kirishni boshqaruvchi obyekt', 'c': True}, {'t': 'Oddiy atribut', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}]},
        {'t': '__get__ metodi nima qiladi?', 'a': [{'t': 'Atribut qiymatini qaytaradi', 'c': True}, {'t': 'Atribut qiymatini o\'rnatadi', 'c': False}, {'t': 'Atributni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '__set__ metodi nima qiladi?', 'a': [{'t': 'Atribut qiymatini o\'rnatadi', 'c': True}, {'t': 'Atribut qiymatini qaytaradi', 'c': False}, {'t': 'Atributni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '__delete__ metodi nima qiladi?', 'a': [{'t': 'Atributni o\'chiradi', 'c': True}, {'t': 'Atribut qiymatini qaytaradi', 'c': False}, {'t': 'Atribut qiymatini o\'rnatadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '@property descriptor hisoblanadimi?', 'a': [{'t': 'Ha, descriptor', 'c': True}, {'t': 'Yo\'q, oddiy dekorator', 'c': False}, {'t': 'Noma\'lum', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Memory Management', 't': 30, 'o': 74, 'q': [
        {'t': 'Python da xotira qanday boshqariladi?', 'a': [{'t': 'Avtomatik (garbage collection)', 'c': True}, {'t': 'Qo\'lda', 'c': False}, {'t': 'Aralash', 'c': False}, {'t': 'Boshqarilmaydi', 'c': False}]},
        {'t': 'Garbage collector nima?', 'a': [{'t': 'Ishlatilmayotgan xotirani tozalash mexanizmi', 'c': True}, {'t': 'Xotira ajratish mexanizmi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Klass', 'c': False}]},
        {'t': 'Reference counting nima?', 'a': [{'t': 'Obyektga havolalar sonini hisoblash', 'c': True}, {'t': 'Obyektlar sonini hisoblash', 'c': False}, {'t': 'Xotira hajmini hisoblash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'gc moduli nima uchun?', 'a': [{'t': 'Garbage collector ni boshqarish', 'c': True}, {'t': 'Xotira ajratish', 'c': False}, {'t': 'Fayllar bilan ishlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'del operatori nima qiladi?', 'a': [{'t': 'Havolani o\'chiradi', 'c': True}, {'t': 'Obyektni darhol o\'chiradi', 'c': False}, {'t': 'Xotirani tozalaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Performance Optimization', 't': 30, 'o': 75, 'q': [
        {'t': 'Python kodni tezlashtirish usullari?', 'a': [{'t': 'List comprehension, generator, caching', 'c': True}, {'t': 'Faqat ko\'proq xotira', 'c': False}, {'t': 'Faqat tezroq kompyuter', 'c': False}, {'t': 'Hech qanday usul yo\'q', 'c': False}]},
        {'t': 'timeit moduli nima uchun?', 'a': [{'t': 'Kod bajarilish vaqtini o\'lchash', 'c': True}, {'t': 'Vaqt bilan ishlash', 'c': False}, {'t': 'Timer yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Generator list dan qanday yaxshiroq?', 'a': [{'t': 'Kam xotira ishlatadi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Oson yoziladi', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
        {'t': '@lru_cache nima uchun?', 'a': [{'t': 'Funksiya natijalarini keshlash', 'c': True}, {'t': 'Funksiyani tezlashtirish', 'c': False}, {'t': 'Xotirani tozalash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Cython nima?', 'a': [{'t': 'Python kodni C ga kompilyatsiya qilish', 'c': True}, {'t': 'Python versiyasi', 'c': False}, {'t': 'Python moduli', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Design Patterns - Singleton', 't': 25, 'o': 76, 'q': [
        {'t': 'Singleton pattern nima?', 'a': [{'t': 'Faqat bitta obyekt yaratish', 'c': True}, {'t': 'Ko\'p obyekt yaratish', 'c': False}, {'t': 'Obyekt yaratmaslik', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Singleton qachon ishlatiladi?', 'a': [{'t': 'Global holat kerak bo\'lganda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
        {'t': 'Singleton ning kamchiligi?', 'a': [{'t': 'Global holat, testing qiyin', 'c': True}, {'t': 'Sekin ishlaydi', 'c': False}, {'t': 'Ko\'p xotira', 'c': False}, {'t': 'Hech qanday kamchilik yo\'q', 'c': False}]},
        {'t': 'Singleton Python da qanday amalga oshiriladi?', 'a': [{'t': '__new__ metodi orqali', 'c': True}, {'t': '__init__ metodi orqali', 'c': False}, {'t': 'Avtomatik', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Singleton misoli?', 'a': [{'t': 'Database connection, Logger', 'c': True}, {'t': 'User obyekti', 'c': False}, {'t': 'List', 'c': False}, {'t': 'String', 'c': False}]},
    ]},
    {'n': 'Design Patterns - Factory', 't': 25, 'o': 77, 'q': [
        {'t': 'Factory pattern nima?', 'a': [{'t': 'Obyekt yaratishni markazlashtirish', 'c': True}, {'t': 'Obyekt o\'chirish', 'c': False}, {'t': 'Obyekt o\'zgartirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Factory pattern qachon ishlatiladi?', 'a': [{'t': 'Obyekt yaratish murakkab bo\'lganda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat kichik dasturlarda', 'c': False}]},
        {'t': 'Factory pattern ning afzalligi?', 'a': [{'t': 'Kodni qayta ishlatish, moslashuvchanlik', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Factory method nima?', 'a': [{'t': 'Obyekt yaratuvchi metod', 'c': True}, {'t': 'Obyekt o\'chiruvchi metod', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Abstract Factory nima?', 'a': [{'t': 'Bog\'liq obyektlar oilasini yaratish', 'c': True}, {'t': 'Bitta obyekt yaratish', 'c': False}, {'t': 'Obyekt o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Design Patterns - Observer', 't': 25, 'o': 78, 'q': [
        {'t': 'Observer pattern nima?', 'a': [{'t': 'Obyekt o\'zgarishini kuzatish', 'c': True}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Obyekt o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Observer pattern qachon ishlatiladi?', 'a': [{'t': 'Bir obyekt o\'zgarganda boshqalarga xabar berish', 'c': True}, {'t': 'Obyekt yaratishda', 'c': False}, {'t': 'Obyekt o\'chirishda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Subject nima?', 'a': [{'t': 'Kuzatilayotgan obyekt', 'c': True}, {'t': 'Kuzatuvchi obyekt', 'c': False}, {'t': 'Oddiy obyekt', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Observer nima?', 'a': [{'t': 'Kuzatuvchi obyekt', 'c': True}, {'t': 'Kuzatilayotgan obyekt', 'c': False}, {'t': 'Oddiy obyekt', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Observer pattern misoli?', 'a': [{'t': 'Event handling, MVC pattern', 'c': True}, {'t': 'Database connection', 'c': False}, {'t': 'File reading', 'c': False}, {'t': 'String manipulation', 'c': False}]},
    ]},
    {'n': 'Design Patterns - Decorator', 't': 25, 'o': 79, 'q': [
        {'t': 'Decorator pattern nima?', 'a': [{'t': 'Obyektga dinamik funksionallik qo\'shish', 'c': True}, {'t': 'Obyekt yaratish', 'c': False}, {'t': 'Obyekt o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Decorator pattern qachon ishlatiladi?', 'a': [{'t': 'Klassni o\'zgartirmasdan funksionallik qo\'shish', 'c': True}, {'t': 'Yangi klass yaratish', 'c': False}, {'t': 'Klass o\'chirish', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Python @decorator va Decorator pattern bir xilmi?', 'a': [{'t': 'Yo\'q, turli narsalar', 'c': True}, {'t': 'Ha, bir xil', 'c': False}, {'t': 'Qisman bir xil', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Decorator pattern ning afzalligi?', 'a': [{'t': 'Moslashuvchanlik, kodni o\'zgartirmaslik', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Decorator pattern misoli?', 'a': [{'t': 'Logging, caching, validation', 'c': True}, {'t': 'Database connection', 'c': False}, {'t': 'File reading', 'c': False}, {'t': 'String manipulation', 'c': False}]},
    ]},
    {'n': 'Best Practices va Code Style', 't': 30, 'o': 80, 'q': [
        {'t': 'PEP 8 nima?', 'a': [{'t': 'Python kod yozish qoidalari', 'c': True}, {'t': 'Python versiyasi', 'c': False}, {'t': 'Python moduli', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Python da indent necha bo\'sh joy?', 'a': [{'t': '4 ta bo\'sh joy', 'c': True}, {'t': '2 ta bo\'sh joy', 'c': False}, {'t': '8 ta bo\'sh joy', 'c': False}, {'t': 'Istalgancha', 'c': False}]},
        {'t': 'O\'zgaruvchi nomi qanday yoziladi?', 'a': [{'t': 'snake_case (kichik harf, pastki chiziq)', 'c': True}, {'t': 'camelCase', 'c': False}, {'t': 'PascalCase', 'c': False}, {'t': 'UPPERCASE', 'c': False}]},
        {'t': 'Klass nomi qanday yoziladi?', 'a': [{'t': 'PascalCase (har bir so\'z bosh harf)', 'c': True}, {'t': 'snake_case', 'c': False}, {'t': 'camelCase', 'c': False}, {'t': 'lowercase', 'c': False}]},
        {'t': 'Konstanta qanday yoziladi?', 'a': [{'t': 'UPPER_CASE (katta harf, pastki chiziq)', 'c': True}, {'t': 'snake_case', 'c': False}, {'t': 'PascalCase', 'c': False}, {'t': 'camelCase', 'c': False}]},
        {'t': 'Docstring nima?', 'a': [{'t': 'Funksiya/klass hujjatlari', 'c': True}, {'t': 'Oddiy izoh', 'c': False}, {'t': 'Kod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🐍 PYTHON DASTURLASH - 100 TA MAVZU")
    print("=" * 80)
    subject = get_or_create_python()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T)
    total = sum(len(t['q']) for t in T)
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! {len(T)} ta mavzu, {total} ta test qo'shildi!")
    print("=" * 80)
