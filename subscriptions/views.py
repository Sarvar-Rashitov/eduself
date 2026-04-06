from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from datetime import timedelta
import json

from accounts.models import User
from .models import (
    SubscriptionPlan, UserSubscription, PromoCode,
    ReferralProgram, UserReferral, ReferralProgress,
    Payment, Donation
)
from .payment_handlers import ClickPaymentHandler, PaymePaymentHandler


def api_subscription_plans(request):
    """API endpoint - Obuna modellarini olish"""
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('order', 'price')
    
    plans_data = []
    for plan in plans:
        plans_data.append({
            'id': plan.id,
            'name': plan.name,
            'slug': plan.slug,
            'description': plan.description,
            'price': str(plan.price),
            'duration_days': plan.duration_days,
            'unlimited_lives': plan.unlimited_lives,
            'ai_analysis_limit': plan.ai_analysis_limit,
            'ai_companion_limit': plan.ai_companion_limit,
            'university_exam_limit': plan.university_exam_limit,
            'mock_exam_limit': plan.mock_exam_limit,
            'certificate_test_limit': plan.certificate_test_limit,
            'icon': plan.icon,
            'color': plan.color,
            'badge_text': plan.badge_text,
            'is_popular': plan.is_popular,
        })
    
    return JsonResponse({'plans': plans_data})


def pro_page(request):
    """EduSelf Pro sahifasi"""
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('order', 'price')
    
    # Foydalanuvchining faol obunasi
    active_subscription = None
    if request.user.is_authenticated:
        active_subscription = UserSubscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        ).first()
    
    context = {
        'plans': plans,
        'active_subscription': active_subscription,
    }
    
    # Mobile yoki Desktop versiyani aniqlash
    from core.views import is_mobile
    if is_mobile(request):
        return render(request, 'subscriptions/pro_page.html', context)
    else:
        return render(request, 'subscriptions/pro_page_desktop.html', context)


@login_required
def subscribe(request, plan_slug):
    """Obuna sotib olish"""
    plan = get_object_or_404(SubscriptionPlan, slug=plan_slug, is_active=True)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        promo_code = request.POST.get('promo_code', '').strip()
        
        # Narxni hisoblash
        final_amount = plan.price
        discount_amount = 0
        promo = None
        
        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code, plan=plan, is_active=True)
                if promo.is_valid():
                    final_amount = promo.get_discounted_price()
                    discount_amount = plan.price - final_amount
                else:
                    messages.error(request, "Promokod amal qilmaydi")
            except PromoCode.DoesNotExist:
                messages.error(request, "Promokod topilmadi")
        
        # To'lov yaratish
        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            payment_method=payment_method,
            amount=plan.price,
            discount_amount=discount_amount,
            final_amount=final_amount,
            promo_code=promo,
            status='pending'
        )
        
        # To'lov tizimiga yo'naltirish
        if payment_method == 'click':
            # Click to'lov sahifasiga yo'naltirish
            click_url = (
                f"https://my.click.uz/services/pay?"
                f"service_id={settings.CLICK_SERVICE_ID}&"
                f"merchant_id={settings.CLICK_MERCHANT_ID}&"
                f"amount={float(payment.final_amount)}&"
                f"transaction_param={payment.id}&"
                f"return_url={request.build_absolute_uri('/subscriptions/my-subscriptions/')}"
            )
            
            # DEBUG rejimida xabar ko'rsatish (lekin baribir redirect qilish)
            if settings.DEBUG:
                messages.info(request, f"💡 Local test: Click to'lov production'da to'liq ishlaydi. Payment ID: {payment.id}")
            
            return redirect(click_url)
            
        elif payment_method == 'payme':
            # Payme to'lov sahifasiga yo'naltirish
            import base64
            account = base64.b64encode(f'{{"payment_id":"{payment.id}"}}'.encode()).decode()
            payme_url = (
                f"{settings.PAYME_ENDPOINT}?"
                f"m={settings.PAYME_MERCHANT_ID}&"
                f"ac={account}&"
                f"a={int(float(payment.final_amount) * 100)}&"
                f"c={request.build_absolute_uri('/subscriptions/my-subscriptions/')}"
            )
            
            # DEBUG rejimida xabar ko'rsatish
            if settings.DEBUG:
                messages.info(request, f"💡 Local test: Payme to'lov production'da to'liq ishlaydi. Payment ID: {payment.id}")
            
            return redirect(payme_url)
        
        messages.error(request, "To'lov usuli noto'g'ri")
        return redirect('subscriptions:pro_page')
    
    context = {
        'plan': plan,
    }
    return render(request, 'subscriptions/subscribe.html', context)


