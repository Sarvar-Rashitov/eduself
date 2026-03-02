from django.core.management.base import BaseCommand
from accounts.models import User
from subscriptions.models import SubscriptionPlan, UserSubscription
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Test subscription - give Pro to first user'

    def handle(self, *args, **options):
        # Birinchi foydalanuvchini topish
        user = User.objects.first()
        
        if not user:
            self.stdout.write(self.style.ERROR('No users found!'))
            return
        
        # Pro ta'rifni topish
        try:
            pro_plan = SubscriptionPlan.objects.get(slug='pro')
        except SubscriptionPlan.DoesNotExist:
            self.stdout.write(self.style.ERROR('Pro plan not found! Run create_sample_plans first.'))
            return
        
        # Eski obunalarni o'chirish
        UserSubscription.objects.filter(user=user, status='active').update(status='expired')
        
        # Yangi obuna yaratish
        subscription = UserSubscription.objects.create(
            user=user,
            plan=pro_plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            status='active',
            acquired_via='admin'
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Pro subscription given to {user.get_display_name()}'))
        self.stdout.write(f'Plan: {pro_plan.name}')
        self.stdout.write(f'Valid until: {subscription.end_date.strftime("%d.%m.%Y")}')
        self.stdout.write(f'\nNow visit:')
        self.stdout.write(f'- Home: http://127.0.0.1:8000/')
        self.stdout.write(f'- Profile: http://127.0.0.1:8000/accounts/profile/')
        self.stdout.write(f'- Pro page: http://127.0.0.1:8000/subscriptions/pro/')
