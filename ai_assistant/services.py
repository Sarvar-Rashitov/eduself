import os
import json
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

from openai import OpenAI
from django.conf import settings
from django.db.models import Q
from .models import ChatSession, ChatMessage, MessageType, SubjectKnowledgeBase, InstitutionRecommendation
from core.models import Subject, Institution, Certificate, InstitutionDirection


class DeepSeekAIService:
    """DeepSeek API bilan ishlash uchun service"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.model = "deepseek-chat"
        self.max_tokens = 2000
        self.temperature = 0.7
        
        # API client yaratish
        if self.api_key and self.api_key.startswith('sk-'):
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com"
                )
                self.use_api = True
            except Exception as e:
                self.client = None
                self.use_api = False
        else:
            self.client = None
            self.use_api = False
    
    def get_system_prompt(self) -> str:
        """Tizim prompt'ini qaytarish"""
        return """Siz EduSelf platformasining AI Hamrohi siz. Sizning vazifangiz:

1. FANLAR BO'YICHA YORDAM:
   - O'quvchilarga turli fanlar bo'yicha savollariga javob berish
   - Mavzularni tushuntirish va misollar keltirish
   - Test savollariga tayyorgarlik ko'rish bo'yicha maslahat berish
   - Qiyin mavzularni sodda tilda tushuntirish

2. TA'LIM MUASSASALARI TANLASH:
   - Foydalanuvchi ehtiyojlariga mos muassasalar tavsiya qilish
   - Kontrakt narxlari, yo'nalishlar haqida ma'lumot berish
   - Qabul jarayoni va talablar haqida yo'riqnoma berish
   - Muassasalar orasida taqqoslash

3. SERTIFIKATLAR BO'YICHA YORDAM:
   - Turli sertifikatlar haqida ma'lumot berish
   - Sertifikat olish jarayoni va talablari
   - Sertifikat testlariga tayyorgarlik

QOIDALAR:
- Har doim o'zbek tilida javob bering
- Aniq va tushunarli javoblar bering
- Agar ma'lumot yo'q bo'lsa, ochiqchasiga aytib bering
- Foydalanuvchini qo'llab-quvvatlang va motivatsiya bering
- Har doim EduSelf platformasidan foydalanishga undang

Javoblaringiz qisqa, aniq va foydali bo'lsin."""

    def generate_response(self, user_message: str, chat_history: List[Dict], context_data: Dict = None, attachment_url: str = None) -> Dict:
        """AI javob generatsiya qilish"""
        start_time = time.time()
        
        # Avval DeepSeek API'ni sinab ko'rish
        if self.use_api and self.client:
            try:
                # Chat tarixini tayyorlash
                messages = [{"role": "system", "content": self.get_system_prompt()}]
                
                # Kontekst ma'lumotlarini qo'shish
                if context_data:
                    context_message = self._build_context_message(context_data)
                    if context_message:
                        messages.append({"role": "system", "content": context_message})
                
                # Chat tarixini qo'shish (oxirgi 5 ta xabar)
                for msg in chat_history[-5:]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Foydalanuvchi xabarini qo'shish (rasm bilan yoki rasmsiz)
                if attachment_url and attachment_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    # Rasm bilan xabar (DeepSeek Vision)
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_message or "Bu rasmni tahlil qiling"},
                            {"type": "image_url", "image_url": {"url": attachment_url}}
                        ]
                    })
                else:
                    # Oddiy matn xabari
                    messages.append({"role": "user", "content": user_message})
                
                # API ga so'rov yuborish
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    stream=False
                )
                
                response_time = time.time() - start_time
                
                # DeepSeek javobini qaytarish
                ai_content = response.choices[0].message.content
                
                if ai_content and len(ai_content.strip()) > 0:
                    return {
                        'success': True,
                        'content': ai_content,
                        'tokens_used': response.usage.total_tokens if response.usage else 0,
                        'response_time': response_time,
                        'source': 'deepseek'
                    }
                
            except Exception as e:
                # Fallback javobga o'tish
                pass
        
        # Fallback: Aqlli oddiy javoblar (API ishlamasa)
        return self._get_smart_fallback_response(user_message, context_data, start_time)
    
    def _get_smart_fallback_response(self, user_message: str, context_data: Dict, start_time: float) -> Dict:
        """Aqlli fallback javoblar"""
        user_lower = user_message.lower()
        
        # Matematika savollariga javoblar
        if any(word in user_lower for word in ['matematika', 'algebra', 'geometriya', 'trigonometriya', 'hisob']):
            response = """📐 **Matematika bo'yicha yordam**

Men sizga matematika fanidan yordam bera olaman:

🔢 **Algebra**: Tenglamalar, tengsizliklar, funksiyalar
📏 **Geometriya**: Shakllar, yuzalar, hajmlar
📊 **Statistika**: Ma'lumotlarni tahlil qilish
🧮 **Arifmetika**: Asosiy hisob-kitoblar

Qaysi mavzu bo'yicha aniq savol bor? Misol keltiring, men tushuntirib beraman!"""
        
        # Fizika savollariga javoblar
        elif any(word in user_lower for word in ['fizika', 'mexanika', 'elektr', 'optika', 'termodinamika']):
            response = """⚡ **Fizika bo'yicha yordam**

Fizika fanidan sizga yordam beraman:

🏃 **Mexanika**: Harakat, kuch, energiya
⚡ **Elektr**: Tok, kuchlanish, qarshilik
🌈 **Optika**: Yorug'lik, ko'zgu, linza
🌡️ **Issiqlik**: Harorat, issiqlik uzatish

Qaysi bo'lim bo'yicha savol bor? Formulalar va misollar bilan tushuntiraman!"""
        
        # Test va imtihon savollariga javoblar
        elif any(word in user_lower for word in ['test', 'imtihon', 'dtm', 'tayyorgarlik', 'qanday']):
            response = """📝 **Test va imtihonlarga tayyorgarlik**

Imtihonlarga tayyorgarlik bo'yicha maslahatlar:

✅ **DTM testlari**: Har kuni 30-50 ta savol ishlang
📚 **Mavzularni takrorlash**: Asosiy formulalarni yodlang
⏰ **Vaqtni boshqarish**: Har savolga 1-2 daqiqa ajrating
🎯 **Zaif tomonlarni aniqlash**: Ko'p xato qilgan mavzularni takrorlang

Qaysi fandan test topshirmoqchisiz? Aniq maslahat beraman!"""
        
        # Muassasa tanlash savollariga javoblar
        elif any(word in user_lower for word in ['muassasa', 'universitet', 'institut', 'kollej', 'tanlash']):
            response = """🏫 **Ta'lim muassasalarini tanlash**

Muassasa tanlashda yordam beraman:

🎓 **Universitetlar**: Davlat va xususiy oliy ta'lim
🏢 **Institutlar**: Ixtisoslashgan ta'lim muassasalari
📚 **Kollejlar**: O'rta maxsus ta'lim
💰 **Narxlar**: Kontrakt va grant imkoniyatlari

Qanday yo'nalishda o'qimoqchisiz? Sizga mos muassasalarni tavsiya qilaman!"""
        
        # Sertifikat savollariga javoblar
        elif any(word in user_lower for word in ['sertifikat', 'diplom', 'guvohnoma']):
            response = """🏆 **Sertifikatlar haqida ma'lumot**

Turli sertifikatlar mavjud:

💻 **IT sertifikatlar**: Dasturlash, web-dizayn
🌐 **Til sertifikatlari**: IELTS, CEFR darajasi
📊 **Kasbiy sertifikatlar**: Buxgalteriya, marketing
🎨 **Ijodiy sertifikatlar**: Dizayn, fotografiya

Qaysi sohada sertifikat olmoqchisiz? Talab va jarayonlar haqida ma'lumot beraman!"""
        
        # Salomlashish
        elif any(word in user_lower for word in ['salom', 'assalom', 'hello', 'hi']):
            response = """👋 **Assalomu alaykum!**

Men EduSelf AI Hamrohiman! Sizning shaxsiy ta'lim yordamchingiz.

Men sizga quyidagilar bilan yordam bera olaman:
📚 Fanlar bo'yicha savollar (matematika, fizika, kimyo...)
🏫 Ta'lim muassasalarini tanlash
🏆 Sertifikatlar va kurslar haqida ma'lumot
📝 Test va imtihonlarga tayyorgarlik

Qanday yordam kerak? Bemalol so'rang!"""
        
        # Umumiy yordam
        elif any(word in user_lower for word in ['yordam', 'help', 'qanday', 'nima']):
            response = """🤝 **Sizga qanday yordam bera olaman?**

Men EduSelf platformasining AI yordamchisiman:

📖 **Fanlar**: Matematika, fizika, kimya, biologiya
🎓 **Ta'lim**: Universitet, kollej, kurs tanlash
📜 **Sertifikatlar**: Turli soha bo'yicha sertifikatlar
📊 **Testlar**: DTM, IELTS va boshqa imtihonlar

Aniq savol bering, batafsil javob beraman!"""
        
        # Default javob
        else:
            response = f"""🤔 **"{user_message}" haqida**

Qiziqarli savol! Men sizga quyidagi yo'nalishlarda yordam bera olaman:

📚 **Fanlar bo'yicha**: Matematika, fizika, kimyo, biologiya
🏫 **Muassasa tanlash**: Universitet, institut, kollej
🏆 **Sertifikatlar**: Turli soha bo'yicha
📝 **Testlar**: DTM, imtihonlarga tayyorgarlik

Qaysi birini tanlaysiz? Yoki boshqa savol bering!"""
        
        return {
            'success': True,
            'content': response,
            'tokens_used': 0,
            'response_time': time.time() - start_time,
            'source': 'fallback'  # Fallback javob ekanini bildirish
        }
    
    def _build_context_message(self, context_data: Dict) -> str:
        """Kontekst ma'lumotlarini xabar ko'rinishida yaratish"""
        context_parts = []
        
        # Fanlar ma'lumoti
        if 'subjects' in context_data:
            subjects_info = "Mavjud fanlar: " + ", ".join([s['name'] for s in context_data['subjects']])
            context_parts.append(subjects_info)
        
        # Muassasalar ma'lumoti
        if 'institutions' in context_data:
            institutions_info = "Mavjud ta'lim muassasalari: " + ", ".join([i['name'] for i in context_data['institutions']])
            context_parts.append(institutions_info)
        
        # Sertifikatlar ma'lumoti
        if 'certificates' in context_data:
            certificates_info = "Mavjud sertifikatlar: " + ", ".join([c['name'] for c in context_data['certificates']])
            context_parts.append(certificates_info)
        
        return "\n".join(context_parts) if context_parts else ""
    
    def _build_context_message(self, context_data: Dict) -> str:
        """Kontekst ma'lumotlarini xabar ko'rinishida yaratish"""
        context_parts = []
        
        # Fanlar ma'lumoti
        if 'subjects' in context_data:
            subjects_info = "Mavjud fanlar: " + ", ".join([s['name'] for s in context_data['subjects']])
            context_parts.append(subjects_info)
        
        # Muassasalar ma'lumoti
        if 'institutions' in context_data:
            institutions_info = "Mavjud ta'lim muassasalari: " + ", ".join([i['name'] for i in context_data['institutions']])
            context_parts.append(institutions_info)
        
        # Sertifikatlar ma'lumoti
        if 'certificates' in context_data:
            certificates_info = "Mavjud sertifikatlar: " + ", ".join([c['name'] for c in context_data['certificates']])
            context_parts.append(certificates_info)
        
        return "\n".join(context_parts) if context_parts else ""


