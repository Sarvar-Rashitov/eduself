"""
JAVASCRIPT DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_javascript():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='JavaScript', defaults={'category': cat, 'description': 'JavaScript dasturlash tili - web dasturlash uchun', 'icon': 'bi-filetype-js', 'order': 6, 'is_active': True})
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
    {'n': 'JavaScript dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'JavaScript dasturlash tili qachon yaratilgan?', 'a': [{'t': '1995 yilda', 'c': True}, {'t': '2000 yilda', 'c': False}, {'t': '1990 yilda', 'c': False}, {'t': '2010 yilda', 'c': False}]},
        {'t': 'JavaScript tilini kim yaratgan?', 'a': [{'t': 'Brendan Eich', 'c': True}, {'t': 'Bill Gates', 'c': False}, {'t': 'Steve Jobs', 'c': False}, {'t': 'Mark Zuckerberg', 'c': False}]},
        {'t': 'JavaScript asosan qayerda ishlatiladi?', 'a': [{'t': 'Web sahifalarda (brauzerda)', 'c': True}, {'t': 'Faqat serverlarda', 'c': False}, {'t': 'Faqat mobil ilovalarda', 'c': False}, {'t': 'Faqat o\'yinlarda', 'c': False}]},
        {'t': 'JavaScript fayl kengaytmasi?', 'a': [{'t': '.js', 'c': True}, {'t': '.java', 'c': False}, {'t': '.jsx', 'c': False}, {'t': '.json', 'c': False}]},
        {'t': 'JavaScript va Java bir xilmi?', 'a': [{'t': 'Yo\'q, butunlay boshqa tillar', 'c': True}, {'t': 'Ha, bir xil', 'c': False}, {'t': 'JavaScript Java ning qisqartmasi', 'c': False}, {'t': 'Java JavaScript ning yangi versiyasi', 'c': False}]},
        {'t': 'JavaScript qanday til?', 'a': [{'t': 'Interpretatsiya qilinadigan, dinamik til', 'c': True}, {'t': 'Kompilyatsiya qilinadigan til', 'c': False}, {'t': 'Faqat statik til', 'c': False}, {'t': 'Mashina tili', 'c': False}]},
    ]},
    {'n': 'Birinchi JavaScript dasturi', 't': 20, 'o': 2, 'q': [
        {'t': 'console.log() nima qiladi?', 'a': [{'t': 'Konsolga chiqaradi', 'c': True}, {'t': 'Ekranga alert ko\'rsatadi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Kiritish qiladi', 'c': False}]},
        {'t': 'alert() nima qiladi?', 'a': [{'t': 'Ogohlantirish oynasini ko\'rsatadi', 'c': True}, {'t': 'Konsolga chiqaradi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Sahifani yangilaydi', 'c': False}]},
        {'t': 'JavaScript da izoh qanday yoziladi?', 'a': [{'t': '// yoki /* */', 'c': True}, {'t': 'Faqat //', 'c': False}, {'t': '# belgisi bilan', 'c': False}, {'t': '\'\'\' bilan', 'c': False}]},
        {'t': 'JavaScript kodini HTML ga qanday qo\'shiladi?', 'a': [{'t': '<script> tegi ichida', 'c': True}, {'t': '<style> tegi ichida', 'c': False}, {'t': '<link> tegi ichida', 'c': False}, {'t': '<div> tegi ichida', 'c': False}]},
        {'t': 'Tashqi JavaScript faylini ulash?', 'a': [{'t': '<script src="file.js"></script>', 'c': True}, {'t': '<link href="file.js">', 'c': False}, {'t': '<import src="file.js">', 'c': False}, {'t': '<include file="file.js">', 'c': False}]},
        {'t': 'JavaScript qatorning oxirida ; kerakmi?', 'a': [{'t': 'Ixtiyoriy, lekin tavsiya etiladi', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar - var, let, const', 't': 25, 'o': 3, 'q': [
        {'t': 'JavaScript da o\'zgaruvchi e\'lon qilish usullari?', 'a': [{'t': 'var, let, const', 'c': True}, {'t': 'Faqat var', 'c': False}, {'t': 'int, string, bool', 'c': False}, {'t': 'define, set, create', 'c': False}]},
        {'t': 'let va var farqi?', 'a': [{'t': 'let block scope, var function scope', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'var yangi, let eski', 'c': False}, {'t': 'let tezroq', 'c': False}]},
        {'t': 'const nima?', 'a': [{'t': 'O\'zgarmas qiymat (constant)', 'c': True}, {'t': 'O\'zgaruvchan qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'const x = 5; x = 10; to\'g\'rimi?', 'a': [{'t': 'Yo\'q, xato (const o\'zgarmas)', 'c': True}, {'t': 'Ha, to\'g\'ri', 'c': False}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'let x; x = 5; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Faqat var bilan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Zamonaviy JavaScript da qaysi tavsiya etiladi?', 'a': [{'t': 'let va const (var emas)', 'c': True}, {'t': 'Faqat var', 'c': False}, {'t': 'Hech qaysi', 'c': False}, {'t': 'Hammasi bir xil', 'c': False}]},
        {'t': 'O\'zgaruvchi nomida $ va _ ishlatish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat $', 'c': False}, {'t': 'Faqat _', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari - Primitiv turlar', 't': 25, 'o': 4, 'q': [
        {'t': 'JavaScript da nechta primitiv tur bor?', 'a': [{'t': '7 ta (string, number, boolean, null, undefined, symbol, bigint)', 'c': True}, {'t': '5 ta', 'c': False}, {'t': '3 ta', 'c': False}, {'t': '10 ta', 'c': False}]},
        {'t': 'typeof "Hello" natijasi?', 'a': [{'t': 'string', 'c': True}, {'t': 'text', 'c': False}, {'t': 'String', 'c': False}, {'t': 'char', 'c': False}]},
        {'t': 'typeof 42 natijasi?', 'a': [{'t': 'number', 'c': True}, {'t': 'int', 'c': False}, {'t': 'integer', 'c': False}, {'t': 'Number', 'c': False}]},
        {'t': 'typeof true natijasi?', 'a': [{'t': 'boolean', 'c': True}, {'t': 'bool', 'c': False}, {'t': 'Boolean', 'c': False}, {'t': 'true', 'c': False}]},
        {'t': 'typeof undefined natijasi?', 'a': [{'t': 'undefined', 'c': True}, {'t': 'null', 'c': False}, {'t': 'object', 'c': False}, {'t': 'Undefined', 'c': False}]},
        {'t': 'typeof null natijasi?', 'a': [{'t': 'object (JavaScript xatosi)', 'c': True}, {'t': 'null', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Null', 'c': False}]},
        {'t': 'JavaScript da butun va o\'nli sonlar farqi bormi?', 'a': [{'t': 'Yo\'q, hammasi number', 'c': True}, {'t': 'Ha, int va float', 'c': False}, {'t': 'Ha, integer va double', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Stringlar bilan ishlash', 't': 25, 'o': 5, 'q': [
        {'t': 'String yaratish usullari?', 'a': [{'t': '"text", \'text\', `text`', 'c': True}, {'t': 'Faqat "text"', 'c': False}, {'t': 'Faqat \'text\'', 'c': False}, {'t': 'String("text")', 'c': False}]},
        {'t': 'Template literal nima?', 'a': [{'t': 'Backtick bilan: `text ${variable}`', 'c': True}, {'t': 'Qo\'shtirnoq bilan', 'c': False}, {'t': 'Bitta tirnoq bilan', 'c': False}, {'t': 'Maxsus funksiya', 'c': False}]},
        {'t': '`Hello ${name}` nima qiladi?', 'a': [{'t': 'O\'zgaruvchini stringga qo\'shadi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Faqat "Hello" ni ko\'rsatadi', 'c': False}, {'t': 'name ni o\'chiradi', 'c': False}]},
        {'t': '"Hello" + " World" natijasi?', 'a': [{'t': 'Hello World', 'c': True}, {'t': 'HelloWorld', 'c': False}, {'t': 'Hello+World', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'str.length nima?', 'a': [{'t': 'String uzunligi', 'c': True}, {'t': 'String turi', 'c': False}, {'t': 'String qiymati', 'c': False}, {'t': 'Metod', 'c': False}]},
        {'t': 'str.toUpperCase() nima qiladi?', 'a': [{'t': 'Katta harflarga o\'tkazadi', 'c': True}, {'t': 'Kichik harflarga o\'tkazadi', 'c': False}, {'t': 'Birinchi harfni katta qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Operatorlar - Arifmetik', 't': 25, 'o': 6, 'q': [
        {'t': '10 + 5 natijasi?', 'a': [{'t': '15', 'c': True}, {'t': '105', 'c': False}, {'t': '5', 'c': False}, {'t': '50', 'c': False}]},
        {'t': '10 - 5 natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '15', 'c': False}, {'t': '50', 'c': False}, {'t': '2', 'c': False}]},
        {'t': '10 * 5 natijasi?', 'a': [{'t': '50', 'c': True}, {'t': '15', 'c': False}, {'t': '5', 'c': False}, {'t': '2', 'c': False}]},
        {'t': '10 / 5 natijasi?', 'a': [{'t': '2', 'c': True}, {'t': '5', 'c': False}, {'t': '50', 'c': False}, {'t': '0', 'c': False}]},
        {'t': '10 % 3 natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '2 ** 3 natijasi?', 'a': [{'t': '8 (2 ning 3-darajasi)', 'c': True}, {'t': '6', 'c': False}, {'t': '5', 'c': False}, {'t': '23', 'c': False}]},
        {'t': '++ operatori nima qiladi?', 'a': [{'t': '1 ga oshiradi', 'c': True}, {'t': '1 ga kamaytiradi', 'c': False}, {'t': '2 ga ko\'paytiradi', 'c': False}, {'t': 'Qo\'shadi', 'c': False}]},
    ]},
    {'n': 'Taqqoslash va mantiqiy operatorlar', 't': 25, 'o': 7, 'q': [
        {'t': '5 == "5" natijasi?', 'a': [{'t': 'true (qiymat teng)', 'c': True}, {'t': 'false', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'undefined', 'c': False}]},
        {'t': '5 === "5" natijasi?', 'a': [{'t': 'false (tur ham tekshiriladi)', 'c': True}, {'t': 'true', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'undefined', 'c': False}]},
        {'t': '== va === farqi?', 'a': [{'t': '=== tur ham tekshiradi (strict)', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '== tezroq', 'c': False}, {'t': '=== eski', 'c': False}]},
        {'t': '10 > 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'true && false natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'true || false natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '!true natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'if operatori', 't': 25, 'o': 8, 'q': [
        {'t': 'if operatori nima uchun?', 'a': [{'t': 'Shartli bajarish', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'if (x > 5) nima tekshiradi?', 'a': [{'t': 'x 5 dan kattami', 'c': True}, {'t': 'x 5 ga tengmi', 'c': False}, {'t': 'x 5 dan kichikmi', 'c': False}, {'t': 'x ga 5 ni beradi', 'c': False}]},
        {'t': 'if blokida kod qanday yoziladi?', 'a': [{'t': 'Jingalak qavslar ichida {}', 'c': True}, {'t': 'Oddiy qavslar ichida ()', 'c': False}, {'t': 'Kvadrat qavslar ichida []', 'c': False}, {'t': 'Qo\'shtirnoqda ""', 'c': False}]},
        {'t': 'Bir qatorli if da {} kerakmi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'if (x) nima tekshiradi?', 'a': [{'t': 'x truthy qiymatmi', 'c': True}, {'t': 'x true ga tengmi', 'c': False}, {'t': 'x mavjudmi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'if-else va ternary operator', 't': 25, 'o': 9, 'q': [
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'else if nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Ternary operator: x > 5 ? "Katta" : "Kichik"', 'a': [{'t': 'x>5 bo\'lsa "Katta", aks holda "Kichik"', 'c': True}, {'t': 'x va 5 ni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Stringlarni qo\'shadi', 'c': False}]},
        {'t': 'Ternary operator qisqartmasi?', 'a': [{'t': 'if-else ning qisqa yozuvi', 'c': True}, {'t': 'switch ning qisqa yozuvi', 'c': False}, {'t': 'for ning qisqa yozuvi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir necha else if ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'switch-case operatori', 't': 25, 'o': 10, 'q': [
        {'t': 'switch-case nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'case nima?', 'a': [{'t': 'Bir variant', 'c': True}, {'t': 'Shart', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'switch dan chiqadi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'switch da break qo\'ymasak?', 'a': [{'t': 'Keyingi case ham bajariladi (fall-through)', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'To\'xtaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'switch qanday turlar bilan ishlaydi?', 'a': [{'t': 'Barcha turlar (string, number, ...)', 'c': True}, {'t': 'Faqat number', 'c': False}, {'t': 'Faqat string', 'c': False}, {'t': 'Faqat boolean', 'c': False}]},
    ]},
    {'n': 'for sikli', 't': 25, 'o': 11, 'q': [
        {'t': 'for sikli nima uchun?', 'a': [{'t': 'Ma\'lum marta takrorlash', 'c': True}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'for (let i=0; i<5; i++) necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for siklining 3 qismi?', 'a': [{'t': 'Boshlang\'ich, shart, o\'zgartirish', 'c': True}, {'t': 'Faqat shart', 'c': False}, {'t': 'Faqat boshlang\'ich', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for (;;) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'while va do-while sikllari', 't': 25, 'o': 12, 'q': [
        {'t': 'while sikli nima uchun?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'while (true) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'do-while va while farqi?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'while kamida 1 marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'do-while da shart qayerda tekshiriladi?', 'a': [{'t': 'Oxirida', 'c': True}, {'t': 'Boshida', 'c': False}, {'t': 'O\'rtada', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Sikldan chiqish uchun?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
    ]},
    {'n': 'Massivlar - Asoslar', 't': 25, 'o': 13, 'q': [
        {'t': 'Massiv nima?', 'a': [{'t': 'Bir necha qiymatlar to\'plami', 'c': True}, {'t': 'Bitta qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'let arr = [1, 2, 3]; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': 'arr[0] nima?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Ikkinchi element', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.length nima qaytaradi?', 'a': [{'t': 'Massiv uzunligi', 'c': True}, {'t': 'Massiv qiymati', 'c': False}, {'t': 'Massiv turi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'JavaScript massivida turli turlar bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, faqat bir xil tur', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Massiv o\'lchamini o\'zgartirish mumkinmi?', 'a': [{'t': 'Ha, dinamik', 'c': True}, {'t': 'Yo\'q, o\'zgarmas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Massiv metodlari - 1-qism', 't': 25, 'o': 14, 'q': [
        {'t': 'arr.push(5) nima qiladi?', 'a': [{'t': 'Oxiriga element qo\'shadi', 'c': True}, {'t': 'Boshiga element qo\'shadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.pop() nima qiladi?', 'a': [{'t': 'Oxirgi elementni o\'chiradi va qaytaradi', 'c': True}, {'t': 'Birinchi elementni o\'chiradi', 'c': False}, {'t': 'Element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.unshift(5) nima qiladi?', 'a': [{'t': 'Boshiga element qo\'shadi', 'c': True}, {'t': 'Oxiriga element qo\'shadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.shift() nima qiladi?', 'a': [{'t': 'Birinchi elementni o\'chiradi va qaytaradi', 'c': True}, {'t': 'Oxirgi elementni o\'chiradi', 'c': False}, {'t': 'Element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.indexOf(5) nima qiladi?', 'a': [{'t': '5 ning indeksini topadi', 'c': True}, {'t': '5 ni o\'chiradi', 'c': False}, {'t': '5 ni qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.includes(5) nima qaytaradi?', 'a': [{'t': 'true yoki false', 'c': True}, {'t': 'Indeks', 'c': False}, {'t': 'Element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Massiv metodlari - 2-qism', 't': 25, 'o': 15, 'q': [
        {'t': 'arr.slice(1, 3) nima qiladi?', 'a': [{'t': '1 dan 3 gacha (3 kirmaydi) qismini oladi', 'c': True}, {'t': 'Elementlarni o\'chiradi', 'c': False}, {'t': 'Element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.splice(1, 2) nima qiladi?', 'a': [{'t': '1-indeksdan 2 ta elementni o\'chiradi', 'c': True}, {'t': 'Element qo\'shadi', 'c': False}, {'t': 'Massivni kesadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.concat([4, 5]) nima qiladi?', 'a': [{'t': 'Massivlarni birlashtiradi', 'c': True}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Massivni kesadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.join("-") nima qiladi?', 'a': [{'t': 'Elementlarni stringga aylantiradi', 'c': True}, {'t': 'Massivlarni birlashtiradi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.reverse() nima qiladi?', 'a': [{'t': 'Massivni teskari qiladi', 'c': True}, {'t': 'Massivni saralaydi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.sort() nima qiladi?', 'a': [{'t': 'Massivni saralaydi', 'c': True}, {'t': 'Massivni teskari qiladi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'for...of va for...in sikllari', 't': 25, 'o': 16, 'q': [
        {'t': 'for...of nima uchun?', 'a': [{'t': 'Massiv qiymatlarini aylanish', 'c': True}, {'t': 'Ob\'ekt kalitlarini aylanish', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'for (let x of arr) nima qiladi?', 'a': [{'t': 'arr qiymatlarini aylanadi', 'c': True}, {'t': 'arr indekslarini aylanadi', 'c': False}, {'t': 'arr ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for...in nima uchun?', 'a': [{'t': 'Ob\'ekt kalitlarini aylanish', 'c': True}, {'t': 'Massiv qiymatlarini aylanish', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'for (let key in obj) nima qiladi?', 'a': [{'t': 'obj kalitlarini aylanadi', 'c': True}, {'t': 'obj qiymatlarini aylanadi', 'c': False}, {'t': 'obj ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for...of va for...in farqi?', 'a': [{'t': 'for...of qiymatlar, for...in kalitlar', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'for...of tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Funksiyalar - Asoslar', 't': 25, 'o': 17, 'q': [
        {'t': 'Funksiya nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Sikl', 'c': False}]},
        {'t': 'function myFunc() {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Funksiyani chaqirish?', 'a': [{'t': 'myFunc();', 'c': True}, {'t': 'call myFunc();', 'c': False}, {'t': 'run myFunc();', 'c': False}, {'t': 'execute myFunc();', 'c': False}]},
        {'t': 'Funksiyadan qiymat qaytarish uchun?', 'a': [{'t': 'return kalit so\'zi', 'c': True}, {'t': 'send kalit so\'zi', 'c': False}, {'t': 'give kalit so\'zi', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'return dan keyin kod bajariladimi?', 'a': [{'t': 'Yo\'q, funksiya to\'xtaydi', 'c': True}, {'t': 'Ha, bajariladi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Funksiya parametr olishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat bitta', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Funksiya parametrlari va argumentlar', 't': 25, 'o': 18, 'q': [
        {'t': 'Parametr nima?', 'a': [{'t': 'Funksiyaga beriladigan qiymat', 'c': True}, {'t': 'Funksiyadan qaytadigan qiymat', 'c': False}, {'t': 'Funksiya nomi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'function myFunc(x, y) {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Default parametr: function f(x=5) {} to\'g\'rimi?', 'a': [{'t': 'Ha, x berilmasa 5 bo\'ladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Rest parametr: function f(...args) {} nima?', 'a': [{'t': 'Barcha argumentlarni massivga yig\'adi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Birinchi argumentni oladi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Funksiyaga ko\'p argument berish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Arrow funksiyalar', 't': 25, 'o': 19, 'q': [
        {'t': 'Arrow funksiya nima?', 'a': [{'t': 'Qisqa funksiya yozuvi: () => {}', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'const f = () => 5; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Arrow funksiyada bitta ifoda bo\'lsa return kerakmi?', 'a': [{'t': 'Yo\'q, avtomatik qaytadi', 'c': True}, {'t': 'Ha, kerak', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'const f = x => x * 2; to\'g\'rimi?', 'a': [{'t': 'Ha, bitta parametrda () yo\'q', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Arrow va oddiy funksiya farqi?', 'a': [{'t': 'Arrow qisqaroq, this farq qiladi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Oddiy funksiya yangi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Arrow funksiyada ko\'p qator kod bo\'lsa?', 'a': [{'t': '{} va return kerak', 'c': True}, {'t': 'Avtomatik', 'c': False}, {'t': 'Mumkin emas', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ob\'ektlar - Asoslar', 't': 25, 'o': 20, 'q': [
        {'t': 'Ob\'ekt nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'let obj = {name: "Ali", age: 20}; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'obj.name ga qanday kirish mumkin?', 'a': [{'t': 'obj.name yoki obj["name"]', 'c': True}, {'t': 'Faqat obj.name', 'c': False}, {'t': 'Faqat obj["name"]', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'Ob\'ektga yangi xususiyat qo\'shish mumkinmi?', 'a': [{'t': 'Ha, obj.newProp = value', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat e\'lon qilishda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'delete obj.name nima qiladi?', 'a': [{'t': 'name xususiyatini o\'chiradi', 'c': True}, {'t': 'Ob\'ektni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Ob\'ektda funksiya bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, metod deyiladi', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ob\'ekt metodlari', 't': 25, 'o': 21, 'q': [
        {'t': 'Object.keys(obj) nima qaytaradi?', 'a': [{'t': 'Ob\'ekt kalitlari massivi', 'c': True}, {'t': 'Ob\'ekt qiymatlari massivi', 'c': False}, {'t': 'Ob\'ektning o\'zi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Object.values(obj) nima qaytaradi?', 'a': [{'t': 'Ob\'ekt qiymatlari massivi', 'c': True}, {'t': 'Ob\'ekt kalitlari massivi', 'c': False}, {'t': 'Ob\'ektning o\'zi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Object.entries(obj) nima qaytaradi?', 'a': [{'t': '[kalit, qiymat] juftliklari massivi', 'c': True}, {'t': 'Faqat kalitlar', 'c': False}, {'t': 'Faqat qiymatlar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Object.assign(target, source) nima qiladi?', 'a': [{'t': 'Ob\'ektlarni birlashtiradi', 'c': True}, {'t': 'Ob\'ektni o\'chiradi', 'c': False}, {'t': 'Ob\'ektni nusxalaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Object.freeze(obj) nima qiladi?', 'a': [{'t': 'Ob\'ektni o\'zgarmas qiladi', 'c': True}, {'t': 'Ob\'ektni o\'chiradi', 'c': False}, {'t': 'Ob\'ektni nusxalaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Array metodlari - map, filter, reduce', 't': 25, 'o': 22, 'q': [
        {'t': 'arr.map() nima qiladi?', 'a': [{'t': 'Har bir elementga funksiya qo\'llab yangi massiv yaratadi', 'c': True}, {'t': 'Elementlarni filtrlaydi', 'c': False}, {'t': 'Elementlarni qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.filter() nima qiladi?', 'a': [{'t': 'Shartga mos elementlarni filtrlaydi', 'c': True}, {'t': 'Har bir elementni o\'zgartiradi', 'c': False}, {'t': 'Elementlarni qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.reduce() nima qiladi?', 'a': [{'t': 'Massivni bitta qiymatga kamaytiradi', 'c': True}, {'t': 'Elementlarni filtrlaydi', 'c': False}, {'t': 'Yangi massiv yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.forEach() nima qiladi?', 'a': [{'t': 'Har bir element uchun funksiya bajaradi', 'c': True}, {'t': 'Yangi massiv qaytaradi', 'c': False}, {'t': 'Elementlarni filtrlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'map va forEach farqi?', 'a': [{'t': 'map yangi massiv qaytaradi, forEach yo\'q', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'forEach tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'arr.find() nima qiladi?', 'a': [{'t': 'Shartga mos birinchi elementni topadi', 'c': True}, {'t': 'Barcha mos elementlarni topadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Scope va hoisting', 't': 25, 'o': 23, 'q': [
        {'t': 'Scope nima?', 'a': [{'t': 'O\'zgaruvchining ko\'rinish doirasi', 'c': True}, {'t': 'O\'zgaruvchi turi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Global scope nima?', 'a': [{'t': 'Hamma joyda ko\'rinadigan o\'zgaruvchi', 'c': True}, {'t': 'Faqat funksiya ichida', 'c': False}, {'t': 'Faqat blok ichida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Local scope nima?', 'a': [{'t': 'Faqat ma\'lum joyda ko\'rinadigan', 'c': True}, {'t': 'Hamma joyda ko\'rinadigan', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Block scope nima?', 'a': [{'t': 'Faqat {} ichida ko\'rinadigan (let, const)', 'c': True}, {'t': 'Hamma joyda ko\'rinadigan', 'c': False}, {'t': 'Faqat var uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Hoisting nima?', 'a': [{'t': 'O\'zgaruvchi e\'lonlarini yuqoriga ko\'tarish', 'c': True}, {'t': 'O\'zgaruvchini o\'chirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'var hoisting qiladimi?', 'a': [{'t': 'Ha, undefined bilan', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Closure (Yopilish)', 't': 25, 'o': 24, 'q': [
        {'t': 'Closure nima?', 'a': [{'t': 'Funksiya tashqi o\'zgaruvchilarga kirishi', 'c': True}, {'t': 'Funksiyani yopish', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Closure qachon hosil bo\'ladi?', 'a': [{'t': 'Funksiya ichida funksiya yaratilganda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure nima uchun foydali?', 'a': [{'t': 'Private o\'zgaruvchilar yaratish', 'c': True}, {'t': 'Tezlikni oshirish', 'c': False}, {'t': 'Xatoliklarni kamaytirish', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Ichki funksiya tashqi o\'zgaruvchiga kiradimi?', 'a': [{'t': 'Ha, closure orqali', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure xotira iste\'mol qiladimi?', 'a': [{'t': 'Ha, o\'zgaruvchilarni saqlaydi', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'this kalit so\'zi', 't': 25, 'o': 25, 'q': [
        {'t': 'this nima?', 'a': [{'t': 'Joriy kontekstga havola', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Global kontekstda this nima?', 'a': [{'t': 'window (brauzerda)', 'c': True}, {'t': 'undefined', 'c': False}, {'t': 'null', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ob\'ekt metodida this nima?', 'a': [{'t': 'Ob\'ektning o\'zi', 'c': True}, {'t': 'window', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Arrow funksiyada this?', 'a': [{'t': 'Tashqi kontekstdan oladi', 'c': True}, {'t': 'O\'z this i bor', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Oddiy funksiyada this?', 'a': [{'t': 'Chaqirilish usuliga bog\'liq', 'c': True}, {'t': 'Har doim window', 'c': False}, {'t': 'Har doim undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Callback funksiyalar', 't': 25, 'o': 26, 'q': [
        {'t': 'Callback funksiya nima?', 'a': [{'t': 'Boshqa funksiyaga argument sifatida beriladigan funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Callback qachon ishlatiladi?', 'a': [{'t': 'Asinxron operatsiyalarda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'setTimeout(callback, 1000) nima qiladi?', 'a': [{'t': '1 soniyadan keyin callback ni chaqiradi', 'c': True}, {'t': 'Darhol chaqiradi', 'c': False}, {'t': '1000 marta chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'setInterval(callback, 1000) nima qiladi?', 'a': [{'t': 'Har 1 soniyada callback ni chaqiradi', 'c': True}, {'t': 'Bir marta chaqiradi', 'c': False}, {'t': '1000 marta chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Callback hell nima?', 'a': [{'t': 'Ko\'p ichma-ich callback lar', 'c': True}, {'t': 'Yaxshi kod', 'c': False}, {'t': 'Tez kod', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Promise (Va\'da)', 't': 25, 'o': 27, 'q': [
        {'t': 'Promise nima?', 'a': [{'t': 'Asinxron operatsiya natijasi', 'c': True}, {'t': 'Sinxron operatsiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Promise ning 3 holati?', 'a': [{'t': 'pending, fulfilled, rejected', 'c': True}, {'t': 'start, end, error', 'c': False}, {'t': 'begin, success, fail', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'promise.then() nima uchun?', 'a': [{'t': 'Muvaffaqiyatli natijani olish', 'c': True}, {'t': 'Xatolikni ushlash', 'c': False}, {'t': 'Promise yaratish', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'promise.catch() nima uchun?', 'a': [{'t': 'Xatolikni ushlash', 'c': True}, {'t': 'Natijani olish', 'c': False}, {'t': 'Promise yaratish', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'promise.finally() nima uchun?', 'a': [{'t': 'Har qanday holatda bajariladi', 'c': True}, {'t': 'Faqat muvaffaqiyatda', 'c': False}, {'t': 'Faqat xatolikda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Promise callback dan yaxshiroqmi?', 'a': [{'t': 'Ha, o\'qish oson', 'c': True}, {'t': 'Yo\'q, bir xil', 'c': False}, {'t': 'Callback yaxshiroq', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'async/await', 't': 25, 'o': 28, 'q': [
        {'t': 'async funksiya nima?', 'a': [{'t': 'Promise qaytaradigan funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'await nima qiladi?', 'a': [{'t': 'Promise tugashini kutadi', 'c': True}, {'t': 'Darhol qaytadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'await qayerda ishlatiladi?', 'a': [{'t': 'Faqat async funksiya ichida', 'c': True}, {'t': 'Hamma joyda', 'c': False}, {'t': 'Faqat global scope da', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'async/await va Promise farqi?', 'a': [{'t': 'async/await o\'qish osonroq', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Promise yangi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'async/await da xatolikni qanday ushlash?', 'a': [{'t': 'try...catch bilan', 'c': True}, {'t': '.catch() bilan', 'c': False}, {'t': 'Avtomatik', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'async funksiya har doim nima qaytaradi?', 'a': [{'t': 'Promise', 'c': True}, {'t': 'Oddiy qiymat', 'c': False}, {'t': 'undefined', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'try...catch - Xatoliklarni boshqarish', 't': 25, 'o': 29, 'q': [
        {'t': 'try...catch nima uchun?', 'a': [{'t': 'Xatoliklarni ushlash', 'c': True}, {'t': 'Kod yozish', 'c': False}, {'t': 'Sikl yaratish', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'try blokida xatolik bo\'lsa?', 'a': [{'t': 'catch bloki bajariladi', 'c': True}, {'t': 'Dastur to\'xtaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'catch bloki qachon bajariladi?', 'a': [{'t': 'try da xatolik bo\'lsa', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'finally bloki nima?', 'a': [{'t': 'Har qanday holatda bajariladi', 'c': True}, {'t': 'Faqat xatolikda', 'c': False}, {'t': 'Faqat muvaffaqiyatda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'throw nima qiladi?', 'a': [{'t': 'Xatolik yaratadi', 'c': True}, {'t': 'Xatolikni ushlaydi', 'c': False}, {'t': 'Dasturni to\'xtatadi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'try...catch xotira iste\'mol qiladimi?', 'a': [{'t': 'Ha, lekin oz', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Juda ko\'p', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'ES6+ yangi xususiyatlar', 't': 25, 'o': 30, 'q': [
        {'t': 'Destructuring nima?', 'a': [{'t': 'Massiv/ob\'ektdan qiymat ajratish', 'c': True}, {'t': 'Ob\'ektni buzish', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'const [a, b] = [1, 2]; to\'g\'rimi?', 'a': [{'t': 'Ha, array destructuring', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Spread operator: ...arr nima qiladi?', 'a': [{'t': 'Massivni yoyadi', 'c': True}, {'t': 'Massivni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Rest operator: ...args nima qiladi?', 'a': [{'t': 'Qolgan elementlarni yig\'adi', 'c': True}, {'t': 'Elementlarni yoyadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Template literal: `${x}` nima?', 'a': [{'t': 'String interpolatsiya', 'c': True}, {'t': 'Oddiy string', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'let va const qaysi ES versiyada?', 'a': [{'t': 'ES6 (ES2015)', 'c': True}, {'t': 'ES5', 'c': False}, {'t': 'ES3', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Arrow funksiya qaysi ES versiyada?', 'a': [{'t': 'ES6 (ES2015)', 'c': True}, {'t': 'ES5', 'c': False}, {'t': 'ES7', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_javascript()
    add_topics(subj, T)
    print(f"\n✅ JavaScript - {len(T)} ta mavzu muvaffaqiyatli qo\'shildi!")
