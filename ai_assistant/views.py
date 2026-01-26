from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import json
from .models import ChatSession, ChatMessage, MessageType
from .services import ChatService, InstitutionRecommendationService, TestAnalysisService
from core.models import Subject, Institution, Certificate


def is_mobile(request):
    """User-Agent orqali mobil qurilmani aniqlash"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone', 'opera mini', 'opera mobi']
    return any(keyword in user_agent for keyword in mobile_keywords)


@login_required
def ai_chat_view(request, session_id=None):
    """AI Chat asosiy sahifasi"""
    chat_service = ChatService()
    
    # Foydalanuvchi sessiyalarini olish
    sessions = chat_service.get_user_sessions(request.user)
    
    # Aktiv sessiyani aniqlash
    if not session_id:
        session_id = request.GET.get('session')
    
    current_session = None
    messages_list = []
    
    if session_id:
        try:
            current_session = ChatSession.objects.get(id=session_id, user=request.user)
            messages_list = chat_service.get_session_messages(current_session)
        except ChatSession.DoesNotExist:
            pass
    
    context = {
        'sessions': sessions,
        'chat_sessions': sessions,
        'current_session': current_session,
        'messages': messages_list,
        'messages_list': messages_list,
    }
    
    if is_mobile(request):
        return render(request, 'ai_assistant/chat.html', context)
    else:
        return render(request, 'ai_assistant/chat_desktop.html', context)





@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Xabar yuborish"""
    try:
        # FormData yoki JSON qabul qilish
        content_type = request.content_type
        
        if 'multipart/form-data' in content_type:
            # FormData (rasm bilan)
            session_id = request.POST.get('session_id')
            message_content = request.POST.get('message', '').strip()
            attachment = request.FILES.get('attachment')
        else:
            # JSON
            data = json.loads(request.body)
            session_id = data.get('session_id')
            message_content = data.get('message', '').strip()
            attachment = None
        
        if not message_content and not attachment:
            return JsonResponse({
                'success': False,
                'error': 'Xabar bo\'sh bo\'lishi mumkin emas'
            }, status=400)
        
        # Chat service yaratish
        chat_service = ChatService()
        
        # Agar session_id yo'q bo'lsa, yangi sessiya yaratish
        if not session_id:
            session = chat_service.create_chat_session(request.user, "Yangi suhbat")
        else:
            # Sessiyani olish
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        
        # Agar fayl yuborilgan bo'lsa, xabarga qo'shish
        if attachment:
            file_name = attachment.name
            if not message_content:
                # Fayl turi bo'yicha xabar
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    message_content = f"📷 Rasm yuborildi: {file_name}"
                elif file_name.lower().endswith('.pdf'):
                    message_content = f"📄 PDF fayl yuborildi: {file_name}"
                elif file_name.lower().endswith(('.doc', '.docx')):
                    message_content = f"📝 Word hujjat yuborildi: {file_name}"
                elif file_name.lower().endswith(('.xls', '.xlsx')):
                    message_content = f"📊 Excel fayl yuborildi: {file_name}"
                elif file_name.lower().endswith(('.ppt', '.pptx')):
                    message_content = f"📽️ PowerPoint yuborildi: {file_name}"
                else:
                    message_content = f"📎 Fayl yuborildi: {file_name}"
        
        # Xabar yuborish va AI javobini olish
        ai_response, source = chat_service.send_message(session, message_content, attachment)
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'ai_response': {
                'id': ai_response.id,
                'content': ai_response.content,
                'created_at': ai_response.created_at.strftime('%H:%M'),
                'tokens_used': ai_response.tokens_used,
                'response_time': round(ai_response.response_time, 2),
                'source': source  # 'deepseek' yoki 'fallback'
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Kechirasiz, xatolik yuz berdi. Iltimos, qayta urinib ko\'ring.'
        }, status=500)


