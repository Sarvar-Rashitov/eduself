#!/usr/bin/env python
"""Barcha email template'larni test qilish"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_test_email(template_name, subject, context, recipient):
    """Test email yuborish"""
    try:
        html_content = render_to_string(template_name, context)
        text_content = f"Test email: {subject}"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        return True
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

print("=" * 70)
print("EMAIL TEMPLATE'LAR TEST")
print("=" * 70)
print(f"Qabul qiluvchi: {settings.EMAIL_HOST_USER}")
print("=" * 70)

# 1. Email Tasdiqlash
print("\n1️⃣  Email Tasdiqlash template'i...")
if send_test_email(
    template_name='emails/verify_email.html',
    subject='EduSelf - Email Tasdiqlash (Test)',
    context={
        'user_name': 'Test User',
        'verify_url': 'https://eduself.uz/accounts/verify/test-token-123456',
    },
    recipient=settings.EMAIL_HOST_USER
):
    print("   ✅ Yuborildi!")
else:
    print("   ❌ Yuborilmadi!")

# 2. Parolni Tiklash
print("\n2️⃣  Parolni Tiklash template'i...")
if send_test_email(
    template_name='emails/reset_password.html',
    subject='EduSelf - Parolni Tiklash (Test)',
    context={
        'user_name': 'Test User',
        'reset_url': 'https://eduself.uz/accounts/reset/test-token-789012',
    },
    recipient=settings.EMAIL_HOST_USER
):
    print("   ✅ Yuborildi!")
else:
    print("   ❌ Yuborilmadi!")

# 3. Xush kelibsiz
print("\n3️⃣  Xush kelibsiz template'i...")
if send_test_email(
    template_name='emails/welcome.html',
    subject='EduSelf - Xush kelibsiz! (Test)',
    context={
        'user_name': 'Test User',
        'site_url': 'https://eduself.uz',
    },
    recipient=settings.EMAIL_HOST_USER
):
    print("   ✅ Yuborildi!")
else:
    print("   ❌ Yuborilmadi!")

print("\n" + "=" * 70)
print("✅ TEST YAKUNLANDI!")
print("=" * 70)
print("\n📧 Inbox'ingizni tekshiring:")
print(f"   {settings.EMAIL_HOST_USER}")
print("\n💡 Nima ko'rishingiz kerak:")
print("   • 3 ta email (tasdiqlash, parolni tiklash, xush kelibsiz)")
print("   • Har birida logo, tugma va chiroyli dizayn")
print("   • Mobil va desktop'da yaxshi ko'rinishi kerak")
print("\n🎨 Agar email'lar chiroyli ko'rinmasa:")
print("   • Gmail'da 'Show original' ni bosing")
print("   • HTML versiyasini ko'ring")
print("   • Boshqa email client'da sinab ko'ring")
