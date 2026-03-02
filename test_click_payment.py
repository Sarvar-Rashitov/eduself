"""
Click to'lov tizimini test qilish skripti
"""
import os
import django
import hashlib
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.conf import settings
from accounts.models import User
from subscriptions.models import SubscriptionPlan, Payment, UserSubscription
from subscriptions.payment_handlers import ClickPaymentHandler


def generate_click_signature(click_trans_id, service_id, secret_key, merchant_trans_id, amount, action, sign_time):
    """Click signature yaratish"""
    signature_string = f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}{amount}{action}{sign_time}"
    return hashlib.md5(signature_string.encode()).hexdigest()


def test_click_payment():
    """Click to'lov tizimini test qilish"""
    
    print("=" * 70)
    print("CLICK TO'LOV TIZIMINI TEST QILISH")
    print("=" * 70)
    
    # 1. Sozlamalarni tekshirish
    print("\n1. Sozlamalarni tekshirish...")
    print(f"   CLICK_MERCHANT_ID: {settings.CLICK_MERCHANT_ID}")
    print(f"   CLICK_SERVICE_ID: {settings.CLICK_SERVICE_ID}")
    print(f"   CLICK_SECRET_KEY: {settings.CLICK_SECRET_KEY[:10]}...")
    
    if settings.CLICK_SECRET_KEY == 'your_click_secret_key':
        print("   ⚠️  OGOHLANTIRISH: Click kalitlari hali sozlanmagan!")
        print("   ℹ️  Test uchun demo kalitlardan foydalanamiz")
    
    # 2. Test foydalanuvchi va ta'rifni yaratish
    print("\n2. Test ma'lumotlarini tayyorlash...")
    
    # Foydalanuvchi
    user, created = User.objects.get_or_create(
        email='click_test@test.com',
        defaults={
            'first_name': 'Click',
            'last_name': 'Test',
            'email_verified': True,
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f"   ✅ Test foydalanuvchi yaratildi: {user.get_display_name()}")
    else:
        print(f"   ✅ Test foydalanuvchi topildi: {user.get_display_name()}")
    
    # Ta'rif
    plan, created = SubscriptionPlan.objects.get_or_create(
        slug='test-plan',
        defaults={
            'name': 'Test Plan',
            'description': 'Test uchun ta\'rif',
            'price': 50000,
            'duration_days': 30,
            'unlimited_lives': True,
            'ai_analysis_limit': -1,
            'is_active': True,
        }
    )
    if created:
        print(f"   ✅ Test ta'rif yaratildi: {plan.name} - {plan.price} so'm")
    else:
        print(f"   ✅ Test ta'rif topildi: {plan.name} - {plan.price} so'm")
    
    # 3. To'lov yaratish
    print("\n3. To'lov yaratish...")
    
    payment = Payment.objects.create(
        user=user,
        plan=plan,
        payment_method='click',
        amount=plan.price,
        discount_amount=0,
        final_amount=plan.price,
        status='pending'
    )
    print(f"   ✅ To'lov yaratildi:")
    print(f"      ID: {payment.id}")
    print(f"      Summa: {payment.final_amount} so'm")
    print(f"      Holat: {payment.status}")
    
    # 4. Click Prepare so'rovini simulyatsiya qilish
    print("\n4. Click Prepare so'rovini test qilish...")
    
    click_trans_id = str(int(time.time() * 1000))  # Unique transaction ID
    service_id = settings.CLICK_SERVICE_ID
    secret_key = settings.CLICK_SECRET_KEY
    merchant_trans_id = str(payment.id)
    amount = str(float(payment.final_amount))
    action = "0"  # 0 = prepare
    sign_time = str(int(time.time()))
    
    # Signature yaratish
    sign_string = generate_click_signature(
        click_trans_id, service_id, secret_key, 
        merchant_trans_id, amount, action, sign_time
    )
    
    prepare_data = {
        'click_trans_id': click_trans_id,
        'service_id': service_id,
        'merchant_trans_id': merchant_trans_id,
        'amount': amount,
        'action': action,
        'sign_time': sign_time,
        'sign_string': sign_string,
    }
    
    print(f"   So'rov ma'lumotlari:")
    print(f"      click_trans_id: {click_trans_id}")
    print(f"      merchant_trans_id: {merchant_trans_id}")
    print(f"      amount: {amount}")
    print(f"      sign_string: {sign_string[:20]}...")
    
    # Prepare handler'ni chaqirish
    prepare_result = ClickPaymentHandler.prepare(prepare_data)
    
    print(f"\n   Prepare natijasi:")
    print(f"      error: {prepare_result.get('error')}")
    print(f"      error_note: {prepare_result.get('error_note')}")
    
    if prepare_result.get('error') == 0:
        print(f"   ✅ Prepare muvaffaqiyatli!")
        
        # To'lov holatini tekshirish
        payment.refresh_from_db()
        print(f"      To'lov holati: {payment.status}")
        print(f"      Transaction ID: {payment.transaction_id}")
    else:
        print(f"   ❌ Prepare xatolik!")
        return
    
    # 5. Click Complete so'rovini simulyatsiya qilish
    print("\n5. Click Complete so'rovini test qilish...")
    
    action = "1"  # 1 = complete
    sign_time = str(int(time.time()))
    
    # Yangi signature yaratish
    sign_string = generate_click_signature(
        click_trans_id, service_id, secret_key, 
        merchant_trans_id, amount, action, sign_time
    )
    
    complete_data = {
        'click_trans_id': click_trans_id,
        'service_id': service_id,
        'merchant_trans_id': merchant_trans_id,
        'amount': amount,
        'action': action,
        'sign_time': sign_time,
        'sign_string': sign_string,
        'error': '0',
        'error_note': 'Success',
    }
    
    print(f"   So'rov ma'lumotlari:")
    print(f"      click_trans_id: {click_trans_id}")
    print(f"      merchant_trans_id: {merchant_trans_id}")
    print(f"      action: {action}")
    
    # Complete handler'ni chaqirish
    complete_result = ClickPaymentHandler.complete(complete_data)
    
    print(f"\n   Complete natijasi:")
    print(f"      error: {complete_result.get('error')}")
    print(f"      error_note: {complete_result.get('error_note')}")
    
    if complete_result.get('error') == 0:
        print(f"   ✅ Complete muvaffaqiyatli!")
        
        # To'lov holatini tekshirish
        payment.refresh_from_db()
        print(f"      To'lov holati: {payment.status}")
        print(f"      Bajarilgan vaqt: {payment.completed_at}")
        
        # Obuna yaratilganligini tekshirish
        if payment.subscription:
            subscription = payment.subscription
            print(f"\n   ✅ Obuna yaratildi:")
            print(f"      Ta'rif: {subscription.plan.name}")
            print(f"      Boshlanish: {subscription.start_date.strftime('%d.%m.%Y')}")
            print(f"      Tugash: {subscription.end_date.strftime('%d.%m.%Y')}")
            print(f"      Holat: {subscription.status}")
        else:
            print(f"   ❌ Obuna yaratilmadi!")
    else:
        print(f"   ❌ Complete xatolik!")
        return
    
    # 6. Natijalarni ko'rsatish
    print("\n" + "=" * 70)
    print("TEST NATIJALARI")
    print("=" * 70)
    
    print(f"\n✅ To'lov:")
    print(f"   ID: {payment.id}")
    print(f"   Foydalanuvchi: {payment.user.get_display_name()}")
    print(f"   Ta'rif: {payment.plan.name}")
    print(f"   Summa: {payment.final_amount} so'm")
    print(f"   Holat: {payment.status}")
    print(f"   Transaction ID: {payment.transaction_id}")
    
    if payment.subscription:
        print(f"\n✅ Obuna:")
        print(f"   ID: {payment.subscription.id}")
        print(f"   Ta'rif: {payment.subscription.plan.name}")
        print(f"   Muddat: {payment.subscription.start_date.strftime('%d.%m.%Y')} - {payment.subscription.end_date.strftime('%d.%m.%Y')}")
        print(f"   Holat: {payment.subscription.status}")
        active_text = "✅ Ha" if payment.subscription.is_active() else "❌ Yo'q"
        print(f"   Faol: {active_text}")
    
    # 7. Foydalanuvchi obunasini tekshirish
    print(f"\n✅ Foydalanuvchi obunalari:")
    user_subscriptions = UserSubscription.objects.filter(user=user)
    print(f"   Jami: {user_subscriptions.count()} ta")
    
    for sub in user_subscriptions:
        print(f"   - {sub.plan.name}: {sub.start_date.strftime('%d.%m.%Y')} - {sub.end_date.strftime('%d.%m.%Y')} ({sub.status})")
    
    # 8. Pro user tekshirish
    print(f"\n✅ Pro user holati:")
    print(f"   is_pro_user(): {user.is_pro_user()}")
    
    active_sub = user.get_active_subscription()
    if active_sub:
        print(f"   Faol obuna: {active_sub.plan.name}")
        print(f"   Cheksiz yurakchalar: {active_sub.plan.unlimited_lives}")
    else:
        print(f"   Faol obuna yo'q")
    
    print("\n" + "=" * 70)
    print("✅ TEST MUVAFFAQIYATLI YAKUNLANDI!")
    print("=" * 70)
    
    # 9. Callback URL'larni ko'rsatish
    print(f"\n📌 Click Merchant panelida sozlash kerak bo'lgan URL'lar:")
    print(f"   Prepare URL: https://eduself.uz/subscriptions/payment/click/prepare/")
    print(f"   Complete URL: https://eduself.uz/subscriptions/payment/click/complete/")
    
    print(f"\n📌 To'lov URL formati:")
    print(f"   https://my.click.uz/services/pay?service_id={service_id}&merchant_id={settings.CLICK_MERCHANT_ID}&amount={amount}&transaction_param={payment.id}")
    
    print(f"\n📌 Test uchun cURL so'rovi:")
    print(f'''
curl -X POST "https://eduself.uz/subscriptions/payment/click/prepare/" \\
  -d "click_trans_id={click_trans_id}" \\
  -d "service_id={service_id}" \\
  -d "merchant_trans_id={payment.id}" \\
  -d "amount={amount}" \\
  -d "action=0" \\
  -d "sign_time={sign_time}" \\
  -d "sign_string={sign_string}"
''')


def test_signature_generation():
    """Signature yaratish va tekshirish testlari"""
    print("\n" + "=" * 70)
    print("SIGNATURE YARATISH TESTLARI")
    print("=" * 70)
    
    # Test ma'lumotlari
    test_data = {
        'click_trans_id': '123456789',
        'service_id': '12345',
        'merchant_trans_id': '1',
        'amount': '50000',
        'action': '0',
        'sign_time': '1234567890',
    }
    
    secret_key = 'test_secret_key'
    
    # Signature yaratish
    signature_string = (
        f"{test_data['click_trans_id']}"
        f"{test_data['service_id']}"
        f"{secret_key}"
        f"{test_data['merchant_trans_id']}"
        f"{test_data['amount']}"
        f"{test_data['action']}"
        f"{test_data['sign_time']}"
    )
    
    signature = hashlib.md5(signature_string.encode()).hexdigest()
    
    print(f"\n1. Signature yaratish:")
    print(f"   Signature string: {signature_string}")
    print(f"   MD5 hash: {signature}")
    
    # Signature tekshirish
    test_data['sign_string'] = signature
    
    # Settings'ni vaqtincha o'zgartirish
    original_secret = settings.CLICK_SECRET_KEY
    settings.CLICK_SECRET_KEY = secret_key
    
    is_valid = ClickPaymentHandler.verify_signature(test_data)
    
    valid_text = "✅ To'g'ri" if is_valid else "❌ Noto'g'ri"
    print(f"\n2. Signature tekshirish:")
    print(f"   Natija: {valid_text}")
    
    # Noto'g'ri signature
    test_data['sign_string'] = 'wrong_signature'
    is_valid = ClickPaymentHandler.verify_signature(test_data)
    
    invalid_text = "❌ To'g'ri (xato!)" if is_valid else "✅ Noto'g'ri (to'g'ri!)"
    print(f"\n3. Noto'g'ri signature tekshirish:")
    print(f"   Natija: {invalid_text}")
    
    # Settings'ni qaytarish
    settings.CLICK_SECRET_KEY = original_secret
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    # Signature testlari
    test_signature_generation()
    
    # To'lov testlari
    test_click_payment()
