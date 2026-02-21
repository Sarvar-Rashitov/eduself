"""
Boshqa email manzilga test yuborish
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

print("=" * 70)
print("BOSHQA EMAIL MANZILGA TEST")
print("=" * 70)

# Test email manzil
test_email = input("\nTest email manzilni kiriting: ").strip()

if not test_email:
    print("❌ Email manzil kiritilmadi!")
    sys.exit(1)

print(f"\n📧 Test email: {test_email}")
print(f"📤 Yuboruvchi: {settings.DEFAULT_FROM_EMAIL}")

# Email yuborish
try:
    html_content = render_to_string('emails/welcome.html', {
        'user_name': 'Test User',
        'site_url': settings.SITE_URL,
    })
    
    text_content = '''Assalomu alaykum!

Bu test email xabari.

Agar bu email kelgan bo'lsa, demak email yuborish to'g'ri ishlayapti!

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Test Email',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print(f"\n✅ Email muvaffaqiyatli yuborildi!")
    print(f"   To: {test_email}")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    
    print(f"\n💡 Emailingizni tekshiring:")
    print(f"   1. Inbox papkasi")
    print(f"   2. Spam papkasi")
    print(f"   3. All Mail papkasi")
    
except Exception as e:
    print(f"\n❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

print()
