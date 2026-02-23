"""
Custom middleware for language handling
"""
from django.utils import translation
from django.conf import settings


class UserLanguageMiddleware:
    """
    Foydalanuvchi tilini avtomatik o'rnatish middleware
    
    Priority:
    1. URL parameter (?lang=uz)
    2. User.language (authenticated users)
    3. Session language
    4. Browser language
    5. Default language
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 1. URL parametrdan til olish
        lang_code = request.GET.get('lang')
        
        # 2. Authenticated user'ning tilini olish
        if not lang_code and request.user.is_authenticated:
            if hasattr(request.user, 'language'):
                lang_code = request.user.language
        
        # 3. Session'dan til olish
        if not lang_code:
            lang_code = request.session.get('django_language')
        
        # 4. Browser tilini olish
        if not lang_code:
            lang_code = request.LANGUAGE_CODE
        
        # 5. Default til
        if not lang_code:
            lang_code = settings.LANGUAGE_CODE
        
        # Tilni tekshirish va o'rnatish
        available_languages = [lang[0] for lang in settings.LANGUAGES]
        if lang_code in available_languages:
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
            
            # Session'ga saqlash
            if request.session.get('django_language') != lang_code:
                request.session['django_language'] = lang_code
        
        response = self.get_response(request)
        return response
