"""
Barcha pending donatlarni completed qilish va message qo'shish
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

# Default xabarlar
default_messages = [
    "Rahmat! Ajoyib loyiha! 🎉",
    "Sizlarni qo'llab-quvvatlayman! 💪",
    "Davom eting, zo'r ish qilyapsizlar!",
    "Ta'lim sohasiga qo'shgan hissangiz uchun rahmat!",
    "Muvaffaqiyatlar tilayman! 🚀",
    "Kelajak avlod uchun qilayotgan ishlaringiz uchun rahmat!",
    "Juda foydali platforma!",
    "O'quvchilarga katta yordam bermoqda!",
    "Sizlar bilan faxrlanaman!",
    "Zo'r loyiha! Davom eting!",
]

updated_count = 0
for i, donation in enumerate(pending_donations):
    # Status'ni completed qilish
    donation.status = 'completed'
    
    # Completed_at qo'shish
    if not donation.completed_at:
        donation.completed_at = timezone.now()
    
    # Agar message bo'lmasa, default message qo'shish
    if not donation.message:
        donation.message = default_messages[i % len(default_messages)]
    
    # Transaction ID qo'shish (agar bo'lmasa)
    if not donation.transaction_id:
        donation.transaction_id = f"MANUAL_{donation.id}_{int(timezone.now().timestamp())}"
    
    donation.save()
    
    print(f"✅ {donation.user.username} - {donation.amount} so'm - Completed")
    updated_count += 1

print(f"\n🎉 Jami {updated_count} ta donat completed qilindi!")

# Natijani ko'rsatish
completed_donations = Donation.objects.filter(status='completed')
donations_with_message = Donation.objects.filter(
    status='completed',
    message__isnull=False
).exclude(message='')

print(f"\n📈 Hozirgi completed donatlar: {completed_donations.count()}")
print(f"💬 Message bor donatlar: {donations_with_message.count()}")

print("\n📝 Oxirgi 5 ta donat:")
for d in donations_with_message.order_by('-completed_at')[:5]:
    print(f"  - {d.user.username}: {d.amount} so'm")
    print(f"    Message: {d.message[:50]}...")
