"""
CMD KOMANDALAR - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_cmd():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='CMD', defaults={'category': cat, 'description': 'CMD - Windows Command Prompt komandalar tizimi', 'icon': 'bi-terminal', 'order': 25, 'is_active': True})
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
    {'n': 'CMD ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'CMD nima?', 'a': [{'t': 'Windows operatsion tizimida komandalar yozish uchun dastur', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Brauzer', 'c': False}, {'t': 'Antivirus dastur', 'c': False}]},
        {'t': 'CMD ni qanday ochish mumkin?', 'a': [{'t': 'Win+R tugmalarini bosib "cmd" yozish', 'c': True}, {'t': 'Ctrl+Alt+Del bosish', 'c': False}, {'t': 'Alt+Tab bosish', 'c': False}, {'t': 'Win+E bosish', 'c': False}]},
        {'t': 'CMD qaysi operatsion tizimda ishlaydi?', 'a': [{'t': 'Windows', 'c': True}, {'t': 'Linux', 'c': False}, {'t': 'MacOS', 'c': False}, {'t': 'Android', 'c': False}]},
        {'t': 'CMD ning to\'liq nomi nima?', 'a': [{'t': 'Command Prompt', 'c': True}, {'t': 'Computer Management Device', 'c': False}, {'t': 'Control Main Directory', 'c': False}, {'t': 'Command Mode Display', 'c': False}]},
        {'t': 'CMD oynasida matn rangi odatda qanday?', 'a': [{'t': 'Oq matn, qora fon', 'c': True}, {'t': 'Qora matn, oq fon', 'c': False}, {'t': 'Ko\'k matn, sariq fon', 'c': False}, {'t': 'Yashil matn, qizil fon', 'c': False}]},
    ]},

    {'n': 'DIR - Fayllarni ko\'rish', 't': 25, 'o': 2, 'q': [
        {'t': 'DIR komandasi nima qiladi?', 'a': [{'t': 'Joriy papkadagi fayllar va papkalarni ko\'rsatadi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'DIR /w komandasi nima uchun ishlatiladi?', 'a': [{'t': 'Fayllarni keng formatda (wide) ko\'rsatish', 'c': True}, {'t': 'Fayllarni o\'chirish', 'c': False}, {'t': 'Fayllarni yashirish', 'c': False}, {'t': 'Fayllarni saralash', 'c': False}]},
        {'t': 'DIR /p nima qiladi?', 'a': [{'t': 'Natijalarni sahifa-sahifa ko\'rsatadi', 'c': True}, {'t': 'Fayllarni print qiladi', 'c': False}, {'t': 'Fayllarni paketlaydi', 'c': False}, {'t': 'Fayllarni parallel ko\'rsatadi', 'c': False}]},
        {'t': 'DIR /a komandasi nima uchun?', 'a': [{'t': 'Barcha fayllarni (yashirin ham) ko\'rsatadi', 'c': True}, {'t': 'Faqat arxiv fayllarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni alifbo tartibida ko\'rsatadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'DIR /s nima uchun ishlatiladi?', 'a': [{'t': 'Barcha ichki papkalarni ham ko\'rsatadi', 'c': True}, {'t': 'Fayllarni saqlaydi', 'c': False}, {'t': 'Fayllarni qidiradi', 'c': False}, {'t': 'Fayllarni sortlaydi', 'c': False}]},
        {'t': 'DIR /o:n komandasi nima qiladi?', 'a': [{'t': 'Fayllarni nom bo\'yicha tartiblaydi', 'c': True}, {'t': 'Fayllarni ochadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'DIR *.txt nima ko\'rsatadi?', 'a': [{'t': 'Faqat .txt kengaytmali fayllarni', 'c': True}, {'t': 'Barcha fayllarni', 'c': False}, {'t': 'Faqat papkalarni', 'c': False}, {'t': 'Faqat yashirin fayllarni', 'c': False}]},
    ]},

    {'n': 'CD - Papkalar orasida harakatlanish', 't': 25, 'o': 3, 'q': [
        {'t': 'CD komandasi nima uchun ishlatiladi?', 'a': [{'t': 'Papkalar orasida o\'tish uchun', 'c': True}, {'t': 'Fayl yaratish uchun', 'c': False}, {'t': 'Faylni o\'chirish uchun', 'c': False}, {'t': 'Diskni formatlash uchun', 'c': False}]},
        {'t': 'CD.. komandasi nima qiladi?', 'a': [{'t': 'Bir daraja yuqori papkaga o\'tadi', 'c': True}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'CD \\ komandasi qayerga olib boradi?', 'a': [{'t': 'Diskning ildiz papkasiga', 'c': True}, {'t': 'Oldingi papkaga', 'c': False}, {'t': 'Desktop papkasiga', 'c': False}, {'t': 'Documents papkasiga', 'c': False}]},
        {'t': 'CD /d D:\\ komandasi nima qiladi?', 'a': [{'t': 'D: diskiga o\'tadi', 'c': True}, {'t': 'D: diskini o\'chiradi', 'c': False}, {'t': 'D: diskini formatlaydi', 'c': False}, {'t': 'D: diskini nusxalaydi', 'c': False}]},
        {'t': 'CD komandasi parametrsiz yozilsa nima ko\'rsatadi?', 'a': [{'t': 'Joriy papka yo\'lini', 'c': True}, {'t': 'Barcha papkalarni', 'c': False}, {'t': 'Barcha fayllarni', 'c': False}, {'t': 'Disk hajmini', 'c': False}]},
        {'t': 'CD "My Documents" qanday ishlaydi?', 'a': [{'t': 'Bo\'sh joy bor papka nomini qo\'shtirnoqda yozish kerak', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat birinchi so\'zni o\'qiydi', 'c': False}, {'t': 'Papkani o\'chiradi', 'c': False}]},
    ]},

    {'n': 'MD va MKDIR - Papka yaratish', 't': 20, 'o': 4, 'q': [
        {'t': 'MD komandasi nima qiladi?', 'a': [{'t': 'Yangi papka yaratadi', 'c': True}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni ko\'chiradi', 'c': False}]},
        {'t': 'MD va MKDIR komandalarida qanday farq bor?', 'a': [{'t': 'Farq yo\'q, ikkalasi ham bir xil', 'c': True}, {'t': 'MD tezroq ishlaydi', 'c': False}, {'t': 'MKDIR ko\'proq imkoniyatga ega', 'c': False}, {'t': 'MD faqat Windows 10 da ishlaydi', 'c': False}]},
        {'t': 'MD test komandasi nima qiladi?', 'a': [{'t': 'Joriy papkada "test" nomli papka yaratadi', 'c': True}, {'t': 'Test faylini yaratadi', 'c': False}, {'t': 'Test papkasini o\'chiradi', 'c': False}, {'t': 'Test papkasiga o\'tadi', 'c': False}]},
        {'t': 'MD C:\\Users\\test komandasi nima qiladi?', 'a': [{'t': 'To\'liq yo\'l bo\'yicha papka yaratadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat test papkasini yaratadi', 'c': False}, {'t': 'Barcha papkalarni o\'chiradi', 'c': False}]},
        {'t': 'MD "My Folder" qanday ishlaydi?', 'a': [{'t': 'Bo\'sh joylik nom uchun qo\'shtirnoq kerak', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Ikkita papka yaratadi', 'c': False}, {'t': 'Faqat birinchi so\'zni oladi', 'c': False}]},
    ]},

    {'n': 'RD va RMDIR - Papka o\'chirish', 't': 25, 'o': 5, 'q': [
        {'t': 'RD komandasi nima qiladi?', 'a': [{'t': 'Papkani o\'chiradi', 'c': True}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'RD /s nima uchun ishlatiladi?', 'a': [{'t': 'Papka va uning ichidagi barcha fayllarni o\'chiradi', 'c': True}, {'t': 'Faqat bo\'sh papkani o\'chiradi', 'c': False}, {'t': 'Papkani saqlaydi', 'c': False}, {'t': 'Papkani ko\'chiradi', 'c': False}]},
        {'t': 'RD /q parametri nima qiladi?', 'a': [{'t': 'Tasdiqlash so\'ramasdan o\'chiradi', 'c': True}, {'t': 'Tezroq o\'chiradi', 'c': False}, {'t': 'Sifatli o\'chiradi', 'c': False}, {'t': 'Quiet rejimda ishlaydi', 'c': False}]},
        {'t': 'RD test komandasi bo\'sh bo\'lmagan papkani o\'chiradimi?', 'a': [{'t': 'Yo\'q, xato beradi', 'c': True}, {'t': 'Ha, o\'chiradi', 'c': False}, {'t': 'Faqat fayllarni o\'chiradi', 'c': False}, {'t': 'Tasdiqlash so\'raydi', 'c': False}]},
        {'t': 'RD /s /q test komandasi nima qiladi?', 'a': [{'t': 'Test papkasini va ichidagi hamma narsani so\'ramasdan o\'chiradi', 'c': True}, {'t': 'Faqat test papkasini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Papkani arxivlaydi', 'c': False}]},
        {'t': 'RMDIR va RD orasida qanday farq bor?', 'a': [{'t': 'Farq yo\'q, ikkalasi ham bir xil', 'c': True}, {'t': 'RMDIR xavflirog', 'c': False}, {'t': 'RD tezroq ishlaydi', 'c': False}, {'t': 'RMDIR faqat bo\'sh papkalarni o\'chiradi', 'c': False}]},
    ]},

    {'n': 'COPY - Fayllarni nusxalash', 't': 30, 'o': 6, 'q': [
        {'t': 'COPY komandasi nima qiladi?', 'a': [{'t': 'Fayllarni nusxalaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni ko\'chiradi', 'c': False}, {'t': 'Fayllarni yaratadi', 'c': False}]},
        {'t': 'COPY file1.txt file2.txt nima qiladi?', 'a': [{'t': 'file1.txt ni file2.txt nomi bilan nusxalaydi', 'c': True}, {'t': 'Ikkala faylni o\'chiradi', 'c': False}, {'t': 'file2.txt ni file1.txt ga o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'COPY *.txt D:\\backup nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni D:\\backup ga nusxalaydi', 'c': True}, {'t': 'Faqat bitta faylni nusxalaydi', 'c': False}, {'t': 'Papkani nusxalaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'COPY /y parametri nima uchun?', 'a': [{'t': 'Mavjud faylni so\'ramasdan almashtiradi', 'c': True}, {'t': 'Faylni yashiradi', 'c': False}, {'t': 'Faylni siqadi', 'c': False}, {'t': 'Faylni shifrlaydi', 'c': False}]},
        {'t': 'COPY /v nima qiladi?', 'a': [{'t': 'Nusxalangan faylni tekshiradi', 'c': True}, {'t': 'Faylni ko\'rsatadi', 'c': False}, {'t': 'Faylni versiyalaydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'COPY file1.txt+file2.txt file3.txt nima qiladi?', 'a': [{'t': 'Ikkita faylni birlashtirib file3.txt yaratadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat file1.txt ni nusxalaydi', 'c': False}, {'t': 'Barcha fayllarni o\'chiradi', 'c': False}]},
        {'t': 'COPY papkalarni nusxalaydi?', 'a': [{'t': 'Yo\'q, faqat fayllarni nusxalaydi', 'c': True}, {'t': 'Ha, papkalarni ham nusxalaydi', 'c': False}, {'t': 'Faqat bo\'sh papkalarni', 'c': False}, {'t': 'Faqat /s parametri bilan', 'c': False}]},
    ]},

    {'n': 'XCOPY - Kengaytirilgan nusxalash', 't': 30, 'o': 7, 'q': [
        {'t': 'XCOPY va COPY orasidagi asosiy farq nima?', 'a': [{'t': 'XCOPY papkalarni ham nusxalaydi', 'c': True}, {'t': 'COPY tezroq ishlaydi', 'c': False}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'XCOPY faqat matn fayllarini nusxalaydi', 'c': False}]},
        {'t': 'XCOPY /s parametri nima qiladi?', 'a': [{'t': 'Barcha ichki papkalarni ham nusxalaydi', 'c': True}, {'t': 'Fayllarni siqadi', 'c': False}, {'t': 'Fayllarni saqlaydi', 'c': False}, {'t': 'Fayllarni sortlaydi', 'c': False}]},
        {'t': 'XCOPY /e nima uchun ishlatiladi?', 'a': [{'t': 'Bo\'sh papkalarni ham nusxalaydi', 'c': True}, {'t': 'Fayllarni shifrlaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xatolarni ko\'rsatadi', 'c': False}]},
        {'t': 'XCOPY /i parametri nima qiladi?', 'a': [{'t': 'Manzil papka bo\'lsa, uni yaratadi', 'c': True}, {'t': 'Fayllarni indekslaydi', 'c': False}, {'t': 'Ma\'lumotlarni import qiladi', 'c': False}, {'t': 'Fayllarni siqadi', 'c': False}]},
        {'t': 'XCOPY /d:12-31-2023 nima qiladi?', 'a': [{'t': 'Faqat ko\'rsatilgan sanadan keyin o\'zgargan fayllarni nusxalaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Sanani o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'XCOPY /h nima uchun?', 'a': [{'t': 'Yashirin va tizim fayllarini ham nusxalaydi', 'c': True}, {'t': 'Yordam ma\'lumotini ko\'rsatadi', 'c': False}, {'t': 'Fayllarni yashiradi', 'c': False}, {'t': 'Fayllarni siqadi', 'c': False}]},
        {'t': 'XCOPY /y parametri nima qiladi?', 'a': [{'t': 'Mavjud fayllarni so\'ramasdan almashtiradi', 'c': True}, {'t': 'Fayllarni yashiradi', 'c': False}, {'t': 'Fayllarni siqadi', 'c': False}, {'t': 'Fayllarni shifrlaydi', 'c': False}]},
    ]},

    {'n': 'MOVE - Fayllarni ko\'chirish', 't': 25, 'o': 8, 'q': [
        {'t': 'MOVE komandasi nima qiladi?', 'a': [{'t': 'Fayllarni bir joydan boshqa joyga ko\'chiradi', 'c': True}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Fayllarni yaratadi', 'c': False}]},
        {'t': 'MOVE va COPY orasidagi farq nima?', 'a': [{'t': 'MOVE asl faylni o\'chiradi, COPY esa saqlab qoladi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'COPY tezroq ishlaydi', 'c': False}, {'t': 'MOVE faqat papkalar uchun', 'c': False}]},
        {'t': 'MOVE file.txt D:\\backup nima qiladi?', 'a': [{'t': 'file.txt ni D:\\backup papkasiga ko\'chiradi', 'c': True}, {'t': 'file.txt ni nusxalaydi', 'c': False}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'MOVE oldname.txt newname.txt nima qiladi?', 'a': [{'t': 'Faylni qayta nomlaydi', 'c': True}, {'t': 'Ikkita fayl yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'MOVE /y parametri nima uchun?', 'a': [{'t': 'Mavjud faylni so\'ramasdan almashtiradi', 'c': True}, {'t': 'Faylni yashiradi', 'c': False}, {'t': 'Faylni siqadi', 'c': False}, {'t': 'Faylni shifrlaydi', 'c': False}]},
        {'t': 'MOVE *.txt D:\\docs nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni D:\\docs ga ko\'chiradi', 'c': True}, {'t': 'Faqat bitta faylni ko\'chiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'DEL va ERASE - Fayllarni o\'chirish', 't': 25, 'o': 9, 'q': [
        {'t': 'DEL komandasi nima qiladi?', 'a': [{'t': 'Fayllarni o\'chiradi', 'c': True}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Fayllarni ko\'chiradi', 'c': False}]},
        {'t': 'DEL va ERASE orasida qanday farq bor?', 'a': [{'t': 'Farq yo\'q, ikkalasi ham bir xil', 'c': True}, {'t': 'DEL xavflirog', 'c': False}, {'t': 'ERASE tezroq ishlaydi', 'c': False}, {'t': 'DEL papkalarni ham o\'chiradi', 'c': False}]},
        {'t': 'DEL *.txt nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarni o\'chiradi', 'c': True}, {'t': 'Faqat bitta faylni o\'chiradi', 'c': False}, {'t': 'Papkani o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'DEL /p parametri nima uchun?', 'a': [{'t': 'Har bir fayl uchun tasdiqlash so\'raydi', 'c': True}, {'t': 'Fayllarni print qiladi', 'c': False}, {'t': 'Fayllarni paketlaydi', 'c': False}, {'t': 'Fayllarni parallel o\'chiradi', 'c': False}]},
        {'t': 'DEL /f nima qiladi?', 'a': [{'t': 'Faqat o\'qish uchun fayllarni ham o\'chiradi', 'c': True}, {'t': 'Fayllarni tez o\'chiradi', 'c': False}, {'t': 'Fayllarni formatlaydi', 'c': False}, {'t': 'Fayllarni topadi', 'c': False}]},
        {'t': 'DEL /s nima uchun ishlatiladi?', 'a': [{'t': 'Barcha ichki papkalardagi fayllarni ham o\'chiradi', 'c': True}, {'t': 'Fayllarni saqlaydi', 'c': False}, {'t': 'Fayllarni sortlaydi', 'c': False}, {'t': 'Fayllarni qidiradi', 'c': False}]},
        {'t': 'DEL /q parametri nima qiladi?', 'a': [{'t': 'Tasdiqlash so\'ramasdan o\'chiradi', 'c': True}, {'t': 'Tezroq o\'chiradi', 'c': False}, {'t': 'Sifatli o\'chiradi', 'c': False}, {'t': 'Quiet rejimda ishlaydi', 'c': False}]},
    ]},

    {'n': 'REN va RENAME - Qayta nomlash', 't': 20, 'o': 10, 'q': [
        {'t': 'REN komandasi nima qiladi?', 'a': [{'t': 'Fayl yoki papkani qayta nomlaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni ko\'chiradi', 'c': False}]},
        {'t': 'REN va RENAME orasida farq bormi?', 'a': [{'t': 'Yo\'q, ikkalasi ham bir xil', 'c': True}, {'t': 'Ha, RENAME ko\'proq imkoniyatga ega', 'c': False}, {'t': 'REN tezroq ishlaydi', 'c': False}, {'t': 'RENAME faqat papkalar uchun', 'c': False}]},
        {'t': 'REN old.txt new.txt nima qiladi?', 'a': [{'t': 'old.txt ni new.txt ga o\'zgartiradi', 'c': True}, {'t': 'Ikkita fayl yaratadi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'REN *.txt *.bak nima qiladi?', 'a': [{'t': 'Barcha .txt fayllarning kengaytmasini .bak ga o\'zgartiradi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'REN bilan faylni boshqa papkaga ko\'chirish mumkinmi?', 'a': [{'t': 'Yo\'q, faqat nom o\'zgartirish mumkin', 'c': True}, {'t': 'Ha, mumkin', 'c': False}, {'t': 'Faqat /m parametri bilan', 'c': False}, {'t': 'Faqat administrator huquqi bilan', 'c': False}]},
    ]},

    {'n': 'TYPE - Fayl mazmunini ko\'rish', 't': 20, 'o': 11, 'q': [
        {'t': 'TYPE komandasi nima qiladi?', 'a': [{'t': 'Fayl mazmunini ekranga chiqaradi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Fayl turini aniqlaydi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'TYPE file.txt nima ko\'rsatadi?', 'a': [{'t': 'file.txt ning ichidagi matnni', 'c': True}, {'t': 'Fayl hajmini', 'c': False}, {'t': 'Fayl sanasini', 'c': False}, {'t': 'Fayl turini', 'c': False}]},
        {'t': 'TYPE qanday turdagi fayllar uchun mos?', 'a': [{'t': 'Matn fayllari uchun', 'c': True}, {'t': 'Rasm fayllari uchun', 'c': False}, {'t': 'Video fayllari uchun', 'c': False}, {'t': 'Arxiv fayllari uchun', 'c': False}]},
        {'t': 'TYPE file1.txt file2.txt nima qiladi?', 'a': [{'t': 'Ikkala faylning mazmunini ketma-ket ko\'rsatadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat birinchi faylni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni birlashtiradi', 'c': False}]},
        {'t': 'TYPE file.txt | MORE nima qiladi?', 'a': [{'t': 'Matnni sahifa-sahifa ko\'rsatadi', 'c': True}, {'t': 'Ko\'proq ma\'lumot qo\'shadi', 'c': False}, {'t': 'Faylni kattalashtiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'CLS - Ekranni tozalash', 't': 15, 'o': 12, 'q': [
        {'t': 'CLS komandasi nima qiladi?', 'a': [{'t': 'CMD ekranini tozalaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Papkalarni tozalaydi', 'c': False}, {'t': 'Diskni tozalaydi', 'c': False}]},
        {'t': 'CLS ning to\'liq nomi nima?', 'a': [{'t': 'Clear Screen', 'c': True}, {'t': 'Close System', 'c': False}, {'t': 'Clean Storage', 'c': False}, {'t': 'Clear System', 'c': False}]},
        {'t': 'CLS komandasi fayllarni o\'chiradimi?', 'a': [{'t': 'Yo\'q, faqat ekranni tozalaydi', 'c': True}, {'t': 'Ha, barcha fayllarni o\'chiradi', 'c': False}, {'t': 'Faqat vaqtinchalik fayllarni', 'c': False}, {'t': 'Faqat yashirin fayllarni', 'c': False}]},
        {'t': 'CLS dan keyin oldingi komandalar yo\'qoladimi?', 'a': [{'t': 'Yo\'q, faqat ekrandan yo\'qoladi, tarixda qoladi', 'c': True}, {'t': 'Ha, butunlay yo\'qoladi', 'c': False}, {'t': 'Faqat oxirgi komanda yo\'qoladi', 'c': False}, {'t': 'Hech narsa yo\'qolmaydi', 'c': False}]},
        {'t': 'CLS komandasi qaysi tugma bilan almashtirilishi mumkin?', 'a': [{'t': 'Hech qaysi tugma bilan almashtirib bo\'lmaydi', 'c': True}, {'t': 'Ctrl+L', 'c': False}, {'t': 'Ctrl+C', 'c': False}, {'t': 'Alt+C', 'c': False}]},
    ]},

    {'n': 'ECHO - Matn chiqarish', 't': 25, 'o': 13, 'q': [
        {'t': 'ECHO komandasi nima qiladi?', 'a': [{'t': 'Matnni ekranga chiqaradi', 'c': True}, {'t': 'Ovozni chiqaradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'ECHO Hello World nima qiladi?', 'a': [{'t': 'Ekranga "Hello World" yozadi', 'c': True}, {'t': 'Hello World nomli fayl yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'ECHO OFF nima qiladi?', 'a': [{'t': 'Komandalarni ekranga chiqarishni o\'chiradi', 'c': True}, {'t': 'CMD ni yopadi', 'c': False}, {'t': 'Ovozni o\'chiradi', 'c': False}, {'t': 'Ekranni o\'chiradi', 'c': False}]},
        {'t': 'ECHO ON nima uchun ishlatiladi?', 'a': [{'t': 'Komandalarni ekranga chiqarishni yoqadi', 'c': True}, {'t': 'CMD ni yoqadi', 'c': False}, {'t': 'Ovozni yoqadi', 'c': False}, {'t': 'Ekranni yoqadi', 'c': False}]},
        {'t': 'ECHO. nima qiladi?', 'a': [{'t': 'Bo\'sh qator chiqaradi', 'c': True}, {'t': 'Nuqta chiqaradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'ECHO %DATE% nima ko\'rsatadi?', 'a': [{'t': 'Joriy sanani', 'c': True}, {'t': '%DATE% matnini', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Fayl sanasini', 'c': False}]},
        {'t': 'ECHO text > file.txt nima qiladi?', 'a': [{'t': 'text ni file.txt ga yozadi', 'c': True}, {'t': 'Ekranga chiqaradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
    ]},

    {'n': 'PAUSE - To\'xtatish', 't': 15, 'o': 14, 'q': [
        {'t': 'PAUSE komandasi nima qiladi?', 'a': [{'t': 'Dasturni to\'xtatadi va tugma bosishni kutadi', 'c': True}, {'t': 'CMD ni yopadi', 'c': False}, {'t': 'Faylni to\'xtatadi', 'c': False}, {'t': 'Vaqtni to\'xtatadi', 'c': False}]},
        {'t': 'PAUSE qanday xabar ko\'rsatadi?', 'a': [{'t': 'Press any key to continue...', 'c': True}, {'t': 'Wait please...', 'c': False}, {'t': 'Paused', 'c': False}, {'t': 'Stop', 'c': False}]},
        {'t': 'PAUSE dan keyin qaysi tugmani bosish kerak?', 'a': [{'t': 'Istalgan tugmani', 'c': True}, {'t': 'Faqat Enter', 'c': False}, {'t': 'Faqat Space', 'c': False}, {'t': 'Faqat Esc', 'c': False}]},
        {'t': 'PAUSE nima uchun ishlatiladi?', 'a': [{'t': 'Foydalanuvchi natijani ko\'rishi uchun', 'c': True}, {'t': 'Tizimni to\'xtatish uchun', 'c': False}, {'t': 'Faylni saqlash uchun', 'c': False}, {'t': 'Xotira tozalash uchun', 'c': False}]},
        {'t': 'PAUSE > nul nima qiladi?', 'a': [{'t': 'Xabar ko\'rsatmasdan kutadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'To\'xtatmaydi', 'c': False}, {'t': 'Faylga yozadi', 'c': False}]},
    ]},

    {'n': 'EXIT - CMD dan chiqish', 't': 15, 'o': 15, 'q': [
        {'t': 'EXIT komandasi nima qiladi?', 'a': [{'t': 'CMD oynasini yopadi', 'c': True}, {'t': 'Kompyuterni o\'chiradi', 'c': False}, {'t': 'Faylni yopadi', 'c': False}, {'t': 'Dasturni o\'chiradi', 'c': False}]},
        {'t': 'EXIT /b nima qiladi?', 'a': [{'t': 'Faqat batch fayldan chiqadi, CMD ni yopmaydi', 'c': True}, {'t': 'CMD ni yopadi', 'c': False}, {'t': 'Kompyuterni qayta ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'EXIT 0 dagi 0 nima?', 'a': [{'t': 'Chiqish kodi (exit code)', 'c': True}, {'t': 'Vaqt', 'c': False}, {'t': 'Fayl raqami', 'c': False}, {'t': 'Xato kodi', 'c': False}]},
        {'t': 'EXIT dan keyin CMD oynasi nima bo\'ladi?', 'a': [{'t': 'Yopiladi', 'c': True}, {'t': 'Minimallashadi', 'c': False}, {'t': 'Tozalanadi', 'c': False}, {'t': 'Qayta ishga tushadi', 'c': False}]},
        {'t': 'EXIT ni qaysi tugmalar bilan almashtirish mumkin?', 'a': [{'t': 'Alt+F4 yoki X tugmasi', 'c': True}, {'t': 'Ctrl+C', 'c': False}, {'t': 'Esc', 'c': False}, {'t': 'Ctrl+Z', 'c': False}]},
    ]},

    {'n': 'ATTRIB - Fayl atributlari', 't': 30, 'o': 16, 'q': [
        {'t': 'ATTRIB komandasi nima qiladi?', 'a': [{'t': 'Fayl atributlarini ko\'rsatadi yoki o\'zgartiradi', 'c': True}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}]},
        {'t': 'ATTRIB +h file.txt nima qiladi?', 'a': [{'t': 'Faylni yashiradi', 'c': True}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni himoyalaydi', 'c': False}]},
        {'t': 'ATTRIB -h file.txt nima qiladi?', 'a': [{'t': 'Faylni ko\'rinadigan qiladi', 'c': True}, {'t': 'Faylni yashiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'ATTRIB +r file.txt nima uchun?', 'a': [{'t': 'Faylni faqat o\'qish uchun qiladi', 'c': True}, {'t': 'Faylni o\'qiydi', 'c': False}, {'t': 'Faylni qayta nomlaydi', 'c': False}, {'t': 'Faylni qayta yozadi', 'c': False}]},
        {'t': 'ATTRIB +s file.txt nima qiladi?', 'a': [{'t': 'Faylni tizim fayli qiladi', 'c': True}, {'t': 'Faylni saqlaydi', 'c': False}, {'t': 'Faylni qidiradi', 'c': False}, {'t': 'Faylni sortlaydi', 'c': False}]},
        {'t': 'ATTRIB +a file.txt nima uchun?', 'a': [{'t': 'Arxiv atributini qo\'yadi', 'c': True}, {'t': 'Faylni arxivlaydi', 'c': False}, {'t': 'Faylni ochadi', 'c': False}, {'t': 'Faylni qo\'shadi', 'c': False}]},
        {'t': 'ATTRIB /s parametri nima qiladi?', 'a': [{'t': 'Barcha ichki papkalarga ham qo\'llaydi', 'c': True}, {'t': 'Faylni saqlaydi', 'c': False}, {'t': 'Faylni qidiradi', 'c': False}, {'t': 'Faylni sortlaydi', 'c': False}]},
        {'t': 'ATTRIB /d nima uchun ishlatiladi?', 'a': [{'t': 'Papkalarga ham qo\'llaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Sanani ko\'rsatadi', 'c': False}, {'t': 'Diskni tekshiradi', 'c': False}]},
    ]},

    {'n': 'FIND - Matn qidirish', 't': 25, 'o': 17, 'q': [
        {'t': 'FIND komandasi nima qiladi?', 'a': [{'t': 'Faylda matn qidiradi', 'c': True}, {'t': 'Fayl qidiradi', 'c': False}, {'t': 'Papka qidiradi', 'c': False}, {'t': 'Disk qidiradi', 'c': False}]},
        {'t': 'FIND "text" file.txt nima qiladi?', 'a': [{'t': 'file.txt da "text" so\'zini qidiradi', 'c': True}, {'t': 'text nomli faylni qidiradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FIND /i parametri nima uchun?', 'a': [{'t': 'Katta-kichik harfni farqlamasdan qidiradi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Indeks yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'FIND /v "text" file.txt nima qiladi?', 'a': [{'t': '"text" yo\'q qatorlarni ko\'rsatadi', 'c': True}, {'t': 'Faylni tekshiradi', 'c': False}, {'t': 'Versiyani ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FIND /c "text" file.txt nima ko\'rsatadi?', 'a': [{'t': '"text" necha marta uchraganini', 'c': True}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Faylni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FIND /n "text" file.txt nima qiladi?', 'a': [{'t': 'Qator raqamlarini ham ko\'rsatadi', 'c': True}, {'t': 'Yangi fayl yaratadi', 'c': False}, {'t': 'Nomini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'FINDSTR - Kengaytirilgan qidiruv', 't': 30, 'o': 18, 'q': [
        {'t': 'FINDSTR va FIND orasidagi farq nima?', 'a': [{'t': 'FINDSTR regex va ko\'p so\'zlarni qo\'llab-quvvatlaydi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'FIND tezroq ishlaydi', 'c': False}, {'t': 'FINDSTR faqat papkalarda ishlaydi', 'c': False}]},
        {'t': 'FINDSTR "hello world" file.txt nima qiladi?', 'a': [{'t': 'hello yoki world so\'zlarini qidiradi', 'c': True}, {'t': 'Faqat "hello world" iborasini qidiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'FINDSTR /c:"hello world" file.txt nima qiladi?', 'a': [{'t': 'Aniq "hello world" iborasini qidiradi', 'c': True}, {'t': 'hello va world ni alohida qidiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FINDSTR /i parametri nima uchun?', 'a': [{'t': 'Katta-kichik harfni farqlamasdan qidiradi', 'c': True}, {'t': 'Ma\'lumotni import qiladi', 'c': False}, {'t': 'Indeks yaratadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'FINDSTR /s "text" *.txt nima qiladi?', 'a': [{'t': 'Barcha ichki papkalardagi .txt fayllardan qidiradi', 'c': True}, {'t': 'Fayllarni saqlaydi', 'c': False}, {'t': 'Fayllarni sortlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FINDSTR /r "^hello" file.txt nima qiladi?', 'a': [{'t': 'hello bilan boshlanadigan qatorlarni topadi', 'c': True}, {'t': 'hello so\'zini o\'chiradi', 'c': False}, {'t': 'Faylni qayta nomlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FINDSTR /n parametri nima qiladi?', 'a': [{'t': 'Qator raqamlarini ko\'rsatadi', 'c': True}, {'t': 'Yangi fayl yaratadi', 'c': False}, {'t': 'Nomini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'DATE va TIME - Sana va vaqt', 't': 20, 'o': 19, 'q': [
        {'t': 'DATE komandasi nima qiladi?', 'a': [{'t': 'Tizim sanasini ko\'rsatadi yoki o\'zgartiradi', 'c': True}, {'t': 'Faylni sanasi bo\'yicha qidiradi', 'c': False}, {'t': 'Fayl sanasini o\'zgartiradi', 'c': False}, {'t': 'Kalendar ochadi', 'c': False}]},
        {'t': 'TIME komandasi nima uchun?', 'a': [{'t': 'Tizim vaqtini ko\'rsatadi yoki o\'zgartiradi', 'c': True}, {'t': 'Vaqtni hisoblaydi', 'c': False}, {'t': 'Taymer o\'rnatadi', 'c': False}, {'t': 'Soat ochadi', 'c': False}]},
        {'t': 'DATE /t nima qiladi?', 'a': [{'t': 'Faqat sanani ko\'rsatadi, o\'zgartirmaydi', 'c': True}, {'t': 'Sanani o\'zgartiradi', 'c': False}, {'t': 'Vaqtni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'TIME /t nima uchun?', 'a': [{'t': 'Faqat vaqtni ko\'rsatadi, o\'zgartirmaydi', 'c': True}, {'t': 'Vaqtni o\'zgartiradi', 'c': False}, {'t': 'Sanani ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'DATE va TIME o\'zgartirish uchun qanday huquq kerak?', 'a': [{'t': 'Administrator huquqi', 'c': True}, {'t': 'Oddiy foydalanuvchi huquqi', 'c': False}, {'t': 'Hech qanday huquq kerak emas', 'c': False}, {'t': 'Guest huquqi', 'c': False}]},
    ]},

    {'n': 'VER - Versiya ma\'lumoti', 't': 15, 'o': 20, 'q': [
        {'t': 'VER komandasi nima ko\'rsatadi?', 'a': [{'t': 'Windows versiyasini', 'c': True}, {'t': 'CMD versiyasini', 'c': False}, {'t': 'Fayl versiyasini', 'c': False}, {'t': 'Dastur versiyasini', 'c': False}]},
        {'t': 'VER ning to\'liq nomi nima?', 'a': [{'t': 'Version', 'c': True}, {'t': 'Verify', 'c': False}, {'t': 'Vertical', 'c': False}, {'t': 'Very', 'c': False}]},
        {'t': 'VER komandasi parametr qabul qiladimi?', 'a': [{'t': 'Yo\'q, parametrsiz ishlaydi', 'c': True}, {'t': 'Ha, ko\'p parametr bor', 'c': False}, {'t': 'Faqat /? parametri', 'c': False}, {'t': 'Faqat /v parametri', 'c': False}]},
        {'t': 'VER qanday ma\'lumot beradi?', 'a': [{'t': 'Windows versiya raqami va build', 'c': True}, {'t': 'Faqat Windows nomi', 'c': False}, {'t': 'Kompyuter nomi', 'c': False}, {'t': 'Foydalanuvchi nomi', 'c': False}]},
        {'t': 'VER nima uchun foydali?', 'a': [{'t': 'Tizim versiyasini bilish uchun', 'c': True}, {'t': 'Fayllarni tekshirish uchun', 'c': False}, {'t': 'Diskni tozalash uchun', 'c': False}, {'t': 'Xotira tekshirish uchun', 'c': False}]},
    ]},

    {'n': 'VOL - Disk nomi', 't': 15, 'o': 21, 'q': [
        {'t': 'VOL komandasi nima ko\'rsatadi?', 'a': [{'t': 'Disk nomini va seriya raqamini', 'c': True}, {'t': 'Disk hajmini', 'c': False}, {'t': 'Disk tezligini', 'c': False}, {'t': 'Disk turini', 'c': False}]},
        {'t': 'VOL C: nima qiladi?', 'a': [{'t': 'C: diskining nomini ko\'rsatadi', 'c': True}, {'t': 'C: diskini ochadi', 'c': False}, {'t': 'C: diskini formatlaydi', 'c': False}, {'t': 'C: diskini o\'chiradi', 'c': False}]},
        {'t': 'VOL ning to\'liq nomi nima?', 'a': [{'t': 'Volume', 'c': True}, {'t': 'Volt', 'c': False}, {'t': 'Voluntary', 'c': False}, {'t': 'Volatile', 'c': False}]},
        {'t': 'VOL disk seriya raqamini nima uchun ko\'rsatadi?', 'a': [{'t': 'Diskni identifikatsiya qilish uchun', 'c': True}, {'t': 'Diskni himoyalash uchun', 'c': False}, {'t': 'Diskni tezlashtirish uchun', 'c': False}, {'t': 'Diskni tozalash uchun', 'c': False}]},
        {'t': 'VOL parametrsiz yozilsa nima ko\'rsatadi?', 'a': [{'t': 'Joriy diskning ma\'lumotini', 'c': True}, {'t': 'Barcha disklarning ma\'lumotini', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Yordam ma\'lumotini', 'c': False}]},
    ]},

    {'n': 'LABEL - Disk nomini o\'zgartirish', 't': 20, 'o': 22, 'q': [
        {'t': 'LABEL komandasi nima qiladi?', 'a': [{'t': 'Disk nomini o\'zgartiradi', 'c': True}, {'t': 'Fayl nomini o\'zgartiradi', 'c': False}, {'t': 'Papka nomini o\'zgartiradi', 'c': False}, {'t': 'Kompyuter nomini o\'zgartiradi', 'c': False}]},
        {'t': 'LABEL C: MyDisk nima qiladi?', 'a': [{'t': 'C: diskiga "MyDisk" nomini beradi', 'c': True}, {'t': 'MyDisk nomli fayl yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Diskni formatlaydi', 'c': False}]},
        {'t': 'LABEL disk nomini o\'chirish mumkinmi?', 'a': [{'t': 'Ha, bo\'sh nom berib', 'c': True}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat formatlash orqali', 'c': False}, {'t': 'Faqat administrator orqali', 'c': False}]},
        {'t': 'LABEL uchun qanday huquq kerak?', 'a': [{'t': 'Administrator huquqi', 'c': True}, {'t': 'Oddiy foydalanuvchi huquqi', 'c': False}, {'t': 'Hech qanday huquq kerak emas', 'c': False}, {'t': 'Guest huquqi', 'c': False}]},
        {'t': 'LABEL disk nomida nechta belgi bo\'lishi mumkin?', 'a': [{'t': '11 ta belgi (NTFS da 32 ta)', 'c': True}, {'t': '8 ta belgi', 'c': False}, {'t': 'Cheksiz', 'c': False}, {'t': '255 ta belgi', 'c': False}]},
    ]},

    {'n': 'CHKDSK - Diskni tekshirish', 't': 25, 'o': 23, 'q': [
        {'t': 'CHKDSK komandasi nima qiladi?', 'a': [{'t': 'Diskni xatolarga tekshiradi', 'c': True}, {'t': 'Diskni formatlaydi', 'c': False}, {'t': 'Diskni tozalaydi', 'c': False}, {'t': 'Diskni nusxalaydi', 'c': False}]},
        {'t': 'CHKDSK /f nima uchun?', 'a': [{'t': 'Topilgan xatolarni tuzatadi', 'c': True}, {'t': 'Fayllarni tekshiradi', 'c': False}, {'t': 'Tez tekshiradi', 'c': False}, {'t': 'To\'liq tekshiradi', 'c': False}]},
        {'t': 'CHKDSK /r nima qiladi?', 'a': [{'t': 'Yomon sektorlarni topadi va ma\'lumotni tiklaydi', 'c': True}, {'t': 'Diskni qayta formatlaydi', 'c': False}, {'t': 'Diskni qayta nomlaydi', 'c': False}, {'t': 'Diskni o\'chiradi', 'c': False}]},
        {'t': 'CHKDSK C: ishlatish uchun nima kerak?', 'a': [{'t': 'Administrator huquqi', 'c': True}, {'t': 'Oddiy foydalanuvchi huquqi', 'c': False}, {'t': 'Hech narsa kerak emas', 'c': False}, {'t': 'Guest huquqi', 'c': False}]},
        {'t': 'CHKDSK /v parametri nima qiladi?', 'a': [{'t': 'Barcha fayl nomlarini ko\'rsatadi', 'c': True}, {'t': 'Versiyani ko\'rsatadi', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'CHKDSK qachon ishlatiladi?', 'a': [{'t': 'Disk xatolari shubhasi bo\'lganda', 'c': True}, {'t': 'Har kuni', 'c': False}, {'t': 'Fayl yaratishdan oldin', 'c': False}, {'t': 'Internet ishlatishdan oldin', 'c': False}]},
    ]},

    {'n': 'FORMAT - Diskni formatlash', 't': 20, 'o': 24, 'q': [
        {'t': 'FORMAT komandasi nima qiladi?', 'a': [{'t': 'Diskni formatlaydi (barcha ma\'lumotni o\'chiradi)', 'c': True}, {'t': 'Diskni tozalaydi', 'c': False}, {'t': 'Diskni tekshiradi', 'c': False}, {'t': 'Diskni nusxalaydi', 'c': False}]},
        {'t': 'FORMAT D: /fs:NTFS nima qiladi?', 'a': [{'t': 'D: diskini NTFS fayl tizimida formatlaydi', 'c': True}, {'t': 'D: diskini tekshiradi', 'c': False}, {'t': 'D: diskini nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FORMAT /q parametri nima uchun?', 'a': [{'t': 'Tez formatlash (quick format)', 'c': True}, {'t': 'Sifatli formatlash', 'c': False}, {'t': 'Quiet rejimda formatlash', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FORMAT C: xavflimi?', 'a': [{'t': 'Ha, tizim diskini o\'chiradi', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Faqat fayllarni o\'chiradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'FORMAT uchun qanday huquq kerak?', 'a': [{'t': 'Administrator huquqi', 'c': True}, {'t': 'Oddiy foydalanuvchi huquqi', 'c': False}, {'t': 'Hech qanday huquq kerak emas', 'c': False}, {'t': 'Guest huquqi', 'c': False}]},
    ]},

    {'n': 'DISKPART - Disk boshqaruvi', 't': 30, 'o': 25, 'q': [
        {'t': 'DISKPART nima?', 'a': [{'t': 'Disklar va bo\'limlarni boshqarish vositasi', 'c': True}, {'t': 'Fayllarni bo\'lish dasturi', 'c': False}, {'t': 'Disk tozalash dasturi', 'c': False}, {'t': 'Disk nusxalash dasturi', 'c': False}]},
        {'t': 'DISKPART ishlatish uchun nima kerak?', 'a': [{'t': 'Administrator huquqi', 'c': True}, {'t': 'Oddiy foydalanuvchi huquqi', 'c': False}, {'t': 'Hech narsa kerak emas', 'c': False}, {'t': 'Guest huquqi', 'c': False}]},
        {'t': 'DISKPART da list disk komandasi nima qiladi?', 'a': [{'t': 'Barcha disklarni ko\'rsatadi', 'c': True}, {'t': 'Diskni o\'chiradi', 'c': False}, {'t': 'Diskni yaratadi', 'c': False}, {'t': 'Diskni formatlaydi', 'c': False}]},
        {'t': 'DISKPART da select disk 0 nima qiladi?', 'a': [{'t': '0-raqamli diskni tanlaydi', 'c': True}, {'t': 'Diskni o\'chiradi', 'c': False}, {'t': 'Diskni formatlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'DISKPART da clean komandasi nima qiladi?', 'a': [{'t': 'Tanlangan diskni butunlay tozalaydi', 'c': True}, {'t': 'Faqat fayllarni o\'chiradi', 'c': False}, {'t': 'Diskni tekshiradi', 'c': False}, {'t': 'Diskni nusxalaydi', 'c': False}]},
        {'t': 'DISKPART xavflimi?', 'a': [{'t': 'Ha, noto\'g\'ri ishlatilsa ma\'lumot yo\'qoladi', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Faqat C: disk uchun xavfli', 'c': False}, {'t': 'Hech qachon xavfli emas', 'c': False}]},
        {'t': 'DISKPART dan chiqish uchun qanday komanda?', 'a': [{'t': 'exit', 'c': True}, {'t': 'quit', 'c': False}, {'t': 'close', 'c': False}, {'t': 'end', 'c': False}]},
    ]},

    {'n': 'TREE - Papka strukturasi', 't': 20, 'o': 26, 'q': [
        {'t': 'TREE komandasi nima qiladi?', 'a': [{'t': 'Papka strukturasini daraxt ko\'rinishida ko\'rsatadi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}]},
        {'t': 'TREE /f nima uchun?', 'a': [{'t': 'Fayllarni ham ko\'rsatadi', 'c': True}, {'t': 'Fayllarni formatlaydi', 'c': False}, {'t': 'Fayllarni topadi', 'c': False}, {'t': 'Tez ko\'rsatadi', 'c': False}]},
        {'t': 'TREE /a parametri nima qiladi?', 'a': [{'t': 'ASCII belgilar bilan chizadi', 'c': True}, {'t': 'Barcha fayllarni ko\'rsatadi', 'c': False}, {'t': 'Arxiv fayllarni ko\'rsatadi', 'c': False}, {'t': 'Atributlarni ko\'rsatadi', 'c': False}]},
        {'t': 'TREE C:\\Users nima ko\'rsatadi?', 'a': [{'t': 'Users papkasining strukturasini', 'c': True}, {'t': 'Faqat Users papkasini', 'c': False}, {'t': 'Barcha fayllarni', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'TREE > tree.txt nima qiladi?', 'a': [{'t': 'Natijani tree.txt fayliga yozadi', 'c': True}, {'t': 'tree.txt ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Ekranga chiqaradi', 'c': False}]},
    ]},

    {'n': 'COMP - Fayllarni solishtirish', 't': 25, 'o': 27, 'q': [
        {'t': 'COMP komandasi nima qiladi?', 'a': [{'t': 'Ikki faylni solishtiradi', 'c': True}, {'t': 'Fayllarni siqadi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Fayllarni birlashtiradi', 'c': False}]},
        {'t': 'COMP file1.txt file2.txt nima qiladi?', 'a': [{'t': 'Ikki faylning farqini ko\'rsatadi', 'c': True}, {'t': 'Fayllarni birlashtiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'COMP /a parametri nima uchun?', 'a': [{'t': 'Farqlarni ASCII belgilar sifatida ko\'rsatadi', 'c': True}, {'t': 'Barcha fayllarni solishtiradi', 'c': False}, {'t': 'Arxiv fayllarni solishtiradi', 'c': False}, {'t': 'Atributlarni solishtiradi', 'c': False}]},
        {'t': 'COMP /n=10 nima qiladi?', 'a': [{'t': 'Faqat birinchi 10 qatorni solishtiradi', 'c': True}, {'t': '10 ta faylni solishtiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Fayllarni 10 qismga bo\'ladi', 'c': False}]},
        {'t': 'COMP fayllar bir xil bo\'lsa nima ko\'rsatadi?', 'a': [{'t': 'Files compare OK', 'c': True}, {'t': 'Files are different', 'c': False}, {'t': 'Error', 'c': False}, {'t': 'Hech narsa ko\'rsatmaydi', 'c': False}]},
    ]},

    {'n': 'FC - Kengaytirilgan solishtirish', 't': 25, 'o': 28, 'q': [
        {'t': 'FC va COMP orasidagi farq nima?', 'a': [{'t': 'FC ko\'proq ma\'lumot va formatlar bilan ishlaydi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'COMP tezroq ishlaydi', 'c': False}, {'t': 'FC faqat matn fayllari uchun', 'c': False}]},
        {'t': 'FC file1.txt file2.txt nima qiladi?', 'a': [{'t': 'Fayllarni qator-qator solishtiradi', 'c': True}, {'t': 'Fayllarni birlashtiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FC /b parametri nima uchun?', 'a': [{'t': 'Binary (ikkilik) rejimda solishtiradi', 'c': True}, {'t': 'Tezroq solishtiradi', 'c': False}, {'t': 'Katta fayllarni solishtiradi', 'c': False}, {'t': 'Backup yaratadi', 'c': False}]},
        {'t': 'FC /c nima qiladi?', 'a': [{'t': 'Katta-kichik harfni farqlamaydi', 'c': True}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Fayllarni tozalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FC /n parametri nima uchun?', 'a': [{'t': 'Qator raqamlarini ko\'rsatadi', 'c': True}, {'t': 'Yangi fayl yaratadi', 'c': False}, {'t': 'Nomlarni solishtiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'FC /w nima qiladi?', 'a': [{'t': 'Bo\'sh joylarni e\'tiborsiz qoldiradi', 'c': True}, {'t': 'Keng formatda ko\'rsatadi', 'c': False}, {'t': 'Fayllarni yozadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'SORT - Saralash', 't': 20, 'o': 29, 'q': [
        {'t': 'SORT komandasi nima qiladi?', 'a': [{'t': 'Matnni saralaydi', 'c': True}, {'t': 'Fayllarni saralaydi', 'c': False}, {'t': 'Papkalarni saralaydi', 'c': False}, {'t': 'Diskni saralaydi', 'c': False}]},
        {'t': 'SORT file.txt nima qiladi?', 'a': [{'t': 'file.txt dagi qatorlarni alifbo tartibida saralaydi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'SORT /r parametri nima uchun?', 'a': [{'t': 'Teskari tartibda saralaydi', 'c': True}, {'t': 'Faylni o\'qiydi', 'c': False}, {'t': 'Faylni qayta yozadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'SORT /+5 nima qiladi?', 'a': [{'t': '5-belgidan boshlab saralaydi', 'c': True}, {'t': '5 ta qator qo\'shadi', 'c': False}, {'t': '5 marta saralaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'DIR | SORT nima qiladi?', 'a': [{'t': 'DIR natijasini saralaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
    ]},

    {'n': 'MORE - Sahifalash', 't': 20, 'o': 30, 'q': [
        {'t': 'MORE komandasi nima qiladi?', 'a': [{'t': 'Matnni sahifa-sahifa ko\'rsatadi', 'c': True}, {'t': 'Ko\'proq ma\'lumot qo\'shadi', 'c': False}, {'t': 'Faylni kattalashtiradi', 'c': False}, {'t': 'Faylni nusxalaydi', 'c': False}]},
        {'t': 'MORE file.txt nima qiladi?', 'a': [{'t': 'file.txt ni sahifa-sahifa ko\'rsatadi', 'c': True}, {'t': 'file.txt ga ma\'lumot qo\'shadi', 'c': False}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'TYPE file.txt | MORE nima uchun?', 'a': [{'t': 'Uzun faylni qulayroq o\'qish uchun', 'c': True}, {'t': 'Faylni nusxalash uchun', 'c': False}, {'t': 'Faylni o\'chirish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'MORE da keyingi sahifaga o\'tish uchun nima bosish kerak?', 'a': [{'t': 'Space yoki Enter', 'c': True}, {'t': 'Esc', 'c': False}, {'t': 'Tab', 'c': False}, {'t': 'Ctrl+C', 'c': False}]},
        {'t': 'MORE /e parametri nima qiladi?', 'a': [{'t': 'Kengaytirilgan funksiyalarni yoqadi', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    print("🚀 CMD - 30 TA MAVZU QO'SHILMOQDA...")
    subject = get_or_create_cmd()
    add_topics(subject, T)
    print(f"\n✅ Jami {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
    print(f"📊 Jami testlar: {sum(len(t['q']) for t in T)} ta")
