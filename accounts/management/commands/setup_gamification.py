from django.core.management.base import BaseCommand
from accounts.models import Level, Badge
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup initial gamification levels and badges'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up gamification system...'))
        
        # Create Levels
        levels_data = [
            {'name': 'Beginner', 'level_number': 0, 'required_xp': 0, 'color': '#94a3b8', 'description': 'Boshlang\'ich daraja'},
            {'name': 'Level 1', 'level_number': 1, 'required_xp': 1000, 'color': '#10b981', 'description': 'Birinchi level'},
            {'name': 'Level 5', 'level_number': 5, 'required_xp': 5000, 'color': '#3b82f6', 'description': 'Beshinchi level'},
            {'name': 'Level 10', 'level_number': 10, 'required_xp': 10000, 'color': '#8b5cf6', 'description': 'O\'ninchi level'},
            {'name': 'Level 20', 'level_number': 20, 'required_xp': 20000, 'color': '#ec4899', 'description': 'Yigirmanchi level'},
            {'name': 'Level 30', 'level_number': 30, 'required_xp': 30000, 'color': '#f59e0b', 'description': 'O\'ttizinchi level'},
            {'name': 'Level 40', 'level_number': 40, 'required_xp': 40000, 'color': '#ef4444', 'description': 'Qirqinchi level'},
        ]
        
        for level_data in levels_data:
            level, created = Level.objects.get_or_create(
                level_number=level_data['level_number'],
                defaults={
                    'name': level_data['name'],
                    'required_xp': level_data['required_xp'],
                    'color': level_data['color'],
                    'description': level_data['description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created level: {level.name}'))
            else:
                self.stdout.write(f'  Level {level.name} already exists')
        
        # Create Level Badges
        level_badges_data = [
            {'name': 'Level 1', 'level_number': 1, 'order': 1},
            {'name': 'Level 5', 'level_number': 5, 'order': 2},
            {'name': 'Level 10', 'level_number': 10, 'order': 3},
            {'name': 'Level 20', 'level_number': 20, 'order': 4},
            {'name': 'Level 30', 'level_number': 30, 'order': 5},
            {'name': 'Level 40', 'level_number': 40, 'order': 6},
        ]
        
        for badge_data in level_badges_data:
            level = Level.objects.filter(level_number=badge_data['level_number']).first()
            if level:
                badge, created = Badge.objects.get_or_create(
                    name=badge_data['name'],
                    badge_type='level',
                    defaults={
                        'description': f'{badge_data["name"]} badge - {level.required_xp} XP kerak',
                        'required_level': level,
                        'is_active': True,
                        'order': badge_data['order'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Created badge: {badge.name}'))
                else:
                    self.stdout.write(f'  Badge {badge.name} already exists')
        
        # Create Streak Badges
        streak_badges_data = [
            {'name': '5 Day Streak', 'days': 5, 'order': 7},
            {'name': '7 Day Streak', 'days': 7, 'order': 8},
            {'name': '15 Day Streak', 'days': 15, 'order': 9},
        ]
        
        for badge_data in streak_badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                badge_type='streak',
                defaults={
                    'description': f'{badge_data["days"]} kun ketma-ket o\'qish',
                    'required_streak_days': badge_data['days'],
                    'is_active': True,
                    'order': badge_data['order'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created badge: {badge.name}'))
            else:
                self.stdout.write(f'  Badge {badge.name} already exists')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Gamification setup complete!'))
        self.stdout.write(self.style.WARNING('\n⚠️  Badge rasmlarini admin paneldan yuklashingiz kerak:'))
        self.stdout.write('   /admin/accounts/badge/')
        self.stdout.write('\n📁 Badge rasmlari: static/images/bagee/ papkasida')
