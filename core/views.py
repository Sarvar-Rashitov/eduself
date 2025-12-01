from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import (
    Subject, Topic, Test, Question, Answer, TestResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    Institution, InstitutionType, Advertisement, Statistic, SiteSettings
)

def home_view(request):
    subjects = Subject.objects.filter(is_active=True)[:6]
    certificates = Certificate.objects.filter(is_active=True)[:4]
    institutions = Institution.objects.filter(is_featured=True, is_active=True)[:4]
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    statistics = Statistic.objects.all()
    
    user_stats = {}
    if request.user.is_authenticated:
        user_stats = {
            'total_tests': request.user.get_total_tests_taken(),
            'passed_tests': request.user.get_passed_tests(),
            'progress': request.user.get_progress_percentage(),
        }
    
    context = {
        'subjects': subjects,
        'certificates': certificates,
        'institutions': institutions,
        'advertisements': advertisements,
        'statistics': statistics,
        'user_stats': user_stats,
    }
    return render(request, 'core/home.html', context)


def subjects_view(request):
    subjects = Subject.objects.filter(is_active=True)
    return render(request, 'core/subjects.html', {'subjects': subjects})


def subject_detail_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, is_active=True)
    topics = subject.topics.filter(is_active=True)
    return render(request, 'core/subject_detail.html', {'subject': subject, 'topics': topics})


def topic_detail_view(request, pk):
    topic = get_object_or_404(Topic, pk=pk, is_active=True)
    tests = topic.tests.filter(is_active=True)
    
    user_results = {}
    if request.user.is_authenticated:
        for test in tests:
            result = TestResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
            if result:
                user_results[test.id] = result
    
    return render(request, 'core/topic_detail.html', {'topic': topic, 'tests': tests, 'user_results': user_results})


@login_required
def take_test_view(request, pk):
    test = get_object_or_404(Test, pk=pk, is_active=True)
    questions = test.questions.all().prefetch_related('answers')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                answer = Answer.objects.filter(id=selected_answer, question=question, is_correct=True).first()
                if answer:
                    correct += 1
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= test.passing_score
        
        TestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed
        )
        
        messages.success(request, f"Test yakunlandi! Natija: {score}% ({correct}/{total})")
        return redirect('core:test_result', pk=test.pk)
    
    return render(request, 'core/take_test.html', {'test': test, 'questions': questions})


@login_required
def test_result_view(request, pk):
    test = get_object_or_404(Test, pk=pk)
    result = TestResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    return render(request, 'core/test_result.html', {'test': test, 'result': result})


def certificates_view(request):
    certificates = Certificate.objects.filter(is_active=True)
    return render(request, 'core/certificates.html', {'certificates': certificates})


def certificate_detail_view(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk, is_active=True)
    topics = certificate.cert_topics.filter(is_active=True)
    return render(request, 'core/certificate_detail.html', {'certificate': certificate, 'topics': topics})


def cert_topic_detail_view(request, pk):
    topic = get_object_or_404(CertificateTopic, pk=pk, is_active=True)
    tests = topic.cert_tests.filter(is_active=True)
    
    user_results = {}
    if request.user.is_authenticated:
        for test in tests:
            result = CertificateResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
            if result:
                user_results[test.id] = result
    
    return render(request, 'core/cert_topic_detail.html', {'topic': topic, 'tests': tests, 'user_results': user_results})


@login_required
def take_cert_test_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk, is_active=True)
    questions = test.cert_questions.all().prefetch_related('cert_answers')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                answer = CertificateAnswer.objects.filter(id=selected_answer, question=question, is_correct=True).first()
                if answer:
                    correct += 1
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= test.passing_score
        
        CertificateResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed
        )
        
        messages.success(request, f"Test yakunlandi! Natija: {score}% ({correct}/{total})")
        return redirect('core:cert_test_result', pk=test.pk)
    
    return render(request, 'core/take_cert_test.html', {'test': test, 'questions': questions})


@login_required
def cert_test_result_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk)
    result = CertificateResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    return render(request, 'core/cert_test_result.html', {'test': test, 'result': result})


def mock_exams_view(request):
    exams = MockExam.objects.filter(is_active=True)
    
    user_results = {}
    if request.user.is_authenticated:
        for exam in exams:
            result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
            if result:
                user_results[exam.id] = result
    
    return render(request, 'core/mock_exams.html', {'exams': exams, 'user_results': user_results})


@login_required
def take_mock_exam_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk, is_active=True)
    questions = exam.mock_questions.all().prefetch_related('mock_answers')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                answer = MockExamAnswer.objects.filter(id=selected_answer, question=question, is_correct=True).first()
                if answer:
                    correct += 1
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= exam.passing_score
        
        MockExamResult.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed
        )
        
        messages.success(request, f"Imtihon yakunlandi! Natija: {score}% ({correct}/{total})")
        return redirect('core:mock_exam_result', pk=exam.pk)
    
    return render(request, 'core/take_mock_exam.html', {'exam': exam, 'questions': questions})


@login_required
def mock_exam_result_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk)
    result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
    return render(request, 'core/mock_exam_result.html', {'exam': exam, 'result': result})


def institutions_view(request):
    institution_type = request.GET.get('type', 'all')
    
    if institution_type == 'training':
        institutions = Institution.objects.filter(institution_type=InstitutionType.TRAINING_CENTER, is_active=True)
        title = "O'quv markazlari"
    elif institution_type == 'schools':
        institutions = Institution.objects.filter(
            institution_type__in=[InstitutionType.STATE_SCHOOL, InstitutionType.PRIVATE_SCHOOL],
            is_active=True
        )
        title = "Maktablar"
    elif institution_type == 'universities':
        institutions = Institution.objects.filter(
            institution_type__in=[InstitutionType.STATE_UNIVERSITY, InstitutionType.FOREIGN_BRANCH, InstitutionType.PRIVATE_UNIVERSITY],
            is_active=True
        )
        title = "Oliy ta'lim muassasalari"
    else:
        institutions = Institution.objects.filter(is_active=True)
        title = "Barcha ta'lim muassasalari"
    
    training_centers = Institution.objects.filter(institution_type=InstitutionType.TRAINING_CENTER, is_active=True).count()
    schools = Institution.objects.filter(
        institution_type__in=[InstitutionType.STATE_SCHOOL, InstitutionType.PRIVATE_SCHOOL],
        is_active=True
    ).count()
    universities = Institution.objects.filter(
        institution_type__in=[InstitutionType.STATE_UNIVERSITY, InstitutionType.FOREIGN_BRANCH, InstitutionType.PRIVATE_UNIVERSITY],
        is_active=True
    ).count()
    
    context = {
        'institutions': institutions,
        'title': title,
        'current_type': institution_type,
        'training_centers_count': training_centers,
        'schools_count': schools,
        'universities_count': universities,
    }
    return render(request, 'core/institutions.html', context)


def institution_detail_view(request, pk):
    institution = get_object_or_404(Institution, pk=pk, is_active=True)
    return render(request, 'core/institution_detail.html', {'institution': institution})
