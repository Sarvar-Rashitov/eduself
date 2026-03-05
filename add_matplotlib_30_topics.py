"""
MATPLOTLIB - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_matplotlib():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Matplotlib', defaults={'category': cat, 'description': 'Matplotlib - Python uchun grafik va vizualizatsiya kutubxonasi', 'icon': 'bi-bar-chart', 'order': 30, 'is_active': True})
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
    {'n': 'Matplotlib ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Matplotlib nima?', 'a': [{'t': 'Python uchun grafik va vizualizatsiya kutubxonasi', 'c': True}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Web framework', 'c': False}, {'t': 'Matematik kutubxona', 'c': False}]},
        {'t': 'Matplotlib nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlarni grafik ko\'rinishda tasvirlash uchun', 'c': True}, {'t': 'Fayllar bilan ishlash uchun', 'c': False}, {'t': 'Web sahifa yaratish uchun', 'c': False}, {'t': 'Ma\'lumotlar bazasi bilan ishlash uchun', 'c': False}]},
        {'t': 'Matplotlib qaysi dasturlash tili uchun?', 'a': [{'t': 'Python', 'c': True}, {'t': 'JavaScript', 'c': False}, {'t': 'Java', 'c': False}, {'t': 'C++', 'c': False}]},
        {'t': 'Matplotlib qanday grafiklar yaratishi mumkin?', 'a': [{'t': 'Chiziqli, ustunli, doira va boshqa ko\'p turli grafiklar', 'c': True}, {'t': 'Faqat chiziqli grafiklar', 'c': False}, {'t': 'Faqat doira grafiklar', 'c': False}, {'t': 'Grafik yarata olmaydi', 'c': False}]},
        {'t': 'Matplotlib kim tomonidan yaratilgan?', 'a': [{'t': 'John Hunter', 'c': True}, {'t': 'Guido van Rossum', 'c': False}, {'t': 'Wes McKinney', 'c': False}, {'t': 'Travis Oliphant', 'c': False}]},
    ]},

    {'n': 'Matplotlib o\'rnatish va import qilish', 't': 20, 'o': 2, 'q': [
        {'t': 'Matplotlib qanday o\'rnatiladi?', 'a': [{'t': 'pip install matplotlib', 'c': True}, {'t': 'npm install matplotlib', 'c': False}, {'t': 'apt-get install matplotlib', 'c': False}, {'t': 'O\'rnatish shart emas', 'c': False}]},
        {'t': 'Matplotlib.pyplot ni qanday import qilish kerak?', 'a': [{'t': 'import matplotlib.pyplot as plt', 'c': True}, {'t': 'import plt', 'c': False}, {'t': 'from matplotlib import *', 'c': False}, {'t': 'include matplotlib', 'c': False}]},
        {'t': 'Nima uchun "as plt" ishlatiladi?', 'a': [{'t': 'Qisqa nom bilan ishlash qulay', 'c': True}, {'t': 'Majburiy', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xavfsizlik uchun', 'c': False}]},
        {'t': 'Matplotlib versiyasini qanday tekshirish mumkin?', 'a': [{'t': 'import matplotlib; matplotlib.__version__', 'c': True}, {'t': 'plt.version()', 'c': False}, {'t': 'matplotlib --version', 'c': False}, {'t': 'print(matplotlib)', 'c': False}]},
        {'t': 'pyplot moduli nima?', 'a': [{'t': 'Matplotlib ning asosiy interfeysi, MATLAB ga o\'xshash', 'c': True}, {'t': 'Alohida kutubxona', 'c': False}, {'t': 'Faqat 3D grafiklar uchun', 'c': False}, {'t': 'Eskirgan modul', 'c': False}]},
    ]},

    {'n': 'Birinchi grafik - plt.plot()', 't': 25, 'o': 3, 'q': [
        {'t': 'plt.plot([1, 2, 3, 4]) nima qiladi?', 'a': [{'t': 'Oddiy chiziqli grafik yaratadi', 'c': True}, {'t': 'Ustunli grafik yaratadi', 'c': False}, {'t': 'Doira grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Grafikni ko\'rsatish uchun qaysi funksiya kerak?', 'a': [{'t': 'plt.show()', 'c': True}, {'t': 'plt.display()', 'c': False}, {'t': 'plt.view()', 'c': False}, {'t': 'plt.open()', 'c': False}]},
        {'t': 'plt.plot(x, y) da x va y nima?', 'a': [{'t': 'x - gorizontal, y - vertikal koordinatalar', 'c': True}, {'t': 'x - vertikal, y - gorizontal', 'c': False}, {'t': 'Ikkalasi ham bir xil', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'plt.plot() ga faqat bitta list berilsa nima bo\'ladi?', 'a': [{'t': 'Y qiymatlari sifatida qabul qilinadi, X avtomatik yaratiladi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Grafik chizilmaydi', 'c': False}, {'t': 'X qiymatlari sifatida qabul qilinadi', 'c': False}]},
        {'t': 'Bir nechta chiziq chizish uchun nima qilish kerak?', 'a': [{'t': 'plt.plot() ni bir necha marta chaqirish', 'c': True}, {'t': 'Faqat bitta chiziq chizish mumkin', 'c': False}, {'t': 'Alohida oyna ochish kerak', 'c': False}, {'t': 'Matplotlib buni qo\'llab-quvvatlamaydi', 'c': False}]},
        {'t': 'plt.plot() qaysi turdagi grafik yaratadi?', 'a': [{'t': 'Chiziqli grafik (line plot)', 'c': True}, {'t': 'Ustunli grafik', 'c': False}, {'t': 'Tarqalish grafigi', 'c': False}, {'t': 'Doira grafik', 'c': False}]},
    ]},

    {'n': 'Grafik uslubi - rang, chiziq turi', 't': 25, 'o': 4, 'q': [
        {'t': 'plt.plot(x, y, \'r\') da \'r\' nima?', 'a': [{'t': 'Qizil rang (red)', 'c': True}, {'t': 'Yashil rang', 'c': False}, {'t': 'Chiziq turi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'plt.plot(x, y, \'--\') nima qiladi?', 'a': [{'t': 'Uzuq chiziq chizadi', 'c': True}, {'t': 'Qizil chiziq chizadi', 'c': False}, {'t': 'Ikki marta chizadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.plot(x, y, \'ro--\') nima bildiradi?', 'a': [{'t': 'Qizil rang, doira marker, uzuq chiziq', 'c': True}, {'t': 'Faqat qizil rang', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Faqat uzuq chiziq', 'c': False}]},
        {'t': 'color parametri nima uchun?', 'a': [{'t': 'Chiziq rangini belgilash uchun', 'c': True}, {'t': 'Fon rangini o\'zgartirish uchun', 'c': False}, {'t': 'Matn rangini o\'zgartirish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'linewidth yoki lw parametri nima?', 'a': [{'t': 'Chiziq qalinligini belgilaydi', 'c': True}, {'t': 'Chiziq uzunligini belgilaydi', 'c': False}, {'t': 'Chiziq rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Qaysi ranglar qisqa kod bilan mavjud?', 'a': [{'t': 'r(qizil), g(yashil), b(ko\'k), k(qora) va boshqalar', 'c': True}, {'t': 'Faqat qizil va ko\'k', 'c': False}, {'t': 'Hech qanday rang yo\'q', 'c': False}, {'t': 'Faqat qora', 'c': False}]},
    ]},

    {'n': 'Marker va nuqta uslublari', 't': 25, 'o': 5, 'q': [
        {'t': 'marker parametri nima uchun?', 'a': [{'t': 'Ma\'lumot nuqtalarini belgilash uchun', 'c': True}, {'t': 'Chiziq rangini belgilash uchun', 'c': False}, {'t': 'Grafik nomini yozish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'marker=\'o\' nima qiladi?', 'a': [{'t': 'Doira shaklidagi markerlar qo\'yadi', 'c': True}, {'t': 'Kvadrat markerlar qo\'yadi', 'c': False}, {'t': 'Uchburchak markerlar qo\'yadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'markersize yoki ms parametri nima?', 'a': [{'t': 'Marker o\'lchamini belgilaydi', 'c': True}, {'t': 'Marker rangini belgilaydi', 'c': False}, {'t': 'Marker sonini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'markerfacecolor nima?', 'a': [{'t': 'Marker ichki rangini belgilaydi', 'c': True}, {'t': 'Marker tashqi rangini belgilaydi', 'c': False}, {'t': 'Fon rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'markeredgecolor nima?', 'a': [{'t': 'Marker chegarasi rangini belgilaydi', 'c': True}, {'t': 'Marker ichki rangini belgilaydi', 'c': False}, {'t': 'Chiziq rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Grafik sarlavha va yorliqlar', 't': 25, 'o': 6, 'q': [
        {'t': 'plt.title() nima qiladi?', 'a': [{'t': 'Grafik sarlavhasini qo\'shadi', 'c': True}, {'t': 'X o\'qi nomini qo\'shadi', 'c': False}, {'t': 'Y o\'qi nomini qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.xlabel() nima uchun?', 'a': [{'t': 'X o\'qi nomini belgilash uchun', 'c': True}, {'t': 'Y o\'qi nomini belgilash uchun', 'c': False}, {'t': 'Sarlavha qo\'shish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.ylabel() nima?', 'a': [{'t': 'Y o\'qi nomini belgilaydi', 'c': True}, {'t': 'X o\'qi nomini belgilaydi', 'c': False}, {'t': 'Sarlavha qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Sarlavhada shrift o\'lchamini qanday o\'zgartirish mumkin?', 'a': [{'t': 'fontsize parametri bilan', 'c': True}, {'t': 'size parametri bilan', 'c': False}, {'t': 'O\'zgartirish mumkin emas', 'c': False}, {'t': 'font parametri bilan', 'c': False}]},
        {'t': 'plt.title("Grafik", fontsize=20) nima qiladi?', 'a': [{'t': '20 o\'lchamli shrift bilan sarlavha qo\'shadi', 'c': True}, {'t': '20 ta sarlavha qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Yorliqlar (labels) nima uchun muhim?', 'a': [{'t': 'Grafik ma\'lumotlarini tushunish oson bo\'ladi', 'c': True}, {'t': 'Grafik chiroyliroq bo\'ladi', 'c': False}, {'t': 'Majburiy emas', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
    ]},

    {'n': 'Legend - grafik izohlar', 't': 30, 'o': 7, 'q': [
        {'t': 'plt.legend() nima qiladi?', 'a': [{'t': 'Grafik izohlarini (legend) ko\'rsatadi', 'c': True}, {'t': 'Sarlavha qo\'shadi', 'c': False}, {'t': 'Grafikni saqlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Legend uchun label qanday beriladi?', 'a': [{'t': 'plt.plot(x, y, label="Nom")', 'c': True}, {'t': 'plt.label("Nom")', 'c': False}, {'t': 'plt.legend("Nom")', 'c': False}, {'t': 'Avtomatik beriladi', 'c': False}]},
        {'t': 'plt.legend(loc="upper right") da loc nima?', 'a': [{'t': 'Legend joylashuvini belgilaydi', 'c': True}, {'t': 'Legend rangini belgilaydi', 'c': False}, {'t': 'Legend o\'lchamini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Legend joylashuvi uchun qanday qiymatlar mavjud?', 'a': [{'t': 'upper/lower/center left/right, best va boshqalar', 'c': True}, {'t': 'Faqat left va right', 'c': False}, {'t': 'Faqat top va bottom', 'c': False}, {'t': 'Joylashuvni belgilab bo\'lmaydi', 'c': False}]},
        {'t': 'loc="best" nima qiladi?', 'a': [{'t': 'Eng mos joyni avtomatik tanlaydi', 'c': True}, {'t': 'Eng yuqori o\'ngga qo\'yadi', 'c': False}, {'t': 'Markazga qo\'yadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Bir nechta chiziq bo\'lsa legend kerakmi?', 'a': [{'t': 'Ha, chiziqlarni farqlash uchun juda foydali', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Faqat 3 tadan ortiq chiziq bo\'lsa', 'c': False}, {'t': 'Majburiy', 'c': False}]},
        {'t': 'Legend shriftini qanday o\'zgartirish mumkin?', 'a': [{'t': 'fontsize parametri bilan', 'c': True}, {'t': 'font parametri bilan', 'c': False}, {'t': 'O\'zgartirish mumkin emas', 'c': False}, {'t': 'size parametri bilan', 'c': False}]},
    ]},

    {'n': 'Grid - koordinata to\'ri', 't': 25, 'o': 8, 'q': [
        {'t': 'plt.grid() nima qiladi?', 'a': [{'t': 'Grafik foniga koordinata to\'rini qo\'shadi', 'c': True}, {'t': 'Grafikni o\'chiradi', 'c': False}, {'t': 'Yangi grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Grid nima uchun foydali?', 'a': [{'t': 'Qiymatlarni aniqroq o\'qish uchun', 'c': True}, {'t': 'Grafik chiroyliroq bo\'ladi', 'c': False}, {'t': 'Majburiy element', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
        {'t': 'plt.grid(True) va plt.grid() farqi nima?', 'a': [{'t': 'Farq yo\'q, ikkalasi ham gridni yoqadi', 'c': True}, {'t': 'True bilan tezroq ishlaydi', 'c': False}, {'t': 'True bilan xato beradi', 'c': False}, {'t': 'Butunlay boshqacha', 'c': False}]},
        {'t': 'plt.grid(False) nima qiladi?', 'a': [{'t': 'Gridni o\'chiradi', 'c': True}, {'t': 'Gridni yoqadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Grid chiziqlarining uslubini o\'zgartirish mumkinmi?', 'a': [{'t': 'Ha, linestyle, color, alpha parametrlari bilan', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat rangini', 'c': False}, {'t': 'Faqat qalinligini', 'c': False}]},
        {'t': 'plt.grid(alpha=0.3) da alpha nima?', 'a': [{'t': 'Grid chiziqlarining shaffofligini belgilaydi', 'c': True}, {'t': 'Grid qalinligini belgilaydi', 'c': False}, {'t': 'Grid rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Grafikni saqlash - plt.savefig()', 't': 25, 'o': 9, 'q': [
        {'t': 'plt.savefig() nima qiladi?', 'a': [{'t': 'Grafikni fayl sifatida saqlaydi', 'c': True}, {'t': 'Grafikni ko\'rsatadi', 'c': False}, {'t': 'Grafikni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.savefig("grafik.png") qanday formatda saqlaydi?', 'a': [{'t': 'PNG format', 'c': True}, {'t': 'JPG format', 'c': False}, {'t': 'PDF format', 'c': False}, {'t': 'TXT format', 'c': False}]},
        {'t': 'Matplotlib qaysi formatlarni qo\'llab-quvvatlaydi?', 'a': [{'t': 'PNG, JPG, PDF, SVG va boshqalar', 'c': True}, {'t': 'Faqat PNG', 'c': False}, {'t': 'Faqat JPG', 'c': False}, {'t': 'Faqat PDF', 'c': False}]},
        {'t': 'dpi parametri nima?', 'a': [{'t': 'Rasm sifatini (dots per inch) belgilaydi', 'c': True}, {'t': 'Rasm o\'lchamini belgilaydi', 'c': False}, {'t': 'Rasm rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.savefig() ni qachon chaqirish kerak?', 'a': [{'t': 'plt.show() dan oldin', 'c': True}, {'t': 'plt.show() dan keyin', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'bbox_inches="tight" nima qiladi?', 'a': [{'t': 'Ortiqcha bo\'sh joylarni olib tashlaydi', 'c': True}, {'t': 'Rasmni kichraytiradi', 'c': False}, {'t': 'Rasmni kattalashtirad', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Scatter plot - tarqalish grafigi', 't': 30, 'o': 10, 'q': [
        {'t': 'plt.scatter() nima qiladi?', 'a': [{'t': 'Tarqalish grafigini (scatter plot) yaratadi', 'c': True}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Ustunli grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Scatter plot qachon ishlatiladi?', 'a': [{'t': 'Ikki o\'zgaruvchi orasidagi bog\'lanishni ko\'rish uchun', 'c': True}, {'t': 'Vaqt bo\'yicha o\'zgarishni ko\'rish uchun', 'c': False}, {'t': 'Kategoriyalarni solishtirish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'plt.scatter() va plt.plot() farqi nima?', 'a': [{'t': 'scatter nuqtalar, plot chiziqlar chizadi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'scatter tezroq', 'c': False}, {'t': 'plot yangi', 'c': False}]},
        {'t': 's parametri scatter da nima?', 'a': [{'t': 'Nuqta o\'lchamini belgilaydi', 'c': True}, {'t': 'Nuqta rangini belgilaydi', 'c': False}, {'t': 'Nuqta sonini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'c parametri scatter da nima?', 'a': [{'t': 'Nuqta rangini belgilaydi', 'c': True}, {'t': 'Nuqta o\'lchamini belgilaydi', 'c': False}, {'t': 'Nuqta shaklini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'alpha parametri nima?', 'a': [{'t': 'Nuqtalarning shaffofligini belgilaydi', 'c': True}, {'t': 'Nuqta o\'lchamini belgilaydi', 'c': False}, {'t': 'Nuqta rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Scatter plot da har bir nuqta turli rangda bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, c parametriga list berish mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat 2 rang', 'c': False}, {'t': 'Faqat qora va oq', 'c': False}]},
    ]},
    {'n': 'Bar plot - ustunli grafik', 't': 30, 'o': 11, 'q': [
        {'t': 'plt.bar() nima qiladi?', 'a': [{'t': 'Ustunli grafik (bar chart) yaratadi', 'c': True}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Doira grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Bar plot qachon ishlatiladi?', 'a': [{'t': 'Kategoriyalarni solishtirish uchun', 'c': True}, {'t': 'Vaqt bo\'yicha o\'zgarishni ko\'rish uchun', 'c': False}, {'t': 'Bog\'lanishni ko\'rish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'plt.bar(x, height) da height nima?', 'a': [{'t': 'Ustunlar balandligi', 'c': True}, {'t': 'Ustunlar kengligi', 'c': False}, {'t': 'Ustunlar soni', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'width parametri nima?', 'a': [{'t': 'Ustunlar kengligini belgilaydi', 'c': True}, {'t': 'Ustunlar balandligini belgilaydi', 'c': False}, {'t': 'Ustunlar rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.barh() nima qiladi?', 'a': [{'t': 'Gorizontal ustunli grafik yaratadi', 'c': True}, {'t': 'Vertikal ustunli grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Ustunlar rangini qanday o\'zgartirish mumkin?', 'a': [{'t': 'color parametri bilan', 'c': True}, {'t': 'O\'zgartirish mumkin emas', 'c': False}, {'t': 'Faqat qora rangda bo\'ladi', 'c': False}, {'t': 'bgcolor parametri bilan', 'c': False}]},
        {'t': 'Har bir ustun turli rangda bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, color parametriga list berish mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat 2 rang', 'c': False}, {'t': 'Faqat bir rang', 'c': False}]},
    ]},

    {'n': 'Histogram - taqsimot grafigi', 't': 30, 'o': 12, 'q': [
        {'t': 'plt.hist() nima qiladi?', 'a': [{'t': 'Histogram (taqsimot grafigi) yaratadi', 'c': True}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Ustunli grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Histogram nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlar taqsimotini ko\'rish uchun', 'c': True}, {'t': 'Kategoriyalarni solishtirish uchun', 'c': False}, {'t': 'Bog\'lanishni ko\'rish uchun', 'c': False}, {'t': 'Vaqtni ko\'rsatish uchun', 'c': False}]},
        {'t': 'bins parametri nima?', 'a': [{'t': 'Histogram ustunlari (oraliqlar) sonini belgilaydi', 'c': True}, {'t': 'Ma\'lumotlar sonini belgilaydi', 'c': False}, {'t': 'Grafik rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.hist(data, bins=20) nima qiladi?', 'a': [{'t': '20 ta oraliqqa bo\'lib histogram yaratadi', 'c': True}, {'t': '20 ta ma\'lumot oladi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Histogram va bar plot farqi nima?', 'a': [{'t': 'Histogram uzluksiz ma\'lumotlar, bar kategorik ma\'lumotlar uchun', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Histogram yangi', 'c': False}, {'t': 'Bar tezroq', 'c': False}]},
        {'t': 'edgecolor parametri nima?', 'a': [{'t': 'Ustunlar chegarasi rangini belgilaydi', 'c': True}, {'t': 'Ustunlar ichki rangini belgilaydi', 'c': False}, {'t': 'Fon rangini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Subplots - bir nechta grafik', 't': 35, 'o': 14, 'q': [
        {'t': 'plt.subplot() nima qiladi?', 'a': [{'t': 'Bir oynada bir nechta grafik yaratish imkonini beradi', 'c': True}, {'t': 'Yangi oyna ochadi', 'c': False}, {'t': 'Grafikni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.subplot(2, 3, 1) raqamlari nimani bildiradi?', 'a': [{'t': '2 qator, 3 ustun, 1-pozitsiya', 'c': True}, {'t': '2 grafik, 3 rang, 1 o\'lcham', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'plt.subplots() nima qaytaradi?', 'a': [{'t': 'Figure va axes obyektlarini', 'c': True}, {'t': 'Faqat grafik', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'fig, ax = plt.subplots(2, 2) nima yaratadi?', 'a': [{'t': '2x2 = 4 ta grafik joyi', 'c': True}, {'t': '2 ta grafik', 'c': False}, {'t': '4 ta alohida oyna', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Subplot da har bir grafik uchun alohida sarlavha qo\'yish mumkinmi?', 'a': [{'t': 'Ha, har bir subplot uchun alohida', 'c': True}, {'t': 'Yo\'q, faqat bitta sarlavha', 'c': False}, {'t': 'Faqat birinchi grafik uchun', 'c': False}, {'t': 'Mumkin emas', 'c': False}]},
        {'t': 'plt.tight_layout() nima qiladi?', 'a': [{'t': 'Subplotlar orasidagi bo\'shliqni avtomatik sozlaydi', 'c': True}, {'t': 'Grafikni kichraytiradi', 'c': False}, {'t': 'Grafikni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Subplot nima uchun foydali?', 'a': [{'t': 'Bir nechta grafikni solishtirish oson', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam joy egallaydi', 'c': False}, {'t': 'Majburiy', 'c': False}]},
    ]},

    {'n': 'Figure va Axes - OOP uslubi', 't': 35, 'o': 15, 'q': [
        {'t': 'Figure nima?', 'a': [{'t': 'Butun grafik oynasi (container)', 'c': True}, {'t': 'Bitta grafik', 'c': False}, {'t': 'Grafik ma\'lumotlari', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Axes nima?', 'a': [{'t': 'Figure ichidagi bitta grafik maydoni', 'c': True}, {'t': 'X va Y o\'qlari', 'c': False}, {'t': 'Grafik sarlavhasi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'fig, ax = plt.subplots() da ax nima?', 'a': [{'t': 'Axes obyekti', 'c': True}, {'t': 'Figure obyekti', 'c': False}, {'t': 'Ma\'lumotlar', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'ax.plot() va plt.plot() farqi nima?', 'a': [{'t': 'ax.plot() OOP uslubi, plt.plot() MATLAB uslubi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'ax.plot() tezroq', 'c': False}, {'t': 'plt.plot() yangi', 'c': False}]},
        {'t': 'Qaysi uslub tavsiya etiladi?', 'a': [{'t': 'OOP uslubi (fig, ax) murakkab grafiklar uchun yaxshi', 'c': True}, {'t': 'Faqat plt uslubi', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Ikkalasi ham yomon', 'c': False}]},
        {'t': 'ax.set_xlabel() nima qiladi?', 'a': [{'t': 'X o\'qi nomini belgilaydi', 'c': True}, {'t': 'Y o\'qi nomini belgilaydi', 'c': False}, {'t': 'Sarlavha qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'fig.suptitle() nima?', 'a': [{'t': 'Butun figure uchun sarlavha', 'c': True}, {'t': 'Bitta axes uchun sarlavha', 'c': False}, {'t': 'X o\'qi nomi', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},


    {'n': 'Xlim va Ylim - o\'q chegaralari', 't': 25, 'o': 16, 'q': [
        {'t': 'plt.xlim() nima qiladi?', 'a': [{'t': 'X o\'qi chegaralarini belgilaydi', 'c': True}, {'t': 'Y o\'qi chegaralarini belgilaydi', 'c': False}, {'t': 'Grafik o\'lchamini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.ylim(0, 100) nima qiladi?', 'a': [{'t': 'Y o\'qini 0 dan 100 gacha cheklaydi', 'c': True}, {'t': 'X o\'qini 0 dan 100 gacha cheklaydi', 'c': False}, {'t': '100 ta nuqta chizadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'O\'q chegaralarini nima uchun o\'zgartirish kerak?', 'a': [{'t': 'Muhim qismni yaxshiroq ko\'rsatish uchun', 'c': True}, {'t': 'Majburiy', 'c': False}, {'t': 'Grafik chiroyliroq bo\'ladi', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'ax.set_xlim() va plt.xlim() farqi nima?', 'a': [{'t': 'Birinchisi OOP, ikkinchisi MATLAB uslubi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'ax.set_xlim() xato', 'c': False}, {'t': 'plt.xlim() eskirgan', 'c': False}]},
        {'t': 'Avtomatik chegaralarni qaytarish mumkinmi?', 'a': [{'t': 'Ha, plt.autoscale() bilan', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat qayta ishga tushirish bilan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Xticks va Yticks - o\'q belgilari', 't': 30, 'o': 17, 'q': [
        {'t': 'plt.xticks() nima qiladi?', 'a': [{'t': 'X o\'qidagi belgilarni sozlaydi', 'c': True}, {'t': 'Y o\'qidagi belgilarni sozlaydi', 'c': False}, {'t': 'Grafik sarlavhasini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.xticks([0, 1, 2], ["A", "B", "C"]) nima qiladi?', 'a': [{'t': '0, 1, 2 pozitsiyalariga A, B, C yozadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat raqamlarni ko\'rsatadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Ticks nima uchun foydali?', 'a': [{'t': 'O\'qlarni tushunarli qilish uchun', 'c': True}, {'t': 'Grafik tezroq chiziladi', 'c': False}, {'t': 'Majburiy element', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
        {'t': 'rotation parametri nima?', 'a': [{'t': 'Belgilarni burishni belgilaydi', 'c': True}, {'t': 'Grafik ni aylantirad', 'c': False}, {'t': 'Belgilar sonini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.xticks(rotation=45) nima qiladi?', 'a': [{'t': 'X o\'qi belgilarini 45 gradusga buradi', 'c': True}, {'t': 'Grafikni 45 gradusga buradi', 'c': False}, {'t': '45 ta belgi qo\'yadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Belgilarni butunlay o\'chirish mumkinmi?', 'a': [{'t': 'Ha, plt.xticks([]) bilan', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat yashirish mumkin', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Annotate - izohlar qo\'shish', 't': 30, 'o': 18, 'q': [
        {'t': 'plt.annotate() nima qiladi?', 'a': [{'t': 'Grafik ustiga izoh (annotation) qo\'shadi', 'c': True}, {'t': 'Sarlavha qo\'shadi', 'c': False}, {'t': 'Legend qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Annotate nima uchun kerak?', 'a': [{'t': 'Muhim nuqtalarni ta\'kidlash uchun', 'c': True}, {'t': 'Grafik chiroyliroq bo\'ladi', 'c': False}, {'t': 'Majburiy element', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'xy parametri nima?', 'a': [{'t': 'Izoh qo\'yiladigan nuqta koordinatalari', 'c': True}, {'t': 'Izoh matni', 'c': False}, {'t': 'Izoh rangi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'xytext parametri nima?', 'a': [{'t': 'Izoh matni joylashuvi', 'c': True}, {'t': 'Izoh nuqtasi', 'c': False}, {'t': 'Izoh rangi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'arrowprops nima uchun?', 'a': [{'t': 'Strelka xususiyatlarini belgilash uchun', 'c': True}, {'t': 'Matn xususiyatlarini belgilash uchun', 'c': False}, {'t': 'Grafik xususiyatlarini belgilash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Bir grafikda bir nechta annotate bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, istalgancha', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Maksimum 3 ta', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Text - matn qo\'shish', 't': 25, 'o': 19, 'q': [
        {'t': 'plt.text() nima qiladi?', 'a': [{'t': 'Grafik ustiga matn qo\'shadi', 'c': True}, {'t': 'Sarlavha qo\'shadi', 'c': False}, {'t': 'Legend qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'plt.text(x, y, "Matn") parametrlari nima?', 'a': [{'t': 'x, y - pozitsiya, "Matn" - ko\'rsatiladigan matn', 'c': True}, {'t': 'Faqat matn', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'plt.text() va plt.annotate() farqi nima?', 'a': [{'t': 'annotate strelka qo\'shishi mumkin, text oddiy matn', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'text yangi', 'c': False}, {'t': 'annotate eskirgan', 'c': False}]},
        {'t': 'fontsize parametri nima?', 'a': [{'t': 'Matn shrift o\'lchamini belgilaydi', 'c': True}, {'t': 'Matn rangini belgilaydi', 'c': False}, {'t': 'Matn pozitsiyasini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'ha va va parametrlari nima?', 'a': [{'t': 'Gorizontal va vertikal tekislash (alignment)', 'c': True}, {'t': 'Matn rangi', 'c': False}, {'t': 'Matn o\'lchami', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Style - grafik uslublari', 't': 30, 'o': 20, 'q': [
        {'t': 'plt.style.use() nima qiladi?', 'a': [{'t': 'Tayyor grafik uslubini qo\'llaydi', 'c': True}, {'t': 'Yangi grafik yaratadi', 'c': False}, {'t': 'Grafikni saqlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Matplotlib da qanday tayyor uslublar bor?', 'a': [{'t': 'ggplot, seaborn, dark_background va boshqalar', 'c': True}, {'t': 'Faqat default', 'c': False}, {'t': 'Hech qanday uslub yo\'q', 'c': False}, {'t': 'Faqat bitta', 'c': False}]},
        {'t': 'plt.style.available nima qaytaradi?', 'a': [{'t': 'Mavjud barcha uslublar ro\'yxatini', 'c': True}, {'t': 'Joriy uslubni', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'plt.style.use("ggplot") nima qiladi?', 'a': [{'t': 'ggplot uslubini qo\'llaydi', 'c': True}, {'t': 'ggplot kutubxonasini import qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Style nima uchun foydali?', 'a': [{'t': 'Grafiklar professional va chiroyli ko\'rinadi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}]},
        {'t': 'O\'z uslubingizni yaratish mumkinmi?', 'a': [{'t': 'Ha, .mplstyle fayl yaratish mumkin', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat tayyor uslublar', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},


    {'n': 'Colormap - rang xaritalari', 't': 30, 'o': 21, 'q': [
        {'t': 'Colormap nima?', 'a': [{'t': 'Qiymatlarni ranglarga mos keltiradigan xarita', 'c': True}, {'t': 'Oddiy rang', 'c': False}, {'t': 'Grafik turi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Colormap qachon ishlatiladi?', 'a': [{'t': 'Qiymatlarni rang orqali ko\'rsatish kerak bo\'lganda', 'c': True}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat 3D grafiklar uchun', 'c': False}]},
        {'t': 'cmap parametri nima?', 'a': [{'t': 'Colormap nomini belgilaydi', 'c': True}, {'t': 'Rang nomini belgilaydi', 'c': False}, {'t': 'Grafik nomini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Qanday mashhur colormaplar bor?', 'a': [{'t': 'viridis, plasma, jet, coolwarm va boshqalar', 'c': True}, {'t': 'Faqat rainbow', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Faqat bitta', 'c': False}]},
        {'t': 'plt.colorbar() nima qiladi?', 'a': [{'t': 'Colormap shkalasini ko\'rsatadi', 'c': True}, {'t': 'Yangi rang qo\'shadi', 'c': False}, {'t': 'Grafikni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Colorbar nima uchun kerak?', 'a': [{'t': 'Ranglar qanday qiymatlarni bildirishi tushunarli bo\'ladi', 'c': True}, {'t': 'Grafik chiroyliroq bo\'ladi', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
    ]},

    {'n': 'Contour plot - kontur grafigi', 't': 30, 'o': 22, 'q': [
        {'t': 'plt.contour() nima qiladi?', 'a': [{'t': 'Kontur (izogipsa) grafigi yaratadi', 'c': True}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Ustunli grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Contour plot qachon ishlatiladi?', 'a': [{'t': '3D ma\'lumotlarni 2D da ko\'rsatish uchun', 'c': True}, {'t': 'Oddiy chiziqlar uchun', 'c': False}, {'t': 'Kategoriyalar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'plt.contourf() nima qiladi?', 'a': [{'t': 'To\'ldirilgan kontur grafigi yaratadi', 'c': True}, {'t': 'Oddiy kontur grafigi yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'levels parametri nima?', 'a': [{'t': 'Kontur chiziqlar sonini belgilaydi', 'c': True}, {'t': 'Grafik balandligini belgilaydi', 'c': False}, {'t': 'Rang sonini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Contour grafikda colorbar kerakmi?', 'a': [{'t': 'Ha, qiymatlarni tushunish uchun juda foydali', 'c': True}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Faqat 3D da', 'c': False}]},
        {'t': 'plt.clabel() nima qiladi?', 'a': [{'t': 'Kontur chiziqlarga qiymat yorliqlari qo\'shadi', 'c': True}, {'t': 'Colorbar qo\'shadi', 'c': False}, {'t': 'Sarlavha qo\'shadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Imshow - rasm ko\'rsatish', 't': 30, 'o': 23, 'q': [
        {'t': 'plt.imshow() nima qiladi?', 'a': [{'t': 'Rasm yoki 2D arrayni ko\'rsatadi', 'c': True}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'imshow qachon ishlatiladi?', 'a': [{'t': 'Rasmlar, heatmap, matritsa vizualizatsiya uchun', 'c': True}, {'t': 'Faqat chiziqli grafiklar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat matn uchun', 'c': False}]},
        {'t': 'cmap parametri imshow da nima uchun?', 'a': [{'t': 'Qiymatlarni qanday ranglarda ko\'rsatishni belgilaydi', 'c': True}, {'t': 'Rasm o\'lchamini belgilaydi', 'c': False}, {'t': 'Rasm nomini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'aspect parametri nima?', 'a': [{'t': 'Piksellar nisbatini belgilaydi', 'c': True}, {'t': 'Rasm rangini belgilaydi', 'c': False}, {'t': 'Rasm o\'lchamini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'interpolation parametri nima qiladi?', 'a': [{'t': 'Piksellar orasidagi interpolatsiya usulini belgilaydi', 'c': True}, {'t': 'Rasm rangini o\'zgartiradi', 'c': False}, {'t': 'Rasm o\'lchamini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'imshow da colorbar kerakmi?', 'a': [{'t': 'Ha, qiymatlarni tushunish uchun foydali', 'c': True}, {'t': 'Yo\'q, hech qachon', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Faqat rasmlar uchun', 'c': False}]},
    ]},

    {'n': 'Heatmap - issiqlik xaritasi', 't': 30, 'o': 24, 'q': [
        {'t': 'Heatmap nima?', 'a': [{'t': 'Qiymatlarni rang intensivligi bilan ko\'rsatadigan grafik', 'c': True}, {'t': 'Harorat grafigi', 'c': False}, {'t': 'Chiziqli grafik', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Heatmap qanday yaratiladi?', 'a': [{'t': 'plt.imshow() yoki seaborn.heatmap() bilan', 'c': True}, {'t': 'plt.plot() bilan', 'c': False}, {'t': 'plt.bar() bilan', 'c': False}, {'t': 'Yaratish mumkin emas', 'c': False}]},
        {'t': 'Heatmap qachon foydali?', 'a': [{'t': 'Korrelyatsiya, matritsa, jadval ma\'lumotlarini ko\'rsatishda', 'c': True}, {'t': 'Faqat harorat uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat vaqt uchun', 'c': False}]},
        {'t': 'Heatmap da qanday colormap yaxshi?', 'a': [{'t': 'coolwarm, RdYlGn, viridis kabi diverging yoki sequential', 'c': True}, {'t': 'Faqat qora-oq', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Faqat rainbow', 'c': False}]},
        {'t': 'Heatmap da raqamlarni ko\'rsatish mumkinmi?', 'a': [{'t': 'Ha, plt.text() yoki seaborn annot=True bilan', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat colorbar orqali', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Boxplot - quti grafigi', 't': 30, 'o': 25, 'q': [
        {'t': 'plt.boxplot() nima qiladi?', 'a': [{'t': 'Quti grafigi (box plot) yaratadi', 'c': True}, {'t': 'Ustunli grafik yaratadi', 'c': False}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Boxplot nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlar taqsimoti va outlierlarni ko\'rish uchun', 'c': True}, {'t': 'Vaqt bo\'yicha o\'zgarishni ko\'rish uchun', 'c': False}, {'t': 'Kategoriyalarni solishtirish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Boxplot da quti nima bildiradi?', 'a': [{'t': 'Interquartile range (IQR) - 25% dan 75% gacha', 'c': True}, {'t': 'Barcha ma\'lumotlar', 'c': False}, {'t': 'Faqat o\'rtacha qiymat', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Boxplot da chiziq (whiskers) nima?', 'a': [{'t': 'Ma\'lumotlar diapazoni (outlierlardan tashqari)', 'c': True}, {'t': 'O\'rtacha qiymat', 'c': False}, {'t': 'Maksimum qiymat', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Boxplot da nuqtalar nima?', 'a': [{'t': 'Outlierlar (chetga chiqib ketgan qiymatlar)', 'c': True}, {'t': 'Barcha ma\'lumotlar', 'c': False}, {'t': 'O\'rtacha qiymatlar', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Bir nechta guruh uchun boxplot chizish mumkinmi?', 'a': [{'t': 'Ha, bir nechta list berish mumkin', 'c': True}, {'t': 'Yo\'q, faqat bitta', 'c': False}, {'t': 'Maksimum 2 ta', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Violinplot - skripka grafigi', 't': 30, 'o': 26, 'q': [
        {'t': 'plt.violinplot() nima qiladi?', 'a': [{'t': 'Violin plot (skripka grafigi) yaratadi', 'c': True}, {'t': 'Boxplot yaratadi', 'c': False}, {'t': 'Chiziqli grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Violinplot nima uchun ishlatiladi?', 'a': [{'t': 'Ma\'lumotlar taqsimotini batafsil ko\'rish uchun', 'c': True}, {'t': 'Vaqt bo\'yicha o\'zgarishni ko\'rish uchun', 'c': False}, {'t': 'Faqat outlierlarni topish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Violinplot va boxplot farqi nima?', 'a': [{'t': 'Violin taqsimot shaklini ko\'rsatadi, box faqat statistika', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Violin yangi', 'c': False}, {'t': 'Box tezroq', 'c': False}]},
        {'t': 'Violinplot kengligi nimani bildiradi?', 'a': [{'t': 'O\'sha qiymatdagi ma\'lumotlar zichligini', 'c': True}, {'t': 'Ma\'lumotlar sonini', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Violinplot qaysi kutubxonada yaxshiroq?', 'a': [{'t': 'Seaborn da ko\'proq imkoniyatlar bor', 'c': True}, {'t': 'Faqat Matplotlib da', 'c': False}, {'t': 'Ikkalasida bir xil', 'c': False}, {'t': 'Hech qayerda yo\'q', 'c': False}]},
    ]},

    {'n': 'Errorbar - xato chiziqlari', 't': 30, 'o': 27, 'q': [
        {'t': 'plt.errorbar() nima qiladi?', 'a': [{'t': 'Xato chiziqlari (error bars) bilan grafik yaratadi', 'c': True}, {'t': 'Oddiy chiziqli grafik yaratadi', 'c': False}, {'t': 'Xato xabarini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Errorbar nima uchun kerak?', 'a': [{'t': 'O\'lchov xatolari yoki noaniqlikni ko\'rsatish uchun', 'c': True}, {'t': 'Grafik chiroyliroq bo\'ladi', 'c': False}, {'t': 'Majburiy element', 'c': False}, {'t': 'Hech qachon kerak emas', 'c': False}]},
        {'t': 'yerr parametri nima?', 'a': [{'t': 'Y o\'qi bo\'yicha xato qiymatlarini belgilaydi', 'c': True}, {'t': 'X o\'qi bo\'yicha xato qiymatlarini belgilaydi', 'c': False}, {'t': 'Xato xabarini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'xerr parametri nima?', 'a': [{'t': 'X o\'qi bo\'yicha xato qiymatlarini belgilaydi', 'c': True}, {'t': 'Y o\'qi bo\'yicha xato qiymatlarini belgilaydi', 'c': False}, {'t': 'Xato xabarini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'capsize parametri nima?', 'a': [{'t': 'Xato chizig\'i uchlaridagi chiziqcha o\'lchamini belgilaydi', 'c': True}, {'t': 'Xato qiymatini belgilaydi', 'c': False}, {'t': 'Grafik o\'lchamini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Errorbar ilmiy grafiklar uchun muhimmi?', 'a': [{'t': 'Ha, juda muhim - noaniqlikni ko\'rsatadi', 'c': True}, {'t': 'Yo\'q, kerak emas', 'c': False}, {'t': 'Faqat ba\'zi hollarda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},


    {'n': 'Polar plot - qutb grafigi', 't': 30, 'o': 28, 'q': [
        {'t': 'Polar plot nima?', 'a': [{'t': 'Qutb koordinatalar sistemasida grafik', 'c': True}, {'t': 'Oddiy chiziqli grafik', 'c': False}, {'t': 'Doira grafik', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Polar plot qanday yaratiladi?', 'a': [{'t': 'plt.subplot(projection="polar") yoki plt.polar()', 'c': True}, {'t': 'plt.plot() bilan', 'c': False}, {'t': 'plt.bar() bilan', 'c': False}, {'t': 'Yaratish mumkin emas', 'c': False}]},
        {'t': 'Polar koordinatalar nima?', 'a': [{'t': 'Burchak (theta) va radius (r)', 'c': True}, {'t': 'X va Y', 'c': False}, {'t': 'Faqat burchak', 'c': False}, {'t': 'Faqat radius', 'c': False}]},
        {'t': 'Polar plot qachon foydali?', 'a': [{'t': 'Yo\'nalish, burchak ma\'lumotlarini ko\'rsatishda', 'c': True}, {'t': 'Oddiy chiziqlar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat doira uchun', 'c': False}]},
        {'t': 'Polar plot da 0 gradus qayerda?', 'a': [{'t': 'O\'ng tomonda (3 soat pozitsiyasi)', 'c': True}, {'t': 'Yuqorida (12 soat)', 'c': False}, {'t': 'Chap tomonda', 'c': False}, {'t': 'Pastda', 'c': False}]},
    ]},

    {'n': '3D grafiklar - mplot3d', 't': 35, 'o': 29, 'q': [
        {'t': '3D grafik qanday yaratiladi?', 'a': [{'t': 'from mpl_toolkits.mplot3d import Axes3D', 'c': True}, {'t': 'plt.plot3d()', 'c': False}, {'t': 'plt.3d()', 'c': False}, {'t': 'Yaratish mumkin emas', 'c': False}]},
        {'t': 'ax = plt.subplot(projection="3d") nima qiladi?', 'a': [{'t': '3D grafik uchun axes yaratadi', 'c': True}, {'t': '2D grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'ax.plot3D() nima qiladi?', 'a': [{'t': '3D chiziqli grafik yaratadi', 'c': True}, {'t': '2D grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'ax.scatter3D() nima?', 'a': [{'t': '3D scatter plot yaratadi', 'c': True}, {'t': '2D scatter plot yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'ax.plot_surface() nima qiladi?', 'a': [{'t': '3D sirt (surface) grafigi yaratadi', 'c': True}, {'t': '2D grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': '3D grafikni aylantirib ko\'rish mumkinmi?', 'a': [{'t': 'Ha, sichqoncha bilan interaktiv aylantiriladi', 'c': True}, {'t': 'Yo\'q, statik', 'c': False}, {'t': 'Faqat kod bilan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'ax.set_zlabel() nima?', 'a': [{'t': 'Z o\'qi nomini belgilaydi', 'c': True}, {'t': 'X o\'qi nomini belgilaydi', 'c': False}, {'t': 'Y o\'qi nomini belgilaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Animation - animatsiya yaratish', 't': 35, 'o': 30, 'q': [
        {'t': 'Matplotlib da animatsiya qanday yaratiladi?', 'a': [{'t': 'matplotlib.animation moduli bilan', 'c': True}, {'t': 'plt.animate() bilan', 'c': False}, {'t': 'Yaratish mumkin emas', 'c': False}, {'t': 'Faqat video import qilish mumkin', 'c': False}]},
        {'t': 'FuncAnimation nima?', 'a': [{'t': 'Funksiyani takrorlab animatsiya yaratadi', 'c': True}, {'t': 'Oddiy grafik yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Animatsiya uchun nima kerak?', 'a': [{'t': 'Yangilanadigan funksiya va FuncAnimation', 'c': True}, {'t': 'Faqat plt.show()', 'c': False}, {'t': 'Faqat video fayl', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'interval parametri nima?', 'a': [{'t': 'Kadrlar orasidagi vaqt (millisekund)', 'c': True}, {'t': 'Animatsiya uzunligi', 'c': False}, {'t': 'Kadrlar soni', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Animatsiyani qanday saqlash mumkin?', 'a': [{'t': 'anim.save("file.gif") yoki .mp4', 'c': True}, {'t': 'plt.savefig() bilan', 'c': False}, {'t': 'Saqlash mumkin emas', 'c': False}, {'t': 'Faqat screenshot', 'c': False}]},
        {'t': 'Animatsiya qachon foydali?', 'a': [{'t': 'Vaqt bo\'yicha o\'zgarishni ko\'rsatishda', 'c': True}, {'t': 'Statik ma\'lumotlar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat o\'yin uchun', 'c': False}]},
        {'t': 'blit parametri nima?', 'a': [{'t': 'Faqat o\'zgargan qismni yangilaydi (tezroq)', 'c': True}, {'t': 'Animatsiyani to\'xtatadi', 'c': False}, {'t': 'Rangni o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_matplotlib()
    add_topics(subj, T)
    print(f"\n✅ Matplotlib: {len(T)} ta mavzu qo'shildi!")
