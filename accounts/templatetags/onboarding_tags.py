from django import template
from accounts.onboarding_models import UserInterestPreference

register = template.Library()


@register.simple_tag
def should_show_section(user, section_type):
    """
    Foydalanuvchi uchun bo'limni ko'rsatish kerakmi?
    
    Args:
        user: User object
        section_type: 'subjects', 'certificates', 'courses', 'mock_exams', 'institutions'
    
    Returns:
        Boolean
    """
    if not user.is_authenticated:
        return True  # Guest users see everything
    
    try:
        preference = user.interest_preference
        
        # Agar onboarding tugallanmagan bo'lsa, hamma narsani ko'rsatish
        if not preference.onboarding_completed:
            return True
        
        # Agar foydalanuvchi hech narsa tanlamagan bo'lsa, hamma narsani ko'rsatish
        if not preference.selected_categories:
            return True
        
        # Bo'limga qarab tekshirish
        if section_type == 'subjects':
            return preference.has_interest_in_subjects()
        elif section_type == 'certificates':
            return preference.has_interest_in_certificates()
        elif section_type == 'courses':
            return preference.has_interest_in_courses()
        elif section_type == 'mock_exams':
            return preference.has_interest_in_mock_exams()
        elif section_type == 'institutions':
            # Institutions har doim ko'rsatiladi
            return True
        
        return True
        
    except UserInterestPreference.DoesNotExist:
        return True  # Agar preference bo'lmasa, hamma narsani ko'rsatish


def _check_user_interests(user):
    """
    Helper function to check if user has any interests
    Faqat selected_categories ni tekshiradi (saved_categories ni emas)
    """
    if not user.is_authenticated:
        return False
    
    try:
        preference = user.interest_preference
        if not preference.onboarding_completed:
            return False
        
        # Faqat selected_categories ni tekshirish
        return (preference.has_interest_in_subjects() or 
                preference.has_interest_in_certificates() or 
                preference.has_interest_in_courses() or 
                preference.has_interest_in_mock_exams())
        
    except UserInterestPreference.DoesNotExist:
        return False


@register.simple_tag
def has_any_interests(user):
    """
    Foydalanuvchi biror narsaga qiziqishi bormi? (Simple tag version)
    Usage: {% has_any_interests user as user_has_interests %}
    """
    return _check_user_interests(user)


@register.filter(name='has_any_interests')
def has_any_interests_filter(user):
    """
    Foydalanuvchi biror narsaga qiziqishi bormi? (Filter version)
    Usage: {{ user|has_any_interests }}
    """
    return _check_user_interests(user)
