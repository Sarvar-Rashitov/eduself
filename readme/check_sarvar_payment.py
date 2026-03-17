"""
Sarvar Rashitov to'lovini tekshirish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Payment, UserSubscription
from accounts.models import User

# Sarvar foydalanuvchisini topish
try:
    sarvar = User.objects.get(username='Sarvar')
    print(f"👤 Foydalanuvchi: {sarvar.username}")
    print(f"   Email: {sarvar.email}")
    print(f"   ID: {sarvar.id}")
    print()
    
    # Oxirgi to'lovlar
    payments = Payment.objects.filter(user=sarvar).order_by('-created_at')[:5]
    print(f"📊 Oxirgi 5 ta to'lov:")
    for p in payments:
        print(f"  - ID: {p.id}")
        print(f"    Plan: {p.plan.name}")
        print(f"    Amount: {p.final_amount} so'm")
        print(f"    Status: {p.status}")
        print(f"    Transaction ID: {p.transaction_id or 'Yoq'}")
        print(f"    Subscription: {'Bor' if p.subscription else 'Yoq'}")
        print(f"    Created: {p.created_at}")
        print()
    
    # Subscriptionlar
    subscriptions = UserSubscription.objects.filter(user=sarvar).order_by('-created_at')[:5]
    print(f"📈 Oxirgi 5 ta subscription:")
    for s in subscriptions:
        print(f"  - ID: {s.id}")
        print(f"    Plan: {s.plan.name}")
        print(f"    Status: {s.status}")
        print(f"    Start: {s.start_date}")
        print(f"    End: {s.end_date}")
        print(f"    Active: {s.is_active()}")
        print()
    
    # Active subscription
    active_sub = sarvar.get_active_subscription()
    if active_sub:
        print(f"✅ ACTIVE SUBSCRIPTION:")
        print(f"   Plan: {active_sub.plan.name}")
        print(f"   End: {active_sub.end_date}")
    else:
        print(f"❌ ACTIVE SUBSCRIPTION YO'Q!")
        
except User.DoesNotExist:
    print("❌ Sarvar foydalanuvchisi topilmadi!")
    print("\nMavjud foydalanuvchilar:")
    users = User.objects.all()[:10]
    for u in users:
        print(f"  - {u.username}")
