from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import (
    SubjectCategory, Subject, Topic, Question, Answer, TopicResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExamCategory, MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    InstitutionCategory, Institution, InstitutionDirection, InstitutionType, Advertisement, Statistic, SiteSettings,
    NewsCategory, News,
    CourseCategory, Course, Lesson, CourseEnrollment,
    Notification, NotificationRead,
    DirectionExam, DirectionExamQuestion, DirectionExamAnswer, DirectionExamResult, Partner
)
from core.translation import translator

def is_mobile(request):
    """User-Agent orqali mobil qurilmani aniqlash - yaxshilangan versiya"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    # Desktop keywords - agar bular bo'lsa, desktop hisoblanadi
    desktop_keywords = ['windows nt', 'macintosh', 'linux x86_64', 'x11']
    is_desktop = any(keyword in user_agent for keyword in desktop_keywords)
    
    # Agar desktop keyword bo'lsa va mobile keyword bo'lmasa, desktop
    if is_desktop and 'mobile' not in user_agent:
        return False
    
    # Mobile keywords
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'opera mobi']
    
    # iPad alohida tekshirish (tablet)
    if 'ipad' in user_agent:
        # iPad'ni desktop sifatida ko'rsatish (katta ekran)
        return False
    
    return any(keyword in user_agent for keyword in mobile_keywords)


def custom_404_view(request, exception=None):
    """Custom 404 sahifa - Desktop va Mobile uchun"""
    if is_mobile(request):
        # Mobil uchun oddiy 404 sahifa
        return render(request, '404.html', status=404)
    else:
        # Desktop uchun interaktiv 404 sahifa
        return render(request, '404_desktop.html', status=404)


def home_view(request):
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    subjects = Subject.objects.filter(is_active=True)[:3]  # 3 ta fan ko'rsatish
    certificates = Certificate.objects.filter(is_active=True)[:3]
    institutions = Institution.objects.filter(is_featured=True, is_active=True)[:4]
    advertisements = Advertisement.objects.filter(is_active=True)[:5]
    partners = Partner.objects.filter(is_active=True).order_by('order')  # Hamkorlar
    
    # Donat qilganlarni olish (completed va message bor bo'lganlar)
    from subscriptions.models import Donation
    recent_donations = Donation.objects.filter(
        status='completed',
        message__isnull=False
    ).exclude(message='').select_related('user').order_by('-completed_at')[:20]  # 20 ta donat
    
    # CRITICAL: View'da oldindan tarjima qilish (template'da emas!)
    # Bu worker timeout'ni oldini oladi
    if lang != 'uz':
        
        # Institutions'ni tarjima qilish (4 ta)
        for inst in institutions:
            inst.translated_name = translator.translate(inst.name, 'uz', lang, 'home')
            inst.translated_description = ''
            # Category name ham tarjima qilish
            if hasattr(inst, 'category') and inst.category:
                inst.translated_category = translator.translate(inst.category.name, 'uz', lang, 'home')
            else:
                inst.translated_category = ''
        
        # Subjects'ni tarjima qilish (3 ta)
        for subj in subjects:
            subj.translated_name = translator.translate(subj.name, 'uz', lang, 'home')
        
        # Certificates'ni tarjima qilish (2-3 ta)
        for cert in certificates:
            cert.translated_name = translator.translate(cert.name, 'uz', lang, 'home')
            cert.translated_description = ''
        
        # Advertisements'ni tarjima qilish (5 ta) - FAQAT TITLE
        for ad in advertisements:
            ad.translated_title = translator.translate(ad.title, 'uz', lang, 'home')
            ad.translated_description = ''  # Description uzun, tarjima qilmaslik
        
        # Partners'ni tarjima qilish - FAQAT NAME
        for partner in partners:
            partner.translated_name = translator.translate(partner.name, 'uz', lang, 'home')
            partner.translated_description = ''  # Description uzun, tarjima qilmaslik
    else:
        # Uzbek tilida - original matnlar
        for inst in institutions:
            inst.translated_name = inst.name
            inst.translated_description = ''
            inst.translated_category = inst.category.name if hasattr(inst, 'category') and inst.category else ''
        
        for subj in subjects:
            subj.translated_name = subj.name
        
        for cert in certificates:
            cert.translated_name = cert.name
            cert.translated_description = ''
        
        for ad in advertisements:
            ad.translated_title = ad.title
            ad.translated_description = ''
        
        for partner in partners:
            partner.translated_name = partner.name
            partner.translated_description = ''
    
    # Dinamik statistikalar
    from accounts.models import User
    total_users = User.objects.count()
    total_questions = Question.objects.count() + CertificateQuestion.objects.count() + MockExamQuestion.objects.count()
    total_certificates = Certificate.objects.filter(is_active=True).count()
    
    # Reyting hisoblash (o'rtacha XP)
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
    last_test_result = None
    next_test = None
    last_cert_result = None
    next_cert_test = None
    
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
        
        # Oxirgi ishlangan testni topish (Topic)
        last_test_result = TopicResult.objects.filter(
            user=request.user
        ).select_related('topic', 'topic__subject').order_by('-completed_at').first()
        
        # Keyingi testni topish (Topic)
        if last_test_result:
            if last_test_result.passed:
                next_test = Topic.objects.filter(
                    subject=last_test_result.topic.subject,
                    is_active=True,
                    order__gt=last_test_result.topic.order
                ).order_by('order').first()
                
                if not next_test:
                    next_test = Topic.objects.filter(
                        is_active=True
                    ).exclude(
                        id__in=TopicResult.objects.filter(
                            user=request.user,
                            passed=True
                        ).values_list('topic_id', flat=True)
                    ).order_by('subject__order', 'order').first()
            else:
                next_test = last_test_result.topic
        else:
            next_test = Topic.objects.filter(is_active=True).order_by('subject__order', 'order').first()
        
        # Oxirgi sertifikat testini topish
        last_cert_result = CertificateResult.objects.filter(
            user=request.user
        ).select_related('test', 'test__topic').order_by('-completed_at').first()
        
        # Keyingi sertifikat testini topish
        if last_cert_result:
            if last_cert_result.passed:
                # Bir xil topic ichida keyingi testni topish
                next_cert_test = CertificateTest.objects.filter(
                    topic=last_cert_result.test.topic,
                    is_active=True,
                    order__gt=last_cert_result.test.order
                ).order_by('order').first()
                
                if not next_cert_test:
                    # Boshqa topicdan birinchi testni topish
                    next_cert_test = CertificateTest.objects.filter(
                        is_active=True
                    ).exclude(
                        id__in=CertificateResult.objects.filter(
                            user=request.user,
                            passed=True
                        ).values_list('test_id', flat=True)
                    ).order_by('topic__order', 'order').first()
            else:
                next_cert_test = last_cert_result.test
        else:
            next_cert_test = CertificateTest.objects.filter(is_active=True).order_by('topic__order', 'order').first()
    
    context = {
        'subjects': subjects,
        'certificates': certificates,
        'institutions': institutions,
        'advertisements': advertisements,
        'statistics': dynamic_statistics,
        'user_stats': user_stats,
        'top_users': top_users,
        'user_position': user_position,
        'partners': partners,
        'last_test_result': last_test_result,
        'next_test': next_test,
        'last_cert_result': last_cert_result,
        'next_cert_test': next_cert_test,
        'recent_donations': recent_donations,
    }
    
    # Mobil yoki Desktop shablonni tanlash
    if is_mobile(request):
        return render(request, 'core/home.html', context)
    else:
        return render(request, 'core/home_desktop.html', context)


def subjects_view(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    category_slug = request.GET.get('category')
    
    # Foydalanuvchi preferences'ini olish
    user_selected_categories = None
    if request.user.is_authenticated:
        try:
            from accounts.onboarding_models import UserInterestPreference
            preference = request.user.interest_preference
            if preference.onboarding_completed:
                user_selected_categories = preference.selected_categories.get('subjects', [])
        except:
            pass
    
    # Kategoriya bo'yicha filterlash
    if category_slug:
        category = get_object_or_404(SubjectCategory, slug=category_slug, is_active=True)
        subjects = Subject.objects.filter(category=category, is_active=True)
        title = category.name
        current_category = category
    else:
        current_category = None
        # MUHIM: "Barchasi" tabida ham personalizatsiya qilish
        if user_selected_categories:
            # Faqat tanlangan kategoriyalardagi fanlarni ko'rsatish
            subjects = Subject.objects.filter(category_id__in=user_selected_categories, is_active=True)
        else:
            # Agar personalizatsiya bo'lmasa, barcha fanlarni ko'rsatish
            subjects = Subject.objects.filter(is_active=True)
        title = "Barcha fanlar"
    
    # Pagination - 8 ta fan har sahifada
    paginator = Paginator(subjects, 8)
    page = request.GET.get('page', 1)
    
    try:
        subjects_page = paginator.page(page)
    except PageNotAnInteger:
        subjects_page = paginator.page(1)
    except EmptyPage:
        subjects_page = paginator.page(paginator.num_pages)
    
    # Kategoriyalar ro'yxati - faqat tanlangan kategoriyalar
    if user_selected_categories:
        categories = SubjectCategory.objects.filter(id__in=user_selected_categories, is_active=True)
    else:
        categories = SubjectCategory.objects.filter(is_active=True)
    
    context = {
        'subjects': subjects_page,
        'categories': categories,
        'current_category': current_category,
        'title': title,
        'has_personalization': bool(user_selected_categories),
        'paginator': paginator,
        'page_obj': subjects_page,
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
    
    # XP bo'yicha saralash (yuqoridan pastga), keyin vaqt bo'yicha (tezroq birinchi)
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
    
    # Lives tekshirish - test boshlashdan oldin
    from accounts.models import LivesSettings
    lives_settings = LivesSettings.get_settings()
    
    if lives_settings.is_active and not request.user.has_lives():
        messages.error(request, "Yurakchalaringiz tugagan! Keyingi yurakcha tiklanishini kuting yoki ertaga qaytib keling.")
        return redirect('core:topic_leaderboard', pk=topic.pk)
    
    questions = topic.questions.all().prefetch_related('answers')
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # CRITICAL: DO NOT translate questions here - let frontend do it via AJAX
    # This prevents timeout errors when starting tests
    if lang != 'uz':
        topic.translated_name = translator.translate(topic.name, 'uz', lang, 'topic_test')
        topic.translated_description = translator.translate(topic.description, 'uz', lang, 'topic_test') if topic.description else ''
    else:
        topic.translated_name = topic.name
        topic.translated_description = topic.description if topic.description else ''
    
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
        
        # Earned points hisoblash - to'g'ri javoblar uchun XP yig'ish
        earned_points = 0
        for question_id, answer_data in user_answers.items():
            if answer_data.get('is_correct', False):
                try:
                    question = Question.objects.get(id=question_id)
                    earned_points += question.points
                except Question.DoesNotExist:
                    continue
        
        # Oldingi eng yaxshi natijani topish
        previous_best = TopicResult.objects.filter(
            user=request.user,
            topic=topic
        ).order_by('-earned_points').first()
        
        previous_best_points = previous_best.earned_points if previous_best else 0
        
        # Yangi natijani saqlash
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
        
        # Lives tekshirish - muvaffaqiyatsiz bo'lsa yurakcha yo'qotish
        from accounts.models import LivesSettings
        lives_settings = LivesSettings.get_settings()
        
        if lives_settings.is_active and not passed:
            request.user.lose_life()
            messages.warning(request, f"Test muvaffaqiyatsiz! Yurakcha yo'qotdingiz. Qolgan: {request.user.current_lives} ❤️")
        
        # Faqat yangi natija oldingi eng yaxshi natijadan yaxshi bo'lsa, farqni qo'shish
        if earned_points > previous_best_points:
            points_to_add = earned_points - previous_best_points
            request.user.total_points += points_to_add
            request.user.save(update_fields=['total_points'])
        
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
            
            # XP ma'lumotini qo'shish
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


def translate_question_ajax(request, question_id):
    """AJAX orqali savolni tarjima qilish - bitta-bitta"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            question = get_object_or_404(Question, id=question_id)
            lang = request.GET.get('lang', 'uz')
            
            logger.info(f"🔄 Translating question {question_id} to {lang}")
            
            if lang == 'uz':
                return JsonResponse({
                    'question_text': question.text,
                    'answers': [{'id': a.id, 'text': a.text} for a in question.answers.all()]
                })
            
            # Translate question and answers
            translated_question = translator.translate(question.text, 'uz', lang, 'topic_test')
            translated_answers = []
            
            for answer in question.answers.all():
                translated_answer = translator.translate(answer.text, 'uz', lang, 'topic_test')
                translated_answers.append({
                    'id': answer.id,
                    'text': translated_answer
                })
            
            logger.info(f"✅ Question {question_id} translated successfully")
            
            return JsonResponse({
                'question_text': translated_question,
                'answers': translated_answers
            })
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"❌ Translation error for question {question_id}: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def certificates_view(request):
    # Foydalanuvchi preferences'ini olish
    user_selected_certificates = None
    if request.user.is_authenticated:
        try:
            from accounts.onboarding_models import UserInterestPreference
            preference = request.user.interest_preference
            if preference.onboarding_completed:
                user_selected_certificates = preference.selected_categories.get('certificates', [])
        except:
            pass
    
    # Faqat tanlangan sertifikatlar
    if user_selected_certificates:
        certificates = Certificate.objects.filter(id__in=user_selected_certificates, is_active=True)
    else:
        certificates = Certificate.objects.filter(is_active=True)
    
    context = {
        'certificates': certificates,
        'has_personalization': bool(user_selected_certificates),
    }
    
    if is_mobile(request):
        return render(request, 'core/certificates.html', context)
    else:
        return render(request, 'core/certificates_desktop.html', context)


