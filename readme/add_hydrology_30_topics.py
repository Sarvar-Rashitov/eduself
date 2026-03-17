"""
GIDROLOGIYA - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_hydrology():
    cat, _ = SubjectCategory.objects.get_or_create(slug='tabiiy-fanlar', defaults={'name': 'Tabiiy fanlar', 'icon': 'bi-globe', 'order': 3, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Gidrologiya', defaults={'category': cat, 'description': 'Gidrologiya - suv resurslari va ularning aylanishi haqidagi fan', 'icon': 'bi-droplet', 'order': 40, 'is_active': True})
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
    {'n': 'Gidrologiya faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Gidrologiya nima?', 'a': [{'t': 'Yer yuzasidagi va yer ostidagi suvlarni o\'rganuvchi fan', 'c': True}, {'t': 'Faqat okeanlarni o\'rganuvchi fan', 'c': False}, {'t': 'Havo sharoitini o\'rganuvchi fan', 'c': False}, {'t': 'Tuproqni o\'rganuvchi fan', 'c': False}]},
        {'t': 'Gidrologiya qaysi fanlar bilan bog\'liq?', 'a': [{'t': 'Geografiya, meteorologiya, ekologiya va boshqalar', 'c': True}, {'t': 'Faqat matematika bilan', 'c': False}, {'t': 'Hech qanday fan bilan bog\'liq emas', 'c': False}, {'t': 'Faqat fizika bilan', 'c': False}]},
        {'t': 'Gidrologiya nima uchun muhim?', 'a': [{'t': 'Suv resurslarini boshqarish va muhofaza qilish uchun', 'c': True}, {'t': 'Faqat ilmiy tadqiqotlar uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat darsliklar uchun', 'c': False}]},
        {'t': 'Gidrologiya qanday bo\'limlarga bo\'linadi?', 'a': [{'t': 'Daryo gidrologiyasi, ko\'l gidrologiyasi, yer osti suvlari va boshqalar', 'c': True}, {'t': 'Faqat daryo gidrologiyasi', 'c': False}, {'t': 'Bo\'linmaydi', 'c': False}, {'t': 'Faqat okean gidrologiyasi', 'c': False}]},
        {'t': 'Gidrologiya sohasida kim ishlaydi?', 'a': [{'t': 'Gidrolog mutaxassislari', 'c': True}, {'t': 'Faqat geograflar', 'c': False}, {'t': 'Faqat fiziklar', 'c': False}, {'t': 'Hech kim', 'c': False}]},
    ]},

    {'n': 'Gidrologik tsikl (suv aylanishi)', 't': 25, 'o': 2, 'q': [
        {'t': 'Gidrologik tsikl nima?', 'a': [{'t': 'Suvning tabiatda doimiy aylanishi jarayoni', 'c': True}, {'t': 'Suvning bir martalik harakati', 'c': False}, {'t': 'Faqat yomg\'ir yog\'ishi', 'c': False}, {'t': 'Suvning muzlashi', 'c': False}]},
        {'t': 'Gidrologik tsiklning asosiy bosqichlari qaysilar?', 'a': [{'t': 'Bug\'lanish, kondensatsiya, yog\'ingarchilik, oqim', 'c': True}, {'t': 'Faqat bug\'lanish', 'c': False}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat oqim', 'c': False}]},
        {'t': 'Bug\'lanish jarayoni qayerda sodir bo\'ladi?', 'a': [{'t': 'Okeanlar, dengizlar, ko\'llar, daryolar va tuproq yuzasida', 'c': True}, {'t': 'Faqat okeanlarda', 'c': False}, {'t': 'Faqat daryolarda', 'c': False}, {'t': 'Hech qayerda', 'c': False}]},
        {'t': 'Kondensatsiya nima?', 'a': [{'t': 'Suv bug\'ining suyuq holatga o\'tishi', 'c': True}, {'t': 'Suvning bug\'lanishi', 'c': False}, {'t': 'Suvning muzlashi', 'c': False}, {'t': 'Yomg\'ir yog\'ishi', 'c': False}]},
        {'t': 'Yog\'ingarchilik qanday shaklda bo\'lishi mumkin?', 'a': [{'t': 'Yomg\'ir, qor, do\'l, shudring', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat qor', 'c': False}, {'t': 'Faqat do\'l', 'c': False}]},
        {'t': 'Transpiratsiya nima?', 'a': [{'t': 'O\'simliklar orqali suvning bug\'lanishi', 'c': True}, {'t': 'Suvning oqishi', 'c': False}, {'t': 'Suvning muzlashi', 'c': False}, {'t': 'Yomg\'ir yog\'ishi', 'c': False}]},
        {'t': 'Gidrologik tsiklda quyosh energiyasi qanday rol o\'ynaydi?', 'a': [{'t': 'Bug\'lanish jarayonini ta\'minlaydi', 'c': True}, {'t': 'Hech qanday rol o\'ynamaydi', 'c': False}, {'t': 'Faqat suvni isitadi', 'c': False}, {'t': 'Faqat yoritadi', 'c': False}]},
    ]},

    {'n': 'Atmosfera yog\'ingarchiligi', 't': 25, 'o': 3, 'q': [
        {'t': 'Yog\'ingarchilik nima?', 'a': [{'t': 'Atmosferadan yer yuzasiga tushadigan suv', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat qor', 'c': False}, {'t': 'Yer ostidagi suv', 'c': False}]},
        {'t': 'Yog\'ingarchilik qanday o\'lchanadi?', 'a': [{'t': 'Millimetr (mm) yoki litr/m² da', 'c': True}, {'t': 'Kilogramm da', 'c': False}, {'t': 'Metr da', 'c': False}, {'t': 'O\'lchanmaydi', 'c': False}]},
        {'t': 'Yog\'ingarchilik o\'lchash asbobi nima deyiladi?', 'a': [{'t': 'Yomg\'ir o\'lchagich (pluviometr)', 'c': True}, {'t': 'Termometr', 'c': False}, {'t': 'Barometr', 'c': False}, {'t': 'Gigrometr', 'c': False}]},
        {'t': 'Yillik yog\'ingarchilik miqdori qayerda ko\'proq?', 'a': [{'t': 'Ekvatorial va tropik hududlarda', 'c': True}, {'t': 'Cho\'llarda', 'c': False}, {'t': 'Qutb hududlarida', 'c': False}, {'t': 'Hamma joyda bir xil', 'c': False}]},
        {'t': 'Qor qoplami nima uchun muhim?', 'a': [{'t': 'Bahor paytida suv manbai bo\'ladi', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat sovuq uchun', 'c': False}]},
        {'t': 'Konvektiv yog\'ingarchilik qanday hosil bo\'ladi?', 'a': [{'t': 'Issiq havo ko\'tarilib, soviydi va yog\'ingarchilik hosil qiladi', 'c': True}, {'t': 'Shamol ta\'sirida', 'c': False}, {'t': 'Tog\'lar ta\'sirida', 'c': False}, {'t': 'Hosil bo\'lmaydi', 'c': False}]},
    ]},

    {'n': 'Bug\'lanish va transpiratsiya', 't': 25, 'o': 4, 'q': [
        {'t': 'Bug\'lanish nima?', 'a': [{'t': 'Suyuq suvning gaz holatiga o\'tishi', 'c': True}, {'t': 'Suvning muzlashi', 'c': False}, {'t': 'Suvning oqishi', 'c': False}, {'t': 'Yomg\'ir yog\'ishi', 'c': False}]},
        {'t': 'Bug\'lanishga qanday omillar ta\'sir qiladi?', 'a': [{'t': 'Harorat, shamol, namlik, quyosh radiatsiyasi', 'c': True}, {'t': 'Faqat harorat', 'c': False}, {'t': 'Faqat shamol', 'c': False}, {'t': 'Hech narsa ta\'sir qilmaydi', 'c': False}]},
        {'t': 'Evapotranspiratsiya nima?', 'a': [{'t': 'Bug\'lanish va transpiratsiyaning yig\'indisi', 'c': True}, {'t': 'Faqat bug\'lanish', 'c': False}, {'t': 'Faqat transpiratsiya', 'c': False}, {'t': 'Yomg\'ir yog\'ishi', 'c': False}]},
        {'t': 'Potensial evapotranspiratsiya nima?', 'a': [{'t': 'Suv yetarli bo\'lganda maksimal bug\'lanish', 'c': True}, {'t': 'Minimal bug\'lanish', 'c': False}, {'t': 'O\'rtacha bug\'lanish', 'c': False}, {'t': 'Hech qanday bug\'lanish yo\'q', 'c': False}]},
        {'t': 'Bug\'lanish qaysi faslda ko\'proq?', 'a': [{'t': 'Yozda', 'c': True}, {'t': 'Qishda', 'c': False}, {'t': 'Bahorda', 'c': False}, {'t': 'Hamma faslda bir xil', 'c': False}]},
        {'t': 'Transpiratsiya jarayonida o\'simliklar nima qiladi?', 'a': [{'t': 'Ildiz orqali olgan suvni bug\'latadi', 'c': True}, {'t': 'Suvni saqlaydi', 'c': False}, {'t': 'Suvni iste\'mol qilmaydi', 'c': False}, {'t': 'Suv ishlab chiqaradi', 'c': False}]},
    ]},

    {'n': 'Yer usti oqimi', 't': 30, 'o': 5, 'q': [
        {'t': 'Yer usti oqimi nima?', 'a': [{'t': 'Yog\'ingarchilikdan keyin yer yuzasi bo\'ylab oqadigan suv', 'c': True}, {'t': 'Yer ostidagi suv', 'c': False}, {'t': 'Atmosferadagi suv', 'c': False}, {'t': 'Muzlikdagi suv', 'c': False}]},
        {'t': 'Yer usti oqimiga qanday omillar ta\'sir qiladi?', 'a': [{'t': 'Yog\'ingarchilik intensivligi, tuproq turi, o\'simlik qoplami, relyef', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat tuproq', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Infiltratsiya nima?', 'a': [{'t': 'Suvning tuproqqa singishi', 'c': True}, {'t': 'Suvning bug\'lanishi', 'c': False}, {'t': 'Suvning oqishi', 'c': False}, {'t': 'Suvning muzlashi', 'c': False}]},
        {'t': 'Qaysi tuproq ko\'proq suvni o\'tkazadi?', 'a': [{'t': 'Qumli tuproq', 'c': True}, {'t': 'Loy tuproq', 'c': False}, {'t': 'Tosh tuproq', 'c': False}, {'t': 'Hamma tuproq bir xil', 'c': False}]},
        {'t': 'O\'simlik qoplami yer usti oqimiga qanday ta\'sir qiladi?', 'a': [{'t': 'Oqimni kamaytiradi va eroziyani oldini oladi', 'c': True}, {'t': 'Oqimni oshiradi', 'c': False}, {'t': 'Hech qanday ta\'sir qilmaydi', 'c': False}, {'t': 'Oqimni to\'xtatadi', 'c': False}]},
        {'t': 'Tik qiyalikda yer usti oqimi qanday bo\'ladi?', 'a': [{'t': 'Tezroq va kuchliroq', 'c': True}, {'t': 'Sekinroq', 'c': False}, {'t': 'Bir xil', 'c': False}, {'t': 'Bo\'lmaydi', 'c': False}]},
        {'t': 'Eroziya nima?', 'a': [{'t': 'Tuproqning suv yoki shamol ta\'sirida yemirilishi', 'c': True}, {'t': 'Tuproqning hosil bo\'lishi', 'c': False}, {'t': 'Tuproqning muzlashi', 'c': False}, {'t': 'Tuproqning quritilishi', 'c': False}]},
    ]},

    {'n': 'Yer osti suvlari', 't': 30, 'o': 6, 'q': [
        {'t': 'Yer osti suvlari nima?', 'a': [{'t': 'Yer qobig\'idagi g\'ovaklar va yoriqlar ichidagi suvlar', 'c': True}, {'t': 'Daryo suvlari', 'c': False}, {'t': 'Yomg\'ir suvlari', 'c': False}, {'t': 'Okean suvlari', 'c': False}]},
        {'t': 'Yer osti suvlari qanday hosil bo\'ladi?', 'a': [{'t': 'Yog\'ingarchilik va yer usti suvlarining infiltratsiyasi orqali', 'c': True}, {'t': 'Faqat yomg\'ir orqali', 'c': False}, {'t': 'Yer ichida paydo bo\'ladi', 'c': False}, {'t': 'Hosil bo\'lmaydi', 'c': False}]},
        {'t': 'Suvli qatlam (akvafer) nima?', 'a': [{'t': 'Suv bilan to\'lgan g\'ovakli yoki yoriqli jins qatlami', 'c': False}, {'t': 'Yer yuzasidagi suv', 'c': False}, {'t': 'Atmosferadagi suv', 'c': False}, {'t': 'Suv bilan to\'lgan g\'ovakli jins qatlami', 'c': True}]},
        {'t': 'Suv o\'tkazmaydigan qatlam nima deyiladi?', 'a': [{'t': 'Akviklad yoki akvifu', 'c': True}, {'t': 'Akvafer', 'c': False}, {'t': 'Infiltratsiya', 'c': False}, {'t': 'Eroziya', 'c': False}]},
        {'t': 'Artezian suvlari nima?', 'a': [{'t': 'Bosim ostidagi yer osti suvlari', 'c': True}, {'t': 'Yer yuzasidagi suvlar', 'c': False}, {'t': 'Daryo suvlari', 'c': False}, {'t': 'Yomg\'ir suvlari', 'c': False}]},
        {'t': 'Yer osti suvlari nima uchun muhim?', 'a': [{'t': 'Ichimlik suvi va qishloq xo\'jaligi uchun asosiy manba', 'c': True}, {'t': 'Faqat ilmiy tadqiqotlar uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat sanoat uchun', 'c': False}]},
        {'t': 'Quduq nima?', 'a': [{'t': 'Yer osti suvlariga erishish uchun qazilgan teshik', 'c': True}, {'t': 'Yer yuzasidagi suv ombori', 'c': False}, {'t': 'Daryo', 'c': False}, {'t': 'Ko\'l', 'c': False}]},
    ]},

    {'n': 'Daryolar va ularning xususiyatlari', 't': 30, 'o': 7, 'q': [
        {'t': 'Daryo nima?', 'a': [{'t': 'Tabiiy suv oqimi bo\'lgan uzun va tor suv havzasi', 'c': True}, {'t': 'Sun\'iy suv ombori', 'c': False}, {'t': 'Yer ostidagi suv', 'c': False}, {'t': 'Atmosferadagi suv', 'c': False}]},
        {'t': 'Daryo havzasi nima?', 'a': [{'t': 'Daryoga suv yig\'iladigan hudud', 'c': True}, {'t': 'Daryo tubidagi joy', 'c': False}, {'t': 'Daryo bo\'yidagi o\'rmon', 'c': False}, {'t': 'Daryo suvi', 'c': False}]},
        {'t': 'Suv ajratgich nima?', 'a': [{'t': 'Ikki daryo havzasini ajratuvchi balandlik', 'c': True}, {'t': 'Daryo ichidagi to\'siq', 'c': False}, {'t': 'Daryo bo\'yidagi bino', 'c': False}, {'t': 'Suv ombori', 'c': False}]},
        {'t': 'Daryo oqimining tezligi nimaga bog\'liq?', 'a': [{'t': 'Qiyalik, suv miqdori, o\'zak shakli', 'c': True}, {'t': 'Faqat suv miqdori', 'c': False}, {'t': 'Faqat qiyalik', 'c': False}, {'t': 'Hech narsaga bog\'liq emas', 'c': False}]},
        {'t': 'Daryo oqimining rejimi nima?', 'a': [{'t': 'Daryo suv miqdorining yil davomida o\'zgarishi', 'c': True}, {'t': 'Daryo tezligi', 'c': False}, {'t': 'Daryo chuqurligi', 'c': False}, {'t': 'Daryo kengligi', 'c': False}]},
        {'t': 'Toshqin nima?', 'a': [{'t': 'Daryo suvi sathining keskin ko\'tarilishi', 'c': True}, {'t': 'Daryo suvining kamayishi', 'c': False}, {'t': 'Daryo muzlashi', 'c': False}, {'t': 'Daryo qurib qolishi', 'c': False}]},
        {'t': 'Qurg\'oqchilik nima?', 'a': [{'t': 'Daryo suvi sathining eng past darajasi', 'c': True}, {'t': 'Daryo suvi ko\'p bo\'lishi', 'c': False}, {'t': 'Yomg\'ir yog\'ishi', 'c': False}, {'t': 'Qor yog\'ishi', 'c': False}]},
    ]},

    {'n': 'Daryo oqimi va sarfi', 't': 30, 'o': 8, 'q': [
        {'t': 'Daryo sarfi nima?', 'a': [{'t': 'Vaqt birligi ichida kesimdan o\'tadigan suv hajmi', 'c': True}, {'t': 'Daryo uzunligi', 'c': False}, {'t': 'Daryo kengligi', 'c': False}, {'t': 'Daryo chuqurligi', 'c': False}]},
        {'t': 'Daryo sarfi qanday o\'lchanadi?', 'a': [{'t': 'Kub metr/soniya (m³/s) da', 'c': True}, {'t': 'Metr da', 'c': False}, {'t': 'Kilogramm da', 'c': False}, {'t': 'Litr da', 'c': False}]},
        {'t': 'O\'rtacha yillik sarfi nima?', 'a': [{'t': 'Bir yil davomidagi o\'rtacha suv sarfi', 'c': True}, {'t': 'Bir oy davomidagi sarfi', 'c': False}, {'t': 'Bir kun davomidagi sarfi', 'c': False}, {'t': 'Maksimal sarfi', 'c': False}]},
        {'t': 'Daryo suvining tezligi nimaga bog\'liq?', 'a': [{'t': 'O\'zak qiyaligi va g\'adir-budurligi', 'c': True}, {'t': 'Faqat suv harorati', 'c': False}, {'t': 'Faqat shamol', 'c': False}, {'t': 'Hech narsaga bog\'liq emas', 'c': False}]},
        {'t': 'Gidropost nima?', 'a': [{'t': 'Daryo suv sathini o\'lchaydigan stansiya', 'c': True}, {'t': 'Pochta bo\'limi', 'c': False}, {'t': 'Elektr stansiyasi', 'c': False}, {'t': 'Suv ombori', 'c': False}]},
        {'t': 'Daryo kesimi nima?', 'a': [{'t': 'Daryo o\'zakining ko\'ndalang kesimi', 'c': True}, {'t': 'Daryo uzunligi', 'c': False}, {'t': 'Daryo chuqurligi', 'c': False}, {'t': 'Daryo kengligi', 'c': False}]},
    ]},

    {'n': 'Daryo oziqlantirish manbalari', 't': 25, 'o': 9, 'q': [
        {'t': 'Daryo oziqlantirish manbalari qaysilar?', 'a': [{'t': 'Yomg\'ir, qor, muzlik, yer osti suvlari', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat qor', 'c': False}, {'t': 'Faqat muzlik', 'c': False}]},
        {'t': 'Yomg\'ir oziqlantirish qaysi hududlarda asosiy?', 'a': [{'t': 'Tropik va ekvatorial hududlarda', 'c': True}, {'t': 'Qutb hududlarida', 'c': False}, {'t': 'Cho\'llarda', 'c': False}, {'t': 'Hamma joyda bir xil', 'c': False}]},
        {'t': 'Qor oziqlantirish qachon muhim?', 'a': [{'t': 'Mo\'tadil va sovuq hududlarda bahor paytida', 'c': True}, {'t': 'Yozda', 'c': False}, {'t': 'Kuzda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Muzlik oziqlantirish qaysi daryolar uchun xos?', 'a': [{'t': 'Tog\' daryolari uchun', 'c': True}, {'t': 'Tekislik daryolari uchun', 'c': False}, {'t': 'Barcha daryolar uchun', 'c': False}, {'t': 'Hech qaysi daryo uchun emas', 'c': False}]},
        {'t': 'Aralash oziqlantirish nima?', 'a': [{'t': 'Bir nechta manba birgalikda daryo oziqlantirishda', 'c': True}, {'t': 'Faqat bitta manba', 'c': False}, {'t': 'Hech qanday manba yo\'q', 'c': False}, {'t': 'Faqat sun\'iy manba', 'c': False}]},
    ]},

    {'n': 'Ko\'llar va ularning turlari', 't': 30, 'o': 10, 'q': [
        {'t': 'Ko\'l nima?', 'a': [{'t': 'Quruqlik ichidagi tabiiy suv ombori', 'c': True}, {'t': 'Sun\'iy suv ombori', 'c': False}, {'t': 'Daryo', 'c': False}, {'t': 'Okean', 'c': False}]},
        {'t': 'Ko\'llar qanday hosil bo\'ladi?', 'a': [{'t': 'Tektonik, vulkanik, muzlik, sun\'iy va boshqa yo\'llar bilan', 'c': True}, {'t': 'Faqat tektonik yo\'l bilan', 'c': False}, {'t': 'Faqat sun\'iy yo\'l bilan', 'c': False}, {'t': 'Hosil bo\'lmaydi', 'c': False}]},
        {'t': 'Tektonik ko\'llar qanday hosil bo\'ladi?', 'a': [{'t': 'Yer qobig\'i harakati natijasida', 'c': True}, {'t': 'Muzlik ta\'sirida', 'c': False}, {'t': 'Vulkan portlashi natijasida', 'c': False}, {'t': 'Inson tomonidan', 'c': False}]},
        {'t': 'Sho\'r ko\'llar qanday hosil bo\'ladi?', 'a': [{'t': 'Bug\'lanish oqimdan ko\'p bo\'lganda', 'c': True}, {'t': 'Dengiz suvi qo\'shilganda', 'c': False}, {'t': 'Tuz qo\'shilganda', 'c': False}, {'t': 'Hosil bo\'lmaydi', 'c': False}]},
        {'t': 'Oqimli ko\'l nima?', 'a': [{'t': 'Daryolar kiradi va chiqadi', 'c': True}, {'t': 'Faqat daryolar kiradi', 'c': False}, {'t': 'Faqat daryolar chiqadi', 'c': False}, {'t': 'Hech qanday daryo yo\'q', 'c': False}]},
        {'t': 'Oqimsiz ko\'l nima?', 'a': [{'t': 'Daryolar faqat kiradi, chiqmaydi', 'c': True}, {'t': 'Hech qanday daryo yo\'q', 'c': False}, {'t': 'Faqat daryolar chiqadi', 'c': False}, {'t': 'Daryolar kiradi va chiqadi', 'c': False}]},
        {'t': 'Ko\'l suvining harorati nimaga bog\'liq?', 'a': [{'t': 'Iqlim, chuqurlik, geografik joylashuv', 'c': True}, {'t': 'Faqat iqlim', 'c': False}, {'t': 'Faqat chuqurlik', 'c': False}, {'t': 'Hech narsaga bog\'liq emas', 'c': False}]},
    ]},

    {'n': 'Suv omborlari va to\'g\'onlar', 't': 30, 'o': 11, 'q': [
        {'t': 'Suv ombori nima?', 'a': [{'t': 'Sun\'iy ravishda yaratilgan katta suv havzasi', 'c': True}, {'t': 'Tabiiy ko\'l', 'c': False}, {'t': 'Daryo', 'c': False}, {'t': 'Okean', 'c': False}]},
        {'t': 'Suv omborlari nima uchun quriladi?', 'a': [{'t': 'Elektr energiyasi, sug\'orish, suv ta\'minoti uchun', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Faqat baliq ovlash uchun', 'c': False}, {'t': 'Hech qanday maqsad yo\'q', 'c': False}]},
        {'t': 'To\'g\'on nima?', 'a': [{'t': 'Daryo oqimini to\'sish uchun qurilgan inshoot', 'c': True}, {'t': 'Ko\'prik', 'c': False}, {'t': 'Bino', 'c': False}, {'t': 'Yo\'l', 'c': False}]},
        {'t': 'Gidroelektr stansiyasi (GES) nima?', 'a': [{'t': 'Suv energiyasidan elektr ishlab chiqaradigan stansiya', 'c': True}, {'t': 'Issiqlik elektr stansiyasi', 'c': False}, {'t': 'Atom elektr stansiyasi', 'c': False}, {'t': 'Shamol elektr stansiyasi', 'c': False}]},
        {'t': 'Suv omborlarining ijobiy tomonlari qaysilar?', 'a': [{'t': 'Elektr energiyasi, sug\'orish, toshqinlarni nazorat qilish', 'c': True}, {'t': 'Faqat elektr energiyasi', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat dam olish joyi', 'c': False}]},
        {'t': 'Suv omborlarining salbiy tomonlari qaysilar?', 'a': [{'t': 'Ekologik muammolar, yerlarning suv ostida qolishi', 'c': True}, {'t': 'Hech qanday salbiy tomoni yo\'q', 'c': False}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat vaqt talab qiladi', 'c': False}]},
        {'t': 'Suv ombori hajmi qanday o\'lchanadi?', 'a': [{'t': 'Kub kilometr (km³) yoki kub metr (m³) da', 'c': True}, {'t': 'Metr da', 'c': False}, {'t': 'Kilogramm da', 'c': False}, {'t': 'Litr da', 'c': False}]},
    ]},

    {'n': 'Muzliklar va qor qoplami', 't': 30, 'o': 12, 'q': [
        {'t': 'Muzlik nima?', 'a': [{'t': 'Ko\'p yillik qor va muzdan iborat katta massa', 'c': True}, {'t': 'Bir yillik qor', 'c': False}, {'t': 'Muzlagan daryo', 'c': False}, {'t': 'Muzlagan ko\'l', 'c': False}]},
        {'t': 'Muzliklar qayerda joylashgan?', 'a': [{'t': 'Qutb hududlari va baland tog\'larda', 'c': True}, {'t': 'Faqat qutblarda', 'c': False}, {'t': 'Faqat tog\'larda', 'c': False}, {'t': 'Hamma joyda', 'c': False}]},
        {'t': 'Muzliklar qanday harakat qiladi?', 'a': [{'t': 'Og\'irlik kuchi ta\'sirida sekin siljiydi', 'c': True}, {'t': 'Tez yuguradi', 'c': False}, {'t': 'Harakat qilmaydi', 'c': False}, {'t': 'Uchib ketadi', 'c': False}]},
        {'t': 'Muzlik erishi nimaga olib keladi?', 'a': [{'t': 'Dengiz sathi ko\'tarilishi va iqlim o\'zgarishi', 'c': True}, {'t': 'Hech narsaga olib kelmaydi', 'c': False}, {'t': 'Faqat suv ko\'payadi', 'c': False}, {'t': 'Faqat sovuq bo\'ladi', 'c': False}]},
        {'t': 'Qor chizig\'i nima?', 'a': [{'t': 'Qor yil bo\'yi saqlanadigan eng past balandlik', 'c': True}, {'t': 'Qor yog\'adigan joy', 'c': False}, {'t': 'Qor qalinligi', 'c': False}, {'t': 'Qor rangi', 'c': False}]},
        {'t': 'Muzlik suvining ahamiyati nima?', 'a': [{'t': 'Ko\'plab daryolar uchun suv manbai', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat sovuq uchun', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}]},
    ]},

    {'n': 'Botqoqlar va ularning ahamiyati', 't': 25, 'o': 13, 'q': [
        {'t': 'Botqoq nima?', 'a': [{'t': 'Suv bilan to\'yingan, o\'simliklar o\'sadigan hudud', 'c': True}, {'t': 'Quruq cho\'l', 'c': False}, {'t': 'Tog\'', 'c': False}, {'t': 'Daryo', 'c': False}]},
        {'t': 'Botqoqlar qanday hosil bo\'ladi?', 'a': [{'t': 'Ortiqcha namlik va yomon drenaj natijasida', 'c': True}, {'t': 'Qurg\'oqchilik natijasida', 'c': False}, {'t': 'Issiqlik natijasida', 'c': False}, {'t': 'Hosil bo\'lmaydi', 'c': False}]},
        {'t': 'Botqoqlarning ekologik ahamiyati nima?', 'a': [{'t': 'Biologik xilma-xillik, suv tozalash, karbonat saqlash', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat zararli', 'c': False}, {'t': 'Faqat joy egallaydi', 'c': False}]},
        {'t': 'Botqoqlar suvni qanday tozalaydi?', 'a': [{'t': 'O\'simliklar va mikroorganizmlar iflosliklarni filtrlaydi', 'c': True}, {'t': 'Tozalamaydi', 'c': False}, {'t': 'Faqat bug\'latadi', 'c': False}, {'t': 'Faqat saqlaydi', 'c': False}]},
        {'t': 'Botqoqlarni quritish qanday oqibatlarga olib keladi?', 'a': [{'t': 'Biologik xilma-xillik yo\'qolishi, iqlim o\'zgarishi', 'c': True}, {'t': 'Hech qanday oqibat yo\'q', 'c': False}, {'t': 'Faqat ijobiy oqibatlar', 'c': False}, {'t': 'Faqat ko\'proq yer', 'c': False}]},
    ]},

    {'n': 'Suv balansi', 't': 30, 'o': 14, 'q': [
        {'t': 'Suv balansi nima?', 'a': [{'t': 'Ma\'lum hududga keladigan va chiqadigan suv miqdorining hisobi', 'c': True}, {'t': 'Faqat yomg\'ir miqdori', 'c': False}, {'t': 'Faqat bug\'lanish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Suv balansi tenglamasi qanday?', 'a': [{'t': 'Kirim - Chiqim = O\'zgarish', 'c': True}, {'t': 'Kirim + Chiqim = O\'zgarish', 'c': False}, {'t': 'Kirim = Chiqim', 'c': False}, {'t': 'Hech qanday tenglama yo\'q', 'c': False}]},
        {'t': 'Suv balansida kirim qismi nima?', 'a': [{'t': 'Yog\'ingarchilik, yer usti va yer osti oqimlari', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat qor', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Suv balansida chiqim qismi nima?', 'a': [{'t': 'Bug\'lanish, oqim, infiltratsiya', 'c': True}, {'t': 'Faqat bug\'lanish', 'c': False}, {'t': 'Faqat oqim', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Suv balansi nima uchun muhim?', 'a': [{'t': 'Suv resurslarini boshqarish va rejalashtirish uchun', 'c': True}, {'t': 'Faqat ilmiy tadqiqotlar uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat darsliklar uchun', 'c': False}]},
        {'t': 'Ijobiy suv balansi nima?', 'a': [{'t': 'Kirim chiqimdan ko\'p', 'c': True}, {'t': 'Chiqim kirimdan ko\'p', 'c': False}, {'t': 'Kirim va chiqim teng', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Salbiy suv balansi nima?', 'a': [{'t': 'Chiqim kirimdan ko\'p', 'c': True}, {'t': 'Kirim chiqimdan ko\'p', 'c': False}, {'t': 'Kirim va chiqim teng', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Suv sifati va ifloslanishi', 't': 30, 'o': 15, 'q': [
        {'t': 'Suv sifati nima?', 'a': [{'t': 'Suvning fizik, kimyoviy va biologik xususiyatlari', 'c': True}, {'t': 'Faqat suv rangi', 'c': False}, {'t': 'Faqat suv ta\'mi', 'c': False}, {'t': 'Faqat suv harorati', 'c': False}]},
        {'t': 'Suv ifloslanishining asosiy manbalari qaysilar?', 'a': [{'t': 'Sanoat, qishloq xo\'jaligi, maishiy chiqindilar', 'c': True}, {'t': 'Faqat sanoat', 'c': False}, {'t': 'Faqat qishloq xo\'jaligi', 'c': False}, {'t': 'Hech qanday manba yo\'q', 'c': False}]},
        {'t': 'Organik ifloslanish nima?', 'a': [{'t': 'Organik moddalar bilan ifloslanish', 'c': True}, {'t': 'Metall bilan ifloslanish', 'c': False}, {'t': 'Tuz bilan ifloslanish', 'c': False}, {'t': 'Hech qanday ifloslanish yo\'q', 'c': False}]},
        {'t': 'Evtrofikatsiya nima?', 'a': [{'t': 'Suvda ozuqa moddalar ortiqcha ko\'payishi', 'c': True}, {'t': 'Suvning tozalanishi', 'c': False}, {'t': 'Suvning muzlashi', 'c': False}, {'t': 'Suvning bug\'lanishi', 'c': False}]},
        {'t': 'Og\'ir metallar suv uchun qanchalik xavfli?', 'a': [{'t': 'Juda xavfli, zaharli va to\'planadi', 'c': True}, {'t': 'Xavfli emas', 'c': False}, {'t': 'Foydali', 'c': False}, {'t': 'Hech qanday ta\'siri yo\'q', 'c': False}]},
        {'t': 'Suv sifatini qanday yaxshilash mumkin?', 'a': [{'t': 'Tozalash inshootlari, ifloslanishni kamaytirish', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Ko\'proq ifloslanish', 'c': False}, {'t': 'Faqat kutish', 'c': False}]},
    ]},

    {'n': 'Suv resurslarini boshqarish', 't': 30, 'o': 16, 'q': [
        {'t': 'Suv resurslarini boshqarish nima?', 'a': [{'t': 'Suv resurslarini samarali va barqaror foydalanish', 'c': True}, {'t': 'Faqat suv yig\'ish', 'c': False}, {'t': 'Faqat suv sarflash', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Suv resurslarini boshqarish nima uchun kerak?', 'a': [{'t': 'Suv tanqisligini oldini olish va barcha ehtiyojlarni qondirish', 'c': True}, {'t': 'Faqat pul tejash uchun', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}, {'t': 'Faqat qonun talabi', 'c': False}]},
        {'t': 'Integrallashgan suv resurslari boshqaruvi (IWRM) nima?', 'a': [{'t': 'Barcha suv foydalanuvchilarni hisobga olgan holda boshqarish', 'c': True}, {'t': 'Faqat sanoat uchun boshqarish', 'c': False}, {'t': 'Faqat qishloq xo\'jaligi uchun', 'c': False}, {'t': 'Hech qanday boshqarish yo\'q', 'c': False}]},
        {'t': 'Suv tejash usullari qaysilar?', 'a': [{'t': 'Samarali sug\'orish, suv qayta ishlash, tejamkor texnologiyalar', 'c': True}, {'t': 'Ko\'proq suv ishlatish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat kamroq yuvish', 'c': False}]},
        {'t': 'Suv huquqi nima?', 'a': [{'t': 'Suv resurslaridan foydalanish huquqi va qoidalari', 'c': True}, {'t': 'Faqat davlat huquqi', 'c': False}, {'t': 'Hech qanday huquq yo\'q', 'c': False}, {'t': 'Faqat boy odamlar huquqi', 'c': False}]},
        {'t': 'Suv tanqisligi nima?', 'a': [{'t': 'Suv talabi mavjud resurslardan ko\'p bo\'lishi', 'c': True}, {'t': 'Suv ko\'p bo\'lishi', 'c': False}, {'t': 'Suv sifati yomon bo\'lishi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Suv xavfsizligi nima?', 'a': [{'t': 'Barcha uchun yetarli va sifatli suv ta\'minoti', 'c': True}, {'t': 'Faqat suv tozaligi', 'c': False}, {'t': 'Faqat suv miqdori', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
    ]},

    {'n': 'Sug\'orish gidrologiyasi', 't': 30, 'o': 17, 'q': [
        {'t': 'Sug\'orish nima?', 'a': [{'t': 'Qishloq xo\'jaligi ekinlariga sun\'iy suv berish', 'c': True}, {'t': 'Tabiiy yomg\'ir', 'c': False}, {'t': 'Tuproqni haydash', 'c': False}, {'t': 'O\'g\'it berish', 'c': False}]},
        {'t': 'Sug\'orish nima uchun kerak?', 'a': [{'t': 'Yog\'ingarchilik yetarli bo\'lmagan hududlarda ekin yetishtirishuchun', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}, {'t': 'Faqat tuproqni yuvish uchun', 'c': False}]},
        {'t': 'Sug\'orish usullari qaysilar?', 'a': [{'t': 'Yer usti, tomchilatib, purkagichli sug\'orish', 'c': True}, {'t': 'Faqat yer usti', 'c': False}, {'t': 'Faqat tomchilatib', 'c': False}, {'t': 'Hech qanday usul yo\'q', 'c': False}]},
        {'t': 'Tomchilatib sug\'orish qanday ishlaydi?', 'a': [{'t': 'Suv to\'g\'ridan-to\'g\'ri o\'simlik ildiziga tomiziladi', 'c': True}, {'t': 'Suv hamma joyga sepiladi', 'c': False}, {'t': 'Suv havoga purkab yuboriladi', 'c': False}, {'t': 'Ishlmaydi', 'c': False}]},
        {'t': 'Qaysi sug\'orish usuli eng tejamkor?', 'a': [{'t': 'Tomchilatib sug\'orish', 'c': True}, {'t': 'Yer usti sug\'orish', 'c': False}, {'t': 'Purkagichli sug\'orish', 'c': False}, {'t': 'Hamma bir xil', 'c': False}]},
        {'t': 'Sug\'orishning salbiy oqibatlari qaysilar?', 'a': [{'t': 'Tuproq sho\'rlanishi, suv isrofi, ekologik muammolar', 'c': True}, {'t': 'Hech qanday salbiy oqibat yo\'q', 'c': False}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat vaqt talab qiladi', 'c': False}]},
        {'t': 'Drenaj nima?', 'a': [{'t': 'Ortiqcha suvni olib tashlash tizimi', 'c': True}, {'t': 'Suv berish tizimi', 'c': False}, {'t': 'Suv tozalash', 'c': False}, {'t': 'Suv saqlash', 'c': False}]},
    ]},

    {'n': 'Toshqinlar va ularning oldini olish', 't': 30, 'o': 18, 'q': [
        {'t': 'Toshqin nima?', 'a': [{'t': 'Suv sathining keskin ko\'tarilib, atrofni bosishi', 'c': True}, {'t': 'Suv kamayishi', 'c': False}, {'t': 'Suv muzlashi', 'c': False}, {'t': 'Suv bug\'lanishi', 'c': False}]},
        {'t': 'Toshqinlarning sabablari qaysilar?', 'a': [{'t': 'Kuchli yomg\'ir, qor erishi, to\'g\'on buzilishi', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat qor', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}]},
        {'t': 'Toshqinlar qanday zarar keltiradi?', 'a': [{'t': 'Uy-joylar, ekinzorlar, infratuzilma buziladi, odamlar halok bo\'ladi', 'c': True}, {'t': 'Hech qanday zarar yo\'q', 'c': False}, {'t': 'Faqat suv ko\'payadi', 'c': False}, {'t': 'Faqat tuproq yuvilib ketadi', 'c': False}]},
        {'t': 'Toshqinlarning oldini olish usullari qaysilar?', 'a': [{'t': 'To\'g\'onlar, suv omborlari, ogohlantirish tizimlari', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat ibodat qilish', 'c': False}, {'t': 'Faqat qochish', 'c': False}]},
        {'t': 'Toshqin xavfi xaritalari nima uchun kerak?', 'a': [{'t': 'Xavfli hududlarni aniqlash va rejalashtirish uchun', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat ilmiy tadqiqotlar uchun', 'c': False}]},
        {'t': 'Toshqin paytida nima qilish kerak?', 'a': [{'t': 'Xavfsiz joyga ko\'chish, ogohlantirishlarga amal qilish', 'c': True}, {'t': 'Uyda qolish', 'c': False}, {'t': 'Suzishga chiqish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
    ]},

    {'n': 'Qurg\'oqchilik va suv tanqisligi', 't': 30, 'o': 19, 'q': [
        {'t': 'Qurg\'oqchilik nima?', 'a': [{'t': 'Uzoq muddat yog\'ingarchilik kamayishi', 'c': True}, {'t': 'Bir kunlik yomg\'irsizlik', 'c': False}, {'t': 'Suv ko\'p bo\'lishi', 'c': False}, {'t': 'Toshqin', 'c': False}]},
        {'t': 'Qurg\'oqchilikning sabablari qaysilar?', 'a': [{'t': 'Iqlim o\'zgarishi, tabiiy tsikllar, inson faoliyati', 'c': True}, {'t': 'Faqat iqlim o\'zgarishi', 'c': False}, {'t': 'Faqat inson faoliyati', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}]},
        {'t': 'Qurg\'oqchilik qanday zarar keltiradi?', 'a': [{'t': 'Ekin nobud bo\'lishi, ochlik, iqtisodiy zarar', 'c': True}, {'t': 'Hech qanday zarar yo\'q', 'c': False}, {'t': 'Faqat tuproq quritiladi', 'c': False}, {'t': 'Faqat issiq bo\'ladi', 'c': False}]},
        {'t': 'Qurg\'oqchilikka qarshi kurashish usullari qaysilar?', 'a': [{'t': 'Suv tejash, samarali sug\'orish, suv omborlari', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Ko\'proq suv ishlatish', 'c': False}, {'t': 'Faqat ibodat qilish', 'c': False}]},
        {'t': 'Cho\'llanish nima?', 'a': [{'t': 'Unumli yerlarning cho\'lga aylanishi', 'c': True}, {'t': 'Cho\'lning kamayishi', 'c': False}, {'t': 'Yomg\'ir ko\'payishi', 'c': False}, {'t': 'O\'rmon ko\'payishi', 'c': False}]},
        {'t': 'Cho\'llanishning sabablari qaysilar?', 'a': [{'t': 'Qurg\'oqchilik, haddan tashqari yaylov, o\'rmon kesish', 'c': True}, {'t': 'Faqat qurg\'oqchilik', 'c': False}, {'t': 'Faqat yaylov', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}]},
    ]},

    {'n': 'Gidrologik prognozlash', 't': 30, 'o': 20, 'q': [
        {'t': 'Gidrologik prognoz nima?', 'a': [{'t': 'Kelajakdagi gidrologik hodisalarni oldindan aytish', 'c': True}, {'t': 'O\'tmishdagi hodisalarni tahlil qilish', 'c': False}, {'t': 'Hozirgi holatni kuzatish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Gidrologik prognoz nima uchun kerak?', 'a': [{'t': 'Toshqin, qurg\'oqchilik va boshqa xavflardan ogohlantirish', 'c': True}, {'t': 'Faqat ilmiy tadqiqotlar uchun', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat darsliklar uchun', 'c': False}]},
        {'t': 'Qisqa muddatli prognoz qancha vaqtga?', 'a': [{'t': 'Bir necha kun yoki hafta', 'c': True}, {'t': 'Bir yil', 'c': False}, {'t': 'O\'n yil', 'c': False}, {'t': 'Bir soat', 'c': False}]},
        {'t': 'Uzoq muddatli prognoz qancha vaqtga?', 'a': [{'t': 'Bir necha oy yoki yil', 'c': True}, {'t': 'Bir kun', 'c': False}, {'t': 'Bir soat', 'c': False}, {'t': 'Bir daqiqa', 'c': False}]},
        {'t': 'Gidrologik prognozda qanday ma\'lumotlar ishlatiladi?', 'a': [{'t': 'Yog\'ingarchilik, harorat, qor qoplami, daryo sarfi', 'c': True}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Faqat harorat', 'c': False}, {'t': 'Hech qanday ma\'lumot yo\'q', 'c': False}]},
        {'t': 'Matematik modellar prognozda qanday ishlatiladi?', 'a': [{'t': 'Gidrologik jarayonlarni simulyatsiya qilish uchun', 'c': True}, {'t': 'Faqat hisoblash uchun', 'c': False}, {'t': 'Ishlatilmaydi', 'c': False}, {'t': 'Faqat chizish uchun', 'c': False}]},
        {'t': 'Prognoz aniqligi nimaga bog\'liq?', 'a': [{'t': 'Ma\'lumotlar sifati, model aniqligi, prognoz muddati', 'c': True}, {'t': 'Faqat omad', 'c': False}, {'t': 'Hech narsaga bog\'liq emas', 'c': False}, {'t': 'Faqat kompyuter tezligi', 'c': False}]},
    ]},

    {'n': 'Gidrologik kuzatuvlar va o\'lchashlar', 't': 30, 'o': 21, 'q': [
        {'t': 'Gidrologik kuzatuv nima?', 'a': [{'t': 'Suv obyektlarining holatini muntazam o\'lchash va qayd qilish', 'c': True}, {'t': 'Faqat bir marta o\'lchash', 'c': False}, {'t': 'Faqat qarash', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Gidropost nima?', 'a': [{'t': 'Daryo suv sathini o\'lchaydigan stansiya', 'c': True}, {'t': 'Pochta bo\'limi', 'c': False}, {'t': 'Elektr stansiyasi', 'c': False}, {'t': 'Suv ombori', 'c': False}]},
        {'t': 'Suv sathi qanday o\'lchanadi?', 'a': [{'t': 'Reyka (o\'lchov chizig\'i) yoki avtomatik datchiklar bilan', 'c': True}, {'t': 'Ko\'z bilan', 'c': False}, {'t': 'Taxmin qilinadi', 'c': False}, {'t': 'O\'lchanmaydi', 'c': False}]},
        {'t': 'Daryo sarfini qanday o\'lchash mumkin?', 'a': [{'t': 'Tezlik va kesim yuzasini o\'lchab, ko\'paytirish orqali', 'c': True}, {'t': 'Faqat ko\'z bilan', 'c': False}, {'t': 'O\'lchash mumkin emas', 'c': False}, {'t': 'Faqat taxmin qilish orqali', 'c': False}]},
        {'t': 'Gidrologik ma\'lumotlar nima uchun kerak?', 'a': [{'t': 'Prognoz, rejalashtirish, tadqiqot uchun', 'c': True}, {'t': 'Faqat arxiv uchun', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat hisobot uchun', 'c': False}]},
        {'t': 'Masofadan zondlash gidrologiyada qanday ishlatiladi?', 'a': [{'t': 'Sun\'iy yo\'ldoshlar orqali keng hududlarni kuzatish', 'c': True}, {'t': 'Ishlatilmaydi', 'c': False}, {'t': 'Faqat suratga olish', 'c': False}, {'t': 'Faqat xarita chizish', 'c': False}]},
    ]},

    {'n': 'Daryo morfologiyasi', 't': 30, 'o': 22, 'q': [
        {'t': 'Daryo morfologiyasi nima?', 'a': [{'t': 'Daryo o\'zagi va vodiy shaklini o\'rganish', 'c': True}, {'t': 'Daryo suvini o\'rganish', 'c': False}, {'t': 'Daryo baliqlarini o\'rganish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Daryo o\'zagi nima?', 'a': [{'t': 'Daryo suvi oqadigan tabiiy ariq', 'c': True}, {'t': 'Daryo tubidagi tosh', 'c': False}, {'t': 'Daryo bo\'yidagi o\'simlik', 'c': False}, {'t': 'Daryo baliq', 'c': False}]},
        {'t': 'Meander nima?', 'a': [{'t': 'Daryo o\'zagining burilish joyi', 'c': True}, {'t': 'To\'g\'ri daryo', 'c': False}, {'t': 'Daryo boshi', 'c': False}, {'t': 'Daryo oxiri', 'c': False}]},
        {'t': 'Daryo terrasasi nima?', 'a': [{'t': 'Daryo vodiyidagi eski daryo sathi qoldig\'i', 'c': True}, {'t': 'Daryo suvi', 'c': False}, {'t': 'Daryo baliq', 'c': False}, {'t': 'Daryo o\'simlik', 'c': False}]},
        {'t': 'Daryo deltasi nima?', 'a': [{'t': 'Daryo dengizga quyiladigan joyda hosil bo\'lgan uchburchak shaklidagi hudud', 'c': True}, {'t': 'Daryo boshi', 'c': False}, {'t': 'Daryo o\'rtasi', 'c': False}, {'t': 'Daryo chuqurligi', 'c': False}]},
        {'t': 'Daryo o\'zagi qanday o\'zgaradi?', 'a': [{'t': 'Eroziya va cho\'kma jarayonlari orqali', 'c': True}, {'t': 'O\'zgarmaydi', 'c': False}, {'t': 'Faqat inson ta\'sirida', 'c': False}, {'t': 'Faqat toshqin paytida', 'c': False}]},
        {'t': 'Daryo profilini nima belgilaydi?', 'a': [{'t': 'Daryo uzunligi bo\'ylab balandlik o\'zgarishi', 'c': True}, {'t': 'Daryo kengligi', 'c': False}, {'t': 'Daryo chuqurligi', 'c': False}, {'t': 'Daryo rangi', 'c': False}]},
    ]},

    {'n': 'Gidrologik tsiklda iqlim o\'zgarishi ta\'siri', 't': 30, 'o': 23, 'q': [
        {'t': 'Iqlim o\'zgarishi gidrologik tsiklga qanday ta\'sir qiladi?', 'a': [{'t': 'Yog\'ingarchilik rejimi, bug\'lanish, muzlik erishi o\'zgaradi', 'c': True}, {'t': 'Hech qanday ta\'sir qilmaydi', 'c': False}, {'t': 'Faqat harorat o\'zgaradi', 'c': False}, {'t': 'Faqat shamol o\'zgaradi', 'c': False}]},
        {'t': 'Global isish muzliklarga qanday ta\'sir qiladi?', 'a': [{'t': 'Muzliklar tezroq eriydi', 'c': True}, {'t': 'Muzliklar ko\'payadi', 'c': False}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}, {'t': 'Muzliklar muzlaydi', 'c': False}]},
        {'t': 'Dengiz sathi ko\'tarilishining sababi nima?', 'a': [{'t': 'Muzliklar erishi va okean suvi kengayishi', 'c': True}, {'t': 'Yomg\'ir ko\'payishi', 'c': False}, {'t': 'Daryo suvi ko\'payishi', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}]},
        {'t': 'Iqlim o\'zgarishi toshqinlarga qanday ta\'sir qiladi?', 'a': [{'t': 'Toshqinlar chastotasi va kuchi oshadi', 'c': True}, {'t': 'Toshqinlar kamayadi', 'c': False}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}, {'t': 'Toshqinlar to\'xtaydi', 'c': False}]},
        {'t': 'Iqlim o\'zgarishi qurg\'oqchilikka qanday ta\'sir qiladi?', 'a': [{'t': 'Ba\'zi hududlarda qurg\'oqchilik ko\'payadi', 'c': True}, {'t': 'Qurg\'oqchilik butunlay yo\'qoladi', 'c': False}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}, {'t': 'Hamma joyda yomg\'ir ko\'payadi', 'c': False}]},
        {'t': 'Iqlim o\'zgarishiga moslashish usullari qaysilar?', 'a': [{'t': 'Suv tejash, samarali boshqarish, infratuzilmani mustahkamlash', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Ko\'proq suv ishlatish', 'c': False}, {'t': 'Faqat kutish', 'c': False}]},
    ]},

    {'n': 'Okean va dengiz gidrologiyasi', 't': 30, 'o': 24, 'q': [
        {'t': 'Okean gidrologiyasi nima?', 'a': [{'t': 'Okean va dengizlarning fizik xususiyatlarini o\'rganish', 'c': True}, {'t': 'Faqat baliqlarni o\'rganish', 'c': False}, {'t': 'Faqat kemalarni o\'rganish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Okean oqimlari nima?', 'a': [{'t': 'Okean suvining katta hajmdagi harakati', 'c': True}, {'t': 'Kichik to\'lqinlar', 'c': False}, {'t': 'Baliq harakati', 'c': False}, {'t': 'Kema harakati', 'c': False}]},
        {'t': 'Okean oqimlariga nima ta\'sir qiladi?', 'a': [{'t': 'Shamol, Yer aylanishi, harorat farqi', 'c': True}, {'t': 'Faqat shamol', 'c': False}, {'t': 'Faqat Oy', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Suv toshqini (to\'lqin) nima?', 'a': [{'t': 'Dengiz sathining davriy ko\'tarilishi va tushishi', 'c': True}, {'t': 'Toshqin', 'c': False}, {'t': 'To\'lqin', 'c': False}, {'t': 'Shamol', 'c': False}]},
        {'t': 'Suv toshqiniga nima sabab bo\'ladi?', 'a': [{'t': 'Oy va Quyoshning tortishish kuchi', 'c': True}, {'t': 'Faqat shamol', 'c': False}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Okean suvi sho\'rligiga nima ta\'sir qiladi?', 'a': [{'t': 'Bug\'lanish, yog\'ingarchilik, muzlik erishi, daryo oqimi', 'c': True}, {'t': 'Faqat bug\'lanish', 'c': False}, {'t': 'Faqat yomg\'ir', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Okean gidrologiyasi nima uchun muhim?', 'a': [{'t': 'Iqlim, baliqchilik, transport uchun', 'c': True}, {'t': 'Faqat ilmiy tadqiqotlar uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat sayohat uchun', 'c': False}]},
    ]},

    {'n': 'Suv ekologiyasi', 't': 30, 'o': 25, 'q': [
        {'t': 'Suv ekologiyasi nima?', 'a': [{'t': 'Suv ekotizimlarini va ularning o\'zaro ta\'sirini o\'rganish', 'c': True}, {'t': 'Faqat baliqlarni o\'rganish', 'c': False}, {'t': 'Faqat o\'simliklarni o\'rganish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Suv ekotizimi nima?', 'a': [{'t': 'Suv muhitidagi tirik organizmlar va ularning muhiti', 'c': True}, {'t': 'Faqat suv', 'c': False}, {'t': 'Faqat baliqlar', 'c': False}, {'t': 'Faqat o\'simliklar', 'c': False}]},
        {'t': 'Suv ekotizimining asosiy komponentlari qaysilar?', 'a': [{'t': 'Ishlab chiqaruvchilar, iste\'molchilar, parchalovchilar', 'c': True}, {'t': 'Faqat baliqlar', 'c': False}, {'t': 'Faqat suv', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Fitoplankton nima?', 'a': [{'t': 'Suvda suzuvchi mikroskopik o\'simliklar', 'c': True}, {'t': 'Katta baliqlar', 'c': False}, {'t': 'Suv o\'tlari', 'c': False}, {'t': 'Toshlar', 'c': False}]},
        {'t': 'Zooplankton nima?', 'a': [{'t': 'Suvda suzuvchi mikroskopik hayvonlar', 'c': True}, {'t': 'Katta baliqlar', 'c': False}, {'t': 'O\'simliklar', 'c': False}, {'t': 'Toshlar', 'c': False}]},
        {'t': 'Suv ekotizimida kislorod qanday hosil bo\'ladi?', 'a': [{'t': 'Suv o\'simliklari fotosintez orqali', 'c': True}, {'t': 'Baliqlar nafas oladi', 'c': False}, {'t': 'Havoda hosil bo\'ladi', 'c': False}, {'t': 'Hosil bo\'lmaydi', 'c': False}]},
        {'t': 'Suv ekotizimining sog\'ligi nimaga bog\'liq?', 'a': [{'t': 'Suv sifati, biologik xilma-xillik, ozuqa zanjiri', 'c': True}, {'t': 'Faqat suv miqdori', 'c': False}, {'t': 'Faqat baliq soni', 'c': False}, {'t': 'Hech narsaga bog\'liq emas', 'c': False}]},
    ]},

    {'n': 'Gidrotexnik inshootlar', 't': 30, 'o': 26, 'q': [
        {'t': 'Gidrotexnik inshoot nima?', 'a': [{'t': 'Suv bilan bog\'liq muhandislik inshootlari', 'c': True}, {'t': 'Oddiy bino', 'c': False}, {'t': 'Yo\'l', 'c': False}, {'t': 'Ko\'prik', 'c': False}]},
        {'t': 'Gidrotexnik inshootlar turlari qaysilar?', 'a': [{'t': 'To\'g\'on, kanal, nasos stansiyasi, suv ombori', 'c': True}, {'t': 'Faqat to\'g\'on', 'c': False}, {'t': 'Faqat kanal', 'c': False}, {'t': 'Hech qanday tur yo\'q', 'c': False}]},
        {'t': 'To\'g\'on nima uchun quriladi?', 'a': [{'t': 'Suv to\'plash, elektr energiyasi, toshqin nazorati', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday maqsad yo\'q', 'c': False}, {'t': 'Faqat yo\'l uchun', 'c': False}]},
        {'t': 'Kanal nima?', 'a': [{'t': 'Sun\'iy suv yo\'li', 'c': True}, {'t': 'Tabiiy daryo', 'c': False}, {'t': 'Ko\'l', 'c': False}, {'t': 'Okean', 'c': False}]},
        {'t': 'Nasos stansiyasi nima qiladi?', 'a': [{'t': 'Suvni bir joydan boshqa joyga ko\'taradi yoki haydaydi', 'c': True}, {'t': 'Suvni tozalaydi', 'c': False}, {'t': 'Suvni isitadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Shlyuz nima?', 'a': [{'t': 'Kemalar uchun suv sathini o\'zgartiruvchi inshoot', 'c': True}, {'t': 'To\'g\'on', 'c': False}, {'t': 'Ko\'prik', 'c': False}, {'t': 'Bino', 'c': False}]},
        {'t': 'Gidrotexnik inshootlarning xavfsizligi nima uchun muhim?', 'a': [{'t': 'Buzilishi katta falokatga olib kelishi mumkin', 'c': True}, {'t': 'Muhim emas', 'c': False}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat chiroyli bo\'lishi uchun', 'c': False}]},
    ]},

    {'n': 'Suv tozalash va qayta ishlash', 't': 30, 'o': 27, 'q': [
        {'t': 'Suv tozalash nima?', 'a': [{'t': 'Suvdan iflosliklarni olib tashlash jarayoni', 'c': True}, {'t': 'Suvni isitish', 'c': False}, {'t': 'Suvni sovutish', 'c': False}, {'t': 'Suvni saqlash', 'c': False}]},
        {'t': 'Suv tozalash nima uchun kerak?', 'a': [{'t': 'Xavfsiz ichimlik suvi va ekologiya uchun', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday sabab yo\'q', 'c': False}, {'t': 'Faqat qonun talabi', 'c': False}]},
        {'t': 'Suv tozalash bosqichlari qaysilar?', 'a': [{'t': 'Mexanik, biologik, kimyoviy tozalash', 'c': True}, {'t': 'Faqat mexanik', 'c': False}, {'t': 'Faqat kimyoviy', 'c': False}, {'t': 'Hech qanday bosqich yo\'q', 'c': False}]},
        {'t': 'Mexanik tozalash nima?', 'a': [{'t': 'Katta qattiq zarralarni filtrlash orqali olib tashlash', 'c': True}, {'t': 'Kimyoviy moddalar qo\'shish', 'c': False}, {'t': 'Bakteriyalar bilan tozalash', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Biologik tozalash nima?', 'a': [{'t': 'Mikroorganizmlar yordamida organik moddalarni parchalash', 'c': True}, {'t': 'Filtrdan o\'tkazish', 'c': False}, {'t': 'Kimyoviy moddalar qo\'shish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Suv qayta ishlash nima?', 'a': [{'t': 'Ishlatilgan suvni tozalab, qayta foydalanish', 'c': True}, {'t': 'Suvni tashlash', 'c': False}, {'t': 'Suvni saqlash', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Suv qayta ishlash nima uchun foydali?', 'a': [{'t': 'Suv tejash va ekologiyani muhofaza qilish', 'c': True}, {'t': 'Faqat pul tejash', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat qonun talabi', 'c': False}]},
    ]},

    {'n': 'Gidrologiyada zamonaviy texnologiyalar', 't': 30, 'o': 28, 'q': [
        {'t': 'Masofadan zondlash gidrologiyada qanday ishlatiladi?', 'a': [{'t': 'Sun\'iy yo\'ldoshlar orqali suv resurslarini kuzatish', 'c': True}, {'t': 'Ishlatilmaydi', 'c': False}, {'t': 'Faqat suratga olish', 'c': False}, {'t': 'Faqat xarita chizish', 'c': False}]},
        {'t': 'GIS (Geografik Axborot Tizimi) gidrologiyada nima uchun?', 'a': [{'t': 'Gidrologik ma\'lumotlarni tahlil qilish va vizualizatsiya qilish', 'c': True}, {'t': 'Faqat xarita chizish', 'c': False}, {'t': 'Ishlatilmaydi', 'c': False}, {'t': 'Faqat ma\'lumot saqlash', 'c': False}]},
        {'t': 'Avtomatik datchiklar qanday foyda beradi?', 'a': [{'t': 'Doimiy va aniq ma\'lumotlar to\'plash', 'c': True}, {'t': 'Hech qanday foyda yo\'q', 'c': False}, {'t': 'Faqat qimmat', 'c': False}, {'t': 'Faqat murakkab', 'c': False}]},
        {'t': 'Gidrologik modellashtirish nima?', 'a': [{'t': 'Kompyuter yordamida gidrologik jarayonlarni simulyatsiya qilish', 'c': True}, {'t': 'Qo\'lda hisoblash', 'c': False}, {'t': 'Faqat chizish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Sun\'iy intellekt gidrologiyada qanday ishlatiladi?', 'a': [{'t': 'Prognozlash, ma\'lumotlar tahlili, qarorlar qabul qilish', 'c': True}, {'t': 'Ishlatilmaydi', 'c': False}, {'t': 'Faqat o\'yin uchun', 'c': False}, {'t': 'Faqat rasm chizish', 'c': False}]},
        {'t': 'IoT (Internet of Things) gidrologiyada nima beradi?', 'a': [{'t': 'Datchiklar tarmog\'i orqali real vaqtda monitoring', 'c': True}, {'t': 'Hech narsa bermaydi', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat telefon', 'c': False}]},
        {'t': 'Zamonaviy texnologiyalar gidrologiyani qanday yaxshilaydi?', 'a': [{'t': 'Aniqlik, tezlik, samaradorlik oshadi', 'c': True}, {'t': 'Hech qanday yaxshilanish yo\'q', 'c': False}, {'t': 'Faqat qimmatroq bo\'ladi', 'c': False}, {'t': 'Faqat murakkab bo\'ladi', 'c': False}]},
    ]},

    {'n': 'Xalqaro suv muammolari', 't': 30, 'o': 29, 'q': [
        {'t': 'Xalqaro suv muammolari nima?', 'a': [{'t': 'Bir nechta davlat o\'rtasidagi suv resurslari bilan bog\'liq muammolar', 'c': True}, {'t': 'Faqat bitta davlat muammosi', 'c': False}, {'t': 'Hech qanday muammo yo\'q', 'c': False}, {'t': 'Faqat okean muammolari', 'c': False}]},
        {'t': 'Transchegaraviy daryolar nima?', 'a': [{'t': 'Bir nechta davlat hududidan o\'tadigan daryolar', 'c': True}, {'t': 'Faqat bitta davlatdagi daryolar', 'c': False}, {'t': 'Sun\'iy daryolar', 'c': False}, {'t': 'Hech qanday daryo yo\'q', 'c': False}]},
        {'t': 'Transchegaraviy daryolar bo\'yicha qanday muammolar bor?', 'a': [{'t': 'Suv taqsimoti, ifloslanish, to\'g\'onlar qurish', 'c': True}, {'t': 'Hech qanday muammo yo\'q', 'c': False}, {'t': 'Faqat baliqchilik', 'c': False}, {'t': 'Faqat transport', 'c': False}]},
        {'t': 'Suv diplomatiyasi nima?', 'a': [{'t': 'Davlatlar o\'rtasida suv masalalarini tinch yo\'l bilan hal qilish', 'c': True}, {'t': 'Urush', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat savdo', 'c': False}]},
        {'t': 'Xalqaro suv shartnomasi nima?', 'a': [{'t': 'Davlatlar o\'rtasida suv foydalanish qoidalarini belgilovchi hujjat', 'c': True}, {'t': 'Oddiy xat', 'c': False}, {'t': 'Hech qanday hujjat yo\'q', 'c': False}, {'t': 'Faqat taklif', 'c': False}]},
        {'t': 'Global suv inqirozi nima?', 'a': [{'t': 'Dunyo miqyosida suv tanqisligi va sifat muammolari', 'c': True}, {'t': 'Suv ko\'p bo\'lishi', 'c': False}, {'t': 'Hech qanday inqiroz yo\'q', 'c': False}, {'t': 'Faqat bitta davlat muammosi', 'c': False}]},
        {'t': 'Xalqaro hamkorlik nima uchun kerak?', 'a': [{'t': 'Suv resurslarini adolatli va samarali boshqarish uchun', 'c': True}, {'t': 'Hech qanday sabab yo\'q', 'c': False}, {'t': 'Faqat siyosiy sabablarga ko\'ra', 'c': False}, {'t': 'Faqat iqtisodiy sabablarga ko\'ra', 'c': False}]},
    ]},

    {'n': 'Barqaror suv boshqaruvi va kelajak', 't': 30, 'o': 30, 'q': [
        {'t': 'Barqaror suv boshqaruvi nima?', 'a': [{'t': 'Kelajak avlodlar uchun suv resurslarini saqlagan holda foydalanish', 'c': True}, {'t': 'Faqat hozir foydalanish', 'c': False}, {'t': 'Hech qanday boshqarish yo\'q', 'c': False}, {'t': 'Faqat ko\'p ishlatish', 'c': False}]},
        {'t': 'Barqaror rivojlanish maqsadlari (SDG) da suv qaysi o\'rinda?', 'a': [{'t': '6-maqsad: Toza suv va sanitariya', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Oxirgi o\'rinda', 'c': False}, {'t': 'Faqat eslatma', 'c': False}]},
        {'t': 'Suv xavfsizligi nima?', 'a': [{'t': 'Barcha uchun yetarli, xavfsiz va arzon suv ta\'minoti', 'c': True}, {'t': 'Faqat boy odamlar uchun suv', 'c': False}, {'t': 'Hech qanday xavfsizlik yo\'q', 'c': False}, {'t': 'Faqat shahar uchun suv', 'c': False}]},
        {'t': 'Kelajakda suv muammolari qanday bo\'ladi?', 'a': [{'t': 'Aholi o\'sishi va iqlim o\'zgarishi tufayli kuchayadi', 'c': True}, {'t': 'Butunlay yo\'qoladi', 'c': False}, {'t': 'Hech qanday muammo bo\'lmaydi', 'c': False}, {'t': 'Kamayadi', 'c': False}]},
        {'t': 'Suv tejash texnologiyalari qaysilar?', 'a': [{'t': 'Tomchilatib sug\'orish, suv qayta ishlash, tejamkor jihozlar', 'c': True}, {'t': 'Ko\'proq suv ishlatish', 'c': False}, {'t': 'Hech qanday texnologiya yo\'q', 'c': False}, {'t': 'Faqat eski usullar', 'c': False}]},
        {'t': 'Suv ta\'limi nima uchun muhim?', 'a': [{'t': 'Odamlar suv qiymatini tushunib, tejaydilar', 'c': True}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat maktab uchun', 'c': False}, {'t': 'Faqat olimlar uchun', 'c': False}]},
        {'t': 'Har bir inson suv muhofazasida nima qila oladi?', 'a': [{'t': 'Suv tejash, ifloslanishni kamaytirish, boshqalarni o\'rgatish', 'c': True}, {'t': 'Hech narsa qila olmaydi', 'c': False}, {'t': 'Faqat ko\'p suv ishlatish', 'c': False}, {'t': 'Faqat kutish', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_hydrology()
    add_topics(subj, T)
    print(f"\n✅ Gidrologiya fani uchun {len(T)} ta mavzu muvaffaqiyatli qo\'shildi!")
