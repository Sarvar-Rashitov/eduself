"""
Referal tizimini test qilish skripti
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from subscriptions.models import (
    SubscriptionPlan, ReferralProgram, UserReferral, 
    ReferralProgress, UserSubscription
)
from django.utils import timezone
from datetime import timedelta


def test_referral_system():
    """Referal tizimini test qilish"""
    
    print("=" * 60)
    print("REFERAL TIZIMINI TEST QILISH")
    print("=" * 60)
    
    # 1. Ta'rif yaratish yoki olish
    print("\n1. Ta'rifni tekshirish...")
    plan, created = SubscriptionPlan.objects.get_or_create(
        slug='pro-monthly',
        defaults={
            'name': 'Pro Monthly',
            'description': 'Oylik Pro obuna',
            'price': 50000,
            'duration_days': 30,
            'unlimited_lives': True,
            'ai_analysis_limit': -1,
            'ai_companion_limit': -1,
            'university_exam_limit': -1,
            'mock_exam_limit': -1,
            'certificate_test_limit': -1,
            'is_active': True,
        }
    )
    if created:
        print(f"   ✅ Yangi ta'rif yaratildi: {plan.name}")
    else:
        print(f"   ✅ Ta'rif topildi: {plan.name}")
    
    # 2. Referal dasturini yaratish yoki olish
    print("\n2. Referal dasturini tekshirish...")
    program, created = ReferralProgram.objects.get_or_create(
        name="3 Do'st - 30 Kun Pro",
        defaults={
            'plan': plan,
            'required_referrals': 3,
            'referral_deadline_days': 30,
            'reward_duration_days': 30,
            'is_active': True,
        }
    )
    if created:
        print(f"   ✅ Yangi dastur yaratildi: {program.name}")
    else:
        print(f"   ✅ Dastur topildi: {program.name}")
    
    print(f"      Shart: {program.required_referrals} ta do'st")
    print(f"      Muddat: {program.referral_deadline_days} kun")
    print(f"      Mukofot: {program.reward_duration_days} kunlik obuna")
    
    # 3. Test foydalanuvchilarini yaratish
    print("\n3. Test foydalanuvchilarini yaratish...")
    
    # Referrer (taklif qiluvchi)
    referrer, created = User.objects.get_or_create(
        email='referrer@test.com',
        defaults={
            'first_name': 'Referrer',
            'last_name': 'User',
            'email_verified': True,
        }
    )
    if created:
        referrer.set_password('test123')
        referrer.save()
        print(f"   ✅ Referrer yaratildi: {referrer.get_display_name()}")
    else:
        print(f"   ✅ Referrer topildi: {referrer.get_display_name()}")
    
    # Referred users (taklif qilinganlar)
    referred_users = []
    for i in range(1, 4):
        user, created = User.objects.get_or_create(
            email=f'referred{i}@test.com',
            defaults={
                'first_name': f'Referred{i}',
                'last_name': 'User',
                'email_verified': True,
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            print(f"   ✅ Referred user {i} yaratildi: {user.get_display_name()}")
        else:
            print(f"   ✅ Referred user {i} topildi: {user.get_display_name()}")
        referred_users.append(user)
    
    # 4. Referal bog'lanishlarini yaratish
    print("\n4. Referal bog'lanishlarini yaratish...")
    
    for i, referred in enumerate(referred_users, 1):
        referral, created = UserReferral.objects.get_or_create(
            referrer=referrer,
            referred=referred,
            program=program
        )
        
        if created:
            print(f"   ✅ Referal {i} yaratildi: {referrer.get_display_name()} -> {referred.get_display_name()}")
            
            # ReferralProgress yangilash
            progress, _ = ReferralProgress.objects.get_or_create(
                user=referrer,
                program=program,
                defaults={
                    'deadline': timezone.now() + timedelta(days=program.referral_deadline_days)
                }
            )
            progress.referral_count += 1
            progress.save()
            
            print(f"      Hisob: {progress.referral_count}/{program.required_referrals}")
        else:
            print(f"   ℹ️  Referal {i} allaqachon mavjud")
    
    # 5. Jarayonni tekshirish
    print("\n5. Jarayonni tekshirish...")
    progress = ReferralProgress.objects.filter(user=referrer, program=program).first()
    
    if progress:
        print(f"   Foydalanuvchi: {referrer.get_display_name()}")
        print(f"   Dastur: {progress.program.name}")
        print(f"   Hisob: {progress.referral_count}/{progress.program.required_referrals}")
        print(f"   Deadline: {progress.deadline.strftime('%d.%m.%Y')}")
        completed_text = "✅ Ha" if progress.is_completed else "❌ Yo'q"
        reward_text = "✅ Ha" if progress.reward_given else "❌ Yo'q"
        print(f"   Bajarilgan: {completed_text}")
        print(f"   Mukofot berilgan: {reward_text}")
        
        # 6. Bajarilganligini tekshirish va mukofot berish
        if progress.check_completion() and not progress.reward_given:
            print("\n6. Mukofot berish...")
            
            subscription = UserSubscription.objects.create(
                user=referrer,
                plan=program.plan,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=program.reward_duration_days),
                status='active',
                acquired_via='referral'
            )
            progress.reward_given = True
            progress.save()
            
            print(f"   ✅ Mukofot berildi!")
            print(f"      Obuna: {subscription.plan.name}")
            print(f"      Muddat: {subscription.start_date.strftime('%d.%m.%Y')} - {subscription.end_date.strftime('%d.%m.%Y')}")
        elif progress.reward_given:
            print("\n6. Mukofot allaqachon berilgan ✅")
        else:
            print(f"\n6. Mukofot berish uchun yana {progress.program.required_referrals - progress.referral_count} ta referal kerak")
    else:
        print("   ❌ Jarayon topilmadi")
    
    # 7. Natijalarni ko'rsatish
    print("\n" + "=" * 60)
    print("TEST NATIJALARI")
    print("=" * 60)
    
    # Referal statistikasi
    total_referrals = UserReferral.objects.filter(referrer=referrer).count()
    print(f"\n📊 Referal statistikasi:")
    print(f"   Jami taklif qilingan: {total_referrals} ta")
    
    # Obuna statistikasi
    subscriptions = UserSubscription.objects.filter(user=referrer, acquired_via='referral')
    print(f"\n🎁 Obuna statistikasi:")
    print(f"   Referal orqali olingan obunalar: {subscriptions.count()} ta")
    
    for sub in subscriptions:
        print(f"   - {sub.plan.name}: {sub.start_date.strftime('%d.%m.%Y')} - {sub.end_date.strftime('%d.%m.%Y')} ({sub.status})")
    
    # Referal linki
    print(f"\n🔗 Referal linki:")
    print(f"   https://eduself.uz/accounts/register/?ref={referrer.id}")
    
    print("\n" + "=" * 60)
    print("✅ TEST MUVAFFAQIYATLI YAKUNLANDI!")
    print("=" * 60)


if __name__ == '__main__':
    test_referral_system()