@require_POST
def check_promo_code(request):
    """Promokodni tekshirish (AJAX)"""
    code = request.POST.get('code', '').strip()
    plan_slug = request.POST.get('plan_slug')
    
    try:
        plan = SubscriptionPlan.objects.get(slug=plan_slug, is_active=True)
        promo = PromoCode.objects.get(code=code, plan=plan, is_active=True)
        
        if promo.is_valid():
            discounted_price = promo.get_discounted_price()
            discount_amount = plan.price - discounted_price
            
            return JsonResponse({
                'valid': True,
                'discount_amount': float(discount_amount),
                'final_price': float(discounted_price),
                'message': f"Promokod qo'llanildi! {discount_amount} so'm chegirma"
            })
        else:
            return JsonResponse({
                'valid': False,
                'message': 'Promokod amal qilmaydi'
            })
    except (SubscriptionPlan.DoesNotExist, PromoCode.DoesNotExist):
        return JsonResponse({
            'valid': False,
            'message': 'Promokod topilmadi'
        })


@login_required
def referral_page(request):
    """Referal sahifasi"""
    active_programs = ReferralProgram.objects.filter(is_active=True)
    
    # Foydalanuvchining referal jarayonlari
    user_progress = ReferralProgress.objects.filter(
        user=request.user,
        deadline__gt=timezone.now()
    ).select_related('program')
    
    # Foydalanuvchi taklif qilgan odamlar
    referrals = UserReferral.objects.filter(
        referrer=request.user
    ).select_related('referred', 'program').order_by('-created_at')
    
    # Referal linkini yaratish
    referral_link = request.build_absolute_uri(f'/accounts/register/?ref={request.user.id}')
    
    # Taklif qilingan do'stlar soni
    total_referrals = referrals.count()
    
    context = {
        'active_programs': active_programs,
        'user_progress': user_progress,
        'referrals': referrals,
        'referral_link': referral_link,
        'total_referrals': total_referrals,
    }
    return render(request, 'subscriptions/referral.html', context)


@login_required
@require_POST
def send_referral_invite(request):
    """Referal taklif yuborish"""
    program_id = request.POST.get('program_id')
    referred_user_id = request.POST.get('referred_user_id')
    
    try:
        program = ReferralProgram.objects.get(id=program_id, is_active=True)
        referred_user = get_object_or_404(User, id=referred_user_id)
        
        # Referal yaratish
        referral, created = UserReferral.objects.get_or_create(
            referrer=request.user,
            referred=referred_user,
            program=program
        )
        
        if created:
            # Jarayonni yangilash yoki yaratish
            progress, _ = ReferralProgress.objects.get_or_create(
                user=request.user,
                program=program,
                defaults={
                    'deadline': timezone.now() + timedelta(days=program.referral_deadline_days)
                }
            )
            progress.referral_count += 1
            progress.save()
            
            # Bajarilganligini tekshirish
            if progress.check_completion() and not progress.reward_given:
                # Mukofot berish
                subscription = UserSubscription.objects.create(
                    user=request.user,
                    plan=program.plan,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=program.reward_duration_days),
                    status='active',
                    acquired_via='referral'
                )
                progress.reward_given = True
                progress.save()
                
                messages.success(request, f"Tabriklaymiz! {program.plan.name} obunasi berildi!")
            else:
                messages.success(request, "Taklif yuborildi!")
        else:
            messages.info(request, "Bu foydalanuvchi allaqachon taklif qilingan")
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Click to'lov tizimi
@csrf_exempt
def click_prepare(request):
    """Click Prepare API - GET yoki POST"""
    try:
        # GET yoki POST parametrlardan ma'lumotlarni olish
        params = request.GET if request.method == 'GET' else request.POST
        data = {
            'click_trans_id': params.get('click_trans_id'),
            'service_id': params.get('service_id'),
            'merchant_trans_id': params.get('merchant_trans_id'),
            'amount': params.get('amount'),
            'action': params.get('action'),
            'sign_time': params.get('sign_time'),
            'sign_string': params.get('sign_string'),
        }
        
        result = ClickPaymentHandler.prepare(data)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'error': -8,
            'error_note': f'Error: {str(e)}'
        })


