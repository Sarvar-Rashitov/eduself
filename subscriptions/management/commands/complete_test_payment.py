"""
Local test uchun to'lovni qo'lda complete qilish
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import Payment, UserSubscription


class Command(BaseCommand):
    help = 'Local test uchun to\'lovni qo\'lda complete qilish'

    def add_arguments(self, parser):
        parser.add_argument('payment_id', type=int, help='Payment ID')

    def handle(self, *args, **options):
        payment_id = options['payment_id']
        
        try:
            payment = Payment.objects.get(id=payment_id)
            
            if payment.status == 'completed':
                self.stdout.write(self.style.WARNING(f'To\'lov allaqachon bajarilgan: {payment.id}'))
                return
            
            # To'lovni tasdiqlash
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.transaction_id = f'TEST_{payment.id}'
            payment.save()
            
            # Obuna yaratish
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
            
            # Promokodni ishlatish
            if payment.promo_code:
                payment.promo_code.use()
            
            self.stdout.write(self.style.SUCCESS(f'✅ To\'lov muvaffaqiyatli bajarildi!'))
            self.stdout.write(f'   Payment ID: {payment.id}')
            self.stdout.write(f'   Foydalanuvchi: {payment.user.get_display_name()}')
            self.stdout.write(f'   Ta\'rif: {payment.plan.name}')
            self.stdout.write(f'   Summa: {payment.final_amount} so\'m')
            self.stdout.write(f'   Obuna ID: {subscription.id}')
            self.stdout.write(f'   Muddat: {subscription.start_date.strftime("%d.%m.%Y")} - {subscription.end_date.strftime("%d.%m.%Y")}')
            
        except Payment.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ To\'lov topilmadi: {payment_id}'))
