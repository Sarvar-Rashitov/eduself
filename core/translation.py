"""
AI-powered translation system using DeepSeek API
Dinamik kontentni tarjima qilish uchun
Page-based load balancing - har bir sahifa o'z API keyidan foydalanadi
"""
import os
import requests
from django.core.cache import cache
from django.conf import settings
import hashlib
import logging
import random

logger = logging.getLogger(__name__)


class AITranslator:
    """DeepSeek AI orqali matnlarni tarjima qilish - Page-based load balancing"""
    
    LANGUAGE_NAMES = {
        'uz': 'Uzbek',
        'en': 'English',
        'ru': 'Russian',
        'kk': 'Kazakh',
        'kaa': 'Karakalpak',
        'tg': 'Tajik',
        'ky': 'Kyrgyz',
    }
    
    # Har bir sahifa uchun API key mapping
    PAGE_API_KEY_MAPPING = {
        'home': 1,              # Home page → KEY_1
        'institutions': 2,      # Institutions → KEY_2
        'courses': 3,           # Courses → KEY_3
        'subjects': 3,          # Subjects → KEY_3
        'mock_exams': 4,        # Mock exams → KEY_4
        'certificates': 4,      # Certificates → KEY_4
        'profile': 5,           # Profile → KEY_5
        'leaderboard': 5,       # Leaderboard → KEY_5
        'news': 2,              # News → KEY_2
        'ai_assistant': 1,      # AI Assistant → KEY_1
        'oferta': 1,            # Oferta → KEY_1
        'default': 1,           # Default → KEY_1
    }
    
    def __init__(self):
        # Ko'p API keylarni yuklash
        self.api_keys = self._load_api_keys()
        self.api_url = settings.DEEPSEEK_API_URL
        self.current_key_index = 0
    
    def _load_api_keys(self):
        """Barcha mavjud API keylarni yuklash"""
        keys = []
        
        # Numbered keys (DEEPSEEK_API_KEY_1, DEEPSEEK_API_KEY_2, ...)
        for i in range(1, 11):  # 1 dan 10 gacha
            key = getattr(settings, f'DEEPSEEK_API_KEY_{i}', None)
            if key and key.strip():
                keys.append(key.strip())
        
        # Agar numbered keylar bo'lmasa, legacy key ishlatish
        if not keys:
            legacy_key = getattr(settings, 'DEEPSEEK_API_KEY', None)
            if legacy_key and legacy_key.strip():
                keys.append(legacy_key.strip())
        
        if keys:
            logger.info(f"✅ Loaded {len(keys)} DeepSeek API key(s) for page-based load balancing")
        else:
            logger.warning("⚠️ No DeepSeek API keys configured")
        
        return keys
    
    def _get_api_key_for_page(self, page_name=None):
        """Sahifa uchun tegishli API keyni olish"""
        if not self.api_keys:
            return None
        
        # Agar sahifa nomi berilmagan bo'lsa, default key
        if not page_name:
            page_name = 'default'
        
        # Sahifa uchun key index olish
        key_index = self.PAGE_API_KEY_MAPPING.get(page_name, 1)
        
        # Agar key mavjud bo'lsa, uni qaytarish
        if key_index <= len(self.api_keys):
            return self.api_keys[key_index - 1]
        
        # Agar key yo'q bo'lsa, birinchi keyni qaytarish
        return self.api_keys[0]
    
    def _get_next_api_key(self):
        """Keyingisi API keyni olish (round-robin) - fallback uchun"""
        if not self.api_keys:
            return None
        
        # Round-robin: har safar keyingisi keyni ishlatish
        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key
    
    def _get_cache_key(self, text, source_lang, target_lang):
        """Cache key yaratish"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"translation:{source_lang}:{target_lang}:{text_hash}"
    
    def translate(self, text, source_lang='uz', target_lang='en', page_name=None):
        """
        Matnni tarjima qilish - Page-based load balancing + Database cache
        
        Args:
            text: Tarjima qilinadigan matn
            source_lang: Manba til kodi (uz, en, ru, ...)
            target_lang: Maqsad til kodi
            page_name: Sahifa nomi (home, institutions, courses, ...)
            
        Returns:
            Tarjima qilingan matn
        """
        # Agar til bir xil bo'lsa, original matnni qaytarish
        if source_lang == target_lang:
            return text
        
        # Bo'sh matn
        if not text or not text.strip():
            return text
        
        # Uzunlik limiti - 1000 chars (database cache bilan)
        if len(text) > 1000:
            logger.debug(f"Text too long for AI translation ({len(text)} chars), returning original")
            return text
        
        # 1. Memory cache'dan tekshirish (eng tez)
        cache_key = self._get_cache_key(text, source_lang, target_lang)
        cached_translation = cache.get(cache_key)
        if cached_translation:
            return cached_translation
        
        # 2. Database cache'dan tekshirish
        text_hash = hashlib.md5(text.encode()).hexdigest()
        try:
            from core.models import TranslationCache
            db_cache = TranslationCache.objects.filter(
                text_hash=text_hash,
                source_lang=source_lang,
                target_lang=target_lang
            ).first()
            
            if db_cache:
                # Hit count'ni oshirish
                db_cache.hit_count += 1
                db_cache.save(update_fields=['hit_count', 'updated_at'])
                
                # Memory cache'ga ham saqlash
                cache.set(cache_key, db_cache.translated_text, 60 * 60 * 24 * 7)
                
                logger.info(f"✅ DB CACHE HIT: {text[:50]}... (hit_count: {db_cache.hit_count})")
                return db_cache.translated_text
            else:
                logger.info(f"⚠️ DB CACHE MISS: {text[:50]}...")
        except Exception as e:
            logger.error(f"❌ DB cache lookup error: {str(e)}")
        
        # API key yo'q bo'lsa, original matnni qaytarish
        if not self.api_keys:
            logger.warning("No DeepSeek API keys configured. Returning original text.")
            return text
        
        # Sahifa uchun tegishli API keyni olish
        api_key = self._get_api_key_for_page(page_name)
        
        try:
            # DeepSeek API ga so'rov yuborish
            source_lang_name = self.LANGUAGE_NAMES.get(source_lang, source_lang)
            target_lang_name = self.LANGUAGE_NAMES.get(target_lang, target_lang)
            
            prompt = f"""Translate the following text from {source_lang_name} to {target_lang_name}. 