class EduSelfContextService:
    """EduSelf platformasi kontekstini tayyorlash"""
    
    @staticmethod
    def get_subjects_context() -> List[Dict]:
        """Fanlar ro'yxatini olish"""
        subjects = Subject.objects.filter(is_active=True).values('id', 'name', 'description')
        return list(subjects)
    
    @staticmethod
    def get_institutions_context() -> List[Dict]:
        """Muassasalar ro'yxatini olish"""
        institutions = Institution.objects.filter(is_active=True).values(
            'id', 'name', 'institution_type', 'short_description', 
            'contract_price_min', 'contract_price_max'
        )
        return list(institutions)
    
    @staticmethod
    def get_certificates_context() -> List[Dict]:
        """Sertifikatlar ro'yxatini olish"""
        certificates = Certificate.objects.filter(is_active=True).values('id', 'name', 'description')
        return list(certificates)
    
    @staticmethod
    def search_relevant_content(query: str) -> Dict:
        """So'rov bo'yicha tegishli kontentni qidirish"""
        context = {}
        
        try:
            # Fanlar bo'yicha qidirish
            subjects = Subject.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_active=True
            ).values('id', 'name', 'description')[:5]
            
            if subjects:
                context['subjects'] = list(subjects)
        except Exception:
            pass
        
        try:
            # Muassasalar bo'yicha qidirish
            institutions = Institution.objects.filter(
                Q(name__icontains=query) | Q(short_description__icontains=query),
                is_active=True
            ).values('id', 'name', 'institution_type', 'short_description')[:5]
            
            if institutions:
                context['institutions'] = list(institutions)
        except Exception:
            pass
        
        try:
            # Sertifikatlar bo'yicha qidirish
            certificates = Certificate.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_active=True
            ).values('id', 'name', 'description')[:5]
            
            if certificates:
                context['certificates'] = list(certificates)
        except Exception:
            pass
        
        return context


