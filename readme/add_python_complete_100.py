"""
PYTHON DASTURLASH - 100 TA MAVZU (to'g'ri javoblar tasodifiy joylashgan)
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
                # Javoblarni aralashtiramiz
                answers = qd['a'].copy()
                random.shuffle(answers)
                for ad in answers:
                    Answer.objects.create(question=q, text=ad['t'], is_correct=ad['c'])

# 100 TA MAVZU
T = [
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
    ]},
    {'n': 'Ma\'lumot turlari - Sonlar', 't': 20, 'o': 4, 'q': [
        {'t': 'Python da qanday son turlari bor?', 'a': [{'t': 'int, float, complex', 'c': True}, {'t': 'Faqat int', 'c': False}, {'t': 'Faqat float', 'c': False}, {'t': 'number', 'c': False}]},
        {'t': 'int nima?', 'a': [{'t': 'Butun son', 'c': True}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'float nima?', 'a': [{'t': 'O\'nli kasr son', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'type(10) natijasi nima?', 'a': [{'t': '<class \'int\'>', 'c': True}, {'t': '<class \'float\'>', 'c': False}, {'t': '<class \'str\'>', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '5 / 2 natijasi nima?', 'a': [{'t': '2.5', 'c': True}, {'t': '2', 'c': False}, {'t': '3', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari - Matnlar', 't': 25, 'o': 5, 'q': [
        {'t': 'Matn (string) qanday yaratiladi?', 'a': [{'t': 'Qo\'shtirnoq yoki birtirnoq ichida', 'c': True}, {'t': 'Faqat qo\'shtirnoqda', 'c': False}, {'t': 'Faqat birtirnoqda', 'c': False}, {'t': 'Qavslar ichida', 'c': False}]},
        {'t': '"Salom" + " " + "Dunyo" natijasi?', 'a': [{'t': 'Salom Dunyo', 'c': True}, {'t': 'SalomDunyo', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Salom + Dunyo', 'c': False}]},
        {'t': '"Python" * 3 natijasi?', 'a': [{'t': 'PythonPythonPython', 'c': True}, {'t': 'Python3', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Python Python Python', 'c': False}]},
        {'t': 'len("Salom") natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '4', 'c': False}, {'t': '6', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '"Python"[0] natijasi?', 'a': [{'t': 'P', 'c': True}, {'t': 'y', 'c': False}, {'t': 'Python', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🐍 PYTHON - 100 TA MAVZU (to'g'ri javoblar aralash)")
    print("=" * 80)
    subject = get_or_create_python()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T[:5])
    total = sum(len(t['q']) for t in T[:5])
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! 5 ta mavzu, {total} ta test qo'shildi!")
    print(f"📝 To'g'ri javoblar tasodifiy joylashtirildi")
    print("=" * 80)
