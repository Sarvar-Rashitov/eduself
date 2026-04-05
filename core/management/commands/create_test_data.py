from django.core.management.base import BaseCommand
from core.models import (
    SubjectCategory, Subject, Topic, Question, Answer,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer
)


class Command(BaseCommand):
    help = 'Test uchun default ma\'lumotlar yaratish (pagination ko\'rish uchun)'

    def handle(self, *args, **options):
        self.stdout.write('Test ma\'lumotlari yaratilmoqda...')
        
        # Avval eski test ma'lumotlarini o'chirish
        self.stdout.write('🗑️  Eski test ma\'lumotlari o\'chirilmoqda...')
        
        # Faqat test ma'lumotlarini o'chirish (real ma'lumotlarni saqlab qolish)
        test_subjects = Subject.objects.filter(name__in=[
            'Matematika', 'Fizika', 'Informatika', 'Kimyo', 'Biologiya', 
            'Geografiya', 'Tarix', 'Huquq', 'Iqtisod', 'Ingliz tili', 
            'Rus tili', 'O\'zbek tili', 'Astronomiya', 'Ekologiya', 'Falsafa',
            'Adabiyot', 'San\'at', 'Musiqa', 'Sport', 'Psixologiya'
        ])
        test_subjects.delete()
        
        test_certificates = Certificate.objects.filter(name__in=[
            'Python dasturlash', 'Web Development', 'Data Science', 
            'Machine Learning', 'Mobile Development', 'DevOps', 
            'Cyber Security', 'Cloud Computing', 'Blockchain', 
            'AI & Neural Networks', 'Frontend Development', 
            'Backend Development', 'Full Stack Development', 
            'Game Development', 'IoT Development'
        ])
        test_certificates.delete()
        
        self.stdout.write(self.style.SUCCESS('✅ Eski ma\'lumotlar o\'chirildi'))
        
        # 1. Subject kategoriyalari va fanlar yaratish
        self.create_subjects()
        
        # 2. Sertifikatlar va topiklar yaratish
        self.create_certificates()
        
        self.stdout.write(self.style.SUCCESS('✅ Test ma\'lumotlari muvaffaqiyatli yaratildi!'))
    
    def create_subjects(self):
        """Fanlar va kategoriyalar yaratish"""
        self.stdout.write('📚 Fanlar yaratilmoqda...')
        
        # Kategoriyalar
        categories_data = [
            {'name': 'Aniq fanlar', 'slug': 'aniq-fanlar'},
            {'name': 'Tabiiy fanlar', 'slug': 'tabiiy-fanlar'},
            {'name': 'Ijtimoiy fanlar', 'slug': 'ijtimoiy-fanlar'},
            {'name': 'Tillar', 'slug': 'tillar'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = SubjectCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'is_active': True}
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'  ✓ Kategoriya yaratildi: {category.name}')
        
        # Fanlar (20 ta - pagination ko'rish uchun)
        subjects_data = [
            {'name': 'Matematika', 'category': 'aniq-fanlar', 'order': 1},
            {'name': 'Fizika', 'category': 'aniq-fanlar', 'order': 2},
            {'name': 'Informatika', 'category': 'aniq-fanlar', 'order': 3},
            {'name': 'Astronomiya', 'category': 'aniq-fanlar', 'order': 4},
            {'name': 'Kimyo', 'category': 'tabiiy-fanlar', 'order': 5},
            {'name': 'Biologiya', 'category': 'tabiiy-fanlar', 'order': 6},
            {'name': 'Geografiya', 'category': 'tabiiy-fanlar', 'order': 7},
            {'name': 'Ekologiya', 'category': 'tabiiy-fanlar', 'order': 8},
            {'name': 'Tarix', 'category': 'ijtimoiy-fanlar', 'order': 9},
            {'name': 'Huquq', 'category': 'ijtimoiy-fanlar', 'order': 10},
            {'name': 'Iqtisod', 'category': 'ijtimoiy-fanlar', 'order': 11},
            {'name': 'Falsafa', 'category': 'ijtimoiy-fanlar', 'order': 12},
            {'name': 'Psixologiya', 'category': 'ijtimoiy-fanlar', 'order': 13},
            {'name': 'Ingliz tili', 'category': 'tillar', 'order': 14},
            {'name': 'Rus tili', 'category': 'tillar', 'order': 15},
            {'name': 'O\'zbek tili', 'category': 'tillar', 'order': 16},
            {'name': 'Adabiyot', 'category': 'tillar', 'order': 17},
            {'name': 'San\'at', 'category': 'tillar', 'order': 18},
            {'name': 'Musiqa', 'category': 'tillar', 'order': 19},
            {'name': 'Sport', 'category': 'tillar', 'order': 20},
        ]
        
        for subj_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subj_data['name'],
                defaults={
                    'category': categories[subj_data['category']],
                    'description': f'{subj_data["name"]} fanidan testlar',
                    'order': subj_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Fan yaratildi: {subject.name}')
                
                # Har bir fan uchun 3 ta mavzu yaratish
                for i in range(1, 4):
                    topic, topic_created = Topic.objects.get_or_create(
                        subject=subject,
                        name=f'{subject.name} - Mavzu {i}',
                        defaults={
                            'description': f'{subject.name} fanining {i}-mavzusi',
                            'order': i,
                            'is_active': True,
                            'passing_score': 60
                        }
                    )
                    
                    if topic_created:
                        # Har bir mavzu uchun 5 ta savol yaratish
                        for j in range(1, 6):
                            question = Question.objects.create(
                                topic=topic,
                                text=f'{topic.name} - Savol {j}',
                                points=10,
                                order=j
                            )
                            
                            # Har bir savol uchun 4 ta javob (1 tasi to'g'ri)
                            for k in range(1, 5):
                                Answer.objects.create(
                                    question=question,
                                    text=f'Javob {k}',
                                    is_correct=(k == 1)  # Birinchi javob to'g'ri
                                )
        
        total_subjects = Subject.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'✅ {len(subjects_data)} ta yangi fan yaratildi. Jami: {total_subjects} ta fan'))
    
    def create_certificates(self):
        """Sertifikatlar va topiklar yaratish"""
        self.stdout.write('🏆 Sertifikatlar yaratilmoqda...')
        
        # Sertifikatlar (15 ta - pagination ko'rish uchun)
        certificates_data = [
            {'name': 'Python dasturlash', 'order': 1},
            {'name': 'Web Development', 'order': 2},
            {'name': 'Data Science', 'order': 3},
            {'name': 'Machine Learning', 'order': 4},
            {'name': 'Mobile Development', 'order': 5},
            {'name': 'DevOps', 'order': 6},
            {'name': 'Cyber Security', 'order': 7},
            {'name': 'Cloud Computing', 'order': 8},
            {'name': 'Blockchain', 'order': 9},
            {'name': 'AI & Neural Networks', 'order': 10},
            {'name': 'Frontend Development', 'order': 11},
            {'name': 'Backend Development', 'order': 12},
            {'name': 'Full Stack Development', 'order': 13},
            {'name': 'Game Development', 'order': 14},
            {'name': 'IoT Development', 'order': 15},
        ]
        
        for cert_data in certificates_data:
            certificate, created = Certificate.objects.get_or_create(
                name=cert_data['name'],
                defaults={
                    'description': f'{cert_data["name"]} bo\'yicha sertifikat',
                    'order': cert_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Sertifikat yaratildi: {certificate.name}')
                
                # Har bir sertifikat uchun 3 ta topic yaratish
                for i in range(1, 4):
                    topic, topic_created = CertificateTopic.objects.get_or_create(
                        certificate=certificate,
                        name=f'{certificate.name} - Topic {i}',
                        defaults={
                            'description': f'{certificate.name} ning {i}-topici',
                            'order': i,
                            'is_active': True
                        }
                    )
                    
                    if topic_created:
                        # Har bir topic uchun 2 ta test yaratish
                        for j in range(1, 3):
                            test = CertificateTest.objects.create(
                                topic=topic,
                                title=f'{topic.name} - Test {j}',
                                description=f'{topic.name} ning {j}-testi',
                                order=j,
                                is_active=True,
                                passing_score=70
                            )
                            
                            # Har bir test uchun 5 ta savol yaratish
                            for k in range(1, 6):
                                question = CertificateQuestion.objects.create(
                                    test=test,
                                    text=f'{test.title} - Savol {k}',
                                    points=10.0,
                                    order=k
                                )
                                
                                # Har bir savol uchun 4 ta javob (1 tasi to'g'ri)
                                for m in range(1, 5):
                                    CertificateAnswer.objects.create(
                                        question=question,
                                        text=f'Javob {m}',
                                        is_correct=(m == 1)  # Birinchi javob to'g'ri
                                    )
        
        total_certificates = Certificate.objects.filter(is_active=True).count()
        self.stdout.write(self.style.SUCCESS(f'✅ {len(certificates_data)} ta yangi sertifikat yaratildi. Jami: {total_certificates} ta sertifikat'))