def certificate_detail_view(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk, is_active=True)
    topics = certificate.cert_topics.filter(is_active=True)
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Translate certificate details if not Uzbek
    if lang != 'uz':
        certificate.translated_name = translator.translate(certificate.name, 'uz', lang, 'certificate_detail')
        certificate.translated_description = translator.translate(certificate.description, 'uz', lang, 'certificate_detail') if certificate.description else ''
        
        # Translate topics
        for topic in topics:
            topic.translated_name = translator.translate(topic.name, 'uz', lang, 'certificate_detail')
            topic.translated_description = translator.translate(topic.description, 'uz', lang, 'certificate_detail') if topic.description else ''
    else:
        certificate.translated_name = certificate.name
        certificate.translated_description = certificate.description if certificate.description else ''
        
        for topic in topics:
            topic.translated_name = topic.name
            topic.translated_description = topic.description if topic.description else ''
    
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
    
    # XP bo'yicha saralash (yuqoridan pastga), keyin vaqt bo'yicha (tezroq birinchi)
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
            
            # XP ma'lumotini qo'shish (float sifatida)
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


def translate_cert_question_ajax(request, question_id):
    """AJAX orqali sertifikat savolini tarjima qilish - bitta-bitta"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            question = get_object_or_404(CertificateQuestion, id=question_id)
            lang = request.GET.get('lang', 'uz')
            
            if lang == 'uz':
                return JsonResponse({
                    'question_text': question.text,
                    'answers': [{'id': a.id, 'text': a.text} for a in question.cert_answers.all()]
                })
            
            # Translate question and answers
            translated_question = translator.translate(question.text, 'uz', lang, 'cert_test')
            translated_answers = []
            
            for answer in question.cert_answers.all():
                translated_answer = translator.translate(answer.text, 'uz', lang, 'cert_test')
                translated_answers.append({
                    'id': answer.id,
                    'text': translated_answer
                })
            
            return JsonResponse({
                'question_text': translated_question,
                'answers': translated_answers
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
    
    # Lives tekshirish - test boshlashdan oldin
    from accounts.models import LivesSettings
    lives_settings = LivesSettings.get_settings()
    
    if lives_settings.is_active and not request.user.has_lives():
        messages.error(request, "Yurakchalaringiz tugagan! Keyingi yurakcha tiklanishini kuting yoki ertaga qaytib keling.")
        return redirect('core:cert_test_leaderboard', pk=test.pk)
    
    questions = test.cert_questions.all().prefetch_related('cert_answers')
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # CRITICAL: DO NOT translate questions here - let frontend do it via AJAX
    # This prevents timeout errors when starting tests
    if lang != 'uz':
        test.translated_title = translator.translate(test.title, 'uz', lang, 'cert_test')
        test.translated_description = translator.translate(test.description, 'uz', lang, 'cert_test') if test.description else ''
    else:
        test.translated_title = test.title
        test.translated_description = test.description if test.description else ''
    
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
        
        # Earned points hisoblash - to'g'ri javoblar uchun XP yig'ish
        earned_points = 0
        for question_id, answer_data in user_answers.items():
            if answer_data.get('is_correct', False):
                try:
                    question = CertificateQuestion.objects.get(id=question_id)
                    earned_points += question.points
                except CertificateQuestion.DoesNotExist:
                    continue
        
        # Oldingi eng yaxshi natijani topish
        previous_best = CertificateResult.objects.filter(
            user=request.user,
            test=test
        ).order_by('-earned_points').first()
        
        previous_best_points = previous_best.earned_points if previous_best else 0
        
        # Yangi natijani saqlash
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
        
        # Lives tekshirish - muvaffaqiyatsiz bo'lsa yurakcha yo'qotish
        from accounts.models import LivesSettings
        lives_settings = LivesSettings.get_settings()
        
        if lives_settings.is_active and not passed:
            request.user.lose_life()
            messages.warning(request, f"Test muvaffaqiyatsiz! Yurakcha yo'qotdingiz. Qolgan: {request.user.current_lives} ❤️")
        
        # Faqat yangi natija oldingi eng yaxshi natijadan yaxshi bo'lsa, farqni qo'shish
        if earned_points > previous_best_points:
            points_to_add = earned_points - previous_best_points
            request.user.total_points += points_to_add
            request.user.save(update_fields=['total_points'])
        
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
    
    # Foydalanuvchi preferences'ini olish
    user_selected_categories = None
    if request.user.is_authenticated:
        try:
            from accounts.onboarding_models import UserInterestPreference
            preference = request.user.interest_preference
            if preference.onboarding_completed:
                user_selected_categories = preference.selected_categories.get('mock_exams', [])
        except:
            pass
    
    if category_slug:
        category = get_object_or_404(MockExamCategory, slug=category_slug, is_active=True)
        exams = MockExam.objects.filter(category=category, is_active=True).order_by('order', 'created_at')
        title = category.name
    else:
        # MUHIM: "Barchasi" tabida ham personalizatsiya qilish
        if user_selected_categories:
            # Faqat tanlangan kategoriyalardagi imtihonlarni ko'rsatish
            exams = MockExam.objects.filter(category_id__in=user_selected_categories, is_active=True).order_by('order', 'created_at')
        else:
            # Agar personalizatsiya bo'lmasa, barcha imtihonlarni ko'rsatish
            exams = MockExam.objects.filter(is_active=True).order_by('order', 'created_at')
        title = "Barcha Mock Imtihonlar"
        category = None
    
    # Faqat tanlangan kategoriyalar
    if user_selected_categories:
        categories = MockExamCategory.objects.filter(id__in=user_selected_categories, is_active=True)
    else:
        categories = MockExamCategory.objects.filter(is_active=True)
    
    user_results = {}
    if request.user.is_authenticated:
        for exam in exams:
            result = MockExamResult.objects.filter(user=request.user, exam=exam).order_by('-completed_at').first()
            if result:
                user_results[exam.id] = result
            # Mock imtihonlar uchun barcha imtihonlar ochiq
            exam.is_unlocked = True
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
        'has_personalization': bool(user_selected_categories),
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
    
    # XP bo'yicha saralash (yuqoridan pastga), keyin vaqt bo'yicha (tezroq birinchi)
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
            
            # XP ma'lumotini qo'shish (float sifatida)
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


def translate_mock_question_ajax(request, question_id):
    """AJAX orqali mock exam savolini tarjima qilish - bitta-bitta"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            question = get_object_or_404(MockExamQuestion, id=question_id)
            lang = request.GET.get('lang', 'uz')
            
            if lang == 'uz':
                return JsonResponse({
                    'question_text': question.text,
                    'answers': [{'id': a.id, 'text': a.text} for a in question.mock_answers.all()]
                })
            
            # Translate question and answers
            translated_question = translator.translate(question.text, 'uz', lang, 'mock_exam')
            translated_answers = []
            
            for answer in question.mock_answers.all():
                translated_answer = translator.translate(answer.text, 'uz', lang, 'mock_exam')
                translated_answers.append({
                    'id': answer.id,
                    'text': translated_answer
                })
            
            return JsonResponse({
                'question_text': translated_question,
                'answers': translated_answers
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def take_mock_exam_view(request, pk):
    exam = get_object_or_404(MockExam, pk=pk, is_active=True)
    
    # Lives tekshirish - test boshlashdan oldin
    from accounts.models import LivesSettings
    lives_settings = LivesSettings.get_settings()
    
    if lives_settings.is_active and not request.user.has_lives():
        messages.error(request, "Yurakchalaringiz tugagan! Keyingi yurakcha tiklanishini kuting yoki ertaga qaytib keling.")
        return redirect('core:mock_exam_leaderboard', pk=exam.pk)
    
    # Mock imtihonlar uchun barcha imtihonlar ochiq
    
    questions = exam.mock_questions.all().prefetch_related('mock_answers')
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # CRITICAL: DO NOT translate questions here - let frontend do it via AJAX
    # This prevents timeout errors when starting tests
    if lang != 'uz':
        exam.translated_name = translator.translate(exam.title, 'uz', lang, 'mock_exam')
        exam.translated_description = translator.translate(exam.description, 'uz', lang, 'mock_exam') if exam.description else ''
    else:
        exam.translated_name = exam.title
        exam.translated_description = exam.description if exam.description else ''
    
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
        
        # Earned points hisoblash - to'g'ri javoblar uchun XP yig'ish
        earned_points = 0
        for question_id, answer_data in user_answers.items():
            if answer_data.get('is_correct', False):
                try:
                    question = MockExamQuestion.objects.get(id=question_id)
                    earned_points += question.points
                except MockExamQuestion.DoesNotExist:
                    continue
        
        # Oldingi eng yaxshi natijani topish
        previous_best = MockExamResult.objects.filter(
            user=request.user,
            exam=exam
        ).order_by('-earned_points').first()
        
        previous_best_points = previous_best.earned_points if previous_best else 0
        
        # Yangi natijani saqlash
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
        
        # Lives tekshirish - muvaffaqiyatsiz bo'lsa yurakcha yo'qotish
        from accounts.models import LivesSettings
        lives_settings = LivesSettings.get_settings()
        
        if lives_settings.is_active and not passed:
            request.user.lose_life()
            messages.warning(request, f"Test muvaffaqiyatsiz! Yurakcha yo'qotdingiz. Qolgan: {request.user.current_lives} ❤️")
        
        # Faqat yangi natija oldingi eng yaxshi natijadan yaxshi bo'lsa, farqni qo'shish
        if earned_points > previous_best_points:
            points_to_add = int(earned_points) - int(previous_best_points)
            request.user.total_points += points_to_add
            request.user.save(update_fields=['total_points'])
        
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
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
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
    
    # Pagination - 8 ta muassasa har sahifada
    paginator = Paginator(institutions, 8)
    page = request.GET.get('page', 1)
    
    try:
        institutions_page = paginator.page(page)
    except PageNotAnInteger:
        institutions_page = paginator.page(1)
    except EmptyPage:
        institutions_page = paginator.page(paginator.num_pages)
    
    # Kategoriyalar ro'yxati
    categories = InstitutionCategory.objects.filter(is_active=True)
    
    context = {
        'institutions': institutions_page,
        'categories': categories,
        'current_category': current_category,
        'title': title,
        'paginator': paginator,
        'page_obj': institutions_page,
    }
    
    if is_mobile(request):
        return render(request, 'core/institutions.html', context)
    else:
        return render(request, 'core/institutions_desktop.html', context)


def institution_detail_view(request, pk):
    institution = get_object_or_404(Institution, pk=pk, is_active=True)
    directions = institution.directions.filter(is_active=True)
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Translate institution details if not Uzbek
    if lang != 'uz':
        institution.translated_name = translator.translate(institution.name, 'uz', lang, 'institution_detail')
        institution.translated_short_description = translator.translate(institution.short_description, 'uz', lang, 'institution_detail') if institution.short_description else ''
        
        # Handle long description - split if needed
        if institution.description:
            desc_length = len(institution.description)
            if desc_length > 1000:
                # Split into chunks of 900 chars (leaving buffer)
                chunks = []
                for i in range(0, desc_length, 900):
                    chunk = institution.description[i:i+900]
                    translated_chunk = translator.translate(chunk, 'uz', lang, 'institution_detail')
                    chunks.append(translated_chunk)
                institution.translated_description = ' '.join(chunks)
            else:
                institution.translated_description = translator.translate(institution.description, 'uz', lang, 'institution_detail')
        else:
            institution.translated_description = ''
        
        institution.translated_address = translator.translate(institution.address, 'uz', lang, 'institution_detail') if institution.address else ''
        
        # Translate category
        if institution.category:
            institution.translated_category = translator.translate(institution.category.name, 'uz', lang, 'institution_detail')
        else:
            institution.translated_category = ''
        
        # Translate directions
        for direction in directions:
            direction.translated_name = translator.translate(direction.name, 'uz', lang, 'institution_detail')
            direction.translated_description = translator.translate(direction.description, 'uz', lang, 'institution_detail') if direction.description else ''
    else:
        institution.translated_name = institution.name
        institution.translated_short_description = institution.short_description if institution.short_description else ''
        institution.translated_description = institution.description if institution.description else ''
        institution.translated_address = institution.address if institution.address else ''
        institution.translated_category = institution.category.name if institution.category else ''
        
        for direction in directions:
            direction.translated_name = direction.name
            direction.translated_description = direction.description if direction.description else ''
    
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
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Translate direction details if not Uzbek
    if lang != 'uz':
        direction.translated_name = translator.translate(direction.name, 'uz', lang, 'direction_detail')
        direction.translated_description = translator.translate(direction.description, 'uz', lang, 'direction_detail') if direction.description else ''
        direction.translated_requirements = translator.translate(direction.requirements, 'uz', lang, 'direction_detail') if direction.requirements else ''
        
        # Translate institution name
        if direction.institution:
            direction.translated_institution = translator.translate(direction.institution.name, 'uz', lang, 'direction_detail')
        else:
            direction.translated_institution = ''
    else:
        direction.translated_name = direction.name
        direction.translated_description = direction.description if direction.description else ''
        direction.translated_requirements = direction.requirements if direction.requirements else ''
        direction.translated_institution = direction.institution.name if direction.institution else ''
    
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
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Translate news list if not Uzbek
    if lang != 'uz':
        for news in news_list:
            news.translated_title = translator.translate(news.title, 'uz', lang, 'news')
            news.translated_summary = translator.translate(news.summary, 'uz', lang, 'news')
        
        for news in featured_news:
            news.translated_title = translator.translate(news.title, 'uz', lang, 'news')
            news.translated_summary = translator.translate(news.summary, 'uz', lang, 'news')
    else:
        for news in news_list:
            news.translated_title = news.title
            news.translated_summary = news.summary
        
        for news in featured_news:
            news.translated_title = news.title
            news.translated_summary = news.summary
    
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
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Translate news content if not Uzbek
    if lang != 'uz':
        news.translated_title = translator.translate(news.title, 'uz', lang, 'news_detail')
        
        # Handle long content - split if needed
        if news.content:
            content_length = len(news.content)
            if content_length > 1000:
                # Split into chunks of 900 chars (leaving buffer)
                chunks = []
                for i in range(0, content_length, 900):
                    chunk = news.content[i:i+900]
                    translated_chunk = translator.translate(chunk, 'uz', lang, 'news_detail')
                    chunks.append(translated_chunk)
                news.translated_content = ' '.join(chunks)
            else:
                news.translated_content = translator.translate(news.content, 'uz', lang, 'news_detail')
        else:
            news.translated_content = ''
        
        if news.category:
            news.translated_category = translator.translate(news.category.name, 'uz', lang, 'news_detail')
    else:
        news.translated_title = news.title
        news.translated_content = news.content
        news.translated_category = news.category.name if news.category else ''
    
    # O'xshash yangiliklar
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:3]
    
    # Translate related news
    if lang != 'uz':
        for item in related_news:
            item.translated_title = translator.translate(item.title, 'uz', lang, 'news_detail')
    else:
        for item in related_news:
            item.translated_title = item.title
    
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
    
    # Foydalanuvchi preferences'ini olish
    user_selected_categories = None
    if request.user.is_authenticated:
        try:
            from accounts.onboarding_models import UserInterestPreference
            preference = request.user.interest_preference
            if preference.onboarding_completed:
                user_selected_categories = preference.selected_categories.get('courses', [])
        except:
            pass
    
    if category_slug:
        category = get_object_or_404(CourseCategory, slug=category_slug, is_active=True)
        courses = Course.objects.filter(category=category, is_active=True)
        title = category.name
    else:
        # MUHIM: "Barchasi" tabida ham personalizatsiya qilish
        if user_selected_categories:
            # Faqat tanlangan kategoriyalardagi kurslarni ko'rsatish
            courses = Course.objects.filter(category_id__in=user_selected_categories, is_active=True)
        else:
            # Agar personalizatsiya bo'lmasa, barcha kurslarni ko'rsatish
            courses = Course.objects.filter(is_active=True)
        title = "Barcha kurslar"
        category = None
    
    # Faqat tanlangan kategoriyalar
    if user_selected_categories:
        categories = CourseCategory.objects.filter(id__in=user_selected_categories, is_active=True)
    else:
        categories = CourseCategory.objects.filter(is_active=True)
    
    featured_courses = Course.objects.filter(is_featured=True, is_active=True)[:3]
    
    context = {
        'courses': courses,
        'categories': categories,
        'featured_courses': featured_courses,
        'current_category': category,
        'title': title,
        'has_personalization': bool(user_selected_categories),
    }
    
    if is_mobile(request):
        return render(request, 'core/courses.html', context)
    else:
        return render(request, 'core/courses_desktop.html', context)


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    lessons = course.lessons.filter(is_active=True).order_by('order')
    
    # Foydalanuvchi kursga yozilganmi va to'lov tasdiqlanganmi?
    is_enrolled = False
    payment_confirmed = False
    completed_lessons = []
    
    if request.user.is_authenticated:
        enrollment = CourseEnrollment.objects.filter(
            user=request.user,
            course=course
        ).first()
        if enrollment:
            is_enrolled = True
            payment_confirmed = enrollment.payment_confirmed
            
            # Tugallangan darslar ro'yxatini olish
            from core.models import LessonProgress
            completed_lessons = list(LessonProgress.objects.filter(
                user=request.user,
                lesson__course=course,
                completed=True
            ).values_list('lesson_id', flat=True))
    
    # Har bir dars uchun ochilganligini aniqlash
    lessons_with_status = []
    for i, lesson in enumerate(lessons):
        is_unlocked = False
        
        # Bepul kurs yoki to'lov tasdiqlangan bo'lsa
        if course.is_free or payment_confirmed:
            # Birinchi dars har doim ochiq
            if i == 0:
                is_unlocked = True
            # Bepul dars har doim ochiq
            elif lesson.is_free:
                is_unlocked = True
            # Oldingi dars tugallangan bo'lsa
            elif i > 0:
                previous_lesson = lessons[i-1]
                is_unlocked = previous_lesson.id in completed_lessons
        # Birinchi dars har doim ochiq (demo uchun)
        elif i == 0:
            is_unlocked = True
        # Bepul dars har doim ochiq
        elif lesson.is_free:
            is_unlocked = True
            
        lessons_with_status.append({
            'lesson': lesson,
            'is_unlocked': is_unlocked,
            'is_completed': lesson.id in completed_lessons
        })
    
    context = {
        'course': course,
        'lessons': lessons,
        'lessons_with_status': lessons_with_status,
        'is_enrolled': is_enrolled,
        'payment_confirmed': payment_confirmed,
    }
    if is_mobile(request):
        return render(request, 'core/course_detail.html', context)
    else:
        return render(request, 'core/course_detail_desktop.html', context)


@login_required
def lesson_detail_view(request, course_slug, lesson_id):
    from core.models import LessonProgress
    from django.utils import timezone
    
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course, is_active=True)
    
    # Kurs darslarini olish
    all_lessons = course.lessons.filter(is_active=True).order_by('order')
    all_lessons_list = list(all_lessons)
    first_lesson = all_lessons_list[0] if all_lessons_list else None
    
    # Keyingi darsni topish
    current_index = next((i for i, l in enumerate(all_lessons_list) if l.id == lesson.id), None)
    next_lesson = None
    if current_index is not None and current_index + 1 < len(all_lessons_list):
        next_lesson = all_lessons_list[current_index + 1]
    
    # Foydalanuvchi kursga yozilganmi va to'lov tasdiqlanganmi?
    enrollment = CourseEnrollment.objects.filter(
        user=request.user,
        course=course
    ).first()
    
    is_enrolled = enrollment is not None
    payment_confirmed = enrollment.payment_confirmed if enrollment else False
    
    # Tugallangan darslar
    completed_lessons = list(LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course,
        completed=True
    ).values_list('lesson_id', flat=True))
    
    # Ketma-ket ochish logikasi
    lesson_index = list(all_lessons).index(lesson)
    can_access = False
    
    # Birinchi dars har doim ochiq
    if lesson_index == 0:
        can_access = True
    # Bepul dars har doim ochiq
    elif lesson.is_free:
        can_access = True
    # Bepul kurs yoki to'lov tasdiqlangan bo'lsa
    elif course.is_free or payment_confirmed:
        # Oldingi dars tugallangan bo'lsa
        if lesson_index > 0:
            previous_lesson = all_lessons[lesson_index - 1]
            can_access = previous_lesson.id in completed_lessons
    
    if not can_access:
        messages.error(request, "Bu darsni ko'rish uchun oldingi darsni tugallashingiz kerak.")
        return redirect('core:course_detail', slug=course_slug)
    
    # Darsni ko'rilgan deb belgilash (avtomatik)
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    # Agar dars tugallanmagan bo'lsa, tugallangan deb belgilash
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
    
    # Get current language
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Translate lesson content if not Uzbek
    if lang != 'uz':
        lesson.translated_title = translator.translate(lesson.title, 'uz', lang, 'lesson_detail')
        lesson.translated_content = translator.translate(lesson.content, 'uz', lang, 'lesson_detail')
        lesson.translated_description = translator.translate(lesson.description, 'uz', lang, 'lesson_detail') if lesson.description else ''
        course.translated_title = translator.translate(course.title, 'uz', lang, 'lesson_detail')
    else:
        lesson.translated_title = lesson.title
        lesson.translated_content = lesson.content
        lesson.translated_description = lesson.description if lesson.description else ''
        course.translated_title = course.title
    
    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'next_lesson': next_lesson,
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
            # Foydalanuvchidan yuqori XP to'plagan foydalanuvchilar sonini hisoblash
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
    if notification.is_global:
        # Global bildirishnoma uchun NotificationRead yaratish
        NotificationRead.objects.get_or_create(
            notification=notification,
            user=request.user
        )
    elif notification.user == request.user:
        # Shaxsiy bildirishnoma uchun is_read ni true qilish
        notification.is_read = True
        notification.save()
    
    # AJAX so'rov bo'lsa JSON qaytarish
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'link': notification.link if notification.link else None
        })
    
    # Agar havola bo'lsa, u yerga yo'naltirish
    if notification.link:
        return redirect(notification.link)
    
    return redirect('core:home')