class ChatService:
    """Chat boshqarish uchun service"""
    
    def __init__(self):
        self.ai_service = DeepSeekAIService()
        self.context_service = EduSelfContextService()
    
    def create_chat_session(self, user, title: str = None) -> ChatSession:
        """Yangi chat sessiyasi yaratish"""
        if not title:
            title = f"Suhbat {user.chat_sessions.count() + 1}"
        
        session = ChatSession.objects.create(
            user=user,
            title=title
        )
        
        # Salomlashish xabari
        welcome_message = """Assalomu alaykum! Men EduSelf AI Hamrohiman. 

Men sizga quyidagi yo'nalishlarda yordam bera olaman:
📚 Fanlar bo'yicha savollaringizga javob berish
🏫 Ta'lim muassasalarini tanlashda maslahat berish  
🏆 Sertifikatlar haqida ma'lumot berish

Qanday yordam kerak?"""
        
        ChatMessage.objects.create(
            session=session,
            message_type=MessageType.ASSISTANT,
            content=welcome_message
        )
        
        return session
    
    def send_message(self, session: ChatSession, user_message: str, attachment=None) -> tuple:
        """Xabar yuborish va AI javobini olish. Returns (ChatMessage, source)"""
        try:
            # Foydalanuvchi xabarini saqlash
            user_msg = ChatMessage.objects.create(
                session=session,
                message_type=MessageType.USER,
                content=user_message,
                attachment=attachment
            )
            
            # Agar bu birinchi foydalanuvchi xabari bo'lsa, sessiya title'ini yangilash
            user_messages_count = session.messages.filter(message_type=MessageType.USER).count()
            if user_messages_count == 1:  # Birinchi foydalanuvchi xabari
                # Xabar uzunligini cheklash va title yaratish
                title = self._generate_session_title(user_message)
                session.title = title
                session.save()
            
            # Attachment URL olish (rasm uchun)
            attachment_url = None
            if attachment and user_msg.attachment:
                try:
                    # To'liq URL yaratish
                    from django.conf import settings
                    attachment_url = user_msg.attachment.url
                    # Agar local bo'lsa, to'liq URL kerak emas, DeepSeek base64 qabul qiladi
                    if attachment_url.startswith('/'):
                        # Local file - base64 ga o'girish
                        import base64
                        with open(user_msg.attachment.path, 'rb') as f:
                            file_data = base64.b64encode(f.read()).decode('utf-8')
                            file_ext = user_msg.attachment.name.split('.')[-1].lower()
                            mime_type = 'image/jpeg' if file_ext in ['jpg', 'jpeg'] else f'image/{file_ext}'
                            attachment_url = f"data:{mime_type};base64,{file_data}"
                except Exception:
                    attachment_url = None
            
            # Chat tarixini olish
            chat_history = []
            try:
                for msg in session.messages.order_by('created_at')[-10:]:
                    role = "user" if msg.message_type == MessageType.USER else "assistant"
                    chat_history.append({
                        "role": role,
                        "content": msg.content
                    })
            except Exception:
                chat_history = []
            
            # Kontekst ma'lumotlarini olish
            try:
                context_data = self.context_service.search_relevant_content(user_message)
            except Exception:
                context_data = {}
            
            # AI javobini olish
            source = 'fallback'
            try:
                ai_response = self.ai_service.generate_response(
                    user_message=user_message,
                    chat_history=chat_history[:-1] if chat_history else [],
                    context_data=context_data,
                    attachment_url=attachment_url
                )
                source = ai_response.get('source', 'fallback')
            except Exception:
                ai_response = {
                    'success': True,
                    'content': 'Salom! Men AI Hamrohman. Sizga qanday yordam bera olaman?',
                    'tokens_used': 0,
                    'response_time': 0.0,
                    'source': 'fallback'
                }
            
            # AI javobini saqlash
            ai_msg = ChatMessage.objects.create(
                session=session,
                message_type=MessageType.ASSISTANT,
                content=ai_response.get('content', 'Kechirasiz, javob berishda xatolik yuz berdi.'),
                tokens_used=ai_response.get('tokens_used', 0),
                response_time=ai_response.get('response_time', 0.0)
            )
            
            # Sessiya vaqtini yangilash
            session.save()
            
            return ai_msg, source
            
        except Exception as e:
            # Agar hamma narsa xato bo'lsa, standart javob
            ai_msg = ChatMessage.objects.create(
                session=session,
                message_type=MessageType.ASSISTANT,
                content='Salom! Men AI Hamrohman. Hozir texnik muammo bor, lekin tez orada hal qilinadi.',
                tokens_used=0,
                response_time=0.0
            )
            return ai_msg, 'error'
    
    def get_user_sessions(self, user) -> List[ChatSession]:
        """Foydalanuvchi sessiyalarini olish"""
        return ChatSession.objects.filter(user=user, is_active=True).order_by('-updated_at')
    
    def get_session_messages(self, session: ChatSession) -> List[ChatMessage]:
        """Sessiya xabarlarini olish"""
        return ChatMessage.objects.filter(session=session).order_by('created_at')
    
    def _generate_session_title(self, user_message: str) -> str:
        """Foydalanuvchi xabari asosida sessiya title'ini yaratish"""
        # Xabarni tozalash va uzunligini cheklash
        message = user_message.strip()
        
        # Agar xabar juda qisqa bo'lsa
        if len(message) < 5:
            return "Yangi suhbat"
        
        # Agar xabar juda uzun bo'lsa, qisqartirish
        if len(message) > 50:
            # So'zlar bo'yicha qisqartirish
            words = message.split()
            title = ""
            for word in words:
                if len(title + " " + word) <= 50:
                    title += (" " if title else "") + word
                else:
                    break
            
            # Agar hali ham uzun bo'lsa, belgilar bo'yicha qisqartirish
            if len(title) > 50:
                title = title[:47] + "..."
            
            return title if title else message[:47] + "..."
        
        return message


