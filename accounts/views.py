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
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from .models import User, PasswordResetToken, EmailVerificationToken


def is_mobile(request):
    """User-Agent orqali mobil qurilmani aniqlash"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'opera mobi']
    return any(keyword in user_agent for keyword in mobile_keywords)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()
            
            # Email verification token yaratish
            token = EmailVerificationToken.objects.create(user=user)
            
            # Verification email yuborish
            verify_url = request.build_absolute_uri(
                reverse('accounts:verify_email', kwargs={'token': token.token})
            )
            try:
                send_mail(
                    subject='EduSelf - Emailni tasdiqlash',
                    message=f'''Assalomu alaykum, {user.username}!

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
            except Exception:
                messages.success(request, "Ro'yxatdan o'tdingiz!")
            
            login(request, user)
            # POST yoki GET dan next parametrini olish
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
    else:
        form = RegisterForm()
    
    context = {
        'form': form,
        'google_client_id': settings.GOOGLE_CLIENT_ID,
        'telegram_bot_username': settings.TELEGRAM_BOT_USERNAME,
    }
    
    if is_mobile(request):
        return render(request, 'accounts/register.html', context)
    else:
        return render(request, 'accounts/register_desktop.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Tizimga kirdingiz!")
            # POST yoki GET dan next parametrini olish
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
    
    if user.email_verified:
        messages.info(request, "Emailingiz allaqachon tasdiqlangan.")
        return redirect('accounts:profile')
    
    # Yangi token yaratish
    token = EmailVerificationToken.objects.create(user=user)
    
    verify_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={'token': token.token})
    )
    
    try:
        send_mail(
            subject='EduSelf - Emailni tasdiqlash',
            message=f'''Assalomu alaykum, {user.username}!

Emailingizni tasdiqlash uchun quyidagi havolaga o'ting:
{verify_url}

Havola 48 soat ichida amal qiladi.

Hurmat bilan,
EduSelf jamoasi''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(request, "Tasdiqlash havolasi emailingizga yuborildi!")
    except Exception:
        messages.error(request, "Email yuborishda xatolik yuz berdi. Keyinroq urinib ko'ring.")
    
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
                    message=f'''Assalomu alaykum, {user.username}!

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
                username = email.split('@')[0]
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    google_id=google_id,
                    email_verified=True,
                    auth_provider='google'
                )
                user.first_name = name.split()[0] if name else ''
                user.last_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
                user.save()
            
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST so\'rov kerak'})


# Telegram Auth
def telegram_auth_view(request):
    """Telegram OAuth callback"""
    # Telegram ma'lumotlarini olish
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
    if not verify_telegram_auth(telegram_data):
        messages.error(request, "Telegram autentifikatsiya xatosi")
        return redirect('accounts:login')
    
    telegram_id = telegram_data['id']
    
    # Foydalanuvchini topish yoki yaratish
    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        # Yangi foydalanuvchi yaratish
        username = telegram_data['username'] or f"tg_{telegram_id}"
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=f"{telegram_id}@telegram.eduself.uz",
            telegram_id=telegram_id,
            email_verified=True,
            auth_provider='telegram'
        )
        user.first_name = telegram_data['first_name']
        user.last_name = telegram_data['last_name']
        user.save()
    
    login(request, user)
    messages.success(request, "Telegram orqali kirdingiz!")
    return redirect('core:home')


def verify_telegram_auth(data):
    """Telegram auth hash'ni tekshirish"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return False
    
    check_hash = data.pop('hash', None)
    if not check_hash:
        return False
    
    # Auth date tekshirish (24 soatdan eski bo'lmasligi kerak)
    auth_date = int(data.get('auth_date', 0))
    if time.time() - auth_date > 86400:
        return False
    
    # Data string yaratish
    data_check_arr = []
    for key, value in sorted(data.items()):
        if value:
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
            
            # Foydalanuvchini qayta login qilish
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
    from core.models import Subject, TestResult, Test
    subjects_progress = []
    
    user_test_ids = TestResult.objects.filter(user=request.user).values_list('test_id', flat=True).distinct()
    user_subjects = Subject.objects.filter(
        topics__tests__id__in=user_test_ids,
        is_active=True
    ).distinct().prefetch_related('topics__tests')
    
    for subject in user_subjects:
        all_tests = Test.objects.filter(
            topic__subject=subject,
            topic__is_active=True,
            is_active=True
        )
        total_tests = all_tests.count()
        
        user_results = TestResult.objects.filter(
            user=request.user,
            test__topic__subject=subject
        )
        
        completed_tests = user_results.values('test').distinct().count()
        passed_tests = user_results.filter(passed=True).values('test').distinct().count()
        
        progress_percentage = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0
        
        subjects_progress.append({
            'subject': subject,
            'total_tests': total_tests,
            'completed_tests': completed_tests,
            'passed_tests': passed_tests,
            'progress_percentage': progress_percentage,
        })
    
    # Sertifikatlar bo'yicha progress
    from core.models import Certificate, CertificateResult, CertificateTest
    certificates_progress = []
    
    user_cert_test_ids = CertificateResult.objects.filter(user=request.user).values_list('test_id', flat=True).distinct()
    user_certificates = Certificate.objects.filter(
        cert_topics__cert_tests__id__in=user_cert_test_ids,
        is_active=True
    ).distinct().prefetch_related('cert_topics__cert_tests')
    
    for certificate in user_certificates:
        all_tests = CertificateTest.objects.filter(
            topic__certificate=certificate,
            topic__is_active=True,
            is_active=True
        )
        total_tests = all_tests.count()
        
        user_results = CertificateResult.objects.filter(
            user=request.user,
            test__topic__certificate=certificate
        )
        
        completed_tests = user_results.values('test').distinct().count()
        passed_tests = user_results.filter(passed=True).values('test').distinct().count()
        
        progress_percentage = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0
        
        certificates_progress.append({
            'certificate': certificate,
            'total_tests': total_tests,
            'completed_tests': completed_tests,
            'passed_tests': passed_tests,
            'progress_percentage': progress_percentage,
        })
    
    # Mock examlar bo'yicha progress
    from core.models import MockExam, MockExamResult
    mock_exams_progress = []
    
    user_mock_exam_ids = MockExamResult.objects.filter(user=request.user).values_list('exam_id', flat=True).distinct()
    user_mock_exams = MockExam.objects.filter(id__in=user_mock_exam_ids, is_active=True)
    
    for exam in user_mock_exams:
        user_results = MockExamResult.objects.filter(user=request.user, exam=exam)
        
        completed_exams = user_results.count()
        passed_exams = user_results.filter(passed=True).count()
        
        progress_percentage = int((passed_exams / completed_exams) * 100) if completed_exams > 0 else 0
        
        best_result = user_results.order_by('-score').first()
        best_score = best_result.score if best_result else 0
        
        mock_exams_progress.append({
            'exam': exam,
            'completed_exams': completed_exams,
            'passed_exams': passed_exams,
            'progress_percentage': progress_percentage,
            'best_score': best_score,
        })
    
    # User stats for profile cards
    from core.models import TestResult, CertificateResult, MockExamResult
    total_tests = TestResult.objects.filter(user=request.user).count()
    total_tests += CertificateResult.objects.filter(user=request.user).count()
    total_tests += MockExamResult.objects.filter(user=request.user).count()
    
    passed_tests = TestResult.objects.filter(user=request.user, passed=True).count()
    passed_tests += CertificateResult.objects.filter(user=request.user, passed=True).count()
    passed_tests += MockExamResult.objects.filter(user=request.user, passed=True).count()
    
    # Calculate overall progress percentage
    progress = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0
    
    user_stats = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'progress': progress,
    }
    
    # User position in global leaderboard
    user_position = None
    if request.user.total_points > 0:
        higher_users_count = User.objects.filter(total_points__gt=request.user.total_points).count()
        user_position = higher_users_count + 1
    
    # Test results for history tab - barcha turdagi testlarni birlashtirish
    from itertools import chain
    from operator import attrgetter
    
    # Oddiy testlar
    regular_tests = TestResult.objects.filter(user=request.user).select_related('test__topic__subject').order_by('-completed_at')[:20]
    
    # Sertifikat testlari
    cert_tests = CertificateResult.objects.filter(user=request.user).select_related('test__topic__certificate').order_by('-completed_at')[:20]
    
    # Mock examlar
    mock_tests = MockExamResult.objects.filter(user=request.user).select_related('exam').order_by('-completed_at')[:20]
    
    # Barcha natijalarni birlashtirish va saralash
    all_results = []
    
    for result in regular_tests:
        all_results.append({
            'type': 'test',
            'title': result.test.title,
            'subtitle': f"{result.test.topic.subject.name} - {result.test.topic.name}",
            'score': result.score,
            'passed': result.passed,
            'completed_at': result.completed_at,
        })
    
    for result in cert_tests:
        all_results.append({
            'type': 'certificate',
            'title': result.test.title,
            'subtitle': f"{result.test.topic.certificate.name} - {result.test.topic.name}",
            'score': result.score,
            'passed': result.passed,
            'completed_at': result.completed_at,
        })
    
    for result in mock_tests:
        all_results.append({
            'type': 'mock',
            'title': result.exam.title,
            'subtitle': f"Mock Exam - {result.exam.category.name if result.exam.category else 'Umumiy'}",
            'score': result.score,
            'passed': result.passed,
            'completed_at': result.completed_at,
        })
    
    # Sanasi bo'yicha saralash
    all_results.sort(key=lambda x: x['completed_at'], reverse=True)
    test_results = all_results[:15]
    
    # Notifications
    from core.models import Notification
    from django.db.models import Q
    notifications_qs = Notification.objects.filter(
        Q(user=request.user) | Q(is_global=True)
    ).order_by('-created_at')
    unread_notifications_count = notifications_qs.filter(is_read=False).count()
    notifications = notifications_qs[:20]
    
    context = {
        'form': form,
        'subjects_progress': subjects_progress,
        'certificates_progress': certificates_progress,
        'mock_exams_progress': mock_exams_progress,
        'user_stats': user_stats,
        'user_position': user_position,
        'test_results': test_results,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    
    if is_mobile(request):
        return render(request, 'accounts/profile.html', context)
    else:
        return render(request, 'accounts/profile_desktop.html', context)
