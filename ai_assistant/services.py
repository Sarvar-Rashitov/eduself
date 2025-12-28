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