@login_required
def mark_all_notifications_read(request):
    """Barcha bildirishnomalarni o'qilgan deb belgilash"""
    if request.method == 'POST':
        # Shaxsiy bildirishnomalarni o'qilgan deb belgilash
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        # Global bildirishnomalar uchun NotificationRead yaratish
        global_notifications = Notification.objects.filter(is_global=True)
        for notification in global_notifications:
            NotificationRead.objects.get_or_create(
                notification=notification,
                user=request.user
            )
        
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
        
        # O'tish XP asosida tekshiriladi
        passed = earned_points >= exam.passing_score
        
        # Oldingi eng yaxshi natijani topish
        previous_best = DirectionExamResult.objects.filter(
            user=request.user,
            exam=exam
        ).order_by('-earned_points').first()
        
        previous_best_points = float(previous_best.earned_points) if previous_best else 0.0
        
        # Yangi natijani saqlash
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
        
        # Faqat yangi natija oldingi eng yaxshi natijadan yaxshi bo'lsa, farqni qo'shish
        if earned_points > previous_best_points:
            points_to_add = int(earned_points - previous_best_points)
            request.user.total_points += points_to_add
            request.user.save(update_fields=['total_points'])
        
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



def oferta_view(request):
    """Ommaviy oferta sahifasi - Mobile/Desktop detection"""
    if is_mobile(request):
        return render(request, 'core/oferta_mobile.html')
    return render(request, 'core/oferta.html')


