from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.models import SubjectCategory, Certificate, CourseCategory, MockExamCategory
from .onboarding_models import UserInterestPreference
import json


def is_mobile(request):
    """User-Agent orqali mobil qurilmani aniqlash"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    # Desktop keywords
    desktop_keywords = ['windows nt', 'macintosh', 'linux x86_64', 'x11']
    is_desktop = any(keyword in user_agent for keyword in desktop_keywords)
    
    if is_desktop and 'mobile' not in user_agent:
        return False
    
    # Mobile keywords
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'opera mobi']
    
    # iPad desktop sifatida
    if 'ipad' in user_agent:
        return False
    
    return any(keyword in user_agent for keyword in mobile_keywords)


@login_required
@login_required
@require_http_methods(["GET"])
def onboarding_view(request):
    """Onboarding sahifasini ko'rsatish"""
    
    # Agar onboarding allaqachon tugallangan bo'lsa, bosh sahifaga yo'naltirish
    try:
        preference = request.user.interest_preference
        if preference.onboarding_completed:
            return redirect('core:home')
    except UserInterestPreference.DoesNotExist:
        pass
    
    # Kategoriyalarni olish
    subject_categories = SubjectCategory.objects.filter(is_active=True).order_by('order', 'name')
    certificates = Certificate.objects.filter(is_active=True).order_by('order', 'name')
    course_categories = CourseCategory.objects.filter(is_active=True).order_by('order', 'name')
    mock_exam_categories = MockExamCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'subject_categories': subject_categories,
        'certificates': certificates,
        'course_categories': course_categories,
        'mock_exam_categories': mock_exam_categories,
    }
    
    # Mobile yoki Desktop template tanlash
    if is_mobile(request):
        return render(request, 'accounts/onboarding_mobile.html', context)
    else:
        return render(request, 'accounts/onboarding_desktop.html', context)


@login_required
@login_required
@require_http_methods(["POST"])
def save_onboarding(request):
    """Onboarding ma'lumotlarini saqlash"""
    
    try:
        data = json.loads(request.body)
        
        # Foydalanuvchi preference'ini olish yoki yaratish
        preference, created = UserInterestPreference.objects.get_or_create(
            user=request.user
        )
        
        # Ma'lumotlarni saqlash
        preference.source = data.get('source', '')  # Yangi: Manba
        preference.role = data.get('role', '')
        
        # Kategoriyalarni saqlash
        selected_categories = {
            'subjects': data.get('subjects', []),
            'certificates': data.get('certificates', []),
            'courses': data.get('courses', []),
            'mock_exams': data.get('mock_exams', []),
        }
        
        preference.selected_categories = selected_categories
        preference.onboarding_completed = True
        preference.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Onboarding muvaffaqiyatli saqlandi',
            'has_subjects': bool(selected_categories.get('subjects')),
            'has_certificates': bool(selected_categories.get('certificates')),
            'has_courses': bool(selected_categories.get('courses')),
            'has_mock_exams': bool(selected_categories.get('mock_exams')),
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def skip_onboarding(request):
    """Onboarding'ni o'tkazib yuborish"""
    
    try:
        preference, created = UserInterestPreference.objects.get_or_create(
            user=request.user
        )
        
        preference.onboarding_completed = True
        preference.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Onboarding o\'tkazib yuborildi'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)



@login_required
@login_required
@require_http_methods(["GET"])
def show_all_platform(request):
    """Barcha platformani ko'rsatish (shaxsiylashtirish o'chiriladi)"""
    
    try:
        preference = request.user.interest_preference
        
        # Avvalgi qiziqishlarni saqlash (agar mavjud bo'lsa)
        if preference.selected_categories:
            preference.saved_categories = preference.selected_categories.copy()
        
        # Barcha kategoriyalarni tanlash (bo'sh qoldirish orqali hamma narsa ko'rsatiladi)
        preference.selected_categories = {}
        preference.save()
        
        # Toast trigger: to'liq platforma rejimiga o'tildi
        response = redirect('core:home')
        response.set_cookie('show_full_platform_toast', 'true', max_age=5)
        return response
        
    except UserInterestPreference.DoesNotExist:
        return redirect('core:home')


@login_required
@require_http_methods(["GET"])
def return_to_interests(request):
    """Qiziqishlarimga qaytish - avvalgi tanlangan kategoriyalarni qayta tiklash"""
    
    try:
        preference = request.user.interest_preference
        
        # Agar saqlangan kategoriyalar mavjud bo'lsa, ularni qaytarish
        if preference.saved_categories:
            preference.selected_categories = preference.saved_categories.copy()
            preference.save()
            
            # Toast trigger: qiziqishlariga qaytdi
            response = redirect('core:home')
            response.set_cookie('show_interests_toast', 'true', max_age=5)
            return response
        
        # Agar saqlangan kategoriyalar bo'lmasa, onboarding'ga yo'naltirish
        return redirect('accounts:onboarding')
        
    except UserInterestPreference.DoesNotExist:
        return redirect('accounts:onboarding')


@login_required
@require_http_methods(["GET"])
def reset_onboarding(request):
    """Onboarding'ni qayta boshlash"""
    
    try:
        preference = request.user.interest_preference
        preference.onboarding_completed = False
        preference.selected_categories = {}
        preference.saved_categories = {}  # Saqlangan kategoriyalarni ham tozalash
        preference.role = ''
        preference.save()
        
        return redirect('accounts:onboarding')
        
    except UserInterestPreference.DoesNotExist:
        return redirect('accounts:onboarding')