Only provide the translation, without any explanations or additional text.

Text to translate:
{text}

Translation:"""
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 1000  # For longer texts
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=15  # 15 seconds timeout for longer texts
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result['choices'][0]['message']['content'].strip()
                
                # 1. Memory cache'ga saqlash (7 kun)
                cache.set(cache_key, translated_text, 60 * 60 * 24 * 7)
                
                # 2. Database cache'ga saqlash
                try:
                    from core.models import TranslationCache
                    obj, created = TranslationCache.objects.update_or_create(
                        text_hash=text_hash,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        defaults={
                            'original_text': text[:1000],  # Limit to 1000 chars
                            'translated_text': translated_text,
                            'hit_count': 1
                        }
                    )
                    if created:
                        logger.info(f"💾 NEW translation saved to DB: {text[:50]}...")
                    else:
                        logger.info(f"🔄 UPDATED translation in DB: {text[:50]}...")
                except Exception as e:
                    logger.error(f"❌ DB cache save error: {str(e)}")
                
                return translated_text
            else:
                logger.error(f"DeepSeek API error: {response.status_code}")
                return text
        
        except requests.exceptions.Timeout:
            logger.warning(f"Translation timeout for: {text[:30]}...")
            return text
        except requests.exceptions.RequestException as e:
            logger.error(f"Translation request error: {str(e)}")
            return text
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text
    
    def translate_batch(self, texts, source_lang='uz', target_lang='en'):
        """
        Ko'p matnni bir vaqtda tarjima qilish
        
        Args:
            texts: Tarjima qilinadigan matnlar ro'yxati
            source_lang: Manba til kodi
            target_lang: Maqsad til kodi
            
        Returns:
            Tarjima qilingan matnlar ro'yxati
        """
        if source_lang == target_lang:
            return texts
        
        translated_texts = []
        for text in texts:
            translated_texts.append(self.translate(text, source_lang, target_lang))
        
        return translated_texts


# Global translator instance
translator = AITranslator()


def translate_text(text, target_lang, source_lang='uz'):
    """
    Helper function - matnni tarjima qilish
    
    Usage:
        from core.translation import translate_text
        translated = translate_text("Salom", "en", "uz")
    """
    return translator.translate(text, source_lang, target_lang)


def get_translated_field(obj, field_name, target_lang, source_lang='uz'):
    """
    Model obyektining fieldini tarjima qilish
    
    Usage:
        from core.translation import get_translated_field
        title = get_translated_field(news, 'title', 'en')
    """
    original_text = getattr(obj, field_name, '')
    if not original_text:
        return ''
    
    return translator.translate(original_text, source_lang, target_lang)
