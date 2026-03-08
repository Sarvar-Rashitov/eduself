from .onboarding_models import UserInterestPreference


def user_preferences(request):
    """
    Foydalanuvchi qiziqishlarini template'larda ishlatish uchun context processor
    """
    context = {
        'user_has_preferences': False,
        'user_preferences': None,
    }
    
    if request.user.is_authenticated:
        try:
            preference = request.user.interest_preference
            context['user_has_preferences'] = preference.onboarding_completed
            context['user_preferences'] = preference
        except UserInterestPreference.DoesNotExist:
            pass
    
    return context
