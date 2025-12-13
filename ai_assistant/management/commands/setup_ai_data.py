from django.core.management.base import BaseCommand
from ai_assistant.models import AIPromptTemplate, SubjectKnowledgeBase
from core.models import Subject


class Command(BaseCommand):
    help = 'AI Hamroh uchun boshlang\'ich ma\'lumotlarni yaratish'

    def handle(self, *args, **options):
        self.stdout.write('AI Hamroh ma\'lumotlarini yaratish...')
        
        # AI Prompt shablonlarini yaratish
        self.create_prompt_templates()
        
        # Fan bilimlar bazasini yaratish
        self.create_subject_knowledge()
        
        self.stdout.write(
            self.style.SUCCESS('AI Hamroh ma\'lumotlari muvaffaqiyatli yaratildi!')
        )

    def create_prompt_templates(self):
        """AI prompt shablonlarini yaratish"""
        templates = [
            {
                'name': 'Matematika yordami',
                'category': 'subject_help',
                'prompt_text': '''Siz matematika bo'yicha mutaxassis AI yordamchisiz. 
                Foydalanuvchiga matematika mavzularini sodda va tushunarli tilda tushuntirib bering.
                Misollar keltiring va bosqichma-bosqich yechim ko'rsating.''',
                'description': 'Matematika fanidan yordam berish uchun'
            },
            {
                'name': 'Fizika yordami',
                'category': 'subject_help',
                'prompt_text': '''Siz fizika bo'yicha mutaxassis AI yordamchisiz.
                Fizika qonunlarini, formulalarini va hodisalarini sodda misollar bilan tushuntiring.
                Amaliy qo'llanishlarini ham ko'rsating.''',
                'description': 'Fizika fanidan yordam berish uchun'
            },
            {
                'name': 'Muassasa tanlash',
                'category': 'institution_advice',
                'prompt_text': '''Siz ta'lim muassasalarini tanlashda mutaxassis maslahatchi siz.
                Foydalanuvchining ehtiyojlari, imkoniyatlari va maqsadlariga qarab eng mos muassasalarni tavsiya qiling.
                Narx, sifat, joylashuv va yo'nalishlarni hisobga oling.''',
                'description': 'Ta\'lim muassasalarini tanlashda yordam'
            },
            {
                'name': 'Sertifikat yo\'riqnomasi',
                'category': 'certificate_guide',
                'prompt_text': '''Siz sertifikatlar bo'yicha mutaxassis yo'riqchi siz.
                Turli sertifikatlar, ularning talablari, foydasi va olish jarayoni haqida batafsil ma'lumot bering.
                Qaysi sertifikat qaysi maqsad uchun mos ekanligini tushuntiring.''',
                'description': 'Sertifikatlar bo\'yicha yo\'riqnoma'
            }
        ]
        
        for template_data in templates:
            template, created = AIPromptTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'  ✓ {template.name} shabloni yaratildi')

    def create_subject_knowledge(self):
        """Fan bilimlar bazasini yaratish"""
        # Matematika uchun bilimlar
        math_subject = Subject.objects.filter(name__icontains='matematik').first()
        if math_subject:
            knowledge_items = [
                {
                    'topic_name': 'Algebra asoslari',
                    'content': '''Algebra - matematikaning harflar va belgilar yordamida sonlar va ularning munosabatlarini o'rganuvchi bo'limi.
                    
                    Asosiy tushunchalar:
                    - O'zgaruvchi (x, y, z)
                    - Koeffitsient
                    - Tenglama va tengsizlik
                    - Ifoda soddalashtirish
                    
                    Misol: 2x + 3 = 7
                    Yechim: x = 2''',
                    'keywords': 'algebra, tenglama, o\'zgaruvchi, koeffitsient',
                    'difficulty_level': 'beginner'
                },
                {
                    'topic_name': 'Geometriya asoslari',
                    'content': '''Geometriya - fazoviy shakllar va ularning xossalarini o'rganuvchi fan.
                    
                    Asosiy figuralar:
                    - Nuqta, to'g'ri chiziq, tekislik
                    - Burchak va uning turlari
                    - Uchburchak va uning xossalari
                    - To'rtburchak va uning turlari
                    
                    Formulalar:
                    - Uchburchak yuzi: S = (a × h) / 2
                    - To'rtburchak yuzi: S = a × b''',
                    'keywords': 'geometriya, uchburchak, to\'rtburchak, yuz, perimetr',
                    'difficulty_level': 'beginner'
                }
            ]
            
            for item in knowledge_items:
                knowledge, created = SubjectKnowledgeBase.objects.get_or_create(
                    subject=math_subject,
                    topic_name=item['topic_name'],
                    defaults=item
                )
                if created:
                    self.stdout.write(f'  ✓ {knowledge.topic_name} bilimi qo\'shildi')
        
        # Fizika uchun bilimlar
        physics_subject = Subject.objects.filter(name__icontains='fizika').first()
        if physics_subject:
            knowledge_items = [
                {
                    'topic_name': 'Mexanika asoslari',
                    'content': '''Mexanika - jismlarning harakati va kuchlarni o'rganuvchi fizika bo'limi.
                    
                    Asosiy tushunchalar:
                    - Tezlik (v = s/t)
                    - Tezlanish (a = Δv/Δt)
                    - Kuch (F = ma)
                    - Energiya va ish
                    
                    Nyutonning qonunlari:
                    1. Inersiya qonuni
                    2. F = ma
                    3. Ta'sir va aks ta'sir qonuni''',
                    'keywords': 'mexanika, tezlik, tezlanish, kuch, nyuton',
                    'difficulty_level': 'intermediate'
                },
                {
                    'topic_name': 'Elektr toki',
                    'content': '''Elektr toki - elektr zaryadlarining tartibli harakati.
                    
                    Asosiy formulalar:
                    - Ohm qonuni: U = I × R
                    - Quvvat: P = U × I
                    - Energiya: W = P × t
                    - Qarshilik: R = ρl/S
                    
                    Tok turlari:
                    - O'zgarmas tok (DC)
                    - O'zgaruvchan tok (AC)''',
                    'keywords': 'elektr, tok, ohm, qarshilik, kuchlanish',
                    'difficulty_level': 'intermediate'
                }
            ]
            
            for item in knowledge_items:
                knowledge, created = SubjectKnowledgeBase.objects.get_or_create(
                    subject=physics_subject,
                    topic_name=item['topic_name'],
                    defaults=item
                )
                if created:
                    self.stdout.write(f'  ✓ {knowledge.topic_name} bilimi qo\'shildi')