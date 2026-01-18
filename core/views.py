from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
import json
from .models import (
    SubjectCategory, Subject, Topic, Question, Answer, TopicResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExamCategory, MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    InstitutionCategory, Institution, InstitutionDirection, InstitutionType, Advertisement, Statistic, SiteSettings,
    NewsCategory, News,
    CourseCategory, Course, Lesson, CourseEnrollment,
    Notification,
    DirectionExam, DirectionExamQuestion, DirectionExamAnswer, DirectionExamResult
)

def is_mobile(request):
    """User-Agent orqali mobil qurilmani aniqlash"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'opera mobi']
    return any(keyword in user_agent for keyword in mobile_keywords)


def home_view(request):
    subjects = Subject.objects.filter(is_active=True)[:3]  # 3 ta fan ko'rsatish
    certificates = Certificate.objects.filter(is_active=True)[:3]
    institutions = Institution.objects.filter(is_featured=True, is_active=True)[:4]
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    
    # Dinamik statistikalar
    from accounts.models import User
    total_users = User.objects.count()
    total_questions = Question.objects.count() + CertificateQuestion.objects.count() + MockExamQuestion.objects.count()
    total_certificates = Certificate.objects.filter(is_active=True).count()
    
    # Reyting hisoblash (o'rtacha ball)
    avg_rating = 4.8  # Hozircha statik, keyinchalik dinamik qilish mumkin
    
    # Dinamik statistikalar ro'yxati
    dynamic_statistics = [
        {'title': 'Foydalanuvchilar', 'value': f'{total_users:,}', 'icon': 'users'},
        {'title': 'Savollar', 'value': f'{total_questions:,}', 'icon': 'book'},
        {'title': 'Sertifikatlar', 'value': f'{total_certificates:,}', 'icon': 'trophy'},
        {'title': 'Reyting', 'value': f'{avg_rating}', 'icon': 'star'},
    ]
    
    # Top 3 foydalanuvchilarni olish
    top_users = User.objects.filter(
        total_points__gt=0
    ).select_related().order_by('-total_points')[:3]
    
    user_stats = {}
    user_position = None
    if request.user.is_authenticated:
        user_stats = {
            'total_tests': request.user.get_total_tests_taken(),
            'passed_tests': request.user.get_passed_tests(),
            'progress': request.user.get_progress_percentage(),
        }
        
        # Foydalanuvchining pozitsiyasini topish
        if request.user.total_points > 0:
            higher_users_count = User.objects.filter(total_points__gt=request.user.total_points).count()
            user_position = higher_users_count + 1
    
    context = {
        'subjects': subjects,
        'certificates': certificates,
        'institutions': institutions,
        'advertisements': advertisements,
        'statistics': dynamic_statistics,
        'user_stats': user_stats,
        'top_users': top_users,
        'user_position': user_position,
    }
    
    # Mobil yoki Desktop shablonni tanlash
    if is_mobile(request):
        return render(request, 'core/home.html', context)
    else:
        return render(request, 'core/home_desktop.html', context)


def subjects_view(request):
    category_slug = request.GET.get('category')
    
    # Kategoriya bo'yicha filterlash
    if category_slug:
        category = get_object_or_404(SubjectCategory, slug=category_slug, is_active=True)
        subjects = Subject.objects.filter(category=category, is_active=True)
        title = category.name
        current_category = category
    else:
        current_category = None
        subjects = Subject.objects.filter(is_active=True)
        title = "Barcha fanlar"
    
    # Kategoriyalar ro'yxati
    categories = SubjectCategory.objects.filter(is_active=True)
    
    context = {
        'subjects': subjects,
        'categories': categories,
        'current_category': current_category,
        'title': title,
    }
    
    if is_mobile(request):
        return render(request, 'core/subjects.html', context)
    else:
        return render(request, 'core/subjects_desktop.html', context)


def subject_detail_view(request, pk):
    subject = get_object_or_404(Subject, pk=pk, is_active=True)
    topics = subject.topics.filter(is_active=True).prefetch_related('questions')
    
    # Har bir mavzu uchun foydalanuvchi natijasini olish
    user_results = {}
    if request.user.is_authenticated:
        for topic in topics:
            result = TopicResult.objects.filter(user=request.user, topic=topic).order_by('-completed_at').first()
            if result:
                user_results[topic.id] = result
    
    context = {'subject': subject, 'topics': topics, 'user_results': user_results}
    
    if is_mobile(request):
        return render(request, 'core/subject_detail.html', context)
    else:
        return render(request, 'core/subject_detail_desktop.html', context)


@login_required
def topic_leaderboard_view(request, pk):
    topic = get_object_or_404(Topic, pk=pk, is_active=True)
    
    # Har bir foydalanuvchining eng yaxshi natijasini olish (earned_points bo'yicha)
    from django.db.models import Max
    best_points = TopicResult.objects.filter(topic=topic).values('user').annotate(
        best_points=Max('earned_points')
    ).values_list('user', 'best_points')
    
    # Har bir foydalanuvchi uchun eng yaxshi natijani topish
    top_results = []
    for user_id, best_earned_points in best_points:
        result = TopicResult.objects.filter(
            topic=topic, 
            user_id=user_id, 
            earned_points=best_earned_points
        ).select_related('user').order_by('completed_at').first()
        if result:
            top_results.append(result)
    
    # Ball bo'yicha saralash (yuqoridan pastga), keyin vaqt bo'yicha (tezroq birinchi)
    top_results = sorted(top_results, key=lambda x: (-x.earned_points, x.completed_at))[:10]
    
    # Foydalanuvchining eng yaxshi natijasi
    user_best = TopicResult.objects.filter(topic=topic, user=request.user).order_by('-earned_points', 'completed_at').first()
    
    context = {
        'topic': topic,
        'top_results': top_results,
        'user_best': user_best,
    }
    if is_mobile(request):
        return render(request, 'core/topic_leaderboard.html', context)
    else:
        return render(request, 'core/topic_leaderboard_desktop.html', context)


@login_required
def take_topic_test_view(request, pk):
    topic = get_object_or_404(Topic, pk=pk, is_active=True)
    questions = topic.questions.all().prefetch_related('answers')
    
    if request.method == 'POST':
        # JSON formatdagi javoblarni olish
        answers_data = request.POST.get('answers_data')
        
        if answers_data:
            try:
                user_answers_dict = json.loads(answers_data)
            except json.JSONDecodeError:
                user_answers_dict = {}
        else:
            user_answers_dict = {}
        
        correct = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            question_id_str = str(question.id)
            if question_id_str in user_answers_dict:
                selected_answer_id = user_answers_dict[question_id_str]
                try:
                    answer = Answer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        user_answers[question_id_str] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': answer.is_correct
                        }
                        if answer.is_correct:
                            correct += 1
                except (ValueError, TypeError):
                    pass
            else:
                user_answers[question_id_str] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False
                }
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= topic.passing_score
        
        # Earned points hisoblash - to'g'ri javoblar uchun ball yig'ish
        earned_points = 0
        for question_id, answer_data in user_answers.items():
            if answer_data.get('is_correct', False):
                try:
                    question = Question.objects.get(id=question_id)
                    earned_points += question.points
                except Question.DoesNotExist:
                    continue
        
        TopicResult.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            user_answers=user_answers,
            earned_points=earned_points
        )
        
        return redirect('core:topic_result', pk=topic.pk)
    
    # Reklamalarni olish
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    
    context = {'topic': topic, 'questions': questions, 'advertisements': advertisements}
    if is_mobile(request):
        return render(request, 'core/take_topic_test.html', context)
    else:
        return render(request, 'core/take_topic_test_desktop.html', context)


@login_required
def topic_result_view(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    result = TopicResult.objects.filter(user=request.user, topic=topic).order_by('-completed_at').first()
    
    # Keyingi mavzuni topish
    next_topic = Topic.objects.filter(
        subject=topic.subject,
        is_active=True,
        order__gt=topic.order
    ).order_by('order').first()
    
    context = {
        'topic': topic,
        'result': result,
        'next_topic': next_topic
    }
    if is_mobile(request):
        return render(request, 'core/topic_result.html', context)
    else:
        return render(request, 'core/topic_result_desktop.html', context)


@login_required
def topic_analysis_view(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    result = TopicResult.objects.filter(user=request.user, topic=topic).order_by('-completed_at').first()
    
    if not result:
        messages.error(request, "Natija topilmadi.")
        return redirect('core:topic_result', pk=topic.pk)
    
    questions = topic.questions.all().prefetch_related('answers')
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
        'topic': topic,
        'result': result,
        'analysis_data': analysis_data,
    }
    if is_mobile(request):
        return render(request, 'core/topic_analysis.html', context)
    else:
        return render(request, 'core/topic_analysis_desktop.html', context)


@login_required
def check_answer_view(request, question_id, answer_id):
    """AJAX orqali javobni tekshirish"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            question = get_object_or_404(Question, id=question_id)
            selected_answer = get_object_or_404(Answer, id=answer_id, question=question)
            correct_answer = question.answers.filter(is_correct=True).first()
            
            # Ball ma'lumotini qo'shish
            points_earned = question.points if selected_answer.is_correct else 0
            
            return JsonResponse({
                'is_correct': selected_answer.is_correct,
                'correct_answer': correct_answer.text if correct_answer else '',
                'correct_answer_id': correct_answer.id if correct_answer else None,
                'selected_answer': selected_answer.text,
                'points_earned': points_earned,
                'question_points': question.points
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def certificates_view(request):
    certificates = Certificate.objects.filter(is_active=True)
    context = {'certificates': certificates}
    
    if is_mobile(request):
        return render(request, 'core/certificates.html', context)
    else:
        return render(request, 'core/certificates_desktop.html', context)


def certificate_detail_view(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk, is_active=True)
    topics = certificate.cert_topics.filter(is_active=True)
    
    context = {'certificate': certificate, 'topics': topics}
    
    if is_mobile(request):
        return render(request, 'core/certificate_detail.html', context)
    else:
        return render(request, 'core/certificate_detail_desktop.html', context)


def cert_topic_detail_view(request, pk):
    topic = get_object_or_404(CertificateTopic, pk=pk, is_active=True)
    tests = topic.cert_tests.filter(is_active=True).order_by('order', 'created_at')
    
    user_results = {}
    if request.user.is_authenticated:
        for test in tests:
            result = CertificateResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
            if result:
                user_results[test.id] = result
            # Test ochilganligini tekshirish
            test.is_unlocked = test.is_unlocked_for_user(request.user)
    else:
        # Mehmonlar uchun ham testlar ochiq ko'rinadi
        for test in tests:
            test.is_unlocked = True
    
    context = {'topic': topic, 'tests': tests, 'user_results': user_results}
    if is_mobile(request):
        return render(request, 'core/cert_topic_detail.html', context)
    else:
        return render(request, 'core/cert_topic_detail_desktop.html', context)


@login_required
def cert_test_leaderboard_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk, is_active=True)
    
    # Har bir foydalanuvchining eng yaxshi natijasini olish (earned_points bo'yicha)
    from django.db.models import Max
    best_points = CertificateResult.objects.filter(test=test).values('user').annotate(
        best_points=Max('earned_points')
    ).values_list('user', 'best_points')
    
    # Har bir foydalanuvchi uchun eng yaxshi natijani topish
    top_results = []
    for user_id, best_earned_points in best_points:
        result = CertificateResult.objects.filter(
            test=test, 
            user_id=user_id, 
            earned_points=best_earned_points
        ).select_related('user').order_by('completed_at').first()  # Tezroq yechgan birinchi
        if result:
            top_results.append(result)
    
    # Ball bo'yicha saralash (yuqoridan pastga), keyin vaqt bo'yicha (tezroq birinchi)
    top_results = sorted(top_results, key=lambda x: (-x.earned_points, x.completed_at))[:10]
    
    # Foydalanuvchining eng yaxshi natijasi
    user_best = CertificateResult.objects.filter(test=test, user=request.user).order_by('-earned_points', 'completed_at').first()
    
    context = {
        'test': test,
        'top_results': top_results,
        'user_best': user_best,
    }
    if is_mobile(request):
        return render(request, 'core/cert_test_leaderboard.html', context)
    else:
        return render(request, 'core/cert_test_leaderboard_desktop.html', context)


@login_required
def check_cert_answer_view(request, question_id, answer_id):
    """AJAX orqali sertifikat test javobini tekshirish"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            question = get_object_or_404(CertificateQuestion, id=question_id)
            selected_answer = get_object_or_404(CertificateAnswer, id=answer_id, question=question)
            correct_answer = question.cert_answers.filter(is_correct=True).first()
            
            # Ball ma'lumotini qo'shish (float sifatida)
            points_earned = float(question.points) if selected_answer.is_correct else 0.0
            
            return JsonResponse({
                'is_correct': selected_answer.is_correct,
                'correct_answer': correct_answer.text if correct_answer else '',
                'correct_answer_id': correct_answer.id if correct_answer else None,
                'selected_answer': selected_answer.text,
                'points_earned': points_earned,
                'question_points': float(question.points)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def take_cert_test_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk, is_active=True)
    
    # Test ochilganligini tekshirish
    if not test.is_unlocked_for_user(request.user):
        messages.error(request, "Bu testni yechish uchun oldingi testlarni muvaffaqiyatli yakunlashingiz kerak.")
        return redirect('core:cert_topic_detail', pk=test.topic.pk)
    
    questions = test.cert_questions.all().prefetch_related('cert_answers')
    
    if request.method == 'POST':
        # JSON formatdagi javoblarni olish
        answers_data = request.POST.get('answers_data')
        if answers_data:
            try:
                user_answers_dict = json.loads(answers_data)
            except json.JSONDecodeError:
                user_answers_dict = {}
        else:
            user_answers_dict = {}
        
        correct = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            question_id_str = str(question.id)
            if question_id_str in user_answers_dict:
                selected_answer_id = user_answers_dict[question_id_str]
                try:
                    answer = CertificateAnswer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        user_answers[question_id_str] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': answer.is_correct
                        }
                        if answer.is_correct:
                            correct += 1
                except (ValueError, TypeError):
                    pass
            else:
                user_answers[question_id_str] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False
                }
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= test.passing_score
        
        # Earned points hisoblash - to'g'ri javoblar uchun ball yig'ish
        earned_points = 0
        for question_id, answer_data in user_answers.items():
            if answer_data.get('is_correct', False):
                try:
                    question = CertificateQuestion.objects.get(id=question_id)
                    earned_points += question.points
                except CertificateQuestion.DoesNotExist:
                    continue
        
        CertificateResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            user_answers=user_answers,
            earned_points=earned_points
        )
        
        return redirect('core:cert_test_result', pk=test.pk)
    
    # Reklamalarni olish
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    
    context = {'test': test, 'questions': questions, 'advertisements': advertisements}
    if is_mobile(request):
        return render(request, 'core/take_cert_test.html', context)
    else:
        return render(request, 'core/take_cert_test_desktop.html', context)


@login_required
def cert_test_result_view(request, pk):
    test = get_object_or_404(CertificateTest, pk=pk)
    result = CertificateResult.objects.filter(user=request.user, test=test).order_by('-completed_at').first()
    
    # Keyingi testni topish
    next_test = CertificateTest.objects.filter(
        topic=test.topic,
        is_active=True,
        id__gt=test.id
    ).order_by('id').first()
    
    context = {
        'test': test,
        'result': result,
        'next_test': next_test
    }
    if is_mobile(request):
        return render(request, 'core/cert_test_result.html', context)
    else:
        return render(request, 'core/cert_test_result_desktop.html', context)


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
    if is_mobile(request):
        return render(request, 'core/cert_test_analysis.html', context)
    else:
        return render(request, 'core/cert_test_analysis_desktop.html', context)


def mock_exams_view(request):
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(MockExamCategory, slug=category_slug, is_active=True)
        exams = MockExam.objects.filter(category=category, is_active=True).order_by('order', 'created_at')
        title = category.name
    else:
        exams = MockExam.objects.filter(is_active=True).order_by('order', 'created_at')
        title = "Barcha Mock Imtihonlar"
        category = None
    
    categories = MockExamCategory.objects.filter(is_active=True)
    
    user_results = {}
    if request.user.is_authenticated:
        for exam in exams:
            result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
            if result:
                user_results[exam.id] = result
            # Imtihon ochilganligini tekshirish
            exam.is_unlocked = exam.is_unlocked_for_user(request.user)
    else:
        # Mehmonlar uchun ham imtihonlar ochiq ko'rinadi
        for exam in exams:
            exam.is_unlocked = True
    
    context = {
        'exams': exams,
        'mock_exams': exams,
        'categories': categories,
        'current_category': category,
        'title': title,
        'user_results': user_results,
    }
    
    if is_mobile(request):
        return render(request, 'core/mock_exams.html', context)
    else:
        return render(request, 'core/mock_exams_desktop.html', context)


@login_required
def mock_exam_leaderboard_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk, is_active=True)
    
    # Har bir foydalanuvchining eng yaxshi natijasini olish (earned_points bo'yicha)
    from django.db.models import Max
    best_points = MockExamResult.objects.filter(exam=exam).values('user').annotate(
        best_points=Max('earned_points')
    ).values_list('user', 'best_points')
    
    # Har bir foydalanuvchi uchun eng yaxshi natijani topish
    top_results = []
    for user_id, best_earned_points in best_points:
        result = MockExamResult.objects.filter(
            exam=exam, 
            user_id=user_id, 
            earned_points=best_earned_points
        ).select_related('user').order_by('completed_at').first()  # Tezroq yechgan birinchi
        if result:
            top_results.append(result)
    
    # Ball bo'yicha saralash (yuqoridan pastga), keyin vaqt bo'yicha (tezroq birinchi)
    top_results = sorted(top_results, key=lambda x: (-x.earned_points, x.completed_at))[:10]
    
    # Foydalanuvchining eng yaxshi natijasi
    user_best = MockExamResult.objects.filter(exam=exam, user=request.user).order_by('-earned_points', 'completed_at').first()
    
    context = {
        'exam': exam,
        'top_results': top_results,
        'user_best': user_best,
    }
    if is_mobile(request):
        return render(request, 'core/mock_exam_leaderboard.html', context)
    else:
        return render(request, 'core/mock_exam_leaderboard_desktop.html', context)


@login_required
def check_mock_answer_view(request, question_id, answer_id):
    """AJAX orqali mock exam javobini tekshirish"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            question = get_object_or_404(MockExamQuestion, id=question_id)
            selected_answer = get_object_or_404(MockExamAnswer, id=answer_id, question=question)
            correct_answer = question.mock_answers.filter(is_correct=True).first()
            
            # Ball ma'lumotini qo'shish (float sifatida)
            points_earned = float(question.points) if selected_answer.is_correct else 0.0
            
            return JsonResponse({
                'is_correct': selected_answer.is_correct,
                'correct_answer': correct_answer.text if correct_answer else '',
                'correct_answer_id': correct_answer.id if correct_answer else None,
                'selected_answer': selected_answer.text,
                'points_earned': points_earned,
                'question_points': float(question.points)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def take_mock_exam_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk, is_active=True)
    
    # Imtihon ochilganligini tekshirish
    if not exam.is_unlocked_for_user(request.user):
        messages.error(request, "Bu imtihonni yechish uchun oldingi imtihonlarni muvaffaqiyatli yakunlashingiz kerak.")
        return redirect('core:mock_exams')
    
    questions = exam.mock_questions.all().prefetch_related('mock_answers')
    
    if request.method == 'POST':
        # JSON formatdagi javoblarni olish
        answers_data = request.POST.get('answers_data')
        if answers_data:
            try:
                user_answers_dict = json.loads(answers_data)
            except json.JSONDecodeError:
                user_answers_dict = {}
        else:
            user_answers_dict = {}
        
        correct = 0
        total = questions.count()
        user_answers = {}
        
        for question in questions:
            question_id_str = str(question.id)
            if question_id_str in user_answers_dict:
                selected_answer_id = user_answers_dict[question_id_str]
                try:
                    answer = MockExamAnswer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        user_answers[question_id_str] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': answer.is_correct
                        }
                        if answer.is_correct:
                            correct += 1
                except (ValueError, TypeError):
                    pass
            else:
                user_answers[question_id_str] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False
                }
        
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= exam.passing_score
        
        # Earned points hisoblash - to'g'ri javoblar uchun ball yig'ish
        earned_points = 0
        for question_id, answer_data in user_answers.items():
            if answer_data.get('is_correct', False):
                try:
                    question = MockExamQuestion.objects.get(id=question_id)
                    earned_points += question.points
                except MockExamQuestion.DoesNotExist:
                    continue
        
        MockExamResult.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            user_answers=user_answers,
            earned_points=earned_points
        )
        
        return redirect('core:mock_exam_result', pk=exam.pk)
    
    # Reklamalarni olish
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    
    context = {'exam': exam, 'questions': questions, 'advertisements': advertisements}
    if is_mobile(request):
        return render(request, 'core/take_mock_exam.html', context)
    else:
        return render(request, 'core/take_mock_exam_desktop.html', context)


@login_required
def mock_exam_result_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk)
    result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
    context = {'exam': exam, 'result': result}
    if is_mobile(request):
        return render(request, 'core/mock_exam_result.html', context)
    else:
        return render(request, 'core/mock_exam_result_desktop.html', context)


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
    if is_mobile(request):
        return render(request, 'core/mock_exam_analysis.html', context)
    else:
        return render(request, 'core/mock_exam_analysis_desktop.html', context)


def institutions_view(request):
    category_slug = request.GET.get('category')
    
    # Kategoriya bo'yicha filterlash
    if category_slug:
        category = get_object_or_404(InstitutionCategory, slug=category_slug, is_active=True)
        institutions = Institution.objects.filter(category=category, is_active=True)
        title = category.name
        current_category = category
    else:
        current_category = None
        institutions = Institution.objects.filter(is_active=True)
        title = "Barcha ta'lim muassasalari"
    
    # Kategoriyalar ro'yxati
    categories = InstitutionCategory.objects.filter(is_active=True)
    
    context = {
        'institutions': institutions,
        'categories': categories,
        'current_category': current_category,
        'title': title,
    }
    
    if is_mobile(request):
        return render(request, 'core/institutions.html', context)
    else:
        return render(request, 'core/institutions_desktop.html', context)


def institution_detail_view(request, pk):
    institution = get_object_or_404(Institution, pk=pk, is_active=True)
    directions = institution.directions.filter(is_active=True)
    
    context = {
        'institution': institution,
        'directions': directions
    }
    
    if is_mobile(request):
        return render(request, 'core/institution_detail.html', context)
    else:
        return render(request, 'core/institution_detail_desktop.html', context)


