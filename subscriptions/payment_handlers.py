"""
Payment handlers for Click and Payme
"""
import hashlib
import base64
from django.conf import settings
from django.utils import timezone
from .models import Payment, UserSubscription
from datetime import timedelta


class ClickPaymentHandler:
    """Click to'lov tizimi handler"""
    
    @staticmethod
    def generate_signature(data):
        """Click signature yaratish"""
        secret_key = settings.CLICK_SECRET_KEY
        
        # Signature string yaratish
        signature_string = (
            f"{data.get('click_trans_id')}"
            f"{data.get('service_id')}"
            f"{secret_key}"
            f"{data.get('merchant_trans_id')}"
            f"{data.get('amount')}"
            f"{data.get('action')}"
            f"{data.get('sign_time')}"
        )
        
        # MD5 hash
        return hashlib.md5(signature_string.encode()).hexdigest()
    
    @staticmethod
    def verify_signature(data):
        """Signature tekshirish"""
        received_signature = data.get('sign_string', '')
        calculated_signature = ClickPaymentHandler.generate_signature(data)
        return received_signature == calculated_signature
    
    @staticmethod
    def prepare(data):
        """
        Click Prepare API
        Bu yerda to'lovni tayyorlash va tekshirish
        """
        # Signature tekshirish
        if not ClickPaymentHandler.verify_signature(data):
            return {
                'error': -1,
                'error_note': 'SIGN CHECK FAILED'
            }
        
        # Payment ID olish
        merchant_trans_id = data.get('merchant_trans_id')
        amount = float(data.get('amount', 0))
        
        try:
            # Donat yoki Payment ekanligini tekshirish
            if str(merchant_trans_id).startswith('DONATE_'):
                # Bu donat
                from .models import Donation
                donation_id = str(merchant_trans_id).replace('DONATE_', '')
                donation = Donation.objects.get(id=donation_id)
                
                # Allaqachon to'langan bo'lsa
                if donation.status == 'completed':
                    return {
                        'error': -4,
                        'error_note': 'Already paid'
                    }
                
                # Summa tekshirish
                if float(donation.amount) != amount:
                    return {
                        'error': -2,
                        'error_note': 'Incorrect parameter amount'
                    }
                
                # Muvaffaqiyatli
                donation.transaction_id = data.get('click_trans_id')
                donation.payment_data = data
                donation.save()
                
                return {
                    'error': 0,
                    'error_note': 'Success',
                    'click_trans_id': data.get('click_trans_id'),
                    'merchant_trans_id': merchant_trans_id,
                    'merchant_prepare_id': donation.id
                }
            else:
                # Bu payment (subscription)
                payment = Payment.objects.get(id=merchant_trans_id)
                
                # Allaqachon to'langan bo'lsa
                if payment.status == 'completed':
                    return {
                        'error': -4,
                        'error_note': 'Already paid'
                    }
                
                # Summa tekshirish
                if float(payment.final_amount) != amount:
                    return {
                        'error': -2,
                        'error_note': 'Incorrect parameter amount'
                    }
                
                # Muvaffaqiyatli
                payment.status = 'processing'
                payment.transaction_id = data.get('click_trans_id')
                payment.payment_data = data
                payment.save()
                
                return {
                    'error': 0,
                    'error_note': 'Success',
                    'click_trans_id': data.get('click_trans_id'),
                    'merchant_trans_id': merchant_trans_id,
                    'merchant_prepare_id': payment.id
                }
            
        except (Payment.DoesNotExist, Exception) as e:
            return {
                'error': -5,
                'error_note': f'Transaction not found: {str(e)}'
            }
    
    @staticmethod
    def complete(data):
        """
        Click Complete API
        To'lovni tasdiqlash va obuna/donat yaratish
        """
        # Signature tekshirish
        if not ClickPaymentHandler.verify_signature(data):
            return {
                'error': -1,
                'error_note': 'SIGN CHECK FAILED'
            }
        
        merchant_trans_id = data.get('merchant_trans_id')
        
        try:
            # Donat yoki Payment ekanligini tekshirish
            if str(merchant_trans_id).startswith('DONATE_'):
                # Bu donat
                from .models import Donation
                donation_id = str(merchant_trans_id).replace('DONATE_', '')
                donation = Donation.objects.get(id=donation_id)
                
                # Agar allaqachon bajarilgan bo'lsa
                if donation.status == 'completed':
                    return {
                        'error': 0,
                        'error_note': 'Success',
                        'click_trans_id': data.get('click_trans_id'),
                        'merchant_trans_id': merchant_trans_id,
                        'merchant_confirm_id': donation.id
                    }
                
                # Donatni tasdiqlash
                donation.status = 'completed'
                donation.completed_at = timezone.now()
                donation.transaction_id = data.get('click_trans_id')
                donation.payment_data = data
                donation.save()
                
                return {
                    'error': 0,
                    'error_note': 'Success',
                    'click_trans_id': data.get('click_trans_id'),
                    'merchant_trans_id': merchant_trans_id,
                    'merchant_confirm_id': donation.id
                }
            else:
                # Bu payment (subscription)
                payment = Payment.objects.get(id=merchant_trans_id)
                
                # Agar allaqachon bajarilgan bo'lsa
                if payment.status == 'completed':
                    return {
                        'error': 0,
                        'error_note': 'Success',
                        'click_trans_id': data.get('click_trans_id'),
                        'merchant_trans_id': merchant_trans_id,
                        'merchant_confirm_id': payment.id
                    }
                
                # To'lovni tasdiqlash
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.transaction_id = data.get('click_trans_id')
                payment.payment_data = data
                payment.save()
                
                # Obuna yaratish
                subscription = UserSubscription.objects.create(
                    user=payment.user,
                    plan=payment.plan,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=payment.plan.duration_days),
                    status='active',
                    acquired_via='payment'
                )
                
                payment.subscription = subscription
                payment.save()
                
                # Promokodni ishlatish
                if payment.promo_code:
                    payment.promo_code.use()
                
                return {
                    'error': 0,
                    'error_note': 'Success',
                    'click_trans_id': data.get('click_trans_id'),
                    'merchant_trans_id': merchant_trans_id,
                    'merchant_confirm_id': payment.id
                }
            
        except (Payment.DoesNotExist, Exception) as e:
            return {
                'error': -5,
                'error_note': f'Transaction not found: {str(e)}'
            }


