"""
GEOGRAFIYA - 100 TA TO'LIQ MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
To'g'ri javoblar turli pozitsiyalarda joylashgan
"""
import os, django, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_geography():
    cat, _ = SubjectCategory.objects.get_or_create(slug='ijtimoiy-fanlar', defaults={'name': 'Ijtimoiy fanlar', 'icon': 'bi-people', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Geografiya', defaults={'category': cat, 'description': 'Geografiya fani - Yer yuzasi va tabiat haqida', 'icon': 'bi-globe', 'order': 3, 'is_active': True})
    return subj

def add_topics(subject, topics_data):
    for td in topics_data:
        topic, created = Topic.objects.get_or_create(subject=subject, name=td['n'], defaults={'time_limit': td['t'], 'passing_score': 60, 'order': td['o'], 'is_active': True})
        print(f"{'✅' if created else 'ℹ️'} §{td['o']}: {td['n']} ({len(td['q'])} test)")
        for i, qd in enumerate(td['q']):
            q, qc = Question.objects.get_or_create(topic=topic, text=qd['t'], defaults={'points': 10, 'order': i + 1})
            if qc:
                for ad in qd['a']:
                    Answer.objects.create(question=q, text=ad['t'], is_correct=ad['c'])

# 100 TA MAVZU
T = [
    # GEOGRAFIYA ASOSLARI (1-10)
    {'n': 'Geografiya faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Geografiya fani nimani o\'rganadi?', 'a': [{'t': 'Yer yuzasi, tabiat va aholini', 'c': True}, {'t': 'Faqat hayvonlarni', 'c': False}, {'t': 'Faqat o\'simliklarni', 'c': False}, {'t': 'Faqat tarixni', 'c': False}]},
        {'t': 'Geografiya so\'zi qaysi tildan olingan?', 'a': [{'t': 'Lotin tilidan', 'c': False}, {'t': 'Yunon tilidan', 'c': True}, {'t': 'Arab tilidan', 'c': False}, {'t': 'Ingliz tilidan', 'c': False}]},
        {'t': 'Geografiya qanday fanlarga bo\'linadi?', 'a': [{'t': 'Faqat fizik geografiya', 'c': False}, {'t': 'Faqat ijtimoiy geografiya', 'c': False}, {'t': 'Fizik va ijtimoiy geografiya', 'c': True}, {'t': 'Hech qanday bo\'linmaydi', 'c': False}]},
        {'t': 'Xarita nima?', 'a': [{'t': 'Yer yuzasining katta tasviri', 'c': False}, {'t': 'Faqat rasm', 'c': False}, {'t': 'Yer yuzasining kichraytirilgan tasviri', 'c': True}, {'t': 'Faqat sxema', 'c': False}]},
        {'t': 'Globus nima?', 'a': [{'t': 'Yerning kichraytirilgan modeli', 'c': True}, {'t': 'Yerning katta modeli', 'c': False}, {'t': 'Xarita', 'c': False}, {'t': 'Atlas', 'c': False}]},
    ]},
    {'n': 'Yer sayyorasi', 't': 25, 'o': 2, 'q': [
        {'t': 'Yer qanday shakldagi?', 'a': [{'t': 'Tekis', 'c': False}, {'t': 'Shar shaklidagi (geoid)', 'c': True}, {'t': 'Kvadrat', 'c': False}, {'t': 'Uchburchak', 'c': False}]},
        {'t': 'Yer o\'z o\'qi atrofida qancha vaqtda aylanadi?', 'a': [{'t': '12 soatda', 'c': False}, {'t': '365 kunda', 'c': False}, {'t': '24 soatda', 'c': True}, {'t': '1 soatda', 'c': False}]},
        {'t': 'Yer Quyosh atrofida qancha vaqtda aylanadi?', 'a': [{'t': '24 soatda', 'c': False}, {'t': '30 kunda', 'c': False}, {'t': '100 kunda', 'c': False}, {'t': '365 kunda (1 yil)', 'c': True}]},
        {'t': 'Yer yuzasining necha foizi suv bilan qoplangan?', 'a': [{'t': '71%', 'c': True}, {'t': '50%', 'c': False}, {'t': '30%', 'c': False}, {'t': '90%', 'c': False}]},
        {'t': 'Yer yuzasining necha foizi quruqlik?', 'a': [{'t': '50%', 'c': False}, {'t': '29%', 'c': True}, {'t': '71%', 'c': False}, {'t': '10%', 'c': False}]},
        {'t': 'Yer atmosferasi nima?', 'a': [{'t': 'Yer yuzasi', 'c': False}, {'t': 'Yerni o\'rab turgan havo qatlami', 'c': True}, {'t': 'Yer ichki qismi', 'c': False}, {'t': 'Okean', 'c': False}]},
    ]},
    {'n': 'Xarita va globus', 't': 20, 'o': 3, 'q': [
        {'t': 'Xarita va globusning farqi nima?', 'a': [{'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Xarita tekis, globus hajmli', 'c': True}, {'t': 'Xarita katta, globus kichik', 'c': False}, {'t': 'Xarita rangli, globus rangsiz', 'c': False}]},
        {'t': 'Xarita masshtabi nima?', 'a': [{'t': 'Xaritaning rangi', 'c': False}, {'t': 'Xaritadagi masofa va haqiqiy masofaning nisbati', 'c': True}, {'t': 'Xaritaning o\'lchami', 'c': False}, {'t': 'Xaritaning shakli', 'c': False}]},
        {'t': 'Xaritada shimol qaysi tomonda ko\'rsatiladi?', 'a': [{'t': 'Pastda', 'c': False}, {'t': 'Chapda', 'c': False}, {'t': 'Yuqorida', 'c': True}, {'t': 'O\'ngda', 'c': False}]},
        {'t': 'Kompas nima uchun ishlatiladi?', 'a': [{'t': 'Masofani o\'lchash uchun', 'c': False}, {'t': 'Yo\'nalishni aniqlash uchun', 'c': True}, {'t': 'Vaqtni bilish uchun', 'c': False}, {'t': 'Haroratni o\'lchash uchun', 'c': False}]},
        {'t': 'Asosiy yo\'nalishlar qaysilar?', 'a': [{'t': 'Shimol, janub, sharq, g\'arb', 'c': True}, {'t': 'Faqat shimol va janub', 'c': False}, {'t': 'Faqat sharq va g\'arb', 'c': False}, {'t': 'Yuqori va past', 'c': False}]},
    ]},
    {'n': 'Materiklar va okeanlar', 't': 20, 'o': 4, 'q': [
        {'t': 'Yer yuzasida nechta materik bor?', 'a': [{'t': '5 ta', 'c': False}, {'t': '6 ta', 'c': True}, {'t': '7 ta', 'c': False}, {'t': '4 ta', 'c': False}]},
        {'t': 'Eng katta materik qaysi?', 'a': [{'t': 'Afrika', 'c': False}, {'t': 'Amerika', 'c': False}, {'t': 'Yevroosiyo', 'c': True}, {'t': 'Avstraliya', 'c': False}]},
        {'t': 'Yer yuzasida nechta okean bor?', 'a': [{'t': '3 ta', 'c': False}, {'t': '4 ta', 'c': True}, {'t': '5 ta', 'c': False}, {'t': '6 ta', 'c': False}]},
        {'t': 'Eng katta okean qaysi?', 'a': [{'t': 'Tinch okeani', 'c': True}, {'t': 'Atlantika okeani', 'c': False}, {'t': 'Hind okeani', 'c': False}, {'t': 'Shimoliy Muz okeani', 'c': False}]},
        {'t': 'Eng kichik materik qaysi?', 'a': [{'t': 'Antarktida', 'c': False}, {'t': 'Avstraliya', 'c': True}, {'t': 'Yevropa', 'c': False}, {'t': 'Afrika', 'c': False}]},
    ]},
    {'n': 'Atmosfera', 't': 20, 'o': 5, 'q': [
        {'t': 'Atmosfera nima?', 'a': [{'t': 'Yer yuzasi', 'c': False}, {'t': 'Yerni o\'rab turgan havo qatlami', 'c': True}, {'t': 'Okean', 'c': False}, {'t': 'Tuproq', 'c': False}]},
        {'t': 'Atmosfera asosan qanday gazlardan iborat?', 'a': [{'t': 'Faqat kislorod', 'c': False}, {'t': 'Azot va kislorod', 'c': True}, {'t': 'Faqat azot', 'c': False}, {'t': 'Faqat karbonat angidrid', 'c': False}]},
        {'t': 'Atmosferaning ahamiyati nima?', 'a': [{'t': 'Faqat nafas olish uchun', 'c': False}, {'t': 'Hayot uchun zarur, himoya qiladi', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
        {'t': 'Havo bosimi nima?', 'a': [{'t': 'Havo harorati', 'c': False}, {'t': 'Havo og\'irligining yer yuzasiga bosimi', 'c': True}, {'t': 'Havo namligi', 'c': False}, {'t': 'Shamol tezligi', 'c': False}]},
        {'t': 'Balandlikka ko\'tarilganda havo bosimi qanday o\'zgaradi?', 'a': [{'t': 'Ortadi', 'c': False}, {'t': 'Kamayadi', 'c': True}, {'t': 'O\'zgarmaydi', 'c': False}, {'t': 'Avval ortadi, keyin kamayadi', 'c': False}]},
    ]},
    {'n': 'Ob-havo va iqlim', 't': 20, 'o': 6, 'q': [
        {'t': 'Ob-havo nima?', 'a': [{'t': 'Ko\'p yillik o\'rtacha holat', 'c': False}, {'t': 'Ma\'lum vaqtdagi atmosfera holati', 'c': True}, {'t': 'Faqat harorat', 'c': False}, {'t': 'Faqat yog\'ingarchilik', 'c': False}]},
        {'t': 'Iqlim nima?', 'a': [{'t': 'Bugungi ob-havo', 'c': False}, {'t': 'Ko\'p yillik o\'rtacha ob-havo', 'c': True}, {'t': 'Faqat harorat', 'c': False}, {'t': 'Faqat shamol', 'c': False}]},
        {'t': 'Ob-havo elementlari qaysilar?', 'a': [{'t': 'Harorat, bosim, shamol, yog\'ingarchilik', 'c': True}, {'t': 'Faqat harorat', 'c': False}, {'t': 'Faqat shamol', 'c': False}, {'t': 'Faqat yog\'ingarchilik', 'c': False}]},
        {'t': 'Termometr nima uchun ishlatiladi?', 'a': [{'t': 'Bosimni o\'lchash uchun', 'c': False}, {'t': 'Haroratni o\'lchash uchun', 'c': True}, {'t': 'Shamolni o\'lchash uchun', 'c': False}, {'t': 'Yog\'ingarchililikni o\'lchash uchun', 'c': False}]},
        {'t': 'Barometr nima uchun ishlatiladi?', 'a': [{'t': 'Havo bosimini o\'lchash uchun', 'c': True}, {'t': 'Haroratni o\'lchash uchun', 'c': False}, {'t': 'Shamolni o\'lchash uchun', 'c': False}, {'t': 'Yog\'ingarchililikni o\'lchash uchun', 'c': False}]},
    ]},
    {'n': 'Shamol', 't': 20, 'o': 7, 'q': [
        {'t': 'Shamol nima?', 'a': [{'t': 'Havoning vertikal harakati', 'c': False}, {'t': 'Havoning gorizontal harakati', 'c': True}, {'t': 'Yog\'ingarchilik', 'c': False}, {'t': 'Bulut', 'c': False}]},
        {'t': 'Shamol qanday hosil bo\'ladi?', 'a': [{'t': 'Harorat farqi tufayli', 'c': False}, {'t': 'Havo bosimi farqi tufayli', 'c': True}, {'t': 'Namlik tufayli', 'c': False}, {'t': 'Bulutlar tufayli', 'c': False}]},
        {'t': 'Shamol qayerdan qayerga esadi?', 'a': [{'t': 'Past bosimdan yuqori bosimga', 'c': False}, {'t': 'Yuqori bosimdan past bosimga', 'c': True}, {'t': 'Issiq joydan sovuq joyga', 'c': False}, {'t': 'Sovuq joydan issiq joyga', 'c': False}]},
        {'t': 'Shamol tezligi qanday o\'lchanadi?', 'a': [{'t': 'Termometr bilan', 'c': False}, {'t': 'Anemometr bilan', 'c': True}, {'t': 'Barometr bilan', 'c': False}, {'t': 'Gigrometr bilan', 'c': False}]},
        {'t': 'Shamolning ahamiyati nima?', 'a': [{'t': 'Iqlimni shakllantiradi, energiya manbai', 'c': True}, {'t': 'Faqat sovutadi', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat zarar keltiradi', 'c': False}]},
    ]},
    {'n': 'Yog\'ingarchilik', 't': 20, 'o': 8, 'q': [
        {'t': 'Yog\'ingarchilik nima?', 'a': [{'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Atmosferadan tushuvchi suv', 'c': True}, {'t': 'Faqat qor', 'c': False}, {'t': 'Faqat do\'l', 'c': False}]},
        {'t': 'Yog\'ingarchilik turlari qaysilar?', 'a': [{'t': 'Yomg\'ir, qor, do\'l, shudring', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat qor', 'c': False}, {'t': 'Faqat do\'l', 'c': False}]},
        {'t': 'Yomg\'ir qanday hosil bo\'ladi?', 'a': [{'t': 'Okeanlardan ko\'tariladi', 'c': False}, {'t': 'Bulutlardagi suv bug\'i kondensatsiyalanadi', 'c': True}, {'t': 'Daryolardan ko\'tariladi', 'c': False}, {'t': 'Tuproqdan ko\'tariladi', 'c': False}]},
        {'t': 'Yog\'ingarchilik qanday o\'lchanadi?', 'a': [{'t': 'Termometr bilan', 'c': False}, {'t': 'Yog\'ingarchilik o\'lchagich bilan', 'c': True}, {'t': 'Barometr bilan', 'c': False}, {'t': 'Anemometr bilan', 'c': False}]},
        {'t': 'Yog\'ingarchilikning ahamiyati nima?', 'a': [{'t': 'Suv manbai, o\'simliklar uchun zarur', 'c': True}, {'t': 'Faqat zarar keltiradi', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat sovutadi', 'c': False}]},
    ]},
    {'n': 'Gidrosfera', 't': 20, 'o': 9, 'q': [
        {'t': 'Gidrosfera nima?', 'a': [{'t': 'Faqat okeanlar', 'c': False}, {'t': 'Yerdagi barcha suv qatlami', 'c': True}, {'t': 'Faqat daryolar', 'c': False}, {'t': 'Faqat ko\'llar', 'c': False}]},
        {'t': 'Gidrosfera nimalardan iborat?', 'a': [{'t': 'Okeanlar, dengizlar, daryolar, ko\'llar', 'c': True}, {'t': 'Faqat okeanlar', 'c': False}, {'t': 'Faqat daryolar', 'c': False}, {'t': 'Faqat ko\'llar', 'c': False}]},
        {'t': 'Yer yuzasidagi suvning ko\'p qismi qayerda?', 'a': [{'t': 'Daryolarda', 'c': False}, {'t': 'Okeanlarda', 'c': True}, {'t': 'Ko\'llarda', 'c': False}, {'t': 'Muzliklarda', 'c': False}]},
        {'t': 'Chuchuk suv qayerda ko\'p?', 'a': [{'t': 'Okeanlarda', 'c': False}, {'t': 'Muzliklarda', 'c': True}, {'t': 'Dengizdarda', 'c': False}, {'t': 'Havoda', 'c': False}]},
        {'t': 'Suvning ahamiyati nima?', 'a': [{'t': 'Hayot uchun zarur, ichimlik, sug\'orish', 'c': True}, {'t': 'Faqat ichimlik uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat transport uchun', 'c': False}]},
    ]},
    {'n': 'Okeanlar va dengizlar', 't': 20, 'o': 10, 'q': [
        {'t': 'Okean va dengizning farqi nima?', 'a': [{'t': 'Hech qanday farq yo\'q', 'c': False}, {'t': 'Okean katta, dengiz kichik', 'c': True}, {'t': 'Okean sho\'r, dengiz chuchuk', 'c': False}, {'t': 'Okean chuqur emas, dengiz chuqur', 'c': False}]},
        {'t': 'Eng katta okean qaysi?', 'a': [{'t': 'Atlantika okeani', 'c': False}, {'t': 'Tinch okeani', 'c': True}, {'t': 'Hind okeani', 'c': False}, {'t': 'Shimoliy Muz okeani', 'c': False}]},
        {'t': 'Okean suvi nima uchun sho\'r?', 'a': [{'t': 'Iflos', 'c': False}, {'t': 'Tuzlar erigan', 'c': True}, {'t': 'Issiq', 'c': False}, {'t': 'Chuqur', 'c': False}]},
        {'t': 'Okean to\'lqinlari qanday hosil bo\'ladi?', 'a': [{'t': 'Baliqlar harakati tufayli', 'c': False}, {'t': 'Shamol ta\'sirida', 'c': True}, {'t': 'Kemalar harakati tufayli', 'c': False}, {'t': 'O\'z-o\'zidan', 'c': False}]},
        {'t': 'Okeanning ahamiyati nima?', 'a': [{'t': 'Iqlimni tartibga soladi, transport, oziq-ovqat', 'c': True}, {'t': 'Faqat transport uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
    ]},
    # DARYOLAR VA KO'LLAR (11-20)
    {'n': 'Daryolar', 't': 20, 'o': 11, 'q': [
        {'t': 'Daryo nima?', 'a': [{'t': 'Sun\'iy kanal', 'c': False}, {'t': 'Tabiiy oqim suv', 'c': True}, {'t': 'Ko\'l', 'c': False}, {'t': 'Okean', 'c': False}]},
        {'t': 'Daryoning qismlari qaysilar?', 'a': [{'t': 'Faqat manba', 'c': False}, {'t': 'Faqat og\'iz', 'c': False}, {'t': 'Manba, o\'rta oqim, og\'iz', 'c': True}, {'t': 'Faqat o\'rta oqim', 'c': False}]},
        {'t': 'Eng uzun daryo qaysi?', 'a': [{'t': 'Amazonka', 'c': False}, {'t': 'Nil daryosi', 'c': True}, {'t': 'Missisipi', 'c': False}, {'t': 'Volga', 'c': False}]},
        {'t': 'Daryoning ahamiyati nima?', 'a': [{'t': 'Faqat ichimlik', 'c': False}, {'t': 'Ichimlik, sug\'orish, transport, energiya', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat transport', 'c': False}]},
        {'t': 'Daryo qayerga quyiladi?', 'a': [{'t': 'Dengiz, okean, ko\'l yoki boshqa daryoga', 'c': True}, {'t': 'Faqat okean', 'c': False}, {'t': 'Faqat dengiz', 'c': False}, {'t': 'Hech qayerga', 'c': False}]},
    ]},
    {'n': 'Ko\'llar', 't': 20, 'o': 12, 'q': [
        {'t': 'Ko\'l nima?', 'a': [{'t': 'Oqim suv', 'c': False}, {'t': 'Quruqlikdagi suv havzasi', 'c': True}, {'t': 'Dengiz', 'c': False}, {'t': 'Okean', 'c': False}]},
        {'t': 'Ko\'llar qanday hosil bo\'ladi?', 'a': [{'t': 'Faqat odamlar qaziydi', 'c': False}, {'t': 'Turli tabiiy jarayonlar natijasida', 'c': True}, {'t': 'Faqat yomg\'ir tufayli', 'c': False}, {'t': 'Faqat qor erishi tufayli', 'c': False}]},
        {'t': 'Eng katta ko\'l qaysi?', 'a': [{'t': 'Baykal', 'c': False}, {'t': 'Kaspiy dengizi', 'c': True}, {'t': 'Aral dengizi', 'c': False}, {'t': 'Issiq-ko\'l', 'c': False}]},
        {'t': 'Ko\'llar qanday bo\'ladi?', 'a': [{'t': 'Chuchuk va sho\'r', 'c': True}, {'t': 'Faqat chuchuk', 'c': False}, {'t': 'Faqat sho\'r', 'c': False}, {'t': 'Hamma bir xil', 'c': False}]},
        {'t': 'Ko\'lning ahamiyati nima?', 'a': [{'t': 'Faqat ichimlik', 'c': False}, {'t': 'Ichimlik, baliqchilik, dam olish', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat bezak', 'c': False}]},
    ]},
    {'n': 'Yer po\'stlog\'i', 't': 25, 'o': 13, 'q': [
        {'t': 'Yer po\'stlog\'i nima?', 'a': [{'t': 'Yerning ichki qismi', 'c': False}, {'t': 'Yerning tashqi qattiq qatlami', 'c': True}, {'t': 'Atmosfera', 'c': False}, {'t': 'Gidrosfera', 'c': False}]},
        {'t': 'Yer po\'stlog\'i nimalardan iborat?', 'a': [{'t': 'Faqat suvdan', 'c': False}, {'t': 'Tog\' jinslaridan', 'c': True}, {'t': 'Faqat havodan', 'c': False}, {'t': 'Faqat tuproqdan', 'c': False}]},
        {'t': 'Tog\' jinslari qanday turlarga bo\'linadi?', 'a': [{'t': 'Magmatik, cho\'kindi, metamorfik', 'c': True}, {'t': 'Faqat magmatik', 'c': False}, {'t': 'Faqat cho\'kindi', 'c': False}, {'t': 'Faqat metamorfik', 'c': False}]},
        {'t': 'Magmatik jinslar qanday hosil bo\'ladi?', 'a': [{'t': 'Cho\'kma natijasida', 'c': False}, {'t': 'Magma sovishi natijasida', 'c': True}, {'t': 'Bosim ta\'sirida', 'c': False}, {'t': 'Shamol ta\'sirida', 'c': False}]},
        {'t': 'Cho\'kindi jinslar qanday hosil bo\'ladi?', 'a': [{'t': 'Magma sovishi natijasida', 'c': False}, {'t': 'Cho\'kma va qattiqlashish natijasida', 'c': True}, {'t': 'Bosim ta\'sirida', 'c': False}, {'t': 'Issiqlik ta\'sirida', 'c': False}]},
        {'t': 'Granit qanday jins?', 'a': [{'t': 'Cho\'kindi jins', 'c': False}, {'t': 'Magmatik jins', 'c': True}, {'t': 'Metamorfik jins', 'c': False}, {'t': 'Organik jins', 'c': False}]},
    ]},
    {'n': 'Tog\'lar', 't': 20, 'o': 14, 'q': [
        {'t': 'Tog\' nima?', 'a': [{'t': 'Yer yuzasining past qismi', 'c': False}, {'t': 'Yer yuzasining baland ko\'tarilgan qismi', 'c': True}, {'t': 'Tekislik', 'c': False}, {'t': 'Daryo', 'c': False}]},
        {'t': 'Tog\'lar qanday hosil bo\'ladi?', 'a': [{'t': 'Shamol ta\'sirida', 'c': False}, {'t': 'Yer po\'stlog\'i harakati natijasida', 'c': True}, {'t': 'Suv ta\'sirida', 'c': False}, {'t': 'Odamlar qurishadi', 'c': False}]},
        {'t': 'Eng baland tog\' qaysi?', 'a': [{'t': 'Elbrus', 'c': False}, {'t': 'Everest (Jomolungma)', 'c': True}, {'t': 'Kilimanjaro', 'c': False}, {'t': 'Akonkagua', 'c': False}]},
        {'t': 'Tog\'ning qismlari qaysilar?', 'a': [{'t': 'Cho\'qqi, yon bag\'ir, etak', 'c': True}, {'t': 'Faqat cho\'qqi', 'c': False}, {'t': 'Faqat etak', 'c': False}, {'t': 'Faqat yon bag\'ir', 'c': False}]},
        {'t': 'Tog\'larda iqlim qanday?', 'a': [{'t': 'Balandlikka ko\'tarilganda isiydi', 'c': False}, {'t': 'Balandlikka ko\'tarilganda sovuqlashadi', 'c': True}, {'t': 'Hamma joyda bir xil', 'c': False}, {'t': 'Iqlim yo\'q', 'c': False}]},
    ]},
    {'n': 'Tekisliklar', 't': 20, 'o': 15, 'q': [
        {'t': 'Tekislik nima?', 'a': [{'t': 'Baland tog\'', 'c': False}, {'t': 'Yer yuzasining tekis yoki kam to\'lqinli qismi', 'c': True}, {'t': 'Chuqur vodiy', 'c': False}, {'t': 'Daryo', 'c': False}]},
        {'t': 'Tekisliklar qanday turlarga bo\'linadi?', 'a': [{'t': 'Faqat past tekisliklar', 'c': False}, {'t': 'Past va baland tekisliklar', 'c': True}, {'t': 'Faqat baland tekisliklar', 'c': False}, {'t': 'Bo\'linmaydi', 'c': False}]},
        {'t': 'Tekisliklarda nima yetishtiriladi?', 'a': [{'t': 'Hech narsa', 'c': False}, {'t': 'Qishloq xo\'jaligi ekinlari', 'c': True}, {'t': 'Faqat o\'rmon', 'c': False}, {'t': 'Faqat gul', 'c': False}]},
        {'t': 'Tekisliklarning ahamiyati nima?', 'a': [{'t': 'Qishloq xo\'jaligi, aholi yashash joyi', 'c': True}, {'t': 'Faqat bezak', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat transport', 'c': False}]},
        {'t': 'Eng katta tekislik qaysi?', 'a': [{'t': 'Turon tekisligi', 'c': False}, {'t': 'Amazonka tekisligi', 'c': True}, {'t': 'G\'arbiy Sibir tekisligi', 'c': False}, {'t': 'Sharqiy Yevropa tekisligi', 'c': False}]},
    ]},
    {'n': 'Vulkanlar', 't': 20, 'o': 16, 'q': [
        {'t': 'Vulkan nima?', 'a': [{'t': 'Oddiy tog\'', 'c': False}, {'t': 'Yer ichidan magma chiqadigan joy', 'c': True}, {'t': 'Daryo', 'c': False}, {'t': 'Ko\'l', 'c': False}]},
        {'t': 'Vulkan qanday hosil bo\'ladi?', 'a': [{'t': 'Odamlar qaziydi', 'c': False}, {'t': 'Yer po\'stlog\'idagi yoriqlar orqali magma chiqadi', 'c': True}, {'t': 'Shamol hosil qiladi', 'c': False}, {'t': 'Suv hosil qiladi', 'c': False}]},
        {'t': 'Vulkan otilishi nima?', 'a': [{'t': 'Magma, gaz va kulning chiqishi', 'c': True}, {'t': 'Faqat suv chiqishi', 'c': False}, {'t': 'Faqat havo chiqishi', 'c': False}, {'t': 'Hech narsa chiqmaydi', 'c': False}]},
        {'t': 'Vulkanlar qanday bo\'ladi?', 'a': [{'t': 'Faqat faol', 'c': False}, {'t': 'Faol, uxlayotgan, o\'chgan', 'c': True}, {'t': 'Faqat o\'chgan', 'c': False}, {'t': 'Hamma bir xil', 'c': False}]},
        {'t': 'Vulkan otilishining oqibatlari?', 'a': [{'t': 'Faqat halokat', 'c': False}, {'t': 'Halokat, lekin unumdor tuproq hosil bo\'ladi', 'c': True}, {'t': 'Hech qanday oqibat yo\'q', 'c': False}, {'t': 'Faqat foyda', 'c': False}]},
    ]},
    {'n': 'Zilzilalar', 't': 20, 'o': 17, 'q': [
        {'t': 'Zilzila nima?', 'a': [{'t': 'Vulkan otilishi', 'c': False}, {'t': 'Yer po\'stlog\'ining silkinishi', 'c': True}, {'t': 'Shamol', 'c': False}, {'t': 'Yomg\'ir', 'c': False}]},
        {'t': 'Zilzila qanday hosil bo\'ladi?', 'a': [{'t': 'Shamol ta\'sirida', 'c': False}, {'t': 'Yer po\'stlog\'i plitalari harakati natijasida', 'c': True}, {'t': 'Suv ta\'sirida', 'c': False}, {'t': 'Odamlar sabab bo\'ladi', 'c': False}]},
        {'t': 'Zilzila kuchi qanday o\'lchanadi?', 'a': [{'t': 'Metrda', 'c': False}, {'t': 'Ballarda (Rixter shkalasi)', 'c': True}, {'t': 'Kilogrammda', 'c': False}, {'t': 'Gradusda', 'c': False}]},
        {'t': 'Zilziladan qanday himoyalanish kerak?', 'a': [{'t': 'Mustahkam binolar qurish, xavfsiz joyga chiqish', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat uyda qolish', 'c': False}, {'t': 'Faqat yugurib qochish', 'c': False}]},
        {'t': 'Zilzila ko\'p bo\'ladigan joylar?', 'a': [{'t': 'Tekisliklar', 'c': False}, {'t': 'Plitalar chegarasidagi hududlar', 'c': True}, {'t': 'Cho\'llar', 'c': False}, {'t': 'Okeanlar', 'c': False}]},
    ]},
    {'n': 'Tuproq', 't': 20, 'o': 18, 'q': [
        {'t': 'Tuproq nima?', 'a': [{'t': 'Oddiy tosh', 'c': False}, {'t': 'Yer yuzasining unumdor qatlami', 'c': True}, {'t': 'Suv', 'c': False}, {'t': 'Havo', 'c': False}]},
        {'t': 'Tuproq qanday hosil bo\'ladi?', 'a': [{'t': 'Faqat suvdan', 'c': False}, {'t': 'Tog\' jinslarining parchalanishi natijasida', 'c': True}, {'t': 'Faqat havodan', 'c': False}, {'t': 'Odamlar yasaydi', 'c': False}]},
        {'t': 'Tuproqning ahamiyati nima?', 'a': [{'t': 'O\'simliklar o\'sadi, oziq-ovqat manbai', 'c': True}, {'t': 'Faqat bezak', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat qurilish uchun', 'c': False}]},
        {'t': 'Tuproqni qanday muhofaza qilish kerak?', 'a': [{'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Eroziyadan saqlash, o\'g\'it solish', 'c': True}, {'t': 'Faqat suv quyish', 'c': False}, {'t': 'Faqat haydash', 'c': False}]},
        {'t': 'Eng unumdor tuproq qaysi?', 'a': [{'t': 'Qum', 'c': False}, {'t': 'Qora tuproq', 'c': True}, {'t': 'Tosh', 'c': False}, {'t': 'Loy', 'c': False}]},
    ]},
    {'n': 'Tabiiy zonalar', 't': 20, 'o': 19, 'q': [
        {'t': 'Tabiiy zona nima?', 'a': [{'t': 'Faqat bir shahar', 'c': False}, {'t': 'O\'xshash iqlim va tabiatga ega hudud', 'c': True}, {'t': 'Faqat bir daryo', 'c': False}, {'t': 'Faqat bir tog\'', 'c': False}]},
        {'t': 'Tabiiy zonalar nimaga bog\'liq?', 'a': [{'t': 'Iqlim va geografik o\'ringa', 'c': True}, {'t': 'Faqat iqlimga', 'c': False}, {'t': 'Faqat geografik o\'ringa', 'c': False}, {'t': 'Hech narsaga', 'c': False}]},
        {'t': 'Asosiy tabiiy zonalar qaysilar?', 'a': [{'t': 'Faqat cho\'l', 'c': False}, {'t': 'Tundra, tayga, cho\'l, savanna, tropik o\'rmon', 'c': True}, {'t': 'Faqat o\'rmon', 'c': False}, {'t': 'Faqat savanna', 'c': False}]},
        {'t': 'Har bir zonada nima o\'ziga xos?', 'a': [{'t': 'O\'simlik va hayvonot dunyosi', 'c': True}, {'t': 'Faqat o\'simliklar', 'c': False}, {'t': 'Faqat hayvonlar', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Tabiiy zonalarni bilishning ahamiyati?', 'a': [{'t': 'Faqat bilim uchun', 'c': False}, {'t': 'Tabiatni muhofaza qilish va foydalanish', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat sayohat uchun', 'c': False}]},
    ]},
    {'n': 'Cho\'llar', 't': 20, 'o': 20, 'q': [
        {'t': 'Cho\'l nima?', 'a': [{'t': 'Nam hudud', 'c': False}, {'t': 'Quruq, issiq, kam yog\'ingarchilikli hudud', 'c': True}, {'t': 'Sovuq hudud', 'c': False}, {'t': 'O\'rmonli hudud', 'c': False}]},
        {'t': 'Cho\'lda nima ko\'p?', 'a': [{'t': 'Suv', 'c': False}, {'t': 'Qum va tosh', 'c': True}, {'t': 'O\'simlik', 'c': False}, {'t': 'Hayvon', 'c': False}]},
        {'t': 'Cho\'lda qanday o\'simliklar o\'sadi?', 'a': [{'t': 'Kaktus, saxovul kabi quruqchilikka chidamli', 'c': True}, {'t': 'Hamma o\'simlik', 'c': False}, {'t': 'Faqat daraxt', 'c': False}, {'t': 'Hech qanday o\'simlik yo\'q', 'c': False}]},
        {'t': 'Cho\'lda qanday hayvonlar yashaydi?', 'a': [{'t': 'Ayiq, bo\'ri', 'c': False}, {'t': 'Tuya, kaltakesak, ilon', 'c': True}, {'t': 'Fil, jiraf', 'c': False}, {'t': 'Hech qanday hayvon yo\'q', 'c': False}]},
        {'t': 'Eng katta cho\'l qaysi?', 'a': [{'t': 'Qizilqum', 'c': False}, {'t': 'Sahro cho\'li', 'c': True}, {'t': 'Qoraqum', 'c': False}, {'t': 'Gobi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🌍 GEOGRAFIYA - 100 TA TO'LIQ MAVZU")
    print("=" * 80)
    subject = get_or_create_geography()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T)
    total = sum(len(t['q']) for t in T)
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! {len(T)} ta mavzu, {total} ta test qo'shildi!")
    print("=" * 80)
