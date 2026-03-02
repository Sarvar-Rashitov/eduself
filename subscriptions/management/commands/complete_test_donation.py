"""
Local test uchun donatni qo'lda complete qilish
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import Donation


class Command(BaseCommand):
    help = 'Local test uchun donatni qo\'lda complete qilish'

    def add_arguments(self, parser):
        parser.add_argument('donation_id', type=int, help='Donation ID')

    def handle(self, *args, **options):
        donation_id = options['donation_id']
        
        try:
            donation = Donation.objects.get(id=donation_id)
            
            if donation.status == 'completed':
                self.stdout.write(self.style.WARNING(f'Donat allaqachon bajarilgan: {donation.id}'))
                return
            
            # Donatni tasdiqlash
            donation.status = 'completed'
            donation.completed_at = timezone.now()
            donation.transaction_id = f'TEST_DONATE_{donation.id}'
            donation.save()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Donat muvaffaqiyatli bajarildi!'))
            self.stdout.write(f'   Donation ID: {donation.id}')
            self.stdout.write(f'   Foydalanuvchi: {donation.user.get_display_name()}')
            self.stdout.write(f'   Summa: {donation.amount} so\'m')
            self.stdout.write(f'   Xabar: {donation.message or "(xabar yo\'q)"}')
            self.stdout.write(f'   Bajarilgan: {donation.completed_at.strftime("%d.%m.%Y %H:%M")}')
            
        except Donation.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Donat topilmadi: {donation_id}'))
