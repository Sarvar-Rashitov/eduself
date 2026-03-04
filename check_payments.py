"""
To'lovlarni tekshirish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Payment, UserSubscription

# Barcha to'lovlar
all_payments = Payment.objects.all()
print(f"📊 Jami to'lovlar: {all_payments.count()}")

# Status bo'yicha
pending = Payment.objects.filter(status='pending')
processing = Payment.objects.filter(status='processing')
completed = Payment.objects.filter(status='completed')

print(f"⏳ Pending: {pending.count()}")
print(f"🔄 Processing: {processing.count()}")
print(f"✅ Completed: {completed.count()}")

print("\n📝 Oxirgi 10 ta to'lov:")
for p in all_payments.order_by('-created_at')[:10]:
    trans_id = p.transaction_id or "Yo'q"
    has_sub = 'Bor' if p.subscription else "Yo'q"
    print(f"  - {p.user.username}: {p.plan.name} - {p.final_amount} so'm")
    print(f"    Status: {p.status}")
    print(f"    Transaction ID: {trans_id}")
    print(f"    Subscription: {has_sub}")
    print()

# Pending to'lovlar batafsil
if pending.count() > 0:
    print("\n⚠️  PENDING TO'LOVLAR:")
    for p in pending:
        trans_id = p.transaction_id or "Yo'q"
        print(f"  - ID: {p.id}")
        print(f"    User: {p.user.username}")
        print(f"    Plan: {p.plan.name}")
        print(f"    Amount: {p.final_amount}")
        print(f"    Transaction ID: {trans_id}")
        print(f"    Payment Data: {bool(p.payment_data)}")
        print()
