"""
CSS DASTURLASH - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_css():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='CSS', defaults={'category': cat, 'description': 'CSS - Veb sahifalarni dizayn qilish tili', 'icon': 'bi-palette', 'order': 11, 'is_active': True})
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
    {'n': 'CSS ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'CSS nima?', 'a': [{'t': 'Cascading Style Sheets - veb sahifalarni dizayn qilish tili', 'c': True}, {'t': 'Computer Style System', 'c': False}, {'t': 'Creative Style Sheets', 'c': False}, {'t': 'Code Style System', 'c': False}]},
        {'t': 'CSS ning asosiy vazifasi nima?', 'a': [{'t': 'HTML elementlarini stillashtirish va dizayn qilish', 'c': True}, {'t': 'Ma\'lumotlar bazasi yaratish', 'c': False}, {'t': 'Dastur mantiqini yozish', 'c': False}, {'t': 'Server sozlash', 'c': False}]},
        {'t': 'CSS qaysi yilda yaratilgan?', 'a': [{'t': '1996 yilda', 'c': True}, {'t': '1990 yilda', 'c': False}, {'t': '2000 yilda', 'c': False}, {'t': '1985 yilda', 'c': False}]},
        {'t': 'CSS ni kim yaratgan?', 'a': [{'t': 'Håkon Wium Lie', 'c': True}, {'t': 'Tim Berners-Lee', 'c': False}, {'t': 'Brendan Eich', 'c': False}, {'t': 'Linus Torvalds', 'c': False}]},
        {'t': 'CSS fayl kengaytmasi qanday?', 'a': [{'t': '.css', 'c': True}, {'t': '.style', 'c': False}, {'t': '.html', 'c': False}, {'t': '.js', 'c': False}]},
        {'t': 'CSS ning "Cascading" so\'zi nimani anglatadi?', 'a': [{'t': 'Stillar ketma-ket qo\'llanilishi va ustunlik tartibi', 'c': True}, {'t': 'Tez ishlash', 'c': False}, {'t': 'Murakkablik', 'c': False}, {'t': 'Soddalik', 'c': False}]},
    ]},

    {'n': 'CSS ni HTML ga ulash', 't': 25, 'o': 2, 'q': [
        {'t': 'CSS ni HTML ga ulashning necha xil usuli bor?', 'a': [{'t': '3 xil: Inline, Internal, External', 'c': True}, {'t': '2 xil', 'c': False}, {'t': '5 xil', 'c': False}, {'t': '1 xil', 'c': False}]},
        {'t': 'Inline CSS qanday yoziladi?', 'a': [{'t': '<p style="color: red;">Matn</p>', 'c': True}, {'t': '<p css="color: red;">Matn</p>', 'c': False}, {'t': '<p class="red">Matn</p>', 'c': False}, {'t': '<p id="red">Matn</p>', 'c': False}]},
        {'t': 'Internal CSS qayerda yoziladi?', 'a': [{'t': '<head> ichida <style> tegi ichida', 'c': True}, {'t': '<body> ichida', 'c': False}, {'t': 'Alohida faylda', 'c': False}, {'t': '<footer> ichida', 'c': False}]},
        {'t': 'External CSS ni ulash uchun qaysi teg ishlatiladi?', 'a': [{'t': '<link rel="stylesheet" href="style.css">', 'c': True}, {'t': '<css src="style.css">', 'c': False}, {'t': '<style src="style.css">', 'c': False}, {'t': '<import href="style.css">', 'c': False}]},
        {'t': 'Qaysi usul eng yaxshi amaliyot hisoblanadi?', 'a': [{'t': 'External CSS - alohida fayl', 'c': True}, {'t': 'Inline CSS', 'c': False}, {'t': 'Internal CSS', 'c': False}, {'t': 'Hammasi bir xil', 'c': False}]},
        {'t': '<link> tegi qayerda yoziladi?', 'a': [{'t': '<head> ichida', 'c': True}, {'t': '<body> ichida', 'c': False}, {'t': '<footer> ichida', 'c': False}, {'t': '<header> ichida', 'c': False}]},
        {'t': '@import qoidasi nima uchun ishlatiladi?', 'a': [{'t': 'Bir CSS faylidan boshqa CSS faylini import qilish uchun', 'c': True}, {'t': 'HTML faylini import qilish uchun', 'c': False}, {'t': 'JavaScript faylini import qilish uchun', 'c': False}, {'t': 'Rasm import qilish uchun', 'c': False}]},
    ]},

    {'n': 'CSS Selektorlar - Asosiy', 't': 25, 'o': 3, 'q': [
        {'t': 'Element selektori qanday yoziladi?', 'a': [{'t': 'p { color: red; }', 'c': True}, {'t': '.p { color: red; }', 'c': False}, {'t': '#p { color: red; }', 'c': False}, {'t': '*p { color: red; }', 'c': False}]},
        {'t': 'Class selektori qanday yoziladi?', 'a': [{'t': '.classname { color: blue; }', 'c': True}, {'t': '#classname { color: blue; }', 'c': False}, {'t': 'classname { color: blue; }', 'c': False}, {'t': '*classname { color: blue; }', 'c': False}]},
        {'t': 'ID selektori qanday yoziladi?', 'a': [{'t': '#idname { color: green; }', 'c': True}, {'t': '.idname { color: green; }', 'c': False}, {'t': 'idname { color: green; }', 'c': False}, {'t': '@idname { color: green; }', 'c': False}]},
        {'t': 'Universal selektor qanday yoziladi?', 'a': [{'t': '* { margin: 0; }', 'c': True}, {'t': 'all { margin: 0; }', 'c': False}, {'t': '# { margin: 0; }', 'c': False}, {'t': '. { margin: 0; }', 'c': False}]},
        {'t': 'Bir nechta elementni tanlash uchun?', 'a': [{'t': 'h1, h2, h3 { color: red; }', 'c': True}, {'t': 'h1 h2 h3 { color: red; }', 'c': False}, {'t': 'h1 + h2 + h3 { color: red; }', 'c': False}, {'t': 'h1 > h2 > h3 { color: red; }', 'c': False}]},
        {'t': 'Class va ID orasidagi asosiy farq nima?', 'a': [{'t': 'Class bir nechta elementda, ID faqat bitta elementda ishlatiladi', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'ID bir nechta elementda ishlatiladi', 'c': False}, {'t': 'Class faqat bitta elementda ishlatiladi', 'c': False}]},
    ]},

    {'n': 'Ranglar bilan ishlash', 't': 25, 'o': 4, 'q': [
        {'t': 'CSS da ranglarni qanday usullar bilan berish mumkin?', 'a': [{'t': 'Nom, HEX, RGB, RGBA, HSL, HSLA', 'c': True}, {'t': 'Faqat nom bilan', 'c': False}, {'t': 'Faqat HEX bilan', 'c': False}, {'t': 'Faqat RGB bilan', 'c': False}]},
        {'t': 'HEX rang kodi qanday yoziladi?', 'a': [{'t': '#FF0000 yoki #F00', 'c': True}, {'t': 'FF0000', 'c': False}, {'t': '0xFF0000', 'c': False}, {'t': 'hex(FF0000)', 'c': False}]},
        {'t': 'RGB rang qanday yoziladi?', 'a': [{'t': 'rgb(255, 0, 0)', 'c': True}, {'t': 'rgb(255-0-0)', 'c': False}, {'t': 'rgb[255, 0, 0]', 'c': False}, {'t': 'rgb:255,0,0', 'c': False}]},
        {'t': 'RGBA dagi "A" nima uchun?', 'a': [{'t': 'Alpha - shaffoflik darajasi (0 dan 1 gacha)', 'c': True}, {'t': 'Automatic', 'c': False}, {'t': 'Advanced', 'c': False}, {'t': 'Alternative', 'c': False}]},
        {'t': 'Qora rang HEX kodida qanday?', 'a': [{'t': '#000000 yoki #000', 'c': True}, {'t': '#FFFFFF', 'c': False}, {'t': '#FF0000', 'c': False}, {'t': '#00FF00', 'c': False}]},
        {'t': 'Oq rang HEX kodida qanday?', 'a': [{'t': '#FFFFFF yoki #FFF', 'c': True}, {'t': '#000000', 'c': False}, {'t': '#FF0000', 'c': False}, {'t': '#0000FF', 'c': False}]},
        {'t': 'Shaffof qilish uchun qaysi xususiyat ishlatiladi?', 'a': [{'t': 'opacity yoki RGBA/HSLA', 'c': True}, {'t': 'transparent', 'c': False}, {'t': 'visibility', 'c': False}, {'t': 'display', 'c': False}]},
    ]},

    {'n': 'Matn stillashtirish', 't': 30, 'o': 5, 'q': [
        {'t': 'Matn rangini o\'zgartirish uchun?', 'a': [{'t': 'color: red;', 'c': True}, {'t': 'text-color: red;', 'c': False}, {'t': 'font-color: red;', 'c': False}, {'t': 'text: red;', 'c': False}]},
        {'t': 'Matn o\'lchamini o\'zgartirish uchun?', 'a': [{'t': 'font-size: 16px;', 'c': True}, {'t': 'text-size: 16px;', 'c': False}, {'t': 'size: 16px;', 'c': False}, {'t': 'font: 16px;', 'c': False}]},
        {'t': 'Matnni qalin qilish uchun?', 'a': [{'t': 'font-weight: bold;', 'c': True}, {'t': 'font-style: bold;', 'c': False}, {'t': 'text-weight: bold;', 'c': False}, {'t': 'bold: true;', 'c': False}]},
        {'t': 'Matnni kursiv qilish uchun?', 'a': [{'t': 'font-style: italic;', 'c': True}, {'t': 'font-weight: italic;', 'c': False}, {'t': 'text-style: italic;', 'c': False}, {'t': 'italic: true;', 'c': False}]},
        {'t': 'Matn ostiga chiziq chizish uchun?', 'a': [{'t': 'text-decoration: underline;', 'c': True}, {'t': 'text-underline: true;', 'c': False}, {'t': 'underline: true;', 'c': False}, {'t': 'border-bottom: 1px;', 'c': False}]},
        {'t': 'Matnni markazlashtirish uchun?', 'a': [{'t': 'text-align: center;', 'c': True}, {'t': 'align: center;', 'c': False}, {'t': 'text-center: true;', 'c': False}, {'t': 'center: true;', 'c': False}]},
        {'t': 'Matn orasidagi bo\'shliqni o\'zgartirish uchun?', 'a': [{'t': 'letter-spacing: 2px;', 'c': True}, {'t': 'text-spacing: 2px;', 'c': False}, {'t': 'char-spacing: 2px;', 'c': False}, {'t': 'space: 2px;', 'c': False}]},
        {'t': 'Qator balandligini o\'zgartirish uchun?', 'a': [{'t': 'line-height: 1.5;', 'c': True}, {'t': 'row-height: 1.5;', 'c': False}, {'t': 'text-height: 1.5;', 'c': False}, {'t': 'height: 1.5;', 'c': False}]},
    ]},

    {'n': 'Font (Shrift) bilan ishlash', 't': 25, 'o': 6, 'q': [
        {'t': 'Font turini o\'zgartirish uchun?', 'a': [{'t': 'font-family: Arial, sans-serif;', 'c': True}, {'t': 'font-type: Arial;', 'c': False}, {'t': 'font: Arial;', 'c': False}, {'t': 'text-font: Arial;', 'c': False}]},
        {'t': 'Web-safe fontlar nima?', 'a': [{'t': 'Ko\'pchilik brauzerlarda mavjud bo\'lgan fontlar', 'c': True}, {'t': 'Faqat Chrome da ishlaydigan fontlar', 'c': False}, {'t': 'Xavfsiz fontlar', 'c': False}, {'t': 'Bepul fontlar', 'c': False}]},
        {'t': 'Google Fonts ni qanday ulash mumkin?', 'a': [{'t': '<link> tegi yoki @import orqali', 'c': True}, {'t': 'Faqat yuklab olish orqali', 'c': False}, {'t': 'Avtomatik ulanadi', 'c': False}, {'t': 'JavaScript orqali', 'c': False}]},
        {'t': 'font-family da nima uchun bir nechta font yoziladi?', 'a': [{'t': 'Birinchisi mavjud bo\'lmasa, keyingisi ishlatiladi (fallback)', 'c': True}, {'t': 'Hammasi birgalikda ishlatiladi', 'c': False}, {'t': 'Tasodifiy biri tanlanadi', 'c': False}, {'t': 'Faqat birinchisi ishlatiladi', 'c': False}]},
        {'t': 'Sans-serif va serif orasidagi farq?', 'a': [{'t': 'Serif da harf uchlarida bezak bor, sans-serif da yo\'q', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Sans-serif kattaroq', 'c': False}, {'t': 'Serif yangi', 'c': False}]},
        {'t': '@font-face nima uchun ishlatiladi?', 'a': [{'t': 'Maxsus fontlarni yuklash va ishlatish uchun', 'c': True}, {'t': 'Font o\'lchamini o\'zgartirish uchun', 'c': False}, {'t': 'Font rangini o\'zgartirish uchun', 'c': False}, {'t': 'Font stilini o\'zgartirish uchun', 'c': False}]},
    ]},

    {'n': 'Box Model - Quti modeli', 't': 30, 'o': 7, 'q': [
        {'t': 'CSS Box Model nima?', 'a': [{'t': 'Har bir HTML element quti sifatida ko\'riladi: content, padding, border, margin', 'c': True}, {'t': 'Faqat border', 'c': False}, {'t': 'Faqat margin', 'c': False}, {'t': 'Faqat padding', 'c': False}]},
        {'t': 'Box Model qismlari to\'g\'ri tartibda?', 'a': [{'t': 'Content → Padding → Border → Margin', 'c': True}, {'t': 'Margin → Border → Padding → Content', 'c': False}, {'t': 'Border → Margin → Padding → Content', 'c': False}, {'t': 'Padding → Content → Border → Margin', 'c': False}]},
        {'t': 'Padding nima?', 'a': [{'t': 'Content va border orasidagi ichki bo\'shliq', 'c': True}, {'t': 'Border va margin orasidagi bo\'shliq', 'c': False}, {'t': 'Elementlar orasidagi bo\'shliq', 'c': False}, {'t': 'Tashqi bo\'shliq', 'c': False}]},
        {'t': 'Margin nima?', 'a': [{'t': 'Element atrofidagi tashqi bo\'shliq', 'c': True}, {'t': 'Ichki bo\'shliq', 'c': False}, {'t': 'Border kengligi', 'c': False}, {'t': 'Content o\'lchami', 'c': False}]},
        {'t': 'Border nima?', 'a': [{'t': 'Element atrofidagi chegara chizig\'i', 'c': True}, {'t': 'Ichki bo\'shliq', 'c': False}, {'t': 'Tashqi bo\'shliq', 'c': False}, {'t': 'Content', 'c': False}]},
        {'t': 'Barcha tomonlarga bir xil padding berish uchun?', 'a': [{'t': 'padding: 10px;', 'c': True}, {'t': 'padding-all: 10px;', 'c': False}, {'t': 'padding: 10px 10px 10px 10px;', 'c': False}, {'t': 'all-padding: 10px;', 'c': False}]},
        {'t': 'Faqat yuqori va pastga margin berish uchun?', 'a': [{'t': 'margin: 10px 0;', 'c': True}, {'t': 'margin-vertical: 10px;', 'c': False}, {'t': 'margin-y: 10px;', 'c': False}, {'t': 'margin: 0 10px;', 'c': False}]},
        {'t': 'box-sizing: border-box; nima qiladi?', 'a': [{'t': 'Width va height ga padding va border ham kiritiladi', 'c': True}, {'t': 'Faqat border kiritiladi', 'c': False}, {'t': 'Faqat padding kiritiladi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'Border - Chegara', 't': 25, 'o': 8, 'q': [
        {'t': 'Border qo\'shish uchun to\'liq sintaksis?', 'a': [{'t': 'border: 1px solid black;', 'c': True}, {'t': 'border: black 1px solid;', 'c': False}, {'t': 'border: solid 1px;', 'c': False}, {'t': 'border-style: 1px solid black;', 'c': False}]},
        {'t': 'Border stillari qaysilar?', 'a': [{'t': 'solid, dashed, dotted, double, groove, ridge, inset, outset', 'c': True}, {'t': 'Faqat solid', 'c': False}, {'t': 'Faqat solid va dashed', 'c': False}, {'t': 'Faqat dotted', 'c': False}]},
        {'t': 'Faqat pastki border qo\'shish uchun?', 'a': [{'t': 'border-bottom: 1px solid black;', 'c': True}, {'t': 'border-down: 1px solid black;', 'c': False}, {'t': 'bottom-border: 1px solid black;', 'c': False}, {'t': 'border: bottom 1px solid black;', 'c': False}]},
        {'t': 'Border burchaklarini yumaloq qilish uchun?', 'a': [{'t': 'border-radius: 10px;', 'c': True}, {'t': 'border-round: 10px;', 'c': False}, {'t': 'border-corner: 10px;', 'c': False}, {'t': 'radius: 10px;', 'c': False}]},
        {'t': 'Doira yasash uchun border-radius qanday bo\'lishi kerak?', 'a': [{'t': '50%', 'c': True}, {'t': '100%', 'c': False}, {'t': '25%', 'c': False}, {'t': '0%', 'c': False}]},
        {'t': 'Border rangini o\'zgartirish uchun?', 'a': [{'t': 'border-color: red;', 'c': True}, {'t': 'border: red;', 'c': False}, {'t': 'color-border: red;', 'c': False}, {'t': 'border-style: red;', 'c': False}]},
    ]},

    {'n': 'Width va Height - O\'lchamlar', 't': 25, 'o': 9, 'q': [
        {'t': 'Element kengligini belgilash uchun?', 'a': [{'t': 'width: 300px;', 'c': True}, {'t': 'size-width: 300px;', 'c': False}, {'t': 'w: 300px;', 'c': False}, {'t': 'length: 300px;', 'c': False}]},
        {'t': 'Element balandligini belgilash uchun?', 'a': [{'t': 'height: 200px;', 'c': True}, {'t': 'size-height: 200px;', 'c': False}, {'t': 'h: 200px;', 'c': False}, {'t': 'tall: 200px;', 'c': False}]},
        {'t': 'Maksimal kenglikni belgilash uchun?', 'a': [{'t': 'max-width: 500px;', 'c': True}, {'t': 'width-max: 500px;', 'c': False}, {'t': 'maximum-width: 500px;', 'c': False}, {'t': 'width: max 500px;', 'c': False}]},
        {'t': 'Minimal balandlikni belgilash uchun?', 'a': [{'t': 'min-height: 100px;', 'c': True}, {'t': 'height-min: 100px;', 'c': False}, {'t': 'minimum-height: 100px;', 'c': False}, {'t': 'height: min 100px;', 'c': False}]},
        {'t': 'O\'lcham birliklari qaysilar?', 'a': [{'t': 'px, %, em, rem, vw, vh, cm, mm', 'c': True}, {'t': 'Faqat px', 'c': False}, {'t': 'Faqat px va %', 'c': False}, {'t': 'Faqat cm', 'c': False}]},
        {'t': '100% kengligi nima bildiradi?', 'a': [{'t': 'Ota elementning to\'liq kengligi', 'c': True}, {'t': 'Ekranning to\'liq kengligi', 'c': False}, {'t': '100 piksel', 'c': False}, {'t': 'Maksimal kenglik', 'c': False}]},
    ]},

    {'n': 'Display xususiyati', 't': 30, 'o': 10, 'q': [
        {'t': 'display xususiyati nima uchun?', 'a': [{'t': 'Elementning ko\'rinish turini belgilash uchun', 'c': True}, {'t': 'Elementni ko\'rsatish/yashirish uchun', 'c': False}, {'t': 'Rang berish uchun', 'c': False}, {'t': 'O\'lcham berish uchun', 'c': False}]},
        {'t': 'display: block; nima qiladi?', 'a': [{'t': 'Element yangi qatordan boshlanadi va to\'liq kenglikni egallaydi', 'c': True}, {'t': 'Element bir qatorda turadi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}, {'t': 'Element markazlashadi', 'c': False}]},
        {'t': 'display: inline; nima qiladi?', 'a': [{'t': 'Element bir qatorda turadi, width/height ishlamaydi', 'c': True}, {'t': 'Element yangi qatordan boshlanadi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}, {'t': 'Element markazlashadi', 'c': False}]},
        {'t': 'display: inline-block; nima qiladi?', 'a': [{'t': 'Inline kabi bir qatorda, lekin width/height ishlaydi', 'c': True}, {'t': 'Block kabi ishlaydi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}, {'t': 'Faqat inline', 'c': False}]},
        {'t': 'display: none; nima qiladi?', 'a': [{'t': 'Elementni butunlay yashiradi va joy egallamaydi', 'c': True}, {'t': 'Elementni shaffof qiladi', 'c': False}, {'t': 'Elementni ko\'rsatadi', 'c': False}, {'t': 'Elementni markazlashtiradi', 'c': False}]},
        {'t': 'display: flex; nima uchun ishlatiladi?', 'a': [{'t': 'Flexbox layout yaratish uchun', 'c': True}, {'t': 'Elementni egiluvchan qilish uchun', 'c': False}, {'t': 'Elementni yashirish uchun', 'c': False}, {'t': 'Matn stillashtirish uchun', 'c': False}]},
        {'t': 'display: grid; nima uchun ishlatiladi?', 'a': [{'t': 'Grid layout yaratish uchun', 'c': True}, {'t': 'Jadval yaratish uchun', 'c': False}, {'t': 'Elementni yashirish uchun', 'c': False}, {'t': 'Rang berish uchun', 'c': False}]},
        {'t': 'Block-level elementlarga misollar?', 'a': [{'t': 'div, p, h1, section, article', 'c': True}, {'t': 'span, a, img', 'c': False}, {'t': 'Faqat div', 'c': False}, {'t': 'Faqat p', 'c': False}]},
    ]},

    {'n': 'Position - Joylashuv', 't': 30, 'o': 11, 'q': [
        {'t': 'position xususiyati qiymatlari?', 'a': [{'t': 'static, relative, absolute, fixed, sticky', 'c': True}, {'t': 'Faqat static va relative', 'c': False}, {'t': 'Faqat absolute va fixed', 'c': False}, {'t': 'top, left, right, bottom', 'c': False}]},
        {'t': 'position: static; nima?', 'a': [{'t': 'Standart joylashuv, top/left/right/bottom ishlamaydi', 'c': True}, {'t': 'Element harakatlanadi', 'c': False}, {'t': 'Element yopishib qoladi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}]},
        {'t': 'position: relative; nima qiladi?', 'a': [{'t': 'Element o\'z joyiga nisbatan siljiydi', 'c': True}, {'t': 'Element ota elementga nisbatan joylashadi', 'c': False}, {'t': 'Element ekranga nisbatan joylashadi', 'c': False}, {'t': 'Element harakatsiz qoladi', 'c': False}]},
        {'t': 'position: absolute; nima qiladi?', 'a': [{'t': 'Element eng yaqin positioned ota elementga nisbatan joylashadi', 'c': True}, {'t': 'Element o\'z joyiga nisbatan siljiydi', 'c': False}, {'t': 'Element harakatsiz qoladi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}]},
        {'t': 'position: fixed; nima qiladi?', 'a': [{'t': 'Element ekranga nisbatan qotib qoladi, scroll qilganda ham', 'c': True}, {'t': 'Element ota elementga nisbatan joylashadi', 'c': False}, {'t': 'Element harakatsiz qoladi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}]},
        {'t': 'position: sticky; nima qiladi?', 'a': [{'t': 'Scroll qilganda ma\'lum joyda yopishib qoladi', 'c': True}, {'t': 'Doim yopishib turadi', 'c': False}, {'t': 'Hech qachon yopishmaydi', 'c': False}, {'t': 'Element ko\'rinmaydi', 'c': False}]},
        {'t': 'top, left, right, bottom xususiyatlari qachon ishlaydi?', 'a': [{'t': 'position static dan boshqa bo\'lganda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat absolute da', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'z-index nima uchun ishlatiladi?', 'a': [{'t': 'Elementlarning ustma-ust joylashish tartibini belgilash uchun', 'c': True}, {'t': 'Element balandligini belgilash uchun', 'c': False}, {'t': 'Element kengligini belgilash uchun', 'c': False}, {'t': 'Rang berish uchun', 'c': False}]},
    ]},

    {'n': 'Float va Clear', 't': 25, 'o': 12, 'q': [
        {'t': 'float xususiyati nima uchun ishlatiladi?', 'a': [{'t': 'Elementni chap yoki o\'ng tomonga suzib joylash uchun', 'c': True}, {'t': 'Elementni markazlashtirish uchun', 'c': False}, {'t': 'Elementni yashirish uchun', 'c': False}, {'t': 'Rang berish uchun', 'c': False}]},
        {'t': 'float qiymatlari?', 'a': [{'t': 'left, right, none', 'c': True}, {'t': 'top, bottom, center', 'c': False}, {'t': 'Faqat left', 'c': False}, {'t': 'Faqat right', 'c': False}]},
        {'t': 'clear xususiyati nima uchun?', 'a': [{'t': 'Float ta\'sirini bekor qilish uchun', 'c': True}, {'t': 'Elementni tozalash uchun', 'c': False}, {'t': 'Rangni o\'chirish uchun', 'c': False}, {'t': 'Matnni o\'chirish uchun', 'c': False}]},
        {'t': 'clear qiymatlari?', 'a': [{'t': 'left, right, both, none', 'c': True}, {'t': 'Faqat both', 'c': False}, {'t': 'top, bottom', 'c': False}, {'t': 'all, none', 'c': False}]},
        {'t': 'Hozirgi kunda float o\'rniga nima ishlatiladi?', 'a': [{'t': 'Flexbox va Grid', 'c': True}, {'t': 'Faqat float', 'c': False}, {'t': 'Position', 'c': False}, {'t': 'Display', 'c': False}]},
    ]},

    {'n': 'Flexbox - Asoslar', 't': 30, 'o': 13, 'q': [
        {'t': 'Flexbox ni yoqish uchun?', 'a': [{'t': 'display: flex;', 'c': True}, {'t': 'flexbox: true;', 'c': False}, {'t': 'layout: flex;', 'c': False}, {'t': 'flex: on;', 'c': False}]},
        {'t': 'flex-direction xususiyati nima qiladi?', 'a': [{'t': 'Elementlar qaysi yo\'nalishda joylashishini belgilaydi', 'c': True}, {'t': 'Elementlar rangini o\'zgartiradi', 'c': False}, {'t': 'Elementlar o\'lchamini o\'zgartiradi', 'c': False}, {'t': 'Elementlarni yashiradi', 'c': False}]},
        {'t': 'flex-direction qiymatlari?', 'a': [{'t': 'row, row-reverse, column, column-reverse', 'c': True}, {'t': 'Faqat row va column', 'c': False}, {'t': 'horizontal, vertical', 'c': False}, {'t': 'left, right, top, bottom', 'c': False}]},
        {'t': 'justify-content nima qiladi?', 'a': [{'t': 'Asosiy o\'q bo\'yicha elementlarni joylashtiradi', 'c': True}, {'t': 'Elementlar rangini o\'zgartiradi', 'c': False}, {'t': 'Elementlar o\'lchamini o\'zgartiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
        {'t': 'justify-content qiymatlari?', 'a': [{'t': 'flex-start, flex-end, center, space-between, space-around, space-evenly', 'c': True}, {'t': 'Faqat center', 'c': False}, {'t': 'left, right, center', 'c': False}, {'t': 'top, bottom, middle', 'c': False}]},
        {'t': 'align-items nima qiladi?', 'a': [{'t': 'Kesishma o\'q bo\'yicha elementlarni joylashtiradi', 'c': True}, {'t': 'Asosiy o\'q bo\'yicha joylashtiradi', 'c': False}, {'t': 'Elementlar rangini o\'zgartiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
        {'t': 'align-items qiymatlari?', 'a': [{'t': 'flex-start, flex-end, center, stretch, baseline', 'c': True}, {'t': 'Faqat center', 'c': False}, {'t': 'left, right, center', 'c': False}, {'t': 'top, bottom, middle', 'c': False}]},
        {'t': 'Elementni markazlashtirish uchun flexbox da?', 'a': [{'t': 'justify-content: center; align-items: center;', 'c': True}, {'t': 'Faqat justify-content: center;', 'c': False}, {'t': 'Faqat align-items: center;', 'c': False}, {'t': 'text-align: center;', 'c': False}]},
    ]},

    {'n': 'Flexbox - Davomi', 't': 30, 'o': 14, 'q': [
        {'t': 'flex-wrap nima qiladi?', 'a': [{'t': 'Elementlar bir qatorga sig\'masa, keyingi qatorga o\'tishini boshqaradi', 'c': True}, {'t': 'Elementlarni o\'rab oladi', 'c': False}, {'t': 'Matnni o\'rab oladi', 'c': False}, {'t': 'Elementlarni yashiradi', 'c': False}]},
        {'t': 'flex-wrap qiymatlari?', 'a': [{'t': 'nowrap, wrap, wrap-reverse', 'c': True}, {'t': 'Faqat wrap', 'c': False}, {'t': 'true, false', 'c': False}, {'t': 'on, off', 'c': False}]},
        {'t': 'flex-grow nima qiladi?', 'a': [{'t': 'Element qancha bo\'sh joyni egallashini belgilaydi', 'c': True}, {'t': 'Element o\'lchamini oshiradi', 'c': False}, {'t': 'Element rangini o\'zgartiradi', 'c': False}, {'t': 'Elementni kattalashtiradi', 'c': False}]},
        {'t': 'flex-shrink nima qiladi?', 'a': [{'t': 'Element qancha kichrayishini belgilaydi', 'c': True}, {'t': 'Elementni yashiradi', 'c': False}, {'t': 'Element rangini o\'zgartiradi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}]},
        {'t': 'flex-basis nima?', 'a': [{'t': 'Elementning boshlang\'ich o\'lchami', 'c': True}, {'t': 'Elementning maksimal o\'lchami', 'c': False}, {'t': 'Elementning minimal o\'lchami', 'c': False}, {'t': 'Elementning rangini belgilaydi', 'c': False}]},
        {'t': 'flex qisqartmasi qanday yoziladi?', 'a': [{'t': 'flex: grow shrink basis;', 'c': True}, {'t': 'flex: basis grow shrink;', 'c': False}, {'t': 'flex: shrink grow basis;', 'c': False}, {'t': 'flex: grow basis shrink;', 'c': False}]},
        {'t': 'align-self nima qiladi?', 'a': [{'t': 'Bitta elementning o\'ziga xos align-items qiymatini belgilaydi', 'c': True}, {'t': 'Barcha elementlarni tekislaydi', 'c': False}, {'t': 'Elementni markazlashtiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
    ]},

    {'n': 'Grid Layout - Asoslar', 't': 30, 'o': 15, 'q': [
        {'t': 'Grid ni yoqish uchun?', 'a': [{'t': 'display: grid;', 'c': True}, {'t': 'grid: true;', 'c': False}, {'t': 'layout: grid;', 'c': False}, {'t': 'grid: on;', 'c': False}]},
        {'t': 'grid-template-columns nima qiladi?', 'a': [{'t': 'Ustunlar sonini va kengligini belgilaydi', 'c': True}, {'t': 'Qatorlar sonini belgilaydi', 'c': False}, {'t': 'Elementlar rangini o\'zgartiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
        {'t': '3 ta teng ustun yaratish uchun?', 'a': [{'t': 'grid-template-columns: 1fr 1fr 1fr; yoki repeat(3, 1fr);', 'c': True}, {'t': 'grid-columns: 3;', 'c': False}, {'t': 'columns: 3;', 'c': False}, {'t': 'grid: 3;', 'c': False}]},
        {'t': 'fr birligi nima?', 'a': [{'t': 'Fraction - bo\'sh joyning bir qismi', 'c': True}, {'t': 'Frame', 'c': False}, {'t': 'Free', 'c': False}, {'t': 'Fixed', 'c': False}]},
        {'t': 'grid-template-rows nima qiladi?', 'a': [{'t': 'Qatorlar sonini va balandligini belgilaydi', 'c': True}, {'t': 'Ustunlar sonini belgilaydi', 'c': False}, {'t': 'Elementlar rangini o\'zgartiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
        {'t': 'gap xususiyati nima qiladi?', 'a': [{'t': 'Grid elementlari orasidagi bo\'shliqni belgilaydi', 'c': True}, {'t': 'Elementlar o\'lchamini belgilaydi', 'c': False}, {'t': 'Elementlar rangini o\'zgartiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
        {'t': 'row-gap va column-gap farqi?', 'a': [{'t': 'row-gap qatorlar, column-gap ustunlar orasidagi bo\'shliq', 'c': True}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'row-gap kattaroq', 'c': False}, {'t': 'column-gap kattaroq', 'c': False}]},
    ]},

    {'n': 'Grid Layout - Davomi', 't': 30, 'o': 16, 'q': [
        {'t': 'grid-column nima qiladi?', 'a': [{'t': 'Element nechta ustunni egallashini belgilaydi', 'c': True}, {'t': 'Ustunlar sonini belgilaydi', 'c': False}, {'t': 'Ustun rangini o\'zgartiradi', 'c': False}, {'t': 'Ustun balandligini belgilaydi', 'c': False}]},
        {'t': 'grid-row nima qiladi?', 'a': [{'t': 'Element nechta qatorni egallashini belgilaydi', 'c': True}, {'t': 'Qatorlar sonini belgilaydi', 'c': False}, {'t': 'Qator rangini o\'zgartiradi', 'c': False}, {'t': 'Qator kengligini belgilaydi', 'c': False}]},
        {'t': 'Elementni 2 ta ustunni egallash uchun?', 'a': [{'t': 'grid-column: span 2;', 'c': True}, {'t': 'grid-column: 2;', 'c': False}, {'t': 'column-span: 2;', 'c': False}, {'t': 'columns: 2;', 'c': False}]},
        {'t': 'grid-area nima uchun ishlatiladi?', 'a': [{'t': 'Elementga nom berish va joylashuvini belgilash uchun', 'c': True}, {'t': 'Element maydonini hisoblash uchun', 'c': False}, {'t': 'Element rangini o\'zgartirish uchun', 'c': False}, {'t': 'Matnni tekislash uchun', 'c': False}]},
        {'t': 'grid-template-areas nima qiladi?', 'a': [{'t': 'Grid layoutni nomlar bilan vizual belgilash', 'c': True}, {'t': 'Grid o\'lchamini belgilash', 'c': False}, {'t': 'Grid rangini o\'zgartirish', 'c': False}, {'t': 'Grid ni yashirish', 'c': False}]},
        {'t': 'justify-items va align-items Grid da nima qiladi?', 'a': [{'t': 'Elementlarni kataklar ichida joylashtiradi', 'c': True}, {'t': 'Grid o\'lchamini o\'zgartiradi', 'c': False}, {'t': 'Grid rangini o\'zgartiradi', 'c': False}, {'t': 'Matnni tekislaydi', 'c': False}]},
    ]},

    {'n': 'Background - Fon', 't': 30, 'o': 17, 'q': [
        {'t': 'Fon rangini belgilash uchun?', 'a': [{'t': 'background-color: blue;', 'c': True}, {'t': 'color: blue;', 'c': False}, {'t': 'bg-color: blue;', 'c': False}, {'t': 'background: blue;', 'c': False}]},
        {'t': 'Fon rasmini qo\'shish uchun?', 'a': [{'t': 'background-image: url("rasm.jpg");', 'c': True}, {'t': 'background: "rasm.jpg";', 'c': False}, {'t': 'image: url("rasm.jpg");', 'c': False}, {'t': 'bg-image: "rasm.jpg";', 'c': False}]},
        {'t': 'Fon rasmini takrorlamaslik uchun?', 'a': [{'t': 'background-repeat: no-repeat;', 'c': True}, {'t': 'background-repeat: false;', 'c': False}, {'t': 'repeat: no;', 'c': False}, {'t': 'no-repeat: true;', 'c': False}]},
        {'t': 'background-repeat qiymatlari?', 'a': [{'t': 'repeat, no-repeat, repeat-x, repeat-y', 'c': True}, {'t': 'Faqat repeat va no-repeat', 'c': False}, {'t': 'true, false', 'c': False}, {'t': 'on, off', 'c': False}]},
        {'t': 'Fon rasmini markazlashtirish uchun?', 'a': [{'t': 'background-position: center;', 'c': True}, {'t': 'background-align: center;', 'c': False}, {'t': 'position: center;', 'c': False}, {'t': 'align: center;', 'c': False}]},
        {'t': 'Fon rasmini to\'liq qoplash uchun?', 'a': [{'t': 'background-size: cover;', 'c': True}, {'t': 'background-size: 100%;', 'c': False}, {'t': 'background: cover;', 'c': False}, {'t': 'size: cover;', 'c': False}]},
        {'t': 'Fon rasmini butunlay ko\'rsatish uchun?', 'a': [{'t': 'background-size: contain;', 'c': True}, {'t': 'background-size: full;', 'c': False}, {'t': 'background: contain;', 'c': False}, {'t': 'size: contain;', 'c': False}]},
        {'t': 'Fon rasmini scroll qilganda qotib turishi uchun?', 'a': [{'t': 'background-attachment: fixed;', 'c': True}, {'t': 'background-fixed: true;', 'c': False}, {'t': 'fixed: true;', 'c': False}, {'t': 'attachment: fixed;', 'c': False}]},
    ]},

    {'n': 'Gradient - Rang o\'tishi', 't': 25, 'o': 18, 'q': [
        {'t': 'Linear gradient yaratish uchun?', 'a': [{'t': 'background: linear-gradient(red, blue);', 'c': True}, {'t': 'background: gradient(red, blue);', 'c': False}, {'t': 'gradient: linear(red, blue);', 'c': False}, {'t': 'background-gradient: red, blue;', 'c': False}]},
        {'t': 'Radial gradient yaratish uchun?', 'a': [{'t': 'background: radial-gradient(red, blue);', 'c': True}, {'t': 'background: circle-gradient(red, blue);', 'c': False}, {'t': 'gradient: radial(red, blue);', 'c': False}, {'t': 'background-gradient: radial red blue;', 'c': False}]},
        {'t': 'Gradient yo\'nalishini belgilash uchun?', 'a': [{'t': 'linear-gradient(to right, red, blue);', 'c': True}, {'t': 'linear-gradient(right, red, blue);', 'c': False}, {'t': 'linear-gradient(direction: right, red, blue);', 'c': False}, {'t': 'gradient(to right, red, blue);', 'c': False}]},
        {'t': 'Gradient burchagini belgilash uchun?', 'a': [{'t': 'linear-gradient(45deg, red, blue);', 'c': True}, {'t': 'linear-gradient(angle: 45, red, blue);', 'c': False}, {'t': 'linear-gradient(45, red, blue);', 'c': False}, {'t': 'gradient(45deg, red, blue);', 'c': False}]},
        {'t': 'Bir nechta rang bilan gradient?', 'a': [{'t': 'linear-gradient(red, yellow, green, blue);', 'c': True}, {'t': 'Faqat 2 ta rang', 'c': False}, {'t': 'Maksimal 3 ta rang', 'c': False}, {'t': 'Faqat 1 ta rang', 'c': False}]},
        {'t': 'Rang to\'xtash joyini belgilash uchun?', 'a': [{'t': 'linear-gradient(red 0%, blue 100%);', 'c': True}, {'t': 'linear-gradient(red: 0%, blue: 100%);', 'c': False}, {'t': 'linear-gradient(red at 0%, blue at 100%);', 'c': False}, {'t': 'gradient(red 0%, blue 100%);', 'c': False}]},
    ]},

    {'n': 'Shadow - Soya', 't': 25, 'o': 19, 'q': [
        {'t': 'Matn soyasi qo\'shish uchun?', 'a': [{'t': 'text-shadow: 2px 2px 5px black;', 'c': True}, {'t': 'shadow: 2px 2px 5px black;', 'c': False}, {'t': 'text-shadow: black 2px 2px 5px;', 'c': False}, {'t': 'shadow-text: 2px 2px 5px black;', 'c': False}]},
        {'t': 'Box soyasi qo\'shish uchun?', 'a': [{'t': 'box-shadow: 2px 2px 5px black;', 'c': True}, {'t': 'shadow: 2px 2px 5px black;', 'c': False}, {'t': 'box-shadow: black 2px 2px 5px;', 'c': False}, {'t': 'shadow-box: 2px 2px 5px black;', 'c': False}]},
        {'t': 'box-shadow qiymatlari tartibi?', 'a': [{'t': 'x-offset y-offset blur spread color', 'c': True}, {'t': 'color x-offset y-offset blur', 'c': False}, {'t': 'blur spread x-offset y-offset color', 'c': False}, {'t': 'x-offset y-offset color blur', 'c': False}]},
        {'t': 'Ichki soya qo\'shish uchun?', 'a': [{'t': 'box-shadow: inset 2px 2px 5px black;', 'c': True}, {'t': 'box-shadow: inner 2px 2px 5px black;', 'c': False}, {'t': 'box-shadow: inside 2px 2px 5px black;', 'c': False}, {'t': 'inner-shadow: 2px 2px 5px black;', 'c': False}]},
        {'t': 'Bir nechta soya qo\'shish mumkinmi?', 'a': [{'t': 'Ha, vergul bilan ajratib', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Faqat 2 ta', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Transform - O\'zgartirish', 't': 30, 'o': 20, 'q': [
        {'t': 'transform xususiyati nima uchun?', 'a': [{'t': 'Elementni aylantirish, kattalashtirish, siljitish uchun', 'c': True}, {'t': 'Elementni o\'zgartirish uchun', 'c': False}, {'t': 'Rang o\'zgartirish uchun', 'c': False}, {'t': 'Matn o\'zgartirish uchun', 'c': False}]},
        {'t': 'Elementni aylantirish uchun?', 'a': [{'t': 'transform: rotate(45deg);', 'c': True}, {'t': 'rotate: 45deg;', 'c': False}, {'t': 'transform: turn(45deg);', 'c': False}, {'t': 'rotation: 45deg;', 'c': False}]},
        {'t': 'Elementni kattalashtirish uchun?', 'a': [{'t': 'transform: scale(1.5);', 'c': True}, {'t': 'scale: 1.5;', 'c': False}, {'t': 'transform: size(1.5);', 'c': False}, {'t': 'zoom: 1.5;', 'c': False}]},
        {'t': 'Elementni siljitish uchun?', 'a': [{'t': 'transform: translate(50px, 100px);', 'c': True}, {'t': 'translate: 50px, 100px;', 'c': False}, {'t': 'transform: move(50px, 100px);', 'c': False}, {'t': 'position: 50px, 100px;', 'c': False}]},
        {'t': 'Elementni egilish uchun?', 'a': [{'t': 'transform: skew(20deg, 10deg);', 'c': True}, {'t': 'skew: 20deg, 10deg;', 'c': False}, {'t': 'transform: bend(20deg, 10deg);', 'c': False}, {'t': 'tilt: 20deg, 10deg;', 'c': False}]},
        {'t': 'Bir nechta transform birlashtirish?', 'a': [{'t': 'transform: rotate(45deg) scale(1.5);', 'c': True}, {'t': 'transform: rotate(45deg), scale(1.5);', 'c': False}, {'t': 'rotate: 45deg; scale: 1.5;', 'c': False}, {'t': 'transform: rotate(45deg) + scale(1.5);', 'c': False}]},
        {'t': 'transform-origin nima qiladi?', 'a': [{'t': 'Transform markazini belgilaydi', 'c': True}, {'t': 'Transform tezligini belgilaydi', 'c': False}, {'t': 'Transform rangini belgilaydi', 'c': False}, {'t': 'Transform yo\'nalishini belgilaydi', 'c': False}]},
    ]},

    {'n': 'Transition - O\'tish effekti', 't': 30, 'o': 21, 'q': [
        {'t': 'transition xususiyati nima uchun?', 'a': [{'t': 'O\'zgarishlarni silliq animatsiya qilish uchun', 'c': True}, {'t': 'Elementni ko\'chirish uchun', 'c': False}, {'t': 'Rang o\'zgartirish uchun', 'c': False}, {'t': 'Matn o\'zgartirish uchun', 'c': False}]},
        {'t': 'transition qanday yoziladi?', 'a': [{'t': 'transition: property duration timing-function delay;', 'c': True}, {'t': 'transition: duration property;', 'c': False}, {'t': 'transition: property delay;', 'c': False}, {'t': 'transition: timing-function duration;', 'c': False}]},
        {'t': 'Barcha xususiyatlarga transition qo\'shish uchun?', 'a': [{'t': 'transition: all 0.3s;', 'c': True}, {'t': 'transition: * 0.3s;', 'c': False}, {'t': 'transition: everything 0.3s;', 'c': False}, {'t': 'transition-all: 0.3s;', 'c': False}]},
        {'t': 'transition-duration nima?', 'a': [{'t': 'O\'tish davomiyligi', 'c': True}, {'t': 'O\'tish kechikishi', 'c': False}, {'t': 'O\'tish tezligi', 'c': False}, {'t': 'O\'tish yo\'nalishi', 'c': False}]},
        {'t': 'transition-timing-function qiymatlari?', 'a': [{'t': 'ease, linear, ease-in, ease-out, ease-in-out, cubic-bezier', 'c': True}, {'t': 'Faqat linear', 'c': False}, {'t': 'fast, slow', 'c': False}, {'t': 'quick, normal', 'c': False}]},
        {'t': 'transition-delay nima?', 'a': [{'t': 'O\'tish boshlanishidan oldingi kechikish', 'c': True}, {'t': 'O\'tish davomiyligi', 'c': False}, {'t': 'O\'tish tezligi', 'c': False}, {'t': 'O\'tish yo\'nalishi', 'c': False}]},
        {'t': 'Bir nechta xususiyatga transition?', 'a': [{'t': 'transition: color 0.3s, transform 0.5s;', 'c': True}, {'t': 'transition: color, transform 0.3s;', 'c': False}, {'t': 'transition: 0.3s color transform;', 'c': False}, {'t': 'transition: all color transform;', 'c': False}]},
    ]},

    {'n': 'Animation - Animatsiya', 't': 30, 'o': 22, 'q': [
        {'t': 'CSS animatsiya yaratish uchun nima kerak?', 'a': [{'t': '@keyframes va animation xususiyati', 'c': True}, {'t': 'Faqat animation', 'c': False}, {'t': 'Faqat @keyframes', 'c': False}, {'t': 'JavaScript kerak', 'c': False}]},
        {'t': '@keyframes qanday yoziladi?', 'a': [{'t': '@keyframes nom { from {} to {} }', 'c': True}, {'t': 'keyframes nom { from {} to {} }', 'c': False}, {'t': '@animation nom { from {} to {} }', 'c': False}, {'t': 'animation nom { from {} to {} }', 'c': False}]},
        {'t': 'Animatsiyani elementga qo\'llash uchun?', 'a': [{'t': 'animation: nom 2s;', 'c': True}, {'t': 'keyframes: nom 2s;', 'c': False}, {'t': 'animate: nom 2s;', 'c': False}, {'t': '@animation: nom 2s;', 'c': False}]},
        {'t': 'animation-duration nima?', 'a': [{'t': 'Animatsiya davomiyligi', 'c': True}, {'t': 'Animatsiya kechikishi', 'c': False}, {'t': 'Animatsiya takrorlanishi', 'c': False}, {'t': 'Animatsiya yo\'nalishi', 'c': False}]},
        {'t': 'Animatsiyani cheksiz takrorlash uchun?', 'a': [{'t': 'animation-iteration-count: infinite;', 'c': True}, {'t': 'animation-repeat: infinite;', 'c': False}, {'t': 'animation-loop: infinite;', 'c': False}, {'t': 'animation: infinite;', 'c': False}]},
        {'t': 'animation-direction qiymatlari?', 'a': [{'t': 'normal, reverse, alternate, alternate-reverse', 'c': True}, {'t': 'Faqat normal va reverse', 'c': False}, {'t': 'forward, backward', 'c': False}, {'t': 'left, right', 'c': False}]},
        {'t': 'animation-fill-mode nima qiladi?', 'a': [{'t': 'Animatsiya tugagandan keyin element holatini belgilaydi', 'c': True}, {'t': 'Animatsiya rangini belgilaydi', 'c': False}, {'t': 'Animatsiya tezligini belgilaydi', 'c': False}, {'t': 'Animatsiya yo\'nalishini belgilaydi', 'c': False}]},
        {'t': '@keyframes da foizlar ishlatish mumkinmi?', 'a': [{'t': 'Ha, 0%, 50%, 100% kabi', 'c': True}, {'t': 'Yo\'q, faqat from va to', 'c': False}, {'t': 'Faqat 0% va 100%', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Pseudo-class selektorlar', 't': 30, 'o': 23, 'q': [
        {'t': 'Pseudo-class nima?', 'a': [{'t': 'Elementning maxsus holatini tanlash uchun selektor', 'c': True}, {'t': 'Yolg\'on class', 'c': False}, {'t': 'Maxsus element', 'c': False}, {'t': 'JavaScript funksiyasi', 'c': False}]},
        {'t': ':hover pseudo-class nima qiladi?', 'a': [{'t': 'Sichqoncha element ustida bo\'lganda stilni qo\'llaydi', 'c': True}, {'t': 'Element bosilganda', 'c': False}, {'t': 'Element tanlanganda', 'c': False}, {'t': 'Element ko\'rinmasa', 'c': False}]},
        {'t': ':active pseudo-class nima qiladi?', 'a': [{'t': 'Element bosilayotgan paytda stilni qo\'llaydi', 'c': True}, {'t': 'Element faol bo\'lganda', 'c': False}, {'t': 'Element ko\'rinayotganda', 'c': False}, {'t': 'Element yashiringanda', 'c': False}]},
        {'t': ':focus pseudo-class nima qiladi?', 'a': [{'t': 'Element fokusda bo\'lganda stilni qo\'llaydi', 'c': True}, {'t': 'Element bosilganda', 'c': False}, {'t': 'Element ko\'rinmasa', 'c': False}, {'t': 'Element yashiringanda', 'c': False}]},
        {'t': ':first-child nima qiladi?', 'a': [{'t': 'Birinchi bola elementni tanlaydi', 'c': True}, {'t': 'Oxirgi bola elementni tanlaydi', 'c': False}, {'t': 'Barcha bolalarni tanlaydi', 'c': False}, {'t': 'Ota elementni tanlaydi', 'c': False}]},
        {'t': ':last-child nima qiladi?', 'a': [{'t': 'Oxirgi bola elementni tanlaydi', 'c': True}, {'t': 'Birinchi bola elementni tanlaydi', 'c': False}, {'t': 'Barcha bolalarni tanlaydi', 'c': False}, {'t': 'Ota elementni tanlaydi', 'c': False}]},
        {'t': ':nth-child(2) nima qiladi?', 'a': [{'t': 'Ikkinchi bola elementni tanlaydi', 'c': True}, {'t': 'Birinchi bola elementni tanlaydi', 'c': False}, {'t': 'Oxirgi bola elementni tanlaydi', 'c': False}, {'t': 'Barcha bolalarni tanlaydi', 'c': False}]},
        {'t': ':nth-child(odd) nima qiladi?', 'a': [{'t': 'Toq tartibdagi bolalarni tanlaydi', 'c': True}, {'t': 'Juft tartibdagi bolalarni tanlaydi', 'c': False}, {'t': 'Barcha bolalarni tanlaydi', 'c': False}, {'t': 'Birinchi bolani tanlaydi', 'c': False}]},
    ]},

    {'n': 'Pseudo-element selektorlar', 't': 25, 'o': 24, 'q': [
        {'t': 'Pseudo-element nima?', 'a': [{'t': 'Elementning ma\'lum qismini stillashtirish uchun', 'c': True}, {'t': 'Yolg\'on element', 'c': False}, {'t': 'Maxsus class', 'c': False}, {'t': 'JavaScript obyekti', 'c': False}]},
        {'t': '::before pseudo-element nima qiladi?', 'a': [{'t': 'Element oldiga kontent qo\'shadi', 'c': True}, {'t': 'Element orqasiga kontent qo\'shadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Elementni yashiradi', 'c': False}]},
        {'t': '::after pseudo-element nima qiladi?', 'a': [{'t': 'Element orqasiga kontent qo\'shadi', 'c': True}, {'t': 'Element oldiga kontent qo\'shadi', 'c': False}, {'t': 'Elementni o\'chiradi', 'c': False}, {'t': 'Elementni yashiradi', 'c': False}]},
        {'t': '::before va ::after da content xususiyati majburiy?', 'a': [{'t': 'Ha, bo\'sh bo\'lsa ham content: ""; yozish kerak', 'c': True}, {'t': 'Yo\'q, ixtiyoriy', 'c': False}, {'t': 'Faqat ::before da', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': '::first-letter nima qiladi?', 'a': [{'t': 'Birinchi harfni stillashtiradi', 'c': True}, {'t': 'Oxirgi harfni stillashtiradi', 'c': False}, {'t': 'Barcha harflarni stillashtiradi', 'c': False}, {'t': 'Birinchi so\'zni stillashtiradi', 'c': False}]},
        {'t': '::first-line nima qiladi?', 'a': [{'t': 'Birinchi qatorni stillashtiradi', 'c': True}, {'t': 'Oxirgi qatorni stillashtiradi', 'c': False}, {'t': 'Barcha qatorlarni stillashtiradi', 'c': False}, {'t': 'Birinchi harfni stillashtiradi', 'c': False}]},
        {'t': '::selection nima qiladi?', 'a': [{'t': 'Tanlangan matnni stillashtiradi', 'c': True}, {'t': 'Barcha matnni stillashtiradi', 'c': False}, {'t': 'Birinchi matnni stillashtiradi', 'c': False}, {'t': 'Oxirgi matnni stillashtiradi', 'c': False}]},
    ]},

    {'n': 'Media Queries - Responsive dizayn', 't': 30, 'o': 25, 'q': [
        {'t': 'Media query nima uchun ishlatiladi?', 'a': [{'t': 'Turli ekran o\'lchamlariga moslashuvchi dizayn yaratish uchun', 'c': True}, {'t': 'Video qo\'shish uchun', 'c': False}, {'t': 'Audio qo\'shish uchun', 'c': False}, {'t': 'Rasm qo\'shish uchun', 'c': False}]},
        {'t': 'Media query qanday yoziladi?', 'a': [{'t': '@media (max-width: 768px) { }', 'c': True}, {'t': 'media (max-width: 768px) { }', 'c': False}, {'t': '@screen (max-width: 768px) { }', 'c': False}, {'t': 'responsive (max-width: 768px) { }', 'c': False}]},
        {'t': 'max-width nima bildiradi?', 'a': [{'t': 'Maksimal kenglik, shu o\'lchamgacha qo\'llanadi', 'c': True}, {'t': 'Minimal kenglik', 'c': False}, {'t': 'Aniq kenglik', 'c': False}, {'t': 'O\'rtacha kenglik', 'c': False}]},
        {'t': 'min-width nima bildiradi?', 'a': [{'t': 'Minimal kenglik, shu o\'lchamdan boshlab qo\'llanadi', 'c': True}, {'t': 'Maksimal kenglik', 'c': False}, {'t': 'Aniq kenglik', 'c': False}, {'t': 'O\'rtacha kenglik', 'c': False}]},
        {'t': 'Mobil qurilmalar uchun odatiy breakpoint?', 'a': [{'t': '768px yoki 480px', 'c': True}, {'t': '1920px', 'c': False}, {'t': '1024px', 'c': False}, {'t': '2560px', 'c': False}]},
        {'t': 'Bir nechta shartni birlashtirish uchun?', 'a': [{'t': '@media (min-width: 768px) and (max-width: 1024px)', 'c': True}, {'t': '@media (min-width: 768px) or (max-width: 1024px)', 'c': False}, {'t': '@media (min-width: 768px), (max-width: 1024px)', 'c': False}, {'t': '@media (min-width: 768px) + (max-width: 1024px)', 'c': False}]},
        {'t': 'Orientatsiyani tekshirish uchun?', 'a': [{'t': '@media (orientation: portrait) yoki (orientation: landscape)', 'c': True}, {'t': '@media (direction: vertical)', 'c': False}, {'t': '@media (rotate: 90deg)', 'c': False}, {'t': '@media (screen: vertical)', 'c': False}]},
        {'t': 'Mobile-first yondashuv nima?', 'a': [{'t': 'Avval mobil uchun yozib, keyin kattaroq ekranlar uchun qo\'shimcha stillar', 'c': True}, {'t': 'Avval desktop uchun yozish', 'c': False}, {'t': 'Faqat mobil uchun dizayn', 'c': False}, {'t': 'Faqat desktop uchun dizayn', 'c': False}]},
    ]},

    {'n': 'Flexbox va Grid - Amaliy', 't': 30, 'o': 26, 'q': [
        {'t': 'Navbar yaratish uchun qaysi layout yaxshi?', 'a': [{'t': 'Flexbox', 'c': True}, {'t': 'Float', 'c': False}, {'t': 'Position', 'c': False}, {'t': 'Table', 'c': False}]},
        {'t': 'Murakkab sahifa layouti uchun qaysi yaxshi?', 'a': [{'t': 'Grid', 'c': True}, {'t': 'Float', 'c': False}, {'t': 'Position', 'c': False}, {'t': 'Table', 'c': False}]},
        {'t': 'Elementni vertikal markazlashtirish uchun Flexbox da?', 'a': [{'t': 'align-items: center;', 'c': True}, {'t': 'justify-content: center;', 'c': False}, {'t': 'vertical-align: center;', 'c': False}, {'t': 'text-align: center;', 'c': False}]},
        {'t': 'Elementni gorizontal markazlashtirish uchun Flexbox da?', 'a': [{'t': 'justify-content: center;', 'c': True}, {'t': 'align-items: center;', 'c': False}, {'t': 'text-align: center;', 'c': False}, {'t': 'horizontal-align: center;', 'c': False}]},
        {'t': 'Teng bo\'lingan ustunlar uchun Grid da?', 'a': [{'t': 'grid-template-columns: repeat(3, 1fr);', 'c': True}, {'t': 'grid-columns: 3;', 'c': False}, {'t': 'columns: 3 equal;', 'c': False}, {'t': 'grid: 3 columns;', 'c': False}]},
        {'t': 'Responsive grid uchun?', 'a': [{'t': 'grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));', 'c': True}, {'t': 'grid-columns: responsive;', 'c': False}, {'t': 'grid: auto;', 'c': False}, {'t': 'responsive-grid: true;', 'c': False}]},
    ]},

    {'n': 'CSS Variables - O\'zgaruvchilar', 't': 25, 'o': 27, 'q': [
        {'t': 'CSS o\'zgaruvchisi qanday e\'lon qilinadi?', 'a': [{'t': '--rang: blue;', 'c': True}, {'t': '$rang: blue;', 'c': False}, {'t': 'var rang: blue;', 'c': False}, {'t': '@rang: blue;', 'c': False}]},
        {'t': 'CSS o\'zgaruvchisini qanday ishlatiladi?', 'a': [{'t': 'color: var(--rang);', 'c': True}, {'t': 'color: $rang;', 'c': False}, {'t': 'color: @rang;', 'c': False}, {'t': 'color: rang;', 'c': False}]},
        {'t': 'Global o\'zgaruvchilar qayerda e\'lon qilinadi?', 'a': [{'t': ':root { --rang: blue; }', 'c': True}, {'t': 'body { --rang: blue; }', 'c': False}, {'t': 'html { --rang: blue; }', 'c': False}, {'t': '* { --rang: blue; }', 'c': False}]},
        {'t': 'O\'zgaruvchiga standart qiymat berish?', 'a': [{'t': 'color: var(--rang, blue);', 'c': True}, {'t': 'color: var(--rang) or blue;', 'c': False}, {'t': 'color: var(--rang, default: blue);', 'c': False}, {'t': 'color: var(--rang || blue);', 'c': False}]},
        {'t': 'CSS o\'zgaruvchilari JavaScript dan o\'zgartirilishi mumkinmi?', 'a': [{'t': 'Ha, getComputedStyle va setProperty orqali', 'c': True}, {'t': 'Yo\'q, faqat CSS dan', 'c': False}, {'t': 'Faqat o\'qish mumkin', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'CSS Specificity - Ustunlik', 't': 25, 'o': 28, 'q': [
        {'t': 'CSS Specificity nima?', 'a': [{'t': 'Qaysi stil qoidasi ustun kelishini belgilovchi tizim', 'c': True}, {'t': 'CSS tezligi', 'c': False}, {'t': 'CSS xavfsizligi', 'c': False}, {'t': 'CSS murakkabligi', 'c': False}]},
        {'t': 'Specificity tartibi (kuchsizdan kuchlisiga)?', 'a': [{'t': 'Element < Class < ID < Inline style', 'c': True}, {'t': 'ID < Class < Element < Inline', 'c': False}, {'t': 'Class < ID < Element < Inline', 'c': False}, {'t': 'Inline < Element < Class < ID', 'c': False}]},
        {'t': 'ID selektorning specificity qiymati?', 'a': [{'t': '100', 'c': True}, {'t': '10', 'c': False}, {'t': '1', 'c': False}, {'t': '1000', 'c': False}]},
        {'t': 'Class selektorning specificity qiymati?', 'a': [{'t': '10', 'c': True}, {'t': '100', 'c': False}, {'t': '1', 'c': False}, {'t': '1000', 'c': False}]},
        {'t': 'Element selektorning specificity qiymati?', 'a': [{'t': '1', 'c': True}, {'t': '10', 'c': False}, {'t': '100', 'c': False}, {'t': '1000', 'c': False}]},
        {'t': '!important nima qiladi?', 'a': [{'t': 'Stilni eng yuqori ustunlikka ega qiladi', 'c': True}, {'t': 'Stilni muhim deb belgilaydi', 'c': False}, {'t': 'Stilni tezlashtiradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': '!important dan qochish kerakmi?', 'a': [{'t': 'Ha, faqat zarurat bo\'lganda ishlatish kerak', 'c': True}, {'t': 'Yo\'q, har doim ishlatish kerak', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Hech qachon ishlatmaslik kerak', 'c': False}]},
    ]},

    {'n': 'CSS Best Practices - Eng yaxshi amaliyotlar', 't': 30, 'o': 29, 'q': [
        {'t': 'CSS fayllarni qanday tashkil qilish yaxshi?', 'a': [{'t': 'Modulli va mantiqiy guruhlarga bo\'lib', 'c': True}, {'t': 'Bitta katta faylda', 'c': False}, {'t': 'Har bir element uchun alohida fayl', 'c': False}, {'t': 'Tasodifiy tartibda', 'c': False}]},
        {'t': 'Class nomlarini qanday yozish kerak?', 'a': [{'t': 'Ma\'noli va tushunarli nomlar bilan', 'c': True}, {'t': 'Qisqa va tushunarsiz', 'c': False}, {'t': 'Faqat raqamlar bilan', 'c': False}, {'t': 'Tasodifiy nomlar', 'c': False}]},
        {'t': 'BEM metodologiyasi nima?', 'a': [{'t': 'Block Element Modifier - class nomlash tizimi', 'c': True}, {'t': 'Best Element Method', 'c': False}, {'t': 'Basic Element Model', 'c': False}, {'t': 'Browser Element Manager', 'c': False}]},
        {'t': 'CSS minify qilish nima?', 'a': [{'t': 'Faylni kichiklashtirish, bo\'sh joylarni olib tashlash', 'c': True}, {'t': 'Faylni kattalashtirish', 'c': False}, {'t': 'Faylni o\'chirish', 'c': False}, {'t': 'Faylni shifrlash', 'c': False}]},
        {'t': 'CSS preprocessor nima?', 'a': [{'t': 'CSS ni kengaytiruvchi til (Sass, Less)', 'c': True}, {'t': 'CSS ni tezlashtiruvchi dastur', 'c': False}, {'t': 'CSS ni o\'chiruvchi dastur', 'c': False}, {'t': 'CSS ni tekshiruvchi dastur', 'c': False}]},
        {'t': 'Vendor prefixlar nima uchun?', 'a': [{'t': 'Turli brauzerlarda yangi xususiyatlarni qo\'llab-quvvatlash uchun', 'c': True}, {'t': 'Faylni kattalashtirish uchun', 'c': False}, {'t': 'Xavfsizlik uchun', 'c': False}, {'t': 'Tezlik uchun', 'c': False}]},
        {'t': 'CSS reset yoki normalize nima uchun?', 'a': [{'t': 'Brauzerlarning standart stillarini bir xil qilish uchun', 'c': True}, {'t': 'Barcha stillarni o\'chirish uchun', 'c': False}, {'t': 'Faylni tozalash uchun', 'c': False}, {'t': 'Xatoliklarni tuzatish uchun', 'c': False}]},
        {'t': 'Mobile-first yoki Desktop-first?', 'a': [{'t': 'Mobile-first zamonaviy yondashuv', 'c': True}, {'t': 'Desktop-first yaxshiroq', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Ikkalasi ham yomon', 'c': False}]},
    ]},

    {'n': 'CSS Kengaytirilgan mavzular', 't': 30, 'o': 30, 'q': [
        {'t': 'CSS Grid va Flexbox qachon ishlatiladi?', 'a': [{'t': 'Grid 2D layout uchun, Flexbox 1D layout uchun', 'c': True}, {'t': 'Faqat Grid ishlatiladi', 'c': False}, {'t': 'Faqat Flexbox ishlatiladi', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'CSS Custom Properties (variables) afzalliklari?', 'a': [{'t': 'Qayta ishlatish, JavaScript bilan integratsiya, dinamik o\'zgarishlar', 'c': True}, {'t': 'Faqat rang saqlash', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}, {'t': 'Faqat tezlik', 'c': False}]},
        {'t': 'CSS Containment nima?', 'a': [{'t': 'Brauzer render optimizatsiyasi uchun', 'c': True}, {'t': 'Elementni yashirish', 'c': False}, {'t': 'Elementni o\'chirish', 'c': False}, {'t': 'Rang berish', 'c': False}]},
        {'t': 'CSS Houdini nima?', 'a': [{'t': 'CSS ning past darajadagi API lari', 'c': True}, {'t': 'CSS framework', 'c': False}, {'t': 'CSS preprocessor', 'c': False}, {'t': 'CSS library', 'c': False}]},
        {'t': 'aspect-ratio xususiyati nima qiladi?', 'a': [{'t': 'Element nisbatini belgilaydi (masalan, 16:9)', 'c': True}, {'t': 'Element o\'lchamini belgilaydi', 'c': False}, {'t': 'Element rangini belgilaydi', 'c': False}, {'t': 'Element joylashuvini belgilaydi', 'c': False}]},
        {'t': 'clamp() funksiyasi nima qiladi?', 'a': [{'t': 'Minimal, ideal va maksimal qiymat orasida o\'lcham belgilaydi', 'c': True}, {'t': 'Elementni qisadi', 'c': False}, {'t': 'Elementni yopadi', 'c': False}, {'t': 'Rangni o\'zgartiradi', 'c': False}]},
        {'t': 'CSS Subgrid nima?', 'a': [{'t': 'Ichki grid ota grid bilan mos kelishi', 'c': True}, {'t': 'Kichik grid', 'c': False}, {'t': 'Yashirin grid', 'c': False}, {'t': 'Ikkinchi grid', 'c': False}]},
        {'t': 'CSS da dark mode qanday amalga oshiriladi?', 'a': [{'t': '@media (prefers-color-scheme: dark) va CSS variables', 'c': True}, {'t': 'Faqat JavaScript bilan', 'c': False}, {'t': 'Alohida CSS fayl', 'c': False}, {'t': 'Amalga oshirib bo\'lmaydi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_css()
    add_topics(subj, T)
    print(f"\n✅ CSS: {len(T)} ta mavzu muvaffaqiyatli qo\'shildi!")
