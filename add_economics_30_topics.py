"""
IQTISOD - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_economics():
    cat, _ = SubjectCategory.objects.get_or_create(slug='fanlar', defaults={'name': 'Fanlar', 'icon': 'bi-book', 'order': 1, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Iqtisod', defaults={'category': cat, 'description': 'Iqtisod fani - iqtisodiy jarayonlar, bozor mexanizmlari va moliyaviy tizimlar', 'icon': 'bi-graph-up', 'order': 40, 'is_active': True})
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
    {'n': 'Iqtisod faniga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Iqtisod nima?', 'a': [{'t': 'Resurslarni samarali taqsimlash va foydalanish haqidagi fan', 'c': True}, {'t': 'Faqat pul haqidagi fan', 'c': False}, {'t': 'Faqat savdo haqidagi fan', 'c': False}, {'t': 'Faqat ishlab chiqarish haqidagi fan', 'c': False}]},
        {'t': 'Iqtisodning asosiy muammosi nima?', 'a': [{'t': 'Cheklangan resurslar va cheksiz ehtiyojlar', 'c': True}, {'t': 'Yuqori narxlar', 'c': False}, {'t': 'Kam ish o\'rinlari', 'c': False}, {'t': 'Kambag\'allik', 'c': False}]},
        {'t': 'Mikroiqtisod nima bilan shug\'ullanadi?', 'a': [{'t': 'Alohida iste\'molchilar va firmalar xatti-harakatlari', 'c': True}, {'t': 'Butun mamlakat iqtisodiyoti', 'c': False}, {'t': 'Xalqaro savdo', 'c': False}, {'t': 'Davlat byudjeti', 'c': False}]},
        {'t': 'Makroiqtisod nimani o\'rganadi?', 'a': [{'t': 'Butun iqtisodiyotning umumiy ko\'rsatkichlari', 'c': True}, {'t': 'Faqat alohida kompaniyalar', 'c': False}, {'t': 'Faqat iste\'molchilar', 'c': False}, {'t': 'Faqat narxlar', 'c': False}]},
        {'t': 'Iqtisodiy resurslar qanday turlarga bo\'linadi?', 'a': [{'t': 'Mehnat, kapital, yer, tadbirkorlik', 'c': True}, {'t': 'Faqat pul va mehnat', 'c': False}, {'t': 'Faqat tabiiy resurslar', 'c': False}, {'t': 'Faqat texnologiya', 'c': False}]},
    ]},

    {'n': 'Talab va taklif qonuni', 't': 25, 'o': 2, 'q': [
        {'t': 'Talab nima?', 'a': [{'t': 'Iste\'molchilarning ma\'lum narxda sotib olishga tayyor bo\'lgan mahsulot miqdori', 'c': True}, {'t': 'Faqat xohish', 'c': False}, {'t': 'Ishlab chiqarish hajmi', 'c': False}, {'t': 'Sotuvchilar soni', 'c': False}]},
        {'t': 'Talab qonuni nimani bildiradi?', 'a': [{'t': 'Narx oshsa, talab kamayadi', 'c': True}, {'t': 'Narx oshsa, talab ortadi', 'c': False}, {'t': 'Narx va talab bog\'liq emas', 'c': False}, {'t': 'Talab doim o\'zgarmas', 'c': False}]},
        {'t': 'Taklif nima?', 'a': [{'t': 'Sotuvchilarning ma\'lum narxda sotishga tayyor bo\'lgan mahsulot miqdori', 'c': True}, {'t': 'Faqat ishlab chiqarish', 'c': False}, {'t': 'Faqat savdo', 'c': False}, {'t': 'Xaridorlar soni', 'c': False}]},
        {'t': 'Taklif qonuni nimani bildiradi?', 'a': [{'t': 'Narx oshsa, taklif ortadi', 'c': True}, {'t': 'Narx oshsa, taklif kamayadi', 'c': False}, {'t': 'Narx va taklif bog\'liq emas', 'c': False}, {'t': 'Taklif doim doimiy', 'c': False}]},
        {'t': 'Muvozanat narxi nima?', 'a': [{'t': 'Talab va taklif teng bo\'lgan narx', 'c': True}, {'t': 'Eng yuqori narx', 'c': False}, {'t': 'Eng past narx', 'c': False}, {'t': 'O\'rtacha narx', 'c': False}]},
        {'t': 'Agar narx muvozanat narxidan yuqori bo\'lsa nima bo\'ladi?', 'a': [{'t': 'Taklif ortiqcha bo\'ladi', 'c': True}, {'t': 'Talab ortiqcha bo\'ladi', 'c': False}, {'t': 'Hech narsa o\'zgarmaydi', 'c': False}, {'t': 'Bozor yo\'qoladi', 'c': False}]},
    ]},

    {'n': 'Bozor turlari', 't': 25, 'o': 3, 'q': [
        {'t': 'Mukammal raqobat bozori nima?', 'a': [{'t': 'Ko\'p sotuvchi va xaridorlar, bir xil mahsulot', 'c': True}, {'t': 'Bitta sotuvchi', 'c': False}, {'t': 'Ikki sotuvchi', 'c': False}, {'t': 'Davlat nazorati', 'c': False}]},
        {'t': 'Monopoliya nima?', 'a': [{'t': 'Bozorda bitta sotuvchi mavjud', 'c': True}, {'t': 'Ko\'p sotuvchilar', 'c': False}, {'t': 'Ikki sotuvchi', 'c': False}, {'t': 'Hech qanday sotuvchi yo\'q', 'c': False}]},
        {'t': 'Oligopoliya nima?', 'a': [{'t': 'Bozorda bir nechta yirik sotuvchilar hukmronlik qiladi', 'c': True}, {'t': 'Bitta sotuvchi', 'c': False}, {'t': 'Juda ko\'p sotuvchilar', 'c': False}, {'t': 'Hech qanday sotuvchi yo\'q', 'c': False}]},
        {'t': 'Monopolistik raqobat nima?', 'a': [{'t': 'Ko\'p sotuvchilar, lekin mahsulotlar farqlanadi', 'c': True}, {'t': 'Bitta sotuvchi', 'c': False}, {'t': 'Bir xil mahsulotlar', 'c': False}, {'t': 'Raqobat yo\'q', 'c': False}]},
        {'t': 'Qaysi bozorda narxlar eng past bo\'ladi?', 'a': [{'t': 'Mukammal raqobat bozorida', 'c': True}, {'t': 'Monopoliyada', 'c': False}, {'t': 'Oligopoliyada', 'c': False}, {'t': 'Hamma joyda bir xil', 'c': False}]},
        {'t': 'Monopoliyaning kamchiligi nima?', 'a': [{'t': 'Yuqori narxlar va kam ishlab chiqarish', 'c': True}, {'t': 'Past narxlar', 'c': False}, {'t': 'Ko\'p tanlov', 'c': False}, {'t': 'Yuqori sifat', 'c': False}]},
    ]},

    {'n': 'Egiluvchanlik (Elastiklik)', 't': 30, 'o': 4, 'q': [
        {'t': 'Talab egiluvchanligi nima?', 'a': [{'t': 'Narx o\'zgarganda talab qanchalik o\'zgarishi', 'c': True}, {'t': 'Faqat narx o\'zgarishi', 'c': False}, {'t': 'Faqat talab o\'zgarishi', 'c': False}, {'t': 'Daromad o\'zgarishi', 'c': False}]},
        {'t': 'Egiluvchan talab qachon bo\'ladi?', 'a': [{'t': 'Narx ozgina o\'zgarganda talab katta o\'zgaradi', 'c': True}, {'t': 'Narx o\'zgarganda talab o\'zgarmaydi', 'c': False}, {'t': 'Talab doim doimiy', 'c': False}, {'t': 'Narx doim doimiy', 'c': False}]},
        {'t': 'Egiluvchan bo\'lmagan talab qachon bo\'ladi?', 'a': [{'t': 'Narx o\'zgarganda talab kam o\'zgaradi', 'c': True}, {'t': 'Narx o\'zgarganda talab katta o\'zgaradi', 'c': False}, {'t': 'Talab yo\'qoladi', 'c': False}, {'t': 'Narx yo\'qoladi', 'c': False}]},
        {'t': 'Qaysi mahsulotlar talabi egiluvchan bo\'ladi?', 'a': [{'t': 'Hashamatli tovarlar, ko\'p o\'rinbosarlari bor tovarlar', 'c': True}, {'t': 'Zarur tovarlar', 'c': False}, {'t': 'Dori-darmonlar', 'c': False}, {'t': 'Oziq-ovqat', 'c': False}]},
        {'t': 'Qaysi mahsulotlar talabi egiluvchan emas?', 'a': [{'t': 'Zarur tovarlar, o\'rinbosari yo\'q tovarlar', 'c': True}, {'t': 'Hashamatli tovarlar', 'c': False}, {'t': 'Avtomobillar', 'c': False}, {'t': 'Sayohat xizmatlari', 'c': False}]},
        {'t': 'Daromad egiluvchanligi nima?', 'a': [{'t': 'Daromad o\'zgarganda talab qanchalik o\'zgarishi', 'c': True}, {'t': 'Faqat narx o\'zgarishi', 'c': False}, {'t': 'Faqat taklif o\'zgarishi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Egiluvchanlik koeffitsienti 1 dan katta bo\'lsa nima degani?', 'a': [{'t': 'Talab egiluvchan', 'c': True}, {'t': 'Talab egiluvchan emas', 'c': False}, {'t': 'Talab yo\'q', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'Iste\'molchi xatti-harakati', 't': 25, 'o': 5, 'q': [
        {'t': 'Foydalilik (utility) nima?', 'a': [{'t': 'Iste\'molchining tovardan olgan qoniqishi', 'c': True}, {'t': 'Tovar narxi', 'c': False}, {'t': 'Tovar sifati', 'c': False}, {'t': 'Tovar miqdori', 'c': False}]},
        {'t': 'Kamayib boruvchi foydalilik qonuni nima?', 'a': [{'t': 'Har bir qo\'shimcha birlik kamroq qoniqish beradi', 'c': True}, {'t': 'Foydalilik doim ortadi', 'c': False}, {'t': 'Foydalilik o\'zgarmaydi', 'c': False}, {'t': 'Foydalilik yo\'qoladi', 'c': False}]},
        {'t': 'Iste\'molchi tanlovida nima muhim?', 'a': [{'t': 'Byudjet cheklovi va afzalliklar', 'c': True}, {'t': 'Faqat narx', 'c': False}, {'t': 'Faqat sifat', 'c': False}, {'t': 'Faqat brend', 'c': False}]},
        {'t': 'Byudjet chizig\'i nima?', 'a': [{'t': 'Iste\'molchining sotib olish imkoniyatlari chegarasi', 'c': True}, {'t': 'Daromad miqdori', 'c': False}, {'t': 'Xarajatlar ro\'yxati', 'c': False}, {'t': 'Narxlar ro\'yxati', 'c': False}]},
        {'t': 'Iste\'molchi muvozanati qachon yuzaga keladi?', 'a': [{'t': 'Maksimal qoniqish olinganda', 'c': True}, {'t': 'Hamma pul sarflanganda', 'c': False}, {'t': 'Eng arzon tovar sotib olinganda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Ishlab chiqarish nazariyasi', 't': 30, 'o': 6, 'q': [
        {'t': 'Ishlab chiqarish omillari qaysilar?', 'a': [{'t': 'Mehnat, kapital, yer, tadbirkorlik', 'c': True}, {'t': 'Faqat mehnat', 'c': False}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat texnologiya', 'c': False}]},
        {'t': 'Qisqa muddat (short run) nima?', 'a': [{'t': 'Kamida bitta omil o\'zgarmas bo\'lgan davr', 'c': True}, {'t': 'Bir hafta', 'c': False}, {'t': 'Bir oy', 'c': False}, {'t': 'Bir yil', 'c': False}]},
        {'t': 'Uzoq muddat (long run) nima?', 'a': [{'t': 'Barcha omillar o\'zgaruvchan bo\'lgan davr', 'c': True}, {'t': 'Bir yil', 'c': False}, {'t': 'O\'n yil', 'c': False}, {'t': 'Abadiy', 'c': False}]},
        {'t': 'Kamayib boruvchi qo\'shimcha mahsulot qonuni nima?', 'a': [{'t': 'Har bir qo\'shimcha omil kamroq mahsulot beradi', 'c': True}, {'t': 'Mahsulot doim ortadi', 'c': False}, {'t': 'Mahsulot kamayadi', 'c': False}, {'t': 'Mahsulot o\'zgarmaydi', 'c': False}]},
        {'t': 'Miqyos samaradorligi (economies of scale) nima?', 'a': [{'t': 'Ishlab chiqarish hajmi oshganda o\'rtacha xarajatlar kamayadi', 'c': True}, {'t': 'Xarajatlar doim ortadi', 'c': False}, {'t': 'Xarajatlar o\'zgarmaydi', 'c': False}, {'t': 'Foyda kamayadi', 'c': False}]},
        {'t': 'Ishlab chiqarish funksiyasi nima?', 'a': [{'t': 'Omillar va mahsulot o\'rtasidagi bog\'lanish', 'c': True}, {'t': 'Faqat xarajatlar', 'c': False}, {'t': 'Faqat daromad', 'c': False}, {'t': 'Faqat foyda', 'c': False}]},
        {'t': 'Texnologik taraqqiyot ishlab chiqarishga qanday ta\'sir qiladi?', 'a': [{'t': 'Kam resurs bilan ko\'proq mahsulot ishlab chiqarish imkonini beradi', 'c': True}, {'t': 'Hech qanday ta\'sir qilmaydi', 'c': False}, {'t': 'Faqat xarajatlarni oshiradi', 'c': False}, {'t': 'Ishlab chiqarishni kamaytiradi', 'c': False}]},
    ]},

    {'n': 'Xarajatlar nazariyasi', 't': 30, 'o': 7, 'q': [
        {'t': 'Doimiy xarajatlar (fixed costs) nima?', 'a': [{'t': 'Ishlab chiqarish hajmiga bog\'liq bo\'lmagan xarajatlar', 'c': True}, {'t': 'Ishlab chiqarish hajmiga bog\'liq xarajatlar', 'c': False}, {'t': 'Faqat mehnat haqi', 'c': False}, {'t': 'Faqat xom ashyo', 'c': False}]},
        {'t': 'O\'zgaruvchan xarajatlar (variable costs) nima?', 'a': [{'t': 'Ishlab chiqarish hajmiga bog\'liq xarajatlar', 'c': True}, {'t': 'Ishlab chiqarish hajmiga bog\'liq bo\'lmagan xarajatlar', 'c': False}, {'t': 'Faqat ijara haqi', 'c': False}, {'t': 'Faqat soliqlar', 'c': False}]},
        {'t': 'Umumiy xarajatlar (total costs) qanday hisoblanadi?', 'a': [{'t': 'Doimiy xarajatlar + O\'zgaruvchan xarajatlar', 'c': True}, {'t': 'Faqat doimiy xarajatlar', 'c': False}, {'t': 'Faqat o\'zgaruvchan xarajatlar', 'c': False}, {'t': 'Daromad - Foyda', 'c': False}]},
        {'t': 'O\'rtacha xarajatlar (average costs) qanday hisoblanadi?', 'a': [{'t': 'Umumiy xarajatlar / Mahsulot miqdori', 'c': True}, {'t': 'Doimiy xarajatlar / 2', 'c': False}, {'t': 'O\'zgaruvchan xarajatlar * 2', 'c': False}, {'t': 'Daromad / Xarajatlar', 'c': False}]},
        {'t': 'Marjinal xarajat (marginal cost) nima?', 'a': [{'t': 'Qo\'shimcha bir birlik mahsulot ishlab chiqarish xarajati', 'c': True}, {'t': 'Umumiy xarajatlar', 'c': False}, {'t': 'O\'rtacha xarajatlar', 'c': False}, {'t': 'Doimiy xarajatlar', 'c': False}]},
        {'t': 'Muqobil xarajat (opportunity cost) nima?', 'a': [{'t': 'Tanlangan variantdan voz kechilgan eng yaxshi imkoniyat qiymati', 'c': True}, {'t': 'Pul xarajatlari', 'c': False}, {'t': 'Ishlab chiqarish xarajatlari', 'c': False}, {'t': 'Savdo xarajatlari', 'c': False}]},
        {'t': 'Qisqa muddatda firma qachon ishlab chiqarishni to\'xtatadi?', 'a': [{'t': 'Narx o\'rtacha o\'zgaruvchan xarajatdan past bo\'lsa', 'c': True}, {'t': 'Foyda kam bo\'lsa', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Doim', 'c': False}]},
    ]},

    {'n': 'Foyda va daromad', 't': 25, 'o': 8, 'q': [
        {'t': 'Umumiy daromad (total revenue) qanday hisoblanadi?', 'a': [{'t': 'Narx × Sotilgan miqdor', 'c': True}, {'t': 'Daromad - Xarajatlar', 'c': False}, {'t': 'Faqat sotilgan miqdor', 'c': False}, {'t': 'Faqat narx', 'c': False}]},
        {'t': 'Marjinal daromad (marginal revenue) nima?', 'a': [{'t': 'Qo\'shimcha bir birlik sotishdan olingan daromad', 'c': True}, {'t': 'Umumiy daromad', 'c': False}, {'t': 'O\'rtacha daromad', 'c': False}, {'t': 'Doimiy daromad', 'c': False}]},
        {'t': 'Iqtisodiy foyda qanday hisoblanadi?', 'a': [{'t': 'Umumiy daromad - Umumiy xarajatlar (muqobil xarajatlar bilan)', 'c': True}, {'t': 'Faqat daromad', 'c': False}, {'t': 'Daromad + Xarajatlar', 'c': False}, {'t': 'Faqat sotuvlar', 'c': False}]},
        {'t': 'Buxgalteriya foydasi nima?', 'a': [{'t': 'Daromad - Aniq pul xarajatlari', 'c': True}, {'t': 'Iqtisodiy foyda bilan bir xil', 'c': False}, {'t': 'Faqat daromad', 'c': False}, {'t': 'Faqat xarajatlar', 'c': False}]},
        {'t': 'Normal foyda nima?', 'a': [{'t': 'Tadbirkorni biznesda ushlab turish uchun minimal foyda', 'c': True}, {'t': 'Maksimal foyda', 'c': False}, {'t': 'Nol foyda', 'c': False}, {'t': 'Manfiy foyda', 'c': False}]},
        {'t': 'Firma qachon maksimal foyda oladi?', 'a': [{'t': 'Marjinal daromad = Marjinal xarajat bo\'lganda', 'c': True}, {'t': 'Eng ko\'p sotganda', 'c': False}, {'t': 'Eng yuqori narxda', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Mehnat bozori', 't': 30, 'o': 9, 'q': [
        {'t': 'Mehnat bozorida talab kimdan keladi?', 'a': [{'t': 'Firmalardan (ish beruvchilardan)', 'c': True}, {'t': 'Ishchilardan', 'c': False}, {'t': 'Davlatdan', 'c': False}, {'t': 'Iste\'molchilardan', 'c': False}]},
        {'t': 'Mehnat bozorida taklif kimdan keladi?', 'a': [{'t': 'Ishchilardan', 'c': True}, {'t': 'Firmalardan', 'c': False}, {'t': 'Davlatdan', 'c': False}, {'t': 'Bankdan', 'c': False}]},
        {'t': 'Ish haqi qanday belgilanadi?', 'a': [{'t': 'Mehnat talabi va taklifi asosida', 'c': True}, {'t': 'Faqat davlat tomonidan', 'c': False}, {'t': 'Faqat firma tomonidan', 'c': False}, {'t': 'Tasodifiy', 'c': False}]},
        {'t': 'Minimal ish haqi nima?', 'a': [{'t': 'Davlat tomonidan belgilangan eng past ish haqi', 'c': True}, {'t': 'Eng yuqori ish haqi', 'c': False}, {'t': 'O\'rtacha ish haqi', 'c': False}, {'t': 'Firma belgilagan ish haqi', 'c': False}]},
        {'t': 'Ishsizlik nima?', 'a': [{'t': 'Ishlashni xohlovchi, lekin ish topa olmagan kishilar', 'c': True}, {'t': 'Ishlashni xohlamaganlar', 'c': False}, {'t': 'Nafaqadagilar', 'c': False}, {'t': 'Talabalar', 'c': False}]},
        {'t': 'Ishsizlik turlari qaysilar?', 'a': [{'t': 'Friksion, strukturaviy, tsiklik', 'c': True}, {'t': 'Faqat friksion', 'c': False}, {'t': 'Faqat tsiklik', 'c': False}, {'t': 'Hech qanday tur yo\'q', 'c': False}]},
        {'t': 'Inson kapitali nima?', 'a': [{'t': 'Bilim, ko\'nikma va tajriba', 'c': True}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat mulk', 'c': False}, {'t': 'Faqat texnika', 'c': False}]},
    ]},

    {'n': 'Kapital va investitsiyalar', 't': 30, 'o': 10, 'q': [
        {'t': 'Kapital nima?', 'a': [{'t': 'Ishlab chiqarishda foydalaniladigan resurslar', 'c': True}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat bino', 'c': False}, {'t': 'Faqat yer', 'c': False}]},
        {'t': 'Jismoniy kapital nima?', 'a': [{'t': 'Mashinalar, binolar, asbob-uskunalar', 'c': True}, {'t': 'Pul', 'c': False}, {'t': 'Bilim', 'c': False}, {'t': 'Mehnat', 'c': False}]},
        {'t': 'Moliyaviy kapital nima?', 'a': [{'t': 'Pul va qimmatli qog\'ozlar', 'c': True}, {'t': 'Mashinalar', 'c': False}, {'t': 'Binolar', 'c': False}, {'t': 'Xom ashyo', 'c': False}]},
        {'t': 'Investitsiya nima?', 'a': [{'t': 'Kelajakda foyda olish uchun mablag\' sarflash', 'c': True}, {'t': 'Faqat xarajat', 'c': False}, {'t': 'Faqat tejash', 'c': False}, {'t': 'Faqat qarz olish', 'c': False}]},
        {'t': 'To\'g\'ridan-to\'g\'ri investitsiya nima?', 'a': [{'t': 'Ishlab chiqarish vositalariga investitsiya', 'c': True}, {'t': 'Faqat aksiyalar sotib olish', 'c': False}, {'t': 'Faqat obligatsiyalar', 'c': False}, {'t': 'Faqat bank depoziti', 'c': False}]},
        {'t': 'Portfel investitsiyasi nima?', 'a': [{'t': 'Qimmatli qog\'ozlarga investitsiya', 'c': True}, {'t': 'Faqat zavod qurish', 'c': False}, {'t': 'Faqat yer sotib olish', 'c': False}, {'t': 'Faqat texnika sotib olish', 'c': False}]},
        {'t': 'Investitsiya samaradorligini qanday baholash mumkin?', 'a': [{'t': 'Foyda darajasi va qaytish muddati orqali', 'c': True}, {'t': 'Faqat hajmi orqali', 'c': False}, {'t': 'Faqat vaqti orqali', 'c': False}, {'t': 'Baholab bo\'lmaydi', 'c': False}]},
    ]},

    {'n': 'Pul va bank tizimi', 't': 30, 'o': 11, 'q': [
        {'t': 'Pul nima?', 'a': [{'t': 'Umumiy qabul qilingan to\'lov vositasi', 'c': True}, {'t': 'Faqat qog\'oz pul', 'c': False}, {'t': 'Faqat oltin', 'c': False}, {'t': 'Faqat plastik karta', 'c': False}]},
        {'t': 'Pulning asosiy funksiyalari qaysilar?', 'a': [{'t': 'Almashinuv vositasi, hisob birligi, qiymat saqlash', 'c': True}, {'t': 'Faqat sotib olish', 'c': False}, {'t': 'Faqat saqlash', 'c': False}, {'t': 'Faqat hisoblash', 'c': False}]},
        {'t': 'Markaziy bank nima qiladi?', 'a': [{'t': 'Pul-kredit siyosatini yuritadi, pulni chiqaradi', 'c': True}, {'t': 'Faqat kredit beradi', 'c': False}, {'t': 'Faqat depozit qabul qiladi', 'c': False}, {'t': 'Faqat valyuta almashinuvi', 'c': False}]},
        {'t': 'Tijorat banklari nima qiladi?', 'a': [{'t': 'Depozit qabul qiladi va kredit beradi', 'c': True}, {'t': 'Faqat pul chiqaradi', 'c': False}, {'t': 'Faqat soliq yig\'adi', 'c': False}, {'t': 'Faqat valyuta sotadi', 'c': False}]},
        {'t': 'Inflyatsiya nima?', 'a': [{'t': 'Narxlarning umumiy ko\'tarilishi', 'c': True}, {'t': 'Narxlarning pasayishi', 'c': False}, {'t': 'Ish haqining oshishi', 'c': False}, {'t': 'Ishlab chiqarishning oshishi', 'c': False}]},
        {'t': 'Deflyatsiya nima?', 'a': [{'t': 'Narxlarning umumiy pasayishi', 'c': True}, {'t': 'Narxlarning oshishi', 'c': False}, {'t': 'Pul miqdorining oshishi', 'c': False}, {'t': 'Ishsizlikning oshishi', 'c': False}]},
        {'t': 'Foiz stavkasi nima?', 'a': [{'t': 'Qarz uchun to\'lanadigan haq foizi', 'c': True}, {'t': 'Soliq stavkasi', 'c': False}, {'t': 'Ish haqi stavkasi', 'c': False}, {'t': 'Narx stavkasi', 'c': False}]},
    ]},

    {'n': 'Yalpi ichki mahsulot (YIM)', 't': 30, 'o': 12, 'q': [
        {'t': 'YIM (GDP) nima?', 'a': [{'t': 'Mamlakatda bir yilda ishlab chiqarilgan barcha yakuniy mahsulotlar qiymati', 'c': True}, {'t': 'Faqat eksport', 'c': False}, {'t': 'Faqat import', 'c': False}, {'t': 'Faqat davlat xarajatlari', 'c': False}]},
        {'t': 'Nominal YIM nima?', 'a': [{'t': 'Joriy narxlarda hisoblangan YIM', 'c': True}, {'t': 'Doimiy narxlarda hisoblangan YIM', 'c': False}, {'t': 'Faqat eksport', 'c': False}, {'t': 'Faqat import', 'c': False}]},
        {'t': 'Real YIM nima?', 'a': [{'t': 'Doimiy (bazaviy) narxlarda hisoblangan YIM', 'c': True}, {'t': 'Joriy narxlarda hisoblangan YIM', 'c': False}, {'t': 'Faqat ishlab chiqarish', 'c': False}, {'t': 'Faqat xizmatlar', 'c': False}]},
        {'t': 'YIM tarkibiga nima kiradi?', 'a': [{'t': 'Iste\'mol, investitsiya, davlat xarajatlari, sof eksport', 'c': True}, {'t': 'Faqat iste\'mol', 'c': False}, {'t': 'Faqat eksport', 'c': False}, {'t': 'Faqat soliqlar', 'c': False}]},
        {'t': 'Aholi jon boshiga YIM nima?', 'a': [{'t': 'YIM / Aholi soni', 'c': True}, {'t': 'YIM × Aholi soni', 'c': False}, {'t': 'Faqat YIM', 'c': False}, {'t': 'Faqat aholi soni', 'c': False}]},
        {'t': 'YIM o\'sish sur\'ati nima ko\'rsatadi?', 'a': [{'t': 'Iqtisodiyot qanchalik tez rivojlanayotganini', 'c': True}, {'t': 'Faqat narxlar o\'zgarishini', 'c': False}, {'t': 'Faqat aholi o\'sishini', 'c': False}, {'t': 'Hech narsani', 'c': False}]},
        {'t': 'YIM ga nima kirmaydi?', 'a': [{'t': 'Oraliq mahsulotlar, qonuniy bo\'lmagan faoliyat', 'c': True}, {'t': 'Yakuniy mahsulotlar', 'c': False}, {'t': 'Xizmatlar', 'c': False}, {'t': 'Investitsiyalar', 'c': False}]},
    ]},

    {'n': 'Iqtisodiy o\'sish', 't': 25, 'o': 13, 'q': [
        {'t': 'Iqtisodiy o\'sish nima?', 'a': [{'t': 'Real YIM ning uzoq muddatli oshishi', 'c': True}, {'t': 'Faqat narxlar oshishi', 'c': False}, {'t': 'Faqat aholi oshishi', 'c': False}, {'t': 'Faqat eksport oshishi', 'c': False}]},
        {'t': 'Iqtisodiy o\'sish omillari qaysilar?', 'a': [{'t': 'Mehnat, kapital, texnologiya, ta\'lim', 'c': True}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat tabiiy resurslar', 'c': False}, {'t': 'Faqat davlat', 'c': False}]},
        {'t': 'Ekstensiv o\'sish nima?', 'a': [{'t': 'Resurslar miqdorini oshirish orqali o\'sish', 'c': True}, {'t': 'Samaradorlikni oshirish orqali o\'sish', 'c': False}, {'t': 'Faqat texnologiya orqali', 'c': False}, {'t': 'Hech qanday o\'sish yo\'q', 'c': False}]},
        {'t': 'Intensiv o\'sish nima?', 'a': [{'t': 'Samaradorlik va texnologiyani oshirish orqali o\'sish', 'c': True}, {'t': 'Faqat resurslar miqdorini oshirish', 'c': False}, {'t': 'Faqat mehnat miqdorini oshirish', 'c': False}, {'t': 'Hech qanday o\'sish yo\'q', 'c': False}]},
        {'t': 'Iqtisodiy rivojlanish nima?', 'a': [{'t': 'O\'sish bilan birga sifat va tuzilma o\'zgarishi', 'c': True}, {'t': 'Faqat YIM oshishi', 'c': False}, {'t': 'Faqat aholi oshishi', 'c': False}, {'t': 'Faqat narxlar oshishi', 'c': False}]},
        {'t': 'Barqaror rivojlanish nima?', 'a': [{'t': 'Kelajak avlodlar uchun resurslarni saqlab o\'sish', 'c': True}, {'t': 'Faqat tez o\'sish', 'c': False}, {'t': 'Faqat iqtisodiy o\'sish', 'c': False}, {'t': 'Hech qanday o\'sish yo\'q', 'c': False}]},
    ]},

    {'n': 'Iqtisodiy tsikllar', 't': 30, 'o': 14, 'q': [
        {'t': 'Iqtisodiy tsikl nima?', 'a': [{'t': 'Iqtisodiyotning davriy ravishda ko\'tarilishi va tushishi', 'c': True}, {'t': 'Faqat o\'sish', 'c': False}, {'t': 'Faqat pasayish', 'c': False}, {'t': 'O\'zgarmas holat', 'c': False}]},
        {'t': 'Iqtisodiy tsiklning bosqichlari qaysilar?', 'a': [{'t': 'Yuksalish, cho\'qqi, pasayish, tublik', 'c': True}, {'t': 'Faqat yuksalish', 'c': False}, {'t': 'Faqat pasayish', 'c': False}, {'t': 'Hech qanday bosqich yo\'q', 'c': False}]},
        {'t': 'Retsessiya nima?', 'a': [{'t': 'Iqtisodiyotning pasayish davri', 'c': True}, {'t': 'Iqtisodiyotning o\'sish davri', 'c': False}, {'t': 'Barqaror holat', 'c': False}, {'t': 'Yuqori o\'sish', 'c': False}]},
        {'t': 'Depressiya nima?', 'a': [{'t': 'Uzoq va chuqur iqtisodiy inqiroz', 'c': True}, {'t': 'Qisqa muddatli pasayish', 'c': False}, {'t': 'Yuqori o\'sish', 'c': False}, {'t': 'Normal holat', 'c': False}]},
        {'t': 'Bum (boom) nima?', 'a': [{'t': 'Iqtisodiyotning tez o\'sish davri', 'c': True}, {'t': 'Pasayish davri', 'c': False}, {'t': 'Inqiroz', 'c': False}, {'t': 'Barqaror holat', 'c': False}]},
        {'t': 'Iqtisodiy tsikllar sabablari nima?', 'a': [{'t': 'Talab o\'zgarishi, investitsiyalar, siyosat, shoklar', 'c': True}, {'t': 'Faqat narxlar', 'c': False}, {'t': 'Faqat ishsizlik', 'c': False}, {'t': 'Sabab yo\'q', 'c': False}]},
        {'t': 'Tsiklik ishsizlik nima?', 'a': [{'t': 'Retsessiya davrida yuzaga keladigan ishsizlik', 'c': True}, {'t': 'Doim mavjud ishsizlik', 'c': False}, {'t': 'Strukturaviy ishsizlik', 'c': False}, {'t': 'Friksion ishsizlik', 'c': False}]},
    ]},

    {'n': 'Fiskal siyosat', 't': 30, 'o': 15, 'q': [
        {'t': 'Fiskal siyosat nima?', 'a': [{'t': 'Davlat xarajatlari va soliqlar orqali iqtisodiyotni boshqarish', 'c': True}, {'t': 'Faqat pul miqdorini boshqarish', 'c': False}, {'t': 'Faqat valyuta kursi', 'c': False}, {'t': 'Faqat tashqi savdo', 'c': False}]},
        {'t': 'Kengaytiruvchi fiskal siyosat nima?', 'a': [{'t': 'Xarajatlarni oshirish yoki soliqlarni kamaytirish', 'c': True}, {'t': 'Xarajatlarni kamaytirish', 'c': False}, {'t': 'Soliqlarni oshirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Qisqartiruvchi fiskal siyosat nima?', 'a': [{'t': 'Xarajatlarni kamaytirish yoki soliqlarni oshirish', 'c': True}, {'t': 'Xarajatlarni oshirish', 'c': False}, {'t': 'Soliqlarni kamaytirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Byudjet defitsiti nima?', 'a': [{'t': 'Davlat xarajatlari daromadlardan ko\'p', 'c': True}, {'t': 'Daromadlar xarajatlardan ko\'p', 'c': False}, {'t': 'Xarajatlar va daromadlar teng', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
        {'t': 'Byudjet profitsiti nima?', 'a': [{'t': 'Davlat daromadlari xarajatlardan ko\'p', 'c': True}, {'t': 'Xarajatlar daromadlardan ko\'p', 'c': False}, {'t': 'Xarajatlar va daromadlar teng', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
        {'t': 'Davlat qarzi nima?', 'a': [{'t': 'Davlatning to\'plangan qarzlari', 'c': True}, {'t': 'Bir yillik defitsit', 'c': False}, {'t': 'Faqat tashqi qarz', 'c': False}, {'t': 'Faqat ichki qarz', 'c': False}]},
        {'t': 'Retsessiya davrida qanday fiskal siyosat kerak?', 'a': [{'t': 'Kengaytiruvchi (xarajatlarni oshirish)', 'c': True}, {'t': 'Qisqartiruvchi', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Faqat soliqlarni oshirish', 'c': False}]},
    ]},

    {'n': 'Monetar (pul-kredit) siyosat', 't': 30, 'o': 16, 'q': [
        {'t': 'Monetar siyosat nima?', 'a': [{'t': 'Markaziy bank tomonidan pul miqdorini boshqarish', 'c': True}, {'t': 'Davlat xarajatlarini boshqarish', 'c': False}, {'t': 'Soliqlarni boshqarish', 'c': False}, {'t': 'Tashqi savdoni boshqarish', 'c': False}]},
        {'t': 'Kengaytiruvchi monetar siyosat nima?', 'a': [{'t': 'Pul miqdorini oshirish, foiz stavkasini kamaytirish', 'c': True}, {'t': 'Pul miqdorini kamaytirish', 'c': False}, {'t': 'Foiz stavkasini oshirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Qisqartiruvchi monetar siyosat nima?', 'a': [{'t': 'Pul miqdorini kamaytirish, foiz stavkasini oshirish', 'c': True}, {'t': 'Pul miqdorini oshirish', 'c': False}, {'t': 'Foiz stavkasini kamaytirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Ochiq bozor operatsiyalari nima?', 'a': [{'t': 'Markaziy bank qimmatli qog\'ozlarni sotib olish/sotish', 'c': True}, {'t': 'Faqat valyuta sotish', 'c': False}, {'t': 'Faqat kredit berish', 'c': False}, {'t': 'Faqat depozit qabul qilish', 'c': False}]},
        {'t': 'Majburiy zaxira normasi nima?', 'a': [{'t': 'Banklar saqlab qolishi kerak bo\'lgan depozitlar foizi', 'c': True}, {'t': 'Foiz stavkasi', 'c': False}, {'t': 'Soliq stavkasi', 'c': False}, {'t': 'Valyuta kursi', 'c': False}]},
        {'t': 'Diskont stavkasi nima?', 'a': [{'t': 'Markaziy bank banklarga kredit beradigan foiz stavkasi', 'c': True}, {'t': 'Tijorat banklari stavkasi', 'c': False}, {'t': 'Soliq stavkasi', 'c': False}, {'t': 'Valyuta kursi', 'c': False}]},
        {'t': 'Inflyatsiya yuqori bo\'lsa qanday monetar siyosat kerak?', 'a': [{'t': 'Qisqartiruvchi (pul miqdorini kamaytirish)', 'c': True}, {'t': 'Kengaytiruvchi', 'c': False}, {'t': 'Hech qanday', 'c': False}, {'t': 'Faqat soliqlarni oshirish', 'c': False}]},
    ]},

    {'n': 'Xalqaro savdo', 't': 30, 'o': 17, 'q': [
        {'t': 'Xalqaro savdo nima?', 'a': [{'t': 'Mamlakatlar o\'rtasida tovar va xizmatlar almashinuvi', 'c': True}, {'t': 'Faqat ichki savdo', 'c': False}, {'t': 'Faqat eksport', 'c': False}, {'t': 'Faqat import', 'c': False}]},
        {'t': 'Eksport nima?', 'a': [{'t': 'Mahsulotlarni boshqa mamlakatlarga sotish', 'c': True}, {'t': 'Mahsulotlarni sotib olish', 'c': False}, {'t': 'Ichki savdo', 'c': False}, {'t': 'Xizmat ko\'rsatish', 'c': False}]},
        {'t': 'Import nima?', 'a': [{'t': 'Boshqa mamlakatlardan mahsulot sotib olish', 'c': True}, {'t': 'Mahsulot sotish', 'c': False}, {'t': 'Ichki ishlab chiqarish', 'c': False}, {'t': 'Xizmat ko\'rsatish', 'c': False}]},
        {'t': 'Savdo balansi nima?', 'a': [{'t': 'Eksport va import o\'rtasidagi farq', 'c': True}, {'t': 'Faqat eksport', 'c': False}, {'t': 'Faqat import', 'c': False}, {'t': 'Davlat byudjeti', 'c': False}]},
        {'t': 'Savdo profitsiti nima?', 'a': [{'t': 'Eksport importdan ko\'p', 'c': True}, {'t': 'Import eksportdan ko\'p', 'c': False}, {'t': 'Eksport va import teng', 'c': False}, {'t': 'Hech qanday savdo yo\'q', 'c': False}]},
        {'t': 'Savdo defitsiti nima?', 'a': [{'t': 'Import eksportdan ko\'p', 'c': True}, {'t': 'Eksport importdan ko\'p', 'c': False}, {'t': 'Eksport va import teng', 'c': False}, {'t': 'Hech qanday savdo yo\'q', 'c': False}]},
        {'t': 'Nisbiy ustunlik nazariyasi nimani aytadi?', 'a': [{'t': 'Har bir mamlakat nisbatan arzonroq ishlab chiqara oladigan mahsulotga ixtisoslashishi kerak', 'c': True}, {'t': 'Hamma narsani o\'zi ishlab chiqarish kerak', 'c': False}, {'t': 'Savdo qilmaslik kerak', 'c': False}, {'t': 'Faqat boy mamlakatlar savdo qilishi kerak', 'c': False}]},
    ]},

    {'n': 'Valyuta kursi', 't': 30, 'o': 18, 'q': [
        {'t': 'Valyuta kursi nima?', 'a': [{'t': 'Bir valyutaning boshqa valyutadagi narxi', 'c': True}, {'t': 'Faqat dollar narxi', 'c': False}, {'t': 'Faqat oltin narxi', 'c': False}, {'t': 'Mahsulot narxi', 'c': False}]},
        {'t': 'Suzuvchi valyuta kursi nima?', 'a': [{'t': 'Bozor talab-taklifi asosida o\'zgaradigan kurs', 'c': True}, {'t': 'Davlat belgilaydigan doimiy kurs', 'c': False}, {'t': 'Hech qachon o\'zgarmaydigan kurs', 'c': False}, {'t': 'Faqat oltin bilan bog\'liq kurs', 'c': False}]},
        {'t': 'Qattiq valyuta kursi nima?', 'a': [{'t': 'Davlat tomonidan belgilangan doimiy kurs', 'c': True}, {'t': 'Bozor belgilaydigan kurs', 'c': False}, {'t': 'Har kuni o\'zgaradigan kurs', 'c': False}, {'t': 'Hech qachon belgilanmaydigan kurs', 'c': False}]},
        {'t': 'Devalvatsiya nima?', 'a': [{'t': 'Milliy valyutaning qadrsizlanishi', 'c': True}, {'t': 'Milliy valyutaning qimmatlashishi', 'c': False}, {'t': 'Valyuta kursi o\'zgarmaydi', 'c': False}, {'t': 'Yangi valyuta kiritish', 'c': False}]},
        {'t': 'Revalvatsiya nima?', 'a': [{'t': 'Milliy valyutaning qimmatlashishi', 'c': True}, {'t': 'Milliy valyutaning qadrsizlanishi', 'c': False}, {'t': 'Valyuta kursi o\'zgarmaydi', 'c': False}, {'t': 'Eski valyutani almashtirish', 'c': False}]},
        {'t': 'Valyuta kursiga nima ta\'sir qiladi?', 'a': [{'t': 'Savdo balansi, foiz stavkasi, inflyatsiya, siyosiy barqarorlik', 'c': True}, {'t': 'Faqat davlat qarori', 'c': False}, {'t': 'Faqat oltin zaxirasi', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Milliy valyuta qadrsizlansa eksportga qanday ta\'sir qiladi?', 'a': [{'t': 'Eksport arzonlashadi va ortadi', 'c': True}, {'t': 'Eksport qimmatlashadi va kamayadi', 'c': False}, {'t': 'Hech qanday ta\'sir qilmaydi', 'c': False}, {'t': 'Eksport to\'xtaydi', 'c': False}]},
    ]},

    {'n': 'Proteksionizm va erkin savdo', 't': 30, 'o': 19, 'q': [
        {'t': 'Proteksionizm nima?', 'a': [{'t': 'Ichki ishlab chiqarishni tashqi raqobatdan himoya qilish siyosati', 'c': True}, {'t': 'Erkin savdo siyosati', 'c': False}, {'t': 'Barcha chegaralarni ochish', 'c': False}, {'t': 'Hech qanday savdo qilmaslik', 'c': False}]},
        {'t': 'Bojxona to\'lovi (tarif) nima?', 'a': [{'t': 'Import qilinadigan tovarlarga qo\'yiladigan soliq', 'c': True}, {'t': 'Eksport qilinadigan tovarlarga soliq', 'c': False}, {'t': 'Ichki savdo solig\'i', 'c': False}, {'t': 'Daromad solig\'i', 'c': False}]},
        {'t': 'Kvota nima?', 'a': [{'t': 'Import yoki eksport miqdorini cheklash', 'c': True}, {'t': 'Soliq stavkasi', 'c': False}, {'t': 'Valyuta kursi', 'c': False}, {'t': 'Narx chegarasi', 'c': False}]},
        {'t': 'Subsidiya nima?', 'a': [{'t': 'Davlat tomonidan ishlab chiqaruvchilarga moliyaviy yordam', 'c': True}, {'t': 'Iste\'molchilarga soliq', 'c': False}, {'t': 'Import to\'lovi', 'c': False}, {'t': 'Eksport taqiqi', 'c': False}]},
        {'t': 'Erkin savdo nima?', 'a': [{'t': 'Xalqaro savdoda cheklovlar yo\'qligi', 'c': True}, {'t': 'Yuqori bojxona to\'lovlari', 'c': False}, {'t': 'Qat\'iy kvotalar', 'c': False}, {'t': 'Savdo taqiqi', 'c': False}]},
        {'t': 'Proteksionizmning afzalligi nima?', 'a': [{'t': 'Ichki ishlab chiqarish va ish o\'rinlarini himoya qiladi', 'c': True}, {'t': 'Narxlarni pasaytiradi', 'c': False}, {'t': 'Tanlovni ko\'paytiradi', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
        {'t': 'Erkin savdoning afzalligi nima?', 'a': [{'t': 'Past narxlar, ko\'p tanlov, samaradorlik', 'c': True}, {'t': 'Ichki ishlab chiqarishni himoya qiladi', 'c': False}, {'t': 'Ish o\'rinlarini ko\'paytiradi', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},

    {'n': 'Iqtisodiy integratsiya', 't': 25, 'o': 20, 'q': [
        {'t': 'Iqtisodiy integratsiya nima?', 'a': [{'t': 'Mamlakatlarning iqtisodiy birlashuvi', 'c': True}, {'t': 'Mamlakatlarning ajralishi', 'c': False}, {'t': 'Faqat siyosiy birlashuv', 'c': False}, {'t': 'Faqat harbiy ittifoq', 'c': False}]},
        {'t': 'Erkin savdo zonasi nima?', 'a': [{'t': 'A\'zo mamlakatlar o\'rtasida bojxona to\'lovlari yo\'q', 'c': True}, {'t': 'Umumiy valyuta', 'c': False}, {'t': 'Umumiy byudjet', 'c': False}, {'t': 'Umumiy hukumat', 'c': False}]},
        {'t': 'Bojxona ittifoqi nima?', 'a': [{'t': 'Erkin savdo + uchinchi mamlakatlarga umumiy tarif', 'c': True}, {'t': 'Faqat erkin savdo', 'c': False}, {'t': 'Umumiy valyuta', 'c': False}, {'t': 'Umumiy hukumat', 'c': False}]},
        {'t': 'Umumiy bozor nima?', 'a': [{'t': 'Bojxona ittifoqi + ishchi kuchi va kapital erkin harakati', 'c': True}, {'t': 'Faqat tovarlar savdosi', 'c': False}, {'t': 'Faqat xizmatlar savdosi', 'c': False}, {'t': 'Hech qanday integratsiya yo\'q', 'c': False}]},
        {'t': 'Iqtisodiy ittifoq nima?', 'a': [{'t': 'Umumiy bozor + umumiy iqtisodiy siyosat', 'c': True}, {'t': 'Faqat erkin savdo', 'c': False}, {'t': 'Faqat bojxona ittifoqi', 'c': False}, {'t': 'Hech qanday birlashuv yo\'q', 'c': False}]},
        {'t': 'Yevropa Ittifoqi (EU) qanday integratsiya?', 'a': [{'t': 'Iqtisodiy va valyuta ittifoqi', 'c': True}, {'t': 'Faqat erkin savdo zonasi', 'c': False}, {'t': 'Faqat bojxona ittifoqi', 'c': False}, {'t': 'Hech qanday integratsiya emas', 'c': False}]},
    ]},

    {'n': 'Iqtisodiy tizimlar', 't': 25, 'o': 21, 'q': [
        {'t': 'Bozor iqtisodiyoti nima?', 'a': [{'t': 'Xususiy mulk va erkin bozor asosidagi tizim', 'c': True}, {'t': 'Davlat boshqaradigan tizim', 'c': False}, {'t': 'Aralash tizim', 'c': False}, {'t': 'An\'anaviy tizim', 'c': False}]},
        {'t': 'Rejali (markazlashgan) iqtisodiyot nima?', 'a': [{'t': 'Davlat barcha iqtisodiy qarorlarni qabul qiladi', 'c': True}, {'t': 'Bozor qarorlar qabul qiladi', 'c': False}, {'t': 'Xususiy mulk asosida', 'c': False}, {'t': 'Erkin raqobat mavjud', 'c': False}]},
        {'t': 'Aralash iqtisodiyot nima?', 'a': [{'t': 'Bozor va davlat aralashuvi birgalikda', 'c': True}, {'t': 'Faqat bozor', 'c': False}, {'t': 'Faqat davlat', 'c': False}, {'t': 'An\'anaviy usullar', 'c': False}]},
        {'t': 'An\'anaviy iqtisodiyot nima?', 'a': [{'t': 'Urf-odatlar va an\'analarga asoslangan tizim', 'c': True}, {'t': 'Zamonaviy bozor tizimi', 'c': False}, {'t': 'Davlat rejasi', 'c': False}, {'t': 'Aralash tizim', 'c': False}]},
        {'t': 'Hozirgi zamonda qaysi tizim ko\'proq qo\'llaniladi?', 'a': [{'t': 'Aralash iqtisodiyot', 'c': True}, {'t': 'Sof bozor iqtisodiyoti', 'c': False}, {'t': 'Sof rejali iqtisodiyot', 'c': False}, {'t': 'An\'anaviy iqtisodiyot', 'c': False}]},
        {'t': 'Bozor iqtisodiyotining asosiy xususiyati nima?', 'a': [{'t': 'Xususiy mulk va erkin narx tizimi', 'c': True}, {'t': 'Davlat mulki', 'c': False}, {'t': 'Belgilangan narxlar', 'c': False}, {'t': 'Markaziy reja', 'c': False}]},
    ]},

    {'n': 'Davlatning iqtisodiyotdagi roli', 't': 30, 'o': 22, 'q': [
        {'t': 'Davlat iqtisodiyotda nima uchun aralashadi?', 'a': [{'t': 'Bozor kamchiliklarini tuzatish, adolatni ta\'minlash', 'c': True}, {'t': 'Faqat soliq yig\'ish uchun', 'c': False}, {'t': 'Faqat pul chiqarish uchun', 'c': False}, {'t': 'Aralashmasligi kerak', 'c': False}]},
        {'t': 'Bozor kamchiliklari (market failures) nima?', 'a': [{'t': 'Bozor samarali natija bera olmaydigan holatlar', 'c': True}, {'t': 'Davlat xatolari', 'c': False}, {'t': 'Iste\'molchi xatolari', 'c': False}, {'t': 'Hech qanday muammo yo\'q', 'c': False}]},
        {'t': 'Jamoat tovarlari (public goods) nima?', 'a': [{'t': 'Hamma foydalana oladigan, raqobatsiz tovarlar (mudofaa, yo\'llar)', 'c': True}, {'t': 'Faqat boylar uchun tovarlar', 'c': False}, {'t': 'Xususiy tovarlar', 'c': False}, {'t': 'Hashamatli tovarlar', 'c': False}]},
        {'t': 'Tashqi ta\'sirlar (externalities) nima?', 'a': [{'t': 'Uchinchi shaxslarga ta\'sir qiluvchi ijobiy yoki salbiy oqibatlar', 'c': True}, {'t': 'Faqat ichki ta\'sirlar', 'c': False}, {'t': 'Faqat narx o\'zgarishi', 'c': False}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}]},
        {'t': 'Salbiy tashqi ta\'sirga misol nima?', 'a': [{'t': 'Ifloslanish, shovqin', 'c': True}, {'t': 'Ta\'lim', 'c': False}, {'t': 'Tibbiyot', 'c': False}, {'t': 'Tadqiqot', 'c': False}]},
        {'t': 'Ijobiy tashqi ta\'sirga misol nima?', 'a': [{'t': 'Ta\'lim, tadqiqot, emlash', 'c': True}, {'t': 'Ifloslanish', 'c': False}, {'t': 'Shovqin', 'c': False}, {'t': 'Chiqindilar', 'c': False}]},
        {'t': 'Davlat qanday tovarlar ishlab chiqaradi?', 'a': [{'t': 'Jamoat tovarlari (mudofaa, yo\'llar, ta\'lim)', 'c': True}, {'t': 'Barcha tovarlar', 'c': False}, {'t': 'Faqat hashamatli tovarlar', 'c': False}, {'t': 'Hech qanday tovar emas', 'c': False}]},
    ]},

    {'n': 'Soliqlar tizimi', 't': 30, 'o': 23, 'q': [
        {'t': 'Soliq nima?', 'a': [{'t': 'Davlatga majburiy to\'lov', 'c': True}, {'t': 'Ixtiyoriy xayriya', 'c': False}, {'t': 'Qarz', 'c': False}, {'t': 'Investitsiya', 'c': False}]},
        {'t': 'To\'g\'ridan-to\'g\'ri soliqlar qaysilar?', 'a': [{'t': 'Daromad, foyda, mulk soliqlari', 'c': True}, {'t': 'QQS, aksiz', 'c': False}, {'t': 'Bojxona to\'lovlari', 'c': False}, {'t': 'Hech qanday soliq yo\'q', 'c': False}]},
        {'t': 'Bilvosita soliqlar qaysilar?', 'a': [{'t': 'QQS, aksiz, bojxona to\'lovlari', 'c': True}, {'t': 'Daromad solig\'i', 'c': False}, {'t': 'Foyda solig\'i', 'c': False}, {'t': 'Mulk solig\'i', 'c': False}]},
        {'t': 'Progressiv soliq nima?', 'a': [{'t': 'Daromad oshgan sari stavka ortadi', 'c': True}, {'t': 'Hamma uchun bir xil stavka', 'c': False}, {'t': 'Daromad oshgan sari stavka kamayadi', 'c': False}, {'t': 'Soliq yo\'q', 'c': False}]},
        {'t': 'Proporsional soliq nima?', 'a': [{'t': 'Hamma uchun bir xil foiz stavkasi', 'c': True}, {'t': 'Daromad oshgan sari stavka ortadi', 'c': False}, {'t': 'Daromad oshgan sari stavka kamayadi', 'c': False}, {'t': 'Soliq yo\'q', 'c': False}]},
        {'t': 'Regressiv soliq nima?', 'a': [{'t': 'Daromad oshgan sari soliq yuki kamayadi', 'c': True}, {'t': 'Daromad oshgan sari stavka ortadi', 'c': False}, {'t': 'Hamma uchun bir xil', 'c': False}, {'t': 'Soliq yo\'q', 'c': False}]},
        {'t': 'Soliqlarning asosiy funksiyalari qaysilar?', 'a': [{'t': 'Fiskal (daromad), tartibga solish, ijtimoiy', 'c': True}, {'t': 'Faqat daromad olish', 'c': False}, {'t': 'Faqat jazolash', 'c': False}, {'t': 'Hech qanday funksiya yo\'q', 'c': False}]},
    ]},

    {'n': 'Iqtisodiy o\'sish ko\'rsatkichlari', 't': 25, 'o': 24, 'q': [
        {'t': 'YIM deflatori nima?', 'a': [{'t': 'Nominal YIM ni real YIM ga aylantirish koeffitsienti', 'c': True}, {'t': 'Faqat inflyatsiya', 'c': False}, {'t': 'Faqat YIM', 'c': False}, {'t': 'Ishsizlik ko\'rsatkichi', 'c': False}]},
        {'t': 'Iste\'mol narxlari indeksi (CPI) nima?', 'a': [{'t': 'Iste\'mol savatidagi tovarlar narxining o\'zgarishi', 'c': True}, {'t': 'Faqat oziq-ovqat narxi', 'c': False}, {'t': 'Faqat xizmatlar narxi', 'c': False}, {'t': 'YIM o\'zgarishi', 'c': False}]},
        {'t': 'Ishlab chiqaruvchilar narxlari indeksi (PPI) nima?', 'a': [{'t': 'Ishlab chiqaruvchilar sotadigan tovarlar narxining o\'zgarishi', 'c': True}, {'t': 'Iste\'mol narxlari', 'c': False}, {'t': 'Faqat xom ashyo narxi', 'c': False}, {'t': 'Ish haqi o\'zgarishi', 'c': False}]},
        {'t': 'Ishsizlik darajasi qanday hisoblanadi?', 'a': [{'t': '(Ishsizlar / Mehnat kuchi) × 100%', 'c': True}, {'t': 'Faqat ishsizlar soni', 'c': False}, {'t': 'Faqat ishchilar soni', 'c': False}, {'t': 'Aholi soni', 'c': False}]},
        {'t': 'Bandlik darajasi nima?', 'a': [{'t': 'Ishlovchilarning mehnat kuchidagi ulushi', 'c': True}, {'t': 'Faqat ishchilar soni', 'c': False}, {'t': 'Faqat ishsizlar soni', 'c': False}, {'t': 'Aholi soni', 'c': False}]},
        {'t': 'Mehnat unumdorligi qanday hisoblanadi?', 'a': [{'t': 'Mahsulot / Mehnat miqdori', 'c': True}, {'t': 'Mehnat / Mahsulot', 'c': False}, {'t': 'Faqat mahsulot', 'c': False}, {'t': 'Faqat mehnat', 'c': False}]},
    ]},

    {'n': 'Kambag\'allik va tengsizlik', 't': 30, 'o': 25, 'q': [
        {'t': 'Absolut kambag\'allik nima?', 'a': [{'t': 'Asosiy ehtiyojlarni qondira olmaslik', 'c': True}, {'t': 'Boshqalarga nisbatan kam daromad', 'c': False}, {'t': 'Ishsizlik', 'c': False}, {'t': 'Yuqori narxlar', 'c': False}]},
        {'t': 'Nisbiy kambag\'allik nima?', 'a': [{'t': 'Jamiyatdagi o\'rtacha daromaddan ancha past daromad', 'c': True}, {'t': 'Asosiy ehtiyojlarni qondira olmaslik', 'c': False}, {'t': 'Ishsizlik', 'c': False}, {'t': 'Yuqori narxlar', 'c': False}]},
        {'t': 'Gini koeffitsienti nima?', 'a': [{'t': 'Daromad tengsizligini o\'lchovchi ko\'rsatkich (0-1)', 'c': True}, {'t': 'Inflyatsiya ko\'rsatkichi', 'c': False}, {'t': 'YIM ko\'rsatkichi', 'c': False}, {'t': 'Ishsizlik ko\'rsatkichi', 'c': False}]},
        {'t': 'Gini koeffitsienti 0 ga yaqin bo\'lsa nima degani?', 'a': [{'t': 'Daromadlar teng taqsimlangan', 'c': True}, {'t': 'Katta tengsizlik', 'c': False}, {'t': 'Yuqori kambag\'allik', 'c': False}, {'t': 'Yuqori inflyatsiya', 'c': False}]},
        {'t': 'Gini koeffitsienti 1 ga yaqin bo\'lsa nima degani?', 'a': [{'t': 'Katta daromad tengsizligi', 'c': True}, {'t': 'Daromadlar teng', 'c': False}, {'t': 'Kambag\'allik yo\'q', 'c': False}, {'t': 'Inflyatsiya yo\'q', 'c': False}]},
        {'t': 'Lorenz egri chizig\'i nima ko\'rsatadi?', 'a': [{'t': 'Daromad taqsimotini grafik ko\'rinishda', 'c': True}, {'t': 'Inflyatsiya o\'zgarishini', 'c': False}, {'t': 'YIM o\'sishini', 'c': False}, {'t': 'Ishsizlik dinamikasini', 'c': False}]},
        {'t': 'Kambag\'alikni kamaytirish usullari qaysilar?', 'a': [{'t': 'Ta\'lim, ish o\'rinlari, ijtimoiy yordam, progressiv soliqlar', 'c': True}, {'t': 'Faqat pul berish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat soliqlarni oshirish', 'c': False}]},
    ]},

    {'n': 'Iqtisodiy rivojlanish ko\'rsatkichlari', 't': 25, 'o': 26, 'q': [
        {'t': 'Inson rivojlanish indeksi (HDI) nima?', 'a': [{'t': 'Umr ko\'rish, ta\'lim va daromad asosidagi murakkab ko\'rsatkich', 'c': True}, {'t': 'Faqat YIM', 'c': False}, {'t': 'Faqat daromad', 'c': False}, {'t': 'Faqat ta\'lim', 'c': False}]},
        {'t': 'HDI qanday qiymatlar orasida bo\'ladi?', 'a': [{'t': '0 dan 1 gacha', 'c': True}, {'t': '0 dan 100 gacha', 'c': False}, {'t': '1 dan 10 gacha', 'c': False}, {'t': 'Cheksiz', 'c': False}]},
        {'t': 'Hayot sifati ko\'rsatkichlariga nima kiradi?', 'a': [{'t': 'Sog\'liqni saqlash, ta\'lim, ekologiya, xavfsizlik', 'c': True}, {'t': 'Faqat daromad', 'c': False}, {'t': 'Faqat YIM', 'c': False}, {'t': 'Faqat ish haqi', 'c': False}]},
        {'t': 'Savodxonlik darajasi nima?', 'a': [{'t': 'O\'qiy va yoza oladigan aholining ulushi', 'c': True}, {'t': 'Faqat maktabga boruvchilar', 'c': False}, {'t': 'Faqat oliy ma\'lumotlilar', 'c': False}, {'t': 'Faqat ishlovchilar', 'c': False}]},
        {'t': 'Chaqaloq o\'limi darajasi nima ko\'rsatadi?', 'a': [{'t': 'Sog\'liqni saqlash tizimi sifatini', 'c': True}, {'t': 'Faqat iqtisodiy o\'sishni', 'c': False}, {'t': 'Faqat daromadni', 'c': False}, {'t': 'Hech narsani', 'c': False}]},
        {'t': 'O\'rtacha umr ko\'rish davomiyligi nima?', 'a': [{'t': 'Tug\'ilgan chaqaloqning kutilayotgan yashash yillari', 'c': True}, {'t': 'Faqat qariyalar yoshi', 'c': False}, {'t': 'Faqat o\'rtacha yosh', 'c': False}, {'t': 'Nafaqaga chiqish yoshi', 'c': False}]},
    ]},

    {'n': 'Globallashuv', 't': 30, 'o': 27, 'q': [
        {'t': 'Globallashuv nima?', 'a': [{'t': 'Dunyo iqtisodiyotlarining o\'zaro bog\'lanishi va integratsiyasi', 'c': True}, {'t': 'Faqat savdo', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat turizm', 'c': False}]},
        {'t': 'Globallashuvning ijobiy tomonlari qaysilar?', 'a': [{'t': 'Savdo o\'sishi, texnologiya tarqalishi, tanlov ko\'payishi', 'c': True}, {'t': 'Faqat narxlar oshishi', 'c': False}, {'t': 'Faqat ishsizlik', 'c': False}, {'t': 'Hech qanday foyda yo\'q', 'c': False}]},
        {'t': 'Globallashuvning salbiy tomonlari qaysilar?', 'a': [{'t': 'Tengsizlik o\'sishi, madaniy yo\'qotishlar, ekologik muammolar', 'c': True}, {'t': 'Faqat ijobiy tomonlari bor', 'c': False}, {'t': 'Hech qanday salbiy tomoni yo\'q', 'c': False}, {'t': 'Faqat narxlar pasayishi', 'c': False}]},
        {'t': 'Transmilliy korporatsiyalar (TNK) nima?', 'a': [{'t': 'Bir nechta mamlakatda faoliyat yurituvchi yirik kompaniyalar', 'c': True}, {'t': 'Faqat bir mamlakatdagi kompaniyalar', 'c': False}, {'t': 'Faqat kichik biznes', 'c': False}, {'t': 'Davlat korxonalari', 'c': False}]},
        {'t': 'To\'g\'ridan-to\'g\'ri xorijiy investitsiyalar (FDI) nima?', 'a': [{'t': 'Boshqa mamlakatda korxona ochish yoki sotib olish', 'c': True}, {'t': 'Faqat aksiyalar sotib olish', 'c': False}, {'t': 'Faqat qarz berish', 'c': False}, {'t': 'Faqat savdo', 'c': False}]},
        {'t': 'Jahon Savdo Tashkiloti (WTO) nima qiladi?', 'a': [{'t': 'Xalqaro savdo qoidalarini tartibga soladi', 'c': True}, {'t': 'Faqat kredit beradi', 'c': False}, {'t': 'Faqat yordam beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Xalqaro Valyuta Fondi (IMF) nima qiladi?', 'a': [{'t': 'Valyuta barqarorligini ta\'minlaydi, moliyaviy yordam beradi', 'c': True}, {'t': 'Faqat savdoni tartibga soladi', 'c': False}, {'t': 'Faqat rivojlanish loyihalarini moliyalashtiradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'Raqamli iqtisodiyot', 't': 30, 'o': 28, 'q': [
        {'t': 'Raqamli iqtisodiyot nima?', 'a': [{'t': 'Raqamli texnologiyalarga asoslangan iqtisodiy faoliyat', 'c': True}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}, {'t': 'An\'anaviy iqtisodiyot', 'c': False}]},
        {'t': 'Elektron tijorat (e-commerce) nima?', 'a': [{'t': 'Internet orqali tovar va xizmatlar savdosi', 'c': True}, {'t': 'Faqat do\'kon savdosi', 'c': False}, {'t': 'Faqat bozor savdosi', 'c': False}, {'t': 'Faqat bank xizmatlari', 'c': False}]},
        {'t': 'Platformali iqtisodiyot nima?', 'a': [{'t': 'Raqamli platformalar orqali xizmat ko\'rsatish (Uber, Airbnb)', 'c': True}, {'t': 'Faqat zavod ishlab chiqarishi', 'c': False}, {'t': 'Faqat qishloq xo\'jaligi', 'c': False}, {'t': 'An\'anaviy biznes', 'c': False}]},
        {'t': 'Kriptovalyuta nima?', 'a': [{'t': 'Raqamli, markazlashtirilmagan pul', 'c': True}, {'t': 'Oddiy qog\'oz pul', 'c': False}, {'t': 'Faqat oltin', 'c': False}, {'t': 'Bank kartasi', 'c': False}]},
        {'t': 'Blokcheyn texnologiyasi nima?', 'a': [{'t': 'Tarqatilgan, o\'zgarmas ma\'lumotlar bazasi', 'c': True}, {'t': 'Oddiy ma\'lumotlar bazasi', 'c': False}, {'t': 'Faqat internet', 'c': False}, {'t': 'Faqat kompyuter', 'c': False}]},
        {'t': 'Sun\'iy intellekt iqtisodiyotga qanday ta\'sir qiladi?', 'a': [{'t': 'Avtomatlashtirish, samaradorlik oshishi, yangi ish o\'rinlari', 'c': True}, {'t': 'Hech qanday ta\'sir yo\'q', 'c': False}, {'t': 'Faqat salbiy ta\'sir', 'c': False}, {'t': 'Faqat ishsizlik', 'c': False}]},
        {'t': 'Raqamli iqtisodiyotning afzalliklari qaysilar?', 'a': [{'t': 'Tezlik, qulaylik, past xarajatlar, global kirish', 'c': True}, {'t': 'Faqat qimmatlik', 'c': False}, {'t': 'Faqat murakkablik', 'c': False}, {'t': 'Hech qanday afzallik yo\'q', 'c': False}]},
    ]},

    {'n': 'Ekologik iqtisodiyot', 't': 30, 'o': 29, 'q': [
        {'t': 'Ekologik iqtisodiyot nima?', 'a': [{'t': 'Atrof-muhitni hisobga olgan iqtisodiy faoliyat', 'c': True}, {'t': 'Faqat ishlab chiqarish', 'c': False}, {'t': 'Faqat savdo', 'c': False}, {'t': 'Atrof-muhitni e\'tiborsiz qoldirish', 'c': False}]},
        {'t': 'Yashil iqtisodiyot nima?', 'a': [{'t': 'Kam uglerodli, resurs tejovchi, ijtimoiy inklyuziv iqtisodiyot', 'c': True}, {'t': 'Faqat qishloq xo\'jaligi', 'c': False}, {'t': 'Faqat o\'rmon xo\'jaligi', 'c': False}, {'t': 'An\'anaviy iqtisodiyot', 'c': False}]},
        {'t': 'Qayta tiklanadigan energiya manbalari qaysilar?', 'a': [{'t': 'Quyosh, shamol, suv, biomassa', 'c': True}, {'t': 'Neft, gaz, ko\'mir', 'c': False}, {'t': 'Faqat atom energiyasi', 'c': False}, {'t': 'Hech qanday manba yo\'q', 'c': False}]},
        {'t': 'Uglerod izi (carbon footprint) nima?', 'a': [{'t': 'Faoliyat natijasida chiqarilgan issiqxona gazlari miqdori', 'c': True}, {'t': 'Faqat elektr iste\'moli', 'c': False}, {'t': 'Faqat suv iste\'moli', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Aylanma iqtisodiyot (circular economy) nima?', 'a': [{'t': 'Chiqindilarni qayta ishlash va resurslarni qayta ishlatish tizimi', 'c': True}, {'t': 'Chiziqli ishlab chiqarish', 'c': False}, {'t': 'Faqat iste\'mol', 'c': False}, {'t': 'Faqat ishlab chiqarish', 'c': False}]},
        {'t': 'Ekologik soliq nima?', 'a': [{'t': 'Atrof-muhitga zarar yetkazish uchun soliq', 'c': True}, {'t': 'Daromad solig\'i', 'c': False}, {'t': 'QQS', 'c': False}, {'t': 'Foyda solig\'i', 'c': False}]},
        {'t': 'Barqaror rivojlanish maqsadlari (SDG) nima?', 'a': [{'t': 'BMT tomonidan belgilangan 17 ta global maqsad', 'c': True}, {'t': 'Faqat iqtisodiy maqsadlar', 'c': False}, {'t': 'Faqat ekologik maqsadlar', 'c': False}, {'t': 'Hech qanday maqsad yo\'q', 'c': False}]},
    ]},

    {'n': 'Tadbirkorlik va innovatsiya', 't': 30, 'o': 30, 'q': [
        {'t': 'Tadbirkor kim?', 'a': [{'t': 'Yangi biznes yaratuvchi, xavf-xatar oluvchi shaxs', 'c': True}, {'t': 'Faqat ishchi', 'c': False}, {'t': 'Faqat menejer', 'c': False}, {'t': 'Faqat investor', 'c': False}]},
        {'t': 'Tadbirkorlikning asosiy xususiyatlari qaysilar?', 'a': [{'t': 'Innovatsiya, xavf-xatar, tashabbuskorlik, mas\'uliyat', 'c': True}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat bilim', 'c': False}, {'t': 'Faqat omad', 'c': False}]},
        {'t': 'Innovatsiya nima?', 'a': [{'t': 'Yangi mahsulot, xizmat yoki jarayonni joriy etish', 'c': True}, {'t': 'Faqat ixtiro', 'c': False}, {'t': 'Faqat texnologiya', 'c': False}, {'t': 'Eski usullar', 'c': False}]},
        {'t': 'Startap nima?', 'a': [{'t': 'Yangi, tez o\'sishga mo\'ljallangan kompaniya', 'c': True}, {'t': 'Eski kompaniya', 'c': False}, {'t': 'Davlat korxonasi', 'c': False}, {'t': 'Kichik do\'kon', 'c': False}]},
        {'t': 'Biznes-reja nima?', 'a': [{'t': 'Biznes maqsadlari va strategiyasini tavsiflovchi hujjat', 'c': True}, {'t': 'Faqat moliyaviy hisobot', 'c': False}, {'t': 'Faqat marketing reja', 'c': False}, {'t': 'Hech qanday hujjat emas', 'c': False}]},
        {'t': 'Venchur kapitali nima?', 'a': [{'t': 'Yuqori xavfli startaplarga investitsiya', 'c': True}, {'t': 'Bank krediti', 'c': False}, {'t': 'Davlat subsidiyasi', 'c': False}, {'t': 'Shaxsiy jamg\'arma', 'c': False}]},
        {'t': 'Tadbirkorlik muhiti nima?', 'a': [{'t': 'Biznes yuritish uchun qonuniy, iqtisodiy va ijtimoiy sharoitlar', 'c': True}, {'t': 'Faqat ofis', 'c': False}, {'t': 'Faqat bozor', 'c': False}, {'t': 'Faqat davlat', 'c': False}]},
        {'t': 'Intellektual mulk nima?', 'a': [{'t': 'Aqliy mehnat mahsulotlari (patent, mualliflik huquqi)', 'c': True}, {'t': 'Faqat jismoniy mulk', 'c': False}, {'t': 'Faqat pul', 'c': False}, {'t': 'Faqat bino', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("🎓 IQTISOD FANI - 30 TA MAVZU QO'SHILMOQDA...")
    subj = get_or_create_economics()
    add_topics(subj, T)
    print(f"\n✅ Jami {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
    print("📊 Har bir mavzuda 5-10 ta test mavjud")
    print("🎯 Testlar to'g'ri javoblari har xil pozitsiyalarda")
    print("📚 Mavzular ketma-ket o'rgatib boradi")
