"""
Pending to'lovlarni completed qilish va subscription yaratish
"""
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Payment, UserSubscription

# Pending to'lovlarni topish
pending_payments = Payment.objects.filter(status='pending')

print(f"📊 Pending to'lovlar: {pending_payments.count()}")

if pending_payments.count() == 0:
    print("✅ Barcha to'lovlar allaqachon completed!")
    exit()

print("\n🔄 To'lovlarni completed qilish va subscription yaratish...")

updated_count = 0
for payment in pending_payments:
    # Status'ni completed qilish
    payment.status = 'completed'
    
    # Completed_at qo'shish
    if not payment.completed_at:
        payment.completed_at = timezone.now()
    
    # Transaction ID qo'shish (agar bo'lmasa)
    if not payment.transaction_id:
        payment.transaction_id = f"MANUAL_{payment.id}_{int(timezone.now().timestamp())}"
    
    payment.save()
    
    # Subscription yaratish (agar yo'q bo'lsa)
    if not payment.subscription:
        subscription = UserSubscription.objects.create(
            user=payment.user,
            plan=payment.plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=payment.plan.duration_days),
            status='active',
            acquired_via='payment'
        )
        
        payment.subscription = subscription
        payment.save()
        
        print(f"✅ {payment.user.username} - {payment.plan.name} - Subscription yaratildi!")
    else:
        print(f"✅ {payment.user.username} - {payment.plan.name} - Completed")
    
    updated_count += 1

print(f"\n🎉 Jami {updated_count} ta to'lov completed qilindi!")

# Natijani ko'rsatish
completed_payments = Payment.objects.filter(status='completed')
active_subscriptions = UserSubscription.objects.filter(status='active')

print(f"\n📈 Hozirgi completed to'lovlar: {completed_payments.count()}")
print(f"📈 Hozirgi active subscriptions: {active_subscriptions.count()}")

print("\n📝 Oxirgi 5 ta subscription:")
for s in active_subscriptions.order_by('-created_at')[:5]:
    print(f"  - {s.user.username}: {s.plan.name}")
    print(f"    Start: {s.start_date.strftime('%Y-%m-%d')}")
    print(f"    End: {s.end_date.strftime('%Y-%m-%d')}")
    print(f"    Status: {s.status}")