@login_required
def get_session_messages(request, session_id):
    """Sessiya xabarlarini olish"""
    try:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        chat_service = ChatService()
        messages_list = chat_service.get_session_messages(session)
        
        messages_data = []
        for msg in messages_list:
            messages_data.append({
                'id': msg.id,
                'type': msg.message_type,
                'content': msg.content,
                'created_at': msg.created_at.strftime('%H:%M'),
                'tokens_used': msg.tokens_used if msg.message_type == MessageType.ASSISTANT else 0
            })
        
        return JsonResponse({
            'success': True,
            'messages': messages_data,
            'session_title': session.title
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_session(request, session_id):
    """Chat sessiyasini o'chirish"""
    try:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        session.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Suhbat o\'chirildi'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def clear_session_messages(request, session_id):
    """Sessiya xabarlarini tozalash (o'chirish)"""
    try:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        # Barcha xabarlarni o'chirish
        session.messages.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Suhbat tozalandi'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def institution_recommendations(request):
    """Muassasa tavsiylari sahifasi"""
    if request.method == 'POST':
        try:
            # Form ma'lumotlarini olish
            institution_type = request.POST.get('institution_type')
            max_price = request.POST.get('max_price')
            location = request.POST.get('location')
            
            # Tavsiya mezonlarini tayyorlash
            criteria = {}
            if institution_type:
                criteria['institution_type'] = institution_type
            if max_price:
                try:
                    criteria['max_price'] = float(max_price)
                except ValueError:
                    pass
            if location:
                criteria['location'] = location
            
            # Tavsiyalarni olish
            recommendations = InstitutionRecommendationService.recommend_institutions(criteria)
            
            context = {
                'recommendations': recommendations,
                'criteria': criteria,
                'form_data': request.POST
            }
            
            return render(request, 'ai_assistant/institution_recommendations.html', context)
        
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    # Institution types for form
    from core.models import InstitutionType
    institution_types = InstitutionType.choices
    
    context = {
        'institution_types': institution_types
    }
    
    return render(request, 'ai_assistant/institution_recommendations.html', context)


@login_required
def ai_help_center(request):
    """AI yordam markazi"""
    # Tez-tez so'raladigan savollar
    faq_data = [
        {
            'category': 'Fanlar bo\'yicha yordam',
            'questions': [
                'Matematika fanini qanday o\'rganish kerak?',
                'Fizika formulalarini yodlash usullari',
                'Kimyo reaksiyalarini tushunish',
                'Biologiya mavzularini takrorlash'
            ]
        },
        {
            'category': 'Muassasa tanlash',
            'questions': [
                'Qaysi universitetni tanlashim kerak?',
                'Kontrakt narxlari qanday?',
                'Qabul talablari nima?',
                'Yo\'nalishlar haqida ma\'lumot'
            ]
        },
        {
            'category': 'Sertifikatlar',
            'questions': [
                'Qanday sertifikatlar mavjud?',
                'Sertifikat olish jarayoni',
                'Test topshirish qoidalari',
                'Sertifikat amal qilish muddati'
            ]
        }
    ]
    
    # Statistika
    total_subjects = Subject.objects.filter(is_active=True).count()
    total_institutions = Institution.objects.filter(is_active=True).count()
    total_certificates = Certificate.objects.filter(is_active=True).count()
    
    context = {
        'faq_data': faq_data,
        'stats': {
            'subjects': total_subjects,
            'institutions': total_institutions,
            'certificates': total_certificates
        }
    }
    
    if is_mobile(request):
        return render(request, 'ai_assistant/help_center.html', context)
    else:
        return render(request, 'ai_assistant/help_center_desktop.html', context)


@login_required
def quick_question(request):
    """Tezkor savol yuborish"""
    if request.method == 'POST':
        try:
            question = request.POST.get('question', '').strip()
            category = request.POST.get('category', 'general')
            
            if not question:
                messages.error(request, 'Savol bo\'sh bo\'lishi mumkin emas')
                return redirect('ai_assistant:help_center')
            
            # Mavjud sessiyani topish yoki yangi yaratish
            chat_service = ChatService()
            sessions = chat_service.get_user_sessions(request.user)
            
            if sessions.exists():
                session = sessions.first()
            else:
                session = chat_service.create_chat_session(
                    request.user, 
                    "Yangi suhbat"
                )
            
            # Savolni yuborish
            chat_service.send_message(session, question)  # tuple qaytaradi, lekin bu yerda kerak emas
            
            return redirect(reverse('ai_assistant:chat') + f'?session={session.id}')
        
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return redirect('ai_assistant:help_center')


def ai_chat_redirect(request):
    """AI Chat sahifasiga yo'naltirish"""
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # Oxirgi sessiyani topish yoki yangi yaratish
    chat_service = ChatService()
    sessions = chat_service.get_user_sessions(request.user)
    
    if sessions.exists():
        latest_session = sessions.first()
        return redirect(reverse('ai_assistant:chat') + f'?session={latest_session.id}')
    else:
        # Avtomatik yangi sessiya yaratish
        session = chat_service.create_chat_session(request.user, "Yangi suhbat")
        return redirect(reverse('ai_assistant:chat') + f'?session={session.id}')


@login_required
def create_new_session(request):
    """Yangi chat sessiyasi yaratish"""
    chat_service = ChatService()
    session = chat_service.create_chat_session(request.user, "Yangi suhbat")
    return redirect(reverse('ai_assistant:chat') + f'?session={session.id}')


@login_required
def analyze_test_result(request, test_type, result_id):
    """Test natijasini AI bilan tahlil qilish"""
    try:
        # Test turini aniqlash va natijani olish
        if test_type == 'topic':
            from core.models import TopicResult
            result = get_object_or_404(TopicResult, id=result_id, user=request.user)
        elif test_type == 'certificate':
            from core.models import CertificateResult
            result = get_object_or_404(CertificateResult, id=result_id, user=request.user)
        elif test_type == 'mock_exam':
            from core.models import MockExamResult
            result = get_object_or_404(MockExamResult, id=result_id, user=request.user)
        elif test_type == 'direction_exam':
            from core.models import DirectionExamResult
            result = get_object_or_404(DirectionExamResult, id=result_id, user=request.user)
        else:
            return JsonResponse({'success': False, 'error': 'Noto\'g\'ri test turi'}, status=400)
        
        # Test tahlil service'ni ishlatish
        analysis_service = TestAnalysisService()
        analysis_result = analysis_service.analyze_test_result(result, test_type)
        
        if analysis_result['success']:
            return JsonResponse({
                'success': True,
                'ai_recommendation': analysis_result['ai_recommendation'],
                'recommendations': analysis_result.get('recommendations', []),
                'analysis': analysis_result.get('analysis', {})
            })
        else:
            return JsonResponse({
                'success': False,
                'error': analysis_result.get('error', 'Tahlil qilishda xatolik'),
                'ai_recommendation': analysis_result.get('ai_recommendation', 'Tahlil mavjud emas')
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Tahlil qilishda xatolik yuz berdi',
            'ai_recommendation': 'Kechirasiz, hozir tahlil qilish imkoni yo\'q. Keyinroq qayta urinib ko\'ring.'
        }, status=500)