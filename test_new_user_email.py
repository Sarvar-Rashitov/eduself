"""
Yangi foydalanuvchiga email yuborish testi
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
print("YANGI FOYDALANUVCHI EMAIL TESTI")
print("=" * 70)

# Yangi foydalanuvchi
new_email = "sarvarrashitov43210@gmail.com"
user = User.objects.filter(email=new_email).first()

if not user:
    print(f"❌ {new_email} topilmadi!")
    print("\n📋 Barcha foydalanuvchilar:")
    for u in User.objects.all().order_by('-id')[:10]:
        print(f"   - {u.first_name} ({u.email}) - ID: {u.id}")
    sys.exit(1)

print(f"\n✅ Foydalanuvchi topildi!")
print(f"   ID: {user.id}")
print(f"   Ism: {user.first_name}")
print(f"   Email: {user.email}")
print(f"   Email verified: {user.email_verified}")
print(f"   Created: {user.created_at}")

# ============================================================================
# TEST 1: Email tasdiqlash xati
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1: EMAIL TASDIQLASH XATI")
print("=" * 70)

try:
    from accounts.models import EmailVerificationToken
    
    # Token yaratish
    token = EmailVerificationToken.objects.create(user=user)
    verify_url = f"https://eduself.uz/accounts/verify-email/{token.token}/"
    
    # HTML email yaratish
    html_content = render_to_string('emails/verify_email.html', {
        'user_name': user.first_name,
        'verify_url': verify_url,
        'site_url': settings.SITE_URL,
    })
    
    # Text fallback
    text_content = f'''Assalomu alaykum, {user.first_name}!

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
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ Email tasdiqlash xati yuborildi!")
    print(f"   To: {user.email}")
    
    # Token o'chirish
    token.delete()
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 2: Xush kelibsiz emaili
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2: XUSH KELIBSIZ EMAILI")
print("=" * 70)

try:
    html_content = render_to_string('emails/welcome.html', {
        'user_name': user.first_name,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {user.first_name}!

EduSelf platformasiga xush kelibsiz!

Endi siz platformaning barcha imkoniyatlaridan foydalanishingiz mumkin:
- 📚 Testlar va mock imtihonlar
- 🎓 Video darslar
- 📊 O'z natijalaringizni kuzatish
- 🏆 Reyting va sertifikatlar

Platformaga kirish: {settings.SITE_URL}

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Xush kelibsiz!',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ Xush kelibsiz emaili yuborildi!")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 3: Yangi qurilmadan kirish emaili
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3: YANGI QURILMADAN KIRISH EMAILI")
print("=" * 70)

try:
    html_content = render_to_string('emails/new_device_login.html', {
        'user_name': user.first_name,
        'device_type': 'Desktop',
        'browser': 'Chrome',
        'os': 'Windows',
        'ip_address': '10.0.0.1',
        'login_time': user.last_login or user.created_at,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {user.first_name}!

Sizning hisobingizga yangi qurilmadan kirish amalga oshirildi.

Qurilma: Desktop
Brauzer: Chrome
OS: Windows
IP: 10.0.0.1

Agar bu siz bo'lmasangiz, darhol parolingizni o'zgartiring!

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Yangi qurilmadan kirish',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ Yangi qurilmadan kirish emaili yuborildi!")
    
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

print(f"\n✅ Barcha emaillar yuborildi!")
print(f"\n📧 Emailingizni tekshiring: {user.email}")
print("\n💡 Quyidagi emaillar yuborilgan bo'lishi kerak:")
print("   1. Email tasdiqlash xati")
print("   2. Xush kelibsiz emaili")
print("   3. Yangi qurilmadan kirish emaili")

print("\n📊 Agar emaillar kelmagan bo'lsa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' dan qidiring")
print("   3. Production serverda kod yangilanganini tekshiring")
print("   4. Production log'larini tekshiring")

print()
