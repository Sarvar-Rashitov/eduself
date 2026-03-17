"""
ASTRONOMIYA - 100 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_astronomy():
    cat, _ = SubjectCategory.objects.get_or_create(slug='tabiiy-fanlar', defaults={'name': 'Tabiiy fanlar', 'icon': 'bi-globe', 'order': 1, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Astronomiya', defaults={'category': cat, 'description': 'Astronomiya fani - koinot va osmon jismlari', 'icon': 'bi-stars', 'order': 5, 'is_active': True})
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

# 100 TA MAVZU (asoslardan murakkabgacha)
T = [
    # ASOSLAR (1-15)
    {'n': 'Astronomiya faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Astronomiya fani nimani o\'rganadi?', 'a': [{'t': 'Osmon jismlari va koinotni', 'c': True}, {'t': 'Faqat Yerni', 'c': False}, {'t': 'Faqat hayvonlarni', 'c': False}, {'t': 'Faqat o\'simliklarni', 'c': False}]},
        {'t': 'Astronomiya so\'zi qaysi tildan olingan?', 'a': [{'t': 'Yunon tilidan (astron - yulduz, nomos - qonun)', 'c': True}, {'t': 'Lotin tilidan', 'c': False}, {'t': 'Arab tilidan', 'c': False}, {'t': 'Rus tilidan', 'c': False}]},
        {'t': 'Astronomiya qaysi fanlarga asoslanadi?', 'a': [{'t': 'Fizika, matematika, kimyo', 'c': True}, {'t': 'Faqat fizika', 'c': False}, {'t': 'Faqat matematika', 'c': False}, {'t': 'Biologiya', 'c': False}]},
        {'t': 'Teleskop nima uchun ishlatiladi?', 'a': [{'t': 'Osmon jismlarini kuzatish uchun', 'c': True}, {'t': 'Mikroorganizmlarni ko\'rish uchun', 'c': False}, {'t': 'Suratga olish uchun', 'c': False}, {'t': 'O\'lchash uchun', 'c': False}]},
        {'t': 'Birinchi teleskopni kim ixtiro qilgan?', 'a': [{'t': 'Galileo Galiley', 'c': True}, {'t': 'Isaak Nyuton', 'c': False}, {'t': 'Albert Eynshteyn', 'c': False}, {'t': 'Kopernik', 'c': False}]},
    ]},
    {'n': 'Koinot va uning tuzilishi', 't': 20, 'o': 2, 'q': [
        {'t': 'Koinot nima?', 'a': [{'t': 'Barcha mavjud materiya va energiya', 'c': True}, {'t': 'Faqat Yer', 'c': False}, {'t': 'Faqat Quyosh sistemasi', 'c': False}, {'t': 'Faqat yulduzlar', 'c': False}]},
        {'t': 'Koinot qachon paydo bo\'lgan?', 'a': [{'t': 'Taxminan 13.8 milliard yil oldin', 'c': True}, {'t': '1000 yil oldin', 'c': False}, {'t': '1 million yil oldin', 'c': False}, {'t': '100 yil oldin', 'c': False}]},
        {'t': 'Katta portlash nazariyasi nimani tushuntiradi?', 'a': [{'t': 'Koinotning paydo bo\'lishini', 'c': True}, {'t': 'Yerning paydo bo\'lishini', 'c': False}, {'t': 'Quyoshning paydo bo\'lishini', 'c': False}, {'t': 'Oyning paydo bo\'lishini', 'c': False}]},
        {'t': 'Koinot qanday harakat qilmoqda?', 'a': [{'t': 'Kengayib bormoqda', 'c': True}, {'t': 'Qisqarib bormoqda', 'c': False}, {'t': 'Harakatsiz turmoqda', 'c': False}, {'t': 'Aylanmoqda', 'c': False}]},
        {'t': 'Koinotda eng ko\'p nima bor?', 'a': [{'t': 'Qorong\'u materiya va qorong\'u energiya', 'c': True}, {'t': 'Yulduzlar', 'c': False}, {'t': 'Sayyoralar', 'c': False}, {'t': 'Asteroidlar', 'c': False}]},
        {'t': 'Galaktika nima?', 'a': [{'t': 'Milliardlab yulduzlar to\'plami', 'c': True}, {'t': 'Bitta yulduz', 'c': False}, {'t': 'Bitta sayyora', 'c': False}, {'t': 'Bitta asteroid', 'c': False}]},
    ]},
    {'n': 'Quyosh sistemasi', 't': 20, 'o': 3, 'q': [
        {'t': 'Quyosh sistemasi nechta sayyoradan iborat?', 'a': [{'t': '8 ta', 'c': True}, {'t': '9 ta', 'c': False}, {'t': '7 ta', 'c': False}, {'t': '10 ta', 'c': False}]},
        {'t': 'Quyosh sistemasining markazida nima bor?', 'a': [{'t': 'Quyosh', 'c': True}, {'t': 'Yer', 'c': False}, {'t': 'Yupiter', 'c': False}, {'t': 'Oy', 'c': False}]},
        {'t': 'Quyosh nima?', 'a': [{'t': 'Yulduz', 'c': True}, {'t': 'Sayyora', 'c': False}, {'t': 'Yo\'ldosh', 'c': False}, {'t': 'Asteroid', 'c': False}]},
        {'t': 'Quyoshga eng yaqin sayyora qaysi?', 'a': [{'t': 'Merkuriy', 'c': True}, {'t': 'Venera', 'c': False}, {'t': 'Yer', 'c': False}, {'t': 'Mars', 'c': False}]},
        {'t': 'Quyosh sistemasida eng katta sayyora qaysi?', 'a': [{'t': 'Yupiter', 'c': True}, {'t': 'Saturn', 'c': False}, {'t': 'Yer', 'c': False}, {'t': 'Mars', 'c': False}]},
        {'t': 'Quyosh sistemasida nechta ichki sayyora bor?', 'a': [{'t': '4 ta (Merkuriy, Venera, Yer, Mars)', 'c': True}, {'t': '2 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '8 ta', 'c': False}]},
        {'t': 'Quyosh sistemasida nechta tashqi sayyora bor?', 'a': [{'t': '4 ta (Yupiter, Saturn, Uran, Neptun)', 'c': True}, {'t': '2 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '8 ta', 'c': False}]},
    ]},
    {'n': 'Quyosh - bizning yulduzimiz', 't': 20, 'o': 4, 'q': [
        {'t': 'Quyosh nimadan tashkil topgan?', 'a': [{'t': 'Asosan vodorod va geliydan', 'c': True}, {'t': 'Toshdan', 'c': False}, {'t': 'Suvdan', 'c': False}, {'t': 'Temirdan', 'c': False}]},
        {'t': 'Quyoshning yoshi taxminan necha?', 'a': [{'t': '4.6 milliard yil', 'c': True}, {'t': '1000 yil', 'c': False}, {'t': '1 million yil', 'c': False}, {'t': '100 yil', 'c': False}]},
        {'t': 'Quyoshda qanday reaksiya sodir bo\'ladi?', 'a': [{'t': 'Yadro sintezi (termoyadro reaksiyasi)', 'c': True}, {'t': 'Yonish', 'c': False}, {'t': 'Portlash', 'c': False}, {'t': 'Erish', 'c': False}]},
        {'t': 'Quyosh sirtining harorati taxminan necha?', 'a': [{'t': '5500°C', 'c': True}, {'t': '100°C', 'c': False}, {'t': '1000°C', 'c': False}, {'t': '10000°C', 'c': False}]},
        {'t': 'Quyosh markazining harorati taxminan necha?', 'a': [{'t': '15 million °C', 'c': True}, {'t': '5500°C', 'c': False}, {'t': '1000°C', 'c': False}, {'t': '100°C', 'c': False}]},
        {'t': 'Quyosh dog\'lari nima?', 'a': [{'t': 'Quyosh sirtidagi sovuqroq joylar', 'c': True}, {'t': 'Quyosh sirtidagi issiqroq joylar', 'c': False}, {'t': 'Quyosh sirtidagi teshiklar', 'c': False}, {'t': 'Quyosh sirtidagi tog\'lar', 'c': False}]},
    ]},
    {'n': 'Merkuriy - birinchi sayyora', 't': 20, 'o': 5, 'q': [
        {'t': 'Merkuriy Quyoshga eng yaqin sayyora, to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, Venera eng yaqin', 'c': False}, {'t': 'Yo\'q, Yer eng yaqin', 'c': False}, {'t': 'Yo\'q, Mars eng yaqin', 'c': False}]},
        {'t': 'Merkuriyda atmosfera bormi?', 'a': [{'t': 'Deyarli yo\'q', 'c': True}, {'t': 'Ha, qalin atmosfera bor', 'c': False}, {'t': 'Ha, Yerdagidek', 'c': False}, {'t': 'Ha, juda qalin', 'c': False}]},
        {'t': 'Merkuriyda bir kun necha Yer kuniga teng?', 'a': [{'t': '176 Yer kuniga', 'c': True}, {'t': '1 Yer kuniga', 'c': False}, {'t': '24 Yer kuniga', 'c': False}, {'t': '365 Yer kuniga', 'c': False}]},
        {'t': 'Merkuriyning sirtida nima ko\'p?', 'a': [{'t': 'Kraterlar', 'c': True}, {'t': 'Dengizlar', 'c': False}, {'t': 'O\'rmonlar', 'c': False}, {'t': 'Muzliklar', 'c': False}]},
        {'t': 'Merkuriyda harorat qanday?', 'a': [{'t': 'Kunduz juda issiq, kechasi juda sovuq', 'c': True}, {'t': 'Doim issiq', 'c': False}, {'t': 'Doim sovuq', 'c': False}, {'t': 'Doim mo\'tadil', 'c': False}]},
    ]},
    {'n': 'Venera - ikkinchi sayyora', 't': 20, 'o': 6, 'q': [
        {'t': 'Venera Yerga eng o\'xshash sayyora, to\'g\'rimi?', 'a': [{'t': 'Ha, o\'lchami jihatidan', 'c': True}, {'t': 'Yo\'q, umuman o\'xshamaydi', 'c': False}, {'t': 'Yo\'q, Mars o\'xshash', 'c': False}, {'t': 'Yo\'q, Yupiter o\'xshash', 'c': False}]},
        {'t': 'Venerada atmosfera qanday?', 'a': [{'t': 'Juda qalin, asosan CO₂ dan', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Yerdagidek', 'c': False}, {'t': 'Juda yupqa', 'c': False}]},
        {'t': 'Venerada harorat qancha?', 'a': [{'t': '460°C gacha (eng issiq sayyora)', 'c': True}, {'t': '20°C', 'c': False}, {'t': '-50°C', 'c': False}, {'t': '100°C', 'c': False}]},
        {'t': 'Venera qaysi yo\'nalishda aylanadi?', 'a': [{'t': 'Teskari yo\'nalishda (soat yo\'nalishi bo\'yicha)', 'c': True}, {'t': 'To\'g\'ri yo\'nalishda', 'c': False}, {'t': 'Aylanmaydi', 'c': False}, {'t': 'Goh to\'g\'ri, goh teskari', 'c': False}]},
        {'t': 'Venerada bir kun necha Yer kuniga teng?', 'a': [{'t': '243 Yer kuniga', 'c': True}, {'t': '1 Yer kuniga', 'c': False}, {'t': '24 Yer kuniga', 'c': False}, {'t': '365 Yer kuniga', 'c': False}]},
        {'t': 'Venerani nima bilan ko\'rish mumkin?', 'a': [{'t': 'Yalang\'och ko\'z bilan, tong va kechqurun', 'c': True}, {'t': 'Faqat teleskop bilan', 'c': False}, {'t': 'Hech qachon ko\'rinmaydi', 'c': False}, {'t': 'Faqat kunduzda', 'c': False}]},
    ]},
    {'n': 'Yer - bizning sayyoramiz', 't': 20, 'o': 7, 'q': [
        {'t': 'Yer Quyoshdan nechanchi sayyora?', 'a': [{'t': 'Uchinchi', 'c': True}, {'t': 'Birinchi', 'c': False}, {'t': 'Ikkinchi', 'c': False}, {'t': 'To\'rtinchi', 'c': False}]},
        {'t': 'Yerning yoshi taxminan necha?', 'a': [{'t': '4.5 milliard yil', 'c': True}, {'t': '1000 yil', 'c': False}, {'t': '1 million yil', 'c': False}, {'t': '100 yil', 'c': False}]},
        {'t': 'Yerning atmosferasi asosan nimadan iborat?', 'a': [{'t': 'Azot (78%) va kislorod (21%)', 'c': True}, {'t': 'Faqat kislorod', 'c': False}, {'t': 'Faqat azot', 'c': False}, {'t': 'Karbonat angidrid', 'c': False}]},
        {'t': 'Yerning sirtining necha foizi suv bilan qoplangan?', 'a': [{'t': '71%', 'c': True}, {'t': '50%', 'c': False}, {'t': '30%', 'c': False}, {'t': '90%', 'c': False}]},
        {'t': 'Yer o\'z o\'qi atrofida necha soatda aylanadi?', 'a': [{'t': '24 soatda', 'c': True}, {'t': '12 soatda', 'c': False}, {'t': '48 soatda', 'c': False}, {'t': '1 soatda', 'c': False}]},
        {'t': 'Yer Quyosh atrofida necha kunda aylanadi?', 'a': [{'t': '365.25 kunda', 'c': True}, {'t': '30 kunda', 'c': False}, {'t': '100 kunda', 'c': False}, {'t': '500 kunda', 'c': False}]},
        {'t': 'Yerda hayot mavjud, chunki?', 'a': [{'t': 'Suv, atmosfera va mo\'tadil harorat bor', 'c': True}, {'t': 'Faqat suv bor', 'c': False}, {'t': 'Faqat atmosfera bor', 'c': False}, {'t': 'Faqat harorat mos', 'c': False}]},
    ]},
    {'n': 'Oy - Yerning yo\'ldoshi', 't': 20, 'o': 8, 'q': [
        {'t': 'Oy nima?', 'a': [{'t': 'Yerning tabiiy yo\'ldoshi', 'c': True}, {'t': 'Sayyora', 'c': False}, {'t': 'Yulduz', 'c': False}, {'t': 'Asteroid', 'c': False}]},
        {'t': 'Oy Yerdan qancha uzoqlikda?', 'a': [{'t': 'Taxminan 384,400 km', 'c': True}, {'t': '1000 km', 'c': False}, {'t': '1 million km', 'c': False}, {'t': '100 km', 'c': False}]},
        {'t': 'Oyda atmosfera bormi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha, qalin atmosfera bor', 'c': False}, {'t': 'Ha, Yerdagidek', 'c': False}, {'t': 'Ha, juda yupqa', 'c': False}]},
        {'t': 'Oy fazalari nima?', 'a': [{'t': 'Oyning turli shakllarda ko\'rinishi', 'c': True}, {'t': 'Oyning rangi', 'c': False}, {'t': 'Oyning harorati', 'c': False}, {'t': 'Oyning tezligi', 'c': False}]},
        {'t': 'To\'lin oy nima?', 'a': [{'t': 'Oyning butun yoritilgan tomoni ko\'rinadi', 'c': True}, {'t': 'Oy ko\'rinmaydi', 'c': False}, {'t': 'Oyning yarmi ko\'rinadi', 'c': False}, {'t': 'Oy qizil rangda', 'c': False}]},
        {'t': 'Yangi oy nima?', 'a': [{'t': 'Oy ko\'rinmaydi', 'c': True}, {'t': 'Oy butunlay ko\'rinadi', 'c': False}, {'t': 'Oyning yarmi ko\'rinadi', 'c': False}, {'t': 'Oy qizil rangda', 'c': False}]},
        {'t': 'Birinchi Oyga qadam qo\'ygan odam kim?', 'a': [{'t': 'Nil Armstrong (1969 yil)', 'c': True}, {'t': 'Yuriy Gagarin', 'c': False}, {'t': 'Buzz Oldrin', 'c': False}, {'t': 'Valentina Tereshkova', 'c': False}]},
    ]},
    {'n': 'Mars - qizil sayyora', 't': 20, 'o': 9, 'q': [
        {'t': 'Mars nima uchun qizil rangda?', 'a': [{'t': 'Sirtida temir oksidi (zang) ko\'p', 'c': True}, {'t': 'Issiq bo\'lgani uchun', 'c': False}, {'t': 'Qon bor', 'c': False}, {'t': 'Qizil tosh bor', 'c': False}]},
        {'t': 'Marsda atmosfera bormi?', 'a': [{'t': 'Ha, lekin juda yupqa', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Ha, Yerdagidek', 'c': False}, {'t': 'Ha, juda qalin', 'c': False}]},
        {'t': 'Marsning nechta yo\'ldoshi bor?', 'a': [{'t': '2 ta (Fobos va Deymos)', 'c': True}, {'t': '1 ta', 'c': False}, {'t': '0 ta', 'c': False}, {'t': '5 ta', 'c': False}]},
        {'t': 'Marsda suv bormi?', 'a': [{'t': 'Ha, muz holida', 'c': True}, {'t': 'Yo\'q, umuman yo\'q', 'c': False}, {'t': 'Ha, suyuq holda', 'c': False}, {'t': 'Ha, bug\' holida', 'c': False}]},
        {'t': 'Marsda bir kun necha soat?', 'a': [{'t': '24.6 soat (Yerdagiga yaqin)', 'c': True}, {'t': '12 soat', 'c': False}, {'t': '48 soat', 'c': False}, {'t': '100 soat', 'c': False}]},
        {'t': 'Marsda eng baland tog\' qaysi?', 'a': [{'t': 'Olimp tog\'i (27 km)', 'c': True}, {'t': 'Everest', 'c': False}, {'t': 'K2', 'c': False}, {'t': 'Kilimanjaro', 'c': False}]},
    ]},
    {'n': 'Asteroid kamari', 't': 20, 'o': 10, 'q': [
        {'t': 'Asteroid kamari qayerda joylashgan?', 'a': [{'t': 'Mars va Yupiter orasida', 'c': True}, {'t': 'Yer va Mars orasida', 'c': False}, {'t': 'Venera va Yer orasida', 'c': False}, {'t': 'Saturn va Uran orasida', 'c': False}]},
        {'t': 'Asteroid nima?', 'a': [{'t': 'Kichik tosh jism', 'c': True}, {'t': 'Katta sayyora', 'c': False}, {'t': 'Yulduz', 'c': False}, {'t': 'Yo\'ldosh', 'c': False}]},
        {'t': 'Asteroid kamarida eng katta asteroid qaysi?', 'a': [{'t': 'Tserer (mitti sayyora)', 'c': True}, {'t': 'Vesta', 'c': False}, {'t': 'Pallas', 'c': False}, {'t': 'Yuno', 'c': False}]},
        {'t': 'Asteroidlar nimadan qolgan?', 'a': [{'t': 'Quyosh sistemasi shakllanishidan qolgan material', 'c': True}, {'t': 'Portlagan sayyoradan', 'c': False}, {'t': 'Yulduzlardan', 'c': False}, {'t': 'Kometalardan', 'c': False}]},
        {'t': 'Asteroid Yerga tushsa nima bo\'ladi?', 'a': [{'t': 'Katta zarar yetkazishi mumkin', 'c': True}, {'t': 'Hech narsa bo\'lmaydi', 'c': False}, {'t': 'Yer yo\'q bo\'ladi', 'c': False}, {'t': 'Yer kattaroq bo\'ladi', 'c': False}]},
    ]},
    {'n': 'Yupiter - gigant sayyora', 't': 20, 'o': 11, 'q': [
        {'t': 'Yupiter Quyosh sistemasining eng katta sayyorasi, to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, Saturn eng katta', 'c': False}, {'t': 'Yo\'q, Yer eng katta', 'c': False}, {'t': 'Yo\'q, Neptun eng katta', 'c': False}]},
        {'t': 'Yupiter nimadan tashkil topgan?', 'a': [{'t': 'Asosan vodorod va geliydan (gaz gigant)', 'c': True}, {'t': 'Toshdan', 'c': False}, {'t': 'Suvdan', 'c': False}, {'t': 'Temirdan', 'c': False}]},
        {'t': 'Yupiterning nechta yo\'ldoshi bor?', 'a': [{'t': '79 tadan ortiq', 'c': True}, {'t': '1 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '10 ta', 'c': False}]},
        {'t': 'Yupiterning eng katta yo\'ldoshi qaysi?', 'a': [{'t': 'Ganimed', 'c': True}, {'t': 'Io', 'c': False}, {'t': 'Europa', 'c': False}, {'t': 'Kallisto', 'c': False}]},
        {'t': 'Yupiterdagi Katta Qizil Dog\' nima?', 'a': [{'t': 'Ulkan bo\'ron (300 yildan beri)', 'c': True}, {'t': 'Krater', 'c': False}, {'t': 'Tog\'', 'c': False}, {'t': 'Dengiz', 'c': False}]},
        {'t': 'Yupiterda bir kun necha soat?', 'a': [{'t': '10 soat (eng tez aylanuvchi sayyora)', 'c': True}, {'t': '24 soat', 'c': False}, {'t': '48 soat', 'c': False}, {'t': '100 soat', 'c': False}]},
    ]},
    {'n': 'Saturn - halqali sayyora', 't': 20, 'o': 12, 'q': [
        {'t': 'Saturn nima bilan mashhur?', 'a': [{'t': 'Go\'zal halqalari bilan', 'c': True}, {'t': 'Qizil rangi bilan', 'c': False}, {'t': 'Katta o\'lchami bilan', 'c': False}, {'t': 'Ko\'p yo\'ldoshlari bilan', 'c': False}]},
        {'t': 'Saturn halqalari nimadan tashkil topgan?', 'a': [{'t': 'Muz va tosh zarralaridan', 'c': True}, {'t': 'Gazdan', 'c': False}, {'t': 'Suvdan', 'c': False}, {'t': 'Metaldan', 'c': False}]},
        {'t': 'Saturn nimadan tashkil topgan?', 'a': [{'t': 'Asosan vodorod va geliydan (gaz gigant)', 'c': True}, {'t': 'Toshdan', 'c': False}, {'t': 'Suvdan', 'c': False}, {'t': 'Temirdan', 'c': False}]},
        {'t': 'Saturnning nechta yo\'ldoshi bor?', 'a': [{'t': '82 tadan ortiq', 'c': True}, {'t': '1 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '10 ta', 'c': False}]},
        {'t': 'Saturnning eng katta yo\'ldoshi qaysi?', 'a': [{'t': 'Titan', 'c': True}, {'t': 'Rea', 'c': False}, {'t': 'Iapetus', 'c': False}, {'t': 'Dione', 'c': False}]},
        {'t': 'Saturn zichligi qanday?', 'a': [{'t': 'Suvdan ham yengil (suvda suzadi)', 'c': True}, {'t': 'Suvdan og\'ir', 'c': False}, {'t': 'Suv bilan bir xil', 'c': False}, {'t': 'Temirdan og\'ir', 'c': False}]},
    ]},
    {'n': 'Uran - yashil sayyora', 't': 20, 'o': 13, 'q': [
        {'t': 'Uran qanday rangda?', 'a': [{'t': 'Yashil-ko\'k rangda', 'c': True}, {'t': 'Qizil rangda', 'c': False}, {'t': 'Sariq rangda', 'c': False}, {'t': 'Oq rangda', 'c': False}]},
        {'t': 'Uran nima uchun yashil-ko\'k rangda?', 'a': [{'t': 'Atmosferasida metan gazi bor', 'c': True}, {'t': 'Suvdan', 'c': False}, {'t': 'O\'simliklardan', 'c': False}, {'t': 'Muzdan', 'c': False}]},
        {'t': 'Uran qanday aylanadi?', 'a': [{'t': 'Yon tomonga ag\'darilgan holda', 'c': True}, {'t': 'To\'g\'ri turgan holda', 'c': False}, {'t': 'Teskari yo\'nalishda', 'c': False}, {'t': 'Aylanmaydi', 'c': False}]},
        {'t': 'Uranning nechta yo\'ldoshi bor?', 'a': [{'t': '27 ta', 'c': True}, {'t': '1 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '100 ta', 'c': False}]},
        {'t': 'Uranning yo\'ldoshlari kimning nomidan olingan?', 'a': [{'t': 'Shekspir va Pope asarlari qahramonlari', 'c': True}, {'t': 'Yunon xudolari', 'c': False}, {'t': 'Rim xudolari', 'c': False}, {'t': 'Olimlar nomi', 'c': False}]},
        {'t': 'Uranda bir yil necha Yer yiliga teng?', 'a': [{'t': '84 Yer yiliga', 'c': True}, {'t': '1 Yer yiliga', 'c': False}, {'t': '10 Yer yiliga', 'c': False}, {'t': '365 Yer yiliga', 'c': False}]},
    ]},
    {'n': 'Neptun - ko\'k sayyora', 't': 20, 'o': 14, 'q': [
        {'t': 'Neptun qanday rangda?', 'a': [{'t': 'To\'q ko\'k rangda', 'c': True}, {'t': 'Qizil rangda', 'c': False}, {'t': 'Sariq rangda', 'c': False}, {'t': 'Yashil rangda', 'c': False}]},
        {'t': 'Neptun Quyoshdan eng uzoq sayyora, to\'g\'rimi?', 'a': [{'t': 'Ha, to\'g\'ri', 'c': True}, {'t': 'Yo\'q, Uran eng uzoq', 'c': False}, {'t': 'Yo\'q, Pluton eng uzoq', 'c': False}, {'t': 'Yo\'q, Saturn eng uzoq', 'c': False}]},
        {'t': 'Neptunda shamol tezligi qanday?', 'a': [{'t': 'Juda kuchli (2000 km/soat gacha)', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Yerdagidek', 'c': False}, {'t': 'Juda sekin', 'c': False}]},
        {'t': 'Neptunning nechta yo\'ldoshi bor?', 'a': [{'t': '14 ta', 'c': True}, {'t': '1 ta', 'c': False}, {'t': '5 ta', 'c': False}, {'t': '100 ta', 'c': False}]},
        {'t': 'Neptunning eng katta yo\'ldoshi qaysi?', 'a': [{'t': 'Triton', 'c': True}, {'t': 'Nereid', 'c': False}, {'t': 'Proteus', 'c': False}, {'t': 'Larissa', 'c': False}]},
        {'t': 'Neptun qanday kashf etilgan?', 'a': [{'t': 'Matematik hisob-kitoblar orqali', 'c': True}, {'t': 'Tasodifan', 'c': False}, {'t': 'Teleskop bilan qidirib', 'c': False}, {'t': 'Kosmik kema orqali', 'c': False}]},
    ]},
    {'n': 'Mitti sayyoralar va Pluton', 't': 20, 'o': 15, 'q': [
        {'t': 'Pluton nima uchun sayyora emas?', 'a': [{'t': 'Orbitasini tozalamagan (mitti sayyora)', 'c': True}, {'t': 'Juda kichik', 'c': False}, {'t': 'Juda uzoq', 'c': False}, {'t': 'Juda sovuq', 'c': False}]},
        {'t': 'Pluton qachon kashf etilgan?', 'a': [{'t': '1930 yilda', 'c': True}, {'t': '2000 yilda', 'c': False}, {'t': '1800 yilda', 'c': False}, {'t': '2020 yilda', 'c': False}]},
        {'t': 'Plutonning eng katta yo\'ldoshi qaysi?', 'a': [{'t': 'Xaron', 'c': True}, {'t': 'Niks', 'c': False}, {'t': 'Gidra', 'c': False}, {'t': 'Kerberos', 'c': False}]},
        {'t': 'Mitti sayyora nima?', 'a': [{'t': 'Sayyoraga o\'xshash, lekin orbitasini tozalamagan jism', 'c': True}, {'t': 'Juda kichik sayyora', 'c': False}, {'t': 'Asteroid', 'c': False}, {'t': 'Kometa', 'c': False}]},
        {'t': 'Quyosh sistemasida nechta mitti sayyora bor?', 'a': [{'t': '5 ta (Tserer, Pluton, Eris, Makemake, Xaumea)', 'c': True}, {'t': '1 ta', 'c': False}, {'t': '10 ta', 'c': False}, {'t': '100 ta', 'c': False}]},
    ]},
    {'n': 'Kometalar', 't': 20, 'o': 16, 'q': [
        {'t': 'Kometa nima?', 'a': [{'t': 'Muz, tosh va changdan iborat osmon jismi', 'c': True}, {'t': 'Yulduz', 'c': False}, {'t': 'Sayyora', 'c': False}, {'t': 'Yo\'ldosh', 'c': False}]},
        {'t': 'Kometa dumi nima?', 'a': [{'t': 'Quyosh yaqinida erigan gaz va chang', 'c': True}, {'t': 'Kometa qismi', 'c': False}, {'t': 'Boshqa kometa', 'c': False}, {'t': 'Yulduz nuri', 'c': False}]},
        {'t': 'Eng mashhur kometa qaysi?', 'a': [{'t': 'Galley kometasi', 'c': True}, {'t': 'Xeyl-Bopp', 'c': False}, {'t': 'Enke', 'c': False}, {'t': 'Shvassmann-Vaxmann', 'c': False}]},
        {'t': 'Galley kometasi necha yilda bir marta ko\'rinadi?', 'a': [{'t': '76 yilda', 'c': True}, {'t': '10 yilda', 'c': False}, {'t': '100 yilda', 'c': False}, {'t': 'Har yili', 'c': False}]},
        {'t': 'Kometalar qayerdan keladi?', 'a': [{'t': 'Oort buluti va Keyper kamaridan', 'c': True}, {'t': 'Marsdan', 'c': False}, {'t': 'Yupiterdan', 'c': False}, {'t': 'Quyoshdan', 'c': False}]},
        {'t': 'Kometa dumi qaysi tomonga yo\'nalgan?', 'a': [{'t': 'Quyoshdan teskari tomonga', 'c': True}, {'t': 'Quyoshga qarab', 'c': False}, {'t': 'Harakat yo\'nalishiga', 'c': False}, {'t': 'Pastga', 'c': False}]},
    ]},
    {'n': 'Meteorlar va meteoritlar', 't': 20, 'o': 17, 'q': [
        {'t': 'Meteor nima?', 'a': [{'t': 'Atmosferada yonayotgan kichik jism (yulduz yomg\'iri)', 'c': True}, {'t': 'Yerga tushgan tosh', 'c': False}, {'t': 'Sayyora', 'c': False}, {'t': 'Yulduz', 'c': False}]},
        {'t': 'Meteorit nima?', 'a': [{'t': 'Yerga tushgan kosmik jism', 'c': True}, {'t': 'Atmosferada yongan jism', 'c': False}, {'t': 'Sayyora', 'c': False}, {'t': 'Yulduz', 'c': False}]},
        {'t': 'Meteoroid nima?', 'a': [{'t': 'Kosmosda uchib yurgan kichik jism', 'c': True}, {'t': 'Yerga tushgan jism', 'c': False}, {'t': 'Atmosferada yongan jism', 'c': False}, {'t': 'Sayyora', 'c': False}]},
        {'t': 'Yulduz yomg\'iri nima?', 'a': [{'t': 'Ko\'p meteorlarning bir vaqtda ko\'rinishi', 'c': True}, {'t': 'Yulduzlarning yog\'ishi', 'c': False}, {'t': 'Yomg\'ir', 'c': False}, {'t': 'Kometa', 'c': False}]},
        {'t': 'Eng katta meteorit krater qayerda?', 'a': [{'t': 'Arizona (AQSh) - Barringer krateri', 'c': True}, {'t': 'Rossiya', 'c': False}, {'t': 'Xitoy', 'c': False}, {'t': 'Hindiston', 'c': False}]},
        {'t': 'Meteorlar nima uchun yonadi?', 'a': [{'t': 'Atmosfera bilan ishqalanish tufayli', 'c': True}, {'t': 'Quyosh isitadi', 'c': False}, {'t': 'O\'z-o\'zidan yonadi', 'c': False}, {'t': 'Chaqmoq uradi', 'c': False}]},
    ]},
    {'n': 'Yulduzlar va ularning turlari', 't': 20, 'o': 18, 'q': [
        {'t': 'Yulduz nima?', 'a': [{'t': 'O\'z nurini chiqaruvchi osmon jismi', 'c': True}, {'t': 'Sayyora', 'c': False}, {'t': 'Yo\'ldosh', 'c': False}, {'t': 'Asteroid', 'c': False}]},
        {'t': 'Yulduzlar nimadan energiya oladi?', 'a': [{'t': 'Yadro sintezi (termoyadro reaksiyasi)', 'c': True}, {'t': 'Yonishdan', 'c': False}, {'t': 'Quyoshdan', 'c': False}, {'t': 'Elektr energiyasidan', 'c': False}]},
        {'t': 'Eng yaqin yulduz qaysi?', 'a': [{'t': 'Quyosh', 'c': True}, {'t': 'Alfa Kentavr', 'c': False}, {'t': 'Sirius', 'c': False}, {'t': 'Vega', 'c': False}]},
        {'t': 'Quyoshdan keyin eng yaqin yulduz qaysi?', 'a': [{'t': 'Proksima Kentavr (4.2 yorug\'lik yili)', 'c': True}, {'t': 'Sirius', 'c': False}, {'t': 'Vega', 'c': False}, {'t': 'Betelgeyze', 'c': False}]},
        {'t': 'Yulduzlar qanday ranglarda bo\'ladi?', 'a': [{'t': 'Qizil, sariq, oq, ko\'k (haroratga bog\'liq)', 'c': True}, {'t': 'Faqat sariq', 'c': False}, {'t': 'Faqat oq', 'c': False}, {'t': 'Faqat qizil', 'c': False}]},
        {'t': 'Eng issiq yulduzlar qanday rangda?', 'a': [{'t': 'Ko\'k rangda', 'c': True}, {'t': 'Qizil rangda', 'c': False}, {'t': 'Sariq rangda', 'c': False}, {'t': 'Yashil rangda', 'c': False}]},
        {'t': 'Eng sovuq yulduzlar qanday rangda?', 'a': [{'t': 'Qizil rangda', 'c': True}, {'t': 'Ko\'k rangda', 'c': False}, {'t': 'Oq rangda', 'c': False}, {'t': 'Yashil rangda', 'c': False}]},
    ]},
    {'n': 'Yulduzlarning hayot sikli', 't': 25, 'o': 19, 'q': [
        {'t': 'Yulduz qanday tug\'iladi?', 'a': [{'t': 'Gaz va chang bulutidan', 'c': True}, {'t': 'Sayyoradan', 'c': False}, {'t': 'Boshqa yulduzdan', 'c': False}, {'t': 'Qora tuynukdan', 'c': False}]},
        {'t': 'Asosiy ketma-ketlik yulduzi nima?', 'a': [{'t': 'Barqaror holatdagi yulduz (masalan, Quyosh)', 'c': True}, {'t': 'Yosh yulduz', 'c': False}, {'t': 'O\'layotgan yulduz', 'c': False}, {'t': 'Portlagan yulduz', 'c': False}]},
        {'t': 'Qizil gigant nima?', 'a': [{'t': 'Katta va sovuq yulduz (keksa yulduz)', 'c': True}, {'t': 'Yosh yulduz', 'c': False}, {'t': 'Kichik yulduz', 'c': False}, {'t': 'Issiq yulduz', 'c': False}]},
        {'t': 'Oq mitti nima?', 'a': [{'t': 'Kichik va juda zich yulduz qoldig\'i', 'c': True}, {'t': 'Yosh yulduz', 'c': False}, {'t': 'Katta yulduz', 'c': False}, {'t': 'Sayyora', 'c': False}]},
        {'t': 'Supernova nima?', 'a': [{'t': 'Yulduzning kuchli portlashi', 'c': True}, {'t': 'Yangi yulduz', 'c': False}, {'t': 'Kichik portlash', 'c': False}, {'t': 'Sayyora portlashi', 'c': False}]},
        {'t': 'Quyosh oxirida nima bo\'ladi?', 'a': [{'t': 'Qizil gigant, keyin oq mitti', 'c': True}, {'t': 'Qora tuynuk', 'c': False}, {'t': 'Neytron yulduzi', 'c': False}, {'t': 'Supernova', 'c': False}]},
    ]},
    {'n': 'Qora tuynuklar', 't': 25, 'o': 20, 'q': [
        {'t': 'Qora tuynuk nima?', 'a': [{'t': 'Juda kuchli tortishish kuchiga ega jism', 'c': True}, {'t': 'Tuynuk', 'c': False}, {'t': 'Sayyora', 'c': False}, {'t': 'Yulduz', 'c': False}]},
        {'t': 'Qora tuynuk qanday hosil bo\'ladi?', 'a': [{'t': 'Katta yulduz portlashidan keyin', 'c': True}, {'t': 'Sayyora portlashidan', 'c': False}, {'t': 'Kometa portlashidan', 'c': False}, {'t': 'O\'z-o\'zidan', 'c': False}]},
        {'t': 'Qora tuynukdan nima chiqib keta olmaydi?', 'a': [{'t': 'Hatto yorug\'lik ham', 'c': True}, {'t': 'Faqat materiya', 'c': False}, {'t': 'Faqat gaz', 'c': False}, {'t': 'Hamma narsa chiqib ketadi', 'c': False}]},
        {'t': 'Qora tuynuk atrofidagi chegara nima deyiladi?', 'a': [{'t': 'Hodisa gorizont', 'c': True}, {'t': 'Qora chegara', 'c': False}, {'t': 'Tuynuk chekkasi', 'c': False}, {'t': 'Tortishish chegarasi', 'c': False}]},
        {'t': 'Qora tuynukni qanday aniqlash mumkin?', 'a': [{'t': 'Atrofidagi jismlarning harakati orqali', 'c': True}, {'t': 'Ko\'rish orqali', 'c': False}, {'t': 'Eshitish orqali', 'c': False}, {'t': 'Hidlash orqali', 'c': False}]},
        {'t': 'Eng yaqin qora tuynuk qayerda?', 'a': [{'t': 'Bizning galaktikamiz markazida', 'c': True}, {'t': 'Quyosh sistemasida', 'c': False}, {'t': 'Yer yaqinida', 'c': False}, {'t': 'Oy yaqinida', 'c': False}]},
    ]},
