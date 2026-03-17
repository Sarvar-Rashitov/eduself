"""
SWIFT DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_swift():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Swift', defaults={'category': cat, 'description': 'Swift dasturlash tili - iOS va macOS uchun zamonaviy dasturlash', 'icon': 'bi-apple', 'order': 9, 'is_active': True})
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
    {'n': 'Swift dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Swift dasturlash tili qachon e\'lon qilindi?', 'a': [{'t': '2014 yilda', 'c': True}, {'t': '2010 yilda', 'c': False}, {'t': '2016 yilda', 'c': False}, {'t': '2012 yilda', 'c': False}]},
        {'t': 'Swift tilini kim yaratgan?', 'a': [{'t': 'Apple kompaniyasi', 'c': True}, {'t': 'Google', 'c': False}, {'t': 'Microsoft', 'c': False}, {'t': 'Facebook', 'c': False}]},
        {'t': 'Swift ning asosiy maqsadi nima edi?', 'a': [{'t': 'Objective-C ni almashtirish', 'c': True}, {'t': 'Java ni almashtirish', 'c': False}, {'t': 'Python ni almashtirish', 'c': False}, {'t': 'C++ ni almashtirish', 'c': False}]},
        {'t': 'Swift fayl kengaytmasi?', 'a': [{'t': '.swift', 'c': True}, {'t': '.sw', 'c': False}, {'t': '.swf', 'c': False}, {'t': '.s', 'c': False}]},
        {'t': 'Swift qanday platformalarda ishlaydi?', 'a': [{'t': 'iOS, macOS, watchOS, tvOS', 'c': True}, {'t': 'Faqat iOS', 'c': False}, {'t': 'Faqat macOS', 'c': False}, {'t': 'Faqat Windows', 'c': False}]},
        {'t': 'Swift open source tilmi?', 'a': [{'t': 'Ha, 2015 yildan boshlab', 'c': True}, {'t': 'Yo\'q, yopiq manba', 'c': False}, {'t': 'Faqat qisman', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Swift Playgrounds nima?', 'a': [{'t': 'Swift kodini sinab ko\'rish muhiti', 'c': True}, {'t': 'O\'yin yaratish dasturi', 'c': False}, {'t': 'Video tahrirlash dasturi', 'c': False}, {'t': 'Grafik dizayn dasturi', 'c': False}]},
    ]},
    
    {'n': 'O\'zgaruvchilar va konstantalar', 't': 25, 'o': 2, 'q': [
        {'t': 'Swift da o\'zgaruvchi qanday e\'lon qilinadi?', 'a': [{'t': 'var nomi = qiymat', 'c': True}, {'t': 'let nomi = qiymat', 'c': False}, {'t': 'const nomi = qiymat', 'c': False}, {'t': 'variable nomi = qiymat', 'c': False}]},
        {'t': 'Konstanta qanday e\'lon qilinadi?', 'a': [{'t': 'let nomi = qiymat', 'c': True}, {'t': 'var nomi = qiymat', 'c': False}, {'t': 'const nomi = qiymat', 'c': False}, {'t': 'final nomi = qiymat', 'c': False}]},
        {'t': 'var va let orasidagi farq nima?', 'a': [{'t': 'var o\'zgaradi, let o\'zgarmaydi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'let o\'zgaradi, var o\'zgarmaydi', 'c': False}, {'t': 'Ikkalasi ham o\'zgaradi', 'c': False}]},
        {'t': 'Swift da tip ko\'rsatish majburiyatmi?', 'a': [{'t': 'Yo\'q, type inference mavjud', 'c': True}, {'t': 'Ha, har doim kerak', 'c': False}, {'t': 'Faqat konstantalarda', 'c': False}, {'t': 'Faqat o\'zgaruvchilarda', 'c': False}]},
        {'t': 'To\'g\'ri tip ko\'rsatish: var age: Int = 25', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat let bilan ishlaydi', 'c': False}]},
        {'t': 'Bir qatorda bir nechta o\'zgaruvchi e\'lon qilish mumkinmi?', 'a': [{'t': 'Ha, vergul bilan: var x = 1, y = 2', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat let bilan', 'c': False}, {'t': 'Faqat var bilan', 'c': False}]},
        {'t': 'O\'zgaruvchi nomida raqam bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, lekin boshida bo\'lmasligi kerak', 'c': True}, {'t': 'Yo\'q, umuman mumkin emas', 'c': False}, {'t': 'Faqat oxirida', 'c': False}, {'t': 'Faqat o\'rtasida', 'c': False}]},
        {'t': 'Underscore (_) bilan boshlangan o\'zgaruvchi nima uchun ishlatiladi?', 'a': [{'t': 'Ishlatilmaydigan qiymatlar uchun', 'c': True}, {'t': 'Maxfiy o\'zgaruvchilar uchun', 'c': False}, {'t': 'Global o\'zgaruvchilar uchun', 'c': False}, {'t': 'Vaqtinchalik o\'zgaruvchilar uchun', 'c': False}]},
    ]},

    {'n': 'Ma\'lumot turlari (Data Types)', 't': 25, 'o': 3, 'q': [
        {'t': 'Swift da butun son turi?', 'a': [{'t': 'Int', 'c': True}, {'t': 'Integer', 'c': False}, {'t': 'Number', 'c': False}, {'t': 'Num', 'c': False}]},
        {'t': 'O\'nlik son turi?', 'a': [{'t': 'Double yoki Float', 'c': True}, {'t': 'Decimal', 'c': False}, {'t': 'Real', 'c': False}, {'t': 'Float64', 'c': False}]},
        {'t': 'Matn turi?', 'a': [{'t': 'String', 'c': True}, {'t': 'Text', 'c': False}, {'t': 'Char', 'c': False}, {'t': 'Str', 'c': False}]},
        {'t': 'Mantiqiy qiymat turi?', 'a': [{'t': 'Bool', 'c': True}, {'t': 'Boolean', 'c': False}, {'t': 'Bit', 'c': False}, {'t': 'Logic', 'c': False}]},
        {'t': 'Bitta belgi turi?', 'a': [{'t': 'Character', 'c': True}, {'t': 'Char', 'c': False}, {'t': 'Letter', 'c': False}, {'t': 'Symbol', 'c': False}]},
        {'t': 'Double va Float orasidagi farq?', 'a': [{'t': 'Double aniqroq (64-bit), Float 32-bit', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Float aniqroq', 'c': False}, {'t': 'Double faqat musbat sonlar uchun', 'c': False}]},
        {'t': 'Type casting nima?', 'a': [{'t': 'Bir turni boshqasiga o\'zgartirish', 'c': True}, {'t': 'Tip tekshirish', 'c': False}, {'t': 'Tip e\'lon qilish', 'c': False}, {'t': 'Tip o\'chirish', 'c': False}]},
        {'t': 'Int dan String ga o\'tkazish: String(42)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat toString() ishlatiladi', 'c': False}]},
    ]},

    {'n': 'Operatorlar', 't': 25, 'o': 4, 'q': [
        {'t': 'Qo\'shish operatori?', 'a': [{'t': '+', 'c': True}, {'t': 'add', 'c': False}, {'t': 'plus', 'c': False}, {'t': '&', 'c': False}]},
        {'t': 'Tenglik tekshirish operatori?', 'a': [{'t': '==', 'c': True}, {'t': '=', 'c': False}, {'t': 'equals', 'c': False}, {'t': '===', 'c': False}]},
        {'t': 'Mantiqiy VA (AND) operatori?', 'a': [{'t': '&&', 'c': True}, {'t': 'AND', 'c': False}, {'t': '&', 'c': False}, {'t': 'and', 'c': False}]},
        {'t': 'Mantiqiy YOKI (OR) operatori?', 'a': [{'t': '||', 'c': True}, {'t': 'OR', 'c': False}, {'t': '|', 'c': False}, {'t': 'or', 'c': False}]},
        {'t': 'Mantiqiy EMAS (NOT) operatori?', 'a': [{'t': '!', 'c': True}, {'t': 'NOT', 'c': False}, {'t': 'not', 'c': False}, {'t': '~', 'c': False}]},
        {'t': 'Diapazon operatori: 1...5 nima beradi?', 'a': [{'t': '1 dan 5 gacha (5 ham kiradi)', 'c': True}, {'t': '1 dan 5 gacha (5 kirmaydi)', 'c': False}, {'t': 'Faqat 1 va 5', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Yarim ochiq diapazon: 1..<5 nima beradi?', 'a': [{'t': '1 dan 4 gacha (5 kirmaydi)', 'c': True}, {'t': '1 dan 5 gacha', 'c': False}, {'t': '2 dan 5 gacha', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Nil-coalescing operator: a ?? b nima qiladi?', 'a': [{'t': 'a nil bo\'lsa b qaytaradi', 'c': True}, {'t': 'a va b ni solishtiradi', 'c': False}, {'t': 'a ni b ga o\'zgartiradi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'String (Matnlar) bilan ishlash', 't': 30, 'o': 5, 'q': [
        {'t': 'String yaratish: let name = "Ali"', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat var bilan', 'c': False}, {'t': 'Qo\'shtirnoq kerak emas', 'c': False}]},
        {'t': 'String interpolation: "Salom \\(name)"', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat + ishlatiladi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'String uzunligini topish?', 'a': [{'t': '.count', 'c': True}, {'t': '.length', 'c': False}, {'t': '.size', 'c': False}, {'t': '.len', 'c': False}]},
        {'t': 'String bo\'shmi tekshirish?', 'a': [{'t': '.isEmpty', 'c': True}, {'t': '.empty', 'c': False}, {'t': '.isNull', 'c': False}, {'t': '.blank', 'c': False}]},
        {'t': 'String ni katta harflarga: .uppercased()', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': '.toUpperCase()', 'c': False}, {'t': '.upper()', 'c': False}]},
        {'t': 'String ni kichik harflarga?', 'a': [{'t': '.lowercased()', 'c': True}, {'t': '.toLowerCase()', 'c': False}, {'t': '.lower()', 'c': False}, {'t': '.small()', 'c': False}]},
        {'t': 'String qo\'shish: str1 + str2', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .append() ishlatiladi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Multi-line string qanday yoziladi?', 'a': [{'t': '"""...""" uch qo\'shtirnoq bilan', 'c': True}, {'t': 'Oddiy qo\'shtirnoq bilan', 'c': False}, {'t': '\\n bilan', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'String ichida qo\'shtirnoq: "U dedi: \\"Salom\\""', 'a': [{'t': 'To\'g\'ri, \\\\ bilan escape qilinadi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Bitta qo\'shtirnoq ishlatiladi', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
    ]},

    {'n': 'Shartli operatorlar (if, else)', 't': 25, 'o': 6, 'q': [
        {'t': 'if operatori sintaksisi?', 'a': [{'t': 'if shart { kod }', 'c': True}, {'t': 'if (shart) { kod }', 'c': False}, {'t': 'if shart then kod', 'c': False}, {'t': 'if: shart { kod }', 'c': False}]},
        {'t': 'if-else sintaksisi to\'g\'ri?', 'a': [{'t': 'if shart { } else { }', 'c': True}, {'t': 'if shart { } otherwise { }', 'c': False}, {'t': 'if shart then else', 'c': False}, {'t': 'if (shart) else', 'c': False}]},
        {'t': 'else if qanday yoziladi?', 'a': [{'t': 'else if shart { }', 'c': True}, {'t': 'elif shart { }', 'c': False}, {'t': 'elseif shart { }', 'c': False}, {'t': 'else-if shart { }', 'c': False}]},
        {'t': 'Ternary operator: a > b ? a : b', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Swift da yo\'q', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'if da qavs kerakmi: if (x > 5)', 'a': [{'t': 'Kerak emas, lekin ishlatish mumkin', 'c': True}, {'t': 'Har doim kerak', 'c': False}, {'t': 'Hech qachon ishlatilmaydi', 'c': False}, {'t': 'Faqat murakkab shartlarda', 'c': False}]},
        {'t': 'Bir qatorli if: if x > 0 { print("Musbat") }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Jingalak qavs kerak emas', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Switch operatori', 't': 30, 'o': 7, 'q': [
        {'t': 'switch operatori sintaksisi?', 'a': [{'t': 'switch qiymat { case 1: kod }', 'c': True}, {'t': 'switch (qiymat) case 1:', 'c': False}, {'t': 'switch qiymat case 1', 'c': False}, {'t': 'case qiymat: kod', 'c': False}]},
        {'t': 'default case majburiyatmi?', 'a': [{'t': 'Ha, barcha holatlar qoplanmasa', 'c': True}, {'t': 'Yo\'q, ixtiyoriy', 'c': False}, {'t': 'Har doim kerak', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'Swift da break kerakmi?', 'a': [{'t': 'Yo\'q, avtomatik to\'xtaydi', 'c': True}, {'t': 'Ha, har doim kerak', 'c': False}, {'t': 'Faqat oxirgi case da', 'c': False}, {'t': 'Faqat default da', 'c': False}]},
        {'t': 'Bir nechta qiymat: case 1, 2, 3:', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat case 1 | 2 | 3', 'c': False}, {'t': 'Har biri alohida case', 'c': False}]},
        {'t': 'Diapazon bilan: case 1...5:', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat if da ishlatiladi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'fallthrough nima qiladi?', 'a': [{'t': 'Keyingi case ga o\'tadi', 'c': True}, {'t': 'Switch dan chiqadi', 'c': False}, {'t': 'Xatolikni ko\'rsatadi', 'c': False}, {'t': 'Default ga o\'tadi', 'c': False}]},
        {'t': 'Tuple bilan switch ishlatish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat 2 elementli tuple', 'c': False}, {'t': 'Faqat String tuple', 'c': False}]},
        {'t': 'where kalit so\'zi switch da nima uchun?', 'a': [{'t': 'Qo\'shimcha shart qo\'yish uchun', 'c': True}, {'t': 'Case ni nomlash uchun', 'c': False}, {'t': 'Default ni almashtirish uchun', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Sikllar: for-in', 't': 25, 'o': 8, 'q': [
        {'t': 'for-in sikli sintaksisi?', 'a': [{'t': 'for item in collection { }', 'c': True}, {'t': 'for (item in collection)', 'c': False}, {'t': 'for item of collection', 'c': False}, {'t': 'foreach item in collection', 'c': False}]},
        {'t': 'Diapazon bilan: for i in 1...5', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat 1..<5', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'O\'zgaruvchi kerak bo\'lmasa: for _ in 1...5', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat for in 1...5', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Array ustidan aylanish: for name in names', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat forEach ishlatiladi', 'c': False}, {'t': 'Index kerak', 'c': False}]},
        {'t': 'Index bilan: for (index, value) in array.enumerated()', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat for i in 0..<array.count', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Dictionary ustidan: for (key, value) in dict', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat keys va values alohida', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'stride funksiyasi nima uchun?', 'a': [{'t': 'Qadam bilan aylanish uchun', 'c': True}, {'t': 'To\'xtatish uchun', 'c': False}, {'t': 'Teskari aylanish uchun', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Sikllar: while va repeat-while', 't': 25, 'o': 9, 'q': [
        {'t': 'while sikli sintaksisi?', 'a': [{'t': 'while shart { kod }', 'c': True}, {'t': 'while (shart) { kod }', 'c': False}, {'t': 'while shart do kod', 'c': False}, {'t': 'while: shart { kod }', 'c': False}]},
        {'t': 'repeat-while nima?', 'a': [{'t': 'do-while ga o\'xshash, avval bajaradi', 'c': True}, {'t': 'while ning boshqa nomi', 'c': False}, {'t': 'Ikki marta bajaradi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'repeat-while sintaksisi?', 'a': [{'t': 'repeat { kod } while shart', 'c': True}, {'t': 'repeat shart { kod }', 'c': False}, {'t': 'do { kod } while shart', 'c': False}, {'t': 'while shart repeat { kod }', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'Sikldan chiqadi', 'c': True}, {'t': 'Iteratsiyani o\'tkazib yuboradi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}, {'t': 'Siklni qayta boshlaydi', 'c': False}]},
        {'t': 'continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Sikldan chiqadi', 'c': False}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Cheksiz sikl: while true { }', 'a': [{'t': 'To\'g\'ri, lekin break kerak', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Avtomatik to\'xtaydi', 'c': False}]},
    ]},

    {'n': 'Array (Massivlar)', 't': 30, 'o': 10, 'q': [
        {'t': 'Array yaratish: var arr = [1, 2, 3]', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat Array(1, 2, 3)', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Bo\'sh array: var arr: [Int] = []', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat var arr = []', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Element qo\'shish?', 'a': [{'t': '.append(element)', 'c': True}, {'t': '.add(element)', 'c': False}, {'t': '.push(element)', 'c': False}, {'t': '.insert(element)', 'c': False}]},
        {'t': 'Elementga murojaat: arr[0]', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat arr.get(0)', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Array uzunligi?', 'a': [{'t': '.count', 'c': True}, {'t': '.length', 'c': False}, {'t': '.size', 'c': False}, {'t': '.len', 'c': False}]},
        {'t': 'Element o\'chirish: .remove(at: index)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .delete(index)', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Oxirgi elementni o\'chirish?', 'a': [{'t': '.removeLast()', 'c': True}, {'t': '.deleteLast()', 'c': False}, {'t': '.pop()', 'c': False}, {'t': '.remove()', 'c': False}]},
        {'t': 'Array bo\'shmi: .isEmpty', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .count == 0', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Ikki arrayni birlashtirish: arr1 + arr2', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .concat()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Array ichida element bormi: .contains(element)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .includes()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Dictionary (Lug\'atlar)', 't': 30, 'o': 11, 'q': [
        {'t': 'Dictionary yaratish: var dict = ["key": "value"]', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat {"key": "value"}', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Bo\'sh dictionary: var dict: [String: Int] = [:]', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat var dict = [:]', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Qiymatga murojaat: dict["key"]', 'a': [{'t': 'To\'g\'ri, optional qaytaradi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat dict.get("key")', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Yangi element qo\'shish: dict["newKey"] = value', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .add()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Element o\'chirish: dict["key"] = nil', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .remove()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Dictionary uzunligi?', 'a': [{'t': '.count', 'c': True}, {'t': '.length', 'c': False}, {'t': '.size', 'c': False}, {'t': '.keys.count', 'c': False}]},
        {'t': 'Barcha kalitlar: dict.keys', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .getKeys()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Barcha qiymatlar: dict.values', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .getValues()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Set (To\'plamlar)', 't': 25, 'o': 12, 'q': [
        {'t': 'Set nima?', 'a': [{'t': 'Takrorlanmaydigan elementlar to\'plami', 'c': True}, {'t': 'Tartiblangan ro\'yxat', 'c': False}, {'t': 'Kalit-qiymat juftligi', 'c': False}, {'t': 'Array ning boshqa nomi', 'c': False}]},
        {'t': 'Set yaratish: var set: Set<Int> = [1, 2, 3]', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat Set([1, 2, 3])', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Element qo\'shish: .insert(element)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .add()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Element o\'chirish: .remove(element)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat .delete()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Set birlashtirish: set1.union(set2)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat set1 + set2', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Kesishma: set1.intersection(set2)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat set1 & set2', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Farq: set1.subtracting(set2)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat set1 - set2', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Tuple (Kortejlar)', 't': 25, 'o': 13, 'q': [
        {'t': 'Tuple nima?', 'a': [{'t': 'Bir nechta qiymatni birlashtiradigan struktura', 'c': True}, {'t': 'Array ning boshqa nomi', 'c': False}, {'t': 'Dictionary ning turi', 'c': False}, {'t': 'Set ning varianti', 'c': False}]},
        {'t': 'Tuple yaratish: let person = ("Ali", 25)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat Tuple("Ali", 25)', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Tuple elementiga murojaat: person.0', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat person[0]', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Nomlangan tuple: let person = (name: "Ali", age: 25)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat dictionary ishlatiladi', 'c': False}]},
        {'t': 'Nomlangan elementga murojaat: person.name', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat person["name"]', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Tuple decomposition: let (name, age) = person', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat array uchun', 'c': False}]},
        {'t': 'Tuple o\'zgartirilishi mumkinmi?', 'a': [{'t': 'Yo\'q, immutable', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Faqat var bilan', 'c': False}, {'t': 'Faqat let bilan', 'c': False}]},
    ]},

    {'n': 'Funksiyalar asoslari', 't': 30, 'o': 14, 'q': [
        {'t': 'Funksiya e\'lon qilish: func name() { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat function name()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Parametrli funksiya: func greet(name: String)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat func greet(String name)', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Qaytaruvchi funksiya: func sum() -> Int', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat func Int sum()', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'return kalit so\'zi nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi', 'c': True}, {'t': 'Funksiyani to\'xtatadi', 'c': False}, {'t': 'Parametr qabul qiladi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Bir qatorli funksiya return kerakmi: func double(_ x: Int) -> Int { x * 2 }', 'a': [{'t': 'Yo\'q, avtomatik qaytaradi', 'c': True}, {'t': 'Ha, har doim kerak', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat let bilan', 'c': False}]},
        {'t': 'Bir nechta qiymat qaytarish: func minMax() -> (Int, Int)', 'a': [{'t': 'To\'g\'ri, tuple qaytaradi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat array qaytaradi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Default parametr: func greet(name: String = "Mehmon")', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat var parametrlarda', 'c': False}]},
        {'t': 'Funksiya chaqirish: greet(name: "Ali")', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat greet("Ali")', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Funksiya parametrlari', 't': 30, 'o': 15, 'q': [
        {'t': 'Argument label: func greet(to name: String)', 'a': [{'t': 'To\'g\'ri, chaqirishda: greet(to: "Ali")', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat internal name', 'c': False}]},
        {'t': 'Argument label ni o\'chirish: func sum(_ a: Int, _ b: Int)', 'a': [{'t': 'To\'g\'ri, chaqirish: sum(5, 3)', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat bitta parametrda', 'c': False}]},
        {'t': 'Variadic parametr: func sum(_ numbers: Int...)', 'a': [{'t': 'To\'g\'ri, istalgancha parametr', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat array', 'c': False}]},
        {'t': 'inout parametr nima?', 'a': [{'t': 'Parametrni o\'zgartirish mumkin', 'c': True}, {'t': 'Kiruvchi parametr', 'c': False}, {'t': 'Chiquvchi parametr', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'inout ishlatish: func swap(_ a: inout Int, _ b: inout Int)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat var parametrlarda', 'c': False}]},
        {'t': 'inout chaqirish: swap(&x, &y)', 'a': [{'t': 'To\'g\'ri, & belgisi kerak', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat swap(x, y)', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Closures (Yopiq funksiyalar)', 't': 30, 'o': 16, 'q': [
        {'t': 'Closure nima?', 'a': [{'t': 'Nomsiz funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Class metodi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Closure sintaksisi: { (parametrlar) -> Tur in kod }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat func ishlatiladi', 'c': False}]},
        {'t': 'Oddiy closure: let greet = { print("Salom") }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat func bilan', 'c': False}]},
        {'t': 'Parametrli closure: { (name: String) in print(name) }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'in kerak emas', 'c': False}]},
        {'t': 'Shorthand argument: $0, $1, $2', 'a': [{'t': 'To\'g\'ri, parametr nomlari o\'rniga', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat array uchun', 'c': False}]},
        {'t': 'Trailing closure: array.map { $0 * 2 }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat qavs ichida', 'c': False}]},
        {'t': 'Capturing values: closure tashqaridagi o\'zgaruvchini ishlatishi', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Mumkin emas', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Escaping closure: @escaping nima?', 'a': [{'t': 'Funksiya tugagandan keyin bajariladi', 'c': True}, {'t': 'Darhol bajariladi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat async uchun', 'c': False}]},
    ]},

    {'n': 'Optionals (Ixtiyoriy qiymatlar)', 't': 30, 'o': 17, 'q': [
        {'t': 'Optional nima?', 'a': [{'t': 'Qiymat yoki nil bo\'lishi mumkin', 'c': True}, {'t': 'Har doim qiymat bor', 'c': False}, {'t': 'Faqat nil', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Optional e\'lon qilish: var name: String?', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Faqat String!', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Optional unwrapping: if let name = optionalName', 'a': [{'t': 'To\'g\'ri, xavfsiz usul', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat guard let', 'c': False}]},
        {'t': 'Force unwrapping: name!', 'a': [{'t': 'To\'g\'ri, lekin xavfli', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Har doim xavfsiz', 'c': False}]},
        {'t': 'Nil-coalescing: name ?? "Default"', 'a': [{'t': 'To\'g\'ri, nil bo\'lsa default beradi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat if let ishlatiladi', 'c': False}]},
        {'t': 'Optional chaining: person?.address?.street', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat bitta ?', 'c': False}]},
        {'t': 'Implicitly unwrapped optional: var name: String!', 'a': [{'t': 'To\'g\'ri, avtomatik ochiladi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Oddiy optional bilan bir xil', 'c': False}]},
        {'t': 'guard let nima uchun ishlatiladi?', 'a': [{'t': 'Early exit uchun', 'c': True}, {'t': 'Loop uchun', 'c': False}, {'t': 'Switch uchun', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Enumerations (Sanab o\'tish)', 't': 30, 'o': 18, 'q': [
        {'t': 'Enum nima?', 'a': [{'t': 'Bog\'liq qiymatlar guruhi', 'c': True}, {'t': 'Array turi', 'c': False}, {'t': 'Dictionary turi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Enum e\'lon qilish: enum Direction { case north, south }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat alohida case', 'c': False}]},
        {'t': 'Enum ishlatish: let dir = Direction.north', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat Direction(north)', 'c': False}]},
        {'t': 'Raw values: enum Planet: Int { case mercury = 1 }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat String', 'c': False}]},
        {'t': 'Associated values: enum Barcode { case upc(Int, Int) }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat raw values', 'c': False}]},
        {'t': 'Enum da metod bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat computed property', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Switch bilan enum: switch direction { case .north: }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat if ishlatiladi', 'c': False}]},
    ]},

    {'n': 'Structures (Strukturalar)', 't': 30, 'o': 19, 'q': [
        {'t': 'Struct nima?', 'a': [{'t': 'Value type ma\'lumot strukturasi', 'c': True}, {'t': 'Reference type', 'c': False}, {'t': 'Class bilan bir xil', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Struct e\'lon qilish: struct Person { var name: String }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class ishlatiladi', 'c': False}]},
        {'t': 'Struct instance yaratish: let person = Person(name: "Ali")', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'new kerak', 'c': False}]},
        {'t': 'Memberwise initializer avtomatik yaratiladi?', 'a': [{'t': 'Ha, struct uchun', 'c': True}, {'t': 'Yo\'q, qo\'lda yoziladi', 'c': False}, {'t': 'Faqat class uchun', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Struct metodi: func greet() { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class da', 'c': False}]},
        {'t': 'Mutating metod nima?', 'a': [{'t': 'Property ni o\'zgartiruvchi metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Static metod', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'mutating func changeName() { self.name = "Yangi" }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'mutating kerak emas', 'c': False}]},
        {'t': 'Computed property: var fullName: String { return name }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat stored property', 'c': False}]},
    ]},

    {'n': 'Classes (Klasslar)', 't': 30, 'o': 20, 'q': [
        {'t': 'Class nima?', 'a': [{'t': 'Reference type ma\'lumot strukturasi', 'c': True}, {'t': 'Value type', 'c': False}, {'t': 'Struct bilan bir xil', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Class e\'lon qilish: class Person { var name: String }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat struct', 'c': False}]},
        {'t': 'Class da initializer kerakmi?', 'a': [{'t': 'Ha, property larga qiymat berish uchun', 'c': True}, {'t': 'Yo\'q, avtomatik', 'c': False}, {'t': 'Faqat struct da', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Initializer: init(name: String) { self.name = name }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat constructor', 'c': False}]},
        {'t': 'Deinitializer: deinit { }', 'a': [{'t': 'To\'g\'ri, xotira tozalanishida', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat struct da', 'c': False}]},
        {'t': 'Inheritance: class Student: Person { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat struct da', 'c': False}]},
        {'t': 'override kalit so\'zi nima uchun?', 'a': [{'t': 'Parent metodni qayta yozish', 'c': True}, {'t': 'Yangi metod yaratish', 'c': False}, {'t': 'Metodni o\'chirish', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'final class nima?', 'a': [{'t': 'Meros olinmaydigan class', 'c': True}, {'t': 'Oxirgi class', 'c': False}, {'t': 'Abstract class', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Class va Struct orasidagi asosiy farq?', 'a': [{'t': 'Class reference, Struct value type', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Struct murakkab', 'c': False}, {'t': 'Class oddiy', 'c': False}]},
    ]},

    {'n': 'Properties (Xususiyatlar)', 't': 30, 'o': 21, 'q': [
        {'t': 'Stored property nima?', 'a': [{'t': 'Qiymat saqlaydigan property', 'c': True}, {'t': 'Hisoblangan property', 'c': False}, {'t': 'Static property', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Computed property nima?', 'a': [{'t': 'Hisoblangan qiymat qaytaradi', 'c': True}, {'t': 'Qiymat saqlaydi', 'c': False}, {'t': 'Konstanta', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Computed property: var area: Double { return width * height }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat stored', 'c': False}]},
        {'t': 'Property observer: didSet { }', 'a': [{'t': 'To\'g\'ri, qiymat o\'zgarganda', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat willSet', 'c': False}]},
        {'t': 'willSet nima qiladi?', 'a': [{'t': 'Qiymat o\'zgarishidan oldin', 'c': True}, {'t': 'Qiymat o\'zgargandan keyin', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'didSet bilan bir xil', 'c': False}]},
        {'t': 'Lazy property: lazy var data = loadData()', 'a': [{'t': 'To\'g\'ri, birinchi ishlatilganda yuklanadi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Darhol yuklanadi', 'c': False}]},
        {'t': 'Static property: static var count = 0', 'a': [{'t': 'To\'g\'ri, type property', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat instance property', 'c': False}]},
        {'t': 'class var nima?', 'a': [{'t': 'Override qilinishi mumkin bo\'lgan type property', 'c': True}, {'t': 'Oddiy property', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'static bilan bir xil', 'c': False}]},
    ]},

    {'n': 'Methods (Metodlar)', 't': 25, 'o': 22, 'q': [
        {'t': 'Instance method nima?', 'a': [{'t': 'Instance ga tegishli metod', 'c': True}, {'t': 'Type metod', 'c': False}, {'t': 'Static metod', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Type method: static func create() { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat instance', 'c': False}]},
        {'t': 'class func nima?', 'a': [{'t': 'Override qilinishi mumkin type method', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'static bilan bir xil', 'c': False}]},
        {'t': 'self kalit so\'zi nima?', 'a': [{'t': 'Joriy instance ga murojaat', 'c': True}, {'t': 'Parent class', 'c': False}, {'t': 'Type', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Struct da mutating metod kerakmi?', 'a': [{'t': 'Ha, property o\'zgartirish uchun', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Faqat class da', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Class da mutating kerakmi?', 'a': [{'t': 'Yo\'q, kerak emas', 'c': True}, {'t': 'Ha, kerak', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Protocols (Protokollar)', 't': 30, 'o': 23, 'q': [
        {'t': 'Protocol nima?', 'a': [{'t': 'Metodlar va property lar shabloni', 'c': True}, {'t': 'Class turi', 'c': False}, {'t': 'Struct turi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Protocol e\'lon qilish: protocol Drivable { func drive() }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat interface', 'c': False}]},
        {'t': 'Protocol qabul qilish: class Car: Drivable { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat implements', 'c': False}]},
        {'t': 'Protocol property: var name: String { get }', 'a': [{'t': 'To\'g\'ri, faqat o\'qish', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat set', 'c': False}]},
        {'t': 'O\'qish va yozish: var name: String { get set }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat get', 'c': False}]},
        {'t': 'Bir nechta protocol: class Car: Drivable, Washable', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat bitta', 'c': False}]},
        {'t': 'Protocol extension nima?', 'a': [{'t': 'Protocol ga default implementatsiya', 'c': True}, {'t': 'Protocol ni kengaytirish', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Yangi protocol', 'c': False}]},
        {'t': 'Protocol inheritance: protocol A: B { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
    ]},

    {'n': 'Extensions (Kengaytmalar)', 't': 25, 'o': 24, 'q': [
        {'t': 'Extension nima?', 'a': [{'t': 'Mavjud turga funksionallik qo\'shish', 'c': True}, {'t': 'Yangi tur yaratish', 'c': False}, {'t': 'Class meros olish', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Extension e\'lon qilish: extension String { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class uchun', 'c': False}]},
        {'t': 'Extension da metod qo\'shish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat property', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Extension da stored property qo\'shish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat computed', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Har doim mumkin', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Extension da initializer qo\'shish mumkinmi?', 'a': [{'t': 'Ha, convenience init', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat designated init', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Protocol conformance: extension Int: MyProtocol { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'Extension barcha turlarga qo\'llanilishi mumkinmi?', 'a': [{'t': 'Ha, class, struct, enum, protocol', 'c': True}, {'t': 'Yo\'q, faqat class', 'c': False}, {'t': 'Faqat struct', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Generics (Umumiy turlar)', 't': 30, 'o': 25, 'q': [
        {'t': 'Generics nima?', 'a': [{'t': 'Har qanday tur bilan ishlaydigan kod', 'c': True}, {'t': 'Faqat Int uchun', 'c': False}, {'t': 'Faqat String uchun', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Generic funksiya: func swap<T>(_ a: inout T, _ b: inout T)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class uchun', 'c': False}]},
        {'t': 'Generic type: struct Stack<Element> { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat funksiya uchun', 'c': False}]},
        {'t': 'Type constraint: func find<T: Equatable>(_ item: T)', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Constraint kerak emas', 'c': False}]},
        {'t': 'Associated type: associatedtype Item', 'a': [{'t': 'To\'g\'ri, protocol da', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class da', 'c': False}]},
        {'t': 'Where clause: func allEqual<T: Equatable>() where T == Int', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'where kerak emas', 'c': False}]},
        {'t': 'Generic extension: extension Array where Element: Numeric', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
    ]},

    {'n': 'Error Handling (Xatolarni boshqarish)', 't': 30, 'o': 26, 'q': [
        {'t': 'Error protocol nima?', 'a': [{'t': 'Xatolarni ifodalash uchun', 'c': True}, {'t': 'Oddiy protocol', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat class uchun', 'c': False}]},
        {'t': 'Error enum: enum FileError: Error { case notFound }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat struct', 'c': False}]},
        {'t': 'Throwing funksiya: func load() throws -> String', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'throw kerak', 'c': False}]},
        {'t': 'Xato tashlash: throw FileError.notFound', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat return', 'c': False}]},
        {'t': 'do-catch: do { try load() } catch { }', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'try kerak emas', 'c': False}]},
        {'t': 'try? nima qiladi?', 'a': [{'t': 'Optional qaytaradi, xato bo\'lsa nil', 'c': True}, {'t': 'Xatoni tashlaydi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'try! nima qiladi?', 'a': [{'t': 'Xato bo\'lsa crash qiladi', 'c': True}, {'t': 'Xatoni ignore qiladi', 'c': False}, {'t': 'Optional qaytaradi', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'defer nima uchun?', 'a': [{'t': 'Kod oxirida bajariladi', 'c': True}, {'t': 'Darhol bajariladi', 'c': False}, {'t': 'Xato bo\'lganda', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Type Casting', 't': 25, 'o': 27, 'q': [
        {'t': 'Type checking: item is String', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat ==', 'c': False}]},
        {'t': 'Downcasting: item as? String', 'a': [{'t': 'To\'g\'ri, optional qaytaradi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat as!', 'c': False}]},
        {'t': 'Forced downcasting: item as! String', 'a': [{'t': 'To\'g\'ri, lekin xavfli', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Har doim xavfsiz', 'c': False}]},
        {'t': 'Upcasting: dog as Animal', 'a': [{'t': 'To\'g\'ri, har doim muvaffaqiyatli', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Xavfli', 'c': False}]},
        {'t': 'Any nima?', 'a': [{'t': 'Har qanday tur', 'c': True}, {'t': 'Faqat class', 'c': False}, {'t': 'Faqat struct', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'AnyObject nima?', 'a': [{'t': 'Har qanday class instance', 'c': True}, {'t': 'Har qanday tur', 'c': False}, {'t': 'Faqat struct', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Access Control', 't': 25, 'o': 28, 'q': [
        {'t': 'open nima?', 'a': [{'t': 'Eng ochiq, boshqa modulda meros olish mumkin', 'c': True}, {'t': 'Faqat ichki', 'c': False}, {'t': 'Private', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'public nima?', 'a': [{'t': 'Boshqa modulda ko\'rinadi, meros yo\'q', 'c': True}, {'t': 'Faqat ichki', 'c': False}, {'t': 'Private', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'internal nima?', 'a': [{'t': 'Faqat o\'z modulida (default)', 'c': True}, {'t': 'Hamma joyda', 'c': False}, {'t': 'Private', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'fileprivate nima?', 'a': [{'t': 'Faqat o\'sha faylda', 'c': True}, {'t': 'Hamma joyda', 'c': False}, {'t': 'Faqat class ichida', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'private nima?', 'a': [{'t': 'Faqat o\'sha scope da', 'c': True}, {'t': 'Hamma joyda', 'c': False}, {'t': 'Faqat faylda', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Default access level?', 'a': [{'t': 'internal', 'c': True}, {'t': 'public', 'c': False}, {'t': 'private', 'c': False}, {'t': 'open', 'c': False}]},
    ]},

    {'n': 'Memory Management (ARC)', 't': 30, 'o': 29, 'q': [
        {'t': 'ARC nima?', 'a': [{'t': 'Automatic Reference Counting', 'c': True}, {'t': 'Array Reference Count', 'c': False}, {'t': 'Auto Release Code', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'Strong reference nima?', 'a': [{'t': 'Oddiy reference, count oshiradi', 'c': True}, {'t': 'Zaif reference', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Count oshirmaydi', 'c': False}]},
        {'t': 'weak reference: weak var delegate: Delegate?', 'a': [{'t': 'To\'g\'ri, count oshirmaydi', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Strong reference', 'c': False}]},
        {'t': 'weak har doim optional bo\'lishi kerakmi?', 'a': [{'t': 'Ha, nil bo\'lishi mumkin', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
        {'t': 'unowned reference nima?', 'a': [{'t': 'weak ga o\'xshash, lekin optional emas', 'c': True}, {'t': 'Strong reference', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'weak bilan bir xil', 'c': False}]},
        {'t': 'Strong reference cycle nima?', 'a': [{'t': 'Ikki obyekt bir-biriga strong reference', 'c': True}, {'t': 'Oddiy reference', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Muammo emas', 'c': False}]},
        {'t': 'Closure da [weak self] nima uchun?', 'a': [{'t': 'Reference cycle oldini olish', 'c': True}, {'t': 'Tezroq ishlash', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Kerak emas', 'c': False}]},
        {'t': '[unowned self] qachon ishlatiladi?', 'a': [{'t': 'self hech qachon nil bo\'lmasa', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},

    {'n': 'Advanced Operators', 't': 25, 'o': 30, 'q': [
        {'t': 'Bitwise NOT: ~a', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat !a', 'c': False}]},
        {'t': 'Bitwise AND: a & b', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat a && b', 'c': False}]},
        {'t': 'Bitwise OR: a | b', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat a || b', 'c': False}]},
        {'t': 'Bitwise XOR: a ^ b', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'Left shift: a << 2', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat >>', 'c': False}]},
        {'t': 'Right shift: a >> 2', 'a': [{'t': 'To\'g\'ri', 'c': True}, {'t': 'Noto\'g\'ri', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Faqat <<', 'c': False}]},
        {'t': 'Overflow operators: &+ nima?', 'a': [{'t': 'Overflow bo\'lsa ham davom etadi', 'c': True}, {'t': 'Oddiy qo\'shish', 'c': False}, {'t': 'Sintaksis xato', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Custom operator yaratish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat Apple', 'c': False}, {'t': 'Sintaksis xato', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_swift()
    add_topics(subj, T)
    print(f"\n✅ Swift: {len(T)} ta mavzu qo\'shildi!")
