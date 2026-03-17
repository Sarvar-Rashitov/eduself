"""
Click to'lov URL'ini test qilish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.conf import settings
from subscriptions.models import SubscriptionPlan, Payment
from accounts.models import User


def test_click_url():
    """Click to'lov URL'ini yaratish va ko'rsatish"""
    
    print("=" * 70)
    print("CLICK TO'LOV URL TEST")
    print("=" * 70)
    
    # Test ma'lumotlari
    user = User.objects.filter(email='click_test@test.com').first()
    plan = SubscriptionPlan.objects.filter(slug='test-plan').first()
    
    if not user or not plan:
        print("\n❌ Test ma'lumotlari topilmadi!")
        print("   Avval test_click_payment.py ni ishga tushiring.")
        return
    
    # To'lov yaratish
    payment = Payment.objects.create(
        user=user,
        plan=plan,
        payment_method='click',
        amount=plan.price,
        final_amount=plan.price,
        status='pending'
    )
    
    print(f"\n✅ To'lov yaratildi:")
    print(f"   Payment ID: {payment.id}")
    print(f"   Summa: {payment.final_amount} so'm")
    print(f"   Foydalanuvchi: {user.get_display_name()}")
    print(f"   Ta'rif: {plan.name}")
    
    # Click URL yaratish
    click_url = (
        f"https://my.click.uz/services/pay?"
        f"service_id={settings.CLICK_SERVICE_ID}&"
        f"merchant_id={settings.CLICK_MERCHANT_ID}&"
        f"amount={payment.final_amount}&"
        f"transaction_param={payment.id}&"
        f"return_url=https://eduself.uz/subscriptions/my-subscriptions/"
    )
    
    print(f"\n🔗 Click To'lov URL:")
    print(f"\n{click_url}")
    
    print(f"\n📋 URL Parametrlari:")
    print(f"   service_id: {settings.CLICK_SERVICE_ID}")
    print(f"   merchant_id: {settings.CLICK_MERCHANT_ID}")
    print(f"   amount: {payment.final_amount}")
    print(f"   transaction_param: {payment.id}")
    print(f"   return_url: https://eduself.uz/subscriptions/my-subscriptions/")
    
    print(f"\n💡 Test Qilish:")
    print(f"   1. Yuqoridagi URL'ni brauzerda oching")
    print(f"   2. Test kartadan foydalaning:")
    print(f"      Karta: 8600 0000 0000 0000")
    print(f"      Muddat: 03/99")
    print(f"      CVV: 123")
    print(f"      SMS: 666666")
    print(f"   3. To'lovni amalga oshiring")
    print(f"   4. Callback URL'lar avtomatik chaqiriladi:")
    print(f"      Prepare: https://eduself.uz/subscriptions/payment/click/prepare/")
    print(f"      Complete: https://eduself.uz/subscriptions/payment/click/complete/")
    
    print(f"\n⚠️  Eslatma:")
    print(f"   - Production muhitda test qilish uchun HTTPS kerak")
    print(f"   - Local test uchun ngrok ishlatishingiz mumkin")
    print(f"   - Click merchant panelda callback URL'lar sozlangan bo'lishi kerak")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    test_click_url()