def direction_detail_view(request, pk):
    """Yo'nalish batafsil sahifasi"""
    direction = get_object_or_404(InstitutionDirection, pk=pk, is_active=True)
    context = {'direction': direction}
    if is_mobile(request):
        return render(request, 'core/direction_detail.html', context)
    else:
        return render(request, 'core/direction_detail_desktop.html', context)


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
    
    if is_mobile(request):
        return render(request, 'core/news_list.html', context)
    else:
        return render(request, 'core/news_list_desktop.html', context)


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
    if is_mobile(request):
        return render(request, 'core/news_detail.html', context)
    else:
        return render(request, 'core/news_detail_desktop.html', context)


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
    
    if is_mobile(request):
        return render(request, 'core/courses.html', context)
    else:
        return render(request, 'core/courses_desktop.html', context)


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    lessons = course.lessons.filter(is_active=True)
    
    # Foydalanuvchi kursga yozilganmi va to'lov tasdiqlanganmi?
    is_enrolled = False
    payment_confirmed = False
    if request.user.is_authenticated:
        enrollment = CourseEnrollment.objects.filter(
            user=request.user,
            course=course
        ).first()
        if enrollment:
            is_enrolled = True
            payment_confirmed = enrollment.payment_confirmed
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'payment_confirmed': payment_confirmed,
    }
    if is_mobile(request):
        return render(request, 'core/course_detail.html', context)
    else:
        return render(request, 'core/course_detail_desktop.html', context)


