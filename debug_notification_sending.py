"""
Notification yuborishni debug qilish
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
from django.conf import settings

print("=" * 70)
print("NOTIFICATION YUBORISH DEBUG")
print("=" * 70)

# Sizning foydalanuvchingizni topish
test_email = "sarvarrashitov4321@gmail.com"
test_user = User.objects.filter(email=test_email).first()

if not test_user:
    print(f"❌ {test_email} topilmadi!")
    sys.exit(1)

print(f"\n✅ Test foydalanuvchi: {test_user.first_name}")
print(f"   Email: {test_user.email}")
print(f"   Email verified: {test_user.email_verified}")
print(f"   Telegram chat_id: {test_user.telegram_chat_id}")

# Email sozlamalarini tekshirish
print("\n" + "=" * 70)
print("EMAIL SOZLAMALARI")
print("=" * 70)
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

# Telegram sozlamalarini tekshirish
print("\n" + "=" * 70)
print("TELEGRAM SOZLAMALARI")
print("=" * 70)
bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
if bot_token:
    print(f"TELEGRAM_BOT_TOKEN: {bot_token[:10]}...{bot_token[-10:]}")
else:
    print("❌ TELEGRAM_BOT_TOKEN topilmadi!")

# Notification yaratish
print("\n" + "=" * 70)
print("NOTIFICATION YARATISH")
print("=" * 70)

notification = Notification.objects.create(
    user=test_user,
    title="Debug Test",
    message="Bu debug test xabari. Email va Telegram kelishi kerak.",
    notification_type='info',
    icon='🔍',
    link='https://eduself.uz'
)

print(f"\n✅ Notification yaratildi: ID={notification.id}")
print("⏳ 10 soniya kutamiz (yuborish uchun)...")

# 10 soniya kutish
time.sleep(10)

print("\n" + "=" * 70)
print("MANUAL EMAIL YUBORISH TESTI")
print("=" * 70)

# Manual email yuborish
try:
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    
    html_content = render_to_string('emails/notification.html', {
        'user_name': test_user.first_name,
        'title': notification.title,
        'message': notification.message,
        'link': notification.link,
        'notification_type': notification.get_notification_type_display(),
        'icon': notification.icon,
        'site_url': settings.SITE_URL,
    })
    
    text_content = f'''Assalomu alaykum, {test_user.first_name}!

{notification.get_notification_type_display()}: {notification.title}

{notification.message}

Havola: {notification.link}

Hurmat bilan,
EduSelf jamoasi'''
    
    email = EmailMultiAlternatives(
        subject=f'EduSelf - {notification.title}',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[test_user.email]
    )
    email.attach_alternative(html_content, "text/html")
    
    print("📧 Email yuborilmoqda...")
    email.send(fail_silently=False)
    print("✅ Email muvaffaqiyatli yuborildi!")
    
except Exception as e:
    print(f"❌ Email yuborishda xatolik: {e}")
    import traceback
    traceback.print_exc()

# Manual Telegram yuborish
print("\n" + "=" * 70)
print("MANUAL TELEGRAM YUBORISH TESTI")
print("=" * 70)

if test_user.telegram_chat_id:
    try:
        from telegram_bot.notification_sender import send_telegram_notification
        
        print("📱 Telegram yuborilmoqda...")
        result = send_telegram_notification(
            user_id=test_user.id,
            title=notification.title,
            message=notification.message,
            link=notification.link,
            is_global=False
        )
        
        if result:
            print("✅ Telegram muvaffaqiyatli yuborildi!")
        else:
            print("❌ Telegram yuborilmadi!")
            
    except Exception as e:
        print(f"❌ Telegram yuborishda xatolik: {e}")
        import traceback
        traceback.print_exc()
else:
    print("⚠️  Telegram chat_id yo'q!")

# Cleanup
print(f"\n🗑️  Test notification o'chirildi")
notification.delete()

print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)
print("\n💡 Agar email yoki telegram kelmagan bo'lsa:")
print("   1. Yuqoridagi xatoliklarni o'qing")
print("   2. Email sozlamalarini tekshiring")
print("   3. Telegram bot ishlayotganini tekshiring")
print("   4. Signal ishlab turganini tekshiring")
print()