def privacy_view(request):
    """Maxfiylik siyosati sahifasi"""
    from datetime import datetime
    context = {
        'current_date': datetime.now().strftime('%d %B %Y')
    }
    return render(request, 'core/privacy.html', context)



def change_language(request):
    """
    Tilni o'zgartirish view
    
    Usage:
        POST /change-language/
        {
            "language": "uz",
            "next": "/courses/"
        }
    """
    from django.utils import translation
    from django.conf import settings
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lang_code = data.get('language')
            next_url = data.get('next', '/')
            
            # Tilni tekshirish
            available_languages = [lang[0] for lang in settings.LANGUAGES]
            if lang_code not in available_languages:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid language code'
                }, status=400)
            
            # Session'ga saqlash
            request.session['django_language'] = lang_code
            translation.activate(lang_code)
            
            # Agar user authenticated bo'lsa, database'ga ham saqlash
            if request.user.is_authenticated:
                request.user.language = lang_code
                request.user.save(update_fields=['language'])
            
            return JsonResponse({
                'success': True,
                'language': lang_code,
                'redirect': next_url
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    # GET request - URL parametrdan til olish
    lang_code = request.GET.get('lang')
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    
    if lang_code:
        available_languages = [lang[0] for lang in settings.LANGUAGES]
        if lang_code in available_languages:
            request.session['django_language'] = lang_code
            translation.activate(lang_code)
            
            if request.user.is_authenticated:
                request.user.language = lang_code
                request.user.save(update_fields=['language'])
    
    return redirect(next_url)


# API endpoint for user profile modal
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def user_profile_api(request, user_id):
    """API endpoint to get user profile data for modal"""
    from accounts.models import User, Badge
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    # Calculate user rank
    higher_users_count = User.objects.filter(total_points__gt=user.total_points).count()
    user_rank = higher_users_count + 1
    
    # Get current level from database
    current_level = user.get_current_level()
    user_level = current_level.level_number if current_level else 0
    
    # Get badges from database
    badges = []
    all_badges = Badge.objects.filter(is_active=True).select_related('required_level').order_by('order')
    
    for badge in all_badges:
        is_unlocked = badge.is_unlocked_for_user(user)
        badge_data = {
            'name': badge.name,
            'image': badge.image.url if badge.image else '',
            'unlocked': is_unlocked
        }
        badges.append(badge_data)
    
    # Weekly activity
    today = timezone.now().date()
    day_names = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya']
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)
    
    weekly_activity = []
    for i in range(7):
        day_date = week_start + timedelta(days=i)
        day_start = timezone.make_aware(timezone.datetime.combine(day_date, timezone.datetime.min.time()))
        day_end = timezone.make_aware(timezone.datetime.combine(day_date, timezone.datetime.max.time()))
        
        # Count activities for this day
        day_activity = TopicResult.objects.filter(
            user=user,
            completed_at__gte=day_start,
            completed_at__lte=day_end
        ).count()
        day_activity += CertificateResult.objects.filter(
            user=user,
            completed_at__gte=day_start,
            completed_at__lte=day_end
        ).count()
        day_activity += MockExamResult.objects.filter(
            user=user,
            completed_at__gte=day_start,
            completed_at__lte=day_end
        ).count()
        
        weekly_activity.append({
            'day_short': day_names[day_date.weekday()],
            'activity': day_activity
        })
    
    # Response data
    data = {
        'username': user.username,
        'full_name': user.get_full_name() or user.username,
        'avatar_url': user.get_avatar_url(),
        'rank': user_rank,
        'total_points': user.total_points,
        'level': user_level,
        'tests_completed': user.get_total_tests_taken(),
        'badges': badges,
        'weekly_activity': weekly_activity
    }
    
    return JsonResponse(data)


# API endpoint for searching users
@require_http_methods(["GET"])
def search_users_api(request):
    """API endpoint to search users by username or name"""
    from accounts.models import User
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'users': []})
    
    # Search users by username or first_name
    users = User.objects.filter(
        Q(username__icontains=query) | Q(first_name__icontains=query),
        total_points__gt=0
    ).order_by('-total_points')[:20]  # Limit to 20 results
    
    # Calculate ranks and format results
    results = []
    for user in users:
        higher_users_count = User.objects.filter(total_points__gt=user.total_points).count()
        user_rank = higher_users_count + 1
        
        results.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name() or user.username,
            'avatar_url': user.get_avatar_url(),
            'rank': user_rank,
            'total_points': user.total_points,
            'tests_completed': user.get_total_tests_taken()
        })
    
    return JsonResponse({'users': results})