@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course, is_active=True)
    
    # Kurs darslarini olish
    all_lessons = course.lessons.filter(is_active=True).order_by('order')
    first_lesson = all_lessons.first()
    
    # Foydalanuvchi kursga yozilganmi va to'lov tasdiqlanganmi?
    enrollment = CourseEnrollment.objects.filter(
        user=request.user,
        course=course
    ).first()
    
    is_enrolled = enrollment is not None
    payment_confirmed = enrollment.payment_confirmed if enrollment else False
    
    # Ruxsat tekshirish: 
    # 1. Bepul kurs bo'lsa
    # 2. Birinchi dars bo'lsa
    # 3. To'lov tasdiqlangan bo'lsa
    # 4. Dars bepul bo'lsa
    can_access = (
        course.is_free or 
        lesson.is_free or 
        (lesson == first_lesson) or 
        payment_confirmed
    )
    
    if not can_access:
        messages.error(request, "Bu darsni ko'rish uchun to'lovingiz tasdiqlanishi kerak.")
        return redirect('core:course_detail', slug=course_slug)
    
    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'is_enrolled': is_enrolled,
        'payment_confirmed': payment_confirmed,
        'is_first_lesson': lesson == first_lesson,
    }
    if is_mobile(request):
        return render(request, 'core/lesson_detail.html', context)
    else:
        return render(request, 'core/lesson_detail_desktop.html', context)


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Faqat bepul kurslarga avtomatik yozilish imkoni
    if not course.is_free:
        messages.error(request, "Bu pullik kurs. To'lov qilganingizdan keyin yozilishingiz mumkin.")
        return redirect('core:course_detail', slug=course.slug)
    
    # Foydalanuvchi allaqachon yozilganmi?
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'payment_confirmed': True}  # Bepul kurslar uchun avtomatik tasdiqlash
    )
    
    if created:
        messages.success(request, f"Siz '{course.title}' bepul kursiga muvaffaqiyatli yozildingiz!")
    else:
        messages.info(request, "Siz allaqachon bu kursga yozilgansiz.")
    
    return redirect('core:course_detail', slug=course.slug)


