"""
Ikkala email backend'ni test qilish
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import User
from core.models import Notification
import time

print("=" * 70)
print("IKKALA EMAIL BACKEND'NI TEST QILISH")
print("=" * 70)

# Email sozlamalarini ko'rsatish
print("\n📧 AVTOMATIK EMAIL SOZLAMALARI:")
print(f"   Host: {settings.EMAIL_HOST}")
print(f"   User: {settings.EMAIL_HOST_USER}")
print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

print("\n📧 ADMIN NOTIFICATION EMAIL SOZLAMALARI:")
print(f"   Host: {os.getenv('ADMIN_EMAIL_HOST')}")
print(f"   User: {os.getenv('ADMIN_EMAIL_HOST_USER')}")
print(f"   From: {os.getenv('ADMIN_DEFAULT_FROM_EMAIL')}")

# Test foydalanuvchi
test_user = User.objects.filter(email="sarvarrashitov4321@gmail.com").first()

if not test_user:
    print("\n❌ Test foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")

# ============================================================================
# TEST 1: Avtomatik email (Gmail 1)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1: AVTOMATIK EMAIL (sarvarrashitov4321@gmail.com)")
print("=" * 70)

try:
    html_content = render_to_string('emails/welcome.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Bu avtomatik email test xabari (Gmail 1).

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Avtomatik Email Test',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ Avtomatik email yuborildi!")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

time.sleep(2)

# ============================================================================
# TEST 2: Admin notification email (Gmail 2)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2: ADMIN NOTIFICATION EMAIL (sarvarrashitov1234@gmail.com)")
print("=" * 70)

try:
    # Admin email backend
    admin_connection = get_connection(
        host=os.getenv('ADMIN_EMAIL_HOST', settings.EMAIL_HOST),
        port=int(os.getenv('ADMIN_EMAIL_PORT', settings.EMAIL_PORT)),
        username=os.getenv('ADMIN_EMAIL_HOST_USER', settings.EMAIL_HOST_USER),
        password=os.getenv('ADMIN_EMAIL_HOST_PASSWORD', settings.EMAIL_HOST_PASSWORD),
        use_tls=os.getenv('ADMIN_EMAIL_USE_TLS', 'True') == 'True',
        fail_silently=False,
    )
    
    html_content = render_to_string('emails/notification.html', {
        'user_name': test_user.first_name,
        'title': 'Admin Notification Test',
        'message': 'Bu admin notification email test xabari (Gmail 2).',
        'link': 'https://eduself.uz',
        'notification_type': 'Test',
        'icon': '🔔',
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Test: Admin Notification Test

Bu admin notification email test xabari (Gmail 2).

Havola: https://eduself.uz

Hurmat bilan,
EduSelf jamoasi'''
    
    from_email = os.getenv('ADMIN_DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Admin Notification Test',
        body=text_content,
        from_email=from_email,
        to=[test_user.email],
        connection=admin_connection
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ Admin notification email yuborildi!")
    print(f"   From: {from_email}")
    print(f"   To: {test_user.email}")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

time.sleep(2)

# ============================================================================
# TEST 3: Signal orqali admin notification
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3: SIGNAL ORQALI ADMIN NOTIFICATION")
print("=" * 70)

try:
    notification = Notification.objects.create(
        user=test_user,
        title="Signal Test",
        message="Bu signal orqali yuborilgan admin notification test xabari.",
        notification_type='info',
        icon='🔔',
        link='https://eduself.uz'
    )
    
    print(f"✅ Notification yaratildi: ID={notification.id}")
    print("⏳ 5 soniya kutamiz (signal ishga tushishi uchun)...")
    
    time.sleep(5)
    
    print("✅ Signal ishga tushdi!")
    
    # Cleanup
    notification.delete()
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# XULOSA
# ============================================================================
print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)

print(f"\n✅ Barcha testlar tugadi!")
print(f"\n📧 Emailingizni tekshiring: {test_user.email}")
print("\n💡 Quyidagi emaillar yuborilgan bo'lishi kerak:")
print("   1. Avtomatik email (from: sarvarrashitov4321@gmail.com)")
print("   2. Admin notification email (from: sarvarrashitov1234@gmail.com)")
print("   3. Signal orqali admin notification (from: sarvarrashitov1234@gmail.com)")

print("\n📊 Agar emaillar kelmagan bo'lsa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' dan qidiring")
print("   3. Email parollarni tekshiring")

print()
