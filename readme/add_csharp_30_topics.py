"""
C# DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_csharp():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='C#', defaults={'category': cat, 'description': 'C# dasturlash tili - zamonaviy dasturlash', 'icon': 'bi-code-square', 'order': 3, 'is_active': True})
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
    {'n': 'C# dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'C# dasturlash tili qachon yaratilgan?', 'a': [{'t': '2000 yilda', 'c': True}, {'t': '1995 yilda', 'c': False}, {'t': '2010 yilda', 'c': False}, {'t': '1990 yilda', 'c': False}]},
        {'t': 'C# tilini kim yaratgan?', 'a': [{'t': 'Microsoft kompaniyasi', 'c': True}, {'t': 'Google', 'c': False}, {'t': 'Apple', 'c': False}, {'t': 'Oracle', 'c': False}]},
        {'t': 'C# qanday platformada ishlaydi?', 'a': [{'t': '.NET platformasida', 'c': True}, {'t': 'Java platformasida', 'c': False}, {'t': 'Python platformasida', 'c': False}, {'t': 'Faqat Windows da', 'c': False}]},
        {'t': 'C# faylining kengaytmasi qanday?', 'a': [{'t': '.cs', 'c': True}, {'t': '.c', 'c': False}, {'t': '.cpp', 'c': False}, {'t': '.csharp', 'c': False}]},
        {'t': 'C# qanday til?', 'a': [{'t': 'Ob\'ektga yo\'naltirilgan til', 'c': True}, {'t': 'Faqat protsedurali til', 'c': False}, {'t': 'Skript tili', 'c': False}, {'t': 'Markup tili', 'c': False}]},
        {'t': 'C# da dastur qayerdan boshlanadi?', 'a': [{'t': 'Main() metodidan', 'c': True}, {'t': 'Start() metodidan', 'c': False}, {'t': 'Begin() metodidan', 'c': False}, {'t': 'Run() metodidan', 'c': False}]},
    ]},
    {'n': 'Birinchi C# dasturi', 't': 20, 'o': 2, 'q': [
        {'t': 'Console.WriteLine() nima qiladi?', 'a': [{'t': 'Ekranga chiqaradi', 'c': True}, {'t': 'Kiritish qiladi', 'c': False}, {'t': 'Hisoblash qiladi', 'c': False}, {'t': 'Saqlaydi', 'c': False}]},
        {'t': 'using System; nima?', 'a': [{'t': 'Namespace ulash', 'c': True}, {'t': 'Izoh', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'C# da ; belgisi nima?', 'a': [{'t': 'Operator tugashi belgisi', 'c': True}, {'t': 'Izoh belgisi', 'c': False}, {'t': 'Qo\'shtirnoq', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Console.ReadLine() nima qiladi?', 'a': [{'t': 'Foydalanuvchidan kiritish oladi', 'c': True}, {'t': 'Ekranga chiqaradi', 'c': False}, {'t': 'Hisoblash qiladi', 'c': False}, {'t': 'Fayldan o\'qiydi', 'c': False}]},
        {'t': 'C# da izoh qanday yoziladi?', 'a': [{'t': '// yoki /* */', 'c': True}, {'t': '# belgisi bilan', 'c': False}, {'t': '<!-- --> bilan', 'c': False}, {'t': '\'\'\' bilan', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar va ma\'lumot turlari', 't': 25, 'o': 3, 'q': [
        {'t': 'int nima?', 'a': [{'t': 'Butun son turi', 'c': True}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'string nima?', 'a': [{'t': 'Matn turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Belgi', 'c': False}]},
        {'t': 'bool nima?', 'a': [{'t': 'Mantiqiy qiymat (true/false)', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'O\'nli kasr', 'c': False}]},
        {'t': 'double nima?', 'a': [{'t': 'O\'nli kasr son turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'char nima?', 'a': [{'t': 'Bitta belgi turi', 'c': True}, {'t': 'Matn', 'c': False}, {'t': 'Butun son', 'c': False}, {'t': 'O\'nli kasr', 'c': False}]},
        {'t': 'int x = 10; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'var nima?', 'a': [{'t': 'Avtomatik tur aniqlash', 'c': True}, {'t': 'O\'zgaruvchi nomi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Konstantalar', 't': 20, 'o': 4, 'q': [
        {'t': 'const nima uchun ishlatiladi?', 'a': [{'t': 'O\'zgarmas qiymat yaratish', 'c': True}, {'t': 'O\'zgaruvchi yaratish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Massiv yaratish', 'c': False}]},
        {'t': 'const int x = 5; x ni o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, o\'zgarmas', 'c': True}, {'t': 'Ha, o\'zgartirish mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'readonly va const farqi?', 'a': [{'t': 'readonly runtime da, const compile time da', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'readonly tezroq', 'c': False}, {'t': 'const o\'zgaradi', 'c': False}]},
        {'t': 'const qiymat qayerda beriladi?', 'a': [{'t': 'E\'lon qilinganda', 'c': True}, {'t': 'Istalgan vaqtda', 'c': False}, {'t': 'Faqat metodda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Konstanta nomi qanday yoziladi?', 'a': [{'t': 'Katta harflar bilan (CONSTANT_NAME)', 'c': True}, {'t': 'Kichik harflar bilan', 'c': False}, {'t': 'Aralash', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
    ]},
    {'n': 'Operatorlar', 't': 25, 'o': 5, 'q': [
        {'t': '+ operatori nima qiladi?', 'a': [{'t': 'Qo\'shish', 'c': True}, {'t': 'Ayirish', 'c': False}, {'t': 'Ko\'paytirish', 'c': False}, {'t': 'Bo\'lish', 'c': False}]},
        {'t': '== operatori nima?', 'a': [{'t': 'Tenglik tekshirish', 'c': True}, {'t': 'Qiymat berish', 'c': False}, {'t': 'Qo\'shish', 'c': False}, {'t': 'Taqqoslash', 'c': False}]},
        {'t': '!= operatori nima?', 'a': [{'t': 'Teng emasligini tekshirish', 'c': True}, {'t': 'Tenglik tekshirish', 'c': False}, {'t': 'Qiymat berish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '&& operatori nima?', 'a': [{'t': 'Mantiqiy VA (AND)', 'c': True}, {'t': 'Mantiqiy YOKI (OR)', 'c': False}, {'t': 'Mantiqiy EMAS (NOT)', 'c': False}, {'t': 'Qo\'shish', 'c': False}]},
        {'t': '|| operatori nima?', 'a': [{'t': 'Mantiqiy YOKI (OR)', 'c': True}, {'t': 'Mantiqiy VA (AND)', 'c': False}, {'t': 'Mantiqiy EMAS (NOT)', 'c': False}, {'t': 'Ayirish', 'c': False}]},
        {'t': '! operatori nima?', 'a': [{'t': 'Mantiqiy EMAS (NOT)', 'c': True}, {'t': 'Mantiqiy VA (AND)', 'c': False}, {'t': 'Mantiqiy YOKI (OR)', 'c': False}, {'t': 'Faktorial', 'c': False}]},
        {'t': '++ operatori nima qiladi?', 'a': [{'t': '1 ga oshiradi', 'c': True}, {'t': '1 ga kamaytiradi', 'c': False}, {'t': '2 ga ko\'paytiradi', 'c': False}, {'t': 'Qo\'shadi', 'c': False}]},
    ]},
    {'n': 'if operatori', 't': 25, 'o': 6, 'q': [
        {'t': 'if operatori nima uchun?', 'a': [{'t': 'Shartli bajarish', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'if (x > 5) Console.WriteLine("Katta"); qachon ishlaydi?', 'a': [{'t': 'x 5 dan katta bo\'lsa', 'c': True}, {'t': 'x 5 ga teng bo\'lsa', 'c': False}, {'t': 'x 5 dan kichik bo\'lsa', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'if blokida kod qanday yoziladi?', 'a': [{'t': 'Jingalak qavslar ichida {}', 'c': True}, {'t': 'Oddiy qavslar ichida ()', 'c': False}, {'t': 'Kvadrat qavslar ichida []', 'c': False}, {'t': 'Qo\'shtirnoqda ""', 'c': False}]},
        {'t': 'if (x == 5) nima tekshiradi?', 'a': [{'t': 'x 5 ga tengmi', 'c': True}, {'t': 'x ga 5 ni beradi', 'c': False}, {'t': 'x 5 dan kattami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir qatorli if da {} kerakmi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'if-else operatori', 't': 25, 'o': 7, 'q': [
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'else if nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'Bir necha else if ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'if-else if-else ketma-ketligi to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, else birinchi', 'c': False}, {'t': 'Yo\'q, else if oxirida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'else dan keyin shart yozish kerakmi?', 'a': [{'t': 'Yo\'q, shart yozilmaydi', 'c': True}, {'t': 'Ha, shart yoziladi', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'switch-case operatori', 't': 25, 'o': 8, 'q': [
        {'t': 'switch-case nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'case nima?', 'a': [{'t': 'Bir variant', 'c': True}, {'t': 'Shart', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'switch dan chiqadi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'C# da switch da break majburiymi?', 'a': [{'t': 'Ha, majburiy', 'c': True}, {'t': 'Yo\'q, ixtiyoriy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'while sikli', 't': 25, 'o': 9, 'q': [
        {'t': 'while sikli nima uchun?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'while (true) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Sikldan chiqish uchun?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'Siklning keyingi iteratsiyasiga o\'tish?', 'a': [{'t': 'continue', 'c': True}, {'t': 'skip', 'c': False}, {'t': 'next', 'c': False}, {'t': 'pass', 'c': False}]},
        {'t': 'int i=0; while(i<3) {Console.Write(i); i++;} necha marta?', 'a': [{'t': '3 marta', 'c': True}, {'t': '2 marta', 'c': False}, {'t': '4 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
    ]},
    {'n': 'do-while sikli', 't': 20, 'o': 10, 'q': [
        {'t': 'do-while va while farqi?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'while kamida 1 marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'do-while da shart qayerda tekshiriladi?', 'a': [{'t': 'Oxirida', 'c': True}, {'t': 'Boshida', 'c': False}, {'t': 'O\'rtada', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'do {...} while(shart); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while oxirida ; kerakmi?', 'a': [{'t': 'Ha, kerak', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while qachon ishlatiladi?', 'a': [{'t': 'Kamida 1 marta bajarish kerak bo\'lsa', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
    ]},
    {'n': 'for sikli', 't': 25, 'o': 11, 'q': [
        {'t': 'for sikli nima uchun?', 'a': [{'t': 'Ma\'lum marta takrorlash', 'c': True}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'for (int i=0; i<5; i++) necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for siklining 3 qismi?', 'a': [{'t': 'Boshlang\'ich, shart, o\'zgartirish', 'c': True}, {'t': 'Faqat shart', 'c': False}, {'t': 'Faqat boshlang\'ich', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for (;;) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'foreach sikli', 't': 25, 'o': 12, 'q': [
        {'t': 'foreach nima uchun?', 'a': [{'t': 'Kolleksiyalarni aylanish', 'c': True}, {'t': 'Oddiy takrorlash', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Metod yaratish', 'c': False}]},
        {'t': 'foreach (int x in arr) nima qiladi?', 'a': [{'t': 'arr massivini aylanadi', 'c': True}, {'t': 'arr ni yaratadi', 'c': False}, {'t': 'arr ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'foreach da elementni o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat o\'qish', 'c': True}, {'t': 'Ha, o\'zgartirish mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'foreach va for farqi?', 'a': [{'t': 'foreach faqat o\'qish, for o\'zgartirish mumkin', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'for faqat o\'qish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'foreach qaysi turlar bilan ishlaydi?', 'a': [{'t': 'IEnumerable turlar bilan', 'c': True}, {'t': 'Faqat massivlar bilan', 'c': False}, {'t': 'Faqat int bilan', 'c': False}, {'t': 'Hech qanday tur bilan', 'c': False}]},
    ]},
    {'n': 'Massivlar', 't': 25, 'o': 13, 'q': [
        {'t': 'Massiv nima?', 'a': [{'t': 'Bir xil turdagi elementlar to\'plami', 'c': True}, {'t': 'Bitta qiymat', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'int[] arr = new int[5]; nima yaratadi?', 'a': [{'t': '5 ta butun son uchun massiv', 'c': True}, {'t': '5 qiymatli massiv', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Bitta o\'zgaruvchi', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': 'arr[0] nima?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Ikkinchi element', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int[] arr = {1,2,3,4,5}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'arr.Length nima qaytaradi?', 'a': [{'t': 'Massiv uzunligini', 'c': True}, {'t': 'Massiv qiymatini', 'c': False}, {'t': 'Massiv indeksini', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Ko\'p o\'lchovli massivlar', 't': 25, 'o': 14, 'q': [
        {'t': '2 o\'lchovli massiv nima?', 'a': [{'t': 'Jadval ko\'rinishidagi massiv', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int[,] arr = new int[3,4]; nima yaratadi?', 'a': [{'t': '3 qator, 4 ustunli massiv', 'c': True}, {'t': '4 qator, 3 ustunli massiv', 'c': False}, {'t': '7 elementli massiv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr[0,0] nima?', 'a': [{'t': 'Birinchi qator, birinchi ustun', 'c': True}, {'t': 'Ikkinchi qator, ikkinchi ustun', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'int[,] arr = {{1,2},{3,4}}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Jagged array nima?', 'a': [{'t': 'Massivlar massivi', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': '2D massiv', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Metodlar - Asoslar', 't': 25, 'o': 15, 'q': [
        {'t': 'Metod nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Metod qanday e\'lon qilinadi?', 'a': [{'t': 'tur_nomi MetodNomi(parametrlar)', 'c': True}, {'t': 'function MetodNomi()', 'c': False}, {'t': 'def MetodNomi()', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'void nima?', 'a': [{'t': 'Hech narsa qaytarmaydi', 'c': True}, {'t': 'Butun son qaytaradi', 'c': False}, {'t': 'Matn qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'return nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi va metoddan chiqadi', 'c': True}, {'t': 'Faqat qiymat qaytaradi', 'c': False}, {'t': 'Faqat metoddan chiqadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Metodning nomi qanday yoziladi?', 'a': [{'t': 'PascalCase (MetodNomi)', 'c': True}, {'t': 'camelCase (metodNomi)', 'c': False}, {'t': 'snake_case (metod_nomi)', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
    ]},
    {'n': 'Metod parametrlari', 't': 25, 'o': 16, 'q': [
        {'t': 'Parametr nima?', 'a': [{'t': 'Metodga beriladigan qiymat', 'c': True}, {'t': 'Metod nomi', 'c': False}, {'t': 'Metod natijasi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'int Sum(int a, int b) - a va b nima?', 'a': [{'t': 'Parametrlar', 'c': True}, {'t': 'Argumentlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Sum(5, 3) - 5 va 3 nima?', 'a': [{'t': 'Argumentlar', 'c': True}, {'t': 'Parametrlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'ref kalit so\'zi nima qiladi?', 'a': [{'t': 'Parametrni referens orqali uzatadi', 'c': True}, {'t': 'Parametrni qiymat orqali uzatadi', 'c': False}, {'t': 'Parametrni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'out kalit so\'zi nima uchun?', 'a': [{'t': 'Metoddan bir necha qiymat qaytarish', 'c': True}, {'t': 'Metodga qiymat berish', 'c': False}, {'t': 'Metodni chaqirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'params kalit so\'zi nima?', 'a': [{'t': 'O\'zgaruvchan sonli parametrlar', 'c': True}, {'t': 'Bitta parametr', 'c': False}, {'t': 'Ikkita parametr', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Metod overloading', 't': 25, 'o': 17, 'q': [
        {'t': 'Method overloading nima?', 'a': [{'t': 'Bir xil nomli, har xil parametrli metodlar', 'c': True}, {'t': 'Har xil nomli metodlar', 'c': False}, {'t': 'Bir xil metodlar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Overloading da nima har xil bo\'lishi kerak?', 'a': [{'t': 'Parametrlar soni yoki turi', 'c': True}, {'t': 'Faqat metod nomi', 'c': False}, {'t': 'Faqat qaytish turi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'int Sum(int a, int b) va double Sum(double a, double b) to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri overloading', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Faqat qaytish turi bilan overloading qilish mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Overloading ning afzalligi?', 'a': [{'t': 'Kodni o\'qish osonroq', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},
    {'n': 'Klasslar - Asoslar', 't': 30, 'o': 18, 'q': [
        {'t': 'Klass nima?', 'a': [{'t': 'Ob\'ekt yaratish uchun shablon', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'class Student {...} nima yaratadi?', 'a': [{'t': 'Student klassini', 'c': True}, {'t': 'Student ob\'ektini', 'c': False}, {'t': 'Student metodini', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ob\'ekt nima?', 'a': [{'t': 'Klassning namunasi', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'Student s = new Student(); nima qiladi?', 'a': [{'t': 'Student ob\'ektini yaratadi', 'c': True}, {'t': 'Student klassini yaratadi', 'c': False}, {'t': 'Student metodini chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'new kalit so\'zi nima uchun?', 'a': [{'t': 'Ob\'ekt yaratish', 'c': True}, {'t': 'Klass yaratish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'O\'zgaruvchi yaratish', 'c': False}]},
        {'t': 'Klass nomi qanday yoziladi?', 'a': [{'t': 'PascalCase (ClassName)', 'c': True}, {'t': 'camelCase (className)', 'c': False}, {'t': 'snake_case (class_name)', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
    ]},
    {'n': 'Konstruktorlar', 't': 25, 'o': 19, 'q': [
        {'t': 'Konstruktor nima?', 'a': [{'t': 'Ob\'ekt yaratilganda chaqiriladigan metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Konstruktor nomi qanday bo\'ladi?', 'a': [{'t': 'Klass nomi bilan bir xil', 'c': True}, {'t': 'Istalgan nom', 'c': False}, {'t': 'constructor', 'c': False}, {'t': '__init__', 'c': False}]},
        {'t': 'Konstruktor qaytish turiga ega bo\'adimi?', 'a': [{'t': 'Yo\'q, qaytish turi yo\'q', 'c': True}, {'t': 'Ha, void', 'c': False}, {'t': 'Ha, int', 'c': False}, {'t': 'Ha, string', 'c': False}]},
        {'t': 'Default konstruktor nima?', 'a': [{'t': 'Parametrsiz konstruktor', 'c': True}, {'t': 'Parametrli konstruktor', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'Bir necha konstruktor bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, overloading orqali', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'Encapsulation', 't': 30, 'o': 20, 'q': [
        {'t': 'Encapsulation nima?', 'a': [{'t': 'Ma\'lumotlarni yashirish', 'c': True}, {'t': 'Ma\'lumotlarni ko\'rsatish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Klass yaratish', 'c': False}]},
        {'t': 'private nima?', 'a': [{'t': 'Faqat klass ichida ko\'rinadi', 'c': True}, {'t': 'Hamma joyda ko\'rinadi', 'c': False}, {'t': 'Faqat paket ichida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'public nima?', 'a': [{'t': 'Hamma joyda ko\'rinadi', 'c': True}, {'t': 'Faqat klass ichida', 'c': False}, {'t': 'Faqat paket ichida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'protected nima?', 'a': [{'t': 'Klass va vorislar uchun', 'c': True}, {'t': 'Faqat klass uchun', 'c': False}, {'t': 'Hamma uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Property nima?', 'a': [{'t': 'Get va set metodlari bilan maydon', 'c': True}, {'t': 'Oddiy o\'zgaruvchi', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Auto-implemented property nima?', 'a': [{'t': 'Avtomatik get/set', 'c': True}, {'t': 'Qo\'lda yozilgan get/set', 'c': False}, {'t': 'Oddiy maydon', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Inheritance (Meros)', 't': 30, 'o': 21, 'q': [
        {'t': 'Inheritance nima?', 'a': [{'t': 'Bir klassdan boshqa klass yaratish', 'c': True}, {'t': 'Klass nusxalash', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'class Dog : Animal nima?', 'a': [{'t': 'Dog Animal dan meros oladi', 'c': True}, {'t': 'Animal Dog dan meros oladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech qanday aloqa yo\'q', 'c': False}]},
        {'t': 'Base class nima?', 'a': [{'t': 'Ota klass', 'c': True}, {'t': 'Bola klass', 'c': False}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Derived class nima?', 'a': [{'t': 'Bola klass', 'c': True}, {'t': 'Ota klass', 'c': False}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'base kalit so\'zi nima uchun?', 'a': [{'t': 'Ota klassga murojaat', 'c': True}, {'t': 'Bola klassga murojaat', 'c': False}, {'t': 'O\'ziga murojaat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'C# da bir necha klassdan meros olish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat bitta klassdan', 'c': True}, {'t': 'Ha, bir necha klassdan', 'c': False}, {'t': 'Faqat ikkita klassdan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Polymorphism', 't': 30, 'o': 22, 'q': [
        {'t': 'Polymorphism nima?', 'a': [{'t': 'Ko\'p shakllilik', 'c': True}, {'t': 'Meros', 'c': False}, {'t': 'Yashirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'virtual kalit so\'zi nima uchun?', 'a': [{'t': 'Metodning override qilinishiga ruxsat', 'c': True}, {'t': 'Metodning yashirilishi', 'c': False}, {'t': 'Metodning o\'chirilishi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'override kalit so\'zi nima?', 'a': [{'t': 'Ota klass metodini qayta yozish', 'c': True}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Metodning nusxasi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'abstract metod nima?', 'a': [{'t': 'Tanasi bo\'lmagan metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Virtual metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'abstract class nima?', 'a': [{'t': 'Ob\'ekt yaratib bo\'lmaydigan klass', 'c': True}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Interface', 't': 30, 'o': 23, 'q': [
        {'t': 'Interface nima?', 'a': [{'t': 'Metodlar shartnomasi', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'interface IAnimal {...} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Interface da metodlar qanday?', 'a': [{'t': 'Faqat imzo, tanasiz', 'c': True}, {'t': 'To\'liq metodlar', 'c': False}, {'t': 'Faqat private', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir klass bir necha interface implement qilishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Interface nomi qanday yoziladi?', 'a': [{'t': 'I harfi bilan boshlanadi (IName)', 'c': True}, {'t': 'Oddiy nom', 'c': False}, {'t': 'Kichik harf bilan', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'Interface va abstract class farqi?', 'a': [{'t': 'Interface faqat imzo, abstract class tanasi bo\'lishi mumkin', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Interface tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Exception Handling', 't': 30, 'o': 24, 'q': [
        {'t': 'Exception nima?', 'a': [{'t': 'Dastur xatosi', 'c': True}, {'t': 'Oddiy xabar', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Klass', 'c': False}]},
        {'t': 'try-catch nima uchun?', 'a': [{'t': 'Xatolarni ushlash', 'c': True}, {'t': 'Xatolarni yaratish', 'c': False}, {'t': 'Xatolarni e\'tiborsiz qoldirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'try blokida nima bo\'ladi?', 'a': [{'t': 'Xato berishi mumkin bo\'lgan kod', 'c': True}, {'t': 'Xatoni qayta ishlash', 'c': False}, {'t': 'Tozalash kodi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'catch blokida nima bo\'ladi?', 'a': [{'t': 'Xatoni qayta ishlash', 'c': True}, {'t': 'Xato yaratish', 'c': False}, {'t': 'Oddiy kod', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'finally bloki nima uchun?', 'a': [{'t': 'Har doim bajariladigan kod', 'c': True}, {'t': 'Faqat xato bo\'lsa', 'c': False}, {'t': 'Faqat xato bo\'lmasa', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'throw kalit so\'zi nima qiladi?', 'a': [{'t': 'Xato tashlaydi', 'c': True}, {'t': 'Xatoni ushlaydi', 'c': False}, {'t': 'Xatoni to\'g\'rilaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Collections - List', 't': 30, 'o': 25, 'q': [
        {'t': 'List nima?', 'a': [{'t': 'Dinamik o\'lchamli massiv', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Klass', 'c': False}]},
        {'t': 'List<int> list = new List<int>(); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'list.Add(5); nima qiladi?', 'a': [{'t': 'Listga 5 ni qo\'shadi', 'c': True}, {'t': 'Listdan 5 ni o\'chiradi', 'c': False}, {'t': 'List o\'lchamini 5 ga o\'zgartiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'list.Remove(5); nima qiladi?', 'a': [{'t': 'Birinchi 5 ni o\'chiradi', 'c': True}, {'t': '5 ni qo\'shadi', 'c': False}, {'t': 'Barcha 5 larni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'list.Count nima qaytaradi?', 'a': [{'t': 'Elementlar sonini', 'c': True}, {'t': 'Birinchi elementni', 'c': False}, {'t': 'Oxirgi elementni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'List va massiv farqi?', 'a': [{'t': 'List dinamik, massiv statik', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Massiv dinamik', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Collections - Dictionary', 't': 30, 'o': 26, 'q': [
        {'t': 'Dictionary nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'List', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Dictionary<string, int> dict = new Dictionary<string, int>(); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'dict.Add("key", 10); nima qiladi?', 'a': [{'t': 'Kalit va qiymat qo\'shadi', 'c': True}, {'t': 'Faqat qiymat qo\'shadi', 'c': False}, {'t': 'Faqat kalitni qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'dict["key"] nima qaytaradi?', 'a': [{'t': '"key" ga mos qiymatni', 'c': True}, {'t': 'Kalitni', 'c': False}, {'t': 'Barcha qiymatlarni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'dict.ContainsKey("key") nima tekshiradi?', 'a': [{'t': 'Kalit mavjudmi', 'c': True}, {'t': 'Qiymat mavjudmi', 'c': False}, {'t': 'Dictionary bo\'shmi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Dictionary da bir xil kalit ikki marta bo\'lishi mumkinmi?', 'a': [{'t': 'Yo\'q, kalit yagona', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'LINQ - Asoslar', 't': 30, 'o': 27, 'q': [
        {'t': 'LINQ nima?', 'a': [{'t': 'Language Integrated Query', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'LINQ nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlarni so\'rov qilish', 'c': True}, {'t': 'Klass yaratish', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Where() nima qiladi?', 'a': [{'t': 'Filtrlash', 'c': True}, {'t': 'Saralash', 'c': False}, {'t': 'Tanlash', 'c': False}, {'t': 'Qo\'shish', 'c': False}]},
        {'t': 'Select() nima qiladi?', 'a': [{'t': 'Proyeksiya (tanlash)', 'c': True}, {'t': 'Filtrlash', 'c': False}, {'t': 'Saralash', 'c': False}, {'t': 'O\'chirish', 'c': False}]},
        {'t': 'OrderBy() nima qiladi?', 'a': [{'t': 'O\'sish tartibida saralash', 'c': True}, {'t': 'Kamayish tartibida saralash', 'c': False}, {'t': 'Filtrlash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'First() nima qaytaradi?', 'a': [{'t': 'Birinchi elementni', 'c': True}, {'t': 'Oxirgi elementni', 'c': False}, {'t': 'Barcha elementlarni', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'File I/O', 't': 30, 'o': 28, 'q': [
        {'t': 'File.ReadAllText() nima qiladi?', 'a': [{'t': 'Faylning barcha matnini o\'qiydi', 'c': True}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'File.WriteAllText() nima qiladi?', 'a': [{'t': 'Faylga matn yozadi', 'c': True}, {'t': 'Fayldan o\'qiydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'File.Exists() nima tekshiradi?', 'a': [{'t': 'Fayl mavjudmi', 'c': True}, {'t': 'Fayl bo\'shmi', 'c': False}, {'t': 'Fayl ochiqmi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'StreamReader nima uchun?', 'a': [{'t': 'Fayldan o\'qish', 'c': True}, {'t': 'Faylga yozish', 'c': False}, {'t': 'Faylni o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'StreamWriter nima uchun?', 'a': [{'t': 'Faylga yozish', 'c': True}, {'t': 'Fayldan o\'qish', 'c': False}, {'t': 'Faylni o\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'using statement nima uchun?', 'a': [{'t': 'Resurslarni avtomatik yopish', 'c': True}, {'t': 'Namespace ulash', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Delegates va Events', 't': 30, 'o': 29, 'q': [
        {'t': 'Delegate nima?', 'a': [{'t': 'Metod referensi', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'delegate void MyDelegate(); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Event nima?', 'a': [{'t': 'Hodisa xabarnomasi', 'c': True}, {'t': 'Metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'event kalit so\'zi nima uchun?', 'a': [{'t': 'Event e\'lon qilish', 'c': True}, {'t': 'Metod e\'lon qilish', 'c': False}, {'t': 'Klass e\'lon qilish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'EventHandler nima?', 'a': [{'t': 'Standart event delegate', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Lambda va Anonymous metodlar', 't': 30, 'o': 30, 'q': [
        {'t': 'Lambda ifoda nima?', 'a': [{'t': 'Qisqa anonim metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': '(x, y) => x + y nima?', 'a': [{'t': 'Lambda ifoda', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': '=> operatori nima?', 'a': [{'t': 'Lambda operatori', 'c': True}, {'t': 'Taqqoslash operatori', 'c': False}, {'t': 'Qiymat berish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Func<int, int, int> nima?', 'a': [{'t': 'Qiymat qaytaruvchi delegate', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Action<int> nima?', 'a': [{'t': 'Qiymat qaytarmaydigan delegate', 'c': True}, {'t': 'Qiymat qaytaruvchi delegate', 'c': False}, {'t': 'Klass', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Lambda ning afzalligi?', 'a': [{'t': 'Qisqa va tushunarli kod', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam xotira', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🔷 C# DASTURLASH - 30 TA MAVZU")
    print("=" * 80)
    subject = get_or_create_csharp()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T)
    total = sum(len(t['q']) for t in T)
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! 30 ta mavzu, {total} ta test qo'shildi!")
    print(f"📝 To'g'ri javoblar tasodifiy joylashtirildi")
    print("=" * 80)
