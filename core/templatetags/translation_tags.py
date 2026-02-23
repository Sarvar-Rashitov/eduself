"""
Custom template tags for AI translation
"""
from django import template
from django.utils.safestring import mark_safe
from core.translation import translator
import json
import os

register = template.Library()

# Statik tarjimalarni yuklash
STATIC_TRANSLATIONS = {}
try:
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'static_translations.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static_translations.json'),
        'static_translations.json',
    ]
    
    for translations_file in possible_paths:
        if os.path.exists(translations_file):
            with open(translations_file, 'r', encoding='utf-8') as f:
                STATIC_TRANSLATIONS = json.load(f)
            print(f"✅ Loaded {len(STATIC_TRANSLATIONS)} static translations from {translations_file}")
            break
    
    if not STATIC_TRANSLATIONS:
        print("⚠️ Warning: static_translations.json not found")
except Exception as e:
    print(f"❌ Error loading static translations: {e}")


@register.simple_tag(takes_context=True)
def translate_with_page(context, text, target_lang=None):
    """
    Page-aware translation tag
    
    Usage:
        {% translate_with_page news.title request.LANGUAGE_CODE %}
        {% translate_with_page course.description "en" %}
    """
    if not text:
        return ''
    
    # Get target language
    if not target_lang:
        target_lang = context.get('CURRENT_LANGUAGE', 'uz')
    
    # Agar til bir xil bo'lsa, original matnni qaytarish
    if target_lang == 'uz':
        return text
    
    # Uzunlik limiti - 200 chars
    if len(text) > 200:
        return text
    
    # Get page name from context
    page_name = context.get('PAGE_NAME', 'default')
    
    # Default source language - uzbek
    source_lang = 'uz'
    
    # Try-except bilan xavfsiz tarjima
    try:
        return translator.translate(text, source_lang, target_lang, page_name)
    except Exception as e:
        # Agar xatolik bo'lsa, original matnni qaytarish
        return text


@register.filter(name='translate')
def translate(text, target_lang):
    """
    Template filter - matnni tarjima qilish (legacy support)
    
    Usage:
        {{ news.title|translate:request.LANGUAGE_CODE }}
        {{ course.description|translate:"en" }}
    """
    if not text:
        return ''
    
    # Agar til bir xil bo'lsa, original matnni qaytarish
    if target_lang == 'uz':
        return text
    
    # Uzunlik limiti - 200 chars
    if len(text) > 200:
        return text
    
    # Default source language - uzbek
    source_lang = 'uz'
    
    # Try-except bilan xavfsiz tarjima (page_name=None - default key ishlatadi)
    try:
        return translator.translate(text, source_lang, target_lang, page_name=None)
    except Exception as e:
        # Agar xatolik bo'lsa, original matnni qaytarish
        return text


@register.filter(name='trans')
def trans(text, target_lang='uz'):
    """
    Statik matnlarni tarjima qilish
    
    Usage:
        {{ "Kirish"|trans:request.LANGUAGE_CODE }}
        {{ "Bosh sahifa"|trans:"en" }}
    """
    if not text or target_lang == 'uz':
        return text
    
    # Statik tarjimalardan qidirish
    if text in STATIC_TRANSLATIONS:
        translations = STATIC_TRANSLATIONS[text]
        if target_lang in translations:
            return translations[target_lang]
    
    # Uzunlik limiti - 200 chars
    if len(text) > 200:
        return text
    
    # Agar topilmasa, AI orqali tarjima qilish (page_name=None)
    try:
        return translator.translate(text, 'uz', target_lang, page_name=None)
    except Exception as e:
        return text


@register.filter(name='translate_from')
def translate_from(text, langs):
    """
    Template filter - source va target tilni ko'rsatish
    
    Usage:
        {{ news.title|translate_from:"uz,en" }}
    """
    if not text or not langs:
        return text
    
    try:
        source_lang, target_lang = langs.split(',')
        return translator.translate(text, source_lang.strip(), target_lang.strip())
    except:
        return text


@register.simple_tag
def translate_text(text, target_lang, source_lang='uz'):
    """
    Template tag - matnni tarjima qilish
    
    Usage:
        {% translate_text news.title request.LANGUAGE_CODE %}
        {% translate_text course.description "en" "uz" %}
    """
    if not text:
        return ''
    
    return translator.translate(text, source_lang, target_lang)


@register.simple_tag
def t(text, lang='uz'):
    """
    Qisqa statik tarjima tag
    
    Usage:
        {% t "Kirish" request.LANGUAGE_CODE %}
        {% t "Bosh sahifa" "en" %}
    """
    if not text or lang == 'uz':
        return text
    
    # Statik tarjimalardan qidirish
    if text in STATIC_TRANSLATIONS:
        translations = STATIC_TRANSLATIONS[text]
        if lang in translations:
            return translations[lang]
    
    # Uzunlik limiti - 200 chars
    if len(text) > 200:
        return text
    
    # Agar topilmasa, AI orqali tarjima qilish (page_name=None)
    try:
        return translator.translate(text, 'uz', lang, page_name=None)
    except Exception as e:
        return text


@register.inclusion_tag('includes/language_selector.html', takes_context=True)
def language_selector(context):
    """
    Til tanlash dropdown
    
    Usage:
        {% load translation_tags %}
        {% language_selector %}
    """
    from django.conf import settings
    
    request = context.get('request')
    current_language = request.LANGUAGE_CODE if request else settings.LANGUAGE_CODE
    
    return {
        'languages': settings.LANGUAGES,
        'current_language': current_language,
        'request': request,
    }


@register.filter(name='get_language_name')
def get_language_name(lang_code):
    """
    Til kodidan til nomini olish
    
    Usage:
        {{ "uz"|get_language_name }}  -> O'zbekcha
    """
    from django.conf import settings
    
    for code, name in settings.LANGUAGES:
        if code == lang_code:
            return name
    
    return lang_code
