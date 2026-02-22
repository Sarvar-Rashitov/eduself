"""
Yangi qurilmadan kirish emailini qo'lda test qilish
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

print("=" * 80)
print("YANGI QURILMADAN KIRISH EMAIL TESTI")
print("=" * 80)

# Test foydalanuvchi
test_user = User.objects.filter(email="sarvarrashitov4321@gmail.com").first()

if not test_user:
    print("\n❌ Test foydalanuvchi topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")

# Test email yuborish
print("\n📧 Yangi qurilmadan kirish emaili yuborilmoqda...")

try:
    device_info = "Desktop - Google Chrome on Windows 10/11"
    ip_address = "192.168.1.1"
    login_time = timezone.now().strftime('%d.%m.%Y, %H:%M')
    
    html_content = render_to_string('emails/new_device_login.html', {
        'user_name': test_user.first_name,
        'device_info': device_info,
        'login_time': login_time,
        'ip_address': ip_address,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

Hisobingizga yangi qurilmadan kirish amalga oshirildi.

Qurilma: {device_info}
Vaqt: {login_time}
IP manzil: {ip_address}

Agar bu siz bo'lmasangiz, darhol parolingizni o'zgartiring.

Hurmat bilan,
EduSelf jamoasi
{settings.SITE_URL}'''
    
    email_message = EmailMultiAlternatives(
        subject='EduSelf - Yangi qurilmadan kirish',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send(fail_silently=False)
    
    print("✅ Email muvaffaqiyatli yuborildi!")
    print(f"\n📊 Tafsilotlar:")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_user.email}")
    print(f"   Subject: EduSelf - Yangi qurilmadan kirish")
    print(f"   Device: {device_info}")
    print(f"   Time: {login_time}")
    print(f"   IP: {ip_address}")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("EMAILINGIZNI TEKSHIRING")
print("=" * 80)
print(f"\n📧 Email: {test_user.email}")
print("💡 Agar inbox'da ko'rinmasa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' dan qidiring")
print("   3. eduselfuz@gmail.com dan kelgan emaillarni qidiring")
print()