class PaymePaymentHandler:
    """Payme to'lov tizimi handler"""
    
    @staticmethod
    def check_auth(request):
        """Payme authorization tekshirish"""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Basic '):
            return False
        
        try:
            # Base64 decode
            credentials = base64.b64decode(auth_header[6:]).decode('utf-8')
            username, password = credentials.split(':')
            
            # Merchant ID va secret key tekshirish
            expected_username = f"Paycom"
            expected_password = settings.PAYME_SECRET_KEY
            
            return username == expected_username and password == expected_password
        except:
            return False
    
    @staticmethod
    def handle_request(request_data):
        """Payme JSON-RPC so'rovlarini qayta ishlash"""
        method = request_data.get('method')
        params = request_data.get('params', {})
        
        if method == 'CheckPerformTransaction':
            return PaymePaymentHandler.check_perform_transaction(params)
        elif method == 'CreateTransaction':
            return PaymePaymentHandler.create_transaction(params)
        elif method == 'PerformTransaction':
            return PaymePaymentHandler.perform_transaction(params)
        elif method == 'CancelTransaction':
            return PaymePaymentHandler.cancel_transaction(params)
        elif method == 'CheckTransaction':
            return PaymePaymentHandler.check_transaction(params)
        else:
            return {
                'error': {
                    'code': -32601,
                    'message': 'Method not found'
                }
            }
    
    @staticmethod
    def check_perform_transaction(params):
        """To'lovni amalga oshirish mumkinligini tekshirish"""
        amount = params.get('amount')
        account = params.get('account', {})
        payment_id = account.get('payment_id')
        
        try:
            payment = Payment.objects.get(id=payment_id, status='pending')
            
            # Summa tekshirish (Payme tiyin'da ishlaydi - 100 tiyin = 1 so'm)
            expected_amount = int(payment.final_amount * 100)
            
            if amount != expected_amount:
                return {
                    'error': {
                        'code': -31001,
                        'message': 'Incorrect amount'
                    }
                }
            
            return {'result': {'allow': True}}
            
        except Payment.DoesNotExist:
            return {
                'error': {
                    'code': -31050,
                    'message': 'Payment not found'
                }
            }
    
    @staticmethod
    def create_transaction(params):
        """Tranzaksiya yaratish"""
        transaction_id = params.get('id')
        amount = params.get('amount')
        account = params.get('account', {})
        payment_id = account.get('payment_id')
        
        try:
            payment = Payment.objects.get(id=payment_id)
            
            # Agar allaqachon yaratilgan bo'lsa
            if payment.transaction_id == transaction_id:
                return {
                    'result': {
                        'create_time': int(payment.created_at.timestamp() * 1000),
                        'transaction': str(payment.id),
                        'state': 1 if payment.status == 'processing' else 2
                    }
                }
            
            # Yangi tranzaksiya
            payment.status = 'processing'
            payment.transaction_id = transaction_id
            payment.payment_data = params
            payment.save()
            
            return {
                'result': {
                    'create_time': int(timezone.now().timestamp() * 1000),
                    'transaction': str(payment.id),
                    'state': 1
                }
            }
            
        except Payment.DoesNotExist:
            return {
                'error': {
                    'code': -31050,
                    'message': 'Payment not found'
                }
            }
    
    @staticmethod
    def perform_transaction(params):
        """To'lovni amalga oshirish"""
        transaction_id = params.get('id')
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            
            # Agar allaqachon bajarilgan bo'lsa
            if payment.status == 'completed':
                return {
                    'result': {
                        'transaction': str(payment.id),
                        'perform_time': int(payment.completed_at.timestamp() * 1000),
                        'state': 2
                    }
                }
            
            # To'lovni tasdiqlash
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
            
            # Obuna yaratish
            subscription = UserSubscription.objects.create(
                user=payment.user,
                plan=payment.plan,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=payment.plan.duration_days),
                status='active',
                acquired_via='payment'
            )
            
            payment.subscription = subscription
            payment.save()
            
            # Promokodni ishlatish
            if payment.promo_code:
                payment.promo_code.use()
            
            return {
                'result': {
                    'transaction': str(payment.id),
                    'perform_time': int(payment.completed_at.timestamp() * 1000),
                    'state': 2
                }
            }
            
        except Payment.DoesNotExist:
            return {
                'error': {
                    'code': -31003,
                    'message': 'Transaction not found'
                }
            }
    
    @staticmethod
    def cancel_transaction(params):
        """Tranzaksiyani bekor qilish"""
        transaction_id = params.get('id')
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            
            # To'lovni bekor qilish
            payment.status = 'cancelled'
            payment.save()
            
            # Agar obuna yaratilgan bo'lsa, uni ham bekor qilish
            if payment.subscription:
                payment.subscription.status = 'cancelled'
                payment.subscription.save()
            
            return {
                'result': {
                    'transaction': str(payment.id),
                    'cancel_time': int(timezone.now().timestamp() * 1000),
                    'state': -1
                }
            }
            
        except Payment.DoesNotExist:
            return {
                'error': {
                    'code': -31003,
                    'message': 'Transaction not found'
                }
            }
    
    @staticmethod
    def check_transaction(params):
        """Tranzaksiya holatini tekshirish"""
        transaction_id = params.get('id')
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            
            state_map = {
                'pending': 0,
                'processing': 1,
                'completed': 2,
                'failed': -1,
                'cancelled': -2
            }
            
            return {
                'result': {
                    'create_time': int(payment.created_at.timestamp() * 1000),
                    'perform_time': int(payment.completed_at.timestamp() * 1000) if payment.completed_at else 0,
                    'cancel_time': 0,
                    'transaction': str(payment.id),
                    'state': state_map.get(payment.status, 0),
                    'reason': None
                }
            }
            
        except Payment.DoesNotExist:
            return {
                'error': {
                    'code': -31003,
                    'message': 'Transaction not found'
                }
            }
