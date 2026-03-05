"""
GO DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_go():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Go', defaults={'category': cat, 'description': 'Go dasturlash tili - zamonaviy va samarali dasturlash', 'icon': 'bi-filetype-go', 'order': 7, 'is_active': True})
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
    {'n': 'Go dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Go dasturlash tili qachon yaratilgan?', 'a': [{'t': '2009 yilda', 'c': True}, {'t': '2015 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}, {'t': '2020 yilda', 'c': False}]},
        {'t': 'Go tilini kim yaratgan?', 'a': [{'t': 'Google kompaniyasi (Robert Griesemer, Rob Pike, Ken Thompson)', 'c': True}, {'t': 'Microsoft', 'c': False}, {'t': 'Apple', 'c': False}, {'t': 'Facebook', 'c': False}]},
        {'t': 'Go tilining boshqa nomi?', 'a': [{'t': 'Golang', 'c': True}, {'t': 'GoLang++', 'c': False}, {'t': 'GoScript', 'c': False}, {'t': 'GoCode', 'c': False}]},
        {'t': 'Go fayl kengaytmasi?', 'a': [{'t': '.go', 'c': True}, {'t': '.golang', 'c': False}, {'t': '.g', 'c': False}, {'t': '.gol', 'c': False}]},
        {'t': 'Go tilining asosiy xususiyati?', 'a': [{'t': 'Tez, oddiy, concurrent dasturlash', 'c': True}, {'t': 'Faqat web dasturlash', 'c': False}, {'t': 'Faqat mobil dasturlash', 'c': False}, {'t': 'Faqat o\'yin dasturlash', 'c': False}]},
        {'t': 'Go qanday til?', 'a': [{'t': 'Kompilyatsiya qilinadigan, statik tipli', 'c': True}, {'t': 'Interpretatsiya qilinadigan', 'c': False}, {'t': 'Dinamik tipli', 'c': False}, {'t': 'Mashina tili', 'c': False}]},
        {'t': 'Go da garbage collection bormi?', 'a': [{'t': 'Ha, avtomatik xotira boshqaruvi bor', 'c': True}, {'t': 'Yo\'q, qo\'lda boshqarish kerak', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Go o\'rnatish va birinchi dastur', 't': 20, 'o': 2, 'q': [
        {'t': 'Go dasturini ishga tushirish buyrug\'i?', 'a': [{'t': 'go run main.go', 'c': True}, {'t': 'go start main.go', 'c': False}, {'t': 'go execute main.go', 'c': False}, {'t': 'run main.go', 'c': False}]},
        {'t': 'Go dasturini kompilyatsiya qilish?', 'a': [{'t': 'go build main.go', 'c': True}, {'t': 'go compile main.go', 'c': False}, {'t': 'go make main.go', 'c': False}, {'t': 'build main.go', 'c': False}]},
        {'t': 'Go dasturining kirish nuqtasi?', 'a': [{'t': 'main() funksiyasi', 'c': True}, {'t': 'start() funksiyasi', 'c': False}, {'t': 'begin() funksiyasi', 'c': False}, {'t': 'run() funksiyasi', 'c': False}]},
        {'t': 'Go dasturida package nima?', 'a': [{'t': 'Kodlarni guruhlash usuli', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Asosiy package nomi?', 'a': [{'t': 'main', 'c': True}, {'t': 'start', 'c': False}, {'t': 'begin', 'c': False}, {'t': 'app', 'c': False}]},
        {'t': 'fmt.Println() nima qiladi?', 'a': [{'t': 'Ekranga chiqaradi', 'c': True}, {'t': 'Faylga yozadi', 'c': False}, {'t': 'Kiritish qiladi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar va konstantalar', 't': 25, 'o': 3, 'q': [
        {'t': 'Go da o\'zgaruvchi e\'lon qilish usullari?', 'a': [{'t': 'var x int, x := 5', 'c': True}, {'t': 'Faqat var x int', 'c': False}, {'t': 'let x = 5', 'c': False}, {'t': 'int x = 5', 'c': False}]},
        {'t': 'var x int nima qiladi?', 'a': [{'t': 'int tipida x o\'zgaruvchisini e\'lon qiladi', 'c': True}, {'t': 'x ga qiymat beradi', 'c': False}, {'t': 'x ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'x := 5 nima?', 'a': [{'t': 'Qisqa e\'lon (tip avtomatik)', 'c': True}, {'t': 'Taqqoslash', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Konstanta', 'c': False}]},
        {'t': ':= qayerda ishlatiladi?', 'a': [{'t': 'Faqat funksiya ichida', 'c': True}, {'t': 'Hamma joyda', 'c': False}, {'t': 'Faqat global', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'const nima?', 'a': [{'t': 'O\'zgarmas qiymat', 'c': True}, {'t': 'O\'zgaruvchan qiymat', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'const x = 5; x = 10; to\'g\'rimi?', 'a': [{'t': 'Yo\'q, xato (const o\'zgarmas)', 'c': True}, {'t': 'Ha, to\'g\'ri', 'c': False}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Go da ishlatilmagan o\'zgaruvchi?', 'a': [{'t': 'Kompilyatsiya xatosi', 'c': True}, {'t': 'Ogohlantirish', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Avtomatik o\'chiriladi', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari - Asosiy turlar', 't': 25, 'o': 4, 'q': [
        {'t': 'Go da butun son turlari?', 'a': [{'t': 'int, int8, int16, int32, int64', 'c': True}, {'t': 'Faqat int', 'c': False}, {'t': 'integer, long', 'c': False}, {'t': 'number', 'c': False}]},
        {'t': 'Go da o\'nli son turlari?', 'a': [{'t': 'float32, float64', 'c': True}, {'t': 'float, double', 'c': False}, {'t': 'decimal', 'c': False}, {'t': 'real', 'c': False}]},
        {'t': 'Go da string turi?', 'a': [{'t': 'string', 'c': True}, {'t': 'str', 'c': False}, {'t': 'text', 'c': False}, {'t': 'char[]', 'c': False}]},
        {'t': 'Go da mantiqiy turi?', 'a': [{'t': 'bool', 'c': True}, {'t': 'boolean', 'c': False}, {'t': 'bit', 'c': False}, {'t': 'flag', 'c': False}]},
        {'t': 'bool qiymatlari?', 'a': [{'t': 'true, false', 'c': True}, {'t': '1, 0', 'c': False}, {'t': 'yes, no', 'c': False}, {'t': 'on, off', 'c': False}]},
        {'t': 'Go da byte nima?', 'a': [{'t': 'uint8 ning boshqa nomi', 'c': True}, {'t': 'Alohida tur', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Go da rune nima?', 'a': [{'t': 'int32 ning boshqa nomi (Unicode belgi)', 'c': True}, {'t': 'String', 'c': False}, {'t': 'Byte', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Stringlar bilan ishlash', 't': 25, 'o': 5, 'q': [
        {'t': 'Go da string yaratish?', 'a': [{'t': '"text" yoki `text`', 'c': True}, {'t': 'Faqat "text"', 'c': False}, {'t': '\'text\'', 'c': False}, {'t': 'String("text")', 'c': False}]},
        {'t': 'Backtick `text` nima?', 'a': [{'t': 'Raw string (escape ishlamaydi)', 'c': True}, {'t': 'Oddiy string', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Izoh', 'c': False}]},
        {'t': 'String qo\'shish?', 'a': [{'t': '"Hello" + " World"', 'c': True}, {'t': '"Hello".add(" World")', 'c': False}, {'t': 'concat("Hello", " World")', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'len("Hello") natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '4', 'c': False}, {'t': '6', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'String o\'zgaradimi?', 'a': [{'t': 'Yo\'q, immutable', 'c': True}, {'t': 'Ha, o\'zgaradi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'String indexlash: s[0] nima qaytaradi?', 'a': [{'t': 'Byte qiymat', 'c': True}, {'t': 'Belgi', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Operatorlar - Arifmetik', 't': 25, 'o': 6, 'q': [
        {'t': '10 + 5 natijasi?', 'a': [{'t': '15', 'c': True}, {'t': '105', 'c': False}, {'t': '5', 'c': False}, {'t': '50', 'c': False}]},
        {'t': '10 - 5 natijasi?', 'a': [{'t': '5', 'c': True}, {'t': '15', 'c': False}, {'t': '50', 'c': False}, {'t': '2', 'c': False}]},
        {'t': '10 * 5 natijasi?', 'a': [{'t': '50', 'c': True}, {'t': '15', 'c': False}, {'t': '5', 'c': False}, {'t': '2', 'c': False}]},
        {'t': '10 / 5 natijasi?', 'a': [{'t': '2', 'c': True}, {'t': '5', 'c': False}, {'t': '50', 'c': False}, {'t': '0', 'c': False}]},
        {'t': '10 % 3 natijasi?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': '10', 'c': False}]},
        {'t': '++ operatori nima qiladi?', 'a': [{'t': '1 ga oshiradi', 'c': True}, {'t': '1 ga kamaytiradi', 'c': False}, {'t': '2 ga ko\'paytiradi', 'c': False}, {'t': 'Qo\'shadi', 'c': False}]},
        {'t': 'Go da x++ ifoda sifatida ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat statement', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Taqqoslash va mantiqiy operatorlar', 't': 25, 'o': 7, 'q': [
        {'t': '5 == 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '1', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '5 != 3 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '2', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 > 5 natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '10 < 5 natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': '5', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'true && false natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '0', 'c': False}]},
        {'t': 'true || false natijasi?', 'a': [{'t': 'true', 'c': True}, {'t': 'false', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '1', 'c': False}]},
        {'t': '!true natijasi?', 'a': [{'t': 'false', 'c': True}, {'t': 'true', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': '0', 'c': False}]},
    ]},
    {'n': 'if operatori', 't': 25, 'o': 8, 'q': [
        {'t': 'if operatori nima uchun?', 'a': [{'t': 'Shartli bajarish', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'if x > 5 {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, () kerak', 'c': False}, {'t': 'Yo\'q, then kerak', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Go da if da () kerakmi?', 'a': [{'t': 'Yo\'q, kerak emas', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Go da if da {} kerakmi?', 'a': [{'t': 'Ha, majburiy', 'c': True}, {'t': 'Yo\'q, ixtiyoriy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'if x := 5; x > 3 {} to\'g\'rimi?', 'a': [{'t': 'Ha, if da o\'zgaruvchi e\'lon qilish mumkin', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'if-else va else if', 't': 25, 'o': 9, 'q': [
        {'t': 'else nima uchun?', 'a': [{'t': 'if sharti bajarilmasa', 'c': True}, {'t': 'Qo\'shimcha shart', 'c': False}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'else if nima?', 'a': [{'t': 'Qo\'shimcha shart', 'c': True}, {'t': 'else bilan bir xil', 'c': False}, {'t': 'if bilan bir xil', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'Go da ternary operator bormi?', 'a': [{'t': 'Yo\'q, faqat if-else', 'c': True}, {'t': 'Ha, bor', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Bir necha else if ishlatish mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat ikkita', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'else dan keyin if yozish to\'g\'rimi?', 'a': [{'t': 'Ha, else if', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'switch operatori', 't': 25, 'o': 10, 'q': [
        {'t': 'switch nima uchun?', 'a': [{'t': 'Ko\'p variantli tanlov', 'c': True}, {'t': 'Takrorlash', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Kiritish', 'c': False}]},
        {'t': 'Go da switch da break kerakmi?', 'a': [{'t': 'Yo\'q, avtomatik to\'xtaydi', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'fallthrough nima qiladi?', 'a': [{'t': 'Keyingi case ga o\'tadi', 'c': True}, {'t': 'To\'xtaydi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'default nima?', 'a': [{'t': 'Hech qaysi case mos kelmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'switch {} (ifoda yo\'q) to\'g\'rimi?', 'a': [{'t': 'Ha, if-else kabi ishlaydi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'switch da bir necha qiymat: case 1, 2, 3: to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'for sikli - Asoslar', 't': 25, 'o': 11, 'q': [
        {'t': 'Go da nechta sikl turi bor?', 'a': [{'t': 'Faqat for (while yo\'q)', 'c': True}, {'t': 'for, while, do-while', 'c': False}, {'t': 'for, foreach', 'c': False}, {'t': 'Ko\'p turlar', 'c': False}]},
        {'t': 'for i := 0; i < 5; i++ {} necha marta?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': 'for {} nima qiladi?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for condition {} nima?', 'a': [{'t': 'while kabi ishlaydi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Bir marta ishlaydi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da break nima qiladi?', 'a': [{'t': 'Siklni to\'xtatadi', 'c': True}, {'t': 'Keyingi iteratsiyaga o\'tadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'for da continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'for range sikli', 't': 25, 'o': 12, 'q': [
        {'t': 'for range nima uchun?', 'a': [{'t': 'Massiv, slice, map aylanish', 'c': True}, {'t': 'Oddiy sikl', 'c': False}, {'t': 'Shart tekshirish', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'for i, v := range arr {} da i va v nima?', 'a': [{'t': 'i - indeks, v - qiymat', 'c': True}, {'t': 'i - qiymat, v - indeks', 'c': False}, {'t': 'Ikkalasi ham indeks', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for _, v := range arr {} da _ nima?', 'a': [{'t': 'Indeksni e\'tiborsiz qoldirish', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Maxsus o\'zgaruvchi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'for i := range arr {} nima qaytaradi?', 'a': [{'t': 'Faqat indeks', 'c': True}, {'t': 'Faqat qiymat', 'c': False}, {'t': 'Indeks va qiymat', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for range string da nima qaytaradi?', 'a': [{'t': 'Indeks va rune (Unicode belgi)', 'c': True}, {'t': 'Indeks va byte', 'c': False}, {'t': 'Faqat belgi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Massivlar (Arrays)', 't': 25, 'o': 13, 'q': [
        {'t': 'Go da massiv nima?', 'a': [{'t': 'O\'zgarmas o\'lchamli elementlar to\'plami', 'c': True}, {'t': 'Dinamik o\'lchamli to\'plam', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'var arr [5]int to\'g\'rimi?', 'a': [{'t': 'Ha, 5 ta int massiv', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'arr := [3]int{1, 2, 3} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Massiv indeksi qayerdan boshlanadi?', 'a': [{'t': '0 dan', 'c': True}, {'t': '1 dan', 'c': False}, {'t': '-1 dan', 'c': False}, {'t': 'Istalgan sondan', 'c': False}]},
        {'t': 'len(arr) nima qaytaradi?', 'a': [{'t': 'Massiv uzunligi', 'c': True}, {'t': 'Massiv qiymati', 'c': False}, {'t': 'Massiv turi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Massiv o\'lchamini o\'zgartirish mumkinmi?', 'a': [{'t': 'Yo\'q, o\'zgarmas', 'c': True}, {'t': 'Ha, dinamik', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Slicelar', 't': 25, 'o': 14, 'q': [
        {'t': 'Slice nima?', 'a': [{'t': 'Dinamik o\'lchamli massiv', 'c': True}, {'t': 'O\'zgarmas o\'lchamli massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'var s []int to\'g\'rimi?', 'a': [{'t': 'Ha, int slice', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 's := []int{1, 2, 3} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'append(s, 4) nima qiladi?', 'a': [{'t': 'Slice ga element qo\'shadi', 'c': True}, {'t': 'Element o\'chiradi', 'c': False}, {'t': 'Slice ni tozalaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'make([]int, 5) nima yaratadi?', 'a': [{'t': '5 ta element bilan slice', 'c': True}, {'t': '5 ta element bilan massiv', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 's[1:3] nima?', 'a': [{'t': '1 dan 3 gacha (3 kirmaydi) qism', 'c': True}, {'t': '1 va 3 elementlar', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'cap(s) nima qaytaradi?', 'a': [{'t': 'Slice sig\'imi (capacity)', 'c': True}, {'t': 'Slice uzunligi', 'c': False}, {'t': 'Slice qiymati', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Maplar (Lug\'atlar)', 't': 25, 'o': 15, 'q': [
        {'t': 'Map nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'var m map[string]int to\'g\'rimi?', 'a': [{'t': 'Ha, string kalit, int qiymat', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'm := make(map[string]int) to\'g\'rimi?', 'a': [{'t': 'Ha, bo\'sh map yaratadi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'm["key"] = 10 nima qiladi?', 'a': [{'t': 'Kalit-qiymat qo\'shadi', 'c': True}, {'t': 'Kalitni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'delete(m, "key") nima qiladi?', 'a': [{'t': 'Kalitni o\'chiradi', 'c': True}, {'t': 'Kalit qo\'shadi', 'c': False}, {'t': 'Map ni tozalaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v, ok := m["key"] da ok nima?', 'a': [{'t': 'Kalit mavjudligini tekshiradi', 'c': True}, {'t': 'Qiymat', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Funksiyalar - Asoslar', 't': 25, 'o': 16, 'q': [
        {'t': 'Funksiya nima?', 'a': [{'t': 'Qayta ishlatish mumkin bo\'lgan kod bloki', 'c': True}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Sikl', 'c': False}]},
        {'t': 'func myFunc() {} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'func add(x int, y int) int {} to\'g\'rimi?', 'a': [{'t': 'Ha, 2 parametr, int qaytaradi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'func add(x, y int) int {} to\'g\'rimi?', 'a': [{'t': 'Ha, qisqa yozuv', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Funksiyadan qiymat qaytarish uchun?', 'a': [{'t': 'return kalit so\'zi', 'c': True}, {'t': 'send kalit so\'zi', 'c': False}, {'t': 'give kalit so\'zi', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'Go da funksiya necha qiymat qaytarishi mumkin?', 'a': [{'t': 'Bir necha qiymat', 'c': True}, {'t': 'Faqat bitta', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ko\'p qiymat qaytarish', 't': 25, 'o': 17, 'q': [
        {'t': 'func swap(x, y int) (int, int) {} to\'g\'rimi?', 'a': [{'t': 'Ha, 2 ta qiymat qaytaradi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'a, b := swap(1, 2) to\'g\'rimi?', 'a': [{'t': 'Ha, 2 ta qiymat oladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'a, _ := swap(1, 2) nima qiladi?', 'a': [{'t': 'Ikkinchi qiymatni e\'tiborsiz qoldiradi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Birinchi qiymatni e\'tiborsiz qoldiradi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Named return values: func f() (x int) {} to\'g\'rimi?', 'a': [{'t': 'Ha, nomli qaytish qiymati', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Named return da return yozish kerakmi?', 'a': [{'t': 'Ha, lekin qiymat yo\'q (naked return)', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Variadic funksiyalar', 't': 25, 'o': 18, 'q': [
        {'t': 'Variadic funksiya nima?', 'a': [{'t': 'Istalgan sondagi parametr qabul qiladi', 'c': True}, {'t': 'Faqat bitta parametr', 'c': False}, {'t': 'Parametrsiz funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'func sum(nums ...int) {} to\'g\'rimi?', 'a': [{'t': 'Ha, variadic funksiya', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Variadic parametr qayerda bo\'lishi kerak?', 'a': [{'t': 'Oxirida', 'c': True}, {'t': 'Boshida', 'c': False}, {'t': 'Istalgan joyda', 'c': False}, {'t': 'O\'rtada', 'c': False}]},
        {'t': 'sum(1, 2, 3, 4) to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'nums ...int ichida nums nima?', 'a': [{'t': 'Slice', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'Map', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Anonymous va Higher-order funksiyalar', 't': 25, 'o': 19, 'q': [
        {'t': 'Anonymous funksiya nima?', 'a': [{'t': 'Nomsiz funksiya', 'c': True}, {'t': 'Nomli funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'f := func() {} to\'g\'rimi?', 'a': [{'t': 'Ha, anonymous funksiya', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'func() { fmt.Println("Hi") }() to\'g\'rimi?', 'a': [{'t': 'Ha, darhol chaqiriladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Higher-order funksiya nima?', 'a': [{'t': 'Funksiyani parametr sifatida oladi yoki qaytaradi', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'func apply(f func(int) int, x int) int {} to\'g\'rimi?', 'a': [{'t': 'Ha, funksiyani parametr sifatida oladi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Closures', 't': 25, 'o': 20, 'q': [
        {'t': 'Closure nima?', 'a': [{'t': 'Tashqi o\'zgaruvchilarga murojaat qiladigan funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure tashqi o\'zgaruvchini eslab qoladimi?', 'a': [{'t': 'Ha, eslab qoladi', 'c': True}, {'t': 'Yo\'q, unutadi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'func counter() func() int {} closure qaytaradimi?', 'a': [{'t': 'Ha, funksiya qaytaradi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure da o\'zgaruvchi o\'zgarishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure qachon foydali?', 'a': [{'t': 'Holat saqlash kerak bo\'lganda', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat oddiy funksiyalarda', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Pointerlar', 't': 25, 'o': 21, 'q': [
        {'t': 'Pointer nima?', 'a': [{'t': 'Xotira manzilini saqlaydigan o\'zgaruvchi', 'c': True}, {'t': 'Oddiy o\'zgaruvchi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'var p *int to\'g\'rimi?', 'a': [{'t': 'Ha, int ga pointer', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '& operatori nima qiladi?', 'a': [{'t': 'Manzilni oladi', 'c': True}, {'t': 'Qiymatni oladi', 'c': False}, {'t': 'Qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '* operatori nima qiladi?', 'a': [{'t': 'Pointer orqali qiymatni oladi (dereference)', 'c': True}, {'t': 'Manzilni oladi', 'c': False}, {'t': 'Ko\'paytiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'p := &x nima qiladi?', 'a': [{'t': 'x ning manzilini p ga beradi', 'c': True}, {'t': 'x ning qiymatini p ga beradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '*p = 10 nima qiladi?', 'a': [{'t': 'p ko\'rsatgan o\'zgaruvchiga 10 beradi', 'c': True}, {'t': 'p ga 10 beradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Go da nil pointer xavflimi?', 'a': [{'t': 'Ha, panic beradi', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Structlar', 't': 25, 'o': 22, 'q': [
        {'t': 'Struct nima?', 'a': [{'t': 'Turli turlarni birlashtiruvchi tur', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'type Person struct { Name string } to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'p := Person{Name: "Ali"} to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'p.Name ga qanday murojaat qilish mumkin?', 'a': [{'t': 'Nuqta orqali', 'c': True}, {'t': 'Kvadrat qavs orqali', 'c': False}, {'t': 'Arrow orqali', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Struct fieldlari katta harf bilan boshlanishi kerakmi?', 'a': [{'t': 'Export qilish uchun kerak', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Anonymous struct yaratish mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Metodlar', 't': 25, 'o': 23, 'q': [
        {'t': 'Metod nima?', 'a': [{'t': 'Receiver bilan funksiya', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'func (p Person) Greet() {} to\'g\'rimi?', 'a': [{'t': 'Ha, Person uchun metod', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Receiver nima?', 'a': [{'t': 'Metod qaysi turga tegishli', 'c': True}, {'t': 'Parametr', 'c': False}, {'t': 'Qaytish qiymati', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Value receiver va pointer receiver farqi?', 'a': [{'t': 'Pointer o\'zgartiradi, value nusxa oladi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Value tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'func (p *Person) SetName(n string) {} nima?', 'a': [{'t': 'Pointer receiver metod', 'c': True}, {'t': 'Value receiver metod', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Metodni chaqirish?', 'a': [{'t': 'p.Greet()', 'c': True}, {'t': 'Greet(p)', 'c': False}, {'t': 'p->Greet()', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Interfacelar', 't': 25, 'o': 24, 'q': [
        {'t': 'Interface nima?', 'a': [{'t': 'Metodlar to\'plami', 'c': True}, {'t': 'Struct', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'type Writer interface { Write() } to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Interface qanday implement qilinadi?', 'a': [{'t': 'Avtomatik (metodlar mavjud bo\'lsa)', 'c': True}, {'t': 'implements kalit so\'zi bilan', 'c': False}, {'t': 'extends kalit so\'zi bilan', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Bo\'sh interface: interface{} nima?', 'a': [{'t': 'Har qanday turni qabul qiladi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa qabul qilmaydi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'any nima? (Go 1.18+)', 'a': [{'t': 'interface{} ning boshqa nomi', 'c': True}, {'t': 'Yangi tur', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Type assertion: v.(string) nima?', 'a': [{'t': 'Interface qiymatini string ga aylantirish', 'c': True}, {'t': 'String yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Xatolar bilan ishlash (Errors)', 't': 25, 'o': 25, 'q': [
        {'t': 'Go da xatolar qanday qaytariladi?', 'a': [{'t': 'error turi orqali', 'c': True}, {'t': 'Exception orqali', 'c': False}, {'t': 'Try-catch orqali', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'error nima?', 'a': [{'t': 'Interface turi', 'c': True}, {'t': 'Struct', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'errors.New("xato") nima qiladi?', 'a': [{'t': 'Yangi xato yaratadi', 'c': True}, {'t': 'Xatoni o\'chiradi', 'c': False}, {'t': 'Xatoni chiqaradi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'if err != nil {} nima tekshiradi?', 'a': [{'t': 'Xato bor-yo\'qligini', 'c': True}, {'t': 'Qiymat bor-yo\'qligini', 'c': False}, {'t': 'Funksiya ishladi-yo\'qligini', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'fmt.Errorf("xato: %v", err) nima qiladi?', 'a': [{'t': 'Formatlangan xato yaratadi', 'c': True}, {'t': 'Xatoni chiqaradi', 'c': False}, {'t': 'Xatoni o\'chiradi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Go da try-catch bormi?', 'a': [{'t': 'Yo\'q, faqat error qaytarish', 'c': True}, {'t': 'Ha, bor', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Panic va Recover', 't': 25, 'o': 26, 'q': [
        {'t': 'panic() nima qiladi?', 'a': [{'t': 'Dasturni to\'xtatadi', 'c': True}, {'t': 'Xato qaytaradi', 'c': False}, {'t': 'Davom etadi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'panic qachon ishlatiladi?', 'a': [{'t': 'Jiddiy xatolarda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Oddiy xatolarda', 'c': False}]},
        {'t': 'recover() nima qiladi?', 'a': [{'t': 'panic dan qaytaradi', 'c': True}, {'t': 'panic yaratadi', 'c': False}, {'t': 'Xato qaytaradi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'recover() qayerda ishlaydi?', 'a': [{'t': 'Faqat defer ichida', 'c': True}, {'t': 'Hamma joyda', 'c': False}, {'t': 'Faqat main da', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'defer nima qiladi?', 'a': [{'t': 'Funksiya oxirida bajaradi', 'c': True}, {'t': 'Darhol bajaradi', 'c': False}, {'t': 'Hech qachon bajarilmaydi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'defer f() qachon bajariladi?', 'a': [{'t': 'Funksiya return qilganda', 'c': True}, {'t': 'Darhol', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Goroutinelar', 't': 25, 'o': 27, 'q': [
        {'t': 'Goroutine nima?', 'a': [{'t': 'Yengil thread (concurrent bajarish)', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
        {'t': 'go f() nima qiladi?', 'a': [{'t': 'f ni yangi goroutine da ishga tushiradi', 'c': True}, {'t': 'f ni oddiy chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Goroutine qachon tugaydi?', 'a': [{'t': 'Funksiya tugaganda', 'c': True}, {'t': 'Dastur tugaganda', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'main() tugasa goroutinelar nima bo\'ladi?', 'a': [{'t': 'Hammasi to\'xtaydi', 'c': True}, {'t': 'Davom etadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Goroutine thread dan farqi?', 'a': [{'t': 'Yengilroq, ko\'proq yaratish mumkin', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Thread yengilroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Nechta goroutine yaratish mumkin?', 'a': [{'t': 'Minglab, hatto millionlab', 'c': True}, {'t': 'Faqat 10 ta', 'c': False}, {'t': 'Faqat 100 ta', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Channellar', 't': 25, 'o': 28, 'q': [
        {'t': 'Channel nima?', 'a': [{'t': 'Goroutinelar orasida ma\'lumot uzatish', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'ch := make(chan int) to\'g\'rimi?', 'a': [{'t': 'Ha, int channel yaratadi', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'ch <- 5 nima qiladi?', 'a': [{'t': 'Channel ga 5 yuboradi', 'c': True}, {'t': 'Channel dan oladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'v := <-ch nima qiladi?', 'a': [{'t': 'Channel dan qiymat oladi', 'c': True}, {'t': 'Channel ga yuboradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'close(ch) nima qiladi?', 'a': [{'t': 'Channel ni yopadi', 'c': True}, {'t': 'Channel ni ochadi', 'c': False}, {'t': 'Channel ni tozalaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Buffered channel: make(chan int, 5) nima?', 'a': [{'t': '5 ta qiymat sig\'adigan channel', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': '5 ta channel', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Select operatori', 't': 25, 'o': 29, 'q': [
        {'t': 'select nima uchun?', 'a': [{'t': 'Bir necha channel bilan ishlash', 'c': True}, {'t': 'Oddiy tanlov', 'c': False}, {'t': 'Sikl', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'select {} switch ga o\'xshaydimi?', 'a': [{'t': 'Ha, lekin channellar uchun', 'c': True}, {'t': 'Yo\'q, butunlay boshqa', 'c': False}, {'t': 'Bir xil', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'select da case <-ch1: nima?', 'a': [{'t': 'ch1 dan qiymat kelsa', 'c': True}, {'t': 'ch1 ga yuborsa', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'select da default nima?', 'a': [{'t': 'Hech qaysi channel tayyor bo\'lmasa', 'c': True}, {'t': 'Birinchi case', 'c': False}, {'t': 'Oxirgi case', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'select bloklash mumkinmi?', 'a': [{'t': 'Ha, default bo\'lmasa', 'c': True}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'select bir necha case tayyor bo\'lsa?', 'a': [{'t': 'Tasodifiy birini tanlaydi', 'c': True}, {'t': 'Birinchisini tanlaydi', 'c': False}, {'t': 'Hammasini bajaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Packagelar va Modullar', 't': 25, 'o': 30, 'q': [
        {'t': 'Package nima?', 'a': [{'t': 'Kodlarni guruhlash usuli', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'import "fmt" nima qiladi?', 'a': [{'t': 'fmt packageni import qiladi', 'c': True}, {'t': 'fmt ni yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Katta harf bilan boshlanadigan nom nima?', 'a': [{'t': 'Exported (tashqaridan ko\'rinadi)', 'c': True}, {'t': 'Private', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Kichik harf bilan boshlanadigan nom nima?', 'a': [{'t': 'Unexported (faqat package ichida)', 'c': True}, {'t': 'Public', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'go mod init nima qiladi?', 'a': [{'t': 'Yangi modul yaratadi', 'c': True}, {'t': 'Modulni o\'chiradi', 'c': False}, {'t': 'Modulni yangilaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'go.mod fayl nima?', 'a': [{'t': 'Modul va dependencylar haqida ma\'lumot', 'c': True}, {'t': 'Asosiy kod fayli', 'c': False}, {'t': 'Test fayli', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'go get nima qiladi?', 'a': [{'t': 'Package yuklab oladi', 'c': True}, {'t': 'Package o\'chiradi', 'c': False}, {'t': 'Dasturni ishga tushiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_go()
    print(f"\n📚 {subj.name} faniga 30 ta mavzu qo'shilmoqda...\n")
    add_topics(subj, T)
    print(f"\n✅ Jami {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
    print(f"📊 Har bir mavzuda 5-10 ta test bor")
    print(f"🎯 Testlar to'g'ri javoblari har xil pozitsiyalarda")
