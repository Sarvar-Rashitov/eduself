"""
NUMPY - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_numpy():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='NumPy', defaults={'category': cat, 'description': 'NumPy - Python uchun ilmiy hisoblash kutubxonasi', 'icon': 'bi-calculator', 'order': 29, 'is_active': True})
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
    {'n': 'NumPy ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'NumPy nima?', 'a': [{'t': 'Python uchun ilmiy hisoblash kutubxonasi', 'c': True}, {'t': 'Ma\'lumotlar bazasi', 'c': False}, {'t': 'Web framework', 'c': False}, {'t': 'Grafik kutubxona', 'c': False}]},
        {'t': 'NumPy ning asosiy ma\'lumot turi nima?', 'a': [{'t': 'ndarray (N-dimensional array)', 'c': True}, {'t': 'list', 'c': False}, {'t': 'dict', 'c': False}, {'t': 'tuple', 'c': False}]},
        {'t': 'NumPy nima uchun kerak?', 'a': [{'t': 'Tez va samarali matematik amallar uchun', 'c': True}, {'t': 'Fayllar bilan ishlash uchun', 'c': False}, {'t': 'Web sahifa yaratish uchun', 'c': False}, {'t': 'Ma\'lumotlar bazasi bilan ishlash uchun', 'c': False}]},
        {'t': 'NumPy oddiy Python list dan qanday farq qiladi?', 'a': [{'t': 'Tezroq va xotirani kam ishlatadi', 'c': True}, {'t': 'Sekinroq ishlaydi', 'c': False}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Faqat matnlar bilan ishlaydi', 'c': False}]},
        {'t': 'NumPy qaysi dasturlash tilida yozilgan?', 'a': [{'t': 'C va Python', 'c': True}, {'t': 'Faqat Python', 'c': False}, {'t': 'Java', 'c': False}, {'t': 'JavaScript', 'c': False}]},
    ]},

    {'n': 'NumPy o\'rnatish va import qilish', 't': 20, 'o': 2, 'q': [
        {'t': 'NumPy qanday o\'rnatiladi?', 'a': [{'t': 'pip install numpy', 'c': True}, {'t': 'npm install numpy', 'c': False}, {'t': 'apt-get install numpy', 'c': False}, {'t': 'O\'rnatish shart emas', 'c': False}]},
        {'t': 'NumPy ni qanday import qilish kerak?', 'a': [{'t': 'import numpy as np', 'c': True}, {'t': 'import np', 'c': False}, {'t': 'from numpy import *', 'c': False}, {'t': 'include numpy', 'c': False}]},
        {'t': 'Nima uchun "as np" ishlatiladi?', 'a': [{'t': 'Qisqa nom bilan ishlash qulay', 'c': True}, {'t': 'Majburiy', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xavfsizlik uchun', 'c': False}]},
        {'t': 'NumPy versiyasini qanday tekshirish mumkin?', 'a': [{'t': 'np.__version__', 'c': True}, {'t': 'np.version()', 'c': False}, {'t': 'numpy --version', 'c': False}, {'t': 'print(numpy)', 'c': False}]},
        {'t': 'NumPy o\'rnatilganini qanday tekshirish mumkin?', 'a': [{'t': 'import numpy yoki pip show numpy', 'c': True}, {'t': 'Faqat kompyuterni qayta ishga tushirish', 'c': False}, {'t': 'Tekshirish mumkin emas', 'c': False}, {'t': 'Faqat pip list', 'c': False}]},
    ]},

    {'n': 'NumPy array yaratish - np.array()', 't': 25, 'o': 3, 'q': [
        {'t': 'np.array() nima qiladi?', 'a': [{'t': 'List yoki tuple dan NumPy array yaratadi', 'c': True}, {'t': 'Faqat raqamlarni qo\'shadi', 'c': False}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Ma\'lumotlar bazasiga yozadi', 'c': False}]},
        {'t': 'np.array([1, 2, 3]) natijasi nima?', 'a': [{'t': '1D array: [1 2 3]', 'c': True}, {'t': 'List: [1, 2, 3]', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'None', 'c': False}]},
        {'t': 'np.array([[1, 2], [3, 4]]) necha o\'lchovli array?', 'a': [{'t': '2D array (matritsa)', 'c': True}, {'t': '1D array', 'c': False}, {'t': '3D array', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'NumPy array faqat bir xil turdagi ma\'lumotlarni saqlaydi, to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, har xil turlarni saqlaydi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Faqat raqamlarni', 'c': False}]},
        {'t': 'np.array([1, 2, "3"]) nima bo\'ladi?', 'a': [{'t': 'Barcha elementlar string ga aylanadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat raqamlar qoladi', 'c': False}, {'t': 'Hech narsa o\'zgarmaydi', 'c': False}]},
        {'t': 'dtype parametri nima uchun?', 'a': [{'t': 'Ma\'lumot turini belgilash uchun', 'c': True}, {'t': 'Array o\'lchamini belgilash uchun', 'c': False}, {'t': 'Array nomini belgilash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Array xususiyatlari - shape, size, ndim', 't': 25, 'o': 4, 'q': [
        {'t': 'arr.shape nima qaytaradi?', 'a': [{'t': 'Array o\'lchamlarini tuple sifatida', 'c': True}, {'t': 'Array elementlar sonini', 'c': False}, {'t': 'Array turini', 'c': False}, {'t': 'Array nomini', 'c': False}]},
        {'t': 'arr.size nima?', 'a': [{'t': 'Array dagi jami elementlar soni', 'c': True}, {'t': 'Array hajmi baytlarda', 'c': False}, {'t': 'Array o\'lchamlari', 'c': False}, {'t': 'Array turi', 'c': False}]},
        {'t': 'arr.ndim nima bildiradi?', 'a': [{'t': 'Array o\'lchovlar soni (dimensiya)', 'c': True}, {'t': 'Array elementlar soni', 'c': False}, {'t': 'Array turi', 'c': False}, {'t': 'Array nomi', 'c': False}]},
        {'t': 'arr.dtype nima?', 'a': [{'t': 'Array elementlarining ma\'lumot turi', 'c': True}, {'t': 'Array o\'lchami', 'c': False}, {'t': 'Array nomi', 'c': False}, {'t': 'Array shakli', 'c': False}]},
        {'t': 'np.array([[1,2,3],[4,5,6]]).shape nima?', 'a': [{'t': '(2, 3)', 'c': True}, {'t': '(3, 2)', 'c': False}, {'t': '6', 'c': False}, {'t': '2', 'c': False}]},
        {'t': 'np.array([1,2,3]).ndim nima?', 'a': [{'t': '1', 'c': True}, {'t': '3', 'c': False}, {'t': '0', 'c': False}, {'t': '2', 'c': False}]},
    ]},

    {'n': 'np.zeros() va np.ones() - Maxsus arraylar', 't': 25, 'o': 5, 'q': [
        {'t': 'np.zeros(5) nima yaratadi?', 'a': [{'t': '5 ta nol dan iborat 1D array', 'c': True}, {'t': '5 ta bir dan iborat array', 'c': False}, {'t': 'Bo\'sh array', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.ones((3, 4)) nima yaratadi?', 'a': [{'t': '3x4 o\'lchamli birlardan iborat 2D array', 'c': True}, {'t': '3 ta bir dan iborat array', 'c': False}, {'t': '4 ta bir dan iborat array', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.zeros() va np.ones() qachon foydali?', 'a': [{'t': 'Boshlang\'ich qiymatlar bilan array kerak bo\'lganda', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat test uchun', 'c': False}, {'t': 'Faqat matematik amallar uchun', 'c': False}]},
        {'t': 'np.zeros((2,3)).shape nima?', 'a': [{'t': '(2, 3)', 'c': True}, {'t': '(3, 2)', 'c': False}, {'t': '6', 'c': False}, {'t': '0', 'c': False}]},
        {'t': 'np.ones(10).sum() natijasi nima?', 'a': [{'t': '10.0', 'c': True}, {'t': '1.0', 'c': False}, {'t': '0', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'np.arange() va np.linspace()', 't': 30, 'o': 6, 'q': [
        {'t': 'np.arange(10) nima yaratadi?', 'a': [{'t': '0 dan 9 gacha raqamlar', 'c': True}, {'t': '1 dan 10 gacha raqamlar', 'c': False}, {'t': '10 ta nol', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.arange(2, 10, 2) nima?', 'a': [{'t': '2 dan 10 gacha 2 qadam bilan: [2,4,6,8]', 'c': True}, {'t': '2 dan 10 gacha barcha raqamlar', 'c': False}, {'t': '[2, 10, 2]', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.linspace(0, 10, 5) nima qiladi?', 'a': [{'t': '0 dan 10 gacha 5 ta teng oraliqli raqam', 'c': True}, {'t': '0 dan 10 gacha 5 qadam bilan', 'c': False}, {'t': '5 ta nol', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.arange() va np.linspace() farqi nima?', 'a': [{'t': 'arange qadam, linspace elementlar sonini belgilaydi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'linspace tezroq', 'c': False}, {'t': 'arange yangi', 'c': False}]},
        {'t': 'np.arange(5).size nima?', 'a': [{'t': '5', 'c': True}, {'t': '4', 'c': False}, {'t': '0', 'c': False}, {'t': '1', 'c': False}]},
        {'t': 'np.linspace(0, 1, 11) oxirgi element nima?', 'a': [{'t': '1.0', 'c': True}, {'t': '0.9', 'c': False}, {'t': '11', 'c': False}, {'t': '10', 'c': False}]},
        {'t': 'np.arange() Python range() ga o\'xshaydi, to\'g\'rimi?', 'a': [{'t': 'Ha, lekin NumPy array qaytaradi', 'c': True}, {'t': 'Yo\'q, umuman farq qiladi', 'c': False}, {'t': 'Bir xil', 'c': False}, {'t': 'range() tezroq', 'c': False}]},
    ]},

    {'n': 'np.random - Tasodifiy sonlar', 't': 30, 'o': 7, 'q': [
        {'t': 'np.random.rand(5) nima yaratadi?', 'a': [{'t': '0 dan 1 gacha 5 ta tasodifiy son', 'c': True}, {'t': '1 dan 5 gacha tasodifiy sonlar', 'c': False}, {'t': '5 ta bir xil son', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.random.randint(1, 10, 5) nima?', 'a': [{'t': '1 dan 10 gacha 5 ta tasodifiy butun son', 'c': True}, {'t': '1 dan 5 gacha tasodifiy sonlar', 'c': False}, {'t': '10 ta tasodifiy son', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.random.randn() qanday taqsimot bo\'yicha?', 'a': [{'t': 'Normal (Gauss) taqsimot', 'c': True}, {'t': 'Bir xil taqsimot', 'c': False}, {'t': 'Eksponensial taqsimot', 'c': False}, {'t': 'Taqsimot yo\'q', 'c': False}]},
        {'t': 'np.random.seed() nima uchun?', 'a': [{'t': 'Tasodifiy sonlarni takrorlanuvchi qilish uchun', 'c': True}, {'t': 'Tasodifiy sonlar yaratish uchun', 'c': False}, {'t': 'Array yaratish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'np.random.choice([1,2,3,4,5], 3) nima qiladi?', 'a': [{'t': 'Berilgan arraydan 3 ta tasodifiy element tanlaydi', 'c': True}, {'t': '1 dan 5 gacha 3 ta son', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.random.shuffle() nima qiladi?', 'a': [{'t': 'Array elementlarini tasodifiy aralashtiradi', 'c': True}, {'t': 'Yangi array yaratadi', 'c': False}, {'t': 'Array ni saralaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'np.random.rand() va np.random.randn() farqi nima?', 'a': [{'t': 'rand bir xil, randn normal taqsimot', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'randn tezroq', 'c': False}, {'t': 'rand yangi', 'c': False}]},
    ]},

    {'n': 'Array indekslash - 1D array', 't': 25, 'o': 8, 'q': [
        {'t': 'arr[0] nima qaytaradi?', 'a': [{'t': 'Birinchi element', 'c': True}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Barcha elementlar', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[-1] nima?', 'a': [{'t': 'Oxirgi element', 'c': True}, {'t': 'Birinchi element', 'c': False}, {'t': '-1', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[1:4] nima qaytaradi?', 'a': [{'t': '1, 2, 3 indeksli elementlar', 'c': True}, {'t': '1, 2, 3, 4 indeksli elementlar', 'c': False}, {'t': 'Faqat 1 va 4', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[::2] nima qiladi?', 'a': [{'t': 'Har ikkinchi elementni oladi', 'c': True}, {'t': 'Birinchi 2 ta elementni oladi', 'c': False}, {'t': 'Array ni 2 ga bo\'ladi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[::-1] nima?', 'a': [{'t': 'Array ni teskari tartibda qaytaradi', 'c': True}, {'t': 'Oxirgi elementni qaytaradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'NumPy indekslash Python list bilan bir xilmi?', 'a': [{'t': 'Ha, asosan bir xil', 'c': True}, {'t': 'Yo\'q, butunlay boshqacha', 'c': False}, {'t': 'Faqat 1D uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Array indekslash - 2D array', 't': 30, 'o': 9, 'q': [
        {'t': 'arr[0, 0] nima?', 'a': [{'t': 'Birinchi qator, birinchi ustun', 'c': True}, {'t': 'Oxirgi element', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Barcha elementlar', 'c': False}]},
        {'t': 'arr[1, :] nima qaytaradi?', 'a': [{'t': 'Ikkinchi qatorning barcha elementlari', 'c': True}, {'t': 'Ikkinchi ustunning barcha elementlari', 'c': False}, {'t': 'Faqat arr[1]', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[:, 0] nima?', 'a': [{'t': 'Birinchi ustunning barcha elementlari', 'c': True}, {'t': 'Birinchi qatorning barcha elementlari', 'c': False}, {'t': 'Faqat arr[0]', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[0:2, 1:3] nima qaytaradi?', 'a': [{'t': 'Birinchi 2 qator, 1-2 ustunlar', 'c': True}, {'t': 'Barcha elementlar', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Faqat bitta element', 'c': False}]},
        {'t': 'arr[-1, -1] nima?', 'a': [{'t': 'Oxirgi qator, oxirgi ustun', 'c': True}, {'t': 'Birinchi element', 'c': False}, {'t': '[-1, -1]', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '2D arrayda arr[0] nima qaytaradi?', 'a': [{'t': 'Birinchi qatorni (1D array)', 'c': True}, {'t': 'Birinchi elementni', 'c': False}, {'t': 'Birinchi ustunni', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr[1][2] va arr[1, 2] bir xilmi?', 'a': [{'t': 'Ha, bir xil natija', 'c': True}, {'t': 'Yo\'q, farq qiladi', 'c': False}, {'t': 'arr[1, 2] xato', 'c': False}, {'t': 'arr[1][2] xato', 'c': False}]},
    ]},

    {'n': 'Boolean indekslash va fancy indexing', 't': 30, 'o': 10, 'q': [
        {'t': 'arr[arr > 5] nima qiladi?', 'a': [{'t': '5 dan katta elementlarni qaytaradi', 'c': True}, {'t': 'Barcha elementlarni 5 ga o\'zgartiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Boolean indekslash nima?', 'a': [{'t': 'Shart bo\'yicha elementlarni tanlash', 'c': True}, {'t': 'True/False qiymatlarni saqlash', 'c': False}, {'t': 'Mantiqiy amallar', 'c': False}, {'t': 'Xato turi', 'c': False}]},
        {'t': 'arr[[0, 2, 4]] nima qiladi?', 'a': [{'t': '0, 2, 4 indeksli elementlarni qaytaradi', 'c': True}, {'t': 'Xato', 'c': False}, {'t': 'Yangi array yaratadi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Fancy indexing nima?', 'a': [{'t': 'Array yoki list bilan indekslash', 'c': True}, {'t': 'Murakkab indekslash', 'c': False}, {'t': 'Xato turi', 'c': False}, {'t': 'Yangi funksiya', 'c': False}]},
        {'t': 'arr[(arr > 2) & (arr < 8)] nima?', 'a': [{'t': '2 dan katta va 8 dan kichik elementlar', 'c': True}, {'t': 'Xato', 'c': False}, {'t': 'Barcha elementlar', 'c': False}, {'t': 'Bo\'sh array', 'c': False}]},
        {'t': 'Boolean indekslashda & va | nima?', 'a': [{'t': 'AND va OR mantiqiy operatorlar', 'c': True}, {'t': 'Qo\'shish va ayirish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr[arr % 2 == 0] nima qaytaradi?', 'a': [{'t': 'Juft sonlarni', 'c': True}, {'t': 'Toq sonlarni', 'c': False}, {'t': 'Barcha sonlarni', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},


    {'n': 'Array o\'zgartirish - reshape()', 't': 25, 'o': 11, 'q': [
        {'t': 'arr.reshape() nima qiladi?', 'a': [{'t': 'Array shaklini o\'zgartiradi', 'c': True}, {'t': 'Array qiymatlarini o\'zgartiradi', 'c': False}, {'t': 'Array ni o\'chiradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.arange(12).reshape(3, 4) nima yaratadi?', 'a': [{'t': '3x4 o\'lchamli 2D array', 'c': True}, {'t': '4x3 o\'lchamli array', 'c': False}, {'t': '12 elementli 1D array', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'reshape() asl arrayni o\'zgartiradi mi?', 'a': [{'t': 'Yo\'q, yangi array qaytaradi', 'c': True}, {'t': 'Ha, asl arrayni o\'zgartiradi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon ishlamaydi', 'c': False}]},
        {'t': 'arr.reshape(-1) nima qiladi?', 'a': [{'t': 'Array ni 1D ga aylantiradi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Array ni o\'chiradi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr.reshape(2, -1) da -1 nima?', 'a': [{'t': 'Avtomatik hisoblash (2 qator, qolgan ustunlar)', 'c': True}, {'t': 'Xato', 'c': False}, {'t': '-1 ustun', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'reshape() qachon xato beradi?', 'a': [{'t': 'Yangi shakl elementlar soniga mos kelmasa', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat 3D da', 'c': False}]},
    ]},

    {'n': 'Array birlashtirish - concatenate, stack', 't': 30, 'o': 12, 'q': [
        {'t': 'np.concatenate() nima qiladi?', 'a': [{'t': 'Arraylarni birlashtiradi', 'c': True}, {'t': 'Array yaratadi', 'c': False}, {'t': 'Array ni bo\'ladi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.concatenate([arr1, arr2]) qanday ishlaydi?', 'a': [{'t': 'arr1 va arr2 ni bitta arrayga birlashtiradi', 'c': True}, {'t': 'arr1 va arr2 ni ko\'paytiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.vstack() nima uchun?', 'a': [{'t': 'Arraylarni vertikal (qator bo\'yicha) birlashtirish', 'c': True}, {'t': 'Arraylarni gorizontal birlashtirish', 'c': False}, {'t': 'Array yaratish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.hstack() nima qiladi?', 'a': [{'t': 'Arraylarni gorizontal (ustun bo\'yicha) birlashtiradi', 'c': True}, {'t': 'Arraylarni vertikal birlashtiradi', 'c': False}, {'t': 'Array yaratadi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.stack() va np.concatenate() farqi nima?', 'a': [{'t': 'stack yangi o\'lcham qo\'shadi, concatenate mavjudda birlashtiradi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'stack tezroq', 'c': False}, {'t': 'concatenate yangi', 'c': False}]},
        {'t': 'concatenate uchun arraylar bir xil shaklda bo\'lishi kerakmi?', 'a': [{'t': 'Ha, birlashtiriladigan o\'lchamdan tashqari', 'c': True}, {'t': 'Yo\'q, har qanday shakl bo\'lishi mumkin', 'c': False}, {'t': 'Faqat 1D uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'np.concatenate() axis parametri nima uchun?', 'a': [{'t': 'Qaysi o\'lcham bo\'yicha birlashtirishni belgilash', 'c': True}, {'t': 'Array o\'lchamini belgilash', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Array bo\'lish - split, hsplit, vsplit', 't': 25, 'o': 13, 'q': [
        {'t': 'np.split() nima qiladi?', 'a': [{'t': 'Array ni bir necha qismga bo\'ladi', 'c': True}, {'t': 'Array ni yaratadi', 'c': False}, {'t': 'Array ni birlashtiradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.split(arr, 3) nima qiladi?', 'a': [{'t': 'arr ni 3 ta teng qismga bo\'ladi', 'c': True}, {'t': 'arr ni 3 ga ko\'paytiradi', 'c': False}, {'t': 'arr dan 3 ni ayiradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.hsplit() nima uchun?', 'a': [{'t': 'Array ni gorizontal (ustun bo\'yicha) bo\'lish', 'c': True}, {'t': 'Array ni vertikal bo\'lish', 'c': False}, {'t': 'Array yaratish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.vsplit() nima qiladi?', 'a': [{'t': 'Array ni vertikal (qator bo\'yicha) bo\'ladi', 'c': True}, {'t': 'Array ni gorizontal bo\'ladi', 'c': False}, {'t': 'Array yaratadi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.split() qachon xato beradi?', 'a': [{'t': 'Array teng bo\'linmasa', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Faqat 2D da', 'c': False}]},
        {'t': 'np.array_split() va np.split() farqi nima?', 'a': [{'t': 'array_split teng bo\'linmasa ham ishlaydi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'split tezroq', 'c': False}, {'t': 'array_split eski', 'c': False}]},
    ]},

    {'n': 'Matematik amallar - asosiy', 't': 30, 'o': 14, 'q': [
        {'t': 'arr + 5 nima qiladi?', 'a': [{'t': 'Har bir elementga 5 qo\'shadi', 'c': True}, {'t': 'Faqat birinchi elementga 5 qo\'shadi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr1 + arr2 nima?', 'a': [{'t': 'Element-wise qo\'shish', 'c': True}, {'t': 'Arraylarni birlashtirish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Faqat birinchi elementlarni qo\'shish', 'c': False}]},
        {'t': 'arr * 2 nima qiladi?', 'a': [{'t': 'Har bir elementni 2 ga ko\'paytiradi', 'c': True}, {'t': 'Array ni 2 marta takrorlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr ** 2 nima?', 'a': [{'t': 'Har bir elementni kvadratga ko\'taradi', 'c': True}, {'t': 'Array ni 2 ga ko\'paytiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr1 * arr2 nima qiladi?', 'a': [{'t': 'Element-wise ko\'paytirish', 'c': True}, {'t': 'Matritsa ko\'paytirish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Birlashtirish', 'c': False}]},
        {'t': 'Broadcasting nima?', 'a': [{'t': 'Turli shakldagi arraylarni avtomatik moslashtirish', 'c': True}, {'t': 'Array yaratish', 'c': False}, {'t': 'Xato turi', 'c': False}, {'t': 'Yangi funksiya', 'c': False}]},
        {'t': 'np.sqrt(arr) nima qiladi?', 'a': [{'t': 'Har bir elementdan kvadrat ildiz oladi', 'c': True}, {'t': 'Array ni saralaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Agregat funksiyalar - sum, mean, min, max', 't': 30, 'o': 15, 'q': [
        {'t': 'arr.sum() nima qaytaradi?', 'a': [{'t': 'Barcha elementlar yig\'indisi', 'c': True}, {'t': 'Elementlar soni', 'c': False}, {'t': 'Eng katta element', 'c': False}, {'t': 'O\'rtacha qiymat', 'c': False}]},
        {'t': 'arr.mean() nima?', 'a': [{'t': 'Elementlarning o\'rtacha qiymati', 'c': True}, {'t': 'Elementlar yig\'indisi', 'c': False}, {'t': 'Eng katta element', 'c': False}, {'t': 'Elementlar soni', 'c': False}]},
        {'t': 'arr.min() va arr.max() nima qiladi?', 'a': [{'t': 'Eng kichik va eng katta elementni topadi', 'c': True}, {'t': 'Array ni saralaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr.std() nima?', 'a': [{'t': 'Standart og\'ish (standard deviation)', 'c': True}, {'t': 'O\'rtacha qiymat', 'c': False}, {'t': 'Yig\'indi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr.sum(axis=0) nima qiladi?', 'a': [{'t': 'Har bir ustun bo\'yicha yig\'indi', 'c': True}, {'t': 'Har bir qator bo\'yicha yig\'indi', 'c': False}, {'t': 'Umumiy yig\'indi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr.sum(axis=1) nima?', 'a': [{'t': 'Har bir qator bo\'yicha yig\'indi', 'c': True}, {'t': 'Har bir ustun bo\'yicha yig\'indi', 'c': False}, {'t': 'Umumiy yig\'indi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.median(arr) nima?', 'a': [{'t': 'Mediana (o\'rta qiymat)', 'c': True}, {'t': 'O\'rtacha qiymat', 'c': False}, {'t': 'Eng katta qiymat', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Saralash va qidirish', 't': 25, 'o': 16, 'q': [
        {'t': 'np.sort(arr) nima qiladi?', 'a': [{'t': 'Array ni o\'sish tartibida saralaydi', 'c': True}, {'t': 'Array ni teskari tartibda saralaydi', 'c': False}, {'t': 'Array ni aralashtiradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr.sort() va np.sort(arr) farqi nima?', 'a': [{'t': 'arr.sort() asl arrayni o\'zgartiradi, np.sort() yangi qaytaradi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'np.sort() tezroq', 'c': False}, {'t': 'arr.sort() yangi', 'c': False}]},
        {'t': 'np.argsort(arr) nima qaytaradi?', 'a': [{'t': 'Saralangan elementlarning indekslarini', 'c': True}, {'t': 'Saralangan arrayni', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.argmax(arr) nima?', 'a': [{'t': 'Eng katta elementning indeksi', 'c': True}, {'t': 'Eng katta element', 'c': False}, {'t': 'Barcha maksimum qiymatlar', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.argmin(arr) nima qaytaradi?', 'a': [{'t': 'Eng kichik elementning indeksi', 'c': True}, {'t': 'Eng kichik element', 'c': False}, {'t': 'Barcha minimum qiymatlar', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.where(arr > 5) nima qiladi?', 'a': [{'t': '5 dan katta elementlarning indekslarini qaytaradi', 'c': True}, {'t': '5 dan katta elementlarni qaytaradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Noyob qiymatlar va takrorlanish', 't': 25, 'o': 17, 'q': [
        {'t': 'np.unique(arr) nima qiladi?', 'a': [{'t': 'Noyob (takrorlanmaydigan) elementlarni qaytaradi', 'c': True}, {'t': 'Barcha elementlarni qaytaradi', 'c': False}, {'t': 'Takrorlanuvchi elementlarni qaytaradi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.unique(arr, return_counts=True) nima?', 'a': [{'t': 'Noyob elementlar va ularning sonini qaytaradi', 'c': True}, {'t': 'Faqat noyob elementlarni qaytaradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.bincount(arr) nima uchun?', 'a': [{'t': 'Har bir qiymat necha marta uchrayotganini sanaydi', 'c': True}, {'t': 'Array ni saralaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.unique() saralangan array qaytaradimi?', 'a': [{'t': 'Ha, avtomatik saralaydi', 'c': True}, {'t': 'Yo\'q, asl tartibda', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'np.in1d(arr1, arr2) nima qiladi?', 'a': [{'t': 'arr1 elementlari arr2 da borligini tekshiradi', 'c': True}, {'t': 'arr1 va arr2 ni birlashtiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Matritsa amallar - transpose, dot', 't': 30, 'o': 18, 'q': [
        {'t': 'arr.T nima qiladi?', 'a': [{'t': 'Matritsani transpoz qiladi (qator va ustunlarni almashtiradi)', 'c': True}, {'t': 'Matritsani ko\'paytiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.dot(arr1, arr2) nima?', 'a': [{'t': 'Matritsa ko\'paytirish (dot product)', 'c': True}, {'t': 'Element-wise ko\'paytirish', 'c': False}, {'t': 'Qo\'shish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr1 @ arr2 nima qiladi?', 'a': [{'t': 'Matritsa ko\'paytirish (np.dot bilan bir xil)', 'c': True}, {'t': 'Element-wise ko\'paytirish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.linalg.inv(arr) nima?', 'a': [{'t': 'Matritsaning teskari matritsasi', 'c': True}, {'t': 'Matritsani teskari tartibda', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.linalg.det(arr) nima qaytaradi?', 'a': [{'t': 'Matritsa determinanti', 'c': True}, {'t': 'Matritsa yig\'indisi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.eye(3) nima yaratadi?', 'a': [{'t': '3x3 birlik (identity) matritsa', 'c': True}, {'t': '3 ta bir dan iborat array', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Bo\'sh matritsa', 'c': False}]},
        {'t': 'Matritsa ko\'paytirish uchun o\'lchamlar mos kelishi kerakmi?', 'a': [{'t': 'Ha, birinchining ustunlari ikkinchining qatorlariga teng', 'c': True}, {'t': 'Yo\'q, har qanday o\'lcham bo\'lishi mumkin', 'c': False}, {'t': 'Faqat kvadrat matritsalar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Copy va View', 't': 25, 'o': 19, 'q': [
        {'t': 'arr2 = arr1 nima qiladi?', 'a': [{'t': 'arr2 arr1 ga havola (reference) bo\'ladi', 'c': True}, {'t': 'arr1 ni nusxalaydi', 'c': False}, {'t': 'Yangi array yaratadi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'View nima?', 'a': [{'t': 'Asl arrayga havola, xotira umumiy', 'c': True}, {'t': 'To\'liq nusxa', 'c': False}, {'t': 'Yangi array', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Copy nima?', 'a': [{'t': 'To\'liq mustaqil nusxa', 'c': True}, {'t': 'Asl arrayga havola', 'c': False}, {'t': 'View bilan bir xil', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'arr.copy() nima qiladi?', 'a': [{'t': 'Array ning to\'liq nusxasini yaratadi', 'c': True}, {'t': 'View yaratadi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'arr[1:3] view mi yoki copy mi?', 'a': [{'t': 'View (asl arrayga bog\'liq)', 'c': True}, {'t': 'Copy (mustaqil)', 'c': False}, {'t': 'Ikkalasi ham emas', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'View o\'zgartirilsa asl array ham o\'zgaradimi?', 'a': [{'t': 'Ha, o\'zgaradi', 'c': True}, {'t': 'Yo\'q, o\'zgarmaydi', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},


    {'n': 'Fayllar bilan ishlash - save, load', 't': 30, 'o': 20, 'q': [
        {'t': 'np.save() nima qiladi?', 'a': [{'t': 'Array ni .npy faylga saqlaydi', 'c': True}, {'t': 'Array ni yaratadi', 'c': False}, {'t': 'Faylni o\'qiydi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.load() nima uchun?', 'a': [{'t': '.npy fayldan array ni yuklaydi', 'c': True}, {'t': 'Array ni saqlaydi', 'c': False}, {'t': 'Array yaratadi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.savetxt() qanday fayl yaratadi?', 'a': [{'t': 'Matn (text) fayl', 'c': True}, {'t': 'Binary fayl', 'c': False}, {'t': 'Excel fayl', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.loadtxt() nima qiladi?', 'a': [{'t': 'Matn fayldan array yuklaydi', 'c': True}, {'t': 'Binary fayldan yuklaydi', 'c': False}, {'t': 'Array saqlaydi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.savez() nima uchun?', 'a': [{'t': 'Bir nechta arrayni bitta faylga saqlash', 'c': True}, {'t': 'Bitta array saqlash', 'c': False}, {'t': 'Matn fayl yaratish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '.npy va .npz farqi nima?', 'a': [{'t': '.npy bitta array, .npz bir nechta array', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': '.npz tezroq', 'c': False}, {'t': '.npy yangi', 'c': False}]},
        {'t': 'np.genfromtxt() nima uchun foydali?', 'a': [{'t': 'Bo\'sh qiymatlar bilan matn fayllarni yuklash uchun', 'c': True}, {'t': 'Binary fayllar uchun', 'c': False}, {'t': 'Faqat raqamlar uchun', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Mantiqiy amallar', 't': 25, 'o': 21, 'q': [
        {'t': 'np.logical_and(arr1, arr2) nima?', 'a': [{'t': 'Element-wise AND amali', 'c': True}, {'t': 'Element-wise OR amali', 'c': False}, {'t': 'Qo\'shish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.logical_or(arr1, arr2) nima qiladi?', 'a': [{'t': 'Element-wise OR amali', 'c': True}, {'t': 'Element-wise AND amali', 'c': False}, {'t': 'Ko\'paytirish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.logical_not(arr) nima?', 'a': [{'t': 'Element-wise NOT amali (inkor)', 'c': True}, {'t': 'Array ni o\'chiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.all(arr) nima qaytaradi?', 'a': [{'t': 'Barcha elementlar True bo\'lsa True', 'c': True}, {'t': 'Biror element True bo\'lsa True', 'c': False}, {'t': 'Elementlar sonini', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.any(arr) nima?', 'a': [{'t': 'Kamida bitta element True bo\'lsa True', 'c': True}, {'t': 'Barcha elementlar True bo\'lsa True', 'c': False}, {'t': 'Hech qachon True qaytarmaydi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.isnan(arr) nima uchun?', 'a': [{'t': 'NaN (Not a Number) qiymatlarni topish', 'c': True}, {'t': 'Nol qiymatlarni topish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Trigonometriya va matematik funksiyalar', 't': 30, 'o': 22, 'q': [
        {'t': 'np.sin(arr) nima qiladi?', 'a': [{'t': 'Har bir elementning sinusini hisoblaydi', 'c': True}, {'t': 'Array ni saralaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.cos(arr) va np.tan(arr) nima?', 'a': [{'t': 'Kosinus va tangens funksiyalari', 'c': True}, {'t': 'Qo\'shish va ayirish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.exp(arr) nima qiladi?', 'a': [{'t': 'e ning arr darajasini hisoblaydi', 'c': True}, {'t': 'Eksponent taqsimot yaratadi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.log(arr) nima?', 'a': [{'t': 'Natural logarifm (ln)', 'c': True}, {'t': '10 asosli logarifm', 'c': False}, {'t': '2 asosli logarifm', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.log10(arr) nima qiladi?', 'a': [{'t': '10 asosli logarifm', 'c': True}, {'t': 'Natural logarifm', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.abs(arr) nima?', 'a': [{'t': 'Absolut qiymat (modul)', 'c': True}, {'t': 'Kvadrat', 'c': False}, {'t': 'Ildiz', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.ceil(arr) va np.floor(arr) nima qiladi?', 'a': [{'t': 'Yuqoriga va pastga yaxlitlash', 'c': True}, {'t': 'Qo\'shish va ayirish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Statistik funksiyalar', 't': 30, 'o': 23, 'q': [
        {'t': 'np.percentile(arr, 50) nima?', 'a': [{'t': '50% percentil (mediana)', 'c': True}, {'t': '50 ga bo\'lish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.var(arr) nima qaytaradi?', 'a': [{'t': 'Dispersiya (variance)', 'c': True}, {'t': 'Standart og\'ish', 'c': False}, {'t': 'O\'rtacha', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.corrcoef(arr1, arr2) nima?', 'a': [{'t': 'Korrelyatsiya koeffitsienti', 'c': True}, {'t': 'Kovariatsiya', 'c': False}, {'t': 'O\'rtacha', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.cov(arr1, arr2) nima qiladi?', 'a': [{'t': 'Kovariatsiya matritsasini hisoblaydi', 'c': True}, {'t': 'Korrelyatsiya hisoblaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.histogram(arr) nima uchun?', 'a': [{'t': 'Ma\'lumotlar taqsimotini hisoblash', 'c': True}, {'t': 'Array ni saralash', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.quantile(arr, 0.25) nima?', 'a': [{'t': '25% kvantil', 'c': True}, {'t': '25 ga bo\'lish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Dispersiya va standart og\'ish orasidagi bog\'liqlik nima?', 'a': [{'t': 'Standart og\'ish = dispersiyaning kvadrat ildizi', 'c': True}, {'t': 'Bir xil', 'c': False}, {'t': 'Bog\'liqlik yo\'q', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Array kengaytirish - tile, repeat', 't': 25, 'o': 24, 'q': [
        {'t': 'np.tile(arr, 3) nima qiladi?', 'a': [{'t': 'Array ni 3 marta takrorlaydi', 'c': True}, {'t': 'Array ni 3 ga ko\'paytiradi', 'c': False}, {'t': 'Array ni 3 ga bo\'ladi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.repeat(arr, 3) nima?', 'a': [{'t': 'Har bir elementni 3 marta takrorlaydi', 'c': True}, {'t': 'Array ni 3 marta takrorlaydi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.tile() va np.repeat() farqi nima?', 'a': [{'t': 'tile butun arrayni, repeat har bir elementni takrorlaydi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'tile tezroq', 'c': False}, {'t': 'repeat yangi', 'c': False}]},
        {'t': 'np.tile([1,2], (2,3)) nima yaratadi?', 'a': [{'t': '2 qator, 3 marta takrorlangan [1,2]', 'c': True}, {'t': '3 qator, 2 marta takrorlangan', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.repeat([1,2,3], 2) natijasi nima?', 'a': [{'t': '[1,1,2,2,3,3]', 'c': True}, {'t': '[1,2,3,1,2,3]', 'c': False}, {'t': '[2,4,6]', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Meshgrid va koordinata tizimi', 't': 25, 'o': 25, 'q': [
        {'t': 'np.meshgrid() nima uchun?', 'a': [{'t': '2D koordinata to\'rini yaratish', 'c': True}, {'t': 'Array ni saralash', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.meshgrid([1,2], [3,4]) nima qaytaradi?', 'a': [{'t': 'Ikkita 2D array (X va Y koordinatalari)', 'c': True}, {'t': 'Bitta 2D array', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'meshgrid qachon foydali?', 'a': [{'t': '3D grafik va matematik funksiyalar uchun', 'c': True}, {'t': 'Oddiy hisoblashlar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat test uchun', 'c': False}]},
        {'t': 'np.mgrid nima?', 'a': [{'t': 'meshgrid ning qisqa versiyasi', 'c': True}, {'t': 'Yangi funksiya', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.ogrid va np.mgrid farqi nima?', 'a': [{'t': 'ogrid open (ochiq), mgrid dense (zich) to\'r', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'ogrid tezroq', 'c': False}, {'t': 'mgrid yangi', 'c': False}]},
    ]},

    {'n': 'Polynomial (ko\'phadlar)', 't': 25, 'o': 26, 'q': [
        {'t': 'np.poly1d() nima yaratadi?', 'a': [{'t': 'Ko\'phad (polynomial) obyekti', 'c': True}, {'t': 'Oddiy array', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.polyfit(x, y, 2) nima qiladi?', 'a': [{'t': '2-darajali ko\'phad bilan ma\'lumotlarni approksimatsiya qiladi', 'c': True}, {'t': 'x va y ni qo\'shadi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.polyval(p, x) nima?', 'a': [{'t': 'Ko\'phadni x nuqtada hisoblaydi', 'c': True}, {'t': 'Ko\'phad yaratadi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.roots(p) nima qaytaradi?', 'a': [{'t': 'Ko\'phadning ildizlari', 'c': True}, {'t': 'Ko\'phadning koeffitsientlari', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Polynomial approksimatsiya nima uchun kerak?', 'a': [{'t': 'Ma\'lumotlarni egri chiziq bilan yaqinlashtirish', 'c': True}, {'t': 'Array yaratish', 'c': False}, {'t': 'Kerak emas', 'c': False}, {'t': 'Faqat test uchun', 'c': False}]},
    ]},

    {'n': 'Gradient va hosilalar', 't': 25, 'o': 27, 'q': [
        {'t': 'np.gradient(arr) nima hisoblaydi?', 'a': [{'t': 'Array ning gradientini (hosilasini)', 'c': True}, {'t': 'Array yig\'indisini', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Gradient nima?', 'a': [{'t': 'Funksiyaning o\'zgarish tezligi', 'c': True}, {'t': 'Funksiyaning qiymati', 'c': False}, {'t': 'Funksiyaning yig\'indisi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.diff(arr) nima qiladi?', 'a': [{'t': 'Ketma-ket elementlar orasidagi farqni hisoblaydi', 'c': True}, {'t': 'Barcha elementlarni ayiradi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'np.diff([1,3,6,10]) natijasi nima?', 'a': [{'t': '[2, 3, 4]', 'c': True}, {'t': '[1, 3, 6, 10]', 'c': False}, {'t': '[10, 6, 3, 1]', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.gradient() va np.diff() farqi nima?', 'a': [{'t': 'gradient markaziy farq, diff oddiy farq', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'diff tezroq', 'c': False}, {'t': 'gradient yangi', 'c': False}]},
    ]},

    {'n': 'Interpolatsiya', 't': 25, 'o': 28, 'q': [
        {'t': 'np.interp() nima qiladi?', 'a': [{'t': '1D chiziqli interpolatsiya', 'c': True}, {'t': 'Array yaratadi', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Interpolatsiya nima?', 'a': [{'t': 'Ma\'lum nuqtalar orasidagi qiymatlarni taxmin qilish', 'c': True}, {'t': 'Ma\'lumotlarni saralash', 'c': False}, {'t': 'Array yaratish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'np.interp(2.5, [1,2,3], [10,20,30]) natijasi nima?', 'a': [{'t': '25 (2 va 3 orasida)', 'c': True}, {'t': '20', 'c': False}, {'t': '30', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Interpolatsiya qachon foydali?', 'a': [{'t': 'Yo\'qolgan ma\'lumotlarni to\'ldirish uchun', 'c': True}, {'t': 'Array yaratish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat test uchun', 'c': False}]},
        {'t': 'Chiziqli interpolatsiya nima?', 'a': [{'t': 'Nuqtalar orasini to\'g\'ri chiziq bilan bog\'lash', 'c': True}, {'t': 'Egri chiziq bilan bog\'lash', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Xotira va samaradorlik', 't': 30, 'o': 29, 'q': [
        {'t': 'NumPy array Python list dan nima uchun tezroq?', 'a': [{'t': 'C da yozilgan va xotirada ketma-ket joylashgan', 'c': True}, {'t': 'Python da yozilgan', 'c': False}, {'t': 'Kichikroq', 'c': False}, {'t': 'Farq yo\'q', 'c': False}]},
        {'t': 'arr.nbytes nima?', 'a': [{'t': 'Array egallagan xotira hajmi (baytlarda)', 'c': True}, {'t': 'Elementlar soni', 'c': False}, {'t': 'Array o\'lchami', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'dtype=np.float32 nima uchun ishlatiladi?', 'a': [{'t': 'Xotirani tejash uchun (float64 o\'rniga)', 'c': True}, {'t': 'Tezroq hisoblash uchun', 'c': False}, {'t': 'Aniqroq natija uchun', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Vectorization nima?', 'a': [{'t': 'Loop o\'rniga butun arrayga amal qo\'llash', 'c': True}, {'t': 'Array yaratish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Nima uchun NumPy da loop ishlatmaslik kerak?', 'a': [{'t': 'Vectorization ancha tezroq', 'c': True}, {'t': 'Loop ishlamaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Farq yo\'q', 'c': False}]},
        {'t': 'arr.flags nima ko\'rsatadi?', 'a': [{'t': 'Array xususiyatlari (C_CONTIGUOUS, WRITEABLE va boshqalar)', 'c': True}, {'t': 'Array qiymatlari', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'NumPy da eng samarali ma\'lumot turi qaysi?', 'a': [{'t': 'Vazifaga bog\'liq, lekin odatda float64 yoki int64', 'c': True}, {'t': 'Har doim float128', 'c': False}, {'t': 'Har doim int8', 'c': False}, {'t': 'Farq yo\'q', 'c': False}]},
    ]},

    {'n': 'NumPy amaliy qo\'llash', 't': 30, 'o': 30, 'q': [
        {'t': 'NumPy qaysi sohalarda ko\'p ishlatiladi?', 'a': [{'t': 'Machine Learning, Data Science, ilmiy hisoblashlar', 'c': True}, {'t': 'Faqat web dasturlash', 'c': False}, {'t': 'Faqat o\'yin yaratish', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Pandas kutubxonasi NumPy ga asoslanganmi?', 'a': [{'t': 'Ha, Pandas NumPy ustiga qurilgan', 'c': True}, {'t': 'Yo\'q, mustaqil', 'c': False}, {'t': 'NumPy Pandas ga asoslangan', 'c': False}, {'t': 'Bog\'liqlik yo\'q', 'c': False}]},
        {'t': 'NumPy rasmlar bilan ishlash uchun ishlatilishi mumkinmi?', 'a': [{'t': 'Ha, rasm piksellarini array sifatida', 'c': True}, {'t': 'Yo\'q, faqat raqamlar uchun', 'c': False}, {'t': 'Faqat qora-oq rasmlar uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'NumPy va TensorFlow/PyTorch munosabati qanday?', 'a': [{'t': 'TensorFlow/PyTorch NumPy ga o\'xshash API ga ega', 'c': True}, {'t': 'Hech qanday munosabat yo\'q', 'c': False}, {'t': 'NumPy yangi', 'c': False}, {'t': 'Bir xil kutubxonalar', 'c': False}]},
        {'t': 'NumPy bilan qanday masalalarni yechish mumkin?', 'a': [{'t': 'Chiziqli algebra, statistika, signal processing', 'c': True}, {'t': 'Faqat oddiy hisoblashlar', 'c': False}, {'t': 'Faqat ma\'lumotlar bazasi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'NumPy o\'rganish uchun qaysi kutubxonalar kerak?', 'a': [{'t': 'Matplotlib (vizualizatsiya), Pandas (ma\'lumotlar)', 'c': True}, {'t': 'Hech qanday', 'c': False}, {'t': 'Faqat Django', 'c': False}, {'t': 'Faqat Flask', 'c': False}]},
        {'t': 'NumPy ning kelajagi qanday?', 'a': [{'t': 'Ilmiy hisoblashlar uchun asosiy kutubxona bo\'lib qoladi', 'c': True}, {'t': 'Tez orada yo\'qoladi', 'c': False}, {'t': 'Faqat o\'quv uchun', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'NumPy hujjatlarini qayerdan topish mumkin?', 'a': [{'t': 'numpy.org va docs.scipy.org', 'c': True}, {'t': 'Faqat Google', 'c': False}, {'t': 'Topib bo\'lmaydi', 'c': False}, {'t': 'Faqat kitoblardan', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_numpy()
    add_topics(subj, T)
    print(f"\n✅ NumPy - 30 ta mavzu muvaffaqiyatli qo'shildi!")