@login_required
def enroll_paid_course(request, course_id):
    """Pullik kursga yozilish (to'lov kutilayotgan holatda)"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Faqat pullik kurslar uchun
    if course.is_free:
        messages.error(request, "Bu bepul kurs. Oddiy yozilish tugmasini ishlating.")
        return redirect('core:course_detail', slug=course.slug)
    
    # To'lov URL mavjudligini tekshirish
    if not course.payment_url:
        messages.error(request, "Bu kurs uchun to'lov tizimi hozircha mavjud emas.")
        return redirect('core:course_detail', slug=course.slug)
    
    # Foydalanuvchi allaqachon yozilganmi?
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'payment_confirmed': False}  # To'lov kutilayotgan holat
    )
    
    if created:
        messages.info(request, f"Siz '{course.title}' kursiga yozildingiz. To'lovingiz tasdiqlanganidan keyin barcha darslarga kirishingiz mumkin.")
    else:
        if enrollment.payment_confirmed:
            messages.info(request, "Sizning to'lovingiz allaqachon tasdiqlangan.")
        else:
            messages.info(request, "Siz allaqachon bu kursga yozilgansiz. To'lovingiz tasdiqlanishini kuting.")
    
    return redirect('core:course_detail', slug=course.slug)


def global_leaderboard_view(request):
    """Global leaderboard - barcha foydalanuvchilarni total_points bo'yicha tartiblanish"""
    from accounts.models import User
    
    # Top 100 foydalanuvchini total_points bo'yicha tartiblanish
    top_users_queryset = User.objects.filter(
        total_points__gt=0
    ).select_related().order_by('-total_points')[:100]
    
    # Har bir foydalanuvchi uchun testlar sonini qo'shish
    top_users = []
    for user in top_users_queryset:
        user.tests_completed = user.get_total_tests_taken()
        top_users.append(user)
    
    # Joriy foydalanuvchining pozitsiyasini topish
    user_position = None
    user_points = None
    if request.user.is_authenticated:
        user_points = request.user.total_points
        if user_points > 0:
            # Foydalanuvchidan yuqori ball to'plagan foydalanuvchilar sonini hisoblash
            higher_users_count = User.objects.filter(total_points__gt=user_points).count()
            user_position = higher_users_count + 1
    
    context = {
        'top_users': top_users,
        'users': top_users,
        'user_position': user_position,
        'user_points': user_points,
        'title': 'Global Leaderboard'
    }
    
    if is_mobile(request):
        return render(request, 'core/global_leaderboard.html', context)
    else:
        return render(request, 'core/global_leaderboard_desktop.html', context)


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    # Bildirishnomani o'qilgan deb belgilash
    if notification.is_global or notification.user == request.user:
        notification.is_read = True
        notification.save()
    
    # AJAX so'rov bo'lsa JSON qaytarish
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'success': True})
    
    # Agar havola bo'lsa, u yerga yo'naltirish
    if notification.link:
        return redirect(notification.link)
    
    return redirect('core:home')


