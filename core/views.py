from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import (
    Subject, Topic, Test, Question, Answer, TestResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExamCategory, MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    Institution, InstitutionType, Advertisement, Statistic, SiteSettings,
    NewsCategory, News,
    CourseCategory, Course, Lesson, CourseEnrollment
)

def home_view(request):
    subjects = Subject.objects.filter(is_active=True)[:3]
    certificates = Certificate.objects.filter(is_active=True)[:3]
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
def test_leaderboard_view(request, pk):
    test = get_object_or_404(Test, pk=pk, is_active=True)
    
    # Har bir foydalanuvchining eng yaxshi natijasini olish
    from django.db.models import Max
    best_scores = TestResult.objects.filter(test=test).values('user').annotate(
        best_score=Max('score')
    ).values_list('user', 'best_score')
    
    # Har bir foydalanuvchi uchun eng yaxshi natijani topish
    top_results = []
    for user_id, best_score in best_scores:
        result = TestResult.objects.filter(
            test=test, 
            user_id=user_id, 
            score=best_score
        ).select_related('user').order_by('-completed_at').first()
        if result:
            top_results.append(result)
    
    # Ball bo'yicha saralash va top 10 ni olish
    top_results = sorted(top_results, key=lambda x: (-x.score, x.completed_at))[:10]
    
    # Foydalanuvchining eng yaxshi natijasi
    user_best = TestResult.objects.filter(test=test, user=request.user).order_by('-score').first()
    
    context = {
        'test': test,
        'top_results': top_results,
        'user_best': user_best,
    }
    return render(request, 'core/test_leaderboard.html', context)


@login_required
def take_test_view(request, pk):
    test = get_object_or_404(Test, pk=pk, is_active=True)
    questions = test.questions.all().prefetch_related('answers')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                try:
                    selected_answer_id = int(selected_answer)
                    answer = Answer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        user_answers[str(question.id)] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': answer.is_correct
                        }
                        if answer.is_correct:
                            correct += 1
                except (ValueError, TypeError):
                    pass
            else:
                user_answers[str(question.id)] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False
                }
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= test.passing_score
        
        TestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            user_answers=user_answers
        )
        
        messages.success(request, f"Test yakunlandi! Natija: {score}% ({correct}/{total})")
        return redirect('core:test_result', pk=test.pk)
    
    return render(request, 'core/take_test.html', {'test': test, 'questions': questions})


@login_required
def test_result_view(request, pk):
    test = get_object_or_404(Test, pk=pk)
    result = TestResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    return render(request, 'core/test_result.html', {'test': test, 'result': result})


@login_required
def test_analysis_view(request, pk):
    test = get_object_or_404(Test, pk=pk)
    result = TestResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    
    if not result:
        messages.error(request, "Natija topilmadi.")
        return redirect('core:test_result', pk=test.pk)
    
    questions = test.questions.all().prefetch_related('answers')
    analysis_data = []
    
    for question in questions:
        question_data = {
            'question': question,
            'all_answers': question.answers.all(),
            'user_answer': None,
            'correct_answer': None,
            'is_correct': False
        }
        
        # Foydalanuvchi javobini topish
        user_answer_data = result.user_answers.get(str(question.id))
        if user_answer_data:
            question_data['user_answer'] = user_answer_data
            question_data['is_correct'] = user_answer_data.get('is_correct', False)
        
        # To'g'ri javobni topish
        correct_answer = question.answers.filter(is_correct=True).first()
        if correct_answer:
            question_data['correct_answer'] = correct_answer
        
        analysis_data.append(question_data)
    
    context = {
        'test': test,
        'result': result,
        'analysis_data': analysis_data,
    }
    return render(request, 'core/test_analysis.html', context)


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
def cert_test_leaderboard_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk, is_active=True)
    
    # Har bir foydalanuvchining eng yaxshi natijasini olish
    from django.db.models import Max
    best_scores = CertificateResult.objects.filter(test=test).values('user').annotate(
        best_score=Max('score')
    ).values_list('user', 'best_score')
    
    # Har bir foydalanuvchi uchun eng yaxshi natijani topish
    top_results = []
    for user_id, best_score in best_scores:
        result = CertificateResult.objects.filter(
            test=test, 
            user_id=user_id, 
            score=best_score
        ).select_related('user').order_by('-completed_at').first()
        if result:
            top_results.append(result)
    
    # Ball bo'yicha saralash va top 10 ni olish
    top_results = sorted(top_results, key=lambda x: (-x.score, x.completed_at))[:10]
    
    # Foydalanuvchining eng yaxshi natijasi
    user_best = CertificateResult.objects.filter(test=test, user=request.user).order_by('-score').first()
    
    context = {
        'test': test,
        'top_results': top_results,
        'user_best': user_best,
    }
    return render(request, 'core/cert_test_leaderboard.html', context)


