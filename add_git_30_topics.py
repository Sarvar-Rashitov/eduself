"""
GIT COMANDALAR - 30 TA MAVZU (ketma-ket o'rgatib boruvchi, har birida 5-10 test)
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, SubjectCategory, Topic, Question, Answer

def get_or_create_git():
    cat, _ = SubjectCategory.objects.get_or_create(slug='dasturlash', defaults={'name': 'Dasturlash', 'icon': 'bi-code-slash', 'order': 2, 'is_active': True})
    subj, _ = Subject.objects.get_or_create(name='Git', defaults={'category': cat, 'description': 'Git - Versiya nazorat tizimi', 'icon': 'bi-git', 'order': 27, 'is_active': True})
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
    {'n': 'Git ga kirish', 't': 20, 'o': 1, 'q': [
        {'t': 'Git nima?', 'a': [{'t': 'Versiya nazorat tizimi', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Operatsion tizim', 'c': False}, {'t': 'Brauzer', 'c': False}]},
        {'t': 'Git ni kim yaratgan?', 'a': [{'t': 'Linus Torvalds', 'c': True}, {'t': 'Bill Gates', 'c': False}, {'t': 'Mark Zuckerberg', 'c': False}, {'t': 'Steve Jobs', 'c': False}]},
        {'t': 'Git nima uchun kerak?', 'a': [{'t': 'Kod o\'zgarishlarini kuzatish uchun', 'c': True}, {'t': 'Fayllarni arxivlash uchun', 'c': False}, {'t': 'Internet orqali suhbatlashish uchun', 'c': False}, {'t': 'Rasm chizish uchun', 'c': False}]},
        {'t': 'Repository nima?', 'a': [{'t': 'Loyihaning barcha fayllar va tarix saqlanadigan joy', 'c': True}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Brauzer', 'c': False}, {'t': 'Operatsion tizim', 'c': False}]},
        {'t': 'Git bilan ishlash uchun nima kerak?', 'a': [{'t': 'Git o\'rnatilgan bo\'lishi kerak', 'c': True}, {'t': 'Faqat internet', 'c': False}, {'t': 'Maxsus litsenziya', 'c': False}, {'t': 'Pullik obuna', 'c': False}]},
    ]},

    {'n': 'git config - Sozlamalar', 't': 25, 'o': 2, 'q': [
        {'t': 'git config nima uchun ishlatiladi?', 'a': [{'t': 'Git sozlamalarini o\'rnatish uchun', 'c': True}, {'t': 'Fayllarni nusxalash uchun', 'c': False}, {'t': 'Repository yaratish uchun', 'c': False}, {'t': 'Commit qilish uchun', 'c': False}]},
        {'t': 'git config --global user.name "Ism" nima qiladi?', 'a': [{'t': 'Foydalanuvchi ismini o\'rnatadi', 'c': True}, {'t': 'Repository yaratadi', 'c': False}, {'t': 'Faylni commit qiladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git config --global user.email nima uchun?', 'a': [{'t': 'Email manzilini o\'rnatish uchun', 'c': True}, {'t': 'Email yuborish uchun', 'c': False}, {'t': 'Parolni o\'zgartirish uchun', 'c': False}, {'t': 'Repository yaratish uchun', 'c': False}]},
        {'t': 'git config --list nima ko\'rsatadi?', 'a': [{'t': 'Barcha sozlamalarni', 'c': True}, {'t': 'Fayllar ro\'yxatini', 'c': False}, {'t': 'Commitlar tarixini', 'c': False}, {'t': 'Branchlar ro\'yxatini', 'c': False}]},
        {'t': '--global parametri nima uchun?', 'a': [{'t': 'Sozlamani barcha repositorylar uchun o\'rnatadi', 'c': True}, {'t': 'Faqat joriy repository uchun', 'c': False}, {'t': 'Internetga ulanadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'git config user.name nima qiladi?', 'a': [{'t': 'Joriy ismni ko\'rsatadi', 'c': True}, {'t': 'Ismni o\'chiradi', 'c': False}, {'t': 'Yangi foydalanuvchi yaratadi', 'c': False}, {'t': 'Repository yaratadi', 'c': False}]},
    ]},

    {'n': 'git init - Repository yaratish', 't': 20, 'o': 3, 'q': [
        {'t': 'git init nima qiladi?', 'a': [{'t': 'Yangi Git repository yaratadi', 'c': True}, {'t': 'Fayllarni commit qiladi', 'c': False}, {'t': 'Repository ni o\'chiradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git init qayerda ishlatiladi?', 'a': [{'t': 'Loyiha papkasida', 'c': True}, {'t': 'Istalgan joyda', 'c': False}, {'t': 'Faqat Desktop da', 'c': False}, {'t': 'Faqat ildiz papkada', 'c': False}]},
        {'t': 'git init dan keyin nima paydo bo\'ladi?', 'a': [{'t': '.git papkasi yaratiladi', 'c': True}, {'t': 'Barcha fayllar o\'chiriladi', 'c': False}, {'t': 'Yangi fayllar yaratiladi', 'c': False}, {'t': 'Hech narsa o\'zgarmaydi', 'c': False}]},
        {'t': '.git papkasi nima uchun kerak?', 'a': [{'t': 'Git ma\'lumotlari saqlanadi', 'c': True}, {'t': 'Loyiha fayllari saqlanadi', 'c': False}, {'t': 'Rasmlar saqlanadi', 'c': False}, {'t': 'Hech narsa saqlanmaydi', 'c': False}]},
        {'t': 'git init bir necha marta ishlatish mumkinmi?', 'a': [{'t': 'Ha, lekin kerak emas', 'c': True}, {'t': 'Yo\'q, xato beradi', 'c': False}, {'t': 'Yo\'q, repository buziladi', 'c': False}, {'t': 'Faqat bir marta', 'c': False}]},
    ]},

    {'n': 'git status - Holat ko\'rish', 't': 25, 'o': 4, 'q': [
        {'t': 'git status nima qiladi?', 'a': [{'t': 'Repository holatini ko\'rsatadi', 'c': True}, {'t': 'Fayllarni commit qiladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'git status qanday ma\'lumot beradi?', 'a': [{'t': 'O\'zgargan fayllar va staging holati', 'c': True}, {'t': 'Faqat commit tarixini', 'c': False}, {'t': 'Faqat branchlarni', 'c': False}, {'t': 'Faqat remote repositoryni', 'c': False}]},
        {'t': 'Untracked files nima?', 'a': [{'t': 'Git tomonidan kuzatilmayotgan yangi fayllar', 'c': True}, {'t': 'O\'chirilgan fayllar', 'c': False}, {'t': 'Commit qilingan fayllar', 'c': False}, {'t': 'Xato fayllari', 'c': False}]},
        {'t': 'Modified files nima?', 'a': [{'t': 'O\'zgartirilgan lekin commit qilinmagan fayllar', 'c': True}, {'t': 'Yangi yaratilgan fayllar', 'c': False}, {'t': 'O\'chirilgan fayllar', 'c': False}, {'t': 'Commit qilingan fayllar', 'c': False}]},
        {'t': 'git status -s nima qiladi?', 'a': [{'t': 'Qisqa formatda ko\'rsatadi', 'c': True}, {'t': 'Fayllarni saqlaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git status qachon ishlatiladi?', 'a': [{'t': 'Har doim, holat tekshirish uchun', 'c': True}, {'t': 'Faqat commit oldidan', 'c': False}, {'t': 'Faqat push oldidan', 'c': False}, {'t': 'Faqat bir marta', 'c': False}]},
    ]},

    {'n': 'git add - Staging ga qo\'shish', 't': 30, 'o': 5, 'q': [
        {'t': 'git add nima qiladi?', 'a': [{'t': 'Fayllarni staging area ga qo\'shadi', 'c': True}, {'t': 'Fayllarni commit qiladi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Repository yaratadi', 'c': False}]},
        {'t': 'Staging area nima?', 'a': [{'t': 'Commit qilishga tayyor fayllar joyi', 'c': True}, {'t': 'O\'chirilgan fayllar joyi', 'c': False}, {'t': 'Remote repository', 'c': False}, {'t': 'Branch nomi', 'c': False}]},
        {'t': 'git add file.txt nima qiladi?', 'a': [{'t': 'file.txt ni staging ga qo\'shadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni commit qiladi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}]},
        {'t': 'git add . nima qiladi?', 'a': [{'t': 'Barcha o\'zgarishlarni staging ga qo\'shadi', 'c': True}, {'t': 'Faqat bitta faylni qo\'shadi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'git add *.js nima qiladi?', 'a': [{'t': 'Barcha .js fayllarni staging ga qo\'shadi', 'c': True}, {'t': 'Faqat bitta .js faylni qo\'shadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git add -A nima qiladi?', 'a': [{'t': 'Barcha o\'zgarishlar va o\'chirilgan fayllarni qo\'shadi', 'c': True}, {'t': 'Faqat yangi fayllarni qo\'shadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git add dan keyin nima qilish kerak?', 'a': [{'t': 'git commit qilish kerak', 'c': True}, {'t': 'git init qilish kerak', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'git status qilish shart', 'c': False}]},
    ]},

    {'n': 'git commit - O\'zgarishlarni saqlash', 't': 30, 'o': 6, 'q': [
        {'t': 'git commit nima qiladi?', 'a': [{'t': 'Staging dagi o\'zgarishlarni tarixga saqlaydi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Repository yaratadi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git commit -m "xabar" nima uchun?', 'a': [{'t': 'Commit xabarini yozish uchun', 'c': True}, {'t': 'Faylni o\'chirish uchun', 'c': False}, {'t': 'Branch yaratish uchun', 'c': False}, {'t': 'Repository yaratish uchun', 'c': False}]},
        {'t': 'Commit xabari nima uchun muhim?', 'a': [{'t': 'Nima o\'zgarganini tushunish uchun', 'c': True}, {'t': 'Git ishlamaydi xabarsiz', 'c': False}, {'t': 'Faqat bezak uchun', 'c': False}, {'t': 'Muhim emas', 'c': False}]},
        {'t': 'git commit -am "xabar" nima qiladi?', 'a': [{'t': 'add va commit ni birga bajaradi', 'c': True}, {'t': 'Faqat commit qiladi', 'c': False}, {'t': 'Faqat add qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git commit --amend nima uchun?', 'a': [{'t': 'Oxirgi commitni o\'zgartirish uchun', 'c': True}, {'t': 'Yangi commit yaratish uchun', 'c': False}, {'t': 'Commitni o\'chirish uchun', 'c': False}, {'t': 'Branch yaratish uchun', 'c': False}]},
        {'t': 'Commit qilishdan oldin nima qilish kerak?', 'a': [{'t': 'git add bilan fayllarni staging ga qo\'shish', 'c': True}, {'t': 'git push qilish', 'c': False}, {'t': 'git pull qilish', 'c': False}, {'t': 'Hech narsa', 'c': False}]},
        {'t': 'Yaxshi commit xabari qanday bo\'lishi kerak?', 'a': [{'t': 'Qisqa va aniq, nima qilganini tushuntiruvchi', 'c': True}, {'t': 'Juda uzun va batafsil', 'c': False}, {'t': 'Faqat bitta so\'z', 'c': False}, {'t': 'Muhim emas', 'c': False}]},
    ]},

    {'n': 'git log - Tarix ko\'rish', 't': 25, 'o': 7, 'q': [
        {'t': 'git log nima qiladi?', 'a': [{'t': 'Commitlar tarixini ko\'rsatadi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git log qanday ma\'lumot beradi?', 'a': [{'t': 'Commit hash, muallif, sana va xabar', 'c': True}, {'t': 'Faqat fayllar ro\'yxati', 'c': False}, {'t': 'Faqat branchlar', 'c': False}, {'t': 'Faqat xatolar', 'c': False}]},
        {'t': 'git log --oneline nima qiladi?', 'a': [{'t': 'Har bir commitni bitta qatorda ko\'rsatadi', 'c': True}, {'t': 'Faqat oxirgi commitni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}]},
        {'t': 'git log -n 5 nima qiladi?', 'a': [{'t': 'Oxirgi 5 ta commitni ko\'rsatadi', 'c': True}, {'t': '5-commitni o\'chiradi', 'c': False}, {'t': '5 ta branch yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git log --graph nima uchun?', 'a': [{'t': 'Branchlarni grafik ko\'rinishda ko\'rsatadi', 'c': True}, {'t': 'Rasmlar yaratadi', 'c': False}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git log file.txt nima qiladi?', 'a': [{'t': 'Faqat file.txt ga tegishli commitlarni ko\'rsatadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git diff - Farqlarni ko\'rish', 't': 25, 'o': 8, 'q': [
        {'t': 'git diff nima qiladi?', 'a': [{'t': 'O\'zgarishlar farqini ko\'rsatadi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git diff qanday farqni ko\'rsatadi?', 'a': [{'t': 'Working directory va staging orasidagi', 'c': True}, {'t': 'Faqat commitlar orasidagi', 'c': False}, {'t': 'Faqat branchlar orasidagi', 'c': False}, {'t': 'Hech qanday farq yo\'q', 'c': False}]},
        {'t': 'git diff --staged nima qiladi?', 'a': [{'t': 'Staging va oxirgi commit orasidagi farqni ko\'rsatadi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git diff HEAD nima qiladi?', 'a': [{'t': 'Barcha o\'zgarishlarni oxirgi commit bilan solishtiradi', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git diff commit1 commit2 nima qiladi?', 'a': [{'t': 'Ikki commit orasidagi farqni ko\'rsatadi', 'c': True}, {'t': 'Commitlarni o\'chiradi', 'c': False}, {'t': 'Yangi commit yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git diff file.txt nima qiladi?', 'a': [{'t': 'Faqat file.txt dagi o\'zgarishlarni ko\'rsatadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git branch - Branchlar bilan ishlash', 't': 30, 'o': 9, 'q': [
        {'t': 'Branch nima?', 'a': [{'t': 'Mustaqil ishlov berish yo\'li', 'c': True}, {'t': 'Fayl turi', 'c': False}, {'t': 'Commit turi', 'c': False}, {'t': 'Repository turi', 'c': False}]},
        {'t': 'git branch nima qiladi?', 'a': [{'t': 'Barcha branchlarni ko\'rsatadi', 'c': True}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git branch feature nima qiladi?', 'a': [{'t': 'feature nomli yangi branch yaratadi', 'c': True}, {'t': 'feature branchini o\'chiradi', 'c': False}, {'t': 'feature branchiga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git branch -d feature nima qiladi?', 'a': [{'t': 'feature branchini o\'chiradi', 'c': True}, {'t': 'feature branchini yaratadi', 'c': False}, {'t': 'feature branchiga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git branch -D nima uchun?', 'a': [{'t': 'Majburiy o\'chirish uchun', 'c': True}, {'t': 'Yangi branch yaratish uchun', 'c': False}, {'t': 'Branch nomini o\'zgartirish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git branch -m old new nima qiladi?', 'a': [{'t': 'Branch nomini o\'zgartiradi', 'c': True}, {'t': 'Yangi branch yaratadi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Asosiy branch odatda qanday nomlanadi?', 'a': [{'t': 'main yoki master', 'c': True}, {'t': 'primary', 'c': False}, {'t': 'default', 'c': False}, {'t': 'root', 'c': False}]},
    ]},

    {'n': 'git checkout - Branch o\'zgartirish', 't': 25, 'o': 10, 'q': [
        {'t': 'git checkout nima qiladi?', 'a': [{'t': 'Boshqa branchga o\'tadi', 'c': True}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git checkout feature nima qiladi?', 'a': [{'t': 'feature branchiga o\'tadi', 'c': True}, {'t': 'feature branchini yaratadi', 'c': False}, {'t': 'feature branchini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git checkout -b new nima qiladi?', 'a': [{'t': 'Yangi branch yaratadi va unga o\'tadi', 'c': True}, {'t': 'Faqat branch yaratadi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git checkout file.txt nima qiladi?', 'a': [{'t': 'file.txt dagi o\'zgarishlarni bekor qiladi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git checkout . nima qiladi?', 'a': [{'t': 'Barcha o\'zgarishlarni bekor qiladi', 'c': True}, {'t': 'Yangi branch yaratadi', 'c': False}, {'t': 'Commit qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git checkout commitHash nima qiladi?', 'a': [{'t': 'O\'sha commitga o\'tadi (detached HEAD)', 'c': True}, {'t': 'Commitni o\'chiradi', 'c': False}, {'t': 'Yangi commit yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git switch - Zamonaviy branch o\'zgartirish', 't': 20, 'o': 11, 'q': [
        {'t': 'git switch nima?', 'a': [{'t': 'Branchlar orasida o\'tish uchun yangi komanda', 'c': True}, {'t': 'Fayllarni almashtirish komandasi', 'c': False}, {'t': 'Commitlarni almashtirish', 'c': False}, {'t': 'Repository almashtirish', 'c': False}]},
        {'t': 'git switch feature nima qiladi?', 'a': [{'t': 'feature branchiga o\'tadi', 'c': True}, {'t': 'feature branchini yaratadi', 'c': False}, {'t': 'feature branchini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git switch -c new nima qiladi?', 'a': [{'t': 'Yangi branch yaratadi va unga o\'tadi', 'c': True}, {'t': 'Faqat branch yaratadi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git switch va git checkout farqi nima?', 'a': [{'t': 'switch faqat branchlar uchun, aniqroq', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'switch tezroq ishlaydi', 'c': False}, {'t': 'checkout yangi, switch eski', 'c': False}]},
        {'t': 'git switch - nima qiladi?', 'a': [{'t': 'Oldingi branchga qaytadi', 'c': True}, {'t': 'Xato beradi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
    ]},

    {'n': 'git merge - Branchlarni birlashtirish', 't': 30, 'o': 12, 'q': [
        {'t': 'git merge nima qiladi?', 'a': [{'t': 'Ikki branchni birlashtiradi', 'c': True}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git merge feature nima qiladi?', 'a': [{'t': 'feature branchini joriy branchga qo\'shadi', 'c': True}, {'t': 'feature branchini o\'chiradi', 'c': False}, {'t': 'feature branchiga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Merge conflict nima?', 'a': [{'t': 'Bir xil joyda turli o\'zgarishlar bo\'lganda', 'c': True}, {'t': 'Branch topilmaganda', 'c': False}, {'t': 'Commit yo\'qligida', 'c': False}, {'t': 'Internet yo\'qligida', 'c': False}]},
        {'t': 'Merge conflict qanday hal qilinadi?', 'a': [{'t': 'Qo\'lda fayllarni tahrirlash va commit qilish', 'c': True}, {'t': 'git merge --fix', 'c': False}, {'t': 'Avtomatik hal bo\'ladi', 'c': False}, {'t': 'Branch o\'chirish kerak', 'c': False}]},
        {'t': 'Fast-forward merge nima?', 'a': [{'t': 'Konflikt bo\'lmagan oddiy birlashtirish', 'c': True}, {'t': 'Tez merge qilish usuli', 'c': False}, {'t': 'Xato turi', 'c': False}, {'t': 'Branch turi', 'c': False}]},
        {'t': 'git merge --no-ff nima uchun?', 'a': [{'t': 'Har doim merge commit yaratish uchun', 'c': True}, {'t': 'Fast-forward qilish uchun', 'c': False}, {'t': 'Merge qilmaslik uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git merge --abort nima qiladi?', 'a': [{'t': 'Merge jarayonini bekor qiladi', 'c': True}, {'t': 'Merge ni yakunlaydi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
    ]},

    {'n': 'git remote - Masofaviy repositorylar', 't': 25, 'o': 13, 'q': [
        {'t': 'Remote repository nima?', 'a': [{'t': 'Internetdagi yoki tarmoqdagi repository', 'c': True}, {'t': 'Lokal repository', 'c': False}, {'t': 'Branch turi', 'c': False}, {'t': 'Commit turi', 'c': False}]},
        {'t': 'git remote nima qiladi?', 'a': [{'t': 'Remote repositorylar ro\'yxatini ko\'rsatadi', 'c': True}, {'t': 'Remote repository yaratadi', 'c': False}, {'t': 'Remote repository o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git remote -v nima qiladi?', 'a': [{'t': 'Remote repositorylar va ularning URL larini ko\'rsatadi', 'c': True}, {'t': 'Versiyani ko\'rsatadi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git remote add origin URL nima qiladi?', 'a': [{'t': 'origin nomli remote repository qo\'shadi', 'c': True}, {'t': 'Repository yaratadi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'origin nima?', 'a': [{'t': 'Asosiy remote repository ning standart nomi', 'c': True}, {'t': 'Branch nomi', 'c': False}, {'t': 'Commit nomi', 'c': False}, {'t': 'Fayl nomi', 'c': False}]},
        {'t': 'git remote remove origin nima qiladi?', 'a': [{'t': 'origin remote ni o\'chiradi', 'c': True}, {'t': 'Repository o\'chiradi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git clone - Repository nusxalash', 't': 20, 'o': 14, 'q': [
        {'t': 'git clone nima qiladi?', 'a': [{'t': 'Remote repositoryni lokal kompyuterga nusxalaydi', 'c': True}, {'t': 'Fayl nusxalaydi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git clone URL nima qiladi?', 'a': [{'t': 'URL dagi repositoryni yuklab oladi', 'c': True}, {'t': 'URL ni o\'chiradi', 'c': False}, {'t': 'URL yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git clone URL myproject nima qiladi?', 'a': [{'t': 'Repository ni myproject papkasiga yuklab oladi', 'c': True}, {'t': 'Faqat myproject faylini oladi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git clone dan keyin nima bo\'ladi?', 'a': [{'t': 'To\'liq repository va tarix yuklab olinadi', 'c': True}, {'t': 'Faqat oxirgi versiya olinadi', 'c': False}, {'t': 'Faqat fayllar olinadi', 'c': False}, {'t': 'Hech narsa bo\'lmaydi', 'c': False}]},
        {'t': 'git clone --depth 1 nima uchun?', 'a': [{'t': 'Faqat oxirgi commitni olish uchun (shallow clone)', 'c': True}, {'t': 'Bitta faylni olish uchun', 'c': False}, {'t': 'Bitta branchni olish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git push - O\'zgarishlarni yuklash', 't': 25, 'o': 15, 'q': [
        {'t': 'git push nima qiladi?', 'a': [{'t': 'Lokal commitlarni remote ga yuklaydi', 'c': True}, {'t': 'Remote dan yuklab oladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git push origin main nima qiladi?', 'a': [{'t': 'main branchni origin ga yuklaydi', 'c': True}, {'t': 'origin dan main ni yuklab oladi', 'c': False}, {'t': 'main branchini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git push -u origin main nima uchun?', 'a': [{'t': 'Upstream ni o\'rnatadi, keyingi safar faqat git push yetadi', 'c': True}, {'t': 'Fayllarni yangilaydi', 'c': False}, {'t': 'Branch o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git push --force nima qiladi?', 'a': [{'t': 'Majburiy yuklaydi, remote tarixni o\'zgartiradi', 'c': True}, {'t': 'Oddiy push qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'git push --force xavflimi?', 'a': [{'t': 'Ha, boshqalarning ishini yo\'qotishi mumkin', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}, {'t': 'Hech qachon xavfli emas', 'c': False}]},
        {'t': 'git push --all nima qiladi?', 'a': [{'t': 'Barcha branchlarni yuklaydi', 'c': True}, {'t': 'Barcha fayllarni yuklaydi', 'c': False}, {'t': 'Barcha commitlarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git pull - O\'zgarishlarni olish', 't': 25, 'o': 16, 'q': [
        {'t': 'git pull nima qiladi?', 'a': [{'t': 'Remote dan o\'zgarishlarni yuklab oladi va merge qiladi', 'c': True}, {'t': 'Remote ga yuklaydi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git pull origin main nima qiladi?', 'a': [{'t': 'origin/main dan o\'zgarishlarni oladi', 'c': True}, {'t': 'main ni origin ga yuklaydi', 'c': False}, {'t': 'main branchini o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git pull = git fetch + ?', 'a': [{'t': 'git merge', 'c': True}, {'t': 'git push', 'c': False}, {'t': 'git commit', 'c': False}, {'t': 'git add', 'c': False}]},
        {'t': 'git pull --rebase nima qiladi?', 'a': [{'t': 'Merge o\'rniga rebase qiladi', 'c': True}, {'t': 'Oddiy pull qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git pull da conflict bo\'lsa nima qilish kerak?', 'a': [{'t': 'Qo\'lda hal qilib commit qilish', 'c': True}, {'t': 'git pull --fix', 'c': False}, {'t': 'Avtomatik hal bo\'ladi', 'c': False}, {'t': 'Repository o\'chirish', 'c': False}]},
        {'t': 'Qachon git pull qilish kerak?', 'a': [{'t': 'Ishni boshlashdan oldin, yangi o\'zgarishlarni olish uchun', 'c': True}, {'t': 'Faqat ishni tugatgandan keyin', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat bir marta', 'c': False}]},
    ]},

    {'n': 'git fetch - Ma\'lumot olish', 't': 20, 'o': 17, 'q': [
        {'t': 'git fetch nima qiladi?', 'a': [{'t': 'Remote dan ma\'lumot oladi lekin merge qilmaydi', 'c': True}, {'t': 'Remote ga yuklaydi', 'c': False}, {'t': 'Avtomatik merge qiladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git fetch va git pull farqi nima?', 'a': [{'t': 'fetch faqat oladi, pull esa merge ham qiladi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'fetch tezroq', 'c': False}, {'t': 'pull xavfliroq', 'c': False}]},
        {'t': 'git fetch origin nima qiladi?', 'a': [{'t': 'origin dan barcha yangilanishlarni oladi', 'c': True}, {'t': 'origin ga yuklaydi', 'c': False}, {'t': 'origin ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git fetch dan keyin nima qilish kerak?', 'a': [{'t': 'git merge yoki git rebase qilish', 'c': True}, {'t': 'git push qilish', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'git commit qilish', 'c': False}]},
        {'t': 'git fetch --all nima qiladi?', 'a': [{'t': 'Barcha remote lardan ma\'lumot oladi', 'c': True}, {'t': 'Barcha fayllarni oladi', 'c': False}, {'t': 'Barcha branchlarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': '.gitignore - Fayllarni e\'tiborsiz qoldirish', 't': 25, 'o': 18, 'q': [
        {'t': '.gitignore nima?', 'a': [{'t': 'Git tomonidan e\'tiborsiz qoldirilishi kerak bo\'lgan fayllar ro\'yxati', 'c': True}, {'t': 'Git sozlamalari fayli', 'c': False}, {'t': 'Branch nomi', 'c': False}, {'t': 'Commit xabari', 'c': False}]},
        {'t': '.gitignore da nima yoziladi?', 'a': [{'t': 'E\'tiborsiz qoldirilishi kerak bo\'lgan fayl va papka nomlari', 'c': True}, {'t': 'Commit xabarlari', 'c': False}, {'t': 'Branch nomlari', 'c': False}, {'t': 'Foydalanuvchi ismlari', 'c': False}]},
        {'t': '.gitignore da *.log nima bildiradi?', 'a': [{'t': 'Barcha .log fayllarni e\'tiborsiz qoldirish', 'c': True}, {'t': 'Faqat log.txt ni e\'tiborsiz qoldirish', 'c': False}, {'t': 'Hech narsani e\'tiborsiz qoldirmaydi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '.gitignore da node_modules/ nima uchun?', 'a': [{'t': 'node_modules papkasini e\'tiborsiz qoldirish uchun', 'c': True}, {'t': 'node_modules ni yaratish uchun', 'c': False}, {'t': 'node_modules ni o\'chirish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': '.gitignore da # nima?', 'a': [{'t': 'Izoh (comment)', 'c': True}, {'t': 'Maxsus belgi', 'c': False}, {'t': 'Fayl nomi', 'c': False}, {'t': 'Xato', 'c': False}]},
        {'t': '.gitignore da ! nima qiladi?', 'a': [{'t': 'Qoidani inkor qiladi (exception)', 'c': True}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'Qachon .gitignore kerak?', 'a': [{'t': 'Parollar, log fayllar, build fayllar uchun', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat katta loyihalarda', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}]},
    ]},

    {'n': 'git stash - Vaqtinchalik saqlash', 't': 25, 'o': 19, 'q': [
        {'t': 'git stash nima qiladi?', 'a': [{'t': 'O\'zgarishlarni vaqtinchalik saqlaydi', 'c': True}, {'t': 'O\'zgarishlarni o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}]},
        {'t': 'git stash qachon foydali?', 'a': [{'t': 'Branchni o\'zgartirish kerak lekin commit qilmoqchi emasman', 'c': True}, {'t': 'Commit qilish uchun', 'c': False}, {'t': 'Push qilish uchun', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'git stash pop nima qiladi?', 'a': [{'t': 'Oxirgi stash ni qaytaradi va o\'chiradi', 'c': True}, {'t': 'Yangi stash yaratadi', 'c': False}, {'t': 'Barcha stashlarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git stash list nima qiladi?', 'a': [{'t': 'Barcha stashlar ro\'yxatini ko\'rsatadi', 'c': True}, {'t': 'Fayllar ro\'yxatini ko\'rsatadi', 'c': False}, {'t': 'Branchlar ro\'yxatini ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git stash apply nima qiladi?', 'a': [{'t': 'Stash ni qaytaradi lekin o\'chirmaydi', 'c': True}, {'t': 'Stash ni o\'chiradi', 'c': False}, {'t': 'Yangi stash yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git stash drop nima qiladi?', 'a': [{'t': 'Oxirgi stash ni o\'chiradi', 'c': True}, {'t': 'Stash ni qaytaradi', 'c': False}, {'t': 'Yangi stash yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git reset - Commitlarni bekor qilish', 't': 30, 'o': 20, 'q': [
        {'t': 'git reset nima qiladi?', 'a': [{'t': 'Commitlarni bekor qiladi', 'c': True}, {'t': 'Commit yaratadi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Push qiladi', 'c': False}]},
        {'t': 'git reset --soft HEAD~1 nima qiladi?', 'a': [{'t': 'Oxirgi commitni bekor qiladi, o\'zgarishlar staging da qoladi', 'c': True}, {'t': 'Oxirgi commitni o\'chiradi, o\'zgarishlar yo\'qoladi', 'c': False}, {'t': 'Yangi commit yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git reset --mixed HEAD~1 nima qiladi?', 'a': [{'t': 'Oxirgi commitni bekor qiladi, o\'zgarishlar working directory da', 'c': True}, {'t': 'Hamma narsani o\'chiradi', 'c': False}, {'t': 'Yangi commit yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git reset --hard HEAD~1 nima qiladi?', 'a': [{'t': 'Oxirgi commitni va barcha o\'zgarishlarni o\'chiradi', 'c': True}, {'t': 'Faqat commitni o\'chiradi', 'c': False}, {'t': 'Yangi commit yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git reset --hard xavflimi?', 'a': [{'t': 'Ha, o\'zgarishlar butunlay yo\'qoladi', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}, {'t': 'Hech qachon xavfli emas', 'c': False}]},
        {'t': 'git reset file.txt nima qiladi?', 'a': [{'t': 'file.txt ni staging dan chiqaradi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni commit qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'HEAD~1 nima bildiradi?', 'a': [{'t': 'Joriy commitdan 1 ta orqadagi commit', 'c': True}, {'t': 'Birinchi commit', 'c': False}, {'t': 'Oxirgi commit', 'c': False}, {'t': 'Branch nomi', 'c': False}]},
    ]},

    {'n': 'git revert - Xavfsiz bekor qilish', 't': 25, 'o': 21, 'q': [
        {'t': 'git revert nima qiladi?', 'a': [{'t': 'Commitni bekor qiluvchi yangi commit yaratadi', 'c': True}, {'t': 'Commitni o\'chiradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Push qiladi', 'c': False}]},
        {'t': 'git revert va git reset farqi nima?', 'a': [{'t': 'revert tarixni saqlab qoladi, reset esa o\'chiradi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'revert tezroq', 'c': False}, {'t': 'reset xavfsizroq', 'c': False}]},
        {'t': 'git revert commitHash nima qiladi?', 'a': [{'t': 'O\'sha commitni bekor qiluvchi yangi commit yaratadi', 'c': True}, {'t': 'O\'sha commitni o\'chiradi', 'c': False}, {'t': 'O\'sha commitga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git revert qachon ishlatiladi?', 'a': [{'t': 'Public repositoryda, tarixni saqlab qolish kerak bo\'lganda', 'c': True}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat lokal repositoryda', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}]},
        {'t': 'git revert --no-commit nima uchun?', 'a': [{'t': 'Avtomatik commit qilmaslik uchun', 'c': True}, {'t': 'Commit qilish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa qilmaydi', 'c': False}]},
        {'t': 'git revert xavfsizmi?', 'a': [{'t': 'Ha, tarixni saqlab qoladi', 'c': True}, {'t': 'Yo\'q, xavfli', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'git rebase - Tarixni qayta yozish', 't': 30, 'o': 22, 'q': [
        {'t': 'git rebase nima qiladi?', 'a': [{'t': 'Commitlarni boshqa base ga ko\'chiradi', 'c': True}, {'t': 'Commitlarni o\'chiradi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Push qiladi', 'c': False}]},
        {'t': 'git rebase main nima qiladi?', 'a': [{'t': 'Joriy branchni main ustiga qayta quradi', 'c': True}, {'t': 'main ni o\'chiradi', 'c': False}, {'t': 'main ga merge qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git rebase va git merge farqi nima?', 'a': [{'t': 'rebase chiziqli tarix yaratadi, merge esa tarmoqlanadi', 'c': True}, {'t': 'Farq yo\'q', 'c': False}, {'t': 'rebase tezroq', 'c': False}, {'t': 'merge yangi', 'c': False}]},
        {'t': 'git rebase -i nima uchun?', 'a': [{'t': 'Interaktiv rebase, commitlarni tahrirlash uchun', 'c': True}, {'t': 'Ma\'lumot import qilish uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'git rebase --continue nima qiladi?', 'a': [{'t': 'Conflict hal qilingandan keyin rebase ni davom ettiradi', 'c': True}, {'t': 'Rebase ni boshlaydi', 'c': False}, {'t': 'Rebase ni bekor qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git rebase --abort nima qiladi?', 'a': [{'t': 'Rebase ni bekor qiladi', 'c': True}, {'t': 'Rebase ni yakunlaydi', 'c': False}, {'t': 'Rebase ni boshlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'Public branchda rebase qilish kerakmi?', 'a': [{'t': 'Yo\'q, boshqalarning ishini buzadi', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
    ]},

    {'n': 'git tag - Versiyalarni belgilash', 't': 25, 'o': 23, 'q': [
        {'t': 'git tag nima?', 'a': [{'t': 'Commitga nom berish, versiya belgilash', 'c': True}, {'t': 'Branch turi', 'c': False}, {'t': 'Fayl turi', 'c': False}, {'t': 'Commit turi', 'c': False}]},
        {'t': 'git tag nima qiladi?', 'a': [{'t': 'Barcha taglar ro\'yxatini ko\'rsatadi', 'c': True}, {'t': 'Tag yaratadi', 'c': False}, {'t': 'Tag o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git tag v1.0.0 nima qiladi?', 'a': [{'t': 'Joriy commitga v1.0.0 tag qo\'yadi', 'c': True}, {'t': 'v1.0.0 commitga o\'tadi', 'c': False}, {'t': 'v1.0.0 ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git tag -a v1.0.0 -m "xabar" nima uchun?', 'a': [{'t': 'Annotated tag yaratadi, xabar bilan', 'c': True}, {'t': 'Oddiy tag yaratadi', 'c': False}, {'t': 'Tag o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git push origin v1.0.0 nima qiladi?', 'a': [{'t': 'v1.0.0 tagni remote ga yuklaydi', 'c': True}, {'t': 'v1.0.0 branchni yuklaydi', 'c': False}, {'t': 'v1.0.0 ni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git tag -d v1.0.0 nima qiladi?', 'a': [{'t': 'Lokal tagni o\'chiradi', 'c': True}, {'t': 'Remote tagni o\'chiradi', 'c': False}, {'t': 'Tag yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git cherry-pick - Tanlangan commitni olish', 't': 20, 'o': 24, 'q': [
        {'t': 'git cherry-pick nima qiladi?', 'a': [{'t': 'Boshqa branchdan bitta commitni oladi', 'c': True}, {'t': 'Barcha commitlarni oladi', 'c': False}, {'t': 'Branch yaratadi', 'c': False}, {'t': 'Commit o\'chiradi', 'c': False}]},
        {'t': 'git cherry-pick commitHash nima qiladi?', 'a': [{'t': 'O\'sha commitni joriy branchga qo\'llaydi', 'c': True}, {'t': 'O\'sha commitni o\'chiradi', 'c': False}, {'t': 'O\'sha commitga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git cherry-pick qachon foydali?', 'a': [{'t': 'Faqat bitta o\'zgarishni olish kerak bo\'lganda', 'c': True}, {'t': 'Barcha o\'zgarishlarni olish kerak bo\'lganda', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Har doim', 'c': False}]},
        {'t': 'git cherry-pick --continue nima qiladi?', 'a': [{'t': 'Conflict hal qilingandan keyin davom ettiradi', 'c': True}, {'t': 'Cherry-pick ni boshlaydi', 'c': False}, {'t': 'Cherry-pick ni bekor qiladi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git cherry-pick --abort nima qiladi?', 'a': [{'t': 'Cherry-pick ni bekor qiladi', 'c': True}, {'t': 'Cherry-pick ni yakunlaydi', 'c': False}, {'t': 'Cherry-pick ni boshlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git blame - Kim o\'zgartirgan?', 't': 20, 'o': 25, 'q': [
        {'t': 'git blame nima qiladi?', 'a': [{'t': 'Har bir qatorni kim yozganini ko\'rsatadi', 'c': True}, {'t': 'Xatolarni topadi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}, {'t': 'Commit qiladi', 'c': False}]},
        {'t': 'git blame file.txt nima qiladi?', 'a': [{'t': 'file.txt ning har bir qatori kim tomonidan yozilganini ko\'rsatadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git blame nima uchun foydali?', 'a': [{'t': 'Kod tarixini va mualliflarni bilish uchun', 'c': True}, {'t': 'Xatolarni tuzatish uchun', 'c': False}, {'t': 'Commit qilish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'git blame -L 10,20 file.txt nima qiladi?', 'a': [{'t': 'Faqat 10-20 qatorlar uchun ma\'lumot beradi', 'c': True}, {'t': 'Barcha qatorlar uchun', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Faylni o\'chiradi', 'c': False}]},
        {'t': 'git blame -e nima qiladi?', 'a': [{'t': 'Muallif email ini ko\'rsatadi', 'c': True}, {'t': 'Xatolarni ko\'rsatadi', 'c': False}, {'t': 'Faylni tahrirlaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git show - Commit tafsilotlari', 't': 20, 'o': 26, 'q': [
        {'t': 'git show nima qiladi?', 'a': [{'t': 'Oxirgi commit tafsilotlarini ko\'rsatadi', 'c': True}, {'t': 'Barcha commitlarni ko\'rsatadi', 'c': False}, {'t': 'Fayllarni ko\'rsatadi', 'c': False}, {'t': 'Branchlarni ko\'rsatadi', 'c': False}]},
        {'t': 'git show commitHash nima qiladi?', 'a': [{'t': 'O\'sha commit tafsilotlarini ko\'rsatadi', 'c': True}, {'t': 'O\'sha commitni o\'chiradi', 'c': False}, {'t': 'O\'sha commitga o\'tadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git show HEAD nima qiladi?', 'a': [{'t': 'Joriy commit tafsilotlarini ko\'rsatadi', 'c': True}, {'t': 'Barcha commitlarni ko\'rsatadi', 'c': False}, {'t': 'Xato beradi', 'c': False}, {'t': 'Commit o\'chiradi', 'c': False}]},
        {'t': 'git show v1.0.0 nima qiladi?', 'a': [{'t': 'v1.0.0 tag tafsilotlarini ko\'rsatadi', 'c': True}, {'t': 'v1.0.0 ni o\'chiradi', 'c': False}, {'t': 'v1.0.0 yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git show commitHash:file.txt nima qiladi?', 'a': [{'t': 'O\'sha commitdagi file.txt mazmunini ko\'rsatadi', 'c': True}, {'t': 'file.txt ni o\'chiradi', 'c': False}, {'t': 'file.txt ni yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
    ]},

    {'n': 'git clean - Kuzatilmagan fayllarni o\'chirish', 't': 20, 'o': 27, 'q': [
        {'t': 'git clean nima qiladi?', 'a': [{'t': 'Kuzatilmagan (untracked) fayllarni o\'chiradi', 'c': True}, {'t': 'Barcha fayllarni o\'chiradi', 'c': False}, {'t': 'Commitlarni o\'chiradi', 'c': False}, {'t': 'Branchlarni o\'chiradi', 'c': False}]},
        {'t': 'git clean -n nima qiladi?', 'a': [{'t': 'Qaysi fayllar o\'chirilishini ko\'rsatadi (dry run)', 'c': True}, {'t': 'Fayllarni o\'chiradi', 'c': False}, {'t': 'Yangi fayllar yaratadi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git clean -f nima qiladi?', 'a': [{'t': 'Majburiy o\'chiradi', 'c': True}, {'t': 'Fayllarni topadi', 'c': False}, {'t': 'Fayllarni nusxalaydi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git clean -fd nima qiladi?', 'a': [{'t': 'Fayllar va papkalarni o\'chiradi', 'c': True}, {'t': 'Faqat fayllarni o\'chiradi', 'c': False}, {'t': 'Faqat papkalarni o\'chiradi', 'c': False}, {'t': 'Xato beradi', 'c': False}]},
        {'t': 'git clean xavflimi?', 'a': [{'t': 'Ha, fayllar butunlay yo\'qoladi', 'c': True}, {'t': 'Yo\'q, xavfsiz', 'c': False}, {'t': 'Faqat birinchi marta', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
    ]},

    {'n': 'GitHub/GitLab bilan ishlash', 't': 30, 'o': 28, 'q': [
        {'t': 'GitHub nima?', 'a': [{'t': 'Git repositorylarni saqlash va hamkorlik qilish platformasi', 'c': True}, {'t': 'Git dasturi', 'c': False}, {'t': 'Matn muharriri', 'c': False}, {'t': 'Operatsion tizim', 'c': False}]},
        {'t': 'Fork nima?', 'a': [{'t': 'Boshqa odamning repositorysidan nusxa olish', 'c': True}, {'t': 'Branch yaratish', 'c': False}, {'t': 'Commit qilish', 'c': False}, {'t': 'Fayl o\'chirish', 'c': False}]},
        {'t': 'Pull Request (PR) nima?', 'a': [{'t': 'O\'zgarishlarni asosiy repositoryga qo\'shish so\'rovi', 'c': True}, {'t': 'Repository yuklab olish', 'c': False}, {'t': 'Branch yaratish', 'c': False}, {'t': 'Commit qilish', 'c': False}]},
        {'t': 'Issue nima?', 'a': [{'t': 'Muammo yoki taklif yozish joyi', 'c': True}, {'t': 'Commit turi', 'c': False}, {'t': 'Branch turi', 'c': False}, {'t': 'Fayl turi', 'c': False}]},
        {'t': 'README.md nima uchun?', 'a': [{'t': 'Loyiha haqida ma\'lumot berish uchun', 'c': True}, {'t': 'Kod yozish uchun', 'c': False}, {'t': 'Sozlamalar uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
        {'t': 'Star nima?', 'a': [{'t': 'Repositoryni yoqtirganimni bildirish', 'c': True}, {'t': 'Repository yaratish', 'c': False}, {'t': 'Commit qilish', 'c': False}, {'t': 'Branch yaratish', 'c': False}]},
        {'t': 'Watch nima uchun?', 'a': [{'t': 'Repository yangilanishlaridan xabardor bo\'lish uchun', 'c': True}, {'t': 'Repository o\'chirish uchun', 'c': False}, {'t': 'Commit qilish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},

    {'n': 'Git workflow va best practices', 't': 30, 'o': 29, 'q': [
        {'t': 'Feature branch workflow nima?', 'a': [{'t': 'Har bir yangi funksiya uchun alohida branch yaratish', 'c': True}, {'t': 'Faqat main branchda ishlash', 'c': False}, {'t': 'Hech qachon branch yaratmaslik', 'c': False}, {'t': 'Faqat bitta branch ishlatish', 'c': False}]},
        {'t': 'Yaxshi commit xabari qanday?', 'a': [{'t': 'Qisqa, aniq va nima qilganini tushuntiruvchi', 'c': True}, {'t': 'Juda uzun va murakkab', 'c': False}, {'t': 'Faqat bitta so\'z', 'c': False}, {'t': 'Muhim emas', 'c': False}]},
        {'t': 'Qancha tez-tez commit qilish kerak?', 'a': [{'t': 'Har bir mantiqiy o\'zgarishdan keyin', 'c': True}, {'t': 'Kuniga bir marta', 'c': False}, {'t': 'Loyiha tugagandan keyin', 'c': False}, {'t': 'Hech qachon', 'c': False}]},
        {'t': 'main branchda to\'g\'ridan-to\'g\'ri ishlash kerakmi?', 'a': [{'t': 'Yo\'q, feature branchda ishlab merge qilish kerak', 'c': True}, {'t': 'Ha, har doim', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Farqi yo\'q', 'c': False}]},
        {'t': 'git pull qachon qilish kerak?', 'a': [{'t': 'Ishni boshlashdan oldin', 'c': True}, {'t': 'Ishni tugatgandan keyin', 'c': False}, {'t': 'Hech qachon', 'c': False}, {'t': 'Faqat bir marta', 'c': False}]},
        {'t': '.gitignore da nima bo\'lishi kerak?', 'a': [{'t': 'Parollar, log fayllar, build fayllar', 'c': True}, {'t': 'Barcha kod fayllari', 'c': False}, {'t': 'Hech narsa', 'c': False}, {'t': 'Faqat README', 'c': False}]},
        {'t': 'Katta fayllarni Git ga qo\'shish kerakmi?', 'a': [{'t': 'Yo\'q, Git LFS yoki boshqa yechim ishlatish kerak', 'c': True}, {'t': 'Ha, muammo yo\'q', 'c': False}, {'t': 'Ba\'zan', 'c': False}, {'t': 'Har doim', 'c': False}]},
    ]},

    {'n': 'Git muammolarini hal qilish', 't': 30, 'o': 30, 'q': [
        {'t': 'Merge conflict qanday hal qilinadi?', 'a': [{'t': 'Qo\'lda fayllarni tahrirlash va commit qilish', 'c': True}, {'t': 'git merge --fix', 'c': False}, {'t': 'Avtomatik hal bo\'ladi', 'c': False}, {'t': 'Repository o\'chirish', 'c': False}]},
        {'t': 'Noto\'g\'ri commitni qanday tuzatish mumkin?', 'a': [{'t': 'git commit --amend yoki git revert', 'c': True}, {'t': 'Faqat git reset', 'c': False}, {'t': 'Hech qanday yo\'l yo\'q', 'c': False}, {'t': 'Repository qayta yaratish', 'c': False}]},
        {'t': 'Parolni commit qilib qo\'ydim, nima qilish kerak?', 'a': [{'t': 'Tarixdan o\'chirish va parolni o\'zgartirish', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat .gitignore ga qo\'shish', 'c': False}, {'t': 'Repository o\'chirish', 'c': False}]},
        {'t': 'Detached HEAD holatidan qanday chiqish mumkin?', 'a': [{'t': 'git switch main yoki git checkout main', 'c': True}, {'t': 'git reset --hard', 'c': False}, {'t': 'Repository qayta yaratish', 'c': False}, {'t': 'Hech qanday yo\'l yo\'q', 'c': False}]},
        {'t': 'git push rad etilsa nima qilish kerak?', 'a': [{'t': 'Avval git pull qilib keyin push qilish', 'c': True}, {'t': 'git push --force', 'c': False}, {'t': 'Repository o\'chirish', 'c': False}, {'t': 'Hech narsa qilmaslik', 'c': False}]},
        {'t': 'Katta faylni noto\'g\'ri commit qildim, nima qilish kerak?', 'a': [{'t': 'git filter-branch yoki BFG Repo-Cleaner ishlatish', 'c': True}, {'t': 'Hech narsa qilmaslik', 'c': False}, {'t': 'Faqat .gitignore ga qo\'shish', 'c': False}, {'t': 'Repository o\'chirish', 'c': False}]},
        {'t': 'git reflog nima uchun foydali?', 'a': [{'t': 'Yo\'qolgan commitlarni topish uchun', 'c': True}, {'t': 'Fayllarni topish uchun', 'c': False}, {'t': 'Branchlarni yaratish uchun', 'c': False}, {'t': 'Hech narsa uchun', 'c': False}]},
    ]},
]

if __name__ == '__main__':
    subject = get_or_create_git()
    add_topics(subject, T)
    print(f"\n✅ Git - {len(T)} ta mavzu muvaffaqiyatli qo'shildi!")