@login_required
def mark_all_notifications_read(request):
    """Barcha bildirishnomalarni o'qilgan deb belgilash"""
    if request.method == 'POST':
        Notification.objects.filter(
            Q(user=request.user) | Q(is_global=True),
            is_read=False
        ).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# ==================== Yo'nalish Imtihon View'lari ====================

def direction_exam_intro_view(request, pk):
    """Imtihon boshlash sahifasi - fanlar va vaqt ko'rsatiladi"""
    exam = get_object_or_404(DirectionExam, pk=pk, is_active=True)
    
    context = {
        'exam': exam,
        'subjects_list': exam.get_subjects_list(),
        'questions_count': exam.get_questions_count(),
    }
    
    if is_mobile(request):
        return render(request, 'core/direction_exam_intro.html', context)
    else:
        return render(request, 'core/direction_exam_intro_desktop.html', context)


@login_required
def take_direction_exam_view(request, pk):
    """Yo'nalish imtihonini yechish"""
    exam = get_object_or_404(DirectionExam, pk=pk, is_active=True)
    questions = exam.direction_questions.all().prefetch_related('direction_answers')
    
    if request.method == 'POST':
        answers_data = request.POST.get('answers_data')
        time_taken = request.POST.get('time_taken', 0)
        
        if answers_data:
            try:
                user_answers_dict = json.loads(answers_data)
            except json.JSONDecodeError:
                user_answers_dict = {}
        else:
            user_answers_dict = {}
        
        correct = 0
        total = questions.count()
        user_answers = {}
        earned_points = 0.0
        
        for question in questions:
            question_id_str = str(question.id)
            correct_answer = question.direction_answers.filter(is_correct=True).first()
            
            if question_id_str in user_answers_dict:
                selected_answer_id = user_answers_dict[question_id_str]
                try:
                    answer = DirectionExamAnswer.objects.filter(id=selected_answer_id, question=question).first()
                    if answer:
                        is_correct = answer.is_correct
                        user_answers[question_id_str] = {
                            'selected_answer_id': selected_answer_id,
                            'selected_answer_text': answer.text,
                            'is_correct': is_correct,
                            'correct_answer_id': correct_answer.id if correct_answer else None,
                            'correct_answer_text': correct_answer.text if correct_answer else None,
                            'points': question.points
                        }
                        if is_correct:
                            correct += 1
                            earned_points += question.points
                except (ValueError, TypeError):
                    user_answers[question_id_str] = {
                        'selected_answer_id': None,
                        'selected_answer_text': None,
                        'is_correct': False,
                        'correct_answer_id': correct_answer.id if correct_answer else None,
                        'correct_answer_text': correct_answer.text if correct_answer else None,
                        'points': question.points
                    }
            else:
                user_answers[question_id_str] = {
                    'selected_answer_id': None,
                    'selected_answer_text': None,
                    'is_correct': False,
                    'correct_answer_id': correct_answer.id if correct_answer else None,
                    'correct_answer_text': correct_answer.text if correct_answer else None,
                    'points': question.points
                }
        
        max_points = exam.get_max_points()
        score = (earned_points / max_points * 100) if max_points > 0 else 0
        
        # O'tish balli ball asosida tekshiriladi
        passed = earned_points >= exam.passing_score
        
        result = DirectionExamResult.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total_questions=total,
            correct_answers=correct,
            passed=passed,
            time_taken=int(time_taken),
            user_answers=user_answers,
            earned_points=earned_points
        )
        
        return redirect('core:direction_exam_result', pk=exam.pk)
    
    # Reklamalarni olish
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    
    context = {
        'exam': exam,
        'questions': questions,
        'advertisements': advertisements,
    }
    
    if is_mobile(request):
        return render(request, 'core/take_direction_exam.html', context)
    else:
        return render(request, 'core/take_direction_exam_desktop.html', context)


