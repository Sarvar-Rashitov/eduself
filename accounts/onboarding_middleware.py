from django.shortcuts import redirect
from django.urls import reverse
from .onboarding_models import UserInterestPreference


class OnboardingMiddleware:
    """
    Yangi foydalanuvchilarni onboarding sahifasiga yo'naltirish
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Onboarding talab qilinmaydigan URL'lar
        self.excluded_paths = [
            '/accounts/onboarding/',
            '/accounts/onboarding/save/',
            '/accounts/onboarding/skip/',
            '/accounts/logout/',
            '/accounts/login/',
            '/accounts/register/',
            '/static/',
            '/media/',
            '/admin/',
        ]
    
    def __call__(self, request):
        # Foydalanuvchi tizimga kirganmi?
        if request.user.is_authenticated:
            # Exclude qilingan yo'llarni tekshirish
            if not any(request.path.startswith(path) for path in self.excluded_paths):
                try:
                    preference = request.user.interest_preference
                    
                    # Agar onboarding tugallanmagan bo'lsa
                    if not preference.onboarding_completed:
                        return redirect('accounts:onboarding')
                        
                except UserInterestPreference.DoesNotExist:
                    # Agar preference mavjud bo'lmasa, onboarding'ga yo'naltirish
                    return redirect('accounts:onboarding')
        
        response = self.get_response(request)
        return response
