"""
Python testlarini o'chirish
"""
import os, django, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, Topic, Question, Answer

python_subject = Subject.objects.filter(name='Python').first()
if python_subject:
    # Savollarni o'chirish
    deleted_questions = Question.objects.filter(topic__subject=python_subject).count()
    Question.objects.filter(topic__subject=python_subject).delete()
    
    # Mavzularni o'chirish
    deleted_topics = Topic.objects.filter(subject=python_subject).count()
    Topic.objects.filter(subject=python_subject).delete()
    
    print(f"✅ {deleted_topics} ta mavzu va {deleted_questions} ta savol o'chirildi")
else:
    print("❌ Python fani topilmadi")
