from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileForm
from .models import User, PasswordResetToken

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tdingiz!")
            return redirect('core:home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Tizimga kirdingiz!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect('core:home')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            messages.success(request, "Agar bu email ro'yxatdan o'tgan bo'lsa, parolni tiklash havolasi yuborildi.")
            try:
                user = User.objects.get(email=email)
                token = PasswordResetToken.objects.create(user=user)
                reset_link = request.build_absolute_uri(f'/accounts/reset-password/{token.token}/')
                send_mail(
                    subject='EduSelf - Parolni tiklash',
                    message=f'Parolni tiklash uchun quyidagi havolaga o\'ting:\n\n{reset_link}\n\nHavola 24 soat ichida amal qiladi.',
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@eduself.uz',
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


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi!")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # Fanlar bo'yicha progress - FAQAT foydalanuvchi ishlagan fanlar
    from core.models import Subject, TestResult, Test
    subjects_progress = []
    
    # Foydalanuvchi ishlagan testlarning fanlarini topish
    user_test_ids = TestResult.objects.filter(user=request.user).values_list('test_id', flat=True).distinct()
    user_subjects = Subject.objects.filter(
        topics__tests__id__in=user_test_ids,
        is_active=True
    ).distinct().prefetch_related('topics__tests')
    
    for subject in user_subjects:
        # Bu fan bo'yicha barcha testlar
        all_tests = Test.objects.filter(
            topic__subject=subject,
            topic__is_active=True,
            is_active=True
        )
        total_tests = all_tests.count()
        
        # Foydalanuvchi ishlagan testlar
        user_results = TestResult.objects.filter(
            user=request.user,
            test__topic__subject=subject
        )
        
        completed_tests = user_results.values('test').distinct().count()
        passed_tests = user_results.filter(passed=True).values('test').distinct().count()
        
        if total_tests > 0:
            progress_percentage = int((passed_tests / total_tests) * 100)
        else:
            progress_percentage = 0
        
        subjects_progress.append({
            'subject': subject,
            'total_tests': total_tests,
            'completed_tests': completed_tests,
            'passed_tests': passed_tests,
            'progress_percentage': progress_percentage,
        })
    
    # Sertifikatlar bo'yicha progress - FAQAT foydalanuvchi ishlagan sertifikatlar
    from core.models import Certificate, CertificateResult, CertificateTest
    certificates_progress = []
    
    # Foydalanuvchi ishlagan sertifikat testlarini topish
    user_cert_test_ids = CertificateResult.objects.filter(user=request.user).values_list('test_id', flat=True).distinct()
    user_certificates = Certificate.objects.filter(
        cert_topics__cert_tests__id__in=user_cert_test_ids,
        is_active=True
    ).distinct().prefetch_related('cert_topics__cert_tests')
    
    for certificate in user_certificates:
        # Bu sertifikat bo'yicha barcha testlar
        all_tests = CertificateTest.objects.filter(
            topic__certificate=certificate,
            topic__is_active=True,
            is_active=True
        )
        total_tests = all_tests.count()
        
        # Foydalanuvchi ishlagan testlar
        user_results = CertificateResult.objects.filter(
            user=request.user,
            test__topic__certificate=certificate
        )
        
        completed_tests = user_results.values('test').distinct().count()
        passed_tests = user_results.filter(passed=True).values('test').distinct().count()
        
        if total_tests > 0:
            progress_percentage = int((passed_tests / total_tests) * 100)
        else:
            progress_percentage = 0
        
        certificates_progress.append({
            'certificate': certificate,
            'total_tests': total_tests,
            'completed_tests': completed_tests,
            'passed_tests': passed_tests,
            'progress_percentage': progress_percentage,
        })
    
    # Mock examlar bo'yicha progress - FAQAT foydalanuvchi ishlagan mock examlar
    from core.models import MockExam, MockExamResult
    mock_exams_progress = []
    
    # Foydalanuvchi ishlagan mock examlarni topish
    user_mock_exam_ids = MockExamResult.objects.filter(user=request.user).values_list('exam_id', flat=True).distinct()
    user_mock_exams = MockExam.objects.filter(id__in=user_mock_exam_ids, is_active=True)
    
    for exam in user_mock_exams:
        # Foydalanuvchi ishlagan imtihonlar
        user_results = MockExamResult.objects.filter(
            user=request.user,
            exam=exam
        )
        
        completed_exams = user_results.count()
        passed_exams = user_results.filter(passed=True).count()
        
        # Har bir mock exam uchun progress - o'tgan yoki o'tmagan
        if completed_exams > 0:
            progress_percentage = int((passed_exams / completed_exams) * 100) if completed_exams > 0 else 0
        else:
            progress_percentage = 0
        
        # Eng yaxshi natija
        best_result = user_results.order_by('-score').first()
        best_score = best_result.score if best_result else 0
        
        mock_exams_progress.append({
            'exam': exam,
            'completed_exams': completed_exams,
            'passed_exams': passed_exams,
            'progress_percentage': progress_percentage,
            'best_score': best_score,
        })
    
    context = {
        'form': form,
        'subjects_progress': subjects_progress,
        'certificates_progress': certificates_progress,
        'mock_exams_progress': mock_exams_progress,
    }
    
    return render(request, 'accounts/profile.html', context)
