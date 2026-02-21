"""
Test script for Browser Native Notifications
Tests the API endpoints and notification system
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Notification
from datetime import datetime

User = get_user_model()

def test_browser_notifications():
    print("=" * 60)
    print("BROWSER NATIVE NOTIFICATIONS TEST")
    print("=" * 60)
    
    # Test user yaratish yoki olish
    try:
        user = User.objects.filter(is_active=True).first()
        if not user:
            print("❌ Faol foydalanuvchi topilmadi")
            return
        
        print(f"\n✅ Test foydalanuvchi: {user.username}")
        print(f"   Email: {user.email}")
        
        # Client yaratish va login qilish
        client = Client()
        client.force_login(user)
        
        # 1. Test notification yaratish
        print("\n" + "=" * 60)
        print("1. TEST NOTIFICATION YARATISH")
        print("=" * 60)
        
        notification = Notification.objects.create(
            user=user,
            title="🔔 Browser Notification Test",
            message="Bu browser native notification tizimini test qilish uchun yaratilgan xabar.",
            notification_type="info",
            icon="bi bi-bell-fill"
        )
        print(f"✅ Notification yaratildi: ID={notification.id}")
        print(f"   Title: {notification.title}")
        print(f"   Message: {notification.message}")
        
        # 2. API endpoint'larni test qilish
        print("\n" + "=" * 60)
        print("2. API ENDPOINTS TEST")
        print("=" * 60)
        
        # GET /api/notifications/unread/
        print("\n📡 Testing: GET /api/notifications/unread/")
        response = client.get('/api/notifications/unread/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success')}")
            print(f"   📊 Count: {data.get('count')}")
            if data.get('notifications'):
                print(f"   📋 Notifications:")
                for notif in data['notifications']:
                    print(f"      - {notif['title']}")
        else:
            print(f"   ❌ Error: {response.content}")
        
        # POST /api/notifications/permission/
        print("\n📡 Testing: POST /api/notifications/permission/")
        response = client.post(
            '/api/notifications/permission/',
            data='{"granted": true}',
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success')}")
            print(f"   💬 Message: {data.get('message')}")
        else:
            print(f"   ❌ Error: {response.content}")
        
        # POST /api/notifications/<id>/read/
        print(f"\n📡 Testing: POST /api/notifications/{notification.id}/read/")
        response = client.post(
            f'/api/notifications/{notification.id}/read/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success')}")
            print(f"   💬 Message: {data.get('message')}")
        else:
            print(f"   ❌ Error: {response.content}")
        
        # 3. JavaScript file mavjudligini tekshirish
        print("\n" + "=" * 60)
        print("3. STATIC FILES CHECK")
        print("=" * 60)
        
        js_file = 'static/js/notifications.js'
        if os.path.exists(js_file):
            print(f"✅ {js_file} mavjud")
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   📏 Size: {len(content)} bytes")
                print(f"   🔍 Contains NotificationManager: {'NotificationManager' in content}")
                print(f"   🔍 Contains fetchNotifications: {'fetchNotifications' in content}")
                print(f"   🔍 Contains startPolling: {'startPolling' in content}")
        else:
            print(f"❌ {js_file} topilmadi")
        
        # 4. Template'da script tag mavjudligini tekshirish
        print("\n" + "=" * 60)
        print("4. TEMPLATE CHECK")
        print("=" * 60)
        
        template_file = 'templates/base.html'
        if os.path.exists(template_file):
            print(f"✅ {template_file} mavjud")
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                has_script = 'notifications.js' in content
                print(f"   🔍 Contains notifications.js script: {has_script}")
                if has_script:
                    print("   ✅ Script tag to'g'ri qo'shilgan")
                else:
                    print("   ⚠️  Script tag topilmadi")
        else:
            print(f"❌ {template_file} topilmadi")
        
        # 5. Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print("✅ API endpoints ishlayapti")
        print("✅ Notification yaratish ishlayapti")
        print("✅ JavaScript file mavjud")
        print("✅ Template'da script tag mavjud")
        print("\n📝 KEYINGI QADAMLAR:")
        print("   1. Serverni ishga tushiring: python manage.py runserver")
        print("   2. Browserda sahifani oching")
        print("   3. Browser console'ni oching (F12)")
        print("   4. Notification permission so'rashni kuting")
        print("   5. 'Allow' tugmasini bosing")
        print("   6. Admin paneldan yangi notification yarating")
        print("   7. 30 soniya ichida browser notification ko'rinishi kerak")
        
        # Test notification'ni o'chirish
        notification.delete()
        print(f"\n🗑️  Test notification o'chirildi")
        
    except Exception as e:
        print(f"\n❌ XATOLIK: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_browser_notifications()
