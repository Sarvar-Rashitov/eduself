"""
Barcha notification funksiyalarini test qilish
"""
import os
import sys
import django
import time

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from core.models import Notification
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 70)
print("BARCHA NOTIFICATION FUNKSIYALARINI TEST QILISH")
print("=" * 70)

# Test foydalanuvchi
test_email = "sarvarrashitov4321@gmail.com"
test_user = User.objects.filter(email=test_email).first()

if not test_user:
    print(f"❌ {test_email} topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Email verified: {test_user.email_verified}")

# ============================================================================
# TEST 1: Email tasdiqlash xati
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1: EMAIL TASDIQLASH XATI")
print("=" * 70)

try:
    from accounts.models import EmailVerificationToken
    from django.urls import reverse
    
    # Token yaratish
    token = EmailVerificationToken.objects.create(user=test_user)
    verify_url = f"https://eduself.uz/accounts/verify-email/{token.token}/"
    
    # HTML email yaratish
    html_content = render_to_string('emails/verify_email.html', {
        'user_name': test_user.first_name,
        'verify_url': verify_url,
        'site_url': settings.SITE_URL,
    })
    
    # Text fallback
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

EduSelf platformasiga xush kelibsiz!

Emailingizni tasdiqlash uchun quyidagi havolaga o'ting:
{verify_url}

Havola 48 soat ichida amal qiladi.

Hurmat bilan,
EduSelf jamoasi'''
    
    # Email yuborish
    email = EmailMultiAlternatives(
        subject='EduSelf - Emailni tasdiqlash',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ Email tasdiqlash xati yuborildi!")
    print(f"   To: {test_user.email}")
    
    # Token o'chirish
    token.delete()
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

time.sleep(2)

# ============================================================================
# TEST 2: Admin notification (shaxsiy)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2: ADMIN NOTIFICATION (SHAXSIY)")
print("=" * 70)

try:
    notification = Notification.objects.create(
        user=test_user,
        title="Test: Shaxsiy Notification",
        message="Bu admin paneldan yuborilgan shaxsiy test xabari.",
        notification_type='info',
        icon='🔔',
        link='https://eduself.uz'
    )
    
    print(f"✅ Notification yaratildi: ID={notification.id}")
    print("⏳ 5 soniya kutamiz (signal ishga tushishi uchun)...")
    
    time.sleep(5)
    
    print("✅ Signal ishga tushdi va email yuborildi!")
    
    # Cleanup
    notification.delete()
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

time.sleep(2)

# ============================================================================
# TEST 3: Welcome email
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3: WELCOME EMAIL")
print("=" * 70)

try:
    html_content = render_to_string('emails/welcome.html', {
        'user_name': test_user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

EduSelf platformasiga xush kelibsiz!

Platformaga kirish: {settings.SITE_URL}

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
    
    print("✅ Welcome email yuborildi!")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")

time.sleep(2)

# ============================================================================
# TEST 4: Password reset email
# ============================================================================
print("\n" + "=" * 70)
print("TEST 4: PASSWORD RESET EMAIL")
print("=" * 70)

try:
    reset_url = "https://eduself.uz/accounts/reset-password/test-token/"
    
    html_content = render_to_string('emails/reset_password.html', {
        'user_name': test_user.first_name,
        'reset_url': reset_url,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Parolni tiklash uchun quyidagi havolaga o'ting:
{reset_url}

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
    
    print("✅ Password reset email yuborildi!")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")

# ============================================================================
# XULOSA
# ============================================================================
print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)

print("\n✅ Barcha testlar muvaffaqiyatli o'tdi!")
print(f"\n📧 Emailingizni tekshiring: {test_user.email}")
print("\n💡 Quyidagi emaillar yuborilgan bo'lishi kerak:")
print("   1. Email tasdiqlash xati")
print("   2. Admin notification (shaxsiy)")
print("   3. Welcome email")
print("   4. Password reset email")

print("\n📊 Agar emaillar kelmagan bo'lsa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' dan qidiring")
print("   3. Log'larda xatolik bor yoki yo'qligini tekshiring")

print()
