"""
ASTRONOMIYA - 100 TA TO'LIQ MAVZU (har birida 5-10 test, to'g'ri javoblar har xil o'rinda)
"""
import os, django, sys, random
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
                # Javoblarni aralashtirish
                answers = qd['a'][:]
                random.shuffle(answers)
                for ad in answers:
                    Answer.objects.create(question=q, text=ad['t'], is_correct=ad['c'])

# Eski mavzularni o'chirish (agar qayta yuklash kerak bo'lsa)
def clear_astronomy_topics():
    from core.models import Subject
    try:
        subj = Subject.objects.get(name='Astronomiya')
        subj.topics.all().delete()
        print("🗑️ Eski mavzular o'chirildi")
    except:
        pass

# Faylni import qilish
import importlib.util
spec = importlib.util.spec_from_file_location("astronomy_data", "add_astronomy_complete_100.py")
astronomy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(astronomy_module)

if __name__ == '__main__':
    # clear_astronomy_topics()  # Agar kerak bo'lsa, kommentdan chiqaring
    subj = get_or_create_astronomy()
    add_topics(subj, astronomy_module.T)
    print(f"\n✅ Jami {len(astronomy_module.T)} ta mavzu qo'shildi!")
    print("🚀 Astronomiya kursi to'liq tayyor (javoblar aralashtirilgan)!")