@login_required
def direction_exam_result_view(request, pk):
    """Yo'nalish imtihon natijasi"""
    exam = get_object_or_404(DirectionExam, pk=pk)
    result = DirectionExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
    
    if not result:
        messages.error(request, "Natija topilmadi.")
        return redirect('core:direction_detail', pk=exam.direction.pk)
    
    context = {
        'exam': exam,
        'result': result,
    }
    
    if is_mobile(request):
        return render(request, 'core/direction_exam_result.html', context)
    else:
        return render(request, 'core/direction_exam_result_desktop.html', context)


@login_required
def direction_exam_analysis_view(request, pk):
    """Yo'nalish imtihon tahlili"""
    exam = get_object_or_404(DirectionExam, pk=pk)
    result = DirectionExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
    
    if not result:
        messages.error(request, "Natija topilmadi.")
        return redirect('core:direction_exam_result', pk=exam.pk)
    
    questions = exam.direction_questions.all().prefetch_related('direction_answers')
    analysis_data = []
    
    for question in questions:
        question_data = {
            'question': question,
            'all_answers': question.direction_answers.all(),
            'user_answer': None,
            'correct_answer': None,
            'is_correct': False,
            'points': question.points
        }
        
        user_answer_data = result.user_answers.get(str(question.id))
        if user_answer_data:
            question_data['user_answer'] = user_answer_data
            question_data['is_correct'] = user_answer_data.get('is_correct', False)
        
        correct_answer = question.direction_answers.filter(is_correct=True).first()
        if correct_answer:
            question_data['correct_answer'] = correct_answer
        
        analysis_data.append(question_data)
    
    context = {
        'exam': exam,
        'result': result,
        'analysis_data': analysis_data,
    }
    
    if is_mobile(request):
        return render(request, 'core/direction_exam_analysis.html', context)
    else:
        return render(request, 'core/direction_exam_analysis_desktop.html', context)