class TestAnalysisService:
    """Test natijalarini tahlil qilish va tavsiyalar berish uchun service"""
    
    def __init__(self):
        self.ai_service = DeepSeekAIService()
    
    def analyze_test_result(self, test_result, test_type='topic') -> Dict:
        """Test natijasini tahlil qilib, AI tavsiyalar berish"""
        try:
            # Test ma'lumotlarini to'plash
            analysis_data = self._prepare_test_data(test_result, test_type)
            
            # AI tavsiya olish
            ai_recommendation = self._get_ai_recommendation(analysis_data)
            
            return {
                'success': True,
                'analysis': analysis_data,
                'ai_recommendation': ai_recommendation,
                'recommendations': self._generate_specific_recommendations(analysis_data)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'ai_recommendation': self._get_fallback_recommendation(test_result, test_type)
            }
    
    def _prepare_test_data(self, test_result, test_type) -> Dict:
        """Test ma'lumotlarini tayyorlash"""
        data = {
            'test_type': test_type,
            'score': test_result.score,
            'total_questions': test_result.total_questions,
            'correct_answers': test_result.correct_answers,
            'incorrect_answers': test_result.total_questions - test_result.correct_answers,
            'passed': test_result.passed,
            'earned_points': getattr(test_result, 'earned_points', 0),
            'topics_analysis': {},
            'difficulty_analysis': {},
            'subject_performance': {}
        }
        
        # Test turiga qarab qo'shimcha ma'lumotlar
        if test_type == 'topic':
            data['topic_name'] = test_result.topic.name
            data['subject_name'] = test_result.topic.subject.name
            data['passing_score'] = test_result.topic.passing_score
            
            # Savollar bo'yicha tahlil
            questions_analysis = self._analyze_topic_questions(test_result)
            data.update(questions_analysis)
            
        elif test_type == 'certificate':
            data['test_name'] = test_result.test.title
            data['topic_name'] = test_result.test.topic.name
            data['certificate_name'] = test_result.test.topic.certificate.name
            data['passing_score'] = test_result.test.passing_score
            
            # Sertifikat test tahlili
            questions_analysis = self._analyze_certificate_questions(test_result)
            data.update(questions_analysis)
            
        elif test_type == 'mock_exam':
            data['exam_name'] = test_result.exam.title
            data['category_name'] = test_result.exam.category.name if test_result.exam.category else "Umumiy"
            data['passing_score'] = test_result.exam.passing_score
            
            # Mock exam tahlili
            questions_analysis = self._analyze_mock_exam_questions(test_result)
            data.update(questions_analysis)
            
        elif test_type == 'direction_exam':
            data['exam_name'] = test_result.exam.title
            data['direction_name'] = test_result.exam.direction.name
            data['institution_name'] = test_result.exam.direction.institution.name
            data['passing_score'] = test_result.exam.passing_score
            data['subjects_list'] = test_result.exam.get_subjects_list()
            
            # Direction exam tahlili
            questions_analysis = self._analyze_direction_exam_questions(test_result)
            data.update(questions_analysis)
        
        return data
    
    def _analyze_topic_questions(self, result) -> Dict:
        """Mavzu test savollarini tahlil qilish"""
        from core.models import Question
        
        analysis = {
            'correct_topics': [],
            'incorrect_topics': [],
            'weak_areas': [],
            'strong_areas': []
        }
        
        try:
            questions = result.topic.questions.all()
            
            for question in questions:
                question_id = str(question.id)
                user_answer = result.user_answers.get(question_id, {})
                is_correct = user_answer.get('is_correct', False)
                
                question_info = {
                    'question_text': question.text[:100] + "..." if len(question.text) > 100 else question.text,
                    'points': question.points,
                    'is_correct': is_correct
                }
                
                if is_correct:
                    analysis['correct_topics'].append(question_info)
                    analysis['strong_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
                else:
                    analysis['incorrect_topics'].append(question_info)
                    analysis['weak_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
        
        except Exception:
            pass
        
        return analysis
    
    def _analyze_certificate_questions(self, result) -> Dict:
        """Sertifikat test savollarini tahlil qilish"""
        analysis = {
            'correct_topics': [],
            'incorrect_topics': [],
            'weak_areas': [],
            'strong_areas': []
        }
        
        try:
            questions = result.test.cert_questions.all()
            
            for question in questions:
                question_id = str(question.id)
                user_answer = result.user_answers.get(question_id, {})
                is_correct = user_answer.get('is_correct', False)
                
                question_info = {
                    'question_text': question.text[:100] + "..." if len(question.text) > 100 else question.text,
                    'points': question.points,
                    'is_correct': is_correct
                }
                
                if is_correct:
                    analysis['correct_topics'].append(question_info)
                    analysis['strong_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
                else:
                    analysis['incorrect_topics'].append(question_info)
                    analysis['weak_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
        
        except Exception:
            pass
        
        return analysis
    
    def _analyze_mock_exam_questions(self, result) -> Dict:
        """Mock exam savollarini tahlil qilish"""
        analysis = {
            'correct_topics': [],
            'incorrect_topics': [],
            'weak_areas': [],
            'strong_areas': []
        }
        
        try:
            questions = result.exam.mock_questions.all()
            
            for question in questions:
                question_id = str(question.id)
                user_answer = result.user_answers.get(question_id, {})
                is_correct = user_answer.get('is_correct', False)
                
                question_info = {
                    'question_text': question.text[:100] + "..." if len(question.text) > 100 else question.text,
                    'points': question.points,
                    'is_correct': is_correct
                }
                
                if is_correct:
                    analysis['correct_topics'].append(question_info)
                    analysis['strong_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
                else:
                    analysis['incorrect_topics'].append(question_info)
                    analysis['weak_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
        
        except Exception:
            pass
        
        return analysis
    
    def _analyze_direction_exam_questions(self, result) -> Dict:
        """Direction exam savollarini tahlil qilish"""
        analysis = {
            'correct_topics': [],
            'incorrect_topics': [],
            'weak_areas': [],
            'strong_areas': [],
            'subject_performance': {}
        }
        
        try:
            questions = result.exam.direction_questions.all()
            subjects_list = result.exam.get_subjects_list()
            
            # Har bir fan bo'yicha performance hisoblash
            for subject in subjects_list:
                analysis['subject_performance'][subject] = {
                    'correct': 0,
                    'total': 0,
                    'percentage': 0
                }
            
            for question in questions:
                question_id = str(question.id)
                user_answer = result.user_answers.get(question_id, {})
                is_correct = user_answer.get('is_correct', False)
                
                question_info = {
                    'question_text': question.text[:100] + "..." if len(question.text) > 100 else question.text,
                    'points': question.points,
                    'is_correct': is_correct
                }
                
                if is_correct:
                    analysis['correct_topics'].append(question_info)
                    analysis['strong_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
                else:
                    analysis['incorrect_topics'].append(question_info)
                    analysis['weak_areas'].append(f"Savol #{question.order}: {question.text[:50]}...")
            
            # Subject performance hisoblash
            for subject in analysis['subject_performance']:
                total = analysis['subject_performance'][subject]['total']
                correct = analysis['subject_performance'][subject]['correct']
                if total > 0:
                    analysis['subject_performance'][subject]['percentage'] = round((correct / total) * 100, 1)
        
        except Exception:
            pass
        
        return analysis
    
    def _get_ai_recommendation(self, analysis_data) -> str:
        """AI dan tavsiya olish"""
        try:
            # AI uchun prompt tayyorlash
            prompt = self._build_analysis_prompt(analysis_data)
            
            # AI dan javob olish
            ai_response = self.ai_service.generate_response(
                user_message=prompt,
                chat_history=[],
                context_data={}
            )
            
            if ai_response.get('success') and ai_response.get('content'):
                return ai_response['content']
            
        except Exception:
            pass
        
        # Fallback tavsiya
        return self._get_fallback_recommendation(analysis_data)
    
    def _build_analysis_prompt(self, data) -> str:
        """AI uchun tahlil prompt'ini yaratish"""
        test_type = data.get('test_type', 'test')
        score = data.get('score', 0)
        correct = data.get('correct_answers', 0)
        total = data.get('total_questions', 0)
        incorrect = data.get('incorrect_answers', 0)
        
        prompt = f"""Foydalanuvchi {test_type} testini topshirdi. Natijalar:

📊 **Test natijalari:**
- Umumiy ball: {score}%
- To'g'ri javoblar: {correct}/{total}
- Noto'g'ri javoblar: {incorrect}
- Test o'tdi: {'Ha' if data.get('passed') else "Yo'q"}

"""
        
        # Test turiga qarab qo'shimcha ma'lumotlar
        if test_type == 'topic':
            prompt += f"📚 **Fan va mavzu:** {data.get('subject_name')} - {data.get('topic_name')}\n"
        elif test_type == 'certificate':
            prompt += f"🏆 **Sertifikat:** {data.get('certificate_name')} - {data.get('topic_name')}\n"
        elif test_type == 'mock_exam':
            prompt += f"📝 **Mock imtihon:** {data.get('exam_name')} ({data.get('category_name')})\n"
        elif test_type == 'direction_exam':
            prompt += f"🎓 **Yo'nalish imtihoni:** {data.get('direction_name')} - {data.get('institution_name')}\n"
            if data.get('subjects_list'):
                prompt += f"📖 **Fanlar:** {', '.join(data['subjects_list'])}\n"
        
        prompt += f"""
🎯 **O'tish balli:** {data.get('passing_score', 60)}%

Iltimos, bu natijalar asosida foydalanuvchiga:
1. Kuchli tomonlarini ta'kidlang
2. Zaif tomonlarini aniqlang  
3. Yaxshilash uchun aniq tavsiyalar bering
4. Keyingi qadamlar bo'yicha yo'riqnoma bering
5. Motivatsion so'zlar bilan yakunlang

Javobingiz o'zbek tilida, qisqa va amaliy bo'lsin."""
        
        return prompt
    
    def _get_fallback_recommendation(self, data, test_type=None) -> str:
        """AI ishlamasa, standart tavsiya"""
        if isinstance(data, dict):
            score = data.get('score', 0)
            correct = data.get('correct_answers', 0)
            total = data.get('total_questions', 0)
            passed = data.get('passed', False)
        else:
            # Agar data test result obyekti bo'lsa
            score = data.score
            correct = data.correct_answers
            total = data.total_questions
            passed = data.passed
        
        if score >= 90:
            return f"""🎉 **Ajoyib natija!**

Siz {score}% ball to'pladingiz - bu juda yuqori natija!

✅ **Kuchli tomonlaringiz:**
- {correct}/{total} savolga to'g'ri javob berdingiz
- Mavzuni juda yaxshi egallabsiz
- Testni muvaffaqiyatli yakunladingiz

🚀 **Keyingi qadamlar:**
- Ushbu darajangizni saqlab qoling
- Yangi mavzularga o'ting
- Boshqa testlarni ham sinab ko'ring
- Bilimlaringizni amaliyotda qo'llang

Tabriklaymiz! Davom eting! 💪"""
        
        elif score >= 70:
            test_status = "Testni muvaffaqiyatli o'tdingiz" if passed else "Deyarli o'tish balliga yetdingiz"
            return f"""👍 **Yaxshi natija!**

Siz {score}% ball to'pladingiz - bu yaxshi ko'rsatkich.

✅ **Kuchli tomonlaringiz:**
- {correct}/{total} savolga to'g'ri javob berdingiz
- Asosiy mavzularni yaxshi bilasiz
- {test_status}

📚 **Yaxshilash uchun:**
- Noto'g'ri javob bergan savollarni qayta ko'rib chiqing
- Zaif mavzularni takrorlang
- Qo'shimcha mashq qiling
- Testni qayta topshirib ko'ring

Siz to'g'ri yo'ldasiz! 🎯"""
        
        elif score >= 50:
            return f"""📖 **O'rtacha natija**

Siz {score}% ball to'pladingiz. Yaxshilash uchun ish bor.

✅ **Kuchli tomonlaringiz:**
- {correct}/{total} savolga to'g'ri javob berdingiz
- Ba'zi mavzularni yaxshi bilasiz

📚 **Tavsiyalar:**
- Noto'g'ri javoblarni diqqat bilan tahlil qiling
- Zaif mavzularni batafsil o'rganing
- Har kuni 30-60 daqiqa o'qishga vaqt ajrating
- Qo'shimcha testlar ishlang
- Darslik va qo'shimcha manbalardan foydalaning

Taslim bo'lmang, davom eting! 💪"""
        
        else:
            return f"""📚 **Takrorlash kerak**

Siz {score}% ball to'pladingiz. Asosiy mavzularni qayta o'rganish kerak.

🎯 **Tavsiyalar:**
- Barcha mavzularni boshidan o'rganing
- Asosiy tushunchalarni mustahkamlang
- Har kuni muntazam o'qing
- O'qituvchi yoki do'stlaringizdan yordam so'rang
- Oddiy savollardan boshlab, asta-sekin qiyinlashtiring

📖 **O'rganish rejasi:**
1. Asosiy nazariyani o'rganing
2. Misollar ustida ishlang  
3. Oddiy testlar ishlang
4. Bilimingizni tekshiring
5. Takrorlang va mustahkamlang

Har bir katta muvaffaqiyat kichik qadamlardan boshlanadi! 🌟"""
    
    def _generate_specific_recommendations(self, analysis_data) -> List[str]:
        """Aniq tavsiyalar ro'yxatini yaratish"""
        recommendations = []
        
        score = analysis_data.get('score', 0)
        weak_areas = analysis_data.get('weak_areas', [])
        strong_areas = analysis_data.get('strong_areas', [])
        
        # Ball asosida umumiy tavsiyalar
        if score >= 90:
            recommendations.extend([
                "Ajoyib! Ushbu darajangizni saqlab qoling",
                "Yangi mavzularga o'ting",
                "Boshqa testlarni ham sinab ko'ring"
            ])
        elif score >= 70:
            recommendations.extend([
                "Yaxshi natija! Zaif tomonlarni mustahkamlang",
                "Noto'g'ri javoblarni qayta ko'rib chiqing",
                "Qo'shimcha mashq qiling"
            ])
        elif score >= 50:
            recommendations.extend([
                "Asosiy mavzularni takrorlang",
                "Har kuni 30-60 daqiqa o'qing",
                "Qo'shimcha testlar ishlang"
            ])
        else:
            recommendations.extend([
                "Barcha mavzularni qayta o'rganing",
                "Asosiy tushunchalarni mustahkamlang",
                "O'qituvchidan yordam so'rang"
            ])
        
        # Zaif tomonlar bo'yicha tavsiyalar
        if weak_areas:
            recommendations.append("Quyidagi mavzularni takrorlang:")
            for area in weak_areas[:3]:  # Faqat birinchi 3 tasini ko'rsatish
                recommendations.append(f"• {area}")
        
        return recommendations


class InstitutionRecommendationService:
    """Muassasa tavsiya qilish uchun service"""
    
    @staticmethod
    def recommend_institutions(criteria: Dict) -> List[Institution]:
        """Mezonlar bo'yicha muassasa tavsiya qilish"""
        queryset = Institution.objects.filter(is_active=True)
        
        # Tur bo'yicha filterlash
        if 'institution_type' in criteria:
            queryset = queryset.filter(institution_type=criteria['institution_type'])
        
        # Narx oralig'i bo'yicha filterlash
        if 'max_price' in criteria:
            queryset = queryset.filter(
                Q(contract_price_min__lte=criteria['max_price']) |
                Q(contract_price_max__lte=criteria['max_price'])
            )
        
        # Joylashuv bo'yicha filterlash
        if 'location' in criteria:
            queryset = queryset.filter(address__icontains=criteria['location'])
        
        return queryset[:10]  # Eng ko'p 10 ta tavsiya