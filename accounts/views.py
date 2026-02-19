from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
import requests
import hashlib
import hmac
import time
import re
from .forms import EmailRegisterForm, PhoneRegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from .models import User, PasswordResetToken, EmailVerificationToken


def is_mobile(request):
    """User-Agent orqali mobil qurilmani aniqlash"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'opera mobi']
    return any(keyword in user_agent for keyword in mobile_keywords)


def register_view(request):
    """Ro'yxatdan o'tish - email yoki telefon tanlash"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    # Ro'yxatdan o'tish turini aniqlash
    register_type = request.GET.get('type', 'email')  # email yoki phone
    
    if request.method == 'POST':
        register_type = request.POST.get('register_type', 'email')
        
        if register_type == 'phone':
            # Country code ni qo'shish
            country_code = request.POST.get('country_code', '+998')
            phone = request.POST.get('phone', '')
            # Country code ni telefon raqamga qo'shish
            phone_digits = re.sub(r'\D', '', phone)
            full_phone = country_code.replace('+', '') + phone_digits
            
            # POST data ni yangilash
            post_data = request.POST.copy()
            post_data['phone'] = full_phone
            form = PhoneRegisterForm(post_data)
        else:
            form = EmailRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            # Email bilan ro'yxatdan o'tgan bo'lsa, tasdiqlash emailini yuborish
            if register_type == 'email' and user.email:
                token = EmailVerificationToken.objects.create(user=user)
                verify_url = request.build_absolute_uri(
                    reverse('accounts:verify_email', kwargs={'token': token.token})
                )
                try:
                    send_mail(
                        subject='EduSelf - Emailni tasdiqlash',
                        message=f'''Assalomu alaykum, {user.first_name}!

EduSelf platformasiga xush kelibsiz!

Emailingizni tasdiqlash uchun quyidagi havolaga o'ting:
{verify_url}

Havola 48 soat ichida amal qiladi.

Hurmat bilan,
EduSelf jamoasi''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                    messages.success(request, "Ro'yxatdan o'tdingiz! Emailingizga tasdiqlash havolasi yuborildi.")
                except Exception as e:
                    print(f"Email yuborishda xatolik: {e}")
                    messages.success(request, "Ro'yxatdan o'tdingiz!")
            else:
                messages.success(request, "Ro'yxatdan o'tdingiz!")
            
            login(request, user, backend='accounts.backends.EmailPhoneBackend')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
        else:
            # Form xatoliklarini ko'rsatish
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        if register_type == 'phone':
            form = PhoneRegisterForm()
        else:
            form = EmailRegisterForm()
    
    context = {
        'form': form,
        'register_type': register_type,
        'google_client_id': settings.GOOGLE_CLIENT_ID,
        'telegram_bot_username': settings.TELEGRAM_BOT_USERNAME,
    }
    
    if is_mobile(request):
        return render(request, 'accounts/register.html', context)
    else:
        return render(request, 'accounts/register_desktop.html', context)


def login_view(request):
    """Kirish - email yoki telefon bilan"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Backend ni specify qilish
            login(request, user, backend='accounts.backends.EmailPhoneBackend')
            messages.success(request, f"Xush kelibsiz, {user.first_name}!")
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'google_client_id': settings.GOOGLE_CLIENT_ID,
        'telegram_bot_username': settings.TELEGRAM_BOT_USERNAME,
    }
    
    if is_mobile(request):
        return render(request, 'accounts/login.html', context)
    else:
        return render(request, 'accounts/login_desktop.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('core:home')



def verify_email_view(request, token):
    """Email tasdiqlash"""
    try:
        verification = EmailVerificationToken.objects.get(token=token)
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, "Noto'g'ri yoki eskirgan havola.")
        return redirect('core:home')
    
    if not verification.is_valid():
        messages.error(request, "Bu havola eskirgan yoki allaqachon ishlatilgan.")
        return redirect('core:home')
    
    user = verification.user
    user.email_verified = True
    user.save()
    
    verification.used = True
    verification.save()
    
    messages.success(request, "Emailingiz muvaffaqiyatli tasdiqlandi!")
    return redirect('core:home')


@login_required
def resend_verification_view(request):
    """Tasdiqlash emailini qayta yuborish"""
    user = request.user
    
    if not user.email:
        messages.warning(request, "Avval profilingizda email manzilini kiriting.")
        return redirect('accounts:profile')
    
    if user.email_verified:
        messages.info(request, "Emailingiz allaqachon tasdiqlangan.")
        return redirect('accounts:profile')
    
    # Email sozlamalari tekshirish
    if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == 'your-email@gmail.com':
        messages.warning(request, "Email xizmati hozircha sozlanmagan. Tez orada ishga tushadi!")
        return redirect('accounts:profile')
    
    # Yangi token yaratish
    token = EmailVerificationToken.objects.create(user=user)
    
    verify_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={'token': token.token})
    )
    
    try:
        send_mail(
            subject='EduSelf - Emailni tasdiqlash',
            message=f'''Assalomu alaykum, {user.first_name}!

Emailingizni tasdiqlash uchun quyidagi havolaga o'ting:
{verify_url}

Havola 48 soat ichida amal qiladi.

Hurmat bilan,
EduSelf jamoasi''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(request, f"Tasdiqlash havolasi {user.email} manziliga yuborildi!")
    except Exception as e:
        print(f"Email yuborishda xatolik: {e}")  # Debug uchun
        messages.error(request, f"Email yuborishda xatolik yuz berdi: {str(e)}")
    
    return redirect('accounts:profile')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            messages.success(request, "Agar bu email ro'yxatdan o'tgan bo'lsa, parolni tiklash havolasi yuborildi.")
            try:
                user = User.objects.get(email=email)
                token = PasswordResetToken.objects.create(user=user)
                reset_link = request.build_absolute_uri(
                    reverse('accounts:reset_password', kwargs={'token': token.token})
                )
                send_mail(
                    subject='EduSelf - Parolni tiklash',
                    message=f'''Assalomu alaykum, {user.first_name}!

Parolni tiklash uchun quyidagi havolaga o'ting:
{reset_link}

Havola 24 soat ichida amal qiladi.

Agar siz bu so'rovni yubormagan bo'lsangiz, bu xabarni e'tiborsiz qoldiring.

Hurmat bilan,
EduSelf jamoasi''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except User.DoesNotExist:
                pass
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password_view(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Noto'g'ri yoki eskirgan havola.")
        return redirect('accounts:forgot_password')
    
    if not reset_token.is_valid():
        messages.error(request, "Bu havola eskirgan yoki allaqachon ishlatilgan.")
        return redirect('accounts:forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = reset_token.user
            user.set_password(form.cleaned_data['password1'])
            user.save()
            reset_token.used = True
            reset_token.save()
            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")
            return redirect('accounts:login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'accounts/reset_password.html', {'form': form})



# Google OAuth
@csrf_exempt
def google_auth_view(request):
    """Google OAuth callback"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            credential = data.get('credential')
            
            if not credential:
                return JsonResponse({'success': False, 'error': 'Token topilmadi'})
            
            # Google token'ni tekshirish
            google_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}'
            response = requests.get(google_url)
            
            if response.status_code != 200:
                return JsonResponse({'success': False, 'error': 'Token noto\'g\'ri'})
            
            google_data = response.json()
            
            # Client ID tekshirish
            if google_data.get('aud') != settings.GOOGLE_CLIENT_ID:
                return JsonResponse({'success': False, 'error': 'Client ID mos kelmadi'})
            
            email = google_data.get('email')
            google_id = google_data.get('sub')
            name = google_data.get('name', '')
            picture = google_data.get('picture', '')
            
            # Foydalanuvchini topish yoki yaratish
            user = None
            
            # Google ID bo'yicha qidirish
            try:
                user = User.objects.get(google_id=google_id)
            except User.DoesNotExist:
                pass
            
            # Email bo'yicha qidirish
            if not user:
                try:
                    user = User.objects.get(email=email)
                    user.google_id = google_id
                    user.save()
                except User.DoesNotExist:
                    pass
            
            # Yangi foydalanuvchi yaratish
            if not user:
                first_name = name.split()[0] if name else ''
                last_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
                
                user = User.objects.create(
                    email=email,
                    google_id=google_id,
                    first_name=first_name,
                    last_name=last_name,
                    email_verified=True,
                    auth_provider='google'
                )
                user.set_unusable_password()
                user.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({'success': True, 'redirect': '/'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST so\'rov kerak'})



# Telegram Auth
def telegram_auth_view(request):
    """Telegram Login Widget callback - hash tekshiruvi bilan"""
    telegram_data = {
        'id': request.GET.get('id'),
        'first_name': request.GET.get('first_name', ''),
        'last_name': request.GET.get('last_name', ''),
        'username': request.GET.get('username', ''),
        'photo_url': request.GET.get('photo_url', ''),
        'auth_date': request.GET.get('auth_date'),
        'hash': request.GET.get('hash'),
    }
    
    if not telegram_data['id'] or not telegram_data['hash']:
        messages.error(request, "Telegram ma'lumotlari noto'g'ri")
        return redirect('accounts:login')
    
    # Hash tekshirish
    if not verify_telegram_auth(telegram_data.copy()):
        messages.error(request, "Telegram autentifikatsiya xatosi")
        return redirect('accounts:login')
    
    telegram_id = str(telegram_data['id'])
    telegram_username = telegram_data['username']
    
    # Foydalanuvchini topish yoki yaratish
    try:
        user = User.objects.get(telegram_id=telegram_id)
        # Ma'lumotlarni yangilash
        if telegram_data['first_name']:
            user.first_name = telegram_data['first_name']
        if telegram_data['last_name']:
            user.last_name = telegram_data['last_name']
        if telegram_username:
            user.telegram_username = telegram_username
        user.save()
    except User.DoesNotExist:
        # Yangi foydalanuvchi yaratish
        user = User.objects.create(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            first_name=telegram_data['first_name'] or 'User',
            last_name=telegram_data['last_name'] or '',
            auth_provider='telegram'
        )
        user.set_unusable_password()
        user.save()
    
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    messages.success(request, f"Telegram orqali kirdingiz, {user.first_name}!")
    return redirect('core:home')


def verify_telegram_auth(data):
    """Telegram auth hash'ni tekshirish"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return False
    
    check_hash = data.pop('hash', None)
    if not check_hash:
        return False
    
    # Auth date tekshirish
    try:
        auth_date = int(data.get('auth_date', 0))
    except (ValueError, TypeError):
        return False
    
    if time.time() - auth_date > 86400:
        return False
    
    # Data string yaratish
    data_check_arr = []
    for key in sorted(data.keys()):
        value = data[key]
        if value is not None and value != '':
            data_check_arr.append(f"{key}={value}")
    data_check_string = '\n'.join(data_check_arr)
    
    # Secret key
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    
    # Hash hisoblash
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return calculated_hash == check_hash


def telegram_callback_view(request):
    """Telegram bot orqali login"""
    from telegram_bot.utils import verify_login_token
    
    telegram_id = request.GET.get('telegram_id')
    token = request.GET.get('token')
    
    if not telegram_id or not token:
        messages.error(request, "Noto'g'ri havola.")
        return redirect('accounts:login')
    
    if not verify_login_token(telegram_id, token):
        messages.error(request, "Havola eskirgan.")
        return redirect('accounts:login')
    
    try:
        user = User.objects.get(telegram_id=str(telegram_id))
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f"Xush kelibsiz, {user.first_name}!")
        return redirect('core:home')
    except User.DoesNotExist:
        messages.error(request, "Foydalanuvchi topilmadi.")
        return redirect('accounts:login')


@csrf_exempt
def telegram_miniapp_auth_view(request):
    """Telegram Mini App orqali login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            init_data = data.get('initData')
            
            if not init_data:
                return JsonResponse({'success': False, 'error': 'initData topilmadi'})
            
            tg_user = verify_telegram_webapp_data(init_data)
            
            if not tg_user:
                return JsonResponse({'success': False, 'error': 'initData noto\'g\'ri'})
            
            telegram_id = str(tg_user.get('id'))
            telegram_username = tg_user.get('username', '')
            
            # Foydalanuvchini topish yoki yaratish
            try:
                user = User.objects.get(telegram_id=telegram_id)
            except User.DoesNotExist:
                user = User.objects.create(
                    telegram_id=telegram_id,
                    telegram_username=telegram_username,
                    first_name=tg_user.get('first_name', 'User'),
                    last_name=tg_user.get('last_name', ''),
                    auth_provider='telegram'
                )
                user.set_unusable_password()
                user.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({
                'success': True, 
                'redirect': '/',
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST so\'rov kerak'})


def verify_telegram_webapp_data(init_data: str) -> dict | None:
    """Telegram Mini App initData ni tekshirish"""
    from urllib.parse import parse_qs, unquote
    
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return None
    
    parsed_data = parse_qs(init_data)
    
    received_hash = parsed_data.get('hash', [None])[0]
    if not received_hash:
        return None
    
    data_check_arr = []
    for key in sorted(parsed_data.keys()):
        if key != 'hash':
            value = parsed_data[key][0]
            data_check_arr.append(f"{key}={value}")
    data_check_string = '\n'.join(data_check_arr)
    
    secret_key = hmac.new(
        b'WebAppData',
        bot_token.encode(),
        hashlib.sha256
    ).digest()
    
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if calculated_hash != received_hash:
        return None
    
    auth_date = int(parsed_data.get('auth_date', [0])[0])
    if time.time() - auth_date > 86400:
        return None
    
    user_data = parsed_data.get('user', [None])[0]
    if user_data:
        return json.loads(unquote(user_data))
    
    return None



@login_required
def profile_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Parolni o'zgartirish
        if action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not request.user.check_password(current_password):
                messages.error(request, "Joriy parol noto'g'ri!")
                return redirect('accounts:profile')
            
            if new_password != confirm_password:
                messages.error(request, "Yangi parollar mos kelmayapti!")
                return redirect('accounts:profile')
            
            if len(new_password) < 8:
                messages.error(request, "Parol kamida 8 ta belgidan iborat bo'lishi kerak!")
                return redirect('accounts:profile')
            
            request.user.set_password(new_password)
            request.user.save()
            
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")
            return redirect('accounts:profile')
        
        # Profil ma'lumotlarini yangilash
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi!")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # Fanlar bo'yicha progress
    from core.models import Subject, TopicResult, Topic
    subjects_progress = []
    
    user_topic_ids = TopicResult.objects.filter(user=request.user).values_list('topic_id', flat=True).distinct()
    user_subjects = Subject.objects.filter(
        topics__id__in=user_topic_ids,
        is_active=True
    ).distinct().prefetch_related('topics')
    
    for subject in user_subjects:
        all_topics = Topic.objects.filter(subject=subject, is_active=True)
        total_topics = all_topics.count()
        
        user_results = TopicResult.objects.filter(user=request.user, topic__subject=subject)
        completed_topics = user_results.values('topic').distinct().count()
        passed_topics = user_results.filter(passed=True).values('topic').distinct().count()
        
        progress_percentage = int((passed_topics / total_topics) * 100) if total_topics > 0 else 0
        
        subjects_progress.append({
            'subject': subject,
            'total_tests': total_topics,
            'completed_tests': completed_topics,
            'passed_tests': passed_topics,
            'progress_percentage': progress_percentage,
        })
    
    # User stats
    from core.models import TopicResult, CertificateResult, MockExamResult
    total_tests = TopicResult.objects.filter(user=request.user).count()
    total_tests += CertificateResult.objects.filter(user=request.user).count()
    total_tests += MockExamResult.objects.filter(user=request.user).count()
    
    passed_tests = TopicResult.objects.filter(user=request.user, passed=True).count()
    passed_tests += CertificateResult.objects.filter(user=request.user, passed=True).count()
    passed_tests += MockExamResult.objects.filter(user=request.user, passed=True).count()
    
    progress = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0
    
    user_stats = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'progress': progress,
    }
    
    # User position
    user_position = None
    if request.user.total_points > 0:
        higher_users_count = User.objects.filter(total_points__gt=request.user.total_points).count()
        user_position = higher_users_count + 1
    
    context = {
        'form': form,
        'subjects_progress': subjects_progress,
        'user_stats': user_stats,
        'user_position': user_position,
    }
    
    if is_mobile(request):
        return render(request, 'accounts/profile.html', context)
    else:
        return render(request, 'accounts/profile_desktop.html', context)