@login_required
def take_cert_test_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk, is_active=True)
    questions = test.cert_questions.all().prefetch_related('cert_answers')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                try:
                    selected_answer_id = int(selected_answer)
                    answer = CertificateAnswer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        user_answers[str(question.id)] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': answer.is_correct
                        }
                        if answer.is_correct:
                            correct += 1
                except (ValueError, TypeError):
                    pass
            else:
                user_answers[str(question.id)] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False
                }
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= test.passing_score
        
        CertificateResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            user_answers=user_answers
        )
        
        messages.success(request, f"Test yakunlandi! Natija: {score}% ({correct}/{total})")
        return redirect('core:cert_test_result', pk=test.pk)
    
    return render(request, 'core/take_cert_test.html', {'test': test, 'questions': questions})


@login_required
def cert_test_result_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk)
    result = CertificateResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    return render(request, 'core/cert_test_result.html', {'test': test, 'result': result})


@login_required
def cert_test_analysis_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk)
    result = CertificateResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    
    if not result:
        messages.error(request, "Natija topilmadi.")
        return redirect('core:cert_test_result', pk=test.pk)
    
    questions = test.cert_questions.all().prefetch_related('cert_answers')
    analysis_data = []
    
    for question in questions:
        question_data = {
            'question': question,
            'all_answers': question.cert_answers.all(),
            'user_answer': None,
            'correct_answer': None,
            'is_correct': False
        }
        
        # Foydalanuvchi javobini topish
        user_answer_data = result.user_answers.get(str(question.id))
        if user_answer_data:
            question_data['user_answer'] = user_answer_data
            question_data['is_correct'] = user_answer_data.get('is_correct', False)
        
        # To'g'ri javobni topish
        correct_answer = question.cert_answers.filter(is_correct=True).first()
        if correct_answer:
            question_data['correct_answer'] = correct_answer
        
        analysis_data.append(question_data)
    
    context = {
        'test': test,
        'result': result,
        'analysis_data': analysis_data,
    }
    return render(request, 'core/cert_test_analysis.html', context)


def mock_exams_view(request):
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(MockExamCategory, slug=category_slug, is_active=True)
        exams = MockExam.objects.filter(category=category, is_active=True)
        title = category.name
    else:
        exams = MockExam.objects.filter(is_active=True)
        title = "Barcha Mock Imtihonlar"
        category = None
    
    categories = MockExamCategory.objects.filter(is_active=True)
    
    user_results = {}
    if request.user.is_authenticated:
        for exam in exams:
            result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
            if result:
                user_results[exam.id] = result
    
    context = {
        'exams': exams,
        'categories': categories,
        'current_category': category,
        'title': title,
        'user_results': user_results,
    }
    return render(request, 'core/mock_exams.html', context)


@login_required
def mock_exam_leaderboard_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk, is_active=True)
    
    # Har bir foydalanuvchining eng yaxshi natijasini olish
    from django.db.models import Max
    best_scores = MockExamResult.objects.filter(exam=exam).values('user').annotate(
        best_score=Max('score')
    ).values_list('user', 'best_score')
    
    # Har bir foydalanuvchi uchun eng yaxshi natijani topish
    top_results = []
    for user_id, best_score in best_scores:
        result = MockExamResult.objects.filter(
            exam=exam, 
            user_id=user_id, 
            score=best_score
        ).select_related('user').order_by('-completed_at').first()
        if result:
            top_results.append(result)
    
    # Ball bo'yicha saralash va top 10 ni olish
    top_results = sorted(top_results, key=lambda x: (-x.score, x.completed_at))[:10]
    
    # Foydalanuvchining eng yaxshi natijasi
    user_best = MockExamResult.objects.filter(exam=exam, user=request.user).order_by('-score').first()
    
    context = {
        'exam': exam,
        'top_results': top_results,
        'user_best': user_best,
    }
    return render(request, 'core/mock_exam_leaderboard.html', context)


@login_required
def take_mock_exam_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk, is_active=True)
    questions = exam.mock_questions.all().prefetch_related('mock_answers')
    
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if selected_answer:
                try:
                    selected_answer_id = int(selected_answer)
                    answer = MockExamAnswer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        user_answers[str(question.id)] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': answer.is_correct
                        }
                        if answer.is_correct:
                            correct += 1
                except (ValueError, TypeError):
                    pass
            else:
                user_answers[str(question.id)] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False
                }
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= exam.passing_score
        
        MockExamResult.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            user_answers=user_answers
        )
        
        messages.success(request, f"Imtihon yakunlandi! Natija: {score}% ({correct}/{total})")
        return redirect('core:mock_exam_result', pk=exam.pk)
    
    return render(request, 'core/take_mock_exam.html', {'exam': exam, 'questions': questions})


