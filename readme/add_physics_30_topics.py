"""
NAZARIY FIZIKA - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_physics():
    cat, _ = SubjectCategory.objects.get_or_create(slug='fan', defaults={'name': 'Fan', 'icon': 'bi-book', 'order': 1, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Nazariy Fizika', defaults={'category': cat, 'description': 'Nazariy fizika - tabiat qonuniyatlarini matematik usullar bilan o\'rganish', 'icon': 'bi-atom', 'order': 5, 'is_active': True})
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
    {'n': 'Fizika faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Fizika nima?', 'a': [{'t': 'Tabiat hodisalarini o\'rganuvchi fan', 'c': True}, {'t': 'Faqat mexanika', 'c': False}, {'t': 'Kimyo fani', 'c': False}, {'t': 'Matematika', 'c': False}]},
        {'t': 'Nazariy fizika nima bilan shug\'ullanadi?', 'a': [{'t': 'Fizik qonunlarni matematik usullar bilan o\'rganish', 'c': True}, {'t': 'Faqat tajriba o\'tkazish', 'c': False}, {'t': 'Asboblar yasash', 'c': False}, {'t': 'Kimyoviy reaksiyalar', 'c': False}]},
        {'t': 'Fizikaning asosiy bo\'limlari qaysilar?', 'a': [{'t': 'Mexanika, termodinamika, elektrodinamika, kvant fizikasi', 'c': True}, {'t': 'Faqat mexanika', 'c': False}, {'t': 'Faqat optika', 'c': False}, {'t': 'Faqat akustika', 'c': False}]},
        {'t': 'Fizik kattalik nima?', 'a': [{'t': 'O\'lchanishi mumkin bo\'lgan xususiyat', 'c': True}, {'t': 'Faqat massa', 'c': False}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Rang', 'c': False}]},
        {'t': 'SI sistemasida asosiy birliklar nechta?', 'a': [{'t': '7 ta', 'c': True}, {'t': '5 ta', 'c': False}, {'t': '10 ta', 'c': False}, {'t': '3 ta', 'c': False}]},
    ]},

    {'n': 'Fizik kattaliklar va o\'lchov birliklari', 't': 25, 'o': 2, 'q': [
        {'t': 'SI sistemasida uzunlik birligi nima?', 'a': [{'t': 'Metr (m)', 'c': True}, {'t': 'Santimetr', 'c': False}, {'t': 'Kilometr', 'c': False}, {'t': 'Fut', 'c': False}]},
        {'t': 'Massa birligi nima?', 'a': [{'t': 'Kilogramm (kg)', 'c': True}, {'t': 'Gramm', 'c': False}, {'t': 'Tonna', 'c': False}, {'t': 'Funt', 'c': False}]},
        {'t': 'Vaqt birligi nima?', 'a': [{'t': 'Sekund (s)', 'c': True}, {'t': 'Minut', 'c': False}, {'t': 'Soat', 'c': False}, {'t': 'Kun', 'c': False}]},
        {'t': 'Harorat birligi (SI)?', 'a': [{'t': 'Kelvin (K)', 'c': True}, {'t': 'Selsiy', 'c': False}, {'t': 'Farengeyt', 'c': False}, {'t': 'Gradus', 'c': False}]},
        {'t': 'Tok kuchi birligi nima?', 'a': [{'t': 'Amper (A)', 'c': True}, {'t': 'Volt', 'c': False}, {'t': 'Om', 'c': False}, {'t': 'Vatt', 'c': False}]},
        {'t': 'Yorug\'lik intensivligi birligi?', 'a': [{'t': 'Kandela (cd)', 'c': True}, {'t': 'Lyumen', 'c': False}, {'t': 'Lyuks', 'c': False}, {'t': 'Vatt', 'c': False}]},
        {'t': 'Modda miqdori birligi?', 'a': [{'t': 'Mol (mol)', 'c': True}, {'t': 'Gramm', 'c': False}, {'t': 'Litr', 'c': False}, {'t': 'Kilogramm', 'c': False}]},
    ]},

    {'n': 'Harakat tushunchasi va yo\'l', 't': 25, 'o': 3, 'q': [
        {'t': 'Mexanik harakat nima?', 'a': [{'t': 'Jismning boshqa jismlarga nisbatan o\'rin almashtirishi', 'c': True}, {'t': 'Faqat tezlik', 'c': False}, {'t': 'Faqat yo\'l', 'c': False}, {'t': 'Issiqlik', 'c': False}]},
        {'t': 'Yo\'l nima?', 'a': [{'t': 'Jism bosib o\'tgan masofa', 'c': True}, {'t': 'Vaqt', 'c': False}, {'t': 'Tezlik', 'c': False}, {'t': 'Massa', 'c': False}]},
        {'t': 'Ko\'chish nima?', 'a': [{'t': 'Boshlang\'ich va oxirgi nuqtalar orasidagi to\'g\'ri chiziq', 'c': True}, {'t': 'Yo\'l bilan bir xil', 'c': False}, {'t': 'Vaqt', 'c': False}, {'t': 'Tezlik', 'c': False}]},
        {'t': 'Yo\'l va ko\'chish har doim tengmi?', 'a': [{'t': 'Yo\'q, faqat to\'g\'ri chiziqli harakatda', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat aylanma harakatda', 'c': False}]},
        {'t': 'Sanoq sistemasi nima?', 'a': [{'t': 'Harakatni kuzatish uchun tanlab olingan jism va koordinatalar', 'c': True}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Faqat koordinatalar', 'c': False}, {'t': 'Massa', 'c': False}]},
        {'t': 'Traektoriya nima?', 'a': [{'t': 'Jism harakat qilgan chiziq', 'c': True}, {'t': 'Tezlik', 'c': False}, {'t': 'Vaqt', 'c': False}, {'t': 'Massa', 'c': False}]},
    ]},

    {'n': 'Tezlik va tezlanish', 't': 30, 'o': 4, 'q': [
        {'t': 'Tezlik nima?', 'a': [{'t': 'Jismning vaqt birligi ichida bosib o\'tgan yo\'li', 'c': True}, {'t': 'Faqat yo\'l', 'c': False}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Massa', 'c': False}]},
        {'t': 'Tezlik formulasi qanday?', 'a': [{'t': 'v = s/t', 'c': True}, {'t': 'v = t/s', 'c': False}, {'t': 'v = s*t', 'c': False}, {'t': 'v = m/t', 'c': False}]},
        {'t': 'Tezlik birligi (SI)?', 'a': [{'t': 'm/s (metr/sekund)', 'c': True}, {'t': 'km/soat', 'c': False}, {'t': 'm/min', 'c': False}, {'t': 'km/s', 'c': False}]},
        {'t': 'Tezlanish nima?', 'a': [{'t': 'Tezlikning vaqt bo\'yicha o\'zgarishi', 'c': True}, {'t': 'Faqat tezlik', 'c': False}, {'t': 'Faqat yo\'l', 'c': False}, {'t': 'Massa', 'c': False}]},
        {'t': 'Tezlanish formulasi?', 'a': [{'t': 'a = (v - v₀)/t', 'c': True}, {'t': 'a = v*t', 'c': False}, {'t': 'a = s/t', 'c': False}, {'t': 'a = m*v', 'c': False}]},
        {'t': 'Tezlanish birligi?', 'a': [{'t': 'm/s² (metr/sekund kvadrat)', 'c': True}, {'t': 'm/s', 'c': False}, {'t': 'km/s²', 'c': False}, {'t': 'N', 'c': False}]},
        {'t': 'Tekis harakat nima?', 'a': [{'t': 'Tezlik o\'zgarmaydigan harakat', 'c': True}, {'t': 'Tezlanish bor harakat', 'c': False}, {'t': 'Faqat to\'xtash', 'c': False}, {'t': 'Aylanma harakat', 'c': False}]},
        {'t': 'Tekis tezlanuvchan harakat nima?', 'a': [{'t': 'Tezlanish o\'zgarmas bo\'lgan harakat', 'c': True}, {'t': 'Tezlik o\'zgarmas', 'c': False}, {'t': 'Harakat yo\'q', 'c': False}, {'t': 'Faqat sekinlashuv', 'c': False}]},
    ]},

    {'n': 'Nyutonning birinchi qonuni', 't': 25, 'o': 5, 'q': [
        {'t': 'Nyutonning birinchi qonuni nima?', 'a': [{'t': 'Jism tinch yoki tekis harakatda qoladi, agar unga kuch ta\'sir qilmasa', 'c': True}, {'t': 'F = ma', 'c': False}, {'t': 'Ta\'sir = Aks ta\'sir', 'c': False}, {'t': 'E = mc²', 'c': False}]},
        {'t': 'Inertsiya nima?', 'a': [{'t': 'Jismning holatini saqlab qolish xususiyati', 'c': True}, {'t': 'Tezlik', 'c': False}, {'t': 'Kuch', 'c': False}, {'t': 'Massa', 'c': False}]},
        {'t': 'Inersial sanoq sistemasi nima?', 'a': [{'t': 'Nyutonning birinchi qonuni bajariladi', 'c': True}, {'t': 'Tezlanuvchan sistema', 'c': False}, {'t': 'Aylanuvchi sistema', 'c': False}, {'t': 'Noinersial sistema', 'c': False}]},
        {'t': 'Inertsiya massaga bog\'liqmi?', 'a': [{'t': 'Ha, massa katta bo\'lsa inertsiya katta', 'c': True}, {'t': 'Yo\'q, bog\'liq emas', 'c': False}, {'t': 'Faqat tezlikka bog\'liq', 'c': False}, {'t': 'Faqat kuchga bog\'liq', 'c': False}]},
        {'t': 'Kosmosda inertsiya bormi?', 'a': [{'t': 'Ha, hamma joyda bor', 'c': True}, {'t': 'Yo\'q', 'c': False}, {'t': 'Faqat Yerda', 'c': False}, {'t': 'Faqat havoda', 'c': False}]},
    ]},

    {'n': 'Nyutonning ikkinchi qonuni', 't': 30, 'o': 6, 'q': [
        {'t': 'Nyutonning ikkinchi qonuni formulasi?', 'a': [{'t': 'F = ma', 'c': True}, {'t': 'F = mv', 'c': False}, {'t': 'F = m/a', 'c': False}, {'t': 'F = a/m', 'c': False}]},
        {'t': 'Kuch birligi (SI)?', 'a': [{'t': 'Nyuton (N)', 'c': True}, {'t': 'Kilogramm', 'c': False}, {'t': 'Metr', 'c': False}, {'t': 'Joul', 'c': False}]},
        {'t': '1 Nyuton nima?', 'a': [{'t': '1 kg massaga 1 m/s² tezlanish beruvchi kuch', 'c': True}, {'t': '1 kg massa', 'c': False}, {'t': '1 m/s tezlik', 'c': False}, {'t': '1 Joul energiya', 'c': False}]},
        {'t': 'Massa 2 kg, tezlanish 3 m/s². Kuch necha?', 'a': [{'t': '6 N', 'c': True}, {'t': '5 N', 'c': False}, {'t': '2 N', 'c': False}, {'t': '3 N', 'c': False}]},
        {'t': 'Kuch ortsa tezlanish qanday o\'zgaradi?', 'a': [{'t': 'Ortadi', 'c': True}, {'t': 'Kamayadi', 'c': False}, {'t': 'O\'zgarmaydi', 'c': False}, {'t': 'Nolga teng bo\'ladi', 'c': False}]},
        {'t': 'Massa ortsa tezlanish qanday o\'zgaradi (kuch o\'zgarmas)?', 'a': [{'t': 'Kamayadi', 'c': True}, {'t': 'Ortadi', 'c': False}, {'t': 'O\'zgarmaydi', 'c': False}, {'t': 'Ikki barobar ortadi', 'c': False}]},
        {'t': 'Bir nechta kuch ta\'sir qilsa?', 'a': [{'t': 'Natija kuch topiladi (vektor yig\'indi)', 'c': True}, {'t': 'Faqat birinchi kuch hisoblanadi', 'c': False}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}, {'t': 'Kuchlar ayriladi', 'c': False}]},
    ]},

    {'n': 'Nyutonning uchinchi qonuni', 't': 25, 'o': 7, 'q': [
        {'t': 'Nyutonning uchinchi qonuni nima?', 'a': [{'t': 'Ta\'sir kuchi aks ta\'sir kuchiga teng va qarama-qarshi yo\'nalgan', 'c': True}, {'t': 'F = ma', 'c': False}, {'t': 'Inertsiya qonuni', 'c': False}, {'t': 'E = mc²', 'c': False}]},
        {'t': 'Ta\'sir va aks ta\'sir kuchlari qaysi jismlarga qo\'yiladi?', 'a': [{'t': 'Turli jismlarga', 'c': True}, {'t': 'Bir xil jismga', 'c': False}, {'t': 'Faqat birinchi jismga', 'c': False}, {'t': 'Hech qaysi jismga emas', 'c': False}]},
        {'t': 'Siz devorni itsangiz, devor sizni itadi. Bu qaysi qonun?', 'a': [{'t': 'Nyutonning uchinchi qonuni', 'c': True}, {'t': 'Birinchi qonun', 'c': False}, {'t': 'Ikkinchi qonun', 'c': False}, {'t': 'Gravitatsiya qonuni', 'c': False}]},
        {'t': 'Raketa qanday uchadi?', 'a': [{'t': 'Gaz chiqaradi, gaz raketani itadi (3-qonun)', 'c': True}, {'t': 'Havoga suyanadi', 'c': False}, {'t': 'Magnit maydon', 'c': False}, {'t': 'Gravitatsiya', 'c': False}]},
        {'t': 'Ta\'sir va aks ta\'sir kuchlari bir-birini yo\'q qiladimi?', 'a': [{'t': 'Yo\'q, turli jismlarga ta\'sir qiladi', 'c': True}, {'t': 'Ha, yo\'q qiladi', 'c': False}, {'t': 'Ba\'zan yo\'q qiladi', 'c': False}, {'t': 'Faqat kosmosda', 'c': False}]},
    ]},

    {'n': 'Gravitatsiya va og\'irlik kuchi', 't': 30, 'o': 8, 'q': [
        {'t': 'Gravitatsiya nima?', 'a': [{'t': 'Massali jismlar orasidagi tortishish kuchi', 'c': True}, {'t': 'Elektr kuchi', 'c': False}, {'t': 'Magnit kuchi', 'c': False}, {'t': 'Ishqalanish kuchi', 'c': False}]},
        {'t': 'Umumiy gravitatsiya qonuni formulasi?', 'a': [{'t': 'F = G(m₁m₂)/r²', 'c': True}, {'t': 'F = ma', 'c': False}, {'t': 'F = mg', 'c': False}, {'t': 'F = kx', 'c': False}]},
        {'t': 'G nima (gravitatsiya doimiysi)?', 'a': [{'t': '6.67×10⁻¹¹ N·m²/kg²', 'c': True}, {'t': '9.8 m/s²', 'c': False}, {'t': '3×10⁸ m/s', 'c': False}, {'t': '1.6×10⁻¹⁹ C', 'c': False}]},
        {'t': 'Og\'irlik kuchi nima?', 'a': [{'t': 'Yerning jismga ta\'sir qiluvchi tortishish kuchi', 'c': True}, {'t': 'Jism massasi', 'c': False}, {'t': 'Ishqalanish kuchi', 'c': False}, {'t': 'Elastiklik kuchi', 'c': False}]},
        {'t': 'Og\'irlik kuchi formulasi?', 'a': [{'t': 'P = mg', 'c': True}, {'t': 'P = ma', 'c': False}, {'t': 'P = mv', 'c': False}, {'t': 'P = m/g', 'c': False}]},
        {'t': 'g nima (erkin tushish tezlanishi)?', 'a': [{'t': '≈9.8 m/s² (Yer yuzasida)', 'c': True}, {'t': '10 m/s', 'c': False}, {'t': '6.67×10⁻¹¹', 'c': False}, {'t': '3×10⁸ m/s', 'c': False}]},
        {'t': 'Massa va og\'irlik bir xilmi?', 'a': [{'t': 'Yo\'q, massa - modda miqdori, og\'irlik - kuch', 'c': True}, {'t': 'Ha, bir xil', 'c': False}, {'t': 'Faqat Yerda bir xil', 'c': False}, {'t': 'Faqat kosmosda farq qiladi', 'c': False}]},
        {'t': 'Oyda og\'irlik kuchi qanday?', 'a': [{'t': 'Yernikidan 6 marta kichik', 'c': True}, {'t': 'Yerdagidek', 'c': False}, {'t': 'Nolga teng', 'c': False}, {'t': 'Yernikidan katta', 'c': False}]},
    ]},

    {'n': 'Ishqalanish kuchi', 't': 25, 'o': 9, 'q': [
        {'t': 'Ishqalanish kuchi nima?', 'a': [{'t': 'Harakatga qarshi yo\'nalgan kuch', 'c': True}, {'t': 'Harakat yo\'nalishidagi kuch', 'c': False}, {'t': 'Gravitatsiya kuchi', 'c': False}, {'t': 'Elastiklik kuchi', 'c': False}]},
        {'t': 'Ishqalanish kuchi formulasi?', 'a': [{'t': 'F = μN', 'c': True}, {'t': 'F = ma', 'c': False}, {'t': 'F = mg', 'c': False}, {'t': 'F = kx', 'c': False}]},
        {'t': 'μ (myu) nima?', 'a': [{'t': 'Ishqalanish koeffitsienti', 'c': True}, {'t': 'Massa', 'c': False}, {'t': 'Tezlik', 'c': False}, {'t': 'Kuch', 'c': False}]},
        {'t': 'N nima (ishqalanish formulasida)?', 'a': [{'t': 'Reaksiya kuchi (normal kuch)', 'c': True}, {'t': 'Nyuton birligi', 'c': False}, {'t': 'Massa', 'c': False}, {'t': 'Tezlik', 'c': False}]},
        {'t': 'Ishqalanish foydali bo\'lishi mumkinmi?', 'a': [{'t': 'Ha, masalan yurish, tormozlash uchun kerak', 'c': True}, {'t': 'Yo\'q, har doim zararli', 'c': False}, {'t': 'Faqat suvda', 'c': False}, {'t': 'Faqat havoda', 'c': False}]},
        {'t': 'Ishqalanishni kamaytirish usullari?', 'a': [{'t': 'Moylab qo\'yish, silliq sirt, g\'ildirak', 'c': True}, {'t': 'Og\'irlik qo\'shish', 'c': False}, {'t': 'Tezlikni oshirish', 'c': False}, {'t': 'Kamaytirish mumkin emas', 'c': False}]},
    ]},

    {'n': 'Ish va quvvat', 't': 30, 'o': 10, 'q': [
        {'t': 'Mexanik ish nima?', 'a': [{'t': 'Kuch ta\'sirida jism ko\'chganda bajarilgan ish', 'c': True}, {'t': 'Faqat harakat', 'c': False}, {'t': 'Faqat kuch', 'c': False}, {'t': 'Vaqt', 'c': False}]},
        {'t': 'Ish formulasi?', 'a': [{'t': 'A = F·s·cosα', 'c': True}, {'t': 'A = F/s', 'c': False}, {'t': 'A = m·v', 'c': False}, {'t': 'A = P·t', 'c': False}]},
        {'t': 'Ish birligi (SI)?', 'a': [{'t': 'Joul (J)', 'c': True}, {'t': 'Vatt', 'c': False}, {'t': 'Nyuton', 'c': False}, {'t': 'Kilogramm', 'c': False}]},
        {'t': '1 Joul nima?', 'a': [{'t': '1 N kuch 1 m masofaga ko\'chirganda bajarilgan ish', 'c': True}, {'t': '1 kg massa', 'c': False}, {'t': '1 Vatt quvvat', 'c': False}, {'t': '1 m/s tezlik', 'c': False}]},
        {'t': 'Quvvat nima?', 'a': [{'t': 'Vaqt birligi ichida bajarilgan ish', 'c': True}, {'t': 'Faqat ish', 'c': False}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Kuch', 'c': False}]},
        {'t': 'Quvvat formulasi?', 'a': [{'t': 'P = A/t', 'c': True}, {'t': 'P = F·s', 'c': False}, {'t': 'P = m·v', 'c': False}, {'t': 'P = F/t', 'c': False}]},
        {'t': 'Quvvat birligi (SI)?', 'a': [{'t': 'Vatt (W)', 'c': True}, {'t': 'Joul', 'c': False}, {'t': 'Nyuton', 'c': False}, {'t': 'Kilogramm', 'c': False}]},
        {'t': '1 Vatt nima?', 'a': [{'t': '1 sekund ichida 1 Joul ish bajarish', 'c': True}, {'t': '1 Joul energiya', 'c': False}, {'t': '1 N kuch', 'c': False}, {'t': '1 kg massa', 'c': False}]},
    ]},

    {'n': 'Energiya va uning turlari', 't': 30, 'o': 11, 'q': [
        {'t': 'Energiya nima?', 'a': [{'t': 'Jismning ish bajarish qobiliyati', 'c': True}, {'t': 'Faqat harakat', 'c': False}, {'t': 'Faqat kuch', 'c': False}, {'t': 'Massa', 'c': False}]},
        {'t': 'Kinetik energiya nima?', 'a': [{'t': 'Harakat energiyasi', 'c': True}, {'t': 'Potensial energiya', 'c': False}, {'t': 'Issiqlik energiyasi', 'c': False}, {'t': 'Yorug\'lik energiyasi', 'c': False}]},
        {'t': 'Kinetik energiya formulasi?', 'a': [{'t': 'Ek = mv²/2', 'c': True}, {'t': 'Ek = mgh', 'c': False}, {'t': 'Ek = F·s', 'c': False}, {'t': 'Ek = P·t', 'c': False}]},
        {'t': 'Potensial energiya nima?', 'a': [{'t': 'Jismning holatiga bog\'liq energiya', 'c': True}, {'t': 'Harakat energiyasi', 'c': False}, {'t': 'Issiqlik energiyasi', 'c': False}, {'t': 'Elektr energiyasi', 'c': False}]},
        {'t': 'Gravitatsion potensial energiya formulasi?', 'a': [{'t': 'Ep = mgh', 'c': True}, {'t': 'Ep = mv²/2', 'c': False}, {'t': 'Ep = F·s', 'c': False}, {'t': 'Ep = kx²/2', 'c': False}]},
        {'t': 'Mexanik energiya nima?', 'a': [{'t': 'Kinetik va potensial energiyalar yig\'indisi', 'c': True}, {'t': 'Faqat kinetik energiya', 'c': False}, {'t': 'Faqat potensial energiya', 'c': False}, {'t': 'Issiqlik energiyasi', 'c': False}]},
        {'t': 'Energiya birligi?', 'a': [{'t': 'Joul (J)', 'c': True}, {'t': 'Vatt', 'c': False}, {'t': 'Nyuton', 'c': False}, {'t': 'Kilogramm', 'c': False}]},
    ]},

    {'n': 'Energiyaning saqlanish qonuni', 't': 30, 'o': 12, 'q': [
        {'t': 'Energiyaning saqlanish qonuni nima?', 'a': [{'t': 'Energiya yo\'qolmaydi va yaratilmaydi, faqat bir turdan ikkinchisiga o\'tadi', 'c': True}, {'t': 'Energiya doim ortadi', 'c': False}, {'t': 'Energiya doim kamayadi', 'c': False}, {'t': 'Energiya o\'zgarmaydi', 'c': False}]},
        {'t': 'Yopiq sistemada mexanik energiya qanday?', 'a': [{'t': 'O\'zgarmas (ishqalanish bo\'lmasa)', 'c': True}, {'t': 'Doim ortadi', 'c': False}, {'t': 'Doim kamayadi', 'c': False}, {'t': 'Nolga teng', 'c': False}]},
        {'t': 'Tosh yuqoriga otilsa, energiya qanday o\'zgaradi?', 'a': [{'t': 'Kinetik kamayadi, potensial ortadi', 'c': True}, {'t': 'Ikkalasi ham ortadi', 'c': False}, {'t': 'Ikkalasi ham kamayadi', 'c': False}, {'t': 'O\'zgarmaydi', 'c': False}]},
        {'t': 'Tosh pastga tushsa, energiya qanday o\'zgaradi?', 'a': [{'t': 'Potensial kamayadi, kinetik ortadi', 'c': True}, {'t': 'Ikkalasi ham ortadi', 'c': False}, {'t': 'Ikkalasi ham kamayadi', 'c': False}, {'t': 'O\'zgarmaydi', 'c': False}]},
        {'t': 'Ishqalanish bo\'lsa energiya qayerga ketadi?', 'a': [{'t': 'Issiqlik energiyasiga aylanadi', 'c': True}, {'t': 'Yo\'qoladi', 'c': False}, {'t': 'Ortadi', 'c': False}, {'t': 'O\'zgarmaydi', 'c': False}]},
        {'t': 'Abadiy harakat dvigateli mumkinmi?', 'a': [{'t': 'Yo\'q, energiya saqlanish qonuniga zid', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Faqat kosmosda', 'c': False}, {'t': 'Faqat suvda', 'c': False}]},
    ]},

    {'n': 'Impuls va impulsning saqlanishi', 't': 30, 'o': 13, 'q': [
        {'t': 'Impuls nima?', 'a': [{'t': 'Massa va tezlik ko\'paytmasi', 'c': True}, {'t': 'Faqat massa', 'c': False}, {'t': 'Faqat tezlik', 'c': False}, {'t': 'Kuch', 'c': False}]},
        {'t': 'Impuls formulasi?', 'a': [{'t': 'p = mv', 'c': True}, {'t': 'p = ma', 'c': False}, {'t': 'p = F·t', 'c': False}, {'t': 'p = m/v', 'c': False}]},
        {'t': 'Impuls birligi?', 'a': [{'t': 'kg·m/s', 'c': True}, {'t': 'N', 'c': False}, {'t': 'J', 'c': False}, {'t': 'W', 'c': False}]},
        {'t': 'Impuls vektor kattalikmi?', 'a': [{'t': 'Ha, yo\'nalishi bor', 'c': True}, {'t': 'Yo\'q, skalyar', 'c': False}, {'t': 'Ba\'zan vektor', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Impulsning saqlanish qonuni nima?', 'a': [{'t': 'Yopiq sistemada umumiy impuls o\'zgarmas', 'c': True}, {'t': 'Impuls doim ortadi', 'c': False}, {'t': 'Impuls doim kamayadi', 'c': False}, {'t': 'Impuls nolga teng', 'c': False}]},
        {'t': 'Ikki shar to\'qnashsa, umumiy impuls qanday?', 'a': [{'t': 'O\'zgarmaydi (yopiq sistemada)', 'c': True}, {'t': 'Ikki barobar ortadi', 'c': False}, {'t': 'Nolga teng bo\'ladi', 'c': False}, {'t': 'Kamayadi', 'c': False}]},
        {'t': 'Kuch impulsi nima?', 'a': [{'t': 'F·Δt - kuch va vaqt ko\'paytmasi', 'c': True}, {'t': 'Faqat kuch', 'c': False}, {'t': 'Faqat vaqt', 'c': False}, {'t': 'Massa', 'c': False}]},
    ]},

    {'n': 'Aylanma harakat', 't': 30, 'o': 14, 'q': [
        {'t': 'Aylanma harakat nima?', 'a': [{'t': 'Jism aylana bo\'ylab harakati', 'c': True}, {'t': 'To\'g\'ri chiziqli harakat', 'c': False}, {'t': 'Tinch holat', 'c': False}, {'t': 'Tebranma harakat', 'c': False}]},
        {'t': 'Chiziqli tezlik va burchak tezligi bog\'lanishi?', 'a': [{'t': 'v = ωr', 'c': True}, {'t': 'v = ω/r', 'c': False}, {'t': 'v = r/ω', 'c': False}, {'t': 'v = ω + r', 'c': False}]},
        {'t': 'Burchak tezligi birligi?', 'a': [{'t': 'rad/s (radian/sekund)', 'c': True}, {'t': 'm/s', 'c': False}, {'t': 'grad/s', 'c': False}, {'t': 'Hz', 'c': False}]},
        {'t': 'Davr nima?', 'a': [{'t': 'Bir marta to\'liq aylanish vaqti', 'c': True}, {'t': 'Tezlik', 'c': False}, {'t': 'Radius', 'c': False}, {'t': 'Kuch', 'c': False}]},
        {'t': 'Chastota nima?', 'a': [{'t': 'Vaqt birligi ichida aylanishlar soni', 'c': True}, {'t': 'Davr', 'c': False}, {'t': 'Tezlik', 'c': False}, {'t': 'Radius', 'c': False}]},
        {'t': 'Davr va chastota bog\'lanishi?', 'a': [{'t': 'T = 1/f', 'c': True}, {'t': 'T = f', 'c': False}, {'t': 'T = 2πf', 'c': False}, {'t': 'T = f²', 'c': False}]},
        {'t': 'Markazga intilma tezlanish formulasi?', 'a': [{'t': 'a = v²/r', 'c': True}, {'t': 'a = vr', 'c': False}, {'t': 'a = v/r', 'c': False}, {'t': 'a = r/v', 'c': False}]},
        {'t': 'Markazga intilma kuch formulasi?', 'a': [{'t': 'F = mv²/r', 'c': True}, {'t': 'F = mvr', 'c': False}, {'t': 'F = m/vr', 'c': False}, {'t': 'F = v/mr', 'c': False}]},
    ]},

    {'n': 'Tebranma harakat', 't': 30, 'o': 15, 'q': [
        {'t': 'Tebranma harakat nima?', 'a': [{'t': 'Muvozanat holati atrofida takrorlanuvchi harakat', 'c': True}, {'t': 'To\'g\'ri chiziqli harakat', 'c': False}, {'t': 'Aylanma harakat', 'c': False}, {'t': 'Tinch holat', 'c': False}]},
        {'t': 'Amplituda nima?', 'a': [{'t': 'Muvozanat holatidan maksimal chetlanish', 'c': True}, {'t': 'Tebranishlar soni', 'c': False}, {'t': 'Tebranish vaqti', 'c': False}, {'t': 'Tezlik', 'c': False}]},
        {'t': 'Tebranish davri nima?', 'a': [{'t': 'Bir to\'liq tebranish vaqti', 'c': True}, {'t': 'Amplituda', 'c': False}, {'t': 'Chastota', 'c': False}, {'t': 'Tezlik', 'c': False}]},
        {'t': 'Tebranish chastotasi nima?', 'a': [{'t': 'Vaqt birligi ichida tebranishlar soni', 'c': True}, {'t': 'Davr', 'c': False}, {'t': 'Amplituda', 'c': False}, {'t': 'Tezlik', 'c': False}]},
        {'t': 'Garmonik tebranish nima?', 'a': [{'t': 'Sinus yoki kosinus qonuni bo\'yicha tebranish', 'c': True}, {'t': 'Tartibsiz tebranish', 'c': False}, {'t': 'To\'g\'ri chiziqli harakat', 'c': False}, {'t': 'Aylanma harakat', 'c': False}]},
        {'t': 'Matematik mayatnik davri formulasi?', 'a': [{'t': 'T = 2π√(l/g)', 'c': True}, {'t': 'T = 2πl/g', 'c': False}, {'t': 'T = √(l/g)', 'c': False}, {'t': 'T = l/g', 'c': False}]},
        {'t': 'Prujinali mayatnik davri formulasi?', 'a': [{'t': 'T = 2π√(m/k)', 'c': True}, {'t': 'T = 2πm/k', 'c': False}, {'t': 'T = √(m/k)', 'c': False}, {'t': 'T = m/k', 'c': False}]},
    ]},

    {'n': 'To\'lqinlar', 't': 30, 'o': 16, 'q': [
        {'t': 'To\'lqin nima?', 'a': [{'t': 'Tebranishlarning muhitda tarqalishi', 'c': True}, {'t': 'Faqat tebranish', 'c': False}, {'t': 'Faqat harakat', 'c': False}, {'t': 'Tinch holat', 'c': False}]},
        {'t': 'Ko\'ndalang to\'lqin nima?', 'a': [{'t': 'Zarralar tarqalish yo\'nalishiga perpendikulyar tebranadi', 'c': True}, {'t': 'Zarralar tarqalish yo\'nalishida tebranadi', 'c': False}, {'t': 'Zarralar harakatlanmaydi', 'c': False}, {'t': 'Faqat suyuqlikda', 'c': False}]},
        {'t': 'Bo\'ylama to\'lqin nima?', 'a': [{'t': 'Zarralar tarqalish yo\'nalishida tebranadi', 'c': True}, {'t': 'Zarralar perpendikulyar tebranadi', 'c': False}, {'t': 'Zarralar harakatlanmaydi', 'c': False}, {'t': 'Faqat qattiq jismda', 'c': False}]},
        {'t': 'To\'lqin uzunligi nima?', 'a': [{'t': 'Ikki qo\'shni cho\'qqi orasidagi masofa', 'c': True}, {'t': 'Amplituda', 'c': False}, {'t': 'Davr', 'c': False}, {'t': 'Chastota', 'c': False}]},
        {'t': 'To\'lqin tezligi formulasi?', 'a': [{'t': 'v = λf (lambda × chastota)', 'c': True}, {'t': 'v = λ/f', 'c': False}, {'t': 'v = f/λ', 'c': False}, {'t': 'v = λ + f', 'c': False}]},
        {'t': 'Tovush to\'lqini qanday to\'lqin?', 'a': [{'t': 'Bo\'ylama to\'lqin', 'c': True}, {'t': 'Ko\'ndalang to\'lqin', 'c': False}, {'t': 'Elektromagnit to\'lqin', 'c': False}, {'t': 'To\'lqin emas', 'c': False}]},
        {'t': 'Yorug\'lik to\'lqini qanday to\'lqin?', 'a': [{'t': 'Ko\'ndalang elektromagnit to\'lqin', 'c': True}, {'t': 'Bo\'ylama to\'lqin', 'c': False}, {'t': 'Mexanik to\'lqin', 'c': False}, {'t': 'To\'lqin emas', 'c': False}]},
    ]},

    {'n': 'Tovush', 't': 25, 'o': 17, 'q': [
        {'t': 'Tovush nima?', 'a': [{'t': 'Muhitda tarqaluvchi mexanik to\'lqin', 'c': True}, {'t': 'Elektromagnit to\'lqin', 'c': False}, {'t': 'Yorug\'lik', 'c': False}, {'t': 'Issiqlik', 'c': False}]},
        {'t': 'Tovush vakuumda tarqaladimi?', 'a': [{'t': 'Yo\'q, muhit kerak', 'c': True}, {'t': 'Ha, tarqaladi', 'c': False}, {'t': 'Faqat kosmosda', 'c': False}, {'t': 'Ba\'zan tarqaladi', 'c': False}]},
        {'t': 'Havoda tovush tezligi taxminan necha?', 'a': [{'t': '≈340 m/s', 'c': True}, {'t': '300 000 km/s', 'c': False}, {'t': '1000 m/s', 'c': False}, {'t': '100 m/s', 'c': False}]},
        {'t': 'Tovush chastotasi nimani belgilaydi?', 'a': [{'t': 'Balandlikni (past yoki yuqori tovush)', 'c': True}, {'t': 'Kuchlilikni', 'c': False}, {'t': 'Tezlikni', 'c': False}, {'t': 'Rangni', 'c': False}]},
        {'t': 'Inson eshitadigan chastota diapazoni?', 'a': [{'t': '20 Hz dan 20 000 Hz gacha', 'c': True}, {'t': '1 Hz dan 100 Hz gacha', 'c': False}, {'t': '100 000 Hz dan yuqori', 'c': False}, {'t': 'Barcha chastotalar', 'c': False}]},
        {'t': 'Ultratovush nima?', 'a': [{'t': '20 000 Hz dan yuqori chastotali tovush', 'c': True}, {'t': '20 Hz dan past', 'c': False}, {'t': 'Oddiy tovush', 'c': False}, {'t': 'Yorug\'lik', 'c': False}]},
    ]},

    {'n': 'Issiqlik va harorat', 't': 30, 'o': 18, 'q': [
        {'t': 'Harorat nima?', 'a': [{'t': 'Jism molekulalarining o\'rtacha kinetik energiyasi', 'c': True}, {'t': 'Issiqlik miqdori', 'c': False}, {'t': 'Massa', 'c': False}, {'t': 'Hajm', 'c': False}]},
        {'t': 'Issiqlik nima?', 'a': [{'t': 'Jismlar orasida o\'tadigan energiya', 'c': True}, {'t': 'Harorat', 'c': False}, {'t': 'Massa', 'c': False}, {'t': 'Tezlik', 'c': False}]},
        {'t': 'Harorat va issiqlik bir xilmi?', 'a': [{'t': 'Yo\'q, harorat - holat, issiqlik - energiya', 'c': True}, {'t': 'Ha, bir xil', 'c': False}, {'t': 'Faqat Selsiyda bir xil', 'c': False}, {'t': 'Faqat Kelvinda bir xil', 'c': False}]},
        {'t': 'Absolut nol harorat necha Kelvin?', 'a': [{'t': '0 K', 'c': True}, {'t': '273 K', 'c': False}, {'t': '-273 K', 'c': False}, {'t': '100 K', 'c': False}]},
        {'t': 'Absolut nol harorat necha Selsiy?', 'a': [{'t': '-273.15°C', 'c': True}, {'t': '0°C', 'c': False}, {'t': '273°C', 'c': False}, {'t': '-100°C', 'c': False}]},
        {'t': 'Kelvin va Selsiy bog\'lanishi?', 'a': [{'t': 'T(K) = t(°C) + 273.15', 'c': True}, {'t': 'T(K) = t(°C) - 273', 'c': False}, {'t': 'T(K) = t(°C)', 'c': False}, {'t': 'T(K) = t(°C) × 273', 'c': False}]},
        {'t': 'Issiqlik sig\'imi nima?', 'a': [{'t': 'Jismni 1 K ga isitish uchun kerak bo\'lgan issiqlik', 'c': True}, {'t': 'Jism massasi', 'c': False}, {'t': 'Jism hajmi', 'c': False}, {'t': 'Jism harorati', 'c': False}]},
    ]},

    {'n': 'Termodinamikaning birinchi qonuni', 't': 30, 'o': 19, 'q': [
        {'t': 'Termodinamikaning birinchi qonuni nima?', 'a': [{'t': 'Energiyaning saqlanish qonuni issiqlik jarayonlari uchun', 'c': True}, {'t': 'Entropiya ortadi', 'c': False}, {'t': 'Absolut nolga yetib bo\'lmaydi', 'c': False}, {'t': 'F = ma', 'c': False}]},
        {'t': 'Birinchi qonun formulasi?', 'a': [{'t': 'ΔU = Q - A', 'c': True}, {'t': 'ΔU = Q + A', 'c': False}, {'t': 'ΔU = Q/A', 'c': False}, {'t': 'ΔU = QA', 'c': False}]},
        {'t': 'ΔU nima?', 'a': [{'t': 'Ichki energiya o\'zgarishi', 'c': True}, {'t': 'Issiqlik miqdori', 'c': False}, {'t': 'Bajarilgan ish', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'Q nima (birinchi qonunda)?', 'a': [{'t': 'Sistemaga berilgan issiqlik', 'c': True}, {'t': 'Bajarilgan ish', 'c': False}, {'t': 'Ichki energiya', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'A nima (birinchi qonunda)?', 'a': [{'t': 'Sistema tomonidan bajarilgan ish', 'c': True}, {'t': 'Issiqlik miqdori', 'c': False}, {'t': 'Ichki energiya', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'Izojarayon nima?', 'a': [{'t': 'Biror parametr o\'zgarmas bo\'lgan jarayon', 'c': True}, {'t': 'Barcha parametrlar o\'zgaradi', 'c': False}, {'t': 'Faqat harorat o\'zgaradi', 'c': False}, {'t': 'Faqat bosim o\'zgaradi', 'c': False}]},
    ]},

    {'n': 'Ideal gaz qonuni', 't': 30, 'o': 20, 'q': [
        {'t': 'Ideal gaz nima?', 'a': [{'t': 'Molekulalar orasida ta\'sir yo\'q deb hisoblangan gaz', 'c': True}, {'t': 'Haqiqiy gaz', 'c': False}, {'t': 'Suyuqlik', 'c': False}, {'t': 'Qattiq jism', 'c': False}]},
        {'t': 'Ideal gaz qonuni (Klapeyron-Mendeleev)?', 'a': [{'t': 'PV = nRT', 'c': True}, {'t': 'PV = T', 'c': False}, {'t': 'P = nRT', 'c': False}, {'t': 'V = nRT', 'c': False}]},
        {'t': 'P nima (gaz qonunida)?', 'a': [{'t': 'Bosim', 'c': True}, {'t': 'Quvvat', 'c': False}, {'t': 'Hajm', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'V nima (gaz qonunida)?', 'a': [{'t': 'Hajm', 'c': True}, {'t': 'Tezlik', 'c': False}, {'t': 'Volt', 'c': False}, {'t': 'Vatt', 'c': False}]},
        {'t': 'n nima (gaz qonunida)?', 'a': [{'t': 'Modda miqdori (mol)', 'c': True}, {'t': 'Molekulalar soni', 'c': False}, {'t': 'Massa', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'R nima (gaz qonunida)?', 'a': [{'t': 'Universal gaz doimiysi (8.31 J/(mol·K))', 'c': True}, {'t': 'Radius', 'c': False}, {'t': 'Qarshilik', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'Boyl-Mariott qonuni (T=const)?', 'a': [{'t': 'PV = const', 'c': True}, {'t': 'P/V = const', 'c': False}, {'t': 'P + V = const', 'c': False}, {'t': 'P - V = const', 'c': False}]},
        {'t': 'Sharl qonuni (P=const)?', 'a': [{'t': 'V/T = const', 'c': True}, {'t': 'VT = const', 'c': False}, {'t': 'V + T = const', 'c': False}, {'t': 'V - T = const', 'c': False}]},
    ]},

    {'n': 'Elektr zaryadi va Kulon qonuni', 't': 30, 'o': 21, 'q': [
        {'t': 'Elektr zaryadi nima?', 'a': [{'t': 'Moddaning elektr xossasini belgilovchi fizik kattalik', 'c': True}, {'t': 'Massa', 'c': False}, {'t': 'Tezlik', 'c': False}, {'t': 'Harorat', 'c': False}]},
        {'t': 'Zaryadning ikki turi qanday?', 'a': [{'t': 'Musbat va manfiy', 'c': True}, {'t': 'Katta va kichik', 'c': False}, {'t': 'Qizil va ko\'k', 'c': False}, {'t': 'Yuqori va past', 'c': False}]},
        {'t': 'Zaryadning saqlanish qonuni nima?', 'a': [{'t': 'Yopiq sistemada umumiy zaryad o\'zgarmas', 'c': True}, {'t': 'Zaryad doim ortadi', 'c': False}, {'t': 'Zaryad doim kamayadi', 'c': False}, {'t': 'Zaryad yo\'qoladi', 'c': False}]},
        {'t': 'Elementar zaryad nima?', 'a': [{'t': 'Elektronning zaryadi: e = 1.6×10⁻¹⁹ C', 'c': True}, {'t': 'Protonning massasi', 'c': False}, {'t': 'Fotonning energiyasi', 'c': False}, {'t': 'Neytronning zaryadi', 'c': False}]},
        {'t': 'Kulon qonuni formulasi?', 'a': [{'t': 'F = k(q₁q₂)/r²', 'c': True}, {'t': 'F = q₁q₂/r', 'c': False}, {'t': 'F = k(q₁ + q₂)/r²', 'c': False}, {'t': 'F = q₁q₂r²', 'c': False}]},
        {'t': 'k nima (Kulon qonunida)?', 'a': [{'t': 'Kulon doimiysi: 9×10⁹ N·m²/C²', 'c': True}, {'t': 'Zaryad', 'c': False}, {'t': 'Masofa', 'c': False}, {'t': 'Kuch', 'c': False}]},
        {'t': 'Bir xil zaryadlar qanday ta\'sir qiladi?', 'a': [{'t': 'Itarishadi', 'c': True}, {'t': 'Tortishadi', 'c': False}, {'t': 'Ta\'sir qilmaydi', 'c': False}, {'t': 'Yo\'q qiladi', 'c': False}]},
        {'t': 'Turli zaryadlar qanday ta\'sir qiladi?', 'a': [{'t': 'Tortishadi', 'c': True}, {'t': 'Itarishadi', 'c': False}, {'t': 'Ta\'sir qilmaydi', 'c': False}, {'t': 'Yo\'q qiladi', 'c': False}]},
    ]},

    {'n': 'Elektr maydoni', 't': 30, 'o': 22, 'q': [
        {'t': 'Elektr maydoni nima?', 'a': [{'t': 'Zaryadlangan jism atrofidagi maxsus materiya', 'c': True}, {'t': 'Magnit maydoni', 'c': False}, {'t': 'Gravitatsiya maydoni', 'c': False}, {'t': 'Havo', 'c': False}]},
        {'t': 'Elektr maydon kuchlanganligi nima?', 'a': [{'t': 'Birlik zaryadga ta\'sir qiluvchi kuch', 'c': True}, {'t': 'Zaryad miqdori', 'c': False}, {'t': 'Potensial', 'c': False}, {'t': 'Tok kuchi', 'c': False}]},
        {'t': 'Maydon kuchlanganligi formulasi?', 'a': [{'t': 'E = F/q', 'c': True}, {'t': 'E = Fq', 'c': False}, {'t': 'E = q/F', 'c': False}, {'t': 'E = F - q', 'c': False}]},
        {'t': 'Maydon kuchlanganligi birligi?', 'a': [{'t': 'V/m yoki N/C', 'c': True}, {'t': 'Volt', 'c': False}, {'t': 'Amper', 'c': False}, {'t': 'Om', 'c': False}]},
        {'t': 'Nuqtaviy zaryad maydoni formulasi?', 'a': [{'t': 'E = kq/r²', 'c': True}, {'t': 'E = kqr²', 'c': False}, {'t': 'E = q/r', 'c': False}, {'t': 'E = kr/q', 'c': False}]},
        {'t': 'Elektr maydon chiziqlari nima?', 'a': [{'t': 'Maydon yo\'nalishini ko\'rsatuvchi chiziqlar', 'c': True}, {'t': 'Tok yo\'li', 'c': False}, {'t': 'Magnit chiziqlari', 'c': False}, {'t': 'Haqiqiy chiziqlar', 'c': False}]},
        {'t': 'Musbat zaryaddan maydon chiziqlari qayerga yo\'nalgan?', 'a': [{'t': 'Tashqariga (zaryaddan uzoqqa)', 'c': True}, {'t': 'Ichkariga (zaryadga)', 'c': False}, {'t': 'Aylana bo\'ylab', 'c': False}, {'t': 'Yo\'nalishi yo\'q', 'c': False}]},
    ]},

    {'n': 'Elektr potensiali va kuchlanish', 't': 30, 'o': 23, 'q': [
        {'t': 'Elektr potensiali nima?', 'a': [{'t': 'Birlik zaryadning potensial energiyasi', 'c': True}, {'t': 'Tok kuchi', 'c': False}, {'t': 'Qarshilik', 'c': False}, {'t': 'Quvvat', 'c': False}]},
        {'t': 'Potensial formulasi?', 'a': [{'t': 'φ = W/q', 'c': True}, {'t': 'φ = Wq', 'c': False}, {'t': 'φ = q/W', 'c': False}, {'t': 'φ = W - q', 'c': False}]},
        {'t': 'Potensial birligi?', 'a': [{'t': 'Volt (V)', 'c': True}, {'t': 'Amper', 'c': False}, {'t': 'Om', 'c': False}, {'t': 'Vatt', 'c': False}]},
        {'t': 'Kuchlanish nima?', 'a': [{'t': 'Ikki nuqta orasidagi potensiallar farqi', 'c': True}, {'t': 'Tok kuchi', 'c': False}, {'t': 'Qarshilik', 'c': False}, {'t': 'Quvvat', 'c': False}]},
        {'t': 'Kuchlanish formulasi?', 'a': [{'t': 'U = φ₁ - φ₂', 'c': True}, {'t': 'U = φ₁ + φ₂', 'c': False}, {'t': 'U = φ₁φ₂', 'c': False}, {'t': 'U = φ₁/φ₂', 'c': False}]},
        {'t': 'Kuchlanish va potensial bir xilmi?', 'a': [{'t': 'Yo\'q, kuchlanish - farq, potensial - nuqtadagi qiymat', 'c': True}, {'t': 'Ha, bir xil', 'c': False}, {'t': 'Faqat DC da bir xil', 'c': False}, {'t': 'Faqat AC da bir xil', 'c': False}]},
    ]},

    {'n': 'Elektr toki va Om qonuni', 't': 30, 'o': 24, 'q': [
        {'t': 'Elektr toki nima?', 'a': [{'t': 'Zaryadlarning tartibli harakati', 'c': True}, {'t': 'Zaryadlar soni', 'c': False}, {'t': 'Kuchlanish', 'c': False}, {'t': 'Qarshilik', 'c': False}]},
        {'t': 'Tok kuchi nima?', 'a': [{'t': 'Vaqt birligi ichida o\'tgan zaryad', 'c': True}, {'t': 'Kuchlanish', 'c': False}, {'t': 'Qarshilik', 'c': False}, {'t': 'Quvvat', 'c': False}]},
        {'t': 'Tok kuchi formulasi?', 'a': [{'t': 'I = q/t', 'c': True}, {'t': 'I = qt', 'c': False}, {'t': 'I = t/q', 'c': False}, {'t': 'I = q - t', 'c': False}]},
        {'t': 'Tok kuchi birligi?', 'a': [{'t': 'Amper (A)', 'c': True}, {'t': 'Volt', 'c': False}, {'t': 'Om', 'c': False}, {'t': 'Vatt', 'c': False}]},
        {'t': 'Om qonuni formulasi?', 'a': [{'t': 'I = U/R', 'c': True}, {'t': 'I = UR', 'c': False}, {'t': 'I = R/U', 'c': False}, {'t': 'I = U + R', 'c': False}]},
        {'t': 'Qarshilik nima?', 'a': [{'t': 'O\'tkazgichning tok o\'tishiga qarshiligi', 'c': True}, {'t': 'Tok kuchi', 'c': False}, {'t': 'Kuchlanish', 'c': False}, {'t': 'Quvvat', 'c': False}]},
        {'t': 'Qarshilik birligi?', 'a': [{'t': 'Om (Ω)', 'c': True}, {'t': 'Amper', 'c': False}, {'t': 'Volt', 'c': False}, {'t': 'Vatt', 'c': False}]},
        {'t': 'Qarshilik ortsa tok kuchi qanday o\'zgaradi?', 'a': [{'t': 'Kamayadi', 'c': True}, {'t': 'Ortadi', 'c': False}, {'t': 'O\'zgarmaydi', 'c': False}, {'t': 'Nolga teng bo\'ladi', 'c': False}]},
    ]},

    {'n': 'Elektr quvvati va Joul-Lens qonuni', 't': 30, 'o': 25, 'q': [
        {'t': 'Elektr quvvati nima?', 'a': [{'t': 'Vaqt birligi ichida bajarilgan elektr ishi', 'c': True}, {'t': 'Tok kuchi', 'c': False}, {'t': 'Kuchlanish', 'c': False}, {'t': 'Qarshilik', 'c': False}]},
        {'t': 'Elektr quvvati formulasi?', 'a': [{'t': 'P = UI', 'c': True}, {'t': 'P = U/I', 'c': False}, {'t': 'P = U + I', 'c': False}, {'t': 'P = U - I', 'c': False}]},
        {'t': 'Quvvat birligi?', 'a': [{'t': 'Vatt (W)', 'c': True}, {'t': 'Joul', 'c': False}, {'t': 'Volt', 'c': False}, {'t': 'Amper', 'c': False}]},
        {'t': 'Joul-Lens qonuni nima?', 'a': [{'t': 'Tokli o\'tkazgichda ajralib chiqadigan issiqlik qonuni', 'c': True}, {'t': 'Om qonuni', 'c': False}, {'t': 'Kulon qonuni', 'c': False}, {'t': 'Nyuton qonuni', 'c': False}]},
        {'t': 'Joul-Lens qonuni formulasi?', 'a': [{'t': 'Q = I²Rt', 'c': True}, {'t': 'Q = IRt', 'c': False}, {'t': 'Q = I/Rt', 'c': False}, {'t': 'Q = I + Rt', 'c': False}]},
        {'t': 'Elektr ishi formulasi?', 'a': [{'t': 'A = UIt', 'c': True}, {'t': 'A = UI/t', 'c': False}, {'t': 'A = U + It', 'c': False}, {'t': 'A = U - It', 'c': False}]},
        {'t': 'Elektr ishi birligi?', 'a': [{'t': 'Joul (J)', 'c': True}, {'t': 'Vatt', 'c': False}, {'t': 'Volt', 'c': False}, {'t': 'Amper', 'c': False}]},
    ]},

    {'n': 'Magnit maydoni', 't': 30, 'o': 26, 'q': [
        {'t': 'Magnit maydoni nima?', 'a': [{'t': 'Harakatlanuvchi zaryadlar va magnitlar atrofidagi maydon', 'c': True}, {'t': 'Elektr maydoni', 'c': False}, {'t': 'Gravitatsiya maydoni', 'c': False}, {'t': 'Issiqlik maydoni', 'c': False}]},
        {'t': 'Magnit induksiyasi nima?', 'a': [{'t': 'Magnit maydonning kuchliligi', 'c': True}, {'t': 'Tok kuchi', 'c': False}, {'t': 'Kuchlanish', 'c': False}, {'t': 'Qarshilik', 'c': False}]},
        {'t': 'Magnit induksiyasi birligi?', 'a': [{'t': 'Tesla (T)', 'c': True}, {'t': 'Veber', 'c': False}, {'t': 'Genri', 'c': False}, {'t': 'Volt', 'c': False}]},
        {'t': 'Amper kuchi nima?', 'a': [{'t': 'Magnit maydonning tokli o\'tkazgichga ta\'sir kuchi', 'c': True}, {'t': 'Elektr kuchi', 'c': False}, {'t': 'Gravitatsiya kuchi', 'c': False}, {'t': 'Ishqalanish kuchi', 'c': False}]},
        {'t': 'Amper kuchi formulasi?', 'a': [{'t': 'F = BILsinα', 'c': True}, {'t': 'F = BIL', 'c': False}, {'t': 'F = B/IL', 'c': False}, {'t': 'F = B + IL', 'c': False}]},
        {'t': 'Lorents kuchi nima?', 'a': [{'t': 'Magnit maydonning harakatlanuvchi zaryadga ta\'sir kuchi', 'c': True}, {'t': 'Elektr kuchi', 'c': False}, {'t': 'Gravitatsiya kuchi', 'c': False}, {'t': 'Ishqalanish kuchi', 'c': False}]},
        {'t': 'Lorents kuchi formulasi?', 'a': [{'t': 'F = qvBsinα', 'c': True}, {'t': 'F = qvB', 'c': False}, {'t': 'F = qv/B', 'c': False}, {'t': 'F = q + vB', 'c': False}]},
    ]},

    {'n': 'Elektromagnit induksiya', 't': 30, 'o': 27, 'q': [
        {'t': 'Elektromagnit induksiya nima?', 'a': [{'t': 'Magnit oqimi o\'zgarganda EYK hosil bo\'lishi', 'c': True}, {'t': 'Tok hosil bo\'lishi', 'c': False}, {'t': 'Magnit hosil bo\'lishi', 'c': False}, {'t': 'Issiqlik hosil bo\'lishi', 'c': False}]},
        {'t': 'Faradey qonuni formulasi?', 'a': [{'t': 'ε = -dΦ/dt', 'c': True}, {'t': 'ε = dΦ/dt', 'c': False}, {'t': 'ε = Φ/t', 'c': False}, {'t': 'ε = Φt', 'c': False}]},
        {'t': 'Magnit oqimi nima?', 'a': [{'t': 'Sirt orqali o\'tuvchi magnit induksiya chiziqlari soni', 'c': True}, {'t': 'Tok kuchi', 'c': False}, {'t': 'Kuchlanish', 'c': False}, {'t': 'Qarshilik', 'c': False}]},
        {'t': 'Magnit oqimi formulasi?', 'a': [{'t': 'Φ = BScosα', 'c': True}, {'t': 'Φ = BS', 'c': False}, {'t': 'Φ = B/S', 'c': False}, {'t': 'Φ = B + S', 'c': False}]},
        {'t': 'Magnit oqimi birligi?', 'a': [{'t': 'Veber (Wb)', 'c': True}, {'t': 'Tesla', 'c': False}, {'t': 'Genri', 'c': False}, {'t': 'Volt', 'c': False}]},
        {'t': 'Lens qoidasi nima?', 'a': [{'t': 'Induksiya toki o\'zgarishga qarshi yo\'nalgan', 'c': True}, {'t': 'Tok ortadi', 'c': False}, {'t': 'Tok kamayadi', 'c': False}, {'t': 'Tok o\'zgarmaydi', 'c': False}]},
        {'t': 'Generator qanday ishlaydi?', 'a': [{'t': 'Mexanik energiyani elektr energiyasiga aylantiradi (induksiya)', 'c': True}, {'t': 'Elektr energiyani mexanik energiyaga aylantiradi', 'c': False}, {'t': 'Issiqlik ishlab chiqaradi', 'c': False}, {'t': 'Yorug\'lik chiqaradi', 'c': False}]},
    ]},

    {'n': 'Yorug\'lik va optika', 't': 30, 'o': 28, 'q': [
        {'t': 'Yorug\'lik nima?', 'a': [{'t': 'Elektromagnit to\'lqin', 'c': True}, {'t': 'Mexanik to\'lqin', 'c': False}, {'t': 'Tovush to\'lqini', 'c': False}, {'t': 'Zarrachalar oqimi', 'c': False}]},
        {'t': 'Vakuumda yorug\'lik tezligi?', 'a': [{'t': 'c = 3×10⁸ m/s', 'c': True}, {'t': '340 m/s', 'c': False}, {'t': '1000 m/s', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'Yorug\'likning qaytish qonuni?', 'a': [{'t': 'Tushish burchagi = qaytish burchagi', 'c': True}, {'t': 'Tushish burchagi > qaytish burchagi', 'c': False}, {'t': 'Tushish burchagi < qaytish burchagi', 'c': False}, {'t': 'Bog\'liq emas', 'c': False}]},
        {'t': 'Yorug\'likning sinish qonuni?', 'a': [{'t': 'n₁sinα₁ = n₂sinα₂', 'c': True}, {'t': 'n₁α₁ = n₂α₂', 'c': False}, {'t': 'n₁/α₁ = n₂/α₂', 'c': False}, {'t': 'n₁ + α₁ = n₂ + α₂', 'c': False}]},
        {'t': 'Sindirish ko\'rsatkichi nima?', 'a': [{'t': 'Vakuumdagi tezlikning muhitdagi tezlikka nisbati', 'c': True}, {'t': 'Tezlik', 'c': False}, {'t': 'Burchak', 'c': False}, {'t': 'Masofa', 'c': False}]},
        {'t': 'Linza nima?', 'a': [{'t': 'Yorug\'likni sindiradigan shaffof jism', 'c': True}, {'t': 'Yorug\'likni qaytaradigan sirt', 'c': False}, {'t': 'Yorug\'lik manbai', 'c': False}, {'t': 'Yorug\'likni yutadigan jism', 'c': False}]},
        {'t': 'Yig\'uvchi linza nima?', 'a': [{'t': 'Nurlarni bir nuqtaga yig\'adigan linza', 'c': True}, {'t': 'Nurlarni tarqatadigan linza', 'c': False}, {'t': 'Tekis linza', 'c': False}, {'t': 'Yorug\'lik manbai', 'c': False}]},
    ]},

    {'n': 'Kvant fizikasi asoslari', 't': 35, 'o': 29, 'q': [
        {'t': 'Kvant fizikasi nima bilan shug\'ullanadi?', 'a': [{'t': 'Mikrodunyodagi zarralar va energiya', 'c': True}, {'t': 'Faqat makroskopik jismlar', 'c': False}, {'t': 'Faqat astronomiya', 'c': False}, {'t': 'Faqat kimyo', 'c': False}]},
        {'t': 'Foton nima?', 'a': [{'t': 'Yorug\'lik kvanti (zarrachasi)', 'c': True}, {'t': 'Elektron', 'c': False}, {'t': 'Proton', 'c': False}, {'t': 'Neytron', 'c': False}]},
        {'t': 'Foton energiyasi formulasi?', 'a': [{'t': 'E = hf (h - Plank doimiysi)', 'c': True}, {'t': 'E = mc²', 'c': False}, {'t': 'E = mv²/2', 'c': False}, {'t': 'E = mgh', 'c': False}]},
        {'t': 'Plank doimiysi nima?', 'a': [{'t': 'h = 6.63×10⁻³⁴ J·s', 'c': True}, {'t': 'c = 3×10⁸ m/s', 'c': False}, {'t': 'G = 6.67×10⁻¹¹', 'c': False}, {'t': 'e = 1.6×10⁻¹⁹ C', 'c': False}]},
        {'t': 'Fotoeffekt nima?', 'a': [{'t': 'Yorug\'lik ta\'sirida metaldan elektronlar chiqishi', 'c': True}, {'t': 'Elektr toki hosil bo\'lishi', 'c': False}, {'t': 'Magnit hosil bo\'lishi', 'c': False}, {'t': 'Issiqlik hosil bo\'lishi', 'c': False}]},
        {'t': 'De Broyl to\'lqini nima?', 'a': [{'t': 'Har bir zarrachaning to\'lqin xossasi bor', 'c': True}, {'t': 'Faqat fotonning to\'lqini', 'c': False}, {'t': 'Faqat elektronning to\'lqini', 'c': False}, {'t': 'To\'lqin yo\'q', 'c': False}]},
        {'t': 'Noaniqlik prinsipi kimga tegishli?', 'a': [{'t': 'Geyzenberg', 'c': True}, {'t': 'Nyuton', 'c': False}, {'t': 'Eynshteyn', 'c': False}, {'t': 'Plank', 'c': False}]},
    ]},

    {'n': 'Atom va yadro fizikasi', 't': 35, 'o': 30, 'q': [
        {'t': 'Atom tuzilishi qanday?', 'a': [{'t': 'Yadro (proton+neytron) va elektronlar', 'c': True}, {'t': 'Faqat elektronlar', 'c': False}, {'t': 'Faqat protonlar', 'c': False}, {'t': 'Bir butun shar', 'c': False}]},
        {'t': 'Proton zaryadi qanday?', 'a': [{'t': 'Musbat (+e)', 'c': True}, {'t': 'Manfiy (-e)', 'c': False}, {'t': 'Neytral (0)', 'c': False}, {'t': 'O\'zgaruvchan', 'c': False}]},
        {'t': 'Elektron zaryadi qanday?', 'a': [{'t': 'Manfiy (-e)', 'c': True}, {'t': 'Musbat (+e)', 'c': False}, {'t': 'Neytral (0)', 'c': False}, {'t': 'O\'zgaruvchan', 'c': False}]},
        {'t': 'Neytron zaryadi qanday?', 'a': [{'t': 'Neytral (0)', 'c': True}, {'t': 'Musbat (+e)', 'c': False}, {'t': 'Manfiy (-e)', 'c': False}, {'t': 'O\'zgaruvchan', 'c': False}]},
        {'t': 'Radioaktivlik nima?', 'a': [{'t': 'Yadro parchalanib zarrachalar va energiya chiqarishi', 'c': True}, {'t': 'Elektr toki', 'c': False}, {'t': 'Yorug\'lik', 'c': False}, {'t': 'Issiqlik', 'c': False}]},
        {'t': 'Alfa-zarracha nima?', 'a': [{'t': 'Geliy yadrosi (2 proton + 2 neytron)', 'c': True}, {'t': 'Elektron', 'c': False}, {'t': 'Foton', 'c': False}, {'t': 'Neytron', 'c': False}]},
        {'t': 'Beta-zarracha nima?', 'a': [{'t': 'Elektron yoki pozitron', 'c': True}, {'t': 'Proton', 'c': False}, {'t': 'Neytron', 'c': False}, {'t': 'Foton', 'c': False}]},
        {'t': 'Gamma-nurlanish nima?', 'a': [{'t': 'Yuqori energiyali elektromagnit to\'lqin', 'c': True}, {'t': 'Zarrachalar oqimi', 'c': False}, {'t': 'Tovush to\'lqini', 'c': False}, {'t': 'Mexanik to\'lqin', 'c': False}]},
        {'t': 'Eynshteynning massa-energiya formulasi?', 'a': [{'t': 'E = mc²', 'c': True}, {'t': 'E = mv²/2', 'c': False}, {'t': 'E = mgh', 'c': False}, {'t': 'E = hf', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_physics()
    add_topics(subj, T)
    print(f"\n✅ Nazariy Fizika: {len(T)} ta mavzu qo'shildi!")
