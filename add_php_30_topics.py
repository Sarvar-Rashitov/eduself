"""
PHP DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_php():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='PHP', defaults={'category': cat, 'description': 'PHP dasturlash tili - web dasturlash asoslari', 'icon': 'bi-code-square', 'order': 4, 'is_active': True})
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
    {'n': 'PHP dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'PHP nima?', 'a': [{'t': 'Server-side dasturlash tili', 'c': True}, {'t': 'Client-side dasturlash tili', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'PHP qachon yaratilgan?', 'a': [{'t': '1994 yilda', 'c': True}, {'t': '2000 yilda', 'c': False}, {'t': '1990 yilda', 'c': False}, {'t': '2010 yilda', 'c': False}]},
        {'t': 'PHP faylining kengaytmasi?', 'a': [{'t': '.php', 'c': True}, {'t': '.html', 'c': False}, {'t': '.js', 'c': False}, {'t': '.py', 'c': False}]},
        {'t': 'PHP kodi qanday boshlanadi?', 'a': [{'t': '<?php', 'c': True}, {'t': '<php>', 'c': False}, {'t': '<?', 'c': False}, {'t': '<script>', 'c': False}]},
        {'t': 'PHP kodi qanday tugaydi?', 'a': [{'t': '?>', 'c': True}, {'t': '</php>', 'c': False}, {'t': ';', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'PHP qayerda ishlaydi?', 'a': [{'t': 'Serverda', 'c': True}, {'t': 'Brauzerda', 'c': False}, {'t': 'Kompyuterda', 'c': False}, {'t': 'Telefonida', 'c': False}]},
    ]},
    {'n': 'Birinchi PHP dasturi', 't': 20, 'o': 2, 'q': [
        {'t': 'echo nima qiladi?', 'a': [{'t': 'Ekranga chiqaradi', 'c': True}, {'t': 'Kiritish qiladi', 'c': False}, {'t': 'Hisoblash qiladi', 'c': False}, {'t': 'Saqlaydi', 'c': False}]},
        {'t': 'echo "Hello"; natijasi?', 'a': [{'t': 'Hello', 'c': True}, {'t': '"Hello"', 'c': False}, {'t': 'echo Hello', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'print va echo farqi?', 'a': [{'t': 'print qiymat qaytaradi, echo yo\'q', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'echo tezroq', 'c': False}, {'t': 'print xato', 'c': False}]},
        {'t': 'PHP da izoh qanday yoziladi?', 'a': [{'t': '// yoki /* */ yoki #', 'c': True}, {'t': 'Faqat //', 'c': False}, {'t': '<!-- -->', 'c': False}, {'t': '\'\'\' bilan', 'c': False}]},
        {'t': 'PHP da operator qanday tugaydi?', 'a': [{'t': '; belgisi bilan', 'c': True}, {'t': 'Yangi qator bilan', 'c': False}, {'t': 'Bo\'sh joy bilan', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar', 't': 25, 'o': 3, 'q': [
        {'t': 'PHP da o\'zgaruvchi qanday boshlanadi?', 'a': [{'t': '$ belgisi bilan', 'c': True}, {'t': '@ belgisi bilan', 'c': False}, {'t': '# belgisi bilan', 'c': False}, {'t': 'Harf bilan', 'c': False}]},
        {'t': '$name = "Ali"; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'PHP da o\'zgaruvchi turini e\'lon qilish kerakmi?', 'a': [{'t': 'Yo\'q, avtomatik aniqlanadi', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan kerak', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '$name va $Name bir xilmi?', 'a': [{'t': 'Yo\'q, PHP case-sensitive', 'c': True}, {'t': 'Ha, bir xil', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'O\'zgaruvchi nomi raqam bilan boshlanishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'var_dump() nima qiladi?', 'a': [{'t': 'O\'zgaruvchi haqida ma\'lumot beradi', 'c': True}, {'t': 'O\'zgaruvchini o\'chiradi', 'c': False}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari', 't': 25, 'o': 4, 'q': [
        {'t': 'PHP da qanday ma\'lumot turlari bor?', 'a': [{'t': 'String, Integer, Float, Boolean, Array, Object, NULL', 'c': True}, {'t': 'Faqat String va Integer', 'c': False}, {'t': 'Faqat Number va Text', 'c': False}, {'t': 'Yo\'q', 'c': False}]},
        {'t': 'String nima?', 'a': [{'t': 'Matn turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'Integer nima?', 'a': [{'t': 'Butun son turi', 'c': True}, {'t': 'O\'nli kasr', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'Float nima?', 'a': [{'t': 'O\'nli kasr son turi', 'c': True}, {'t': 'Butun son', 'c': False}, {'t': 'Matn', 'c': False}, {'t': 'Mantiqiy qiymat', 'c': False}]},
        {'t': 'Boolean qanday qiymatlar oladi?', 'a': [{'t': 'true yoki false', 'c': True}, {'t': '0 yoki 1', 'c': False}, {'t': 'yes yoki no', 'c': False}, {'t': 'on yoki off', 'c': False}]},
        {'t': 'NULL nima?', 'a': [{'t': 'Qiymat yo\'q', 'c': True}, {'t': '0 qiymati', 'c': False}, {'t': 'Bo\'sh string', 'c': False}, {'t': 'false', 'c': False}]},
        {'t': 'gettype() nima qiladi?', 'a': [{'t': 'O\'zgaruvchi turini qaytaradi', 'c': True}, {'t': 'O\'zgaruvchi qiymatini qaytaradi', 'c': False}, {'t': 'O\'zgaruvchini o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Stringlar bilan ishlash', 't': 25, 'o': 5, 'q': [
        {'t': 'Stringlarni birlashtirish operatori?', 'a': [{'t': '. (nuqta)', 'c': True}, {'t': '+ (plyus)', 'c': False}, {'t': '& (ampersand)', 'c': False}, {'t': ', (vergul)', 'c': False}]},
        {'t': '"Hello" . " World" natijasi?', 'a': [{'t': 'Hello World', 'c': True}, {'t': 'HelloWorld', 'c': False}, {'t': 'Hello.World', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'strlen() nima qiladi?', 'a': [{'t': 'String uzunligini qaytaradi', 'c': True}, {'t': 'Stringni o\'chiradi', 'c': False}, {'t': 'Stringni teskari qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'str_replace() nima qiladi?', 'a': [{'t': 'Stringda qidirish va almashtirish', 'c': True}, {'t': 'Stringni o\'chiradi', 'c': False}, {'t': 'Stringni teskari qiladi', 'c': False}, {'t': 'String uzunligini topadi', 'c': False}]},
        {'t': 'strtoupper() nima qiladi?', 'a': [{'t': 'Katta harflarga o\'tkazadi', 'c': True}, {'t': 'Kichik harflarga o\'tkazadi', 'c': False}, {'t': 'Birinchi harfni katta qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'strtolower() nima qiladi?', 'a': [{'t': 'Kichik harflarga o\'tkazadi', 'c': True}, {'t': 'Katta harflarga o\'tkazadi', 'c': False}, {'t': 'Birinchi harfni kichik qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Operatorlar', 't': 25, 'o': 6, 'q': [
        {'t': '5 + 3 natijasi?', 'a': [{'t': '8', 'c': True}, {'t': '53', 'c': False}, {'t': '2', 'c': False}, {'t': '15', 'c': False}]},
        {'t': '10 / 3 natijasi?', 'a': [{'t': '3.333...', 'c': True}, {'t': '3', 'c': False}, {'t': '4', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '10 % 3 natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '5 == "5" natijasi?', 'a': [{'t': 'true (qiymat teng)', 'c': True}, {'t': 'false', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'NULL', 'c': False}]},
        {'t': '5 === "5" natijasi?', 'a': [{'t': 'false (tur ham tekshiriladi)', 'c': True}, {'t': 'true', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'NULL', 'c': False}]},
        {'t': '++ operatori nima qiladi?', 'a': [{'t': '1 ga oshiradi', 'c': True}, {'t': '1 ga kamaytiradi', 'c': False}, {'t': '2 ga ko\'paytiradi', 'c': False}, {'t': 'Qo\'shadi', 'c': False}]},
        {'t': '&& operatori nima?', 'a': [{'t': 'Mantiqiy VA (AND)', 'c': True}, {'t': 'Mantiqiy YOKI (OR)', 'c': False}, {'t': 'Mantiqiy EMAS (NOT)', 'c': False}, {'t': 'Qo\'shish', 'c': False}]},
    ]},
    {'n': 'if operatori', 't': 25, 'o': 7, 'q': [
        {'t': 'if operatori nima uchun?', 'a': [{'t': 'Shartli bajarish', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'if ($x > 5) echo "Katta"; qachon ishlaydi?', 'a': [{'t': '$x 5 dan katta bo\'lsa', 'c': True}, {'t': '$x 5 ga teng bo\'lsa', 'c': False}, {'t': '$x 5 dan kichik bo\'lsa', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'if blokida kod qanday yoziladi?', 'a': [{'t': 'Jingalak qavslar ichida {}', 'c': True}, {'t': 'Oddiy qavslar ichida ()', 'c': False}, {'t': 'Kvadrat qavslar ichida []', 'c': False}, {'t': 'Qo\'shtirnoqda ""', 'c': False}]},
        {'t': 'if ($x == 5) nima tekshiradi?', 'a': [{'t': '$x 5 ga tengmi', 'c': True}, {'t': '$x ga 5 ni beradi', 'c': False}, {'t': '$x 5 dan kattami', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir qatorli if da {} kerakmi?', 'a': [{'t': 'Yo\'q, ixtiyoriy', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'if-else operatori', 't': 25, 'o': 8, 'q': [
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'elseif nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Bir necha elseif ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'if-elseif-else ketma-ketligi to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, else birinchi', 'c': False}, {'t': 'Yo\'q, elseif oxirida', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Ternary operator: $x > 5 ? "Katta" : "Kichik"', 'a': [{'t': '$x>5 bo\'lsa "Katta", aks holda "Kichik"', 'c': True}, {'t': '$x va 5 ni taqqoslaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Stringlarni qo\'shadi', 'c': False}]},
    ]},
    {'n': 'switch-case operatori', 't': 25, 'o': 9, 'q': [
        {'t': 'switch-case nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'case nima?', 'a': [{'t': 'Bir variant', 'c': True}, {'t': 'Shart', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'break nima qiladi?', 'a': [{'t': 'switch dan chiqadi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Qayta boshlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'switch da break qo\'ymasak?', 'a': [{'t': 'Keyingi case ham bajariladi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'To\'xtaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'while sikli', 't': 25, 'o': 10, 'q': [
        {'t': 'while sikli nima uchun?', 'a': [{'t': 'Shart to\'g\'ri bo\'lguncha takrorlash', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'while (true) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Sikldan chiqish uchun?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'Siklning keyingi iteratsiyasiga o\'tish?', 'a': [{'t': 'continue', 'c': True}, {'t': 'skip', 'c': False}, {'t': 'next', 'c': False}, {'t': 'pass', 'c': False}]},
        {'t': '$i=0; while($i<3) {echo $i; $i++;} necha marta?', 'a': [{'t': '3 marta', 'c': True}, {'t': '2 marta', 'c': False}, {'t': '4 marta', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
    ]},
    {'n': 'do-while sikli', 't': 20, 'o': 11, 'q': [
        {'t': 'do-while va while farqi?', 'a': [{'t': 'do-while kamida 1 marta ishlaydi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'while kamida 1 marta ishlaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'do-while da shart qayerda tekshiriladi?', 'a': [{'t': 'Oxirida', 'c': True}, {'t': 'Boshida', 'c': False}, {'t': 'O\'rtada', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'do {...} while($shart); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while oxirida ; kerakmi?', 'a': [{'t': 'Ha, kerak', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'do-while qachon ishlatiladi?', 'a': [{'t': 'Kamida 1 marta bajarish kerak bo\'lsa', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat katta dasturlarda', 'c': False}]},
    ]},
    {'n': 'for sikli', 't': 25, 'o': 12, 'q': [
        {'t': 'for sikli nima uchun?', 'a': [{'t': 'Ma\'lum marta takrorlash', 'c': True}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'for ($i=0; $i<5; $i++) necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for siklining 3 qismi?', 'a': [{'t': 'Boshlang\'ich, shart, o\'zgartirish', 'c': True}, {'t': 'Faqat shart', 'c': False}, {'t': 'Faqat boshlang\'ich', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for (;;) nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'foreach sikli', 't': 25, 'o': 13, 'q': [
        {'t': 'foreach nima uchun?', 'a': [{'t': 'Massivlarni aylanish', 'c': True}, {'t': 'Oddiy takrorlash', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}]},
        {'t': 'foreach ($arr as $value) nima qiladi?', 'a': [{'t': '$arr massivini aylanadi', 'c': True}, {'t': '$arr ni yaratadi', 'c': False}, {'t': '$arr ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'foreach ($arr as $key => $value) nima?', 'a': [{'t': 'Kalit va qiymatni oladi', 'c': True}, {'t': 'Faqat qiymatni oladi', 'c': False}, {'t': 'Faqat kalitni oladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'foreach da elementni o\'zgartirish uchun?', 'a': [{'t': 'foreach ($arr as &$value)', 'c': True}, {'t': 'foreach ($arr as $value)', 'c': False}, {'t': 'foreach ($arr)', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'foreach va for farqi?', 'a': [{'t': 'foreach massivlar uchun qulay', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'for tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Massivlar - Asoslar', 't': 25, 'o': 14, 'q': [
        {'t': 'Massiv nima?', 'a': [{'t': 'Bir necha qiymatni saqlovchi o\'zgaruvchi', 'c': True}, {'t': 'Bitta qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': '$arr = array(1,2,3); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '$arr = [1,2,3]; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri (PHP 5.4+)', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Faqat PHP 7 da', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': '$arr[0] nima?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Ikkinchi element', 'c': False}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'count() nima qiladi?', 'a': [{'t': 'Massiv elementlari sonini qaytaradi', 'c': True}, {'t': 'Massivni o\'chiradi', 'c': False}, {'t': 'Massivni saralaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Assotsiativ massivlar', 't': 25, 'o': 15, 'q': [
        {'t': 'Assotsiativ massiv nima?', 'a': [{'t': 'Kalit-qiymat juftliklari massivi', 'c': True}, {'t': 'Oddiy massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '$arr = ["ism" => "Ali", "yosh" => 20]; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '$arr["ism"] nima qaytaradi?', 'a': [{'t': '"Ali"', 'c': True}, {'t': '"ism"', 'c': False}, {'t': '0', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'array_keys() nima qiladi?', 'a': [{'t': 'Barcha kalitlarni qaytaradi', 'c': True}, {'t': 'Barcha qiymatlarni qaytaradi', 'c': False}, {'t': 'Massivni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'array_values() nima qiladi?', 'a': [{'t': 'Barcha qiymatlarni qaytaradi', 'c': True}, {'t': 'Barcha kalitlarni qaytaradi', 'c': False}, {'t': 'Massivni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Massiv funksiyalari', 't': 30, 'o': 16, 'q': [
        {'t': 'array_push() nima qiladi?', 'a': [{'t': 'Massiv oxiriga element qo\'shadi', 'c': True}, {'t': 'Massiv boshiga element qo\'shadi', 'c': False}, {'t': 'Massivdan element o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'array_pop() nima qiladi?', 'a': [{'t': 'Massiv oxiridan element o\'chiradi', 'c': True}, {'t': 'Massiv boshidan element o\'chiradi', 'c': False}, {'t': 'Massivga element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'array_shift() nima qiladi?', 'a': [{'t': 'Massiv boshidan element o\'chiradi', 'c': True}, {'t': 'Massiv oxiridan element o\'chiradi', 'c': False}, {'t': 'Massivga element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'array_unshift() nima qiladi?', 'a': [{'t': 'Massiv boshiga element qo\'shadi', 'c': True}, {'t': 'Massiv oxiriga element qo\'shadi', 'c': False}, {'t': 'Massivdan element o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sort() nima qiladi?', 'a': [{'t': 'Massivni o\'sish tartibida saralaydi', 'c': True}, {'t': 'Massivni kamayish tartibida saralaydi', 'c': False}, {'t': 'Massivni teskari qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'rsort() nima qiladi?', 'a': [{'t': 'Massivni kamayish tartibida saralaydi', 'c': True}, {'t': 'Massivni o\'sish tartibida saralaydi', 'c': False}, {'t': 'Massivni teskari qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'in_array() nima qiladi?', 'a': [{'t': 'Element massivda bormi tekshiradi', 'c': True}, {'t': 'Elementni massivga qo\'shadi', 'c': False}, {'t': 'Elementni massivdan o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'array_merge() nima qiladi?', 'a': [{'t': 'Massivlarni birlashtiradi', 'c': True}, {'t': 'Massivni bo\'ladi', 'c': False}, {'t': 'Massivni saralaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Funksiyalar - Asoslar', 't': 25, 'o': 17, 'q': [
        {'t': 'Funksiya nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Ma\'lumot turi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'function salom() {...} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Funksiya qanday chaqiriladi?', 'a': [{'t': 'salom();', 'c': True}, {'t': 'call salom();', 'c': False}, {'t': 'run salom();', 'c': False}, {'t': 'execute salom();', 'c': False}]},
        {'t': 'return nima qiladi?', 'a': [{'t': 'Qiymat qaytaradi va funksiyadan chiqadi', 'c': True}, {'t': 'Faqat qiymat qaytaradi', 'c': False}, {'t': 'Faqat funksiyadan chiqadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiya parametrsiz bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, kamida 1 ta parametr kerak', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Funksiya parametrlari', 't': 25, 'o': 18, 'q': [
        {'t': 'function sum($a, $b) - $a va $b nima?', 'a': [{'t': 'Parametrlar', 'c': True}, {'t': 'Argumentlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'sum(5, 3) - 5 va 3 nima?', 'a': [{'t': 'Argumentlar', 'c': True}, {'t': 'Parametrlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Default parametr nima?', 'a': [{'t': 'Standart qiymatga ega parametr', 'c': True}, {'t': 'Majburiy parametr', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Funksiya nomi', 'c': False}]},
        {'t': 'function salom($ism = "Mehmon") to\'g\'rimi?', 'a': [{'t': 'Ha, default parametr', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Parametrni referens orqali uzatish?', 'a': [{'t': 'function test(&$x)', 'c': True}, {'t': 'function test($x)', 'c': False}, {'t': 'function test(*$x)', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'func_get_args() nima qiladi?', 'a': [{'t': 'Barcha argumentlarni massiv sifatida qaytaradi', 'c': True}, {'t': 'Birinchi argumentni qaytaradi', 'c': False}, {'t': 'Argumentlar sonini qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Global va lokal o\'zgaruvchilar', 't': 25, 'o': 19, 'q': [
        {'t': 'Lokal o\'zgaruvchi nima?', 'a': [{'t': 'Funksiya ichida e\'lon qilingan', 'c': True}, {'t': 'Funksiya tashqarida e\'lon qilingan', 'c': False}, {'t': 'Hamma joyda ko\'rinadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Global o\'zgaruvchi nima?', 'a': [{'t': 'Funksiya tashqarida e\'lon qilingan', 'c': True}, {'t': 'Funksiya ichida e\'lon qilingan', 'c': False}, {'t': 'Faqat funksiyada ko\'rinadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiyada global o\'zgaruvchiga qanday kirish mumkin?', 'a': [{'t': 'global kalit so\'zi bilan', 'c': True}, {'t': 'Avtomatik', 'c': False}, {'t': 'import bilan', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': '$GLOBALS nima?', 'a': [{'t': 'Barcha global o\'zgaruvchilar massivi', 'c': True}, {'t': 'Lokal o\'zgaruvchilar massivi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'static o\'zgaruvchi nima?', 'a': [{'t': 'Qiymati saqlanib qoladigan lokal o\'zgaruvchi', 'c': True}, {'t': 'Global o\'zgaruvchi', 'c': False}, {'t': 'Oddiy lokal o\'zgaruvchi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Include va Require', 't': 25, 'o': 20, 'q': [
        {'t': 'include nima qiladi?', 'a': [{'t': 'Boshqa faylni ulaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'require nima qiladi?', 'a': [{'t': 'Boshqa faylni ulaydi (majburiy)', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'include va require farqi?', 'a': [{'t': 'require xato bo\'lsa dasturni to\'xtatadi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'include tezroq', 'c': False}, {'t': 'require sekinroq', 'c': False}]},
        {'t': 'include_once nima?', 'a': [{'t': 'Faylni faqat bir marta ulaydi', 'c': True}, {'t': 'Faylni bir necha marta ulaydi', 'c': False}, {'t': 'Faylni ulamaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'require_once nima?', 'a': [{'t': 'Faylni faqat bir marta ulaydi (majburiy)', 'c': True}, {'t': 'Faylni bir necha marta ulaydi', 'c': False}, {'t': 'Faylni ulamaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Superglobal o\'zgaruvchilar', 't': 30, 'o': 21, 'q': [
        {'t': 'Superglobal o\'zgaruvchilar nima?', 'a': [{'t': 'Hamma joyda mavjud bo\'lgan o\'zgaruvchilar', 'c': True}, {'t': 'Oddiy o\'zgaruvchilar', 'c': False}, {'t': 'Lokal o\'zgaruvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '$_GET nima uchun?', 'a': [{'t': 'URL parametrlarini olish', 'c': True}, {'t': 'POST ma\'lumotlarini olish', 'c': False}, {'t': 'Cookie olish', 'c': False}, {'t': 'Session olish', 'c': False}]},
        {'t': '$_POST nima uchun?', 'a': [{'t': 'POST ma\'lumotlarini olish', 'c': True}, {'t': 'URL parametrlarini olish', 'c': False}, {'t': 'Cookie olish', 'c': False}, {'t': 'Session olish', 'c': False}]},
        {'t': '$_SESSION nima uchun?', 'a': [{'t': 'Session ma\'lumotlarini saqlash', 'c': True}, {'t': 'Cookie saqlash', 'c': False}, {'t': 'POST ma\'lumotlarini olish', 'c': False}, {'t': 'URL parametrlarini olish', 'c': False}]},
        {'t': '$_COOKIE nima uchun?', 'a': [{'t': 'Cookie ma\'lumotlarini olish', 'c': True}, {'t': 'Session ma\'lumotlarini olish', 'c': False}, {'t': 'POST ma\'lumotlarini olish', 'c': False}, {'t': 'URL parametrlarini olish', 'c': False}]},
        {'t': '$_SERVER nima?', 'a': [{'t': 'Server va muhit ma\'lumotlari', 'c': True}, {'t': 'Foydalanuvchi ma\'lumotlari', 'c': False}, {'t': 'POST ma\'lumotlari', 'c': False}, {'t': 'Cookie ma\'lumotlari', 'c': False}]},
        {'t': '$_FILES nima uchun?', 'a': [{'t': 'Yuklangan fayllar haqida ma\'lumot', 'c': True}, {'t': 'Server fayllari', 'c': False}, {'t': 'Cookie fayllari', 'c': False}, {'t': 'Session fayllari', 'c': False}]},
    ]},
    {'n': 'Form bilan ishlash', 't': 30, 'o': 22, 'q': [
        {'t': 'Form ma\'lumotlarini qanday olish mumkin?', 'a': [{'t': '$_GET yoki $_POST orqali', 'c': True}, {'t': '$_FORM orqali', 'c': False}, {'t': '$_INPUT orqali', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'GET metodi nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlarni URL orqali yuborish', 'c': True}, {'t': 'Maxfiy ma\'lumotlarni yuborish', 'c': False}, {'t': 'Fayl yuborish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'POST metodi nima uchun ishlatiladi?', 'a': [{'t': 'Maxfiy ma\'lumotlarni yuborish', 'c': True}, {'t': 'Ma\'lumotlarni URL da ko\'rsatish', 'c': False}, {'t': 'Faqat raqam yuborish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'GET va POST farqi?', 'a': [{'t': 'GET URL da ko\'rinadi, POST yo\'q', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'POST tezroq', 'c': False}, {'t': 'GET xavfsizroq', 'c': False}]},
        {'t': 'isset() nima qiladi?', 'a': [{'t': 'O\'zgaruvchi mavjudmi tekshiradi', 'c': True}, {'t': 'O\'zgaruvchi qiymatini oladi', 'c': False}, {'t': 'O\'zgaruvchini o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'empty() nima qiladi?', 'a': [{'t': 'O\'zgaruvchi bo\'shmi tekshiradi', 'c': True}, {'t': 'O\'zgaruvchini bo\'shatadi', 'c': False}, {'t': 'O\'zgaruvchi yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Fayl bilan ishlash', 't': 30, 'o': 23, 'q': [
        {'t': 'fopen() nima qiladi?', 'a': [{'t': 'Faylni ochadi', 'c': True}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'fclose() nima qiladi?', 'a': [{'t': 'Faylni yopadi', 'c': True}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'fread() nima qiladi?', 'a': [{'t': 'Fayldan o\'qiydi', 'c': True}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'fwrite() nima qiladi?', 'a': [{'t': 'Faylga yozadi', 'c': True}, {'t': 'Fayldan o\'qiydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'file_get_contents() nima qiladi?', 'a': [{'t': 'Fayl mazmunini string sifatida o\'qiydi', 'c': True}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'file_put_contents() nima qiladi?', 'a': [{'t': 'Faylga string yozadi', 'c': True}, {'t': 'Fayldan o\'qiydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Fayl yaratadi va yozadi', 'c': False}]},
        {'t': 'unlink() nima qiladi?', 'a': [{'t': 'Faylni o\'chiradi', 'c': True}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Fayldan o\'qiydi', 'c': False}]},
    ]},
    {'n': 'Cookie va Session', 't': 30, 'o': 24, 'q': [
        {'t': 'Cookie nima?', 'a': [{'t': 'Foydalanuvchi kompyuterida saqlanadigan ma\'lumot', 'c': True}, {'t': 'Serverda saqlanadigan ma\'lumot', 'c': False}, {'t': 'Ma\'lumotlar bazasida saqlanadigan ma\'lumot', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'setcookie() nima qiladi?', 'a': [{'t': 'Cookie yaratadi', 'c': True}, {'t': 'Cookie o\'chiradi', 'c': False}, {'t': 'Cookie o\'qiydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Session nima?', 'a': [{'t': 'Serverda saqlanadigan foydalanuvchi ma\'lumotlari', 'c': True}, {'t': 'Foydalanuvchi kompyuterida saqlanadigan ma\'lumot', 'c': False}, {'t': 'Ma\'lumotlar bazasida saqlanadigan ma\'lumot', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'session_start() nima qiladi?', 'a': [{'t': 'Session boshlaydi', 'c': True}, {'t': 'Session to\'xtatadi', 'c': False}, {'t': 'Session o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'session_destroy() nima qiladi?', 'a': [{'t': 'Session ma\'lumotlarini o\'chiradi', 'c': True}, {'t': 'Session boshlaydi', 'c': False}, {'t': 'Session yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Cookie va Session farqi?', 'a': [{'t': 'Cookie clientda, Session serverda', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Cookie xavfsizroq', 'c': False}, {'t': 'Session tezroq', 'c': False}]},
    ]},
    {'n': 'OOP - Klasslar va Obyektlar', 't': 30, 'o': 25, 'q': [
        {'t': 'Klass nima?', 'a': [{'t': 'Obyektlar uchun shablon', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Modul', 'c': False}]},
        {'t': 'class Student {...} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Obyekt nima?', 'a': [{'t': 'Klassning namunasi', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': '$s = new Student(); nima qiladi?', 'a': [{'t': 'Student obyektini yaratadi', 'c': True}, {'t': 'Student klassini yaratadi', 'c': False}, {'t': 'Student funksiyasini chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'new kalit so\'zi nima uchun?', 'a': [{'t': 'Obyekt yaratish', 'c': True}, {'t': 'Klass yaratish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'O\'zgaruvchi yaratish', 'c': False}]},
        {'t': '$this nima?', 'a': [{'t': 'Joriy obyektga murojaat', 'c': True}, {'t': 'Klassga murojaat', 'c': False}, {'t': 'Funksiyaga murojaat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OOP - Properties va Methods', 't': 30, 'o': 26, 'q': [
        {'t': 'Property nima?', 'a': [{'t': 'Klass o\'zgaruvchisi', 'c': True}, {'t': 'Klass funksiyasi', 'c': False}, {'t': 'Obyekt', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Method nima?', 'a': [{'t': 'Klass funksiyasi', 'c': True}, {'t': 'Klass o\'zgaruvchisi', 'c': False}, {'t': 'Obyekt', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'public nima?', 'a': [{'t': 'Hamma joydan kirish mumkin', 'c': True}, {'t': 'Faqat klass ichidan', 'c': False}, {'t': 'Faqat meros oluvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'private nima?', 'a': [{'t': 'Faqat klass ichidan kirish mumkin', 'c': True}, {'t': 'Hamma joydan kirish mumkin', 'c': False}, {'t': 'Faqat meros oluvchilar', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'protected nima?', 'a': [{'t': 'Klass va meros oluvchilar', 'c': True}, {'t': 'Faqat klass ichidan', 'c': False}, {'t': 'Hamma joydan', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '$obj->property qanday ishlaydi?', 'a': [{'t': 'Obyekt propertyga murojaat', 'c': True}, {'t': 'Klass propertyga murojaat', 'c': False}, {'t': 'Funksiya chaqiruvi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'OOP - Constructor va Destructor', 't': 25, 'o': 27, 'q': [
        {'t': 'Constructor nima?', 'a': [{'t': 'Obyekt yaratilganda chaqiriladigan metod', 'c': True}, {'t': 'Obyekt o\'chirilganda chaqiriladigan metod', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '__construct() nima?', 'a': [{'t': 'Constructor metodi', 'c': True}, {'t': 'Destructor metodi', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Destructor nima?', 'a': [{'t': 'Obyekt o\'chirilganda chaqiriladigan metod', 'c': True}, {'t': 'Obyekt yaratilganda chaqiriladigan metod', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '__destruct() nima?', 'a': [{'t': 'Destructor metodi', 'c': True}, {'t': 'Constructor metodi', 'c': False}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Constructor parametr olishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat bitta parametr', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'OOP - Inheritance (Meros)', 't': 30, 'o': 28, 'q': [
        {'t': 'Inheritance nima?', 'a': [{'t': 'Bir klassdan boshqa klass yaratish', 'c': True}, {'t': 'Klass nusxalash', 'c': False}, {'t': 'Metod yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'class Dog extends Animal nima?', 'a': [{'t': 'Dog Animal dan meros oladi', 'c': True}, {'t': 'Animal Dog dan meros oladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech qanday aloqa yo\'q', 'c': False}]},
        {'t': 'extends kalit so\'zi nima uchun?', 'a': [{'t': 'Meros olish uchun', 'c': True}, {'t': 'Klass yaratish uchun', 'c': False}, {'t': 'Metod yaratish uchun', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'parent:: nima uchun?', 'a': [{'t': 'Ota klassga murojaat', 'c': True}, {'t': 'Bola klassga murojaat', 'c': False}, {'t': 'O\'ziga murojaat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'PHP da bir necha klassdan meros olish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat bitta klassdan', 'c': True}, {'t': 'Ha, bir necha klassdan', 'c': False}, {'t': 'Faqat ikkita klassdan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'OOP - Abstract va Interface', 't': 30, 'o': 29, 'q': [
        {'t': 'Abstract class nima?', 'a': [{'t': 'Obyekt yaratib bo\'lmaydigan klass', 'c': True}, {'t': 'Oddiy klass', 'c': False}, {'t': 'Interface', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'abstract kalit so\'zi nima uchun?', 'a': [{'t': 'Abstract klass yoki metod yaratish', 'c': True}, {'t': 'Oddiy klass yaratish', 'c': False}, {'t': 'Interface yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Abstract metod nima?', 'a': [{'t': 'Tanasi bo\'lmagan metod', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Private metod', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Interface nima?', 'a': [{'t': 'Metodlar shartnomasi', 'c': True}, {'t': 'Klass', 'c': False}, {'t': 'Metod', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'interface IAnimal {...} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'implements kalit so\'zi nima uchun?', 'a': [{'t': 'Interface implement qilish', 'c': True}, {'t': 'Meros olish', 'c': False}, {'t': 'Klass yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bir klass bir necha interface implement qilishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},
    {'n': 'MySQL bilan ishlash', 't': 30, 'o': 30, 'q': [
        {'t': 'MySQL nima?', 'a': [{'t': 'Ma\'lumotlar bazasi tizimi', 'c': True}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Web server', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'mysqli_connect() nima qiladi?', 'a': [{'t': 'Ma\'lumotlar bazasiga ulanadi', 'c': True}, {'t': 'Ma\'lumotlar bazasini yaratadi', 'c': False}, {'t': 'Ma\'lumotlar bazasini o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'mysqli_query() nima qiladi?', 'a': [{'t': 'SQL so\'rovini bajaradi', 'c': True}, {'t': 'Ma\'lumotlar bazasiga ulanadi', 'c': False}, {'t': 'Ma\'lumotlar bazasini yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'SELECT so\'rovi nima uchun?', 'a': [{'t': 'Ma\'lumotlarni o\'qish', 'c': True}, {'t': 'Ma\'lumotlarni qo\'shish', 'c': False}, {'t': 'Ma\'lumotlarni o\'chirish', 'c': False}, {'t': 'Ma\'lumotlarni yangilash', 'c': False}]},
        {'t': 'INSERT so\'rovi nima uchun?', 'a': [{'t': 'Ma\'lumotlarni qo\'shish', 'c': True}, {'t': 'Ma\'lumotlarni o\'qish', 'c': False}, {'t': 'Ma\'lumotlarni o\'chirish', 'c': False}, {'t': 'Ma\'lumotlarni yangilash', 'c': False}]},
        {'t': 'UPDATE so\'rovi nima uchun?', 'a': [{'t': 'Ma\'lumotlarni yangilash', 'c': True}, {'t': 'Ma\'lumotlarni qo\'shish', 'c': False}, {'t': 'Ma\'lumotlarni o\'chirish', 'c': False}, {'t': 'Ma\'lumotlarni o\'qish', 'c': False}]},
        {'t': 'DELETE so\'rovi nima uchun?', 'a': [{'t': 'Ma\'lumotlarni o\'chirish', 'c': True}, {'t': 'Ma\'lumotlarni qo\'shish', 'c': False}, {'t': 'Ma\'lumotlarni yangilash', 'c': False}, {'t': 'Ma\'lumotlarni o\'qish', 'c': False}]},
        {'t': 'mysqli_fetch_assoc() nima qiladi?', 'a': [{'t': 'Natijani assotsiativ massiv sifatida oladi', 'c': True}, {'t': 'Natijani oddiy massiv sifatida oladi', 'c': False}, {'t': 'Natijani o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🔷 PHP DASTURLASH - 30 TA MAVZU")
    print("=" * 80)
    subject = get_or_create_php()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T)
    total = sum(len(t['q']) for t in T)
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! {len(T)} ta mavzu, {total} ta test qo'shildi!")
    print(f"📝 To'g'ri javoblar tasodifiy joylashtirildi")
    print("=" * 80)
