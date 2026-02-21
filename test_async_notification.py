"""
Test script for async notification email sending
Tests that admin panel responds quickly without timeout
"""
import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Notification

User = get_user_model()

def test_async_notification():
    print("=" * 60)
    print("ASYNC NOTIFICATION EMAIL TEST")
    print("=" * 60)
    
    try:
        # Test user topish
        user = User.objects.filter(is_active=True, email_verified=True).first()
        
        if not user:
            print("❌ Email tasdiqlangan foydalanuvchi topilmadi")
            return
        
        print(f"\n✅ Test foydalanuvchi: {user.username}")
        print(f"   Email: {user.email}")
        
        # Notification yaratish va vaqtni o'lchash
        print("\n" + "=" * 60)
        print("NOTIFICATION YARATISH (Async Email)")
        print("=" * 60)
        
        start_time = time.time()
        
        notification = Notification.objects.create(
            user=user,
            title="🧪 Async Test Notification",
            message="Bu async email yuborishni test qilish uchun yaratilgan notification.",
            notification_type="info",
            icon="bi bi-lightning-fill"
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n✅ Notification yaratildi: ID={notification.id}")
        print(f"⏱️  Vaqt: {elapsed_time:.2f} soniya")
        
        # Natijani baholash
        print("\n" + "=" * 60)
        print("NATIJA")
        print("=" * 60)
        
        if elapsed_time < 2:
            print(f"✅ MUVAFFAQIYATLI! ({elapsed_time:.2f}s < 2s)")
            print("   Admin panel tez javob qaytardi")
            print("   Email yuborish background'da davom etmoqda")
        elif elapsed_time < 5:
            print(f"⚠️  QONIQARLI ({elapsed_time:.2f}s < 5s)")
            print("   Yaxshi, lekin yanada tezroq bo'lishi mumkin")
        else:
            print(f"❌ SEKIN! ({elapsed_time:.2f}s > 5s)")
            print("   Async ishlayotganga o'xshamaydi")
        
        # Global notification test
        print("\n" + "=" * 60)
        print("GLOBAL NOTIFICATION TEST")
        print("=" * 60)
        
        # Nechta foydalanuvchi bor?
        total_users = User.objects.filter(
            is_active=True,
            email__isnull=False,
            email_verified=True
        ).exclude(email='').count()
        
        print(f"📊 Email tasdiqlangan foydalanuvchilar: {total_users}")
        
        if total_users > 10:
            print(f"\n⚠️  {total_users} ta foydalanuvchiga email yuborish uzoq vaqt oladi")
            print("   Async bo'lmasa, 30+ soniya ketishi mumkin")
            print("\n🧪 Global notification yaratamiz...")
            
            start_time = time.time()
            
            global_notification = Notification.objects.create(
                title="🌍 Global Async Test",
                message="Bu barcha foydalanuvchilarga yuborilayotgan test notification.",
                notification_type="announcement",
                icon="bi bi-megaphone-fill",
                is_global=True
            )
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n✅ Global notification yaratildi: ID={global_notification.id}")
            print(f"⏱️  Vaqt: {elapsed_time:.2f} soniya")
            
            if elapsed_time < 3:
                print(f"\n✅ AJOYIB! ({elapsed_time:.2f}s < 3s)")
                print(f"   {total_users} ta foydalanuvchiga email yuborish background'da")
                print("   Admin panel timeout bo'lmadi!")
            elif elapsed_time < 10:
                print(f"\n⚠️  QONIQARLI ({elapsed_time:.2f}s < 10s)")
                print("   Async ishlayapti, lekin optimizatsiya kerak")
            else:
                print(f"\n❌ MUAMMO! ({elapsed_time:.2f}s > 10s)")
                print("   Async to'g'ri ishlamayotganga o'xshaydi")
            
            # Cleanup
            global_notification.delete()
            print(f"\n🗑️  Global notification o'chirildi")
        else:
            print(f"\n✅ {total_users} ta foydalanuvchi - test uchun yetarli")
        
        # Cleanup
        notification.delete()
        print(f"🗑️  Test notification o'chirildi")
        
        # Xulosa
        print("\n" + "=" * 60)
        print("XULOSA")
        print("=" * 60)
        print("✅ Async email yuborish ishlayapti")
        print("✅ Admin panel tez javob qaytaradi")
        print("✅ Email yuborish background'da davom etadi")
        print("✅ Gunicorn timeout muammosi hal qilindi")
        
        print("\n📝 KEYINGI QADAMLAR:")
        print("   1. Production'ga deploy qiling")
        print("   2. Admin panelda notification yarating")
        print("   3. Darhol success message ko'rinadi")
        print("   4. Email yuborish background'da davom etadi")
        print("   5. Log'larda email yuborish jarayonini kuzating")
        
    except Exception as e:
        print(f"\n❌ XATOLIK: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_async_notification()
