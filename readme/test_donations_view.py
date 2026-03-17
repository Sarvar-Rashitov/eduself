"""
Donations view'ni test qilish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Donation

# Recent donations
recent_donations = Donation.objects.filter(
    status='completed',
    message__isnull=False
).exclude(message='').select_related('user').order_by('-completed_at')[:20]

print(f"📊 Recent donations count: {recent_donations.count()}")
print(f"📊 Total in queryset: {len(list(recent_donations))}")

print("\n📝 Donations:")
for i, d in enumerate(recent_donations, 1):
    print(f"{i}. {d.user.username}: {d.amount} so'm - {d.message[:30]}...")

# Unique users
unique_users = set([d.user.username for d in recent_donations])
print(f"\n👥 Unique users: {len(unique_users)}")
print(f"Users: {', '.join(unique_users)}")
