"""Accounts app uchun yordamchi funksiyalar"""
import re
from django.utils import timezone


def get_client_ip(request):
    """Request'dan foydalanuvchi IP manzilini olish"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_user_agent(user_agent_string):
    """User agent string'dan qurilma ma'lumotlarini ajratib olish"""
    user_agent_string = user_agent_string.lower()
    
    # Device type
    device_type = 'Desktop'
    if 'mobile' in user_agent_string or 'android' in user_agent_string:
        device_type = 'Mobile'
    elif 'tablet' in user_agent_string or 'ipad' in user_agent_string:
        device_type = 'Tablet'
    
    # Browser
    browser = 'Unknown'
    if 'edg' in user_agent_string or 'edge' in user_agent_string:
        browser = 'Microsoft Edge'
    elif 'chrome' in user_agent_string and 'safari' in user_agent_string:
        browser = 'Google Chrome'
    elif 'firefox' in user_agent_string:
        browser = 'Mozilla Firefox'
    elif 'safari' in user_agent_string and 'chrome' not in user_agent_string:
        browser = 'Safari'
    elif 'opera' in user_agent_string or 'opr' in user_agent_string:
        browser = 'Opera'
    
    # Operating System
    os = 'Unknown'
    if 'windows nt 10' in user_agent_string:
        os = 'Windows 10/11'
    elif 'windows nt 6.3' in user_agent_string:
        os = 'Windows 8.1'
    elif 'windows nt 6.2' in user_agent_string:
        os = 'Windows 8'
    elif 'windows nt 6.1' in user_agent_string:
        os = 'Windows 7'
    elif 'windows' in user_agent_string:
        os = 'Windows'
    elif 'mac os x' in user_agent_string:
        os = 'macOS'
    elif 'android' in user_agent_string:
        # Android versiyasini olish
        match = re.search(r'android (\d+\.?\d*)', user_agent_string)
        if match:
            os = f'Android {match.group(1)}'
        else:
            os = 'Android'
    elif 'iphone' in user_agent_string or 'ipad' in user_agent_string:
        os = 'iOS'
    elif 'linux' in user_agent_string:
        os = 'Linux'
    
    return {
        'device_type': device_type,
        'browser': browser,
        'os': os,
    }


def is_new_device(user, ip_address, user_agent):
    """Qurilma yangi yoki eski ekanligini tekshirish"""
    from .models import LoginHistory
    
    # Oxirgi 30 kundagi kirish tarixini tekshirish
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    
    # Bir xil IP va user agent bilan kirish bo'lganmi?
    existing_login = LoginHistory.objects.filter(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        login_time__gte=thirty_days_ago
    ).exists()
    
    return not existing_login


def create_login_history(user, request):
    """Kirish tarixini yaratish"""
    from .models import LoginHistory
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    device_info = parse_user_agent(user_agent)
    
    # Yangi qurilma ekanligini tekshirish
    is_new = is_new_device(user, ip_address, user_agent)
    
    # Kirish tarixini saqlash
    login_history = LoginHistory.objects.create(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        device_type=device_info['device_type'],
        browser=device_info['browser'],
        os=device_info['os'],
        is_new_device=is_new,
    )
    
    return login_history


def send_new_device_email(user, login_history, request):
    """Yangi qurilmadan kirish haqida email yuborish"""
    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings
    from django.urls import reverse
    
    if not user.email or not user.email_verified:
        return False
    
    try:
        # Parolni tiklash URL
        reset_password_url = request.build_absolute_uri(
            reverse('accounts:forgot_password')
        )
        
        # HTML email yaratish
        html_content = render_to_string('emails/new_device_login.html', {
            'user_name': user.first_name,
            'login_time': login_history.login_time.strftime('%d.%m.%Y %H:%M'),
            'device_type': login_history.device_type,
            'browser': login_history.browser,
            'os': login_history.os,
            'ip_address': login_history.ip_address,
            'location': login_history.location,
            'reset_password_url': reset_password_url,
        })
        
        # Text fallback
        text_content = f'''Assalomu alaykum, {user.first_name}!

XAVFSIZLIK OGOHLANTIRISHI!

Sizning EduSelf hisobingizga yangi qurilmadan kirish amalga oshirildi.

Kirish ma'lumotlari:
- Vaqt: {login_history.login_time.strftime('%d.%m.%Y %H:%M')}
- Qurilma: {login_history.device_type}
- Brauzer: {login_history.browser}
- OS: {login_history.os}
- IP: {login_history.ip_address}

Bu siz edingizmi?
Agar bu siz bo'lsangiz, hech narsa qilishingiz shart emas.

Bu siz bo'lmasa:
Darhol parolingizni o'zgartiring: {reset_password_url}

Hurmat bilan,
EduSelf jamoasi'''
        
        # Email yuborish
        email = EmailMultiAlternatives(
            subject='EduSelf - Yangi qurilmadan kirish',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)
        
        return True
    except Exception as e:
        print(f"New device email yuborishda xatolik: {e}")
        return False