@login_required
def mock_exam_result_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk)
    result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
    return render(request, 'core/mock_exam_result.html', {'exam': exam, 'result': result})


@login_required
def mock_exam_analysis_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk)
    result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
    
    if not result:
        messages.error(request, "Natija topilmadi.")
        return redirect('core:mock_exam_result', pk=exam.pk)
    
    questions = exam.mock_questions.all().prefetch_related('mock_answers')
    analysis_data = []
    
    for question in questions:
        question_data = {
            'question': question,
            'all_answers': question.mock_answers.all(),
            'user_answer': None,
            'correct_answer': None,
            'is_correct': False
        }
        
        # Foydalanuvchi javobini topish
        user_answer_data = result.user_answers.get(str(question.id))
        if user_answer_data:
            question_data['user_answer'] = user_answer_data
            question_data['is_correct'] = user_answer_data.get('is_correct', False)
        
        # To'g'ri javobni topish
        correct_answer = question.mock_answers.filter(is_correct=True).first()
        if correct_answer:
            question_data['correct_answer'] = correct_answer
        
        analysis_data.append(question_data)
    
    context = {
        'exam': exam,
        'result': result,
        'analysis_data': analysis_data,
    }
    return render(request, 'core/mock_exam_analysis.html', context)


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
    elif institution_type == 'consulting':
        institutions = Institution.objects.filter(institution_type=InstitutionType.CONSULTING, is_active=True)
        title = "Konsalting"
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
    consulting = Institution.objects.filter(institution_type=InstitutionType.CONSULTING, is_active=True).count()
    
    context = {
        'institutions': institutions,
        'title': title,
        'current_type': institution_type,
        'training_centers_count': training_centers,
        'schools_count': schools,
        'universities_count': universities,
        'consulting_count': consulting,
    }
    return render(request, 'core/institutions.html', context)


def institution_detail_view(request, pk):
    institution = get_object_or_404(Institution, pk=pk, is_active=True)
    return render(request, 'core/institution_detail.html', {'institution': institution})


def news_list_view(request):
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(NewsCategory, slug=category_slug, is_active=True)
        news_list = News.objects.filter(category=category, is_published=True)
        title = category.name
    else:
        news_list = News.objects.filter(is_published=True)
        title = "Barcha yangiliklar"
        category = None
    
    categories = NewsCategory.objects.filter(is_active=True)
    featured_news = News.objects.filter(is_featured=True, is_published=True)[:3]
    
    context = {
        'news_list': news_list,
        'categories': categories,
        'featured_news': featured_news,
        'current_category': category,
        'title': title,
    }
    return render(request, 'core/news_list.html', context)


def news_detail_view(request, slug):
    news = get_object_or_404(News, slug=slug, is_published=True)
    news.increment_views()
    
    # O'xshash yangiliklar
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'core/news_detail.html', context)


def courses_view(request):
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(CourseCategory, slug=category_slug, is_active=True)
        courses = Course.objects.filter(category=category, is_active=True)
        title = category.name
    else:
        courses = Course.objects.filter(is_active=True)
        title = "Barcha kurslar"
        category = None
    
    categories = CourseCategory.objects.filter(is_active=True)
    featured_courses = Course.objects.filter(is_featured=True, is_active=True)[:3]
    
    context = {
        'courses': courses,
        'categories': categories,
        'featured_courses': featured_courses,
        'current_category': category,
        'title': title,
    }
    return render(request, 'core/courses.html', context)


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    lessons = course.lessons.filter(is_active=True)
    
    # Foydalanuvchi kursga yozilganmi?
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = CourseEnrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'core/course_detail.html', context)


@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course, is_active=True)
    
    # Foydalanuvchi kursga yozilganmi yoki dars bepulmi?
    is_enrolled = CourseEnrollment.objects.filter(
        user=request.user,
        course=course
    ).exists()
    
    if not is_enrolled and not lesson.is_free and not course.is_free:
        messages.error(request, "Bu darsni ko'rish uchun kursga yozilishingiz kerak.")
        return redirect('core:course_detail', slug=course_slug)
    
    # Kurs darslarini olish
    all_lessons = course.lessons.filter(is_active=True)
    
    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'core/lesson_detail.html', context)


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Foydalanuvchi allaqachon yozilganmi?
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f"Siz '{course.title}' kursiga muvaffaqiyatli yozildingiz!")
    else:
        messages.info(request, "Siz allaqachon bu kursga yozilgansiz.")
    
    return redirect('core:course_detail', slug=course.slug)


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Bildirishnomani o'qilgan deb belgilash
    if notification.is_global or notification.user == request.user:
        if not notification.is_global:
            notification.is_read = True
            notification.save()
    
    # Agar havola bo'lsa, u yerga yo'naltirish
    if notification.link:
        return redirect(notification.link)
    
    return redirect('core:home')
