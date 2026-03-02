from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan, ReferralProgram
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create sample subscription plans and referral programs'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample subscription plans...')
        
        # Basic Plan
        basic, created = SubscriptionPlan.objects.get_or_create(
            slug='basic',
            defaults={
                'name': 'EduSelf Basic',
                'description': 'Asosiy xususiyatlar bilan tanishing',
                'price': 29000,
                'duration_days': 30,
                'unlimited_lives': False,
                'ai_analysis_limit': 10,
                'ai_companion_limit': 20,
                'university_exam_limit': 5,
                'mock_exam_limit': 10,
                'certificate_test_limit': 5,
                'icon': 'bi-star',
                'color': '#6366f1',
                'badge_text': 'Boshlang\'ich',
                'is_popular': False,
                'is_active': True,
                'order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {basic.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'- Already exists: {basic.name}'))
        
        # Pro Plan
        pro, created = SubscriptionPlan.objects.get_or_create(
            slug='pro',
            defaults={
                'name': 'EduSelf Pro',
                'description': 'Eng mashhur tanlov - barcha imkoniyatlar',
                'price': 79000,
                'duration_days': 30,
                'unlimited_lives': True,
                'ai_analysis_limit': -1,  # Cheksiz
                'ai_companion_limit': -1,
                'university_exam_limit': -1,
                'mock_exam_limit': -1,
                'certificate_test_limit': -1,
                'icon': 'bi-star-fill',
                'color': '#8b5cf6',
                'badge_text': 'Mashhur',
                'is_popular': True,
                'is_active': True,
                'order': 2
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {pro.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'- Already exists: {pro.name}'))
        
        # Premium Plan
        premium, created = SubscriptionPlan.objects.get_or_create(
            slug='premium',
            defaults={
                'name': 'EduSelf Premium',
                'description': 'Maksimal imkoniyatlar va ustunliklar',
                'price': 149000,
                'duration_days': 90,
                'unlimited_lives': True,
                'ai_analysis_limit': -1,
                'ai_companion_limit': -1,
                'university_exam_limit': -1,
                'mock_exam_limit': -1,
                'certificate_test_limit': -1,
                'icon': 'bi-gem',
                'color': '#f59e0b',
                'badge_text': 'Premium',
                'is_popular': False,
                'is_active': True,
                'order': 3
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {premium.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'- Already exists: {premium.name}'))
        
        # Referral Program
        self.stdout.write('\nCreating referral programs...')
        
        ref_basic, created = ReferralProgram.objects.get_or_create(
            name='Basic Referral',
            plan=basic,
            defaults={
                'required_referrals': 3,
                'referral_deadline_days': 30,
                'reward_duration_days': 30,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {ref_basic.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'- Already exists: {ref_basic.name}'))
        
        ref_pro, created = ReferralProgram.objects.get_or_create(
            name='Pro Referral',
            plan=pro,
            defaults={
                'required_referrals': 5,
                'referral_deadline_days': 30,
                'reward_duration_days': 30,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {ref_pro.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'- Already exists: {ref_pro.name}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Visit /subscriptions/pro/ to see plans')
        self.stdout.write('2. Create promo codes in admin panel')
        self.stdout.write('3. Test payment integration')
