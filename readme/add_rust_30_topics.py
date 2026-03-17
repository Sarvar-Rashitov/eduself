"""
RUST DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_rust():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Rust', defaults={'category': cat, 'description': 'Rust dasturlash tili - xavfsiz va tez dasturlash', 'icon': 'bi-gear-fill', 'order': 7, 'is_active': True})
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
    {'n': 'Rust dasturlashga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Rust dasturlash tili qachon yaratilgan?', 'a': [{'t': '2010 yilda', 'c': True}, {'t': '2015 yilda', 'c': False}, {'t': '2005 yilda', 'c': False}, {'t': '2020 yilda', 'c': False}]},
        {'t': 'Rust tilini kim yaratgan?', 'a': [{'t': 'Graydon Hoare', 'c': True}, {'t': 'Linus Torvalds', 'c': False}, {'t': 'Bjarne Stroustrup', 'c': False}, {'t': 'Dennis Ritchie', 'c': False}]},
        {'t': 'Rust ning asosiy afzalligi nima?', 'a': [{'t': 'Xotira xavfsizligi va tezlik', 'c': True}, {'t': 'Faqat tezlik', 'c': False}, {'t': 'Faqat soddalik', 'c': False}, {'t': 'Faqat portativlik', 'c': False}]},
        {'t': 'Rust fayl kengaytmasi?', 'a': [{'t': '.rs', 'c': True}, {'t': '.rust', 'c': False}, {'t': '.r', 'c': False}, {'t': '.rt', 'c': False}]},
        {'t': 'Rust qanday til?', 'a': [{'t': 'Kompilyatsiya qilinadigan, statik tipli', 'c': True}, {'t': 'Interpretatsiya qilinadigan', 'c': False}, {'t': 'Dinamik tipli', 'c': False}, {'t': 'Skript tili', 'c': False}]},
        {'t': 'Rust da garbage collector bormi?', 'a': [{'t': 'Yo\'q, ownership tizimi bor', 'c': True}, {'t': 'Ha, bor', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Rust o\'rnatish va birinchi dastur', 't': 20, 'o': 2, 'q': [
        {'t': 'Rust ni qanday o\'rnatish mumkin?', 'a': [{'t': 'rustup orqali', 'c': True}, {'t': 'npm orqali', 'c': False}, {'t': 'pip orqali', 'c': False}, {'t': 'apt orqali', 'c': False}]},
        {'t': 'Rust kompilyatori nomi?', 'a': [{'t': 'rustc', 'c': True}, {'t': 'gcc', 'c': False}, {'t': 'clang', 'c': False}, {'t': 'rust', 'c': False}]},
        {'t': 'Rust paket menejeri nomi?', 'a': [{'t': 'cargo', 'c': True}, {'t': 'npm', 'c': False}, {'t': 'pip', 'c': False}, {'t': 'gem', 'c': False}]},
        {'t': 'Yangi Rust loyihasi yaratish?', 'a': [{'t': 'cargo new project_name', 'c': True}, {'t': 'rustc new project_name', 'c': False}, {'t': 'rust init project_name', 'c': False}, {'t': 'cargo init project_name', 'c': False}]},
        {'t': 'Rust dasturini ishga tushirish?', 'a': [{'t': 'cargo run', 'c': True}, {'t': 'rust run', 'c': False}, {'t': 'rustc run', 'c': False}, {'t': 'cargo start', 'c': False}]},
        {'t': 'println! nima?', 'a': [{'t': 'Ekranga chiqarish makrosi', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'fn main() {} nima?', 'a': [{'t': 'Asosiy funksiya (kirish nuqtasi)', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Makros', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}]},
    ]},
    {'n': 'O\'zgaruvchilar va o\'zgarmaslik', 't': 25, 'o': 3, 'q': [
        {'t': 'Rust da o\'zgaruvchi qanday e\'lon qilinadi?', 'a': [{'t': 'let x = 5;', 'c': True}, {'t': 'var x = 5;', 'c': False}, {'t': 'int x = 5;', 'c': False}, {'t': 'x = 5;', 'c': False}]},
        {'t': 'Rust da o\'zgaruvchilar default holatda?', 'a': [{'t': 'O\'zgarmas (immutable)', 'c': True}, {'t': 'O\'zgaruvchan (mutable)', 'c': False}, {'t': 'Ikkalasi ham', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'O\'zgaruvchan o\'zgaruvchi qanday yaratiladi?', 'a': [{'t': 'let mut x = 5;', 'c': True}, {'t': 'let x = 5;', 'c': False}, {'t': 'var x = 5;', 'c': False}, {'t': 'mutable x = 5;', 'c': False}]},
        {'t': 'let x = 5; x = 10; to\'g\'rimi?', 'a': [{'t': 'Yo\'q, xato (x immutable)', 'c': True}, {'t': 'Ha, to\'g\'ri', 'c': False}, {'t': 'Ba\'zan to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Shadowing nima?', 'a': [{'t': 'O\'zgaruvchini qayta e\'lon qilish', 'c': True}, {'t': 'O\'zgaruvchini o\'chirish', 'c': False}, {'t': 'O\'zgaruvchini nusxalash', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'let x = 5; let x = 10; to\'g\'rimi?', 'a': [{'t': 'Ha, shadowing', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Ma\'lumot turlari - Skalar turlar', 't': 25, 'o': 4, 'q': [
        {'t': 'Rust da nechta skalar tur bor?', 'a': [{'t': '4 ta (integer, float, boolean, char)', 'c': True}, {'t': '3 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '2 ta', 'c': False}]},
        {'t': 'i32 nima?', 'a': [{'t': '32-bitli signed integer', 'c': True}, {'t': '32-bitli unsigned integer', 'c': False}, {'t': '32-bitli float', 'c': False}, {'t': 'String', 'c': False}]},
        {'t': 'u32 nima?', 'a': [{'t': '32-bitli unsigned integer', 'c': True}, {'t': '32-bitli signed integer', 'c': False}, {'t': '32-bitli float', 'c': False}, {'t': 'Boolean', 'c': False}]},
        {'t': 'f64 nima?', 'a': [{'t': '64-bitli float', 'c': True}, {'t': '64-bitli integer', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Boolean', 'c': False}]},
        {'t': 'bool turi qanday qiymatlar oladi?', 'a': [{'t': 'true yoki false', 'c': True}, {'t': '0 yoki 1', 'c': False}, {'t': 'yes yoki no', 'c': False}, {'t': 'Istalgan qiymat', 'c': False}]},
        {'t': 'char turi nima?', 'a': [{'t': 'Unicode belgi', 'c': True}, {'t': 'ASCII belgi', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Integer', 'c': False}]},
        {'t': 'let x: i32 = 5; da :i32 nima?', 'a': [{'t': 'Tur annotatsiyasi', 'c': True}, {'t': 'Qiymat', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Murakkab ma\'lumot turlari', 't': 25, 'o': 5, 'q': [
        {'t': 'Tuple nima?', 'a': [{'t': 'Turli turlarni birlashtiruvchi tur', 'c': True}, {'t': 'Faqat bir xil turlar', 'c': False}, {'t': 'Dinamik o\'lchamli', 'c': False}, {'t': 'String', 'c': False}]},
        {'t': 'let tup = (1, 2.5, "hi"); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Tuple elementiga qanday kirish mumkin?', 'a': [{'t': 'tup.0, tup.1, ...', 'c': True}, {'t': 'tup[0], tup[1], ...', 'c': False}, {'t': 'tup(0), tup(1), ...', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'Array nima?', 'a': [{'t': 'Bir xil turli, fix o\'lchamli to\'plam', 'c': True}, {'t': 'Turli turli elementlar', 'c': False}, {'t': 'Dinamik o\'lchamli', 'c': False}, {'t': 'String', 'c': False}]},
        {'t': 'let arr = [1, 2, 3]; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Array elementiga qanday kirish mumkin?', 'a': [{'t': 'arr[0], arr[1], ...', 'c': True}, {'t': 'arr.0, arr.1, ...', 'c': False}, {'t': 'arr(0), arr(1), ...', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'let arr: [i32; 3] = [1, 2, 3]; da ;3 nima?', 'a': [{'t': 'Array o\'lchami', 'c': True}, {'t': 'Qiymat', 'c': False}, {'t': 'Tur', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Funksiyalar', 't': 25, 'o': 6, 'q': [
        {'t': 'Rust da funksiya qanday e\'lon qilinadi?', 'a': [{'t': 'fn function_name() {}', 'c': True}, {'t': 'function function_name() {}', 'c': False}, {'t': 'def function_name() {}', 'c': False}, {'t': 'func function_name() {}', 'c': False}]},
        {'t': 'fn add(x: i32, y: i32) -> i32 { x + y } to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '-> i32 nima?', 'a': [{'t': 'Qaytish turi', 'c': True}, {'t': 'Parametr turi', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiyadan qiymat qaytarish uchun?', 'a': [{'t': 'Oxirgi ifoda (;siz) yoki return', 'c': True}, {'t': 'Faqat return', 'c': False}, {'t': 'Faqat oxirgi ifoda', 'c': False}, {'t': 'Avtomatik', 'c': False}]},
        {'t': 'fn test() { 5 } va fn test() { 5; } farqi?', 'a': [{'t': 'Birinchisi 5 qaytaradi, ikkinchisi ()', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Ikkalasi ham 5 qaytaradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Funksiya parametrlarida tur ko\'rsatish majburiyatmi?', 'a': [{'t': 'Ha, majburiy', 'c': True}, {'t': 'Yo\'q, ixtiyoriy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Izohlar va kod formatlash', 't': 20, 'o': 7, 'q': [
        {'t': 'Rust da izoh qanday yoziladi?', 'a': [{'t': '// yoki /* */', 'c': True}, {'t': 'Faqat //', 'c': False}, {'t': '# belgisi bilan', 'c': False}, {'t': '\'\'\' bilan', 'c': False}]},
        {'t': 'Dokumentatsiya izohi qanday?', 'a': [{'t': '/// yoki //!', 'c': True}, {'t': 'Faqat //', 'c': False}, {'t': '/** */', 'c': False}, {'t': '# belgisi bilan', 'c': False}]},
        {'t': 'cargo fmt nima qiladi?', 'a': [{'t': 'Kodni formatlaydi', 'c': True}, {'t': 'Kodni kompilyatsiya qiladi', 'c': False}, {'t': 'Testlarni ishga tushiradi', 'c': False}, {'t': 'Xatoliklarni topadi', 'c': False}]},
        {'t': 'cargo clippy nima qiladi?', 'a': [{'t': 'Kod sifatini tekshiradi (linter)', 'c': True}, {'t': 'Kodni formatlaydi', 'c': False}, {'t': 'Kodni kompilyatsiya qiladi', 'c': False}, {'t': 'Testlarni ishga tushiradi', 'c': False}]},
        {'t': 'Rust da snake_case qayerda ishlatiladi?', 'a': [{'t': 'Funksiya va o\'zgaruvchi nomlari', 'c': True}, {'t': 'Tur nomlari', 'c': False}, {'t': 'Konstantalar', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
    ]},
    {'n': 'Boshqaruv oqimi - if', 't': 25, 'o': 8, 'q': [
        {'t': 'if operatori Rust da qanday?', 'a': [{'t': 'if condition { }', 'c': True}, {'t': 'if (condition) { }', 'c': False}, {'t': 'if condition then', 'c': False}, {'t': 'if: condition', 'c': False}]},
        {'t': 'if x > 5 { } da () kerakmi?', 'a': [{'t': 'Yo\'q, kerak emas', 'c': True}, {'t': 'Ha, kerak', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'if ifodasi qiymat qaytaradimi?', 'a': [{'t': 'Ha, qaytaradi', 'c': True}, {'t': 'Yo\'q, qaytarmaydi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'let x = if true { 5 } else { 10 }; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'if shartida faqat bool bo\'lishi kerakmi?', 'a': [{'t': 'Ha, faqat bool', 'c': True}, {'t': 'Yo\'q, istalgan tur', 'c': False}, {'t': 'Integer ham bo\'ladi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'else if qanday ishlatiladi?', 'a': [{'t': 'else if condition { }', 'c': True}, {'t': 'elif condition { }', 'c': False}, {'t': 'elseif condition { }', 'c': False}, {'t': 'else: if condition { }', 'c': False}]},
    ]},
    {'n': 'Boshqaruv oqimi - loop va while', 't': 25, 'o': 9, 'q': [
        {'t': 'loop nima?', 'a': [{'t': 'Cheksiz sikl', 'c': True}, {'t': 'Bir marta bajarish', 'c': False}, {'t': 'Shart bilan sikl', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'loop dan qanday chiqish mumkin?', 'a': [{'t': 'break', 'c': True}, {'t': 'stop', 'c': False}, {'t': 'exit', 'c': False}, {'t': 'end', 'c': False}]},
        {'t': 'loop { break 5; } nima qaytaradi?', 'a': [{'t': '5', 'c': True}, {'t': 'Hech narsa', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'true', 'c': False}]},
        {'t': 'while sikli qanday?', 'a': [{'t': 'while condition { }', 'c': True}, {'t': 'while (condition) { }', 'c': False}, {'t': 'while: condition', 'c': False}, {'t': 'while condition do', 'c': False}]},
        {'t': 'continue nima qiladi?', 'a': [{'t': 'Keyingi iteratsiyaga o\'tadi', 'c': True}, {'t': 'Siklni to\'xtatadi', 'c': False}, {'t': 'Funksiyadan chiqadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Sikl labelini qanday qo\'yish mumkin?', 'a': [{'t': '\'label: loop { }', 'c': True}, {'t': 'label: loop { }', 'c': False}, {'t': '@label loop { }', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
    ]},
    {'n': 'Boshqaruv oqimi - for', 't': 25, 'o': 10, 'q': [
        {'t': 'for sikli qanday?', 'a': [{'t': 'for item in collection { }', 'c': True}, {'t': 'for (item in collection) { }', 'c': False}, {'t': 'for item: collection { }', 'c': False}, {'t': 'for (i=0; i<10; i++) { }', 'c': False}]},
        {'t': 'for i in 0..5 necha marta ishlaydi?', 'a': [{'t': '5 marta (0 dan 4 gacha)', 'c': True}, {'t': '4 marta', 'c': False}, {'t': '6 marta', 'c': False}, {'t': '1 marta', 'c': False}]},
        {'t': '0..5 nima?', 'a': [{'t': 'Range (0 dan 4 gacha)', 'c': True}, {'t': 'Array', 'c': False}, {'t': 'Tuple', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': '0..=5 nima?', 'a': [{'t': 'Inclusive range (0 dan 5 gacha)', 'c': True}, {'t': 'Exclusive range', 'c': False}, {'t': 'Array', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'for i in (0..5).rev() nima qiladi?', 'a': [{'t': 'Teskari tartibda (4 dan 0 gacha)', 'c': True}, {'t': 'To\'g\'ri tartibda', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},
    {'n': 'Ownership (Egalik) - Asoslar', 't': 25, 'o': 11, 'q': [
        {'t': 'Ownership nima?', 'a': [{'t': 'Rust ning xotira boshqaruv tizimi', 'c': True}, {'t': 'O\'zgaruvchi turi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Har bir qiymatning nechta egasi bo\'ladi?', 'a': [{'t': 'Faqat bitta', 'c': True}, {'t': 'Ko\'p', 'c': False}, {'t': 'Nol', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'Ega scope dan chiqsa nima bo\'ladi?', 'a': [{'t': 'Qiymat o\'chiriladi (drop)', 'c': True}, {'t': 'Hech narsa', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'let s1 = String::from("hi"); let s2 = s1; dan keyin s1 ishlatish mumkinmi?', 'a': [{'t': 'Yo\'q, s1 move bo\'lgan', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Move nima?', 'a': [{'t': 'Egalikni o\'tkazish', 'c': True}, {'t': 'Nusxalash', 'c': False}, {'t': 'O\'chirish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Stack da saqlanadigan turlar move bo\'ladimi?', 'a': [{'t': 'Yo\'q, copy bo\'ladi', 'c': True}, {'t': 'Ha, move bo\'ladi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'References va Borrowing', 't': 25, 'o': 12, 'q': [
        {'t': 'Reference nima?', 'a': [{'t': 'Qiymatga havola (egalikni olmaydi)', 'c': True}, {'t': 'Egalikni oladi', 'c': False}, {'t': 'Nusxalaydi', 'c': False}, {'t': 'O\'chiradi', 'c': False}]},
        {'t': 'Reference qanday yaratiladi?', 'a': [{'t': '&x', 'c': True}, {'t': '*x', 'c': False}, {'t': 'ref x', 'c': False}, {'t': 'x&', 'c': False}]},
        {'t': 'Borrowing nima?', 'a': [{'t': 'Reference orqali qiymatdan foydalanish', 'c': True}, {'t': 'Egalikni olish', 'c': False}, {'t': 'Nusxalash', 'c': False}, {'t': 'O\'chirish', 'c': False}]},
        {'t': 'Immutable reference qanday?', 'a': [{'t': '&x', 'c': True}, {'t': '&mut x', 'c': False}, {'t': '*x', 'c': False}, {'t': 'ref x', 'c': False}]},
        {'t': 'Mutable reference qanday?', 'a': [{'t': '&mut x', 'c': True}, {'t': '&x', 'c': False}, {'t': '*mut x', 'c': False}, {'t': 'mut &x', 'c': False}]},
        {'t': 'Bir vaqtda nechta mutable reference bo\'lishi mumkin?', 'a': [{'t': 'Faqat bitta', 'c': True}, {'t': 'Ko\'p', 'c': False}, {'t': 'Cheksiz', 'c': False}, {'t': 'Nol', 'c': False}]},
        {'t': 'Immutable va mutable reference bir vaqtda bo\'lishi mumkinmi?', 'a': [{'t': 'Yo\'q, mumkin emas', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Slice turi', 't': 25, 'o': 13, 'q': [
        {'t': 'Slice nima?', 'a': [{'t': 'Ketma-ketlikning bir qismi', 'c': True}, {'t': 'To\'liq array', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Tuple', 'c': False}]},
        {'t': 'String slice qanday yaratiladi?', 'a': [{'t': '&s[0..5]', 'c': True}, {'t': 's[0..5]', 'c': False}, {'t': 's.slice(0, 5)', 'c': False}, {'t': 'slice(s, 0, 5)', 'c': False}]},
        {'t': '&str nima?', 'a': [{'t': 'String slice turi', 'c': True}, {'t': 'String turi', 'c': False}, {'t': 'Char turi', 'c': False}, {'t': 'Array turi', 'c': False}]},
        {'t': 'String va &str farqi?', 'a': [{'t': 'String egalik bor, &str yo\'q', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '&str yangi', 'c': False}, {'t': 'String tezroq', 'c': False}]},
        {'t': 'Array slice qanday?', 'a': [{'t': '&arr[1..3]', 'c': True}, {'t': 'arr[1..3]', 'c': False}, {'t': 'arr.slice(1, 3)', 'c': False}, {'t': 'slice(arr, 1, 3)', 'c': False}]},
        {'t': 'Slice turi qanday yoziladi?', 'a': [{'t': '&[T]', 'c': True}, {'t': '[T]', 'c': False}, {'t': 'slice<T>', 'c': False}, {'t': 'Slice<T>', 'c': False}]},
    ]},
    {'n': 'Struct (Tuzilma)', 't': 25, 'o': 14, 'q': [
        {'t': 'Struct nima?', 'a': [{'t': 'Ma\'lumotlarni guruhlash uchun tur', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Sikl', 'c': False}]},
        {'t': 'Struct qanday e\'lon qilinadi?', 'a': [{'t': 'struct Name { field: Type }', 'c': True}, {'t': 'class Name { field: Type }', 'c': False}, {'t': 'type Name { field: Type }', 'c': False}, {'t': 'struct Name(Type)', 'c': False}]},
        {'t': 'Struct instance qanday yaratiladi?', 'a': [{'t': 'Name { field: value }', 'c': True}, {'t': 'new Name(value)', 'c': False}, {'t': 'Name(value)', 'c': False}, {'t': 'Name::new(value)', 'c': False}]},
        {'t': 'Struct field ga qanday kirish mumkin?', 'a': [{'t': 'instance.field', 'c': True}, {'t': 'instance->field', 'c': False}, {'t': 'instance[field]', 'c': False}, {'t': 'instance::field', 'c': False}]},
        {'t': 'Tuple struct nima?', 'a': [{'t': 'struct Name(Type1, Type2);', 'c': True}, {'t': 'Oddiy struct', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Unit-like struct nima?', 'a': [{'t': 'struct Name; (fieldsiz)', 'c': True}, {'t': 'struct Name { }', 'c': False}, {'t': 'struct Name();', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Struct metodlari va impl', 't': 25, 'o': 15, 'q': [
        {'t': 'impl nima?', 'a': [{'t': 'Struct uchun metodlar e\'lon qilish', 'c': True}, {'t': 'Struct yaratish', 'c': False}, {'t': 'Funksiya yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'impl Name { } ichida nima yoziladi?', 'a': [{'t': 'Metodlar va funksiyalar', 'c': True}, {'t': 'Fieldlar', 'c': False}, {'t': 'O\'zgaruvchilar', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Metod birinchi parametri nima?', 'a': [{'t': '&self yoki &mut self', 'c': True}, {'t': 'self', 'c': False}, {'t': 'this', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Associated function nima?', 'a': [{'t': 'self parametrisiz funksiya', 'c': True}, {'t': 'Oddiy metod', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Associated function qanday chaqiriladi?', 'a': [{'t': 'Name::function()', 'c': True}, {'t': 'instance.function()', 'c': False}, {'t': 'function(Name)', 'c': False}, {'t': 'Name.function()', 'c': False}]},
        {'t': 'String::from() nima?', 'a': [{'t': 'Associated function', 'c': True}, {'t': 'Metod', 'c': False}, {'t': 'Makros', 'c': False}, {'t': 'Operator', 'c': False}]},
    ]},
    {'n': 'Enum (Sanash)', 't': 25, 'o': 16, 'q': [
        {'t': 'Enum nima?', 'a': [{'t': 'Bir necha variantlardan biri bo\'lishi mumkin bo\'lgan tur', 'c': True}, {'t': 'Struct', 'c': False}, {'t': 'Array', 'c': False}, {'t': 'Tuple', 'c': False}]},
        {'t': 'enum Color { Red, Green, Blue } to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Enum variantiga qanday kirish mumkin?', 'a': [{'t': 'Color::Red', 'c': True}, {'t': 'Color.Red', 'c': False}, {'t': 'Color[Red]', 'c': False}, {'t': 'Red', 'c': False}]},
        {'t': 'Enum variantida ma\'lumot bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'enum Message { Quit, Move { x: i32 } } to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Option<T> nima?', 'a': [{'t': 'Qiymat bor yoki yo\'q (Some/None)', 'c': True}, {'t': 'Xatolik turi', 'c': False}, {'t': 'Array turi', 'c': False}, {'t': 'String turi', 'c': False}]},
    ]},
    {'n': 'Pattern matching - match', 't': 25, 'o': 17, 'q': [
        {'t': 'match nima?', 'a': [{'t': 'Pattern matching operatori', 'c': True}, {'t': 'Sikl', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'match exhaustive bo\'lishi kerakmi?', 'a': [{'t': 'Ha, barcha holatlar qamrab olinishi kerak', 'c': True}, {'t': 'Yo\'q, ba\'zi holatlar yetarli', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'match da _ nima?', 'a': [{'t': 'Qolgan barcha holatlar', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'O\'zgaruvchi', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'match qiymat qaytaradimi?', 'a': [{'t': 'Ha, qaytaradi', 'c': True}, {'t': 'Yo\'q, qaytarmaydi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'match Some(x) => x nima qiladi?', 'a': [{'t': 'x ni chiqarib oladi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'if let nima?', 'a': [{'t': 'match ning qisqa yozuvi (bitta holat)', 'c': True}, {'t': 'Oddiy if', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Result va xatoliklarni boshqarish', 't': 25, 'o': 18, 'q': [
        {'t': 'Result<T, E> nima?', 'a': [{'t': 'Muvaffaqiyat (Ok) yoki xatolik (Err)', 'c': True}, {'t': 'Faqat muvaffaqiyat', 'c': False}, {'t': 'Faqat xatolik', 'c': False}, {'t': 'Option', 'c': False}]},
        {'t': 'Ok(value) nima?', 'a': [{'t': 'Muvaffaqiyatli natija', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'None', 'c': False}, {'t': 'Some', 'c': False}]},
        {'t': 'Err(error) nima?', 'a': [{'t': 'Xatolik natijasi', 'c': True}, {'t': 'Muvaffaqiyat', 'c': False}, {'t': 'None', 'c': False}, {'t': 'Some', 'c': False}]},
        {'t': 'unwrap() nima qiladi?', 'a': [{'t': 'Ok dan qiymat oladi, Err da panic', 'c': True}, {'t': 'Har doim xavfsiz', 'c': False}, {'t': 'Xatolikni ignore qiladi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'expect("msg") nima qiladi?', 'a': [{'t': 'unwrap kabi, lekin xabar bilan', 'c': True}, {'t': 'Xatolikni qaytaradi', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '? operatori nima qiladi?', 'a': [{'t': 'Err bo\'lsa qaytaradi, Ok bo\'lsa davom etadi', 'c': True}, {'t': 'Panic qiladi', 'c': False}, {'t': 'Ignore qiladi', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Vec (Vector) - Dinamik massiv', 't': 25, 'o': 19, 'q': [
        {'t': 'Vec nima?', 'a': [{'t': 'Dinamik o\'lchamli massiv', 'c': True}, {'t': 'Fix o\'lchamli massiv', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Tuple', 'c': False}]},
        {'t': 'Vec qanday yaratiladi?', 'a': [{'t': 'Vec::new() yoki vec![]', 'c': True}, {'t': 'Faqat Vec::new()', 'c': False}, {'t': 'Faqat vec![]', 'c': False}, {'t': 'new Vec()', 'c': False}]},
        {'t': 'vec![1, 2, 3] to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'v.push(5) nima qiladi?', 'a': [{'t': 'Oxiriga element qo\'shadi', 'c': True}, {'t': 'Boshiga element qo\'shadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v.pop() nima qiladi?', 'a': [{'t': 'Oxirgi elementni o\'chiradi va qaytaradi', 'c': True}, {'t': 'Birinchi elementni o\'chiradi', 'c': False}, {'t': 'Element qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Vec elementiga qanday kirish mumkin?', 'a': [{'t': 'v[i] yoki v.get(i)', 'c': True}, {'t': 'Faqat v[i]', 'c': False}, {'t': 'Faqat v.get(i)', 'c': False}, {'t': 'v.at(i)', 'c': False}]},
        {'t': 'v[i] va v.get(i) farqi?', 'a': [{'t': 'v[i] panic, v.get(i) Option qaytaradi', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'v.get(i) tezroq', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'String va String metodlari', 't': 25, 'o': 20, 'q': [
        {'t': 'String qanday yaratiladi?', 'a': [{'t': 'String::new() yoki String::from("text")', 'c': True}, {'t': 'Faqat "text"', 'c': False}, {'t': 'new String("text")', 'c': False}, {'t': 'string("text")', 'c': False}]},
        {'t': 'String va &str farqi?', 'a': [{'t': 'String heap da, &str stack/heap da', 'c': True}, {'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': '&str yangi', 'c': False}, {'t': 'String tezroq', 'c': False}]},
        {'t': 's.push_str("text") nima qiladi?', 'a': [{'t': 'String ga qo\'shadi', 'c': True}, {'t': 'Yangi String yaratadi', 'c': False}, {'t': 'Stringni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 's.push(\'c\') nima qiladi?', 'a': [{'t': 'Bitta char qo\'shadi', 'c': True}, {'t': 'String qo\'shadi', 'c': False}, {'t': 'Char ni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'String concatenation: s1 + &s2 to\'g\'rimi?', 'a': [{'t': 'Ha, lekin s1 move bo\'ladi', 'c': True}, {'t': 'Ha, ikkalasi ham qoladi', 'c': False}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'format!("{}_{}", s1, s2) nima qiladi?', 'a': [{'t': 'Yangi String yaratadi (move yo\'q)', 'c': True}, {'t': 's1 ni o\'zgartiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'HashMap - Kalit-qiymat to\'plami', 't': 25, 'o': 21, 'q': [
        {'t': 'HashMap nima?', 'a': [{'t': 'Kalit-qiymat juftliklari to\'plami', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'String', 'c': False}, {'t': 'Tuple', 'c': False}]},
        {'t': 'HashMap qanday yaratiladi?', 'a': [{'t': 'HashMap::new()', 'c': True}, {'t': 'new HashMap()', 'c': False}, {'t': 'hashmap![]', 'c': False}, {'t': 'HashMap()', 'c': False}]},
        {'t': 'HashMap ishlatish uchun nima kerak?', 'a': [{'t': 'use std::collections::HashMap;', 'c': True}, {'t': 'Hech narsa', 'c': False}, {'t': 'import HashMap', 'c': False}, {'t': 'include HashMap', 'c': False}]},
        {'t': 'map.insert(key, value) nima qiladi?', 'a': [{'t': 'Kalit-qiymat qo\'shadi', 'c': True}, {'t': 'Qiymatni o\'chiradi', 'c': False}, {'t': 'Qiymatni oladi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'map.get(&key) nima qaytaradi?', 'a': [{'t': 'Option<&V>', 'c': True}, {'t': 'V', 'c': False}, {'t': '&V', 'c': False}, {'t': 'Result<V>', 'c': False}]},
        {'t': 'map.entry(key).or_insert(value) nima qiladi?', 'a': [{'t': 'Kalit yo\'q bo\'lsa qo\'shadi', 'c': True}, {'t': 'Har doim qo\'shadi', 'c': False}, {'t': 'Kalitni o\'chiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Generic turlar', 't': 25, 'o': 22, 'q': [
        {'t': 'Generic nima?', 'a': [{'t': 'Turlarni parametrlash', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Sikl', 'c': False}]},
        {'t': 'fn largest<T>(list: &[T]) -> T to\'g\'rimi?', 'a': [{'t': 'Ha, generic funksiya', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'struct Point<T> { x: T, y: T } to\'g\'rimi?', 'a': [{'t': 'Ha, generic struct', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'enum Option<T> { Some(T), None } to\'g\'rimi?', 'a': [{'t': 'Ha, generic enum', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Generic turlar runtime da overhead qo\'shadimi?', 'a': [{'t': 'Yo\'q, monomorphization', 'c': True}, {'t': 'Ha, qo\'shadi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Trait (Xususiyat)', 't': 25, 'o': 23, 'q': [
        {'t': 'Trait nima?', 'a': [{'t': 'Umumiy xatti-harakatni aniqlash', 'c': True}, {'t': 'Struct', 'c': False}, {'t': 'Enum', 'c': False}, {'t': 'Funksiya', 'c': False}]},
        {'t': 'trait Summary { fn summarize(&self) -> String; } to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Trait qanday implement qilinadi?', 'a': [{'t': 'impl Trait for Type { }', 'c': True}, {'t': 'impl Type: Trait { }', 'c': False}, {'t': 'Type implements Trait { }', 'c': False}, {'t': 'Trait for Type { }', 'c': False}]},
        {'t': 'Trait bound nima?', 'a': [{'t': 'Generic turga trait talabi', 'c': True}, {'t': 'Trait yaratish', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'fn notify<T: Summary>(item: T) to\'g\'rimi?', 'a': [{'t': 'Ha, trait bound', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'fn notify(item: impl Summary) to\'g\'rimi?', 'a': [{'t': 'Ha, impl Trait syntax', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Lifetime (Hayot davri)', 't': 25, 'o': 24, 'q': [
        {'t': 'Lifetime nima?', 'a': [{'t': 'Reference qancha vaqt yaroqli', 'c': True}, {'t': 'O\'zgaruvchi turi', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'Lifetime annotation qanday yoziladi?', 'a': [{'t': '\'a', 'c': True}, {'t': '@a', 'c': False}, {'t': '#a', 'c': False}, {'t': 'a:', 'c': False}]},
        {'t': 'fn longest<\'a>(x: &\'a str, y: &\'a str) -> &\'a str to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Lifetime elision nima?', 'a': [{'t': 'Kompilyator lifetime ni avtomatik aniqlaydi', 'c': True}, {'t': 'Xatolik', 'c': False}, {'t': 'Lifetime yo\'q', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '\'static lifetime nima?', 'a': [{'t': 'Butun dastur davomida yaroqli', 'c': True}, {'t': 'Qisqa muddatli', 'c': False}, {'t': 'O\'zgaruvchan', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Struct da lifetime kerakmi?', 'a': [{'t': 'Ha, agar reference field bo\'lsa', 'c': True}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Modullar va paketlar', 't': 25, 'o': 25, 'q': [
        {'t': 'mod nima?', 'a': [{'t': 'Modul e\'lon qilish', 'c': True}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}, {'t': 'Tur', 'c': False}]},
        {'t': 'mod name { } to\'g\'rimi?', 'a': [{'t': 'Ha, inline modul', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'mod name; nima qiladi?', 'a': [{'t': 'name.rs faylidan modul yuklaydi', 'c': True}, {'t': 'Bo\'sh modul yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'pub nima?', 'a': [{'t': 'Public (ommaviy) qilish', 'c': True}, {'t': 'Private qilish', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'use nima qiladi?', 'a': [{'t': 'Yo\'lni scope ga olib kiradi', 'c': True}, {'t': 'Modul yaratadi', 'c': False}, {'t': 'Funksiya chaqiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'use std::collections::HashMap; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'crate nima?', 'a': [{'t': 'Paket (library yoki binary)', 'c': True}, {'t': 'Modul', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Tur', 'c': False}]},
    ]},
    {'n': 'Testlar yozish', 't': 25, 'o': 26, 'q': [
        {'t': 'Test funksiyasi qanday belgilanadi?', 'a': [{'t': '#[test]', 'c': True}, {'t': '@test', 'c': False}, {'t': 'test:', 'c': False}, {'t': 'fn test()', 'c': False}]},
        {'t': 'cargo test nima qiladi?', 'a': [{'t': 'Testlarni ishga tushiradi', 'c': True}, {'t': 'Kodni kompilyatsiya qiladi', 'c': False}, {'t': 'Kodni formatlaydi', 'c': False}, {'t': 'Xatoliklarni topadi', 'c': False}]},
        {'t': 'assert_eq!(a, b) nima qiladi?', 'a': [{'t': 'a va b teng ekanligini tekshiradi', 'c': True}, {'t': 'a ni b ga tenglashtiradi', 'c': False}, {'t': 'a va b ni qo\'shadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'assert!(condition) nima qiladi?', 'a': [{'t': 'condition true ekanligini tekshiradi', 'c': True}, {'t': 'condition ni o\'zgartiradi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': '#[should_panic] nima?', 'a': [{'t': 'Test panic qilishi kerak', 'c': True}, {'t': 'Test panic qilmasligi kerak', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Test moduli qanday yaratiladi?', 'a': [{'t': '#[cfg(test)] mod tests { }', 'c': True}, {'t': 'mod tests { }', 'c': False}, {'t': 'test mod tests { }', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Closure (Yopilish)', 't': 25, 'o': 27, 'q': [
        {'t': 'Closure nima?', 'a': [{'t': 'Anonim funksiya (environment ni capture qiladi)', 'c': True}, {'t': 'Oddiy funksiya', 'c': False}, {'t': 'Makros', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'let add = |x, y| x + y; to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure parametr turini ko\'rsatish majburiyatmi?', 'a': [{'t': 'Yo\'q, kompilyator aniqlaydi', 'c': True}, {'t': 'Ha, majburiy', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Closure environment ni qanday capture qiladi?', 'a': [{'t': 'Borrow, mutable borrow, yoki move', 'c': True}, {'t': 'Faqat borrow', 'c': False}, {'t': 'Faqat move', 'c': False}, {'t': 'Capture qilmaydi', 'c': False}]},
        {'t': 'move |x| x + y nima qiladi?', 'a': [{'t': 'y ni move qiladi', 'c': True}, {'t': 'y ni borrow qiladi', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Fn, FnMut, FnOnce nima?', 'a': [{'t': 'Closure traitlari', 'c': True}, {'t': 'Funksiya turlari', 'c': False}, {'t': 'Makroslar', 'c': False}, {'t': 'Operatorlar', 'c': False}]},
    ]},
    {'n': 'Iterator va iterator metodlari', 't': 25, 'o': 28, 'q': [
        {'t': 'Iterator nima?', 'a': [{'t': 'Ketma-ketlikni aylanish mexanizmi', 'c': True}, {'t': 'Massiv', 'c': False}, {'t': 'Funksiya', 'c': False}, {'t': 'Operator', 'c': False}]},
        {'t': 'v.iter() nima qaytaradi?', 'a': [{'t': 'Immutable reference iterator', 'c': True}, {'t': 'Mutable reference iterator', 'c': False}, {'t': 'Owned iterator', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v.iter_mut() nima qaytaradi?', 'a': [{'t': 'Mutable reference iterator', 'c': True}, {'t': 'Immutable reference iterator', 'c': False}, {'t': 'Owned iterator', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'v.into_iter() nima qiladi?', 'a': [{'t': 'Owned iterator (v ni consume qiladi)', 'c': True}, {'t': 'Reference iterator', 'c': False}, {'t': 'v ni o\'zgartirmaydi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'map() nima qiladi?', 'a': [{'t': 'Har bir elementga funksiya qo\'llaydi', 'c': True}, {'t': 'Elementlarni filtrlaydi', 'c': False}, {'t': 'Elementlarni yig\'adi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'filter() nima qiladi?', 'a': [{'t': 'Shartga mos elementlarni filtrlaydi', 'c': True}, {'t': 'Elementlarni o\'zgartiradi', 'c': False}, {'t': 'Elementlarni yig\'adi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'collect() nima qiladi?', 'a': [{'t': 'Iterator ni to\'plamga aylantiradi', 'c': True}, {'t': 'Elementlarni filtrlaydi', 'c': False}, {'t': 'Elementlarni o\'zgartiradi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
    {'n': 'Smart pointerlar - Box', 't': 25, 'o': 29, 'q': [
        {'t': 'Smart pointer nima?', 'a': [{'t': 'Qo\'shimcha metadata va funksiyalarga ega pointer', 'c': True}, {'t': 'Oddiy pointer', 'c': False}, {'t': 'Reference', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'Box<T> nima?', 'a': [{'t': 'Heap da ma\'lumot saqlash', 'c': True}, {'t': 'Stack da ma\'lumot saqlash', 'c': False}, {'t': 'Reference', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'let b = Box::new(5); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Box qachon ishlatiladi?', 'a': [{'t': 'Katta ma\'lumot, rekursiv tur, trait object', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Box scope dan chiqsa nima bo\'ladi?', 'a': [{'t': 'Heap ma\'lumoti o\'chiriladi', 'c': True}, {'t': 'Hech narsa', 'c': False}, {'t': 'Xatolik', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
    ]},
    {'n': 'Concurrency - Thread va Message Passing', 't': 25, 'o': 30, 'q': [
        {'t': 'thread::spawn nima qiladi?', 'a': [{'t': 'Yangi thread yaratadi', 'c': True}, {'t': 'Thread ni to\'xtatadi', 'c': False}, {'t': 'Thread ni kutadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'let handle = thread::spawn(|| { }); to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'handle.join() nima qiladi?', 'a': [{'t': 'Thread tugashini kutadi', 'c': True}, {'t': 'Thread ni to\'xtatadi', 'c': False}, {'t': 'Yangi thread yaratadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'mpsc nima?', 'a': [{'t': 'Multiple producer, single consumer channel', 'c': True}, {'t': 'Thread turi', 'c': False}, {'t': 'Mutex', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'let (tx, rx) = mpsc::channel(); to\'g\'rimi?', 'a': [{'t': 'Ha, transmitter va receiver', 'c': True}, {'t': 'Yo\'q, xato', 'c': False}, {'t': 'Qisman to\'g\'ri', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'tx.send(value) nima qiladi?', 'a': [{'t': 'Channel orqali qiymat yuboradi', 'c': True}, {'t': 'Qiymat qabul qiladi', 'c': False}, {'t': 'Channel ni yopadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
        {'t': 'rx.recv() nima qiladi?', 'a': [{'t': 'Qiymat qabul qiladi (blocking)', 'c': True}, {'t': 'Qiymat yuboradi', 'c': False}, {'t': 'Channel ni yopadi', 'c': False}, {'t': 'Xatolik', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_rust()
    add_topics(subj, T)
    print(f"\n✅ Rust - {len(T)} ta mavzu muvaffaqiyatli qo\'shildi!")
