"""
Email ulanishini va sozlamalarni tekshirish
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("=" * 80)
print("EMAIL ULANISH VA SOZLAMALARNI TEKSHIRISH")
print("=" * 80)

# Email sozlamalarini ko'rsatish
print("\n📧 EMAIL SOZLAMALARI:")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"   EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Test email manzil
test_email = "sarvarrashitov4321@gmail.com"

# ============================================================================
# TEST 1: SMTP ulanishini tekshirish
# ============================================================================
print("\n" + "=" * 80)
print("TEST 1: SMTP ULANISHINI TEKSHIRISH")
print("=" * 80)

try:
    print("\n🔌 SMTP serverga ulanish...")
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.set_debuglevel(1)  # Debug rejimi
    server.ehlo()
    
    print("\n🔐 TLS yoqish...")
    server.starttls()
    server.ehlo()
    
    print("\n🔑 Login qilish...")
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    
    print("\n✅ SMTP ulanish muvaffaqiyatli!")
    server.quit()
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ Autentifikatsiya xatosi: {e}")
    print("\n💡 Yechim:")
    print("   1. Gmail App Password to'g'riligini tekshiring")
    print("   2. .env faylda EMAIL_HOST_PASSWORD to'g'ri ekanligini tekshiring")
    print("   3. Gmail'da 2-Step Verification yoqilganligini tekshiring")
    
except Exception as e:
    print(f"\n❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 2: Oddiy email yuborish (Django send_mail)
# ============================================================================
print("\n" + "=" * 80)
print("TEST 2: ODDIY EMAIL YUBORISH (Django send_mail)")
print("=" * 80)

try:
    print(f"\n📧 Email yuborilmoqda: {test_email}")
    
    send_mail(
        subject='EduSelf - Test Email (send_mail)',
        message='Bu oddiy test email. Agar bu emailni ko\'rsangiz, email tizimi ishlayapti!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        fail_silently=False,
    )
    
    print("✅ Email yuborildi!")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_email}")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 3: HTML email yuborish (EmailMultiAlternatives)
# ============================================================================
print("\n" + "=" * 80)
print("TEST 3: HTML EMAIL YUBORISH (EmailMultiAlternatives)")
print("=" * 80)

try:
    print(f"\n📧 HTML email yuborilmoqda: {test_email}")
    
    text_content = 'Bu HTML test email. Agar bu emailni ko\'rsangiz, email tizimi ishlayapti!'
    html_content = '''
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #4F46E5;">EduSelf - Test Email</h2>
            <p>Bu HTML test email.</p>
            <p>Agar bu emailni ko'rsangiz, <strong>email tizimi ishlayapti!</strong></p>
            <hr>
            <p style="color: #666; font-size: 12px;">EduSelf jamoasi</p>
        </body>
    </html>
    '''
    
    email = EmailMultiAlternatives(
        subject='EduSelf - Test Email (HTML)',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    
    print("✅ HTML email yuborildi!")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   To: {test_email}")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# TEST 4: To'g'ridan-to'g'ri SMTP orqali yuborish
# ============================================================================
print("\n" + "=" * 80)
print("TEST 4: TO'G'RIDAN-TO'G'RI SMTP ORQALI YUBORISH")
print("=" * 80)

try:
    print(f"\n📧 SMTP email yuborilmoqda: {test_email}")
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'EduSelf - Test Email (Direct SMTP)'
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = test_email
    
    text = 'Bu to\'g\'ridan-to\'g\'ri SMTP orqali yuborilgan test email.'
    html = '''
    <html>
        <body>
            <h2>EduSelf - Test Email (Direct SMTP)</h2>
            <p>Bu to'g'ridan-to'g'ri SMTP orqali yuborilgan test email.</p>
        </body>
    </html>
    '''
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.send_message(msg)
    server.quit()
    
    print("✅ SMTP email yuborildi!")
    print(f"   From: {settings.EMAIL_HOST_USER}")
    print(f"   To: {test_email}")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# XULOSA
# ============================================================================
print("\n" + "=" * 80)
print("XULOSA")
print("=" * 80)

print(f"\n📧 Emailingizni tekshiring: {test_email}")
print("\n💡 Agar emaillar kelmagan bo'lsa:")
print("   1. Spam papkasini tekshiring")
print("   2. Gmail'da 'EduSelf' yoki 'eduselfuz' dan qidiring")
print("   3. Gmail'da 'All Mail' papkasini tekshiring")
print("   4. Gmail App Password to'g'riligini tekshiring")
print("   5. 2-3 daqiqa kutib ko'ring")

print("\n🔧 Agar hali ham kelmasa:")
print("   1. Gmail'da 'Less secure app access' yoqilganligini tekshiring")
print("   2. Gmail'da 'IMAP/POP' yoqilganligini tekshiring")
print("   3. Boshqa email manzilga test qiling")

print()
