"""
Completed lekin subscription yo'q to'lovlarni tuzatish
"""
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Payment, UserSubscription

# Completed lekin subscription yo'q to'lovlarni topish
payments_without_sub = Payment.objects.filter(
    status='completed',
    subscription__isnull=True
)

print(f"📊 Completed lekin subscription yo'q to'lovlar: {payments_without_sub.count()}")

if payments_without_sub.count() == 0:
    print("✅ Barcha completed to'lovlarda subscription bor!")
    exit()

print("\n🔄 Subscriptionlar yaratish...")

created_count = 0
for payment in payments_without_sub:
    # Subscription yaratish
    subscription = UserSubscription.objects.create(
        user=payment.user,
        plan=payment.plan,
        start_date=payment.completed_at or timezone.now(),
        end_date=(payment.completed_at or timezone.now()) + timedelta(days=payment.plan.duration_days),
        status='active',
        acquired_via='payment'
    )
    
    payment.subscription = subscription
    payment.save()
    
    print(f"✅ {payment.user.username} - {payment.plan.name} - Subscription yaratildi!")
    print(f"   Payment ID: {payment.id}")
    print(f"   Subscription ID: {subscription.id}")
    print(f"   End Date: {subscription.end_date.strftime('%Y-%m-%d')}")
    print()
    
    created_count += 1

print(f"\n🎉 Jami {created_count} ta subscription yaratildi!")

# Natijani ko'rsatish
active_subscriptions = UserSubscription.objects.filter(status='active')
print(f"\n📈 Hozirgi active subscriptions: {active_subscriptions.count()}")

# Sarvar'ni tekshirish
from accounts.models import User
try:
    sarvar = User.objects.get(username='Sarvar')
    sarvar_subs = UserSubscription.objects.filter(user=sarvar, status='active')
    print(f"\n👤 Sarvar subscriptions: {sarvar_subs.count()}")
    for s in sarvar_subs:
        print(f"   - {s.plan.name} (End: {s.end_date.strftime('%Y-%m-%d')})")
except User.DoesNotExist:
    pass