@csrf_exempt
def click_complete(request):
    """Click Complete API - GET yoki POST"""
    try:
        # GET yoki POST parametrlardan ma'lumotlarni olish
        params = request.GET if request.method == 'GET' else request.POST
        data = {
            'click_trans_id': params.get('click_trans_id'),
            'service_id': params.get('service_id'),
            'merchant_trans_id': params.get('merchant_trans_id'),
            'amount': params.get('amount'),
            'action': params.get('action'),
            'sign_time': params.get('sign_time'),
            'sign_string': params.get('sign_string'),
            'error': params.get('error'),
            'error_note': params.get('error_note'),
        }
        
        result = ClickPaymentHandler.complete(data)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({
            'error': -8,
            'error_note': f'Error: {str(e)}'
        })


# Payme to'lov tizimi
@csrf_exempt
def payme_callback(request):
    """Payme Callback API - JSON-RPC 2.0"""
    try:
        # Authorization tekshirish
        if not PaymePaymentHandler.check_auth(request):
            return JsonResponse({
                'error': {
                    'code': -32504,
                    'message': 'Insufficient privilege to perform this method'
                }
            })
        
        # JSON ma'lumotlarni olish
        request_data = json.loads(request.body.decode('utf-8'))
        
        # So'rovni qayta ishlash
        result = PaymePaymentHandler.handle_request(request_data)
        
        # JSON-RPC 2.0 response
        response = {
            'jsonrpc': '2.0',
            'id': request_data.get('id'),
        }
        response.update(result)
        
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({
            'jsonrpc': '2.0',
            'error': {
                'code': -32700,
                'message': f'Parse error: {str(e)}'
            },
            'id': None
        })


@login_required
def donate_page(request):
    """Donat sahifasi"""
    return render(request, 'subscriptions/donate.html')


@login_required
@require_POST
def process_donation(request):
    """Donat jarayoni"""
    amount = request.POST.get('amount')
    message = request.POST.get('message', '')
    payment_method = request.POST.get('payment_method')
    
    try:
        amount = float(amount)
        if amount < 1000:
            messages.error(request, "Minimal donat summasi 1000 so'm")
            return redirect('subscriptions:donate')
        
        # Donat yaratish
        donation = Donation.objects.create(
            user=request.user,
            amount=amount,
            message=message,
            payment_method=payment_method,
            status='pending'
        )
        
        # To'lov tizimiga yo'naltirish
        if payment_method == 'click':
            # Click to'lov sahifasiga yo'naltirish
            click_url = (
                f"https://my.click.uz/services/pay?"
                f"service_id={settings.CLICK_SERVICE_ID}&"
                f"merchant_id={settings.CLICK_MERCHANT_ID}&"
                f"amount={donation.amount}&"
                f"transaction_param=DONATE_{donation.id}&"
                f"return_url={request.build_absolute_uri('/subscriptions/donate/')}"
            )
            
            # DEBUG rejimida xabar ko'rsatish
            if settings.DEBUG:
                messages.info(request, f"💡 Local test: Click to'lov production'da to'liq ishlaydi. Donation ID: {donation.id}")
            
            return redirect(click_url)
            
        elif payment_method == 'payme':
            # Payme to'lov sahifasiga yo'naltirish
            import base64
            account = base64.b64encode(f'{{"donation_id":"{donation.id}"}}'.encode()).decode()
            payme_url = (
                f"{settings.PAYME_ENDPOINT}?"
                f"m={settings.PAYME_MERCHANT_ID}&"
                f"ac={account}&"
                f"a={int(donation.amount * 100)}&"
                f"c={request.build_absolute_uri('/subscriptions/donate/')}"
            )
            
            # DEBUG rejimida xabar ko'rsatish
            if settings.DEBUG:
                messages.info(request, f"💡 Local test: Payme to'lov production'da to'liq ishlaydi. Donation ID: {donation.id}")
            
            return redirect(payme_url)
        
        messages.success(request, "Rahmat! To'lov sahifasiga yo'naltirilmoqda...")
        return redirect('subscriptions:donate')
    except Exception as e:
        messages.error(request, f"Xatolik: {str(e)}")
        return redirect('subscriptions:donate')


@login_required
def my_subscriptions(request):
    """Foydalanuvchi obunalari"""
    subscriptions = UserSubscription.objects.filter(
        user=request.user
    ).select_related('plan').order_by('-created_at')
    
    context = {
        'subscriptions': subscriptions,
    }
    return render(request, 'subscriptions/my_subscriptions.html', context)
