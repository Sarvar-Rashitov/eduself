"""
Test uchun donatlar yaratish
"""
import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from accounts.models import User
from subscriptions.models import Donation

# Test foydalanuvchilarni olish
users = User.objects.all()[:5]

if not users:
    print("❌ Foydalanuvchilar topilmadi!")
    exit()

# Test donatlar
test_donations = [
    {
        'amount': 15000,
        'message': "Juda zo'r loyiha! Muvaffaqiyatlar tilayman! 🎉",
    },
    {
        'amount': 35000,
        'message': "Rahmat sizlarga! Ta'lim sohasiga qo'shgan hissangiz uchun.",
    },
    {
        'amount': 75000,
        'message': "Ajoyib platforma! O'quvchilarga katta yordam bermoqda.",
    },
    {
        'amount': 25000,
        'message': "Davom eting! Sizlar bilan faxrlanaman! 💪",
    },
    {
        'amount': 50000,
        'message': "Kelajak avlod uchun qilayotgan ishlaringiz uchun rahmat!",
    },
]

created_count = 0

for i, donation_data in enumerate(test_donations):
    if i >= len(users):
        break
    
    user = users[i]
    
    # Donat yaratish
    donation = Donation.objects.create(
        user=user,
        amount=donation_data['amount'],
        message=donation_data['message'],
        payment_method='click',
        status='completed',
        transaction_id=f'TEST_{timezone.now().timestamp()}',
        completed_at=timezone.now() - timedelta(hours=i)
    )
    
    created_count += 1
    print(f"✅ Donat yaratildi: {user.username} - {donation.amount} so'm")

print(f"\n🎉 Jami {created_count} ta test donat yaratildi!")
