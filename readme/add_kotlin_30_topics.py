"""
KOTLIN DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_kotlin():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Kotlin', defaults={'category': cat, 'description': 'Kotlin dasturlash tili - zamonaviy Android dasturlash', 'icon': 'bi-phone-fill', 'order': 7, 'is_active': True})
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
    {'n': 'Kotlin dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Kotlin dasturlash tili qachon yaratilgan?', 'a': [{'t': '2011 yilda', 'c': True}, {'t': '2015 yilda', 'c': False}, {'t': '2008 yilda', 'c': False}, {'t': '2020 yilda', 'c': False}]},
        {'t': 'Kotlin tilini kim yaratgan?', 'a': [{'t': 'Google', 'c': False}, {'t': 'JetBrains kompaniyasi', 'c': True}, {'t': 'Oracle', 'c': False}, {'t': 'Microsoft', 'c': False}]},
        {'t': 'Kotlin ning asosiy qo\'llanilish sohasi?', 'a': [{'t': 'Faqat web dasturlash', 'c': False}, {'t': 'Faqat o\'yin dasturlash', 'c': False}, {'t': 'Android mobil ilovalar', 'c': True}, {'t': 'Faqat desktop', 'c': False}]},
        {'t': 'Kotlin fayl kengaytmasi?', 'a': [{'t': '.kotlin', 'c': False}, {'t': '.kt', 'c': True}, {'t': '.kl', 'c': False}, {'t': '.ktl', 'c': False}]},
        {'t': 'Kotlin qaysi platformada ishlaydi?', 'a': [{'t': 'JVM (Java Virtual Machine)', 'c': True}, {'t': 'Faqat Windows', 'c': False}, {'t': 'Faqat Linux', 'c': False}, {'t': 'Faqat macOS', 'c': False}]},
        {'t': 'Kotlin Java bilan qanday munosabatda?', 'a': [{'t': 'Umuman mos kelmaydi', 'c': False}, {'t': '100% Java bilan mos keladi', 'c': True}, {'t': 'Faqat ba\'zi hollarda mos', 'c': False}, {'t': 'Java o\'rnini bosadi', 'c': False}]},
        {'t': 'Google Kotlin ni Android uchun qachon rasmiy til deb e\'lon qildi?', 'a': [{'t': '2011 yilda', 'c': False}, {'t': '2020 yilda', 'c': False}, {'t': '2017 yilda', 'c': True}, {'t': '2015 yilda', 'c': False}]},
    ]},

    {'n': 'Birinchi Kotlin dasturi', 't': 15, 'o': 2, 'q': [
        {'t': 'Kotlin dasturining asosiy funksiyasi?', 'a': [{'t': 'fun main() {}', 'c': True}, {'t': 'void main() {}', 'c': False}, {'t': 'function main() {}', 'c': False}, {'t': 'start() {}', 'c': False}]},
        {'t': 'Ekranga matn chiqarish uchun qaysi funksiya ishlatiladi?', 'a': [{'t': 'echo()', 'c': False}, {'t': 'console.log()', 'c': False}, {'t': 'println()', 'c': True}, {'t': 'write()', 'c': False}]},
        {'t': 'println("Salom") natijasi?', 'a': [{'t': '"Salom"', 'c': False}, {'t': 'Salom', 'c': True}, {'t': 'print Salom', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'print() va println() orasidagi farq?', 'a': [{'t': 'println() yangi qatorga o\'tadi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'print() tezroq ishlaydi', 'c': False}, {'t': 'println() xato beradi', 'c': False}]},
        {'t': 'Kotlin da qator oxirida ; belgisi majburiymi?', 'a': [{'t': 'Ha, majburiy', 'c': False}, {'t': 'Faqat funksiyalarda', 'c': False}, {'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Faqat siklda', 'c': False}]},
        {'t': 'Kotlin da izoh qanday yoziladi?', 'a': [{'t': 'Faqat #', 'c': False}, {'t': '// yoki /* */', 'c': True}, {'t': 'Faqat <!-- -->', 'c': False}, {'t': '-- izoh', 'c': False}]},
    ]},

    {'n': 'O\'zgaruvchilar: var va val', 't': 20, 'o': 3, 'q': [
        {'t': 'Kotlin da o\'zgaruvchi e\'lon qilish uchun?', 'a': [{'t': 'var va val', 'c': True}, {'t': 'Faqat let', 'c': False}, {'t': 'Faqat dim', 'c': False}, {'t': 'declare', 'c': False}]},
        {'t': 'var x = 10 bu qanday o\'zgaruvchi?', 'a': [{'t': 'O\'zgarmas (immutable)', 'c': False}, {'t': 'O\'zgaruvchan (mutable)', 'c': True}, {'t': 'Konstanta', 'c': False}, {'t': 'Static', 'c': False}]},
        {'t': 'val nomi = "Ali" bu qanday o\'zgaruvchi?', 'a': [{'t': 'O\'zgaruvchan', 'c': False}, {'t': 'Dinamik', 'c': False}, {'t': 'O\'zgarmas (immutable)', 'c': True}, {'t': 'Global', 'c': False}]},
        {'t': 'var va val orasidagi asosiy farq?', 'a': [{'t': 'var o\'zgaradi, val o\'zgarmaydi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'val tezroq ishlaydi', 'c': False}, {'t': 'var faqat sonlar uchun', 'c': False}]},
        {'t': 'val x = 5; x = 10; bu to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': False}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Yo\'q, xato beradi', 'c': True}, {'t': 'Faqat debug rejimida', 'c': False}]},
        {'t': 'O\'zgaruvchi nomida raqam bilan boshlanishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Faqat 0 bilan', 'c': False}, {'t': 'Faqat var da', 'c': False}]},
        {'t': 'Qaysi biri to\'g\'ri e\'lon?', 'a': [{'t': 'var 1son = 10', 'c': False}, {'t': 'var son-1 = 10', 'c': False}, {'t': 'var son1 = 10', 'c': True}, {'t': 'var son 1 = 10', 'c': False}]},
    ]},

    {'n': 'Ma\'lumot turlari: Int, Double, String', 't': 20, 'o': 4, 'q': [
        {'t': 'val x: Int = 5 bu qanday ma\'lumot turi?', 'a': [{'t': 'O\'nlik son', 'c': False}, {'t': 'Butun son', 'c': True}, {'t': 'Matn', 'c': False}, {'t': 'Boolean', 'c': False}]},
        {'t': 'val y: Double = 3.14 bu qanday ma\'lumot turi?', 'a': [{'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'O\'nlik son', 'c': True}, {'t': 'Char', 'c': False}]},
        {'t': 'val ism: String = "Ali" bu qanday ma\'lumot turi?', 'a': [{'t': 'Matn (String)', 'c': True}, {'t': 'Char', 'c': False}, {'t': 'Int', 'c': False}, {'t': 'Boolean', 'c': False}]},
        {'t': 'Kotlin da tip ko\'rsatish majburiymi?', 'a': [{'t': 'Ha, har doim', 'c': False}, {'t': 'Yo\'q, type inference mavjud', 'c': True}, {'t': 'Faqat val da', 'c': False}, {'t': 'Faqat var da', 'c': False}]},
        {'t': 'val x = 10 bu qanday tip?', 'a': [{'t': 'Int', 'c': True}, {'t': 'String', 'c': False}, {'t': 'Double', 'c': False}, {'t': 'Float', 'c': False}]},
        {'t': 'val y = 10.5 bu qanday tip?', 'a': [{'t': 'Int', 'c': False}, {'t': 'Double', 'c': True}, {'t': 'Float', 'c': False}, {'t': 'Long', 'c': False}]},
        {'t': 'Int ning maksimal qiymati?', 'a': [{'t': '32,767', 'c': False}, {'t': '2,147,483,647', 'c': True}, {'t': '65,535', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'Katta butun sonlar uchun qaysi tip ishlatiladi?', 'a': [{'t': 'Long', 'c': True}, {'t': 'Int', 'c': False}, {'t': 'BigInt', 'c': False}, {'t': 'Double', 'c': False}]},
    ]},

    {'n': 'Boolean va Char turlari', 't': 15, 'o': 5, 'q': [
        {'t': 'Boolean tipida qanday qiymatlar bo\'ladi?', 'a': [{'t': '0 va 1', 'c': False}, {'t': 'true va false', 'c': True}, {'t': 'yes va no', 'c': False}, {'t': 'on va off', 'c': False}]},
        {'t': 'val javob: Boolean = true bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat var bilan', 'c': False}]},
        {'t': 'Char tipi uchun qaysi belgi ishlatiladi?', 'a': [{'t': 'Bitta qo\'shtirnoq \'a\'', 'c': True}, {'t': 'Qo\'sh qo\'shtirnoq "a"', 'c': False}, {'t': 'Kvadrat qavs [a]', 'c': False}, {'t': 'Oddiy qavs (a)', 'c': False}]},
        {'t': 'val harf: Char = \'A\' bu to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat String uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'val x: Char = "A" bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri, xato', 'c': True}, {'t': 'To\'g\'ri', 'c': False}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Faqat var da', 'c': False}]},
        {'t': 'Boolean qiymatni qanday tekshirish mumkin?', 'a': [{'t': 'if (javob == 1) {}', 'c': False}, {'t': 'if (javob) {}', 'c': True}, {'t': 'if (javob == "true") {}', 'c': False}, {'t': 'check(javob)', 'c': False}]},
    ]},

    {'n': 'Arifmetik operatorlar', 't': 20, 'o': 6, 'q': [
        {'t': 'Kotlin da qo\'shish operatori?', 'a': [{'t': 'add', 'c': False}, {'t': '+', 'c': True}, {'t': 'plus', 'c': False}, {'t': '&', 'c': False}]},
        {'t': '10 + 5 natijasi?', 'a': [{'t': '105', 'c': False}, {'t': '15', 'c': True}, {'t': '50', 'c': False}, {'t': '5', 'c': False}]},
        {'t': '20 - 8 natijasi?', 'a': [{'t': '12', 'c': True}, {'t': '28', 'c': False}, {'t': '8', 'c': False}, {'t': '160', 'c': False}]},
        {'t': '6 * 7 natijasi?', 'a': [{'t': '13', 'c': False}, {'t': '67', 'c': False}, {'t': '42', 'c': True}, {'t': '49', 'c': False}]},
        {'t': '20 / 4 natijasi?', 'a': [{'t': '4', 'c': False}, {'t': '5', 'c': True}, {'t': '80', 'c': False}, {'t': '16', 'c': False}]},
        {'t': '17 % 5 (qoldiq) natijasi?', 'a': [{'t': '2', 'c': True}, {'t': '3', 'c': False}, {'t': '5', 'c': False}, {'t': '12', 'c': False}]},
        {'t': 'Darajaga ko\'tarish uchun qaysi funksiya ishlatiladi?', 'a': [{'t': '^', 'c': False}, {'t': 'pow()', 'c': True}, {'t': '**', 'c': False}, {'t': 'power()', 'c': False}]},
        {'t': 'var x = 10; x++ natijasi?', 'a': [{'t': '10', 'c': False}, {'t': '11', 'c': True}, {'t': '9', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'String bilan ishlash', 't': 25, 'o': 7, 'q': [
        {'t': 'Stringlarni birlashtirish uchun?', 'a': [{'t': '+ operatori', 'c': True}, {'t': 'concat()', 'c': False}, {'t': 'merge()', 'c': False}, {'t': 'join()', 'c': False}]},
        {'t': '"Salom" + " " + "Dunyo" natijasi?', 'a': [{'t': 'SalomDunyo', 'c': False}, {'t': 'Salom Dunyo', 'c': True}, {'t': 'Salom+Dunyo', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'String interpolatsiya qanday amalga oshiriladi?', 'a': [{'t': '%s', 'c': False}, {'t': '${o\'zgaruvchi}', 'c': True}, {'t': '{o\'zgaruvchi}', 'c': False}, {'t': '@o\'zgaruvchi', 'c': False}]},
        {'t': 'val ism = "Ali"; "Salom $ism" natijasi?', 'a': [{'t': 'Salom $ism', 'c': False}, {'t': 'Salom Ali', 'c': True}, {'t': 'Salom {Ali}', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'String uzunligini aniqlash?', 'a': [{'t': 'length', 'c': True}, {'t': 'size', 'c': False}, {'t': 'count', 'c': False}, {'t': 'len()', 'c': False}]},
        {'t': '"Kotlin".length natijasi?', 'a': [{'t': '5', 'c': False}, {'t': '7', 'c': False}, {'t': '6', 'c': True}, {'t': '8', 'c': False}]},
        {'t': 'Stringni katta harflarga o\'zgartirish?', 'a': [{'t': 'upper()', 'c': False}, {'t': 'toUpperCase()', 'c': True}, {'t': 'capitalize()', 'c': False}, {'t': 'big()', 'c': False}]},
        {'t': '"kotlin".toUpperCase() natijasi?', 'a': [{'t': 'Kotlin', 'c': False}, {'t': 'KOTLIN', 'c': True}, {'t': 'kotlin', 'c': False}, {'t': 'KoTlIn', 'c': False}]},
    ]},

    {'n': 'Taqqoslash operatorlari', 't': 20, 'o': 8, 'q': [
        {'t': 'Tenglik operatori?', 'a': [{'t': '=', 'c': False}, {'t': '==', 'c': True}, {'t': '===', 'c': False}, {'t': 'eq', 'c': False}]},
        {'t': '5 == 5 natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '5', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Teng emaslik operatori?', 'a': [{'t': '!=', 'c': True}, {'t': '<>', 'c': False}, {'t': '!==', 'c': False}, {'t': 'not', 'c': False}]},
        {'t': '10 > 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '10', 'c': False}, {'t': '5', 'c': False}]},
        {'t': '3 < 8 natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '3', 'c': False}, {'t': '8', 'c': False}]},
        {'t': '7 >= 7 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '7', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '5 <= 3 natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': '5', 'c': False}, {'t': '3', 'c': False}]},
    ]},

    {'n': 'Mantiqiy operatorlar', 't': 20, 'o': 9, 'q': [
        {'t': 'Mantiqiy VA (AND) operatori?', 'a': [{'t': '&', 'c': False}, {'t': '&&', 'c': True}, {'t': 'and', 'c': False}, {'t': 'AND', 'c': False}]},
        {'t': 'true && true natijasi?', 'a': [{'t': 'false', 'c': False}, {'t': 'true', 'c': True}, {'t': '1', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'true && false natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': '0', 'c': False}, {'t': 'null', 'c': False}]},
        {'t': 'Mantiqiy YOKI (OR) operatori?', 'a': [{'t': '|', 'c': False}, {'t': '||', 'c': True}, {'t': 'or', 'c': False}, {'t': 'OR', 'c': False}]},
        {'t': 'false || true natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '1', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Mantiqiy EMAS (NOT) operatori?', 'a': [{'t': 'not', 'c': False}, {'t': '!', 'c': True}, {'t': '~', 'c': False}, {'t': 'NOT', 'c': False}]},
        {'t': '!true natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': '0', 'c': False}, {'t': 'null', 'c': False}]},
        {'t': '!false natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '1', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'if shartli operatori', 't': 25, 'o': 10, 'q': [
        {'t': 'if operatori sintaksisi?', 'a': [{'t': 'if shart {}', 'c': False}, {'t': 'if (shart) {}', 'c': True}, {'t': 'if [shart] {}', 'c': False}, {'t': 'if {shart}', 'c': False}]},
        {'t': 'val x = 10; if (x > 5) print("Katta") natijasi?', 'a': [{'t': 'Hech narsa', 'c': False}, {'t': 'Katta', 'c': True}, {'t': '10', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'if-else sintaksisi to\'g\'rimi? if (shart) {} else {}', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat if kerak', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'val y = 3; if (y < 5) "Kichik" else "Katta" natijasi?', 'a': [{'t': 'Katta', 'c': False}, {'t': 'Kichik', 'c': True}, {'t': '3', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Kotlin da if ifoda (expression) bo\'lishi mumkinmi?', 'a': [{'t': 'Yo\'q, faqat operator', 'c': False}, {'t': 'Ha, qiymat qaytarishi mumkin', 'c': True}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'val max = if (a > b) a else b bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat var bilan', 'c': False}]},
        {'t': 'if-else if-else zanjiri mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat 2 ta shart', 'c': False}, {'t': 'Faqat when bilan', 'c': False}]},
    ]},

    {'n': 'when operatori (switch)', 't': 25, 'o': 11, 'q': [
        {'t': 'when operatori nima uchun ishlatiladi?', 'a': [{'t': 'Ko\'p shartlarni tekshirish', 'c': True}, {'t': 'Faqat sikl uchun', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'O\'zgaruvchi e\'lon qilish', 'c': False}]},
        {'t': 'when operatori Java dagi qaysi operatorga o\'xshaydi?', 'a': [{'t': 'if', 'c': False}, {'t': 'switch', 'c': True}, {'t': 'for', 'c': False}, {'t': 'while', 'c': False}]},
        {'t': 'when (x) { 1 -> "Bir" } sintaksisi to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat if bilan', 'c': False}]},
        {'t': 'when da else qismi majburiymi?', 'a': [{'t': 'Ha, har doim', 'c': False}, {'t': 'Yo\'q, lekin tavsiya etiladi', 'c': True}, {'t': 'Faqat expression da', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'when da bir nechta qiymatni tekshirish: when (x) { 1, 2 -> "Kichik" }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat if bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'when argumentsiz ishlatilishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ha, if-else zanjiri o\'rniga', 'c': True}, {'t': 'Faqat funksiyada', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'when da diapazon tekshirish: when (x) { in 1..10 -> "Kichik" }', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat if da', 'c': False}]},
    ]},

    {'n': 'for sikli', 't': 25, 'o': 12, 'q': [
        {'t': 'for sikli sintaksisi?', 'a': [{'t': 'for (i in 1..5) {}', 'c': True}, {'t': 'for (i = 1; i <= 5; i++) {}', 'c': False}, {'t': 'for i in range(1, 5) {}', 'c': False}, {'t': 'for (i to 5) {}', 'c': False}]},
        {'t': 'for (i in 1..5) print(i) nechta marta ishlaydi?', 'a': [{'t': '4 marta', 'c': False}, {'t': '5 marta', 'c': True}, {'t': '6 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': '1..5 bu nima?', 'a': [{'t': 'Diapazon (range)', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'for (i in 1 until 5) nechta marta ishlaydi?', 'a': [{'t': '5 marta', 'c': False}, {'t': '4 marta', 'c': True}, {'t': '3 marta', 'c': False}, {'t': '6 marta', 'c': False}]},
        {'t': 'Teskari tartibda sikl: for (i in 5 downTo 1)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat while bilan', 'c': False}]},
        {'t': 'Qadam bilan sikl: for (i in 1..10 step 2) nechta marta?', 'a': [{'t': '10 marta', 'c': False}, {'t': '5 marta', 'c': True}, {'t': '2 marta', 'c': False}, {'t': '20 marta', 'c': False}]},
        {'t': 'Massiv bo\'ylab sikl: for (item in array) to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat while bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Indeks bilan sikl: for ((index, value) in array.withIndex())', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat forEach', 'c': False}]},
    ]},

    {'n': 'while va do-while sikllari', 't': 20, 'o': 13, 'q': [
        {'t': 'while sikli sintaksisi?', 'a': [{'t': 'while shart {}', 'c': False}, {'t': 'while (shart) {}', 'c': True}, {'t': 'while [shart] {}', 'c': False}, {'t': 'while {shart}', 'c': False}]},
        {'t': 'var x = 0; while (x < 3) { x++ } x ning qiymati?', 'a': [{'t': '2', 'c': False}, {'t': '3', 'c': True}, {'t': '4', 'c': False}, {'t': '0', 'c': False}]},
        {'t': 'while va do-while orasidagi farq?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'while tezroq', 'c': False}, {'t': 'do-while xato beradi', 'c': False}]},
        {'t': 'do-while sintaksisi?', 'a': [{'t': 'do {} while (shart)', 'c': True}, {'t': 'do (shart) {}', 'c': False}, {'t': 'while {} do (shart)', 'c': False}, {'t': 'do while shart {}', 'c': False}]},
        {'t': 'Cheksiz sikl qanday yaratiladi?', 'a': [{'t': 'while (false)', 'c': False}, {'t': 'while (true)', 'c': True}, {'t': 'while (1)', 'c': False}, {'t': 'while ()', 'c': False}]},
        {'t': 'Sikldan chiqish uchun qaysi kalit so\'z?', 'a': [{'t': 'exit', 'c': False}, {'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'Sikl iteratsiyasini o\'tkazib yuborish uchun?', 'a': [{'t': 'continue', 'c': True}, {'t': 'skip', 'c': False}, {'t': 'next', 'c': False}, {'t': 'pass', 'c': False}]},
    ]},

    {'n': 'Funksiyalar asoslari', 't': 25, 'o': 14, 'q': [
        {'t': 'Funksiya qanday e\'lon qilinadi?', 'a': [{'t': 'function ism() {}', 'c': False}, {'t': 'fun ism() {}', 'c': True}, {'t': 'def ism() {}', 'c': False}, {'t': 'void ism() {}', 'c': False}]},
        {'t': 'fun salom() { println("Salom") } bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat main da', 'c': False}]},
        {'t': 'Funksiyani chaqirish?', 'a': [{'t': 'salom()', 'c': True}, {'t': 'call salom()', 'c': False}, {'t': 'run salom', 'c': False}, {'t': 'execute salom', 'c': False}]},
        {'t': 'Parametrli funksiya: fun salom(ism: String)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat Int uchun', 'c': False}]},
        {'t': 'Qiymat qaytaruvchi funksiya: fun yig\'indi(a: Int, b: Int): Int', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat return kerak', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'fun yig\'indi(a: Int, b: Int): Int { return a + b } to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'return kerak emas', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Bir qatorli funksiya: fun yig\'indi(a: Int, b: Int) = a + b', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'return kerak', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Hech narsa qaytarmaydigan funksiya qaysi tipga ega?', 'a': [{'t': 'void', 'c': False}, {'t': 'Unit', 'c': True}, {'t': 'null', 'c': False}, {'t': 'None', 'c': False}]},
    ]},

    {'n': 'Funksiya parametrlari va default qiymatlar', 't': 25, 'o': 15, 'q': [
        {'t': 'Default parametr qiymati: fun salom(ism: String = "Mehmon")', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat Int uchun', 'c': False}]},
        {'t': 'fun salom(ism: String = "Ali") chaqirilsa: salom()', 'a': [{'t': 'Xato', 'c': False}, {'t': '"Ali" ishlatiladi', 'c': True}, {'t': 'Bo\'sh string', 'c': False}, {'t': 'null', 'c': False}]},
        {'t': 'Named arguments: salom(ism = "Vali", yosh = 20)', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat pozitsion', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Named arguments tartibini o\'zgartirish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat default bilan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'O\'zgaruvchan parametrlar soni: fun yig\'indi(vararg sonlar: Int)', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat Array', 'c': False}]},
        {'t': 'vararg parametr ichida nima bo\'ladi?', 'a': [{'t': 'List', 'c': False}, {'t': 'Array', 'c': True}, {'t': 'Set', 'c': False}, {'t': 'Map', 'c': False}]},
        {'t': 'Funksiyaga funksiya parametr sifatida berilishi mumkinmi?', 'a': [{'t': 'Ha, higher-order functions', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat lambda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},

    {'n': 'Massivlar (Arrays)', 't': 25, 'o': 16, 'q': [
        {'t': 'Massiv qanday yaratiladi?', 'a': [{'t': 'arrayOf(1, 2, 3)', 'c': True}, {'t': 'array(1, 2, 3)', 'c': False}, {'t': '[1, 2, 3]', 'c': False}, {'t': 'new Array(1, 2, 3)', 'c': False}]},
        {'t': 'val arr = arrayOf(1, 2, 3); arr[0] qiymati?', 'a': [{'t': '0', 'c': False}, {'t': '1', 'c': True}, {'t': '2', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Massiv elementiga qanday murojaat qilinadi?', 'a': [{'t': 'arr.get(0)', 'c': False}, {'t': 'arr[0]', 'c': True}, {'t': 'arr(0)', 'c': False}, {'t': 'arr{0}', 'c': False}]},
        {'t': 'Massiv uzunligi: arr.size yoki arr.length?', 'a': [{'t': 'arr.size', 'c': True}, {'t': 'arr.length', 'c': False}, {'t': 'arr.count', 'c': False}, {'t': 'arr.len', 'c': False}]},
        {'t': 'Massiv elementini o\'zgartirish: arr[0] = 10', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat var bilan', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Bo\'sh massiv yaratish: arrayOfNulls<Int>(5)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat arrayOf', 'c': False}]},
        {'t': 'Massivda element borligini tekshirish: 5 in arr', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat contains()', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'IntArray, DoubleArray bu nima?', 'a': [{'t': 'Maxsus primitiv massivlar', 'c': True}, {'t': 'Oddiy massivlar', 'c': False}, {'t': 'List turlari', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Listlar bilan ishlash', 't': 25, 'o': 17, 'q': [
        {'t': 'O\'zgarmas list yaratish?', 'a': [{'t': 'listOf(1, 2, 3)', 'c': True}, {'t': 'list(1, 2, 3)', 'c': False}, {'t': 'List(1, 2, 3)', 'c': False}, {'t': 'newList(1, 2, 3)', 'c': False}]},
        {'t': 'O\'zgaruvchan list yaratish?', 'a': [{'t': 'listOf()', 'c': False}, {'t': 'mutableListOf()', 'c': True}, {'t': 'arrayListOf()', 'c': False}, {'t': 'list()', 'c': False}]},
        {'t': 'val list = listOf(1, 2, 3); list[0] qiymati?', 'a': [{'t': '1', 'c': True}, {'t': '0', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Listga element qo\'shish: list.add(4)', 'a': [{'t': 'Faqat mutableList da', 'c': True}, {'t': 'Har doim ishlaydi', 'c': False}, {'t': 'Hech qachon ishlamaydi', 'c': False}, {'t': 'Faqat arrayOf da', 'c': False}]},
        {'t': 'Listdan element o\'chirish: list.remove(2)', 'a': [{'t': 'Faqat mutableList da', 'c': True}, {'t': 'Har doim ishlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Faqat arrayOf da', 'c': False}]},
        {'t': 'List uzunligi: list.size', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri, list.length', 'c': False}, {'t': 'list.count', 'c': False}, {'t': 'list.len', 'c': False}]},
        {'t': 'Listda element borligini tekshirish: 5 in list', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat contains()', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Bo\'sh list yaratish: emptyList<Int>()', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat listOf()', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Set va Map to\'plamlari', 't': 25, 'o': 18, 'q': [
        {'t': 'Set nima?', 'a': [{'t': 'Takrorlanmaydigan elementlar to\'plami', 'c': True}, {'t': 'Oddiy list', 'c': False}, {'t': 'Kalit-qiymat juftligi', 'c': False}, {'t': 'Massiv', 'c': False}]},
        {'t': 'Set yaratish: setOf(1, 2, 2, 3) nechta element?', 'a': [{'t': '4 ta', 'c': False}, {'t': '3 ta', 'c': True}, {'t': '2 ta', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'O\'zgaruvchan Set: mutableSetOf()', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat setOf()', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Map nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Oddiy list', 'c': False}, {'t': 'Takrorlanmaydigan to\'plam', 'c': False}, {'t': 'Massiv', 'c': False}]},
        {'t': 'Map yaratish: mapOf("a" to 1, "b" to 2)', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat hashMapOf', 'c': False}]},
        {'t': 'Map dan qiymat olish: map["a"]', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat map.get("a")', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'O\'zgaruvchan Map: mutableMapOf()', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat mapOf()', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Map ga element qo\'shish: map["c"] = 3', 'a': [{'t': 'Faqat mutableMap da', 'c': True}, {'t': 'Har doim ishlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Faqat put() bilan', 'c': False}]},
    ]},

    {'n': 'Null Safety asoslari', 't': 25, 'o': 19, 'q': [
        {'t': 'Kotlin da null xavfsizligi (null safety) bormi?', 'a': [{'t': 'Ha, til darajasida', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Nullable tip qanday belgilanadi?', 'a': [{'t': 'String?', 'c': True}, {'t': 'String!', 'c': False}, {'t': 'String*', 'c': False}, {'t': 'nullable String', 'c': False}]},
        {'t': 'var ism: String = null bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri, xato', 'c': True}, {'t': 'To\'g\'ri', 'c': False}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Faqat val bilan', 'c': False}]},
        {'t': 'var ism: String? = null bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat var bilan', 'c': False}]},
        {'t': 'Safe call operatori?', 'a': [{'t': '?.', 'c': True}, {'t': '?', 'c': False}, {'t': '!.', 'c': False}, {'t': '!!', 'c': False}]},
        {'t': 'val uzunlik = ism?.length bu nima qiladi?', 'a': [{'t': 'ism null bo\'lsa null qaytaradi', 'c': True}, {'t': 'Har doim xato', 'c': False}, {'t': 'ism null bo\'lsa 0 qaytaradi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}]},
        {'t': 'Elvis operatori: val uzunlik = ism?.length ?: 0', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat if bilan', 'c': False}]},
        {'t': 'Not-null assertion: ism!! nima qiladi?', 'a': [{'t': 'null bo\'lsa xato beradi', 'c': True}, {'t': 'null ni 0 ga aylantiradi', 'c': False}, {'t': 'Xavfsiz tekshiradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'Lambda funksiyalar', 't': 25, 'o': 20, 'q': [
        {'t': 'Lambda funksiya nima?', 'a': [{'t': 'Nomsiz funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Class', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'Lambda sintaksisi: { x: Int -> x * 2 }', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat fun bilan', 'c': False}]},
        {'t': 'val kvadrat = { x: Int -> x * x }; kvadrat(5) natijasi?', 'a': [{'t': '10', 'c': False}, {'t': '25', 'c': True}, {'t': '5', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Lambda parametrsiz: val salom = { println("Salom") }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Parametr kerak', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Lambda bir parametrli bo\'lsa, it ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, default nom', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat 2 parametrda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'list.filter { it > 5 } nima qiladi?', 'a': [{'t': '5 dan katta elementlarni filtrlaydi', 'c': True}, {'t': 'Hammasi 5 ga teng', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'list.map { it * 2 } nima qiladi?', 'a': [{'t': 'Har bir elementni 2 ga ko\'paytiradi', 'c': True}, {'t': 'Faqat filtrlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Higher-Order funksiyalar', 't': 25, 'o': 21, 'q': [
        {'t': 'Higher-order funksiya nima?', 'a': [{'t': 'Funksiyani parametr yoki natija sifatida qabul qiladi', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Faqat lambda', 'c': False}, {'t': 'Class metodi', 'c': False}]},
        {'t': 'fun amal(x: Int, f: (Int) -> Int) = f(x) bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat lambda', 'c': False}]},
        {'t': 'forEach nima qiladi?', 'a': [{'t': 'Har bir element uchun amal bajaradi', 'c': True}, {'t': 'Faqat filtrlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'filter funksiyasi nima qaytaradi?', 'a': [{'t': 'Shartga mos elementlar', 'c': True}, {'t': 'Birinchi element', 'c': False}, {'t': 'Boolean', 'c': False}, {'t': 'Int', 'c': False}]},
        {'t': 'map funksiyasi nima qiladi?', 'a': [{'t': 'Har bir elementni o\'zgartiradi', 'c': True}, {'t': 'Faqat filtrlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'reduce funksiyasi nima qiladi?', 'a': [{'t': 'Elementlarni bitta qiymatga jamlaydi', 'c': True}, {'t': 'Faqat filtrlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'listOf(1,2,3).reduce { acc, i -> acc + i } natijasi?', 'a': [{'t': '6', 'c': True}, {'t': '3', 'c': False}, {'t': '1', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Classlar va obyektlar', 't': 30, 'o': 22, 'q': [
        {'t': 'Class qanday e\'lon qilinadi?', 'a': [{'t': 'class Ism {}', 'c': True}, {'t': 'Class Ism {}', 'c': False}, {'t': 'def class Ism {}', 'c': False}, {'t': 'new class Ism', 'c': False}]},
        {'t': 'class Odam { var ism = "Ali" } bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat val', 'c': False}]},
        {'t': 'Obyekt qanday yaratiladi?', 'a': [{'t': 'val odam = Odam()', 'c': True}, {'t': 'val odam = new Odam()', 'c': False}, {'t': 'Odam odam = new Odam()', 'c': False}, {'t': 'create Odam()', 'c': False}]},
        {'t': 'Primary constructor: class Odam(val ism: String)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat var', 'c': False}]},
        {'t': 'class Odam(val ism: String, var yosh: Int) nechta parametr?', 'a': [{'t': '1 ta', 'c': False}, {'t': '2 ta', 'c': True}, {'t': '0 ta', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Class ichida funksiya (metod) bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat static', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'val odam = Odam("Ali", 25); odam.ism qanday murojaat?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat getIsm()', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'init bloki nima uchun?', 'a': [{'t': 'Constructor kodini yozish', 'c': True}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'O\'zgaruvchi e\'lon qilish', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Inheritance (Meros olish)', 't': 30, 'o': 23, 'q': [
        {'t': 'Kotlin da barcha classlar qaysi classdan meros oladi?', 'a': [{'t': 'Object', 'c': False}, {'t': 'Any', 'c': True}, {'t': 'Base', 'c': False}, {'t': 'Super', 'c': False}]},
        {'t': 'Meros olish uchun class qanday bo\'lishi kerak?', 'a': [{'t': 'open', 'c': True}, {'t': 'public', 'c': False}, {'t': 'abstract', 'c': False}, {'t': 'sealed', 'c': False}]},
        {'t': 'open class Hayvon; class Mushuk : Hayvon() bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat extends', 'c': False}]},
        {'t': 'Metodni override qilish uchun nima kerak?', 'a': [{'t': 'open va override', 'c': True}, {'t': 'Faqat override', 'c': False}, {'t': 'Faqat open', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'open class A { open fun salom() {} }; class B : A() { override fun salom() {} }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'open kerak emas', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'super kalit so\'zi nima uchun?', 'a': [{'t': 'Ota-class ga murojaat', 'c': True}, {'t': 'Yangi class yaratish', 'c': False}, {'t': 'O\'zgaruvchi e\'lon qilish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Kotlin da bir nechta classdan meros olish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat bitta', 'c': True}, {'t': 'Ha, cheksiz', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Faqat interface', 'c': False}]},
    ]},

    {'n': 'Abstract class va Interface', 't': 30, 'o': 24, 'q': [
        {'t': 'Abstract class nima?', 'a': [{'t': 'To\'liq amalga oshirilmagan class', 'c': True}, {'t': 'Oddiy class', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Object', 'c': False}]},
        {'t': 'abstract class Shakl { abstract fun yuza(): Double }', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat interface', 'c': False}]},
        {'t': 'Abstract classdan obyekt yaratish mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan mumkin', 'c': False}, {'t': 'Faqat meros olgan class', 'c': False}]},
        {'t': 'Interface qanday e\'lon qilinadi?', 'a': [{'t': 'interface Ism {}', 'c': True}, {'t': 'class interface Ism {}', 'c': False}, {'t': 'abstract interface Ism', 'c': False}, {'t': 'def interface Ism', 'c': False}]},
        {'t': 'Interface da property bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, lekin abstract', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat val', 'c': False}, {'t': 'Faqat var', 'c': False}]},
        {'t': 'Interface da funksiya tanasi (body) bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, default implementation', 'c': True}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Faqat abstract', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Bir nechta interface implement qilish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'class Aylana : Shakl, Rangli bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat bitta', 'c': False}]},
    ]},

    {'n': 'Data class', 't': 25, 'o': 25, 'q': [
        {'t': 'Data class nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumot saqlash uchun', 'c': True}, {'t': 'Faqat funksiyalar uchun', 'c': False}, {'t': 'Interface yaratish', 'c': False}, {'t': 'Abstract class', 'c': False}]},
        {'t': 'data class Odam(val ism: String, val yosh: Int) bu to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class', 'c': False}]},
        {'t': 'Data class avtomatik qaysi metodlarni yaratadi?', 'a': [{'t': 'equals(), hashCode(), toString(), copy()', 'c': True}, {'t': 'Faqat toString()', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Faqat equals()', 'c': False}]},
        {'t': 'val odam1 = Odam("Ali", 25); val odam2 = odam1.copy(yosh = 26)', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat clone()', 'c': False}]},
        {'t': 'Data class kamida nechta parametr talab qiladi?', 'a': [{'t': '0 ta', 'c': False}, {'t': '1 ta', 'c': True}, {'t': '2 ta', 'c': False}, {'t': '3 ta', 'c': False}]},
        {'t': 'Data class open bo\'lishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan mumkin', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Destructuring: val (ism, yosh) = odam bu to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat array uchun', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Object va Companion object', 't': 25, 'o': 26, 'q': [
        {'t': 'object kalit so\'zi nima yaratadi?', 'a': [{'t': 'Singleton obyekt', 'c': True}, {'t': 'Oddiy class', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Abstract class', 'c': False}]},
        {'t': 'object Database { fun connect() {} } bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class', 'c': False}]},
        {'t': 'object dan nechta instance yaratiladi?', 'a': [{'t': 'Faqat 1 ta', 'c': True}, {'t': 'Cheksiz', 'c': False}, {'t': '0 ta', 'c': False}, {'t': '2 ta', 'c': False}]},
        {'t': 'Companion object nima?', 'a': [{'t': 'Class ichidagi static o\'xshash obyekt', 'c': True}, {'t': 'Oddiy obyekt', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Abstract class', 'c': False}]},
        {'t': 'class Odam { companion object { fun yaratish() {} } }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat object', 'c': False}]},
        {'t': 'Companion object ga qanday murojaat qilinadi?', 'a': [{'t': 'Odam.yaratish()', 'c': True}, {'t': 'Odam().yaratish()', 'c': False}, {'t': 'new Odam.yaratish()', 'c': False}, {'t': 'Odam::yaratish()', 'c': False}]},
        {'t': 'Bir classda nechta companion object bo\'lishi mumkin?', 'a': [{'t': 'Faqat 1 ta', 'c': True}, {'t': 'Cheksiz', 'c': False}, {'t': '2 ta', 'c': False}, {'t': '0 ta', 'c': False}]},
    ]},

    {'n': 'Extension funksiyalar', 't': 25, 'o': 27, 'q': [
        {'t': 'Extension funksiya nima?', 'a': [{'t': 'Mavjud classga yangi funksiya qo\'shish', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Class yaratish', 'c': False}, {'t': 'Interface', 'c': False}]},
        {'t': 'fun String.birinchiHarf() = this[0] bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class ichida', 'c': False}]},
        {'t': 'Extension funksiyada this nima?', 'a': [{'t': 'Kengaytirilayotgan obyekt', 'c': True}, {'t': 'Funksiya o\'zi', 'c': False}, {'t': 'null', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '"Kotlin".birinchiHarf() natijasi?', 'a': [{'t': 'K', 'c': True}, {'t': 'Kotlin', 'c': False}, {'t': 'n', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Extension funksiya class ichidagi private ga kirishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan mumkin', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'fun Int.kvadrat() = this * this; 5.kvadrat() natijasi?', 'a': [{'t': '10', 'c': False}, {'t': '25', 'c': True}, {'t': '5', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Extension property yaratish mumkinmi?', 'a': [{'t': 'Ha, lekin backing field yo\'q', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat val', 'c': False}, {'t': 'Faqat var', 'c': False}]},
    ]},

    {'n': 'Sealed class va Enum', 't': 25, 'o': 28, 'q': [
        {'t': 'Enum class nima?', 'a': [{'t': 'Cheklangan konstantalar to\'plami', 'c': True}, {'t': 'Oddiy class', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Abstract class', 'c': False}]},
        {'t': 'enum class Rang { QIZIL, YASHIL, KOK } bu to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class', 'c': False}]},
        {'t': 'Enum qiymatlariga qanday murojaat qilinadi?', 'a': [{'t': 'Rang.QIZIL', 'c': True}, {'t': 'Rang[QIZIL]', 'c': False}, {'t': 'Rang(QIZIL)', 'c': False}, {'t': 'new Rang.QIZIL', 'c': False}]},
        {'t': 'Sealed class nima?', 'a': [{'t': 'Cheklangan meros ierarxiyasi', 'c': True}, {'t': 'Oddiy class', 'c': False}, {'t': 'Enum', 'c': False}, {'t': 'Interface', 'c': False}]},
        {'t': 'sealed class Natija; class Muvaffaqiyat : Natija(); class Xato : Natija()', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat enum', 'c': False}]},
        {'t': 'Sealed class meroschilarini when da tekshirish to\'liq bo\'lishi kerakmi?', 'a': [{'t': 'Ha, else kerak emas', 'c': True}, {'t': 'Yo\'q, else majburiy', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Sealed class va Enum orasidagi farq?', 'a': [{'t': 'Sealed class har xil turda bo\'lishi mumkin', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Enum kuchliroq', 'c': False}, {'t': 'Sealed class eski', 'c': False}]},
    ]},

    {'n': 'Exception handling', 't': 25, 'o': 29, 'q': [
        {'t': 'Xatolarni ushlash uchun qaysi blok ishlatiladi?', 'a': [{'t': 'try-catch', 'c': True}, {'t': 'if-else', 'c': False}, {'t': 'when', 'c': False}, {'t': 'do-while', 'c': False}]},
        {'t': 'try { kod } catch (e: Exception) { } bu to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat Java da', 'c': False}]},
        {'t': 'finally bloki nima uchun?', 'a': [{'t': 'Har doim bajariladigan kod', 'c': True}, {'t': 'Faqat xato bo\'lsa', 'c': False}, {'t': 'Faqat xato bo\'lmasa', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'try { } catch (e: Exception) { } finally { } tartib to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'finally birinchi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Kotlin da checked exception bormi?', 'a': [{'t': 'Yo\'q, hammasi unchecked', 'c': True}, {'t': 'Ha, bor', 'c': False}, {'t': 'Ba\'zan bor', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Xato tashlash: throw Exception("Xato")', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat try ichida', 'c': False}]},
        {'t': 'try ifoda (expression) bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, qiymat qaytarishi mumkin', 'c': True}, {'t': 'Yo\'q, faqat operator', 'c': False}, {'t': 'Faqat catch', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},

    {'n': 'Scope funksiyalar: let, run, with, apply, also', 't': 30, 'o': 30, 'q': [
        {'t': 'Scope funksiyalar nima?', 'a': [{'t': 'Obyekt kontekstida kod bajarish', 'c': True}, {'t': 'Oddiy funksiyalar', 'c': False}, {'t': 'Class yaratish', 'c': False}, {'t': 'Interface', 'c': False}]},
        {'t': 'let funksiyasi nima qaytaradi?', 'a': [{'t': 'Lambda natijasi', 'c': True}, {'t': 'Obyektning o\'zi', 'c': False}, {'t': 'null', 'c': False}, {'t': 'Unit', 'c': False}]},
        {'t': 'odam?.let { println(it.ism) } null safety uchun to\'g\'rimi?', 'a': [{'t': 'Noto\'g\'ri', 'c': False}, {'t': 'To\'g\'ri', 'c': True}, {'t': 'Faqat run', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'apply funksiyasi nima qaytaradi?', 'a': [{'t': 'Obyektning o\'zi', 'c': True}, {'t': 'Lambda natijasi', 'c': False}, {'t': 'null', 'c': False}, {'t': 'Unit', 'c': False}]},
        {'t': 'val odam = Odam().apply { ism = "Ali"; yosh = 25 } to\'g\'rimi?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat let', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'run funksiyasi apply dan farqi?', 'a': [{'t': 'run lambda natijasini qaytaradi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'run tezroq', 'c': False}, {'t': 'apply yangi', 'c': False}]},
        {'t': 'with funksiyasi qanday chaqiriladi?', 'a': [{'t': 'with(obyekt) { }', 'c': True}, {'t': 'obyekt.with { }', 'c': False}, {'t': 'obyekt with { }', 'c': False}, {'t': 'with { obyekt }', 'c': False}]},
        {'t': 'also funksiyasi nima uchun?', 'a': [{'t': 'Qo\'shimcha amallar, obyektni qaytaradi', 'c': True}, {'t': 'Faqat chop etish', 'c': False}, {'t': 'Xato ushlash', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'let va also orasidagi farq?', 'a': [{'t': 'let lambda natijasi, also obyekt', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'let yangi', 'c': False}, {'t': 'also eski', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_kotlin()
    add_topics(subj, T)
    print(f"\n✅ Kotlin: {len(T)} ta mavzu muvaffaqiyatli qo\'shildi!")
