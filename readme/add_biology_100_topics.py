"""
BIOLOGIYA - 100 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_biology():
    cat, _ = SubjectCategory.objects.get_or_create(slug='tabiiy-fanlar', defaults={'name': 'Tabiiy fanlar', 'icon': 'bi-globe', 'order': 1, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Biologiya', defaults={'category': cat, 'description': 'Biologiya fani - tirik organizmlar haqida', 'icon': 'bi-flower1', 'order': 4, 'is_active': True})
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
    # BIOLOGIYA ASOSLARI (1-10)
    {'n': 'Biologiya faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Biologiya fani nimani o\'rganadi?', 'a': [{'t': 'Tirik organizmlarni', 'c': True}, {'t': 'Faqat moddalarni', 'c': False}, {'t': 'Faqat fizik hodisalarni', 'c': False}, {'t': 'Faqat kimyoviy reaksiyalarni', 'c': False}]},
        {'t': 'Tirik organizmlarning asosiy belgisi?', 'a': [{'t': 'Nafas olish, oziqlanish, ko\'payish', 'c': True}, {'t': 'Faqat harakat', 'c': False}, {'t': 'Faqat o\'sish', 'c': False}, {'t': 'Hech qanday belgi yo\'q', 'c': False}]},
        {'t': 'Hujayra nima?', 'a': [{'t': 'Tirik organizmning eng kichik birligi', 'c': True}, {'t': 'Katta organ', 'c': False}, {'t': 'To\'qima', 'c': False}, {'t': 'Organizm', 'c': False}]},
        {'t': 'Biologiya qaysi fanlarga bo\'linadi?', 'a': [{'t': 'Botanika, zoologiya, anatomiya', 'c': True}, {'t': 'Faqat botanika', 'c': False}, {'t': 'Faqat zoologiya', 'c': False}, {'t': 'Faqat anatomiya', 'c': False}]},
        {'t': 'Mikroskop nima uchun ishlatiladi?', 'a': [{'t': 'Kichik organizmlarni ko\'rish uchun', 'c': True}, {'t': 'Katta hayvonlarni ko\'rish uchun', 'c': False}, {'t': 'Faqat o\'simliklarni ko\'rish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},
    {'n': 'Hujayra tuzilishi', 't': 25, 'o': 2, 'q': [
        {'t': 'Hujayra qanday qismlardan iborat?', 'a': [{'t': 'Yadro, sitoplazma, membrana', 'c': True}, {'t': 'Faqat yadro', 'c': False}, {'t': 'Faqat membrana', 'c': False}, {'t': 'Faqat sitoplazma', 'c': False}]},
        {'t': 'Hujayra membranasi vazifasi?', 'a': [{'t': 'Hujayrani himoya qilish va moddalar almashinuvi', 'c': True}, {'t': 'Faqat himoya qilish', 'c': False}, {'t': 'Faqat oziqlanish', 'c': False}, {'t': 'Hech qanday vazifa yo\'q', 'c': False}]},
        {'t': 'Yadro vazifasi?', 'a': [{'t': 'Irsiy ma\'lumotni saqlash', 'c': True}, {'t': 'Oziqlanish', 'c': False}, {'t': 'Nafas olish', 'c': False}, {'t': 'Harakat', 'c': False}]},
        {'t': 'Sitoplazma nima?', 'a': [{'t': 'Hujayra ichidagi suyuqlik', 'c': True}, {'t': 'Hujayra membranasi', 'c': False}, {'t': 'Yadro', 'c': False}, {'t': 'Organoid', 'c': False}]},
        {'t': 'Mitoxondriya vazifasi?', 'a': [{'t': 'Energiya ishlab chiqarish', 'c': True}, {'t': 'Oqsil sintezi', 'c': False}, {'t': 'Fotosintez', 'c': False}, {'t': 'Himoya', 'c': False}]},
        {'t': 'Xloroplast qayerda bo\'ladi?', 'a': [{'t': 'O\'simlik hujayrasida', 'c': True}, {'t': 'Hayvon hujayrasida', 'c': False}, {'t': 'Bakteriya hujayrasida', 'c': False}, {'t': 'Zamburug\' hujayrasida', 'c': False}]},
    ]},
    {'n': 'O\'simlik va hayvon hujayralari', 't': 20, 'o': 3, 'q': [
        {'t': 'O\'simlik hujayrasining o\'ziga xos xususiyati?', 'a': [{'t': 'Hujayra devori va xloroplast bor', 'c': True}, {'t': 'Faqat yadro bor', 'c': False}, {'t': 'Faqat membrana bor', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
        {'t': 'Hayvon hujayrasida nima yo\'q?', 'a': [{'t': 'Hujayra devori va xloroplast', 'c': True}, {'t': 'Yadro', 'c': False}, {'t': 'Membrana', 'c': False}, {'t': 'Sitoplazma', 'c': False}]},
        {'t': 'Hujayra devori nimadan tashkil topgan?', 'a': [{'t': 'Tsellyulozadan', 'c': True}, {'t': 'Oqsildan', 'c': False}, {'t': 'Yog\'dan', 'c': False}, {'t': 'Suvdan', 'c': False}]},
        {'t': 'Xloroplast vazifasi?', 'a': [{'t': 'Fotosintez jarayonini amalga oshirish', 'c': True}, {'t': 'Nafas olish', 'c': False}, {'t': 'Energiya ishlab chiqarish', 'c': False}, {'t': 'Himoya', 'c': False}]},
        {'t': 'Vakuola nima?', 'a': [{'t': 'Hujayra ichidagi suyuqlik to\'ldirilgan bo\'shliq', 'c': True}, {'t': 'Yadro', 'c': False}, {'t': 'Membrana', 'c': False}, {'t': 'Organoid', 'c': False}]},
    ]},
    {'n': 'To\'qimalar', 't': 20, 'o': 4, 'q': [
        {'t': 'To\'qima nima?', 'a': [{'t': 'Bir xil vazifani bajaruvchi hujayra guruhi', 'c': True}, {'t': 'Bitta hujayra', 'c': False}, {'t': 'Organ', 'c': False}, {'t': 'Organizm', 'c': False}]},
        {'t': 'O\'simlik to\'qimalari qaysilar?', 'a': [{'t': 'Mex, o\'tkazuvchi, asosiy, himoya', 'c': True}, {'t': 'Faqat mex', 'c': False}, {'t': 'Faqat himoya', 'c': False}, {'t': 'Faqat asosiy', 'c': False}]},
        {'t': 'Hayvon to\'qimalari qaysilar?', 'a': [{'t': 'Epiteliy, biriktiruvchi, muskul, nerv', 'c': True}, {'t': 'Faqat epiteliy', 'c': False}, {'t': 'Faqat muskul', 'c': False}, {'t': 'Faqat nerv', 'c': False}]},
        {'t': 'Mex to\'qima vazifasi?', 'a': [{'t': 'O\'simlikning o\'sishini ta\'minlash', 'c': True}, {'t': 'Himoya qilish', 'c': False}, {'t': 'Oziqlanish', 'c': False}, {'t': 'Nafas olish', 'c': False}]},
        {'t': 'Epiteliy to\'qima qayerda joylashgan?', 'a': [{'t': 'Organlar yuzasida', 'c': True}, {'t': 'Suyak ichida', 'c': False}, {'t': 'Muskul ichida', 'c': False}, {'t': 'Nerv ichida', 'c': False}]},
    ]},
    {'n': 'Organlar va organ sistemalari', 't': 20, 'o': 5, 'q': [
        {'t': 'Organ nima?', 'a': [{'t': 'Bir necha to\'qimalardan tashkil topgan qism', 'c': True}, {'t': 'Bitta to\'qima', 'c': False}, {'t': 'Bitta hujayra', 'c': False}, {'t': 'Organizm', 'c': False}]},
        {'t': 'Organ sistemasi nima?', 'a': [{'t': 'Bir vazifani bajaruvchi organlar guruhi', 'c': True}, {'t': 'Bitta organ', 'c': False}, {'t': 'Bitta to\'qima', 'c': False}, {'t': 'Bitta hujayra', 'c': False}]},
        {'t': 'Inson organizmida nechta organ sistemasi bor?', 'a': [{'t': '10-12 ta', 'c': True}, {'t': '5 ta', 'c': False}, {'t': '20 ta', 'c': False}, {'t': '3 ta', 'c': False}]},
        {'t': 'Yurak qaysi sistemaga kiradi?', 'a': [{'t': 'Qon aylanish sistemasi', 'c': True}, {'t': 'Nafas olish sistemasi', 'c': False}, {'t': 'Hazm qilish sistemasi', 'c': False}, {'t': 'Nerv sistemasi', 'c': False}]},
        {'t': 'O\'pka qaysi sistemaga kiradi?', 'a': [{'t': 'Nafas olish sistemasi', 'c': True}, {'t': 'Qon aylanish sistemasi', 'c': False}, {'t': 'Hazm qilish sistemasi', 'c': False}, {'t': 'Nerv sistemasi', 'c': False}]},
    ]},
    {'n': 'Bakteriyalar', 't': 20, 'o': 6, 'q': [
        {'t': 'Bakteriyalar qanday organizmlar?', 'a': [{'t': 'Bir hujayrali prokariot organizmlar', 'c': True}, {'t': 'Ko\'p hujayrali organizmlar', 'c': False}, {'t': 'Eukariot organizmlar', 'c': False}, {'t': 'Viruslar', 'c': False}]},
        {'t': 'Bakteriyalarda yadro bormi?', 'a': [{'t': 'Yo\'q, yadro yo\'q', 'c': True}, {'t': 'Ha, yadro bor', 'c': False}, {'t': 'Ba\'zilarida bor', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Bakteriyalar qanday ko\'payadi?', 'a': [{'t': 'Bo\'linish yo\'li bilan', 'c': True}, {'t': 'Urug\' orqali', 'c': False}, {'t': 'Tuxum orqali', 'c': False}, {'t': 'Ko\'paymaydi', 'c': False}]},
        {'t': 'Foydali bakteriyalar qayerda ishlatiladi?', 'a': [{'t': 'Yogurt, pishloq tayyorlashda', 'c': True}, {'t': 'Faqat kasallik keltirishda', 'c': False}, {'t': 'Hech qayerda', 'c': False}, {'t': 'Faqat tuproqda', 'c': False}]},
        {'t': 'Zararli bakteriyalar nima qiladi?', 'a': [{'t': 'Kasallik keltirib chiqaradi', 'c': True}, {'t': 'Faqat foyda keltiradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Faqat oziqlanadi', 'c': False}]},
    ]},
    {'n': 'Zamburug\'lar', 't': 20, 'o': 7, 'q': [
        {'t': 'Zamburug\'lar qanday organizmlar?', 'a': [{'t': 'Alohida organizmlar guruhi', 'c': True}, {'t': 'O\'simliklar', 'c': False}, {'t': 'Hayvonlar', 'c': False}, {'t': 'Bakteriyalar', 'c': False}]},
        {'t': 'Zamburug\'larda xloroplast bormi?', 'a': [{'t': 'Yo\'q', 'c': True}, {'t': 'Ha', 'c': False}, {'t': 'Ba\'zilarida bor', 'c': False}, {'t': 'Noma\'lum', 'c': False}]},
        {'t': 'Zamburug\'lar qanday oziqlanadi?', 'a': [{'t': 'Tayyor organik moddalar bilan', 'c': True}, {'t': 'Fotosintez yo\'li bilan', 'c': False}, {'t': 'Faqat suv bilan', 'c': False}, {'t': 'Oziqlanmaydi', 'c': False}]},
        {'t': 'Qo\'ziqorin qanday zamburug\'?', 'a': [{'t': 'Yeydigan zamburug\'', 'c': True}, {'t': 'Zaharli zamburug\'', 'c': False}, {'t': 'Mog\'or zamburug\'i', 'c': False}, {'t': 'Achitqi zamburug\'i', 'c': False}]},
        {'t': 'Mog\'or zamburug\'i qayerda o\'sadi?', 'a': [{'t': 'Nam joylarda', 'c': True}, {'t': 'Quruq joylarda', 'c': False}, {'t': 'Faqat suvda', 'c': False}, {'t': 'Faqat havoda', 'c': False}]},
    ]},
    {'n': 'Suv o\'simliklari', 't': 20, 'o': 8, 'q': [
        {'t': 'Suv o\'simliklari qayerda yashaydi?', 'a': [{'t': 'Suvda', 'c': True}, {'t': 'Quruqlikda', 'c': False}, {'t': 'Havoda', 'c': False}, {'t': 'Tuproqda', 'c': False}]},
        {'t': 'Suv o\'simliklarining o\'ziga xos xususiyati?', 'a': [{'t': 'Suvda yashashga moslashgan', 'c': True}, {'t': 'Quruqlikda yashashga moslashgan', 'c': False}, {'t': 'Hech qanday xususiyat yo\'q', 'c': False}, {'t': 'Faqat ildizi bor', 'c': False}]},
        {'t': 'Suv o\'simliklariga misol?', 'a': [{'t': 'Nilufar, elodea', 'c': True}, {'t': 'Archa, qarag\'ay', 'c': False}, {'t': 'Pomidor, bodring', 'c': False}, {'t': 'Olma, nok', 'c': False}]},
        {'t': 'Suv o\'simliklari qanday nafas oladi?', 'a': [{'t': 'Suvdagi kislorod orqali', 'c': True}, {'t': 'Faqat havo orqali', 'c': False}, {'t': 'Nafas olmaydi', 'c': False}, {'t': 'Faqat tuproq orqali', 'c': False}]},
        {'t': 'Suv o\'simliklarining ahamiyati?', 'a': [{'t': 'Suvni tozalaydi, kislorod beradi', 'c': True}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Hech qanday ahamiyati yo\'q', 'c': False}, {'t': 'Faqat oziq-ovqat uchun', 'c': False}]},
    ]},
    {'n': 'Quruqlik o\'simliklari', 't': 20, 'o': 9, 'q': [
        {'t': 'Quruqlik o\'simliklari qayerda yashaydi?', 'a': [{'t': 'Quruqlikda', 'c': True}, {'t': 'Suvda', 'c': False}, {'t': 'Havoda', 'c': False}, {'t': 'Faqat tuproq ostida', 'c': False}]},
        {'t': 'Quruqlik o\'simliklarining asosiy qismlari?', 'a': [{'t': 'Ildiz, poya, barg', 'c': True}, {'t': 'Faqat ildiz', 'c': False}, {'t': 'Faqat poya', 'c': False}, {'t': 'Faqat barg', 'c': False}]},
        {'t': 'Ildiz vazifasi?', 'a': [{'t': 'O\'simlikni mahkamlash va oziqlanish', 'c': True}, {'t': 'Faqat mahkamlash', 'c': False}, {'t': 'Faqat oziqlanish', 'c': False}, {'t': 'Hech qanday vazifa yo\'q', 'c': False}]},
        {'t': 'Poya vazifasi?', 'a': [{'t': 'Moddalar tashish va o\'simlikni ko\'tarish', 'c': True}, {'t': 'Faqat ko\'tarish', 'c': False}, {'t': 'Faqat oziqlanish', 'c': False}, {'t': 'Hech qanday vazifa yo\'q', 'c': False}]},
        {'t': 'Barg vazifasi?', 'a': [{'t': 'Fotosintez va nafas olish', 'c': True}, {'t': 'Faqat fotosintez', 'c': False}, {'t': 'Faqat nafas olish', 'c': False}, {'t': 'Hech qanday vazifa yo\'q', 'c': False}]},
    ]},
    {'n': 'Fotosintez', 't': 25, 'o': 10, 'q': [
        {'t': 'Fotosintez nima?', 'a': [{'t': 'Yorug\'lik energiyasidan foydalanib organik modda sintezi', 'c': True}, {'t': 'Nafas olish jarayoni', 'c': False}, {'t': 'Oziqlanish jarayoni', 'c': False}, {'t': 'Ko\'payish jarayoni', 'c': False}]},
        {'t': 'Fotosintez qayerda sodir bo\'ladi?', 'a': [{'t': 'Xloroplastda', 'c': True}, {'t': 'Mitoxondriyada', 'c': False}, {'t': 'Yadroda', 'c': False}, {'t': 'Membranada', 'c': False}]},
        {'t': 'Fotosintez uchun nima kerak?', 'a': [{'t': 'Yorug\'lik, suv, karbonat angidrid', 'c': True}, {'t': 'Faqat yorug\'lik', 'c': False}, {'t': 'Faqat suv', 'c': False}, {'t': 'Faqat karbonat angidrid', 'c': False}]},
        {'t': 'Fotosintez natijasida nima hosil bo\'ladi?', 'a': [{'t': 'Glyukoza va kislorod', 'c': True}, {'t': 'Faqat glyukoza', 'c': False}, {'t': 'Faqat kislorod', 'c': False}, {'t': 'Karbonat angidrid', 'c': False}]},
        {'t': 'Fotosintez qachon sodir bo\'ladi?', 'a': [{'t': 'Yorug\'likda', 'c': True}, {'t': 'Qorong\'ida', 'c': False}, {'t': 'Har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'Fotosintezning ahamiyati?', 'a': [{'t': 'Kislorod ishlab chiqarish va oziq-ovqat hosil qilish', 'c': True}, {'t': 'Faqat kislorod ishlab chiqarish', 'c': False}, {'t': 'Faqat oziq-ovqat hosil qilish', 'c': False}, {'t': 'Hech qanday ahamiyat yo\'q', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("=" * 80)
    print("🌿 BIOLOGIYA - 100 TA MAVZU (ketma-ket o'rgatib boruvchi)")
    print("=" * 80)
    subject = get_or_create_biology()
    print(f"\n✅ Fan: {subject.name}\n")
    add_topics(subject, T[:10])  # Birinchi 10 ta mavzu
    total = sum(len(t['q']) for t in T[:10])
    print("\n" + "=" * 80)
    print(f"✅ TAYYOR! 10 ta mavzu, {total} ta test qo'shildi!")
    print("=" * 80)
