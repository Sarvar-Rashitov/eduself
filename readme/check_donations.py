"""
Donatlarni tekshirish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Donation

# Barcha donatlar
all_donations = Donation.objects.all()
print(f"📊 Jami donatlar: {all_donations.count()}")

# Completed donatlar
completed_donations = Donation.objects.filter(status='completed')
print(f"✅ Completed donatlar: {completed_donations.count()}")

# Message bor donatlar
donations_with_message = Donation.objects.filter(
    status='completed',
    message__isnull=False
).exclude(message='')
print(f"💬 Message bor donatlar: {donations_with_message.count()}")

print("\n📝 Donatlar ro'yxati:")
for d in donations_with_message[:10]:
    print(f"  - {d.user.username}: {d.amount} so'm")
    print(f"    Message: {d.message[:50]}...")
    print(f"    Status: {d.status}")
    print()
