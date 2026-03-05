"""
LINUX COMANDALAR - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_linux():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Linux', defaults={'category': cat, 'description': 'Linux - Terminal va komandalar tizimi', 'icon': 'bi-terminal-fill', 'order': 26, 'is_active': True})
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
    {'n': 'Linux ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Linux nima?', 'a': [{'t': 'Bepul va ochiq kodli operatsion tizim', 'c': True}, {'t': 'Pullik operatsion tizim', 'c': False}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Linux ni kim yaratgan?', 'a': [{'t': 'Linus Torvalds', 'c': True}, {'t': 'Bill Gates', 'c': False}, {'t': 'Steve Jobs', 'c': False}, {'t': 'Mark Zuckerberg', 'c': False}]},
        {'t': 'Terminal nima?', 'a': [{'t': 'Komandalar yozish uchun interfeys', 'c': True}, {'t': 'Fayl menejeri', 'c': False}, {'t': 'Brauzer', 'c': False}, {'t': 'Matn muharriri', 'c': False}]},
        {'t': 'Shell nima?', 'a': [{'t': 'Komandalarni bajaradigan dastur', 'c': True}, {'t': 'Grafik interfeys', 'c': False}, {'t': 'Fayl tizimi', 'c': False}, {'t': 'Operatsion tizim', 'c': False}]},
        {'t': 'Bash nima?', 'a': [{'t': 'Eng mashhur Linux shell', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Fayl menejeri', 'c': False}, {'t': 'Brauzer', 'c': False}]},
    ]},

    {'n': 'pwd - Joriy papkani ko\'rish', 't': 15, 'o': 2, 'q': [
        {'t': 'pwd komandasi nima qiladi?', 'a': [{'t': 'Joriy papka yo\'lini ko\'rsatadi', 'c': True}, {'t': 'Parolni o\'zgartiradi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'pwd ning to\'liq nomi nima?', 'a': [{'t': 'Print Working Directory', 'c': True}, {'t': 'Password', 'c': False}, {'t': 'Power Directory', 'c': False}, {'t': 'Print Word Document', 'c': False}]},
        {'t': 'pwd komandasi qanday natija beradi?', 'a': [{'t': '/home/user kabi to\'liq yo\'l', 'c': True}, {'t': 'Fayllar ro\'yxati', 'c': False}, {'t': 'Parol', 'c': False}, {'t': 'Xato xabari', 'c': False}]},
        {'t': 'pwd komandasi parametr talab qiladimi?', 'a': [{'t': 'Yo\'q, parametrsiz ishlaydi', 'c': True}, {'t': 'Ha, papka nomi kerak', 'c': False}, {'t': 'Ha, fayl nomi kerak', 'c': False}, {'t': 'Ha, parol kerak', 'c': False}]},
        {'t': 'pwd qachon foydali?', 'a': [{'t': 'Qaysi papkada ekanligingizni bilish uchun', 'c': True}, {'t': 'Fayl yaratish uchun', 'c': False}, {'t': 'Parolni o\'zgartirish uchun', 'c': False}, {'t': 'Tizimni o\'chirish uchun', 'c': False}]},
    ]},

    {'n': 'ls - Fayllarni ko\'rish', 't': 25, 'o': 3, 'q': [
        {'t': 'ls komandasi nima qiladi?', 'a': [{'t': 'Joriy papkadagi fayllar va papkalarni ko\'rsatadi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'ls -l nima qiladi?', 'a': [{'t': 'Batafsil ma\'lumot bilan ko\'rsatadi', 'c': True}, {'t': 'Faqat papkalarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Yashirin fayllarni ko\'rsatadi', 'c': False}]},
        {'t': 'ls -a nima uchun ishlatiladi?', 'a': [{'t': 'Yashirin fayllarni ham ko\'rsatadi', 'c': True}, {'t': 'Fayllarni alifbo tartibida ko\'rsatadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni arxivlaydi', 'c': False}]},
        {'t': 'ls -h nima qiladi?', 'a': [{'t': 'Fayl hajmini odam tushunadigan formatda ko\'rsatadi', 'c': True}, {'t': 'Yordam ma\'lumotini ko\'rsatadi', 'c': False}, {'t': 'Yashirin fayllarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'ls -R nima qiladi?', 'a': [{'t': 'Barcha ichki papkalarni ham ko\'rsatadi', 'c': True}, {'t': 'Fayllarni qayta nomlaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'ls -t nima uchun?', 'a': [{'t': 'Fayllarni vaqt bo\'yicha tartiblaydi', 'c': True}, {'t': 'Fayllarni turi bo\'yicha ko\'rsatadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Matn fayllarini ko\'rsatadi', 'c': False}]},
        {'t': 'ls *.txt nima ko\'rsatadi?', 'a': [{'t': 'Faqat .txt kengaytmali fayllarni', 'c': True}, {'t': 'Barcha fayllarni', 'c': False}, {'t': 'Faqat papkalarni', 'c': False}, {'t': 'Yashirin fayllarni', 'c': False}]},
    ]},

    {'n': 'cd - Papkalar orasida harakatlanish', 't': 25, 'o': 4, 'q': [
        {'t': 'cd komandasi nima uchun ishlatiladi?', 'a': [{'t': 'Papkalar orasida o\'tish uchun', 'c': True}, {'t': 'Fayl yaratish uchun', 'c': False}, {'t': 'Faylni o\'chirish uchun', 'c': False}, {'t': 'Diskni formatlash uchun', 'c': False}]},
        {'t': 'cd .. komandasi nima qiladi?', 'a': [{'t': 'Bir daraja yuqori papkaga o\'tadi', 'c': True}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'cd / komandasi qayerga olib boradi?', 'a': [{'t': 'Ildiz (root) papkasiga', 'c': True}, {'t': 'Oldingi papkaga', 'c': False}, {'t': 'Uy papkasiga', 'c': False}, {'t': 'Desktop papkasiga', 'c': False}]},
        {'t': 'cd ~ komandasi nima qiladi?', 'a': [{'t': 'Uy (home) papkasiga o\'tadi', 'c': True}, {'t': 'Ildiz papkasiga o\'tadi', 'c': False}, {'t': 'Oldingi papkaga qaytadi', 'c': False}, {'t': 'Desktop ga o\'tadi', 'c': False}]},
        {'t': 'cd - komandasi nima qiladi?', 'a': [{'t': 'Oldingi papkaga qaytadi', 'c': True}, {'t': 'Ildiz papkasiga o\'tadi', 'c': False}, {'t': 'Uy papkasiga o\'tadi', 'c': False}, {'t': 'Papkani o\'chiradi', 'c': False}]},
        {'t': 'cd parametrsiz yozilsa nima bo\'ladi?', 'a': [{'t': 'Uy papkasiga o\'tadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Ildiz papkasiga o\'tadi', 'c': False}]},
    ]},

    {'n': 'mkdir - Papka yaratish', 't': 20, 'o': 5, 'q': [
        {'t': 'mkdir komandasi nima qiladi?', 'a': [{'t': 'Yangi papka yaratadi', 'c': True}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni ko\'chiradi', 'c': False}]},
        {'t': 'mkdir test komandasi nima qiladi?', 'a': [{'t': 'Joriy papkada "test" nomli papka yaratadi', 'c': True}, {'t': 'Test faylini yaratadi', 'c': False}, {'t': 'Test papkasini o\'chiradi', 'c': False}, {'t': 'Test papkasiga o\'tadi', 'c': False}]},
        {'t': 'mkdir -p nima uchun ishlatiladi?', 'a': [{'t': 'Kerakli ota-papkalarni ham yaratadi', 'c': True}, {'t': 'Parol so\'raydi', 'c': False}, {'t': 'Papkani yashiradi', 'c': False}, {'t': 'Papkani o\'chiradi', 'c': False}]},
        {'t': 'mkdir -p a/b/c nima qiladi?', 'a': [{'t': 'a, b va c papkalarini ketma-ket yaratadi', 'c': True}, {'t': 'Faqat c papkasini yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Barcha papkalarni o\'chiradi', 'c': False}]},
        {'t': 'mkdir "My Folder" qanday ishlaydi?', 'a': [{'t': 'Bo\'sh joylik nom uchun qo\'shtirnoq kerak', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Ikkita papka yaratadi', 'c': False}, {'t': 'Faqat birinchi so\'zni oladi', 'c': False}]},
    ]},

    {'n': 'rmdir va rm -r - Papka o\'chirish', 't': 25, 'o': 6, 'q': [
        {'t': 'rmdir komandasi nima qiladi?', 'a': [{'t': 'Bo\'sh papkani o\'chiradi', 'c': True}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'rmdir test komandasi bo\'sh bo\'lmagan papkani o\'chiradimi?', 'a': [{'t': 'Yo\'q, xato beradi', 'c': True}, {'t': 'Ha, o\'chiradi', 'c': False}, {'t': 'Faqat fayllarni o\'chiradi', 'c': False}, {'t': 'Tasdiqlash so\'raydi', 'c': False}]},
        {'t': 'rm -r nima qiladi?', 'a': [{'t': 'Papka va uning ichidagi barcha fayllarni o\'chiradi', 'c': True}, {'t': 'Faqat bo\'sh papkani o\'chiradi', 'c': False}, {'t': 'Papkani qayta nomlaydi', 'c': False}, {'t': 'Papkani ko\'chiradi', 'c': False}]},
        {'t': 'rm -rf nima uchun xavfli?', 'a': [{'t': 'Tasdiqlash so\'ramasdan hamma narsani o\'chiradi', 'c': True}, {'t': 'Tizimni buzadi', 'c': False}, {'t': 'Fayllarni shifrlaydi', 'c': False}, {'t': 'Xavfli emas', 'c': False}]},
        {'t': 'rm -r test/ nima qiladi?', 'a': [{'t': 'test papkasini va ichidagi hamma narsani o\'chiradi', 'c': True}, {'t': 'Faqat test papkasini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Papkani arxivlaydi', 'c': False}]},
        {'t': 'rm -i nima qiladi?', 'a': [{'t': 'Har bir fayl uchun tasdiqlash so\'raydi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Fayllarni yashiradi', 'c': False}, {'t': 'Fayllarni indekslaydi', 'c': False}]},
    ]},

    {'n': 'touch - Fayl yaratish', 't': 20, 'o': 7, 'q': [
        {'t': 'touch komandasi nima qiladi?', 'a': [{'t': 'Bo\'sh fayl yaratadi yoki fayl vaqtini yangilaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'touch file.txt nima qiladi?', 'a': [{'t': 'file.txt nomli bo\'sh fayl yaratadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni ochadi', 'c': False}, {'t': 'file.txt ni nusxalaydi', 'c': False}]},
        {'t': 'touch mavjud faylga qo\'llanilsa nima bo\'ladi?', 'a': [{'t': 'Fayl vaqti yangilanadi, mazmuni o\'zgarmaydi', 'c': True}, {'t': 'Fayl o\'chiriladi', 'c': False}, {'t': 'Fayl nusxalanadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'touch file1.txt file2.txt file3.txt nima qiladi?', 'a': [{'t': 'Uchta fayl yaratadi', 'c': True}, {'t': 'Faqat birinchi faylni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Fayllarni birlashtiradi', 'c': False}]},
        {'t': 'touch nima uchun foydali?', 'a': [{'t': 'Tez va oson fayl yaratish uchun', 'c': True}, {'t': 'Fayl mazmunini o\'zgartirish uchun', 'c': False}, {'t': 'Faylni o\'chirish uchun', 'c': False}, {'t': 'Papka yaratish uchun', 'c': False}]},
    ]},

    {'n': 'cp - Fayllarni nusxalash', 't': 30, 'o': 8, 'q': [
        {'t': 'cp komandasi nima qiladi?', 'a': [{'t': 'Fayllarni nusxalaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni ko\'chiradi', 'c': False}, {'t': 'Fayllarni yaratadi', 'c': False}]},
        {'t': 'cp file1.txt file2.txt nima qiladi?', 'a': [{'t': 'file1.txt ni file2.txt nomi bilan nusxalaydi', 'c': True}, {'t': 'Ikkala faylni o\'chiradi', 'c': False}, {'t': 'file2.txt ni file1.txt ga o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'cp file.txt /home/user/ nima qiladi?', 'a': [{'t': 'file.txt ni /home/user/ papkasiga nusxalaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'cp -r nima uchun ishlatiladi?', 'a': [{'t': 'Papkalarni nusxalash uchun', 'c': True}, {'t': 'Fayllarni qayta nomlash uchun', 'c': False}, {'t': 'Fayllarni o\'chirish uchun', 'c': False}, {'t': 'Fayllarni ko\'rish uchun', 'c': False}]},
        {'t': 'cp -i nima qiladi?', 'a': [{'t': 'Mavjud faylni almashtirish oldidan so\'raydi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Fayllarni yashiradi', 'c': False}, {'t': 'Fayllarni indekslaydi', 'c': False}]},
        {'t': 'cp *.txt backup/ nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni backup papkasiga nusxalaydi', 'c': True}, {'t': 'Faqat bitta faylni nusxalaydi', 'c': False}, {'t': 'Papkani nusxalaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'cp -v nima qiladi?', 'a': [{'t': 'Nusxalash jarayonini ko\'rsatadi', 'c': True}, {'t': 'Faylni tekshiradi', 'c': False}, {'t': 'Versiyani ko\'rsatadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
    ]},

    {'n': 'mv - Fayllarni ko\'chirish va qayta nomlash', 't': 25, 'o': 9, 'q': [
        {'t': 'mv komandasi nima qiladi?', 'a': [{'t': 'Fayllarni ko\'chiradi yoki qayta nomlaydi', 'c': True}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni yaratadi', 'c': False}]},
        {'t': 'mv va cp orasidagi farq nima?', 'a': [{'t': 'mv asl faylni o\'chiradi, cp esa saqlab qoladi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'cp tezroq ishlaydi', 'c': False}, {'t': 'mv faqat papkalar uchun', 'c': False}]},
        {'t': 'mv old.txt new.txt nima qiladi?', 'a': [{'t': 'old.txt ni new.txt ga qayta nomlaydi', 'c': True}, {'t': 'Ikkita fayl yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'mv file.txt /home/user/ nima qiladi?', 'a': [{'t': 'file.txt ni /home/user/ papkasiga ko\'chiradi', 'c': True}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'mv -i nima uchun?', 'a': [{'t': 'Mavjud faylni almashtirish oldidan so\'raydi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Faylni yashiradi', 'c': False}, {'t': 'Faylni indekslaydi', 'c': False}]},
        {'t': 'mv *.txt docs/ nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni docs papkasiga ko\'chiradi', 'c': True}, {'t': 'Faqat bitta faylni ko\'chiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'rm - Fayllarni o\'chirish', 't': 25, 'o': 10, 'q': [
        {'t': 'rm komandasi nima qiladi?', 'a': [{'t': 'Fayllarni o\'chiradi', 'c': True}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Fayllarni ko\'chiradi', 'c': False}]},
        {'t': 'rm file.txt nima qiladi?', 'a': [{'t': 'file.txt ni o\'chiradi', 'c': True}, {'t': 'file.txt ni nusxalaydi', 'c': False}, {'t': 'file.txt ni ochadi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}]},
        {'t': 'rm *.txt nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni o\'chiradi', 'c': True}, {'t': 'Faqat bitta faylni o\'chiradi', 'c': False}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'rm -i nima uchun?', 'a': [{'t': 'Har bir fayl uchun tasdiqlash so\'raydi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Fayllarni yashiradi', 'c': False}, {'t': 'Fayllarni indekslaydi', 'c': False}]},
        {'t': 'rm -f nima qiladi?', 'a': [{'t': 'Majburiy o\'chiradi, xato bermasdan', 'c': True}, {'t': 'Fayllarni topadi', 'c': False}, {'t': 'Fayllarni formatlaydi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'rm -v nima qiladi?', 'a': [{'t': 'O\'chirish jarayonini ko\'rsatadi', 'c': True}, {'t': 'Faylni tekshiradi', 'c': False}, {'t': 'Versiyani ko\'rsatadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'rm papkalarni o\'chiradimi?', 'a': [{'t': 'Yo\'q, -r parametri kerak', 'c': True}, {'t': 'Ha, o\'chiradi', 'c': False}, {'t': 'Faqat bo\'sh papkalarni', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'cat - Fayl mazmunini ko\'rish', 't': 20, 'o': 11, 'q': [
        {'t': 'cat komandasi nima qiladi?', 'a': [{'t': 'Fayl mazmunini ekranga chiqaradi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Fayl yaratadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'cat file.txt nima ko\'rsatadi?', 'a': [{'t': 'file.txt ning ichidagi matnni', 'c': True}, {'t': 'Fayl hajmini', 'c': False}, {'t': 'Fayl sanasini', 'c': False}, {'t': 'Fayl turini', 'c': False}]},
        {'t': 'cat qanday turdagi fayllar uchun mos?', 'a': [{'t': 'Matn fayllari uchun', 'c': True}, {'t': 'Rasm fayllari uchun', 'c': False}, {'t': 'Video fayllari uchun', 'c': False}, {'t': 'Arxiv fayllari uchun', 'c': False}]},
        {'t': 'cat file1.txt file2.txt nima qiladi?', 'a': [{'t': 'Ikkala faylning mazmunini ketma-ket ko\'rsatadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat birinchi faylni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni birlashtiradi', 'c': False}]},
        {'t': 'cat > file.txt nima qiladi?', 'a': [{'t': 'Yangi fayl yaratadi va matn yozish imkonini beradi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'less va more - Fayl mazmunini sahifalab ko\'rish', 't': 20, 'o': 12, 'q': [
        {'t': 'less komandasi nima qiladi?', 'a': [{'t': 'Fayl mazmunini sahifa-sahifa ko\'rsatadi', 'c': True}, {'t': 'Faylni kichiklashtiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'less va cat orasidagi farq?', 'a': [{'t': 'less sahifalab ko\'rsatadi, cat hammasi birdan', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'cat tezroq', 'c': False}, {'t': 'less faqat kichik fayllar uchun', 'c': False}]},
        {'t': 'less da qanday harakatlanish mumkin?', 'a': [{'t': 'Space - keyingi sahifa, b - oldingi sahifa, q - chiqish', 'c': True}, {'t': 'Faqat Enter bilan', 'c': False}, {'t': 'Faqat Esc bilan', 'c': False}, {'t': 'Harakatlanib bo\'lmaydi', 'c': False}]},
        {'t': 'less da qidirish qanday amalga oshiriladi?', 'a': [{'t': '/ belgisi va qidiruv so\'zi', 'c': True}, {'t': 'Ctrl+F', 'c': False}, {'t': 'Qidirish mumkin emas', 'c': False}, {'t': 'Alt+S', 'c': False}]},
        {'t': 'more va less orasidagi farq?', 'a': [{'t': 'less ko\'proq imkoniyatga ega (orqaga qaytish)', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'more yangi', 'c': False}, {'t': 'less eskirgan', 'c': False}]},
    ]},

    {'n': 'head va tail - Fayl boshi va oxiri', 't': 25, 'o': 13, 'q': [
        {'t': 'head komandasi nima qiladi?', 'a': [{'t': 'Fayl boshidan bir necha qatorni ko\'rsatadi', 'c': True}, {'t': 'Fayl oxirini ko\'rsatadi', 'c': False}, {'t': 'Fayl sarlavhasini o\'zgartiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'head file.txt standart necha qator ko\'rsatadi?', 'a': [{'t': '10 qator', 'c': True}, {'t': '5 qator', 'c': False}, {'t': '20 qator', 'c': False}, {'t': 'Barcha qatorlarni', 'c': False}]},
        {'t': 'head -n 5 file.txt nima qiladi?', 'a': [{'t': 'Birinchi 5 qatorni ko\'rsatadi', 'c': True}, {'t': 'Oxirgi 5 qatorni ko\'rsatadi', 'c': False}, {'t': '5-qatorni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'tail komandasi nima qiladi?', 'a': [{'t': 'Fayl oxiridan bir necha qatorni ko\'rsatadi', 'c': True}, {'t': 'Fayl boshini ko\'rsatadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'tail -f file.txt nima uchun foydali?', 'a': [{'t': 'Faylga yangi qo\'shilgan qatorlarni jonli ko\'rsatadi', 'c': True}, {'t': 'Faylni tez ko\'rsatadi', 'c': False}, {'t': 'Faylni formatlaydi', 'c': False}, {'t': 'Faylni topadi', 'c': False}]},
        {'t': 'tail -f qachon ishlatiladi?', 'a': [{'t': 'Log fayllarni kuzatish uchun', 'c': True}, {'t': 'Fayllarni o\'chirish uchun', 'c': False}, {'t': 'Fayllarni yaratish uchun', 'c': False}, {'t': 'Fayllarni nusxalash uchun', 'c': False}]},
    ]},

    {'n': 'grep - Matn qidirish', 't': 30, 'o': 14, 'q': [
        {'t': 'grep komandasi nima qiladi?', 'a': [{'t': 'Faylda matn qidiradi', 'c': True}, {'t': 'Fayl qidiradi', 'c': False}, {'t': 'Papka qidiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'grep "text" file.txt nima qiladi?', 'a': [{'t': 'file.txt da "text" so\'zini qidiradi', 'c': True}, {'t': 'text nomli faylni qidiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'grep -i nima uchun?', 'a': [{'t': 'Katta-kichik harfni farqlamasdan qidiradi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Indeks yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'grep -r "text" /path nima qiladi?', 'a': [{'t': 'Barcha ichki papkalarda ham qidiradi', 'c': True}, {'t': 'Fayllarni qayta nomlaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'grep -n "text" file.txt nima qiladi?', 'a': [{'t': 'Qator raqamlarini ham ko\'rsatadi', 'c': True}, {'t': 'Yangi fayl yaratadi', 'c': False}, {'t': 'Nomini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'grep -v "text" file.txt nima qiladi?', 'a': [{'t': '"text" yo\'q qatorlarni ko\'rsatadi', 'c': True}, {'t': 'Faylni tekshiradi', 'c': False}, {'t': 'Versiyani ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'grep -c "text" file.txt nima ko\'rsatadi?', 'a': [{'t': '"text" necha marta uchraganini', 'c': True}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'find - Fayl va papka qidirish', 't': 30, 'o': 15, 'q': [
        {'t': 'find komandasi nima qiladi?', 'a': [{'t': 'Fayl va papkalarni qidiradi', 'c': True}, {'t': 'Matn qidiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'find . -name "file.txt" nima qiladi?', 'a': [{'t': 'Joriy papkadan file.txt ni qidiradi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'find da . nima bildiradi?', 'a': [{'t': 'Joriy papka', 'c': True}, {'t': 'Ildiz papka', 'c': False}, {'t': 'Uy papkasi', 'c': False}, {'t': 'Barcha papkalar', 'c': False}]},
        {'t': 'find . -type f nima qiladi?', 'a': [{'t': 'Faqat fayllarni qidiradi', 'c': True}, {'t': 'Faqat papkalarni qidiradi', 'c': False}, {'t': 'Barcha narsani qidiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'find . -type d nima qiladi?', 'a': [{'t': 'Faqat papkalarni qidiradi', 'c': True}, {'t': 'Faqat fayllarni qidiradi', 'c': False}, {'t': 'Diskni qidiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'find . -name "*.txt" nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni qidiradi', 'c': True}, {'t': 'Faqat bitta faylni qidiradi', 'c': False}, {'t': 'Papkalarni qidiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'find . -size +10M nima qiladi?', 'a': [{'t': '10 MB dan katta fayllarni qidiradi', 'c': True}, {'t': '10 MB dan kichik fayllarni qidiradi', 'c': False}, {'t': 'Aniq 10 MB fayllarni qidiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'chmod - Fayl ruxsatlarini o\'zgartirish', 't': 30, 'o': 16, 'q': [
        {'t': 'chmod komandasi nima qiladi?', 'a': [{'t': 'Fayl ruxsatlarini o\'zgartiradi', 'c': True}, {'t': 'Fayl nomini o\'zgartiradi', 'c': False}, {'t': 'Fayl egasini o\'zgartiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'Linux da qanday ruxsatlar bor?', 'a': [{'t': 'Read (r), Write (w), Execute (x)', 'c': True}, {'t': 'Faqat Read va Write', 'c': False}, {'t': 'Open, Close, Delete', 'c': False}, {'t': 'View, Edit, Run', 'c': False}]},
        {'t': 'chmod +x file.sh nima qiladi?', 'a': [{'t': 'Faylni bajariluvchi qiladi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yashiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'chmod 755 file.sh nima bildiradi?', 'a': [{'t': 'Egasi: rwx, Guruh: r-x, Boshqalar: r-x', 'c': True}, {'t': 'Hammaga barcha ruxsat', 'c': False}, {'t': 'Hech kimga ruxsat yo\'q', 'c': False}, {'t': 'Faqat o\'qish ruxsati', 'c': False}]},
        {'t': 'chmod 644 file.txt nima bildiradi?', 'a': [{'t': 'Egasi: rw-, Guruh: r--, Boshqalar: r--', 'c': True}, {'t': 'Hammaga yozish ruxsati', 'c': False}, {'t': 'Hech kimga ruxsat yo\'q', 'c': False}, {'t': 'Faqat bajarish ruxsati', 'c': False}]},
        {'t': 'chmod -R nima uchun ishlatiladi?', 'a': [{'t': 'Barcha ichki fayllar va papkalarga qo\'llash uchun', 'c': True}, {'t': 'Ruxsatlarni o\'chirish uchun', 'c': False}, {'t': 'Fayllarni qayta nomlash uchun', 'c': False}, {'t': 'Fayllarni o\'chirish uchun', 'c': False}]},
        {'t': 'chmod 777 nima uchun xavfli?', 'a': [{'t': 'Hammaga barcha ruxsat beradi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xavfli emas', 'c': False}, {'t': 'Faylni yashiradi', 'c': False}]},
    ]},

    {'n': 'chown - Fayl egasini o\'zgartirish', 't': 20, 'o': 17, 'q': [
        {'t': 'chown komandasi nima qiladi?', 'a': [{'t': 'Fayl egasini o\'zgartiradi', 'c': True}, {'t': 'Fayl ruxsatlarini o\'zgartiradi', 'c': False}, {'t': 'Fayl nomini o\'zgartiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'chown user file.txt nima qiladi?', 'a': [{'t': 'file.txt egasini user ga o\'zgartiradi', 'c': True}, {'t': 'user nomli fayl yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'chown user:group file.txt nima qiladi?', 'a': [{'t': 'Egasi va guruhini o\'zgartiradi', 'c': True}, {'t': 'Faqat egasini o\'zgartiradi', 'c': False}, {'t': 'Faqat guruhini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'chown -R nima uchun?', 'a': [{'t': 'Barcha ichki fayllar va papkalarga qo\'llash uchun', 'c': True}, {'t': 'Fayllarni o\'chirish uchun', 'c': False}, {'t': 'Fayllarni qayta nomlash uchun', 'c': False}, {'t': 'Fayllarni nusxalash uchun', 'c': False}]},
        {'t': 'chown uchun qanday huquq kerak?', 'a': [{'t': 'Root yoki sudo huquqi', 'c': True}, {'t': 'Oddiy foydalanuvchi huquqi', 'c': False}, {'t': 'Hech qanday huquq kerak emas', 'c': False}, {'t': 'Faqat o\'qish huquqi', 'c': False}]},
    ]},

    {'n': 'tar - Arxivlash', 't': 30, 'o': 18, 'q': [
        {'t': 'tar komandasi nima qiladi?', 'a': [{'t': 'Fayllarni arxivlaydi va arxivdan chiqaradi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Fayllarni qidiradi', 'c': False}]},
        {'t': 'tar -czf archive.tar.gz folder/ nima qiladi?', 'a': [{'t': 'folder ni siqib arxivlaydi', 'c': True}, {'t': 'Arxivni ochadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'tar -xzf archive.tar.gz nima qiladi?', 'a': [{'t': 'Arxivni ochadi', 'c': True}, {'t': 'Arxiv yaratadi', 'c': False}, {'t': 'Arxivni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'tar da -c parametri nima uchun?', 'a': [{'t': 'Create - arxiv yaratish', 'c': True}, {'t': 'Copy - nusxalash', 'c': False}, {'t': 'Check - tekshirish', 'c': False}, {'t': 'Close - yopish', 'c': False}]},
        {'t': 'tar da -x parametri nima uchun?', 'a': [{'t': 'Extract - arxivdan chiqarish', 'c': True}, {'t': 'Exit - chiqish', 'c': False}, {'t': 'Execute - bajarish', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'tar da -z parametri nima qiladi?', 'a': [{'t': 'gzip bilan siqadi', 'c': True}, {'t': 'zip bilan siqadi', 'c': False}, {'t': 'Siqmaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'tar da -v parametri nima uchun?', 'a': [{'t': 'Verbose - jarayonni ko\'rsatadi', 'c': True}, {'t': 'Version - versiyani ko\'rsatadi', 'c': False}, {'t': 'Verify - tekshiradi', 'c': False}, {'t': 'View - ko\'rsatadi', 'c': False}]},
    ]},

    {'n': 'gzip va gunzip - Siqish', 't': 20, 'o': 19, 'q': [
        {'t': 'gzip komandasi nima qiladi?', 'a': [{'t': 'Fayllarni siqadi', 'c': True}, {'t': 'Fayllarni ochadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'gzip file.txt nima qiladi?', 'a': [{'t': 'file.txt ni siqib file.txt.gz yaratadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'gunzip file.txt.gz nima qiladi?', 'a': [{'t': 'file.txt.gz ni ochib file.txt yaratadi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'gzip asl faylni saqlab qoladimi?', 'a': [{'t': 'Yo\'q, asl faylni o\'chiradi', 'c': True}, {'t': 'Ha, saqlab qoladi', 'c': False}, {'t': 'Ba\'zan saqlab qoladi', 'c': False}, {'t': 'Parametrga bog\'liq', 'c': False}]},
        {'t': 'gzip -k nima qiladi?', 'a': [{'t': 'Asl faylni saqlab qoladi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'ps - Jarayonlarni ko\'rish', 't': 25, 'o': 20, 'q': [
        {'t': 'ps komandasi nima qiladi?', 'a': [{'t': 'Ishlab turgan jarayonlarni ko\'rsatadi', 'c': True}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Papkalarni ko\'rsatadi', 'c': False}, {'t': 'Parolni o\'zgartiradi', 'c': False}]},
        {'t': 'ps aux nima ko\'rsatadi?', 'a': [{'t': 'Barcha foydalanuvchilarning barcha jarayonlarini', 'c': True}, {'t': 'Faqat joriy foydalanuvchi jarayonlarini', 'c': False}, {'t': 'Faqat tizim jarayonlarini', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'ps da PID nima?', 'a': [{'t': 'Process ID - jarayon identifikatori', 'c': True}, {'t': 'Password ID', 'c': False}, {'t': 'Program ID', 'c': False}, {'t': 'Port ID', 'c': False}]},
        {'t': 'ps -ef nima qiladi?', 'a': [{'t': 'Barcha jarayonlarni to\'liq formatda ko\'rsatadi', 'c': True}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Xatolarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'ps | grep firefox nima qiladi?', 'a': [{'t': 'Firefox jarayonlarini qidiradi', 'c': True}, {'t': 'Firefox ni ishga tushiradi', 'c': False}, {'t': 'Firefox ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'kill - Jarayonni to\'xtatish', 't': 25, 'o': 21, 'q': [
        {'t': 'kill komandasi nima qiladi?', 'a': [{'t': 'Jarayonni to\'xtatadi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Dasturni ishga tushiradi', 'c': False}, {'t': 'Tizimni o\'chiradi', 'c': False}]},
        {'t': 'kill 1234 nima qiladi?', 'a': [{'t': 'PID 1234 bo\'lgan jarayonni to\'xtatadi', 'c': True}, {'t': '1234 nomli faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'kill -9 nima uchun ishlatiladi?', 'a': [{'t': 'Jarayonni majburiy to\'xtatadi', 'c': True}, {'t': '9 ta jarayonni to\'xtatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Jarayonni sekinlashtiradi', 'c': False}]},
        {'t': 'killall firefox nima qiladi?', 'a': [{'t': 'Barcha firefox jarayonlarini to\'xtatadi', 'c': True}, {'t': 'Faqat bitta firefox ni to\'xtatadi', 'c': False}, {'t': 'Firefox ni ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'pkill nima qiladi?', 'a': [{'t': 'Nom bo\'yicha jarayonni to\'xtatadi', 'c': True}, {'t': 'Paketlarni o\'chiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'top va htop - Tizim monitoringi', 't': 25, 'o': 22, 'q': [
        {'t': 'top komandasi nima qiladi?', 'a': [{'t': 'Jarayonlarni jonli rejimda ko\'rsatadi', 'c': True}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Papkalarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'top da q tugmasi nima qiladi?', 'a': [{'t': 'top dan chiqadi', 'c': True}, {'t': 'Jarayonni to\'xtatadi', 'c': False}, {'t': 'Tezroq yangilaydi', 'c': False}, {'t': 'Qidirish oynasini ochadi', 'c': False}]},
        {'t': 'top da k tugmasi nima qiladi?', 'a': [{'t': 'Jarayonni to\'xtatish uchun PID so\'raydi', 'c': True}, {'t': 'Klaviatura sozlamalarini ochadi', 'c': False}, {'t': 'top dan chiqadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'htop va top orasidagi farq?', 'a': [{'t': 'htop ko\'proq imkoniyatga ega va ranglirog', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'top yangi', 'c': False}, {'t': 'htop eskirgan', 'c': False}]},
        {'t': 'top da CPU foizi nima ko\'rsatadi?', 'a': [{'t': 'Jarayon qancha protsessor ishlatayotganini', 'c': True}, {'t': 'Disk ishlatilishini', 'c': False}, {'t': 'Xotira ishlatilishini', 'c': False}, {'t': 'Tarmoq tezligini', 'c': False}]},
    ]},

    {'n': 'df va du - Disk ma\'lumotlari', 't': 25, 'o': 23, 'q': [
        {'t': 'df komandasi nima qiladi?', 'a': [{'t': 'Disk bo\'sh joyini ko\'rsatadi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Diskni formatlaydi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'df -h nima qiladi?', 'a': [{'t': 'Odam tushunadigan formatda ko\'rsatadi (GB, MB)', 'c': True}, {'t': 'Yashirin disklarni ko\'rsatadi', 'c': False}, {'t': 'Yordam ma\'lumotini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'du komandasi nima qiladi?', 'a': [{'t': 'Fayl va papkalar hajmini ko\'rsatadi', 'c': True}, {'t': 'Diskni formatlaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'du -sh folder/ nima qiladi?', 'a': [{'t': 'folder hajmini umumiy ko\'rsatadi', 'c': True}, {'t': 'folder ni o\'chiradi', 'c': False}, {'t': 'folder ni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'df va du orasidagi farq?', 'a': [{'t': 'df disk bo\'sh joyini, du fayl hajmini ko\'rsatadi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'df tezroq', 'c': False}, {'t': 'du yangi', 'c': False}]},
    ]},

    {'n': 'wget - Fayllarni yuklab olish', 't': 25, 'o': 24, 'q': [
        {'t': 'wget komandasi nima qiladi?', 'a': [{'t': 'Internetdan fayl yuklab oladi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Fayllarni qidiradi', 'c': False}]},
        {'t': 'wget http://example.com/file.zip nima qiladi?', 'a': [{'t': 'file.zip ni yuklab oladi', 'c': True}, {'t': 'Saytni ochadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'wget -O newname.zip http://example.com/file.zip nima qiladi?', 'a': [{'t': 'Faylni newname.zip nomi bilan saqlaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni ochadi', 'c': False}]},
        {'t': 'wget -c nima uchun?', 'a': [{'t': 'To\'xtatilgan yuklanishni davom ettiradi', 'c': True}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'wget -b nima qiladi?', 'a': [{'t': 'Fonda (background) yuklab oladi', 'c': True}, {'t': 'Tezroq yuklab oladi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'curl - HTTP so\'rovlar', 't': 25, 'o': 25, 'q': [
        {'t': 'curl komandasi nima qiladi?', 'a': [{'t': 'HTTP so\'rovlar yuboradi va javobni oladi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'curl http://example.com nima qiladi?', 'a': [{'t': 'Sayt HTML kodini ko\'rsatadi', 'c': True}, {'t': 'Saytni brauzerda ochadi', 'c': False}, {'t': 'Saytni yuklab oladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'curl -O http://example.com/file.zip nima qiladi?', 'a': [{'t': 'Faylni asl nomi bilan yuklab oladi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni ochadi', 'c': False}]},
        {'t': 'curl va wget orasidagi farq?', 'a': [{'t': 'curl ko\'proq protokollarni qo\'llab-quvvatlaydi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'wget yangi', 'c': False}, {'t': 'curl eskirgan', 'c': False}]},
        {'t': 'curl -I http://example.com nima qiladi?', 'a': [{'t': 'Faqat HTTP headerlarni ko\'rsatadi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'ssh - Masofaviy ulanish', 't': 25, 'o': 26, 'q': [
        {'t': 'ssh komandasi nima qiladi?', 'a': [{'t': 'Masofaviy serverga xavfsiz ulanadi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'ssh user@192.168.1.100 nima qiladi?', 'a': [{'t': '192.168.1.100 serverga user sifatida ulanadi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'ssh ning to\'liq nomi nima?', 'a': [{'t': 'Secure Shell', 'c': True}, {'t': 'Super Shell', 'c': False}, {'t': 'System Shell', 'c': False}, {'t': 'Safe Shell', 'c': False}]},
        {'t': 'ssh -p 2222 user@server nima qiladi?', 'a': [{'t': '2222 portidan ulanadi', 'c': True}, {'t': 'Parolni o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'ssh dan chiqish uchun?', 'a': [{'t': 'exit yoki logout yozish', 'c': True}, {'t': 'Ctrl+C', 'c': False}, {'t': 'Alt+F4', 'c': False}, {'t': 'Esc', 'c': False}]},
    ]},

    {'n': 'scp - Masofaviy fayl nusxalash', 't': 25, 'o': 27, 'q': [
        {'t': 'scp komandasi nima qiladi?', 'a': [{'t': 'Masofaviy serverga/dan fayl nusxalaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Fayllarni qidiradi', 'c': False}]},
        {'t': 'scp file.txt user@server:/path nima qiladi?', 'a': [{'t': 'file.txt ni serverga nusxalaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni ochadi', 'c': False}]},
        {'t': 'scp user@server:/path/file.txt . nima qiladi?', 'a': [{'t': 'Serverdan faylni joriy papkaga nusxalaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'scp -r nima uchun?', 'a': [{'t': 'Papkalarni nusxalash uchun', 'c': True}, {'t': 'Fayllarni o\'chirish uchun', 'c': False}, {'t': 'Fayllarni qayta nomlash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'scp ning to\'liq nomi nima?', 'a': [{'t': 'Secure Copy', 'c': True}, {'t': 'Super Copy', 'c': False}, {'t': 'System Copy', 'c': False}, {'t': 'Safe Copy', 'c': False}]},
    ]},

    {'n': 'man va --help - Yordam', 't': 20, 'o': 28, 'q': [
        {'t': 'man komandasi nima qiladi?', 'a': [{'t': 'Komanda haqida qo\'llanma ko\'rsatadi', 'c': True}, {'t': 'Fayllarni boshqaradi', 'c': False}, {'t': 'Foydalanuvchilarni boshqaradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'man ls nima ko\'rsatadi?', 'a': [{'t': 'ls komandasi haqida to\'liq ma\'lumot', 'c': True}, {'t': 'Fayllar ro\'yxati', 'c': False}, {'t': 'Xato xabari', 'c': False}, {'t': 'Papkalar ro\'yxati', 'c': False}]},
        {'t': 'man ning to\'liq nomi nima?', 'a': [{'t': 'Manual', 'c': True}, {'t': 'Manager', 'c': False}, {'t': 'Manipulate', 'c': False}, {'t': 'Mandatory', 'c': False}]},
        {'t': 'ls --help nima qiladi?', 'a': [{'t': 'ls komandasi haqida qisqacha yordam ko\'rsatadi', 'c': True}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Papkalarni ko\'rsatadi', 'c': False}]},
        {'t': 'man va --help orasidagi farq?', 'a': [{'t': 'man to\'liqroq, --help qisqaroq', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': '--help to\'liqroq', 'c': False}, {'t': 'man eskirgan', 'c': False}]},
    ]},

    {'n': 'history - Komandalar tarixi', 't': 20, 'o': 29, 'q': [
        {'t': 'history komandasi nima qiladi?', 'a': [{'t': 'Oldingi komandalar tarixini ko\'rsatadi', 'c': True}, {'t': 'Fayllar tarixini ko\'rsatadi', 'c': False}, {'t': 'Tizim tarixini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': '!123 nima qiladi?', 'a': [{'t': 'Tarixdagi 123-komandani bajaradi', 'c': True}, {'t': '123 nomli faylni ochadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': '!! nima qiladi?', 'a': [{'t': 'Oxirgi komandani takrorlaydi', 'c': True}, {'t': 'Ikkita undov belgisi chiqaradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'history -c nima qiladi?', 'a': [{'t': 'Komandalar tarixini tozalaydi', 'c': True}, {'t': 'Tarixni nusxalaydi', 'c': False}, {'t': 'Tarixni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Ctrl+R nima qiladi?', 'a': [{'t': 'Tarixda qidirish', 'c': True}, {'t': 'Komandani takrorlash', 'c': False}, {'t': 'Terminaldan chiqish', 'c': False}, {'t': 'Faylni ochish', 'c': False}]},
    ]},

    {'n': 'alias - Qisqa komandalar yaratish', 't': 20, 'o': 30, 'q': [
        {'t': 'alias komandasi nima qiladi?', 'a': [{'t': 'Komanda uchun qisqa nom yaratadi', 'c': True}, {'t': 'Faylni qayta nomlaydi', 'c': False}, {'t': 'Foydalanuvchi yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'alias ll="ls -la" nima qiladi?', 'a': [{'t': 'll komandasi ls -la ni bajaradi', 'c': True}, {'t': 'll nomli fayl yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'alias parametrsiz yozilsa nima bo\'ladi?', 'a': [{'t': 'Barcha aliaslarni ko\'rsatadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Aliaslarni o\'chiradi', 'c': False}]},
        {'t': 'unalias ll nima qiladi?', 'a': [{'t': 'll aliasini o\'chiradi', 'c': True}, {'t': 'll faylini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Aliaslarni doimiy saqlash uchun qayerga yozish kerak?', 'a': [{'t': '~/.bashrc yoki ~/.bash_profile fayliga', 'c': True}, {'t': '/etc/alias fayliga', 'c': False}, {'t': '/var/alias fayliga', 'c': False}, {'t': 'Saqlab bo\'lmaydi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subject = get_or_create_linux()
    add_topics(subject, T)
    print(f"\n✅ {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