# Lives System API
@require_http_methods(["GET"])
def lives_info_api(request):
    """API endpoint to get user's lives information"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    lives_info = request.user.get_lives_info()
    
    # Convert timedelta to seconds for frontend
    if lives_info['next_life_in']:
        lives_info['next_life_in'] = int(lives_info['next_life_in'].total_seconds())
    
    return JsonResponse(lives_info)


# PWA Views
@require_http_methods(["POST"])
@csrf_exempt
def push_subscribe_api(request):
    """
    PWA Push Notification Subscription endpoint
    Foydalanuvchi push notification'ga obuna bo'lganda chaqiriladi
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        import json
        subscription_data = json.loads(request.body)
        
        # TODO: Subscription'ni database'ga saqlash
        # PushSubscription model yaratish kerak:
        # - user (ForeignKey)
        # - endpoint (TextField)
        # - p256dh (TextField)
        # - auth (TextField)
        # - created_at (DateTimeField)
        
        # Hozircha faqat success qaytaramiz
        return JsonResponse({
            'success': True,
            'message': 'Push notification subscription saved'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

def offline_view(request):
    """
    Offline sahifa - Service Worker tomonidan ko'rsatiladi
    """
    return render(request, 'offline.html')


# Service Worker View
def service_worker_view(request):
    """
    Service Worker faylini to'g'ri Content-Type bilan serve qilish
    """
    from django.http import FileResponse
    import os
    from django.conf import settings
    
    sw_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'service-worker.js')
    
    if not os.path.exists(sw_path):
        sw_path = os.path.join(settings.BASE_DIR, 'static', 'service-worker.js')
    
    response = FileResponse(open(sw_path, 'rb'), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

def manifest_view(request):
    """
    Manifest.json faylini to'g'ri Content-Type bilan serve qilish
    """
    from django.http import FileResponse
    import os
    from django.conf import settings
    
    manifest_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'manifest.json')
    
    if not os.path.exists(manifest_path):
        manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    
    response = FileResponse(open(manifest_path, 'rb'), content_type='application/manifest+json')
    response['Cache-Control'] = 'public, max-age=3600'
    return response
