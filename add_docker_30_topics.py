"""
DOCKER - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_docker():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Docker', defaults={'category': cat, 'description': 'Docker - Konteynerlashtirish platformasi', 'icon': 'bi-box-seam', 'order': 28, 'is_active': True})
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
    {'n': 'Docker ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Docker nima?', 'a': [{'t': 'Konteynerlashtirish platformasi', 'c': True}, {'t': 'Virtual mashina', 'c': False}, {'t': 'Operatsion tizim', 'c': False}, {'t': 'Matn muharriri', 'c': False}]},
        {'t': 'Docker nima uchun kerak?', 'a': [{'t': 'Ilovalarni izolyatsiya qilingan muhitda ishga tushirish uchun', 'c': True}, {'t': 'Fayllarni arxivlash uchun', 'c': False}, {'t': 'Kod yozish uchun', 'c': False}, {'t': 'Ma\'lumotlar bazasini yaratish uchun', 'c': False}]},
        {'t': 'Container nima?', 'a': [{'t': 'Ilovani va uning barcha bog\'liqliklarini o\'z ichiga olgan yengil paket', 'c': True}, {'t': 'Virtual mashina', 'c': False}, {'t': 'Fayl tizimi', 'c': False}, {'t': 'Tarmoq protokoli', 'c': False}]},
        {'t': 'Docker va Virtual Machine orasidagi asosiy farq nima?', 'a': [{'t': 'Docker yengilroq va tezroq ishga tushadi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'VM tezroq ishlaydi', 'c': False}, {'t': 'Docker faqat Linux da ishlaydi', 'c': False}]},
        {'t': 'Docker qaysi operatsion tizimlarda ishlaydi?', 'a': [{'t': 'Linux, Windows, MacOS', 'c': True}, {'t': 'Faqat Linux', 'c': False}, {'t': 'Faqat Windows', 'c': False}, {'t': 'Faqat MacOS', 'c': False}]},
    ]},

    {'n': 'Docker o\'rnatish', 't': 20, 'o': 2, 'q': [
        {'t': 'Docker qanday o\'rnatiladi?', 'a': [{'t': 'Docker Desktop yoki docker.com dan yuklab olish orqali', 'c': True}, {'t': 'Faqat apt-get orqali', 'c': False}, {'t': 'Faqat npm orqali', 'c': False}, {'t': 'O\'rnatish shart emas', 'c': False}]},
        {'t': 'docker --version komandasi nima qiladi?', 'a': [{'t': 'Docker versiyasini ko\'rsatadi', 'c': True}, {'t': 'Docker ni o\'rnatadi', 'c': False}, {'t': 'Docker ni yangilaydi', 'c': False}, {'t': 'Docker ni o\'chiradi', 'c': False}]},
        {'t': 'Docker Desktop nima?', 'a': [{'t': 'Windows va Mac uchun Docker dasturi', 'c': True}, {'t': 'Faqat Linux uchun', 'c': False}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Docker o\'rnatilganini qanday tekshirish mumkin?', 'a': [{'t': 'docker --version yoki docker info', 'c': True}, {'t': 'Faqat kompyuterni qayta ishga tushirish', 'c': False}, {'t': 'Faqat Docker Desktop ochish', 'c': False}, {'t': 'Tekshirish mumkin emas', 'c': False}]},
        {'t': 'Docker ishga tushganini qanday bilish mumkin?', 'a': [{'t': 'docker ps komandasi ishlaydi', 'c': True}, {'t': 'Kompyuter tezroq ishlaydi', 'c': False}, {'t': 'Ekranda xabar chiqadi', 'c': False}, {'t': 'Bilish mumkin emas', 'c': False}]},
    ]},

    {'n': 'Docker Image nima?', 't': 25, 'o': 3, 'q': [
        {'t': 'Docker Image nima?', 'a': [{'t': 'Container yaratish uchun shablon', 'c': True}, {'t': 'Rasm fayli', 'c': False}, {'t': 'Video fayl', 'c': False}, {'t': 'Matn fayli', 'c': False}]},
        {'t': 'Image va Container orasidagi farq nima?', 'a': [{'t': 'Image - shablon, Container - ishga tushgan nusxa', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Container kattaroq', 'c': False}, {'t': 'Image tezroq ishlaydi', 'c': False}]},
        {'t': 'Docker Hub nima?', 'a': [{'t': 'Docker image larni saqlash va ulashish xizmati', 'c': True}, {'t': 'Docker o\'rnatish dasturi', 'c': False}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Official image nima?', 'a': [{'t': 'Docker tomonidan tasdiqlangan rasmiy image', 'c': True}, {'t': 'Eng yangi image', 'c': False}, {'t': 'Eng katta image', 'c': False}, {'t': 'Pullik image', 'c': False}]},
        {'t': 'Image tag nima?', 'a': [{'t': 'Image versiyasini belgilovchi yorliq', 'c': True}, {'t': 'Image nomi', 'c': False}, {'t': 'Image hajmi', 'c': False}, {'t': 'Image turi', 'c': False}]},
        {'t': 'latest tag nima bildiradi?', 'a': [{'t': 'Eng so\'nggi versiya', 'c': True}, {'t': 'Eng eski versiya', 'c': False}, {'t': 'Eng katta versiya', 'c': False}, {'t': 'Test versiyasi', 'c': False}]},
    ]},

    {'n': 'docker pull - Image yuklab olish', 't': 20, 'o': 4, 'q': [
        {'t': 'docker pull nima qiladi?', 'a': [{'t': 'Docker Hub dan image yuklab oladi', 'c': True}, {'t': 'Container ishga tushiradi', 'c': False}, {'t': 'Image o\'chiradi', 'c': False}, {'t': 'Container to\'xtatadi', 'c': False}]},
        {'t': 'docker pull nginx nima qiladi?', 'a': [{'t': 'nginx image ni yuklab oladi', 'c': True}, {'t': 'nginx ni o\'rnatadi', 'c': False}, {'t': 'nginx ni o\'chiradi', 'c': False}, {'t': 'nginx ni ishga tushiradi', 'c': False}]},
        {'t': 'docker pull ubuntu:20.04 da :20.04 nima?', 'a': [{'t': 'Image versiyasi (tag)', 'c': True}, {'t': 'Port raqami', 'c': False}, {'t': 'Container nomi', 'c': False}, {'t': 'Hajmi', 'c': False}]},
        {'t': 'docker pull dan keyin nima qilish kerak?', 'a': [{'t': 'docker run bilan container yaratish', 'c': True}, {'t': 'Kompyuterni qayta ishga tushirish', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Docker ni o\'chirish', 'c': False}]},
        {'t': 'docker pull qachon ishlatiladi?', 'a': [{'t': 'Yangi image kerak bo\'lganda', 'c': True}, {'t': 'Container ishga tushirishdan oldin har doim', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}]},
    ]},

    {'n': 'docker images - Image larni ko\'rish', 't': 20, 'o': 5, 'q': [
        {'t': 'docker images nima qiladi?', 'a': [{'t': 'Lokal kompyuterdagi barcha image larni ko\'rsatadi', 'c': True}, {'t': 'Docker Hub dagi imagelarni ko\'rsatadi', 'c': False}, {'t': 'Containerlarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}]},
        {'t': 'docker images qanday ma\'lumot beradi?', 'a': [{'t': 'Repository, Tag, Image ID, Yaratilgan vaqt, Hajm', 'c': True}, {'t': 'Faqat nom', 'c': False}, {'t': 'Faqat hajm', 'c': False}, {'t': 'Faqat versiya', 'c': False}]},
        {'t': 'docker images -a nima qiladi?', 'a': [{'t': 'Barcha imagelarni (intermediate ham) ko\'rsatadi', 'c': True}, {'t': 'Faqat official imagelarni ko\'rsatadi', 'c': False}, {'t': 'Faqat ishlab turgan imagelarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker images -q nima uchun?', 'a': [{'t': 'Faqat Image ID larni ko\'rsatadi', 'c': True}, {'t': 'Quiet rejimda ishlaydi', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Image ID nima?', 'a': [{'t': 'Image ning noyob identifikatori', 'c': True}, {'t': 'Image nomi', 'c': False}, {'t': 'Image versiyasi', 'c': False}, {'t': 'Image hajmi', 'c': False}]},
    ]},

    {'n': 'docker run - Container yaratish', 't': 30, 'o': 6, 'q': [
        {'t': 'docker run nima qiladi?', 'a': [{'t': 'Image dan yangi container yaratadi va ishga tushiradi', 'c': True}, {'t': 'Faqat container yaratadi', 'c': False}, {'t': 'Faqat container ishga tushiradi', 'c': False}, {'t': 'Image yuklab oladi', 'c': False}]},
        {'t': 'docker run hello-world nima qiladi?', 'a': [{'t': 'hello-world containerini ishga tushiradi va test xabarini ko\'rsatadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Docker ni o\'chiradi', 'c': False}]},
        {'t': 'docker run -d nima uchun?', 'a': [{'t': 'Container ni background (detached) rejimda ishga tushiradi', 'c': True}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Debug rejimda ishga tushiradi', 'c': False}, {'t': 'Download qiladi', 'c': False}]},
        {'t': 'docker run -it nima qiladi?', 'a': [{'t': 'Interactive terminal rejimda ishga tushiradi', 'c': True}, {'t': 'Internet orqali ishga tushiradi', 'c': False}, {'t': 'Tezroq ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker run --name myapp nima uchun?', 'a': [{'t': 'Container ga nom beradi', 'c': True}, {'t': 'Image nomini o\'zgartiradi', 'c': False}, {'t': 'Fayl yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker run -p 8080:80 nima qiladi?', 'a': [{'t': 'Host 8080 portini container 80 portiga bog\'laydi', 'c': True}, {'t': '8080 ta container yaratadi', 'c': False}, {'t': 'Parolni o\'rnatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker run --rm nima uchun?', 'a': [{'t': 'Container to\'xtagandan keyin avtomatik o\'chiradi', 'c': True}, {'t': 'Container ni darhol o\'chiradi', 'c': False}, {'t': 'Remote serverda ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'docker ps - Containerlarni ko\'rish', 't': 25, 'o': 7, 'q': [
        {'t': 'docker ps nima qiladi?', 'a': [{'t': 'Ishlab turgan containerlarni ko\'rsatadi', 'c': True}, {'t': 'Barcha containerlarni ko\'rsatadi', 'c': False}, {'t': 'Imagelarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}]},
        {'t': 'docker ps -a nima qiladi?', 'a': [{'t': 'Barcha containerlarni (to\'xtagan ham) ko\'rsatadi', 'c': True}, {'t': 'Faqat ishlab turganlarni ko\'rsatadi', 'c': False}, {'t': 'Faqat to\'xtaganlarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker ps qanday ma\'lumot beradi?', 'a': [{'t': 'Container ID, Image, Command, Status, Ports, Names', 'c': True}, {'t': 'Faqat nom', 'c': False}, {'t': 'Faqat status', 'c': False}, {'t': 'Faqat ID', 'c': False}]},
        {'t': 'docker ps -q nima uchun?', 'a': [{'t': 'Faqat Container ID larni ko\'rsatadi', 'c': True}, {'t': 'Quiet rejimda ishlaydi', 'c': False}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker ps -l nima qiladi?', 'a': [{'t': 'Oxirgi yaratilgan containerni ko\'rsatadi', 'c': True}, {'t': 'Eng katta containerni ko\'rsatadi', 'c': False}, {'t': 'Eng eski containerni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Container ID nima?', 'a': [{'t': 'Container ning noyob identifikatori', 'c': True}, {'t': 'Container nomi', 'c': False}, {'t': 'Container versiyasi', 'c': False}, {'t': 'Container hajmi', 'c': False}]},
    ]},

    {'n': 'docker start/stop - Container boshqarish', 't': 25, 'o': 8, 'q': [
        {'t': 'docker start nima qiladi?', 'a': [{'t': 'To\'xtagan containerni ishga tushiradi', 'c': True}, {'t': 'Yangi container yaratadi', 'c': False}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Image yuklab oladi', 'c': False}]},
        {'t': 'docker stop nima qiladi?', 'a': [{'t': 'Ishlab turgan containerni to\'xtatadi', 'c': True}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Container ni yaratadi', 'c': False}, {'t': 'Image ni o\'chiradi', 'c': False}]},
        {'t': 'docker start mycontainer nima qiladi?', 'a': [{'t': 'mycontainer nomli containerni ishga tushiradi', 'c': True}, {'t': 'mycontainer nomli image yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'docker stop va docker kill farqi nima?', 'a': [{'t': 'stop yumshoq to\'xtatadi, kill majburiy', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'kill xavfsizroq', 'c': False}, {'t': 'stop tezroq', 'c': False}]},
        {'t': 'docker restart nima qiladi?', 'a': [{'t': 'Container ni qayta ishga tushiradi', 'c': True}, {'t': 'Docker ni qayta ishga tushiradi', 'c': False}, {'t': 'Kompyuterni qayta ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker pause nima uchun?', 'a': [{'t': 'Container jarayonlarini vaqtincha to\'xtatadi', 'c': True}, {'t': 'Container ni butunlay to\'xtatadi', 'c': False}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'docker rm - Container o\'chirish', 't': 20, 'o': 9, 'q': [
        {'t': 'docker rm nima qiladi?', 'a': [{'t': 'Container ni o\'chiradi', 'c': True}, {'t': 'Image ni o\'chiradi', 'c': False}, {'t': 'Container ni to\'xtatadi', 'c': False}, {'t': 'Container ni yaratadi', 'c': False}]},
        {'t': 'docker rm mycontainer nima qiladi?', 'a': [{'t': 'mycontainer ni o\'chiradi', 'c': True}, {'t': 'mycontainer ni yaratadi', 'c': False}, {'t': 'mycontainer ni ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker rm -f nima uchun?', 'a': [{'t': 'Ishlab turgan containerni ham majburiy o\'chiradi', 'c': True}, {'t': 'Tezroq o\'chiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker rm $(docker ps -aq) nima qiladi?', 'a': [{'t': 'Barcha containerlarni o\'chiradi', 'c': True}, {'t': 'Faqat bitta containerni o\'chiradi', 'c': False}, {'t': 'Imagelarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'To\'xtagan containerni o\'chirish mumkinmi?', 'a': [{'t': 'Ha, docker rm bilan', 'c': True}, {'t': 'Yo\'q, avval ishga tushirish kerak', 'c': False}, {'t': 'Yo\'q, mumkin emas', 'c': False}, {'t': 'Faqat -f bilan', 'c': False}]},
    ]},

    {'n': 'docker rmi - Image o\'chirish', 't': 20, 'o': 10, 'q': [
        {'t': 'docker rmi nima qiladi?', 'a': [{'t': 'Image ni o\'chiradi', 'c': True}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Image yaratadi', 'c': False}, {'t': 'Container yaratadi', 'c': False}]},
        {'t': 'docker rmi nginx nima qiladi?', 'a': [{'t': 'nginx image ni o\'chiradi', 'c': True}, {'t': 'nginx containerni o\'chiradi', 'c': False}, {'t': 'nginx ni o\'rnatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker rmi -f nima uchun?', 'a': [{'t': 'Majburiy o\'chiradi, containerlar bo\'lsa ham', 'c': True}, {'t': 'Tezroq o\'chiradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Image ishlatilayotgan bo\'lsa o\'chirish mumkinmi?', 'a': [{'t': 'Yo\'q, avval containerlarni o\'chirish kerak', 'c': True}, {'t': 'Ha, muammo yo\'q', 'c': False}, {'t': 'Faqat -f bilan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'docker image prune nima qiladi?', 'a': [{'t': 'Ishlatilmayotgan imagelarni o\'chiradi', 'c': True}, {'t': 'Barcha imagelarni o\'chiradi', 'c': False}, {'t': 'Containerlarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'docker exec - Container ichida komanda bajarish', 't': 25, 'o': 11, 'q': [
        {'t': 'docker exec nima qiladi?', 'a': [{'t': 'Ishlab turgan container ichida komanda bajaradi', 'c': True}, {'t': 'Yangi container yaratadi', 'c': False}, {'t': 'Container ni to\'xtatadi', 'c': False}, {'t': 'Image yaratadi', 'c': False}]},
        {'t': 'docker exec -it myapp bash nima qiladi?', 'a': [{'t': 'myapp container ichiga bash terminal orqali kiradi', 'c': True}, {'t': 'myapp ni o\'chiradi', 'c': False}, {'t': 'bash ni o\'rnatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker exec -it nima uchun?', 'a': [{'t': 'Interactive terminal rejimda ishlash uchun', 'c': True}, {'t': 'Internet orqali ishlash uchun', 'c': False}, {'t': 'Tezroq ishlash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker exec myapp ls nima qiladi?', 'a': [{'t': 'myapp container ichidagi fayllarni ko\'rsatadi', 'c': True}, {'t': 'Host kompyuter fayllarini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Container ni o\'chiradi', 'c': False}]},
        {'t': 'docker exec va docker run farqi nima?', 'a': [{'t': 'exec mavjud containerda ishlaydi, run yangi yaratadi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'run tezroq', 'c': False}, {'t': 'exec xavflirog', 'c': False}]},
        {'t': 'docker exec qachon ishlatiladi?', 'a': [{'t': 'Container ichini tekshirish yoki debug qilish uchun', 'c': True}, {'t': 'Container yaratish uchun', 'c': False}, {'t': 'Image yuklab olish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'docker logs - Container loglari', 't': 20, 'o': 12, 'q': [
        {'t': 'docker logs nima qiladi?', 'a': [{'t': 'Container loglarini ko\'rsatadi', 'c': True}, {'t': 'Container ni ishga tushiradi', 'c': False}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Image yaratadi', 'c': False}]},
        {'t': 'docker logs myapp nima qiladi?', 'a': [{'t': 'myapp container loglarini ko\'rsatadi', 'c': True}, {'t': 'myapp ni o\'chiradi', 'c': False}, {'t': 'myapp ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker logs -f nima uchun?', 'a': [{'t': 'Loglarni jonli kuzatish (follow) uchun', 'c': True}, {'t': 'Faylga yozish uchun', 'c': False}, {'t': 'Tezroq ko\'rsatish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker logs --tail 50 nima qiladi?', 'a': [{'t': 'Oxirgi 50 ta log qatorini ko\'rsatadi', 'c': True}, {'t': 'Birinchi 50 ta qatorni ko\'rsatadi', 'c': False}, {'t': '50 ta container logini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker logs --since 1h nima qiladi?', 'a': [{'t': 'Oxirgi 1 soatdagi loglarni ko\'rsatadi', 'c': True}, {'t': '1 soatdan oldingi loglarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'docker inspect - Batafsil ma\'lumot', 't': 20, 'o': 13, 'q': [
        {'t': 'docker inspect nima qiladi?', 'a': [{'t': 'Container yoki image haqida batafsil ma\'lumot beradi', 'c': True}, {'t': 'Container ni tekshiradi va tuzatadi', 'c': False}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Image yaratadi', 'c': False}]},
        {'t': 'docker inspect myapp nima ko\'rsatadi?', 'a': [{'t': 'JSON formatda to\'liq konfiguratsiya', 'c': True}, {'t': 'Faqat nom', 'c': False}, {'t': 'Faqat status', 'c': False}, {'t': 'Faqat hajm', 'c': False}]},
        {'t': 'docker inspect --format nima uchun?', 'a': [{'t': 'Ma\'lum qismini olish uchun', 'c': True}, {'t': 'Formatni o\'zgartirish uchun', 'c': False}, {'t': 'Faylni formatlash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker inspect qanday ma\'lumot beradi?', 'a': [{'t': 'IP, Portlar, Volume, Environment, Network va boshqalar', 'c': True}, {'t': 'Faqat IP manzil', 'c': False}, {'t': 'Faqat hajm', 'c': False}, {'t': 'Faqat nom', 'c': False}]},
        {'t': 'docker inspect qachon foydali?', 'a': [{'t': 'Debug qilish va konfiguratsiyani tekshirish uchun', 'c': True}, {'t': 'Container yaratish uchun', 'c': False}, {'t': 'Image yuklab olish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'Dockerfile nima?', 't': 25, 'o': 14, 'q': [
        {'t': 'Dockerfile nima?', 'a': [{'t': 'Docker image yaratish uchun ko\'rsatmalar fayli', 'c': True}, {'t': 'Container konfiguratsiya fayli', 'c': False}, {'t': 'Log fayli', 'c': False}, {'t': 'Ma\'lumotlar bazasi fayli', 'c': False}]},
        {'t': 'Dockerfile qanday nomlanadi?', 'a': [{'t': 'Aniq "Dockerfile" (kengaytmasiz)', 'c': True}, {'t': 'dockerfile.txt', 'c': False}, {'t': 'docker.file', 'c': False}, {'t': 'Istalgan nom', 'c': False}]},
        {'t': 'FROM nima qiladi?', 'a': [{'t': 'Asosiy (base) image ni belgilaydi', 'c': True}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Komanda bajaradi', 'c': False}, {'t': 'Port ochadi', 'c': False}]},
        {'t': 'RUN nima uchun ishlatiladi?', 'a': [{'t': 'Image yaratish vaqtida komanda bajarish uchun', 'c': True}, {'t': 'Container ishga tushganda komanda bajarish uchun', 'c': False}, {'t': 'Fayllarni nusxalash uchun', 'c': False}, {'t': 'Port ochish uchun', 'c': False}]},
        {'t': 'CMD nima qiladi?', 'a': [{'t': 'Container ishga tushganda bajariladigan standart komanda', 'c': True}, {'t': 'Image yaratishda bajariladigan komanda', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Port ochadi', 'c': False}]},
        {'t': 'COPY nima uchun?', 'a': [{'t': 'Host dan container ga fayl nusxalash uchun', 'c': True}, {'t': 'Container ichida fayl nusxalash uchun', 'c': False}, {'t': 'Image nusxalash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'docker build - Image yaratish', 't': 25, 'o': 15, 'q': [
        {'t': 'docker build nima qiladi?', 'a': [{'t': 'Dockerfile dan yangi image yaratadi', 'c': True}, {'t': 'Container yaratadi', 'c': False}, {'t': 'Dockerfile yaratadi', 'c': False}, {'t': 'Image ni o\'chiradi', 'c': False}]},
        {'t': 'docker build -t myapp . nima qiladi?', 'a': [{'t': 'Joriy papkadagi Dockerfile dan myapp nomli image yaratadi', 'c': True}, {'t': 'myapp nomli Dockerfile yaratadi', 'c': False}, {'t': 'myapp containerni ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker build da -t nima uchun?', 'a': [{'t': 'Image ga nom (tag) berish uchun', 'c': True}, {'t': 'Test rejimda yaratish uchun', 'c': False}, {'t': 'Vaqtni belgilash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker build . da nuqta nima?', 'a': [{'t': 'Build context - joriy papka', 'c': True}, {'t': 'Fayl nomi', 'c': False}, {'t': 'Xato belgisi', 'c': False}, {'t': 'Tugash belgisi', 'c': False}]},
        {'t': 'docker build --no-cache nima uchun?', 'a': [{'t': 'Keshni ishlatmasdan qayta yaratish uchun', 'c': True}, {'t': 'Tezroq yaratish uchun', 'c': False}, {'t': 'Xotira tejash uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker build qachon ishlatiladi?', 'a': [{'t': 'O\'z custom image yaratish kerak bo\'lganda', 'c': True}, {'t': 'Har doim container yaratishdan oldin', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}]},
    ]},

    {'n': 'Dockerfile - WORKDIR, ENV, EXPOSE', 't': 30, 'o': 16, 'q': [
        {'t': 'WORKDIR nima qiladi?', 'a': [{'t': 'Container ichida ish papkasini o\'rnatadi', 'c': True}, {'t': 'Komanda bajaradi', 'c': False}, {'t': 'Port ochadi', 'c': False}, {'t': 'Fayl nusxalaydi', 'c': False}]},
        {'t': 'ENV nima uchun ishlatiladi?', 'a': [{'t': 'Environment o\'zgaruvchilarini o\'rnatish uchun', 'c': True}, {'t': 'Fayllarni nusxalash uchun', 'c': False}, {'t': 'Port ochish uchun', 'c': False}, {'t': 'Komanda bajarish uchun', 'c': False}]},
        {'t': 'EXPOSE 80 nima qiladi?', 'a': [{'t': 'Container 80-portda tinglashini bildiradi', 'c': True}, {'t': '80-portni ochadi', 'c': False}, {'t': '80 ta container yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'EXPOSE port ochib beradimi?', 'a': [{'t': 'Yo\'q, faqat hujjatlashtirish uchun, -p kerak', 'c': True}, {'t': 'Ha, avtomatik ochadi', 'c': False}, {'t': 'Ba\'zan ochadi', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'WORKDIR /app nima qiladi?', 'a': [{'t': '/app papkasini yaratadi va unga o\'tadi', 'c': True}, {'t': 'Faqat /app ga o\'tadi', 'c': False}, {'t': '/app ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'ENV NODE_ENV=production nima qiladi?', 'a': [{'t': 'NODE_ENV o\'zgaruvchisini production qilib o\'rnatadi', 'c': True}, {'t': 'Node.js ni o\'rnatadi', 'c': False}, {'t': 'Production rejimga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'WORKDIR necha marta ishlatish mumkin?', 'a': [{'t': 'Bir necha marta, har safar papka o\'zgaradi', 'c': True}, {'t': 'Faqat bir marta', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat ikki marta', 'c': False}]},
    ]},

    {'n': 'Dockerfile - ADD, ENTRYPOINT, USER', 't': 30, 'o': 17, 'q': [
        {'t': 'ADD va COPY orasidagi farq nima?', 'a': [{'t': 'ADD URL dan yuklab oladi va arxivlarni ochadi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'COPY tezroq', 'c': False}, {'t': 'ADD xavflirog', 'c': False}]},
        {'t': 'ENTRYPOINT nima qiladi?', 'a': [{'t': 'Container ishga tushganda bajariladigan asosiy komanda', 'c': True}, {'t': 'Image yaratishda bajariladigan komanda', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Port ochadi', 'c': False}]},
        {'t': 'CMD va ENTRYPOINT farqi nima?', 'a': [{'t': 'ENTRYPOINT o\'zgartirib bo\'lmaydi, CMD esa o\'zgaradi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'CMD muhimroq', 'c': False}, {'t': 'ENTRYPOINT eski', 'c': False}]},
        {'t': 'USER nima uchun ishlatiladi?', 'a': [{'t': 'Container ichida qaysi foydalanuvchi nomidan ishlashini belgilash', 'c': True}, {'t': 'Yangi foydalanuvchi yaratish', 'c': False}, {'t': 'Parol o\'rnatish', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'USER node nima qiladi?', 'a': [{'t': 'Keyingi komandalar node foydalanuvchisi nomidan bajariladi', 'c': True}, {'t': 'Node.js ni o\'rnatadi', 'c': False}, {'t': 'node nomli papka yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Nima uchun root o\'rniga boshqa USER ishlatish kerak?', 'a': [{'t': 'Xavfsizlik uchun', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'ADD https://example.com/file.tar.gz /app/ nima qiladi?', 'a': [{'t': 'URL dan yuklab oladi va /app ga joylashtiradi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faqat lokal fayllarni nusxalaydi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
    ]},

    {'n': 'Docker Volume - Ma\'lumotlarni saqlash', 't': 30, 'o': 18, 'q': [
        {'t': 'Docker Volume nima?', 'a': [{'t': 'Container ma\'lumotlarini saqlash uchun maxsus joy', 'c': True}, {'t': 'Ovoz balandligi', 'c': False}, {'t': 'Container hajmi', 'c': False}, {'t': 'Image hajmi', 'c': False}]},
        {'t': 'Volume nima uchun kerak?', 'a': [{'t': 'Container o\'chirilganda ham ma\'lumotlar saqlanishi uchun', 'c': True}, {'t': 'Container tezroq ishlashi uchun', 'c': False}, {'t': 'Xotira tejash uchun', 'c': False}, {'t': 'Kerak emas', 'c': False}]},
        {'t': 'docker volume create nima qiladi?', 'a': [{'t': 'Yangi volume yaratadi', 'c': True}, {'t': 'Container yaratadi', 'c': False}, {'t': 'Image yaratadi', 'c': False}, {'t': 'Papka yaratadi', 'c': False}]},
        {'t': 'docker volume ls nima qiladi?', 'a': [{'t': 'Barcha volumelarni ko\'rsatadi', 'c': True}, {'t': 'Containerlarni ko\'rsatadi', 'c': False}, {'t': 'Imagelarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}]},
        {'t': 'docker run -v mydata:/data nima qiladi?', 'a': [{'t': 'mydata volumeni container /data papkasiga bog\'laydi', 'c': True}, {'t': 'mydata nomli container yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'docker volume rm nima qiladi?', 'a': [{'t': 'Volume ni o\'chiradi', 'c': True}, {'t': 'Container ni o\'chiradi', 'c': False}, {'t': 'Image ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Volume va Bind Mount farqi nima?', 'a': [{'t': 'Volume Docker tomonidan boshqariladi, Bind Mount host papkasi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'Bind Mount yangi', 'c': False}, {'t': 'Volume eski', 'c': False}]},
    ]},

    {'n': 'Docker Network - Tarmoq', 't': 30, 'o': 19, 'q': [
        {'t': 'Docker Network nima?', 'a': [{'t': 'Containerlar orasida aloqa o\'rnatish tarmog\'i', 'c': True}, {'t': 'Internet aloqasi', 'c': False}, {'t': 'Wi-Fi tarmog\'i', 'c': False}, {'t': 'Kabel tarmog\'i', 'c': False}]},
        {'t': 'docker network ls nima qiladi?', 'a': [{'t': 'Barcha tarmoqlarni ko\'rsatadi', 'c': True}, {'t': 'Containerlarni ko\'rsatadi', 'c': False}, {'t': 'Imagelarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}]},
        {'t': 'docker network create nima qiladi?', 'a': [{'t': 'Yangi tarmoq yaratadi', 'c': True}, {'t': 'Container yaratadi', 'c': False}, {'t': 'Image yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Bridge network nima?', 'a': [{'t': 'Standart Docker tarmoq turi', 'c': True}, {'t': 'Ko\'prik qurilmasi', 'c': False}, {'t': 'Xato turi', 'c': False}, {'t': 'Image turi', 'c': False}]},
        {'t': 'Host network nima qiladi?', 'a': [{'t': 'Container host tarmoqdan to\'g\'ridan-to\'g\'ri foydalanadi', 'c': True}, {'t': 'Yangi tarmoq yaratadi', 'c': False}, {'t': 'Tarmoqni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker run --network mynet nima qiladi?', 'a': [{'t': 'Container ni mynet tarmoqqa ulaydi', 'c': True}, {'t': 'mynet nomli container yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Bir tarmoqdagi containerlar bir-birini qanday topadi?', 'a': [{'t': 'Container nomi orqali', 'c': True}, {'t': 'IP manzil orqali', 'c': False}, {'t': 'Topa olmaydi', 'c': False}, {'t': 'Faqat port orqali', 'c': False}]},
    ]},

    {'n': 'docker-compose nima?', 't': 25, 'o': 20, 'q': [
        {'t': 'docker-compose nima?', 'a': [{'t': 'Ko\'p containerli ilovalarni boshqarish vositasi', 'c': True}, {'t': 'Musiqa yaratish dasturi', 'c': False}, {'t': 'Image yaratish vositasi', 'c': False}, {'t': 'Matn muharriri', 'c': False}]},
        {'t': 'docker-compose.yml nima?', 'a': [{'t': 'docker-compose konfiguratsiya fayli', 'c': True}, {'t': 'Dockerfile', 'c': False}, {'t': 'Log fayli', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}]},
        {'t': 'docker-compose up nima qiladi?', 'a': [{'t': 'Barcha containerlarni yaratadi va ishga tushiradi', 'c': True}, {'t': 'Faqat yaratadi', 'c': False}, {'t': 'Faqat ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose down nima qiladi?', 'a': [{'t': 'Barcha containerlarni to\'xtatadi va o\'chiradi', 'c': True}, {'t': 'Faqat to\'xtatadi', 'c': False}, {'t': 'Faqat o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose nima uchun foydali?', 'a': [{'t': 'Ko\'p containerli ilovalarni oson boshqarish uchun', 'c': True}, {'t': 'Bitta container uchun', 'c': False}, {'t': 'Faqat test uchun', 'c': False}, {'t': 'Foydasi yo\'q', 'c': False}]},
        {'t': 'docker-compose.yml da services nima?', 'a': [{'t': 'Yaratilishi kerak bo\'lgan containerlar ro\'yxati', 'c': True}, {'t': 'Xizmatlar ro\'yxati', 'c': False}, {'t': 'Fayllar ro\'yxati', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'docker-compose - Asosiy komandalar', 't': 30, 'o': 21, 'q': [
        {'t': 'docker-compose ps nima qiladi?', 'a': [{'t': 'docker-compose containerlarini ko\'rsatadi', 'c': True}, {'t': 'Barcha containerlarni ko\'rsatadi', 'c': False}, {'t': 'Imagelarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose logs nima qiladi?', 'a': [{'t': 'Barcha servislarnig loglarini ko\'rsatadi', 'c': True}, {'t': 'Faqat bitta servis logini ko\'rsatadi', 'c': False}, {'t': 'Xato loglarini ko\'rsatadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'docker-compose build nima qiladi?', 'a': [{'t': 'Servislardagi imagelarni qayta yaratadi', 'c': True}, {'t': 'Containerlarni yaratadi', 'c': False}, {'t': 'Fayllarni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose start nima qiladi?', 'a': [{'t': 'To\'xtagan containerlarni ishga tushiradi', 'c': True}, {'t': 'Yangi containerlar yaratadi', 'c': False}, {'t': 'Imagelarni yuklab oladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose stop nima qiladi?', 'a': [{'t': 'Ishlab turgan containerlarni to\'xtatadi', 'c': True}, {'t': 'Containerlarni o\'chiradi', 'c': False}, {'t': 'Imagelarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose restart nima qiladi?', 'a': [{'t': 'Barcha servislarni qayta ishga tushiradi', 'c': True}, {'t': 'Docker ni qayta ishga tushiradi', 'c': False}, {'t': 'Kompyuterni qayta ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker-compose exec web bash nima qiladi?', 'a': [{'t': 'web servisi containeriga bash orqali kiradi', 'c': True}, {'t': 'web servisini o\'chiradi', 'c': False}, {'t': 'bash ni o\'rnatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'docker-compose.yml - Konfiguratsiya', 't': 30, 'o': 22, 'q': [
        {'t': 'version: "3" nima bildiradi?', 'a': [{'t': 'docker-compose fayl formatining versiyasi', 'c': True}, {'t': 'Docker versiyasi', 'c': False}, {'t': 'Ilova versiyasi', 'c': False}, {'t': 'Container versiyasi', 'c': False}]},
        {'t': 'services: nima uchun?', 'a': [{'t': 'Containerlar (servislar) ro\'yxatini boshlash uchun', 'c': True}, {'t': 'Xizmatlar ro\'yxati uchun', 'c': False}, {'t': 'Fayllar ro\'yxati uchun', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'image: nginx nima qiladi?', 'a': [{'t': 'nginx image dan container yaratadi', 'c': True}, {'t': 'nginx ni o\'rnatadi', 'c': False}, {'t': 'nginx faylini yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'build: . nima bildiradi?', 'a': [{'t': 'Joriy papkadagi Dockerfile dan image yaratadi', 'c': True}, {'t': 'Nuqta nomli fayl yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'ports: - "8080:80" nima qiladi?', 'a': [{'t': 'Host 8080 ni container 80 ga bog\'laydi', 'c': True}, {'t': '8080 ta port ochadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'volumes: - ./data:/app/data nima qiladi?', 'a': [{'t': 'Host ./data ni container /app/data ga bog\'laydi', 'c': True}, {'t': 'data nomli volume yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'environment: nima uchun?', 'a': [{'t': 'Environment o\'zgaruvchilarini o\'rnatish uchun', 'c': True}, {'t': 'Muhit sozlamalari uchun', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},

    {'n': 'docker-compose - depends_on va networks', 't': 25, 'o': 23, 'q': [
        {'t': 'depends_on nima qiladi?', 'a': [{'t': 'Servislar ishga tushish tartibini belgilaydi', 'c': True}, {'t': 'Bog\'liqliklarni o\'rnatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'depends_on: - db nima bildiradi?', 'a': [{'t': 'Bu servis db servisidan keyin ishga tushadi', 'c': True}, {'t': 'Bu servis db ga bog\'liq emas', 'c': False}, {'t': 'db ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'networks: nima uchun?', 'a': [{'t': 'Servislarni tarmoqlarga ulash uchun', 'c': True}, {'t': 'Internet sozlamalari uchun', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'restart: always nima qiladi?', 'a': [{'t': 'Container to\'xtaganda avtomatik qayta ishga tushiradi', 'c': True}, {'t': 'Har doim qayta ishga tushiradi', 'c': False}, {'t': 'Hech qachon qayta ishga tushmaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'command: nima uchun?', 'a': [{'t': 'Container ishga tushganda bajariladigan komandani o\'zgartirish', 'c': True}, {'t': 'Yangi komanda yaratish', 'c': False}, {'t': 'Xato', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'container_name: myapp nima qiladi?', 'a': [{'t': 'Container ga aniq nom beradi', 'c': True}, {'t': 'Servis nomini o\'zgartiradi', 'c': False}, {'t': 'Image nomini o\'zgartiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Docker Registry - Image saqlash', 't': 25, 'o': 24, 'q': [
        {'t': 'Docker Registry nima?', 'a': [{'t': 'Docker imagelarni saqlash va tarqatish xizmati', 'c': True}, {'t': 'Ro\'yxatdan o\'tish tizimi', 'c': False}, {'t': 'Container boshqaruv tizimi', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}]},
        {'t': 'Docker Hub nima?', 'a': [{'t': 'Eng mashhur ommaviy Docker Registry', 'c': True}, {'t': 'Docker o\'rnatish dasturi', 'c': False}, {'t': 'Docker versiyasi', 'c': False}, {'t': 'Docker komandasi', 'c': False}]},
        {'t': 'docker login nima qiladi?', 'a': [{'t': 'Docker Hub ga kirish', 'c': True}, {'t': 'Docker ni ishga tushirish', 'c': False}, {'t': 'Container ga kirish', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker push nima qiladi?', 'a': [{'t': 'Image ni registry ga yuklaydi', 'c': True}, {'t': 'Container ni ishga tushiradi', 'c': False}, {'t': 'Image ni yuklab oladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker tag myapp username/myapp nima qiladi?', 'a': [{'t': 'Image ga yangi nom (tag) beradi', 'c': True}, {'t': 'Image ni o\'chiradi', 'c': False}, {'t': 'Image ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Private registry nima?', 'a': [{'t': 'Shaxsiy yoki korporativ image saqlash xizmati', 'c': True}, {'t': 'Yashirin registry', 'c': False}, {'t': 'Pullik registry', 'c': False}, {'t': 'Xato', 'c': False}]},
    ]},

    {'n': 'docker push va pull - Image ulashish', 't': 25, 'o': 25, 'q': [
        {'t': 'docker push username/myapp nima qiladi?', 'a': [{'t': 'myapp image ni Docker Hub ga yuklaydi', 'c': True}, {'t': 'Image ni yuklab oladi', 'c': False}, {'t': 'Container ni ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker push dan oldin nima qilish kerak?', 'a': [{'t': 'docker login va docker tag', 'c': True}, {'t': 'Faqat docker build', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Faqat docker run', 'c': False}]},
        {'t': 'docker pull username/myapp nima qiladi?', 'a': [{'t': 'Docker Hub dan myapp image ni yuklab oladi', 'c': True}, {'t': 'Image ni yuklaydi', 'c': False}, {'t': 'Container ni ishga tushiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Image nomida username nima uchun?', 'a': [{'t': 'Docker Hub dagi foydalanuvchi yoki tashkilot nomi', 'c': True}, {'t': 'Kompyuter foydalanuvchisi', 'c': False}, {'t': 'Container nomi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'docker push qachon ishlatiladi?', 'a': [{'t': 'O\'z imagelarini boshqalar bilan ulashish uchun', 'c': True}, {'t': 'Har doim image yaratgandan keyin', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}]},
        {'t': 'docker pull qachon kerak?', 'a': [{'t': 'Boshqa odamlarning imagelarini ishlatish uchun', 'c': True}, {'t': 'Har doim container yaratishdan oldin', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}]},
    ]},

    {'n': 'Docker Best Practices - Yaxshi amaliyotlar', 't': 30, 'o': 26, 'q': [
        {'t': '.dockerignore nima?', 'a': [{'t': 'Image ga qo\'shilmasligi kerak bo\'lgan fayllar ro\'yxati', 'c': True}, {'t': 'Docker sozlamalari', 'c': False}, {'t': 'Xato loglari', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}]},
        {'t': 'Nima uchun image hajmini kichik saqlash kerak?', 'a': [{'t': 'Tezroq yuklanadi va kam joy egallaydi', 'c': True}, {'t': 'Majburiy', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Faqat chiroyli ko\'rinish uchun', 'c': False}]},
        {'t': 'Alpine image nima?', 'a': [{'t': 'Juda kichik hajmli Linux distributivi', 'c': True}, {'t': 'Tog\' nomi', 'c': False}, {'t': 'Docker versiyasi', 'c': False}, {'t': 'Dasturlash tili', 'c': False}]},
        {'t': 'Multi-stage build nima?', 'a': [{'t': 'Bir necha bosqichda image yaratish, hajmni kamaytirish uchun', 'c': True}, {'t': 'Ko\'p containerlar yaratish', 'c': False}, {'t': 'Ko\'p imagelar yaratish', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Dockerfile da RUN komandalarini birlashtirishning foydasi nima?', 'a': [{'t': 'Layerlar sonini kamaytiradi, image kichikroq bo\'ladi', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Xavfsizroq', 'c': False}, {'t': 'Foydasi yo\'q', 'c': False}]},
        {'t': 'Nima uchun root o\'rniga oddiy user ishlatish kerak?', 'a': [{'t': 'Xavfsizlik uchun', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'COPY va ADD dan qaysi birini ishlatish yaxshiroq?', 'a': [{'t': 'COPY, chunki sodda va aniq', 'c': True}, {'t': 'ADD, chunki ko\'proq imkoniyat', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Ikkalasi ham yomon', 'c': False}]},
    ]},

    {'n': 'Docker Security - Xavfsizlik', 't': 30, 'o': 27, 'q': [
        {'t': 'Docker xavfsizligida eng muhim narsa nima?', 'a': [{'t': 'Root o\'rniga oddiy user ishlatish', 'c': True}, {'t': 'Ko\'p container yaratish', 'c': False}, {'t': 'Katta image ishlatish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Nima uchun official imagelarni ishlatish yaxshi?', 'a': [{'t': 'Xavfsiz va tekshirilgan', 'c': True}, {'t': 'Bepul', 'c': False}, {'t': 'Katta hajmli', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'Image ni qayerdan yuklab olish xavfsizroq?', 'a': [{'t': 'Docker Hub dan official imagelar', 'c': True}, {'t': 'Istalgan joydan', 'c': False}, {'t': 'Noma\'lum manbalardan', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'Secrets (sirlar) ni qanday saqlash kerak?', 'a': [{'t': 'Docker secrets yoki environment variables orqali', 'c': True}, {'t': 'Dockerfile da', 'c': False}, {'t': 'Image ichida', 'c': False}, {'t': 'Oddiy faylda', 'c': False}]},
        {'t': 'Parollarni Dockerfile ga yozish mumkinmi?', 'a': [{'t': 'Yo\'q, juda xavfli', 'c': True}, {'t': 'Ha, muammo yo\'q', 'c': False}, {'t': 'Ba\'zan mumkin', 'c': False}, {'t': 'Majburiy', 'c': False}]},
        {'t': 'Container ni read-only qilishning foydasi nima?', 'a': [{'t': 'Xavfsizlikni oshiradi, o\'zgartirish mumkin emas', 'c': True}, {'t': 'Tezroq ishlaydi', 'c': False}, {'t': 'Kam joy egallaydi', 'c': False}, {'t': 'Foydasi yo\'q', 'c': False}]},
        {'t': 'docker scan nima qiladi?', 'a': [{'t': 'Image dagi xavfsizlik zaifliklarini tekshiradi', 'c': True}, {'t': 'Container ni skanerlaydi', 'c': False}, {'t': 'Fayllarni skanerlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'Docker Monitoring - Monitoring qilish', 't': 25, 'o': 28, 'q': [
        {'t': 'docker stats nima qiladi?', 'a': [{'t': 'Containerlarning CPU, RAM ishlatilishini ko\'rsatadi', 'c': True}, {'t': 'Statistika yaratadi', 'c': False}, {'t': 'Container ni to\'xtatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker top nima qiladi?', 'a': [{'t': 'Container ichidagi jarayonlarni ko\'rsatadi', 'c': True}, {'t': 'Eng yaxshi containerni ko\'rsatadi', 'c': False}, {'t': 'Container ni yuqoriga ko\'taradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker events nima uchun?', 'a': [{'t': 'Docker hodisalarini real vaqtda kuzatish', 'c': True}, {'t': 'Tadbirlar ro\'yxatini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'docker system df nima qiladi?', 'a': [{'t': 'Docker obyektlari egallagan joyni ko\'rsatadi', 'c': True}, {'t': 'Disk formatini ko\'rsatadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'docker system prune nima qiladi?', 'a': [{'t': 'Ishlatilmayotgan obyektlarni o\'chiradi', 'c': True}, {'t': 'Barcha containerlarni o\'chiradi', 'c': False}, {'t': 'Docker ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Nima uchun monitoring muhim?', 'a': [{'t': 'Muammolarni erta aniqlash va resurslarni boshqarish', 'c': True}, {'t': 'Majburiy', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}, {'t': 'Faqat katta loyihalarda', 'c': False}]},
    ]},

    {'n': 'Docker Troubleshooting - Muammolarni hal qilish', 't': 30, 'o': 29, 'q': [
        {'t': 'Container ishga tushmasa birinchi nima qilish kerak?', 'a': [{'t': 'docker logs bilan loglarni tekshirish', 'c': True}, {'t': 'Kompyuterni qayta ishga tushirish', 'c': False}, {'t': 'Docker ni o\'chirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Port band bo\'lsa nima qilish kerak?', 'a': [{'t': 'Boshqa port ishlatish yoki band qilgan jarayonni to\'xtatish', 'c': True}, {'t': 'Kompyuterni qayta ishga tushirish', 'c': False}, {'t': 'Docker ni o\'chirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Image not found xatosi nima degani?', 'a': [{'t': 'Image lokal yo\'q, docker pull qilish kerak', 'c': True}, {'t': 'Docker ishlamayapti', 'c': False}, {'t': 'Disk to\'lgan', 'c': False}, {'t': 'Internet yo\'q', 'c': False}]},
        {'t': 'Container darhol to\'xtab qolsa nima qilish kerak?', 'a': [{'t': 'docker logs va docker inspect bilan sabab topish', 'c': True}, {'t': 'Qayta ishga tushirish', 'c': False}, {'t': 'O\'chirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Disk to\'lsa nima qilish kerak?', 'a': [{'t': 'docker system prune bilan tozalash', 'c': True}, {'t': 'Kompyuterni formatlash', 'c': False}, {'t': 'Docker ni o\'chirish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Network muammosi bo\'lsa nima tekshirish kerak?', 'a': [{'t': 'docker network ls va container network sozlamalarini', 'c': True}, {'t': 'Internet aloqasini', 'c': False}, {'t': 'Wi-Fi ni', 'c': False}, {'t': 'Hech narsani', 'c': False}]},
        {'t': 'Permission denied xatosi nima degani?', 'a': [{'t': 'Ruxsat yo\'q, sudo ishlatish yoki user qo\'shish kerak', 'c': True}, {'t': 'Docker ishlamayapti', 'c': False}, {'t': 'Fayl yo\'q', 'c': False}, {'t': 'Disk to\'lgan', 'c': False}]},
    ]},

    {'n': 'Docker Production - Ishlab chiqarishda ishlatish', 't': 30, 'o': 30, 'q': [
        {'t': 'Production da Docker ishlatishning afzalliklari nima?', 'a': [{'t': 'Bir xil muhit, oson deploy, masshtablanish', 'c': True}, {'t': 'Faqat bepul', 'c': False}, {'t': 'Faqat tez', 'c': False}, {'t': 'Afzalligi yo\'q', 'c': False}]},
        {'t': 'Docker Swarm nima?', 'a': [{'t': 'Docker ning o\'z orkestrlash vositasi', 'c': True}, {'t': 'Ko\'p containerlar to\'plami', 'c': False}, {'t': 'Xato turi', 'c': False}, {'t': 'Image turi', 'c': False}]},
        {'t': 'Kubernetes nima?', 'a': [{'t': 'Containerlarni boshqarish va orkestrlash platformasi', 'c': True}, {'t': 'Docker versiyasi', 'c': False}, {'t': 'Dasturlash tili', 'c': False}, {'t': 'Ma\'lumotlar bazasi', 'c': False}]},
        {'t': 'Health check nima uchun kerak?', 'a': [{'t': 'Container sog\'ligini tekshirish va avtomatik qayta ishga tushirish', 'c': True}, {'t': 'Shifokorga ko\'rsatish uchun', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Kerak emas', 'c': False}]},
        {'t': 'Rolling update nima?', 'a': [{'t': 'Containerlarni asta-sekin yangilash, downtime siz', 'c': True}, {'t': 'Tez yangilash', 'c': False}, {'t': 'Avtomatik yangilash', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': 'Load balancer nima uchun kerak?', 'a': [{'t': 'Trafikni bir necha container orasida taqsimlash', 'c': True}, {'t': 'Yukni kamaytirish', 'c': False}, {'t': 'Majburiy', 'c': False}, {'t': 'Kerak emas', 'c': False}]},
        {'t': 'Production da qanday imagelarni ishlatish kerak?', 'a': [{'t': 'Kichik, xavfsiz, versiyalangan imagelar', 'c': True}, {'t': 'Eng katta imagelar', 'c': False}, {'t': 'latest tag bilan', 'c': False}, {'t': 'Istalgan imagelar', 'c': False}]},
        {'t': 'CI/CD da Docker qanday ishlatiladi?', 'a': [{'t': 'Build, test va deploy jarayonlarini avtomatlashtirish', 'c': True}, {'t': 'Faqat test uchun', 'c': False}, {'t': 'Faqat deploy uchun', 'c': False}, {'t': 'Ishlatilmaydi', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subj = get_or_create_docker()
    add_topics(subj, T)
    print(f"\n✅ Docker: {len(T)} ta mavzu qo'shildi!")
