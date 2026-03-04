"""
Pending holatdagi donatlarni completed qilish
"""
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from subscriptions.models import Donation

# Pending holatdagi donatlarni topish
pending_donations = Donation.objects.filter(status='pending')

print(f"📊 Pending holatdagi donatlar: {pending_donations.count()}")

if pending_donations.count() == 0:
    print("✅ Barcha donatlar allaqachon completed!")
    exit()

print("\n🔄 Donatlarni completed qilish...")

updated_count = 0
for donation in pending_donations:
    # Agar transaction_id bo'lsa, to'lov amalga oshgan deb hisoblaymiz
    if donation.transaction_id or donation.payment_data:
        donation.status = 'completed'
        if not donation.completed_at:
            donation.completed_at = timezone.now()
        donation.save()
        
        print(f"✅ {donation.user.username} - {donation.amount} so'm - Completed")
        updated_count += 1
    else:
        print(f"⚠️  {donation.user.username} - {donation.amount} so'm - Transaction ID yo'q")

print(f"\n🎉 Jami {updated_count} ta donat completed qilindi!")

# Natijani ko'rsatish
completed_donations = Donation.objects.filter(status='completed')
print(f"\n📈 Hozirgi completed donatlar: {completed_donations.count()}")
