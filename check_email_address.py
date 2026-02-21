"""
Email manzilni tekshirish
"""
import os
import sys
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User

print("=" * 70)
print("EMAIL MANZILNI TEKSHIRISH")
print("=" * 70)

# Email manzillar
email1 = "sarvarrashitov43210@gmail.com"
email2 = "sarvarrashitov4321@gmail.com"

print(f"\n🔍 Qidirilayotgan email: {email1}")

user = User.objects.filter(email=email1).first()

if user:
    print(f"\n✅ Foydalanuvchi topildi!")
    print(f"   ID: {user.id}")
    print(f"   Ism: {user.first_name} {user.last_name}")
    print(f"   Email: '{user.email}'")
    print(f"   Email verified: {user.email_verified}")
    print(f"   Created: {user.created_at}")
    
    # Email manzilni tekshirish
    if user.email != email1:
        print(f"\n⚠️  EMAIL MANZIL NOTO'G'RI!")
        print(f"   Kutilgan: '{email1}'")
        print(f"   Haqiqiy: '{user.email}'")
        print(f"   Farq: Bo'sh joy yoki boshqa belgilar bor")
    else:
        print(f"\n✅ Email manzil to'g'ri")
else:
    print(f"\n❌ {email1} topilmadi!")
    
    # Shunga o'xshash emaillarni qidirish
    print(f"\n🔍 Shunga o'xshash emaillar:")
    similar_users = User.objects.filter(email__icontains='sarvarrashitov').order_by('-id')
    
    if similar_users:
        for u in similar_users:
            print(f"   - ID: {u.id}, Email: '{u.email}', Ism: {u.first_name}")
    else:
        print("   Topilmadi")

print("\n" + "=" * 70)
print("XULOSA")
print("=" * 70)

if user:
    print(f"\n✅ Email manzil: {user.email}")
    print(f"\n💡 Agar email kelmagan bo'lsa:")
    print("   1. Gmail'da spam papkasini tekshiring")
    print("   2. Gmail'da 'EduSelf' dan qidiring")
    print("   3. Gmail'da 'from:sarvarrashitov4321@gmail.com' dan qidiring")
    print("   4. Gmail'ning 'All Mail' papkasini tekshiring")
    print("   5. Email manzil to'g'ri kiritilganini tekshiring")
else:
    print(f"\n❌ Foydalanuvchi topilmadi!")
    print(f"   Email: {email1}")

print()
