"""
AI-powered translation system using DeepSeek API
Dinamik kontentni tarjima qilish uchun
"""
import os
import requests
from django.core.cache import cache
from django.conf import settings
import hashlib
import logging

logger = logging.getLogger(__name__)


class AITranslator:
    """DeepSeek AI orqali matnlarni tarjima qilish"""
    
    LANGUAGE_NAMES = {
        'uz': 'Uzbek',
        'en': 'English',
        'ru': 'Russian',
        'kk': 'Kazakh',
        'kaa': 'Karakalpak',
        'tg': 'Tajik',
        'ky': 'Kyrgyz',
    }
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
    
    def _get_cache_key(self, text, source_lang, target_lang):
        """Cache key yaratish"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"translation:{source_lang}:{target_lang}:{text_hash}"
    
    def translate(self, text, source_lang='uz', target_lang='en'):
        """
        Matnni tarjima qilish
        
        Args:
            text: Tarjima qilinadigan matn
            source_lang: Manba til kodi (uz, en, ru, ...)
            target_lang: Maqsad til kodi
            
        Returns:
            Tarjima qilingan matn
        """
        # Agar til bir xil bo'lsa, original matnni qaytarish
        if source_lang == target_lang:
            return text
        
        # Bo'sh matn
        if not text or not text.strip():
            return text
        
        # Cache'dan tekshirish
        cache_key = self._get_cache_key(text, source_lang, target_lang)
        cached_translation = cache.get(cache_key)
        if cached_translation:
            return cached_translation
        
        # API key yo'q bo'lsa, original matnni qaytarish
        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY not configured. Returning original text.")
            return text
        
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
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': len(text) * 3  # Tarjima uchun yetarli token
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=10  # Reduced timeout to prevent worker timeouts
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result['choices'][0]['message']['content'].strip()
                
                # Cache'ga saqlash (24 soat)
                cache.set(cache_key, translated_text, 60 * 60 * 24)
                
                return translated_text
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
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
