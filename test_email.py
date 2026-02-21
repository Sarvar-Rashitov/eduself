#!/usr/bin/env python
"""Email sozlamalarini test qilish"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("EMAIL SOZLAMALARI TEST")
print("=" * 60)
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
password_display = '*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else "BO'SH"
print(f"EMAIL_HOST_PASSWORD: {password_display}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 60)

if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
    print("\n❌ XATOLIK: EMAIL_HOST_USER yoki EMAIL_HOST_PASSWORD bo'sh!")
    print("\nYechim:")
    print("1. Google hisobingizda 2-bosqichli tasdiqlashni yoqing")
    print("2. App Password yarating: https://myaccount.google.com/apppasswords")
    print("3. .env faylida EMAIL_HOST_PASSWORD ni yangilang (bo'sh joysiz!)")
    exit(1)

print("\n📧 Test email yuborilmoqda...")
print(f"Qabul qiluvchi: {settings.EMAIL_HOST_USER}")

try:
    result = send_mail(
        subject='EduSelf - Email Test',
        message='Bu test xabari. Agar bu xabar kelgan bo\'lsa, email sozlamalari to\'g\'ri ishlayapti! ✓',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    
    if result:
        print("\n✅ Email muvaffaqiyatli yuborildi!")
        print(f"✓ {settings.EMAIL_HOST_USER} manziliga xabar yuborildi")
        print("\nInbox'ingizni tekshiring!")
    else:
        print("\n❌ Email yuborilmadi (result=0)")
        
except Exception as e:
    print(f"\n❌ XATOLIK: {e}")
    print("\nMumkin bo'lgan sabablar:")
    print("1. Gmail App Password noto'g'ri yoki eskirgan")
    print("2. 2-bosqichli tasdiqlash yoqilmagan")
    print("3. Internet aloqasi yo'q")
    print("4. Gmail hisobingiz bloklangan")
    print("\nYechim:")
    print("1. https://myaccount.google.com/apppasswords ga kiring")
    print("2. Yangi App Password yarating")
    print("3. .env faylida EMAIL_HOST_PASSWORD ni yangilang")
    print("   Format: EMAIL_HOST_PASSWORD=abcdefghijklmnop (bo'sh joysiz!)")
