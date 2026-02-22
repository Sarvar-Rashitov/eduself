"""
BARCHA EMAIL HOLATLARINI TEST QILISH
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import User
from core.models import Notification
import time

print("=" * 80)
print("BARCHA EMAIL HOLATLARINI TEST QILISH")
print("=" * 80)

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
print(f"   Email verified: {test_user.email_verified}")

# Test counter
test_count = 0
success_count = 0

def run_test(test_name, test_func):
    global test_count, success_count
    test_count += 1
    print("\n" + "=" * 80)
    print(f"TEST {test_count}: {test_name}")
    print("=" * 80)
    try:
        test_func()
        success_count += 1
        print(f"✅ Test muvaffaqiyatli!")
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        import traceback
        traceback.print_exc()
    time.sleep(2)

# ============================================================================
# TEST 1: Welcome Email (Avtomatik)
# ============================================================================
def test_welcome_email():
    html_content = render_to_string('emails/welcome.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

EduSelf platformasiga xush kelibsiz!

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Xush kelibsiz!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")

run_test("WELCOME EMAIL (Avtomatik - eduselfuz@gmail.com)", test_welcome_email)

# ============================================================================
# TEST 2: Email Verification (Avtomatik)
# ============================================================================
def test_verify_email():
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    
    token = default_token_generator.make_token(test_user)
    uid = urlsafe_base64_encode(force_bytes(test_user.pk))
    verification_link = f"{settings.SITE_URL}/accounts/verify-email/{uid}/{token}/"
    
    html_content = render_to_string('emails/verify_email.html', {
        'user_name': test_user.first_name,
        'verification_link': verification_link,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Email manzilingizni tasdiqlash uchun quyidagi havolaga bosing:
{verification_link}

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Email tasdiqlash',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")

run_test("EMAIL VERIFICATION (Avtomatik - eduselfuz@gmail.com)", test_verify_email)

# ============================================================================
# TEST 3: New Device Login (Avtomatik)
# ============================================================================
def test_new_device_login():
    html_content = render_to_string('emails/new_device_login.html', {
        'user_name': test_user.first_name,
        'device_info': 'Chrome on Windows',
        'login_time': 'Bugun, 14:30',
        'ip_address': '192.168.1.1',
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Hisobingizga yangi qurilmadan kirish amalga oshirildi.

Qurilma: Chrome on Windows
Vaqt: Bugun, 14:30
IP: 192.168.1.1

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Yangi qurilmadan kirish',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")

run_test("NEW DEVICE LOGIN (Avtomatik - eduselfuz@gmail.com)", test_new_device_login)

# ============================================================================
# TEST 4: Password Reset (Avtomatik)
# ============================================================================
def test_password_reset():
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    
    token = default_token_generator.make_token(test_user)
    uid = urlsafe_base64_encode(force_bytes(test_user.pk))
    reset_link = f"{settings.SITE_URL}/accounts/reset-password/{uid}/{token}/"
    
    html_content = render_to_string('emails/reset_password.html', {
        'user_name': test_user.first_name,
        'reset_link': reset_link,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Parolni tiklash uchun quyidagi havolaga bosing:
{reset_link}

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Parolni tiklash',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")

run_test("PASSWORD RESET (Avtomatik - eduselfuz@gmail.com)", test_password_reset)

# ============================================================================
# TEST 5: Inactive Reminder (Avtomatik)
# ============================================================================
def test_inactive_reminder():
    html_content = render_to_string('emails/inactive_reminder.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Sizni ko'rmay qoldik! EduSelf platformasiga qaytishingizni kutamiz.

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Sizni sog\'indik!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")

run_test("INACTIVE REMINDER (Avtomatik - eduselfuz@gmail.com)", test_inactive_reminder)

# ============================================================================
# TEST 6: Welcome Back (Avtomatik)
# ============================================================================
def test_welcome_back():
    html_content = render_to_string('emails/welcome_back.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Qaytganingizdan xursandmiz!

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Qaytganingizdan xursandmiz!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")

run_test("WELCOME BACK (Avtomatik - eduselfuz@gmail.com)", test_welcome_back)

# ============================================================================
# TEST 7: Admin Notification (Direct)
# ============================================================================
def test_admin_notification_direct():
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
        'title': 'Test Admin Notification',
        'message': 'Bu admin paneldan yuborilgan test bildirishnoma.',
        'link': 'https://eduself.uz',
        'notification_type': 'Muhim',
        'icon': '🔔',
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Muhim: Test Admin Notification

Bu admin paneldan yuborilgan test bildirishnoma.

Havola: https://eduself.uz

Hurmat bilan,
EduSelf jamoasi'''
    
    from_email = os.getenv('ADMIN_DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Test Admin Notification',
        body=text_content,
        from_email=from_email,
        to=[test_user.email],
        connection=admin_connection
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {from_email}")
    print(f"   To: {test_user.email}")

run_test("ADMIN NOTIFICATION DIRECT (notificationeduselfuz@gmail.com)", test_admin_notification_direct)

# ============================================================================
# TEST 8: Admin Notification via Signal
# ============================================================================
def test_admin_notification_signal():
    notification = Notification.objects.create(
        user=test_user,
        title="Signal Test Notification",
        message="Bu signal orqali yuborilgan admin notification test xabari.",
        notification_type='info',
        icon='📢',
        link='https://eduself.uz'
    )
    
    print(f"   Notification ID: {notification.id}")
    print("   ⏳ 5 soniya kutamiz (signal async ishga tushishi uchun)...")
    
    time.sleep(5)
    
    print("   ✅ Signal ishga tushdi!")
    
    # Cleanup
    notification.delete()

run_test("ADMIN NOTIFICATION VIA SIGNAL (notificationeduselfuz@gmail.com)", test_admin_notification_signal)

# ============================================================================
# TEST 9: Global Admin Notification
# ============================================================================
def test_global_notification():
    notification = Notification.objects.create(
        title="Global Test Notification",
        message="Bu barcha foydalanuvchilarga yuborilgan global test bildirishnoma.",
        notification_type='announcement',
        icon='📣',
        link='https://eduself.uz',
        is_global=True
    )
    
    print(f"   Notification ID: {notification.id}")
    print("   ⏳ 5 soniya kutamiz (signal async ishga tushishi uchun)...")
    
    time.sleep(5)
    
    print("   ✅ Signal ishga tushdi!")
    
    # Cleanup
    notification.delete()

run_test("GLOBAL ADMIN NOTIFICATION (notificationeduselfuz@gmail.com)", test_global_notification)

# ============================================================================
# XULOSA
# ============================================================================
print("\n" + "=" * 80)
print("XULOSA")
print("=" * 80)

print(f"\n📊 Test natijalari: {success_count}/{test_count} muvaffaqiyatli")

print(f"\n📧 Emailingizni tekshiring: {test_user.email}")

print("\n💡 Quyidagi emaillar yuborilgan bo'lishi kerak:")
print("\n   AVTOMATIK EMAILLAR (eduselfuz@gmail.com):")
print("   1. Welcome Email")
print("   2. Email Verification")
print("   3. New Device Login")
print("   4. Password Reset")
print("   5. Inactive Reminder")
print("   6. Welcome Back")

print("\n   ADMIN NOTIFICATIONS (notificationeduselfuz@gmail.com):")
print("   7. Admin Notification (Direct)")
print("   8. Admin Notification (Signal)")
print("   9. Global Admin Notification")

print("\n📊 Agar emaillar kelmagan bo'lsa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' dan qidiring")
print("   3. Email parollarni tekshiring")
print("   4. Gmail'da 'Less secure app access' yoqilganligini tekshiring")

print()
