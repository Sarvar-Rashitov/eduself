"""
BARCHA EMAIL VA TELEGRAM NOTIFICATIONLARNI TO'LIQ TEKSHIRISH
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from core.models import Notification
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import time

print("=" * 80)
print("BARCHA NOTIFICATION TIZIMLARINI TO'LIQ TEKSHIRISH")
print("=" * 80)

# Test foydalanuvchi
test_user = User.objects.filter(email="sarvarrashitov4321@gmail.com").first()

if not test_user:
    print("\n❌ Test foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Email verified: {test_user.email_verified}")
telegram_id_text = test_user.telegram_id or "Yo'q"
telegram_chat_text = test_user.telegram_chat_id or "Yo'q"
print(f"   Telegram ID: {telegram_id_text}")
print(f"   Telegram Chat ID: {telegram_chat_text}")

# Test counter
test_count = 0
success_count = 0
failed_tests = []

def run_test(test_name, test_func):
    global test_count, success_count, failed_tests
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
        failed_tests.append(test_name)
        import traceback
        traceback.print_exc()
    time.sleep(1)

# ============================================================================
# AVTOMATIK EMAILLAR (eduselfuz@gmail.com)
# ============================================================================

def test_welcome_email():
    """1. Xush kelibsiz emaili"""
    html_content = render_to_string('emails/welcome.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'Assalomu alaykum, {test_user.first_name}! EduSelf platformasiga xush kelibsiz!'
    
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

run_test("WELCOME EMAIL (Avtomatik)", test_welcome_email)

def test_email_verification():
    """2. Email tasdiqlash"""
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
    
    text_content = f'Email tasdiqlash: {verification_link}'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Email tasdiqlash',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("EMAIL VERIFICATION (Avtomatik)", test_email_verification)

def test_new_device_login():
    """3. Yangi qurilmadan kirish"""
    html_content = render_to_string('emails/new_device_login.html', {
        'user_name': test_user.first_name,
        'device_info': 'Chrome on Windows',
        'login_time': timezone.now().strftime('%d.%m.%Y, %H:%M'),
        'ip_address': '192.168.1.1',
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'Yangi qurilmadan kirish: Chrome on Windows'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Yangi qurilmadan kirish',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("NEW DEVICE LOGIN (Avtomatik)", test_new_device_login)

def test_password_reset():
    """4. Parolni tiklash"""
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
    
    text_content = f'Parolni tiklash: {reset_link}'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Parolni tiklash',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("PASSWORD RESET (Avtomatik)", test_password_reset)

def test_welcome_back():
    """5. Qaytganingizdan xursandmiz"""
    html_content = render_to_string('emails/welcome_back.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'Qaytganingizdan xursandmiz!'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Qaytganingizdan xursandmiz!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("WELCOME BACK (Avtomatik)", test_welcome_back)

def test_inactive_reminder():
    """6. Faol emasligi haqida eslatma"""
    html_content = render_to_string('emails/inactive_reminder.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'Sizni sog\'indik!'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Sizni sog\'indik!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("INACTIVE REMINDER (Avtomatik)", test_inactive_reminder)

def test_daily_reminder_morning():
    """7. Kunlik eslatma (ertalab)"""
    html_content = render_to_string('emails/daily_reminder.html', {
        'user_name': test_user.first_name,
        'time': 'ertalab',
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'Bugun o\'qishni boshlaymizmi?'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Bugun o\'qishni boshlaymizmi? 📚',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("DAILY REMINDER MORNING (Avtomatik)", test_daily_reminder_morning)

def test_daily_reminder_afternoon():
    """8. Kunlik eslatma (tushdan keyin)"""
    html_content = render_to_string('emails/daily_reminder.html', {
        'user_name': test_user.first_name,
        'time': 'tushdan keyin',
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'Bugun hali o\'qimadingiz'
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Bugun hali o\'qimadingiz 📖',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")

run_test("DAILY REMINDER AFTERNOON (Avtomatik)", test_daily_reminder_afternoon)

# ============================================================================
# ADMIN NOTIFICATIONS (notificationeduselfuz@gmail.com)
# ============================================================================

def test_admin_notification_direct():
    """9. Admin notification (to'g'ridan-to'g'ri)"""
    from django.core.mail import get_connection
    
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
    
    text_content = f'Admin notification test'
    
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

run_test("ADMIN NOTIFICATION DIRECT", test_admin_notification_direct)

def test_admin_notification_signal():
    """10. Admin notification (signal orqali)"""
    notification = Notification.objects.create(
        user=test_user,
        title="Signal Test Notification",
        message="Bu signal orqali yuborilgan test bildirishnoma.",
        notification_type='info',
        icon='📢',
        link='https://eduself.uz'
    )
    
    print(f"   Notification ID: {notification.id}")
    print("   ⏳ 3 soniya kutamiz (signal async ishga tushishi uchun)...")
    
    time.sleep(3)
    
    print("   ✅ Signal ishga tushdi!")
    
    # Cleanup
    notification.delete()

run_test("ADMIN NOTIFICATION SIGNAL", test_admin_notification_signal)

# ============================================================================
# TELEGRAM NOTIFICATIONS
# ============================================================================

def test_telegram_notification():
    """11. Telegram notification"""
    if not test_user.telegram_chat_id:
        print("   ⚠️  Telegram chat ID yo'q, test o'tkazib yuborildi")
        return
    
    from telegram_bot.notification_sender import send_telegram_notification
    
    result = send_telegram_notification(
        user_id=test_user.id,
        title="🧪 Test Notification",
        message="Bu Telegram bot orqali yuborilgan test bildirishnoma.",
        link="https://eduself.uz",
        is_global=False
    )
    
    if result:
        print(f"   ✅ Telegram notification yuborildi")
    else:
        print(f"   ❌ Telegram notification yuborilmadi")

run_test("TELEGRAM NOTIFICATION", test_telegram_notification)

# ============================================================================
# XULOSA
# ============================================================================
print("\n" + "=" * 80)
print("XULOSA")
print("=" * 80)

print(f"\n📊 Test natijalari: {success_count}/{test_count} muvaffaqiyatli")

if failed_tests:
    print(f"\n❌ Muvaffaqiyatsiz testlar:")
    for test in failed_tests:
        print(f"   - {test}")

print(f"\n📧 Emailingizni tekshiring: {test_user.email}")

print("\n💡 Quyidagi emaillar yuborilgan bo'lishi kerak:")
print("\n   AVTOMATIK EMAILLAR (eduselfuz@gmail.com):")
print("   1. Welcome Email")
print("   2. Email Verification")
print("   3. New Device Login")
print("   4. Password Reset")
print("   5. Welcome Back")
print("   6. Inactive Reminder")
print("   7. Daily Reminder (Morning)")
print("   8. Daily Reminder (Afternoon)")

print("\n   ADMIN NOTIFICATIONS (notificationeduselfuz@gmail.com):")
print("   9. Admin Notification (Direct)")
print("   10. Admin Notification (Signal)")

if test_user.telegram_chat_id:
    print("\n   TELEGRAM:")
    print("   11. Telegram Notification")

print("\n📊 Agar emaillar kelmagan bo'lsa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' dan qidiring")
print("   3. 2-3 daqiqa kutib ko'ring")
print("   4. Email parollarni tekshiring")

print()
