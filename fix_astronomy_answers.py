"""
Astronomiya testlarini to'g'rilash - javoblarni aralashtirish
"""
import os, django, sys, random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
from core.models import Subject, Topic, Question, Answer

def fix_astronomy_answers():
    try:
        subj = Subject.objects.get(name='Astronomiya')
        topics = subj.topics.all()
        
        print(f"🔧 {topics.count()} ta mavzu topildi")
        
        for topic in topics:
            questions = topic.questions.all()
            for question in questions:
                # Hozirgi javoblarni olish
                answers = list(question.answers.all())
                if len(answers) < 2:
                    continue
                
                # Javoblar ma'lumotlarini saqlash
                answer_data = [(a.text, a.is_correct) for a in answers]
                
                # Eski javoblarni o'chirish
                question.answers.all().delete()
                
                # Javoblarni aralashtirish
                random.shuffle(answer_data)
                
                # Yangi tartibda qayta yaratish
                for text, is_correct in answer_data:
                    Answer.objects.create(
                        question=question,
                        text=text,
                        is_correct=is_correct
                    )
            
            print(f"✅ {topic.name}: {questions.count()} ta savol to'g'rilandi")
        
        print(f"\n🎉 Barcha javoblar aralashtirildi!")
        
    except Subject.DoesNotExist:
        print("❌ Astronomiya fani topilmadi")
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    fix_astronomy_answers()
