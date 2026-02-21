"""
Sizga to'g'ridan-to'g'ri email yuborish testi
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

print("=" * 70)
print("TO'G'RIDAN-TO'G'RI EMAIL YUBORISH TESTI")
print("=" * 70)

# Sizning foydalanuvchingiz
user = User.objects.filter(email="sarvarrashitov4321@gmail.com").first()

if not user:
    print("❌ Foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Foydalanuvchi: {user.first_name}")
print(f"   Email: {user.email}")
print(f"   Email verified: {user.email_verified}")

print("\n" + "=" * 70)
print("EMAIL YUBORISH")
print("=" * 70)

try:
    # HTML email yaratish
    html_content = render_to_string('emails/notification.html', {
        'user_name': user.first_name,
        'title': "Test Email",
        'message': "Bu to'g'ridan-to'g'ri yuborilgan test email. Agar bu email kelsa, demak email yuborish ishlayapti!",
        'link': "https://eduself.uz",
        'notification_type': "Test",
        'icon': '✉️',
        'site_url': settings.SITE_URL,
    })
    
    # Text fallback
    text_content = f'''Assalomu alaykum, {user.first_name}!

Test: Test Email

Bu to'g'ridan-to'g'ri yuborilgan test email. Agar bu email kelsa, demak email yuborish ishlayapti!

Havola: https://eduself.uz

Hurmat bilan,
EduSelf jamoasi'''
    
    # Email yuborish
    print("\n📧 Email yuborilmoqda...")
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Test Email',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    
    result = email.send(fail_silently=False)
    
    print(f"✅ Email muvaffaqiyatli yuborildi!")
    print(f"   Natija: {result}")
    print(f"   To: {user.email}")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n💡 Emailingizni tekshiring:")
    print("   1. Inbox papkasi")
    print("   2. Spam papkasi")
    print("   3. Gmail qidiruv: 'EduSelf'")
    print("   4. Gmail qidiruv: 'from:sarvarrashitov4321@gmail.com'")
    
except Exception as e:
    print(f"❌ Email yuborishda xatolik: {e}")
    import traceback
    traceback.print_exc()

print()
