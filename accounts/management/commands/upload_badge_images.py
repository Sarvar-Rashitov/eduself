from django.core.management.base import BaseCommand
from accounts.models import Badge
from django.core.files import File
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Upload badge images from static folder to database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Uploading badge images...'))
        
        # Badge image mapping
        badge_images = {
            'Level 1': 'level-1.png',
            'Level 5': 'level-5.png',
            'Level 10': 'level-10.png',
            'Level 20': 'level-20.png',
            'Level 30': 'level-30.png',
            'Level 40': 'level-40.png',
            '5 Day Streak': '5-day.png',
            '7 Day Streak': '7-day.png',
            '15 Day Streak': '15-day.png',
        }
        
        badges_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'bagee')
        
        if not os.path.exists(badges_dir):
            self.stdout.write(self.style.ERROR(f'❌ Badge images folder not found: {badges_dir}'))
            return
        
        for badge_name, image_filename in badge_images.items():
            try:
                badge = Badge.objects.get(name=badge_name)
                image_path = os.path.join(badges_dir, image_filename)
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        badge.image.save(image_filename, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'✓ Uploaded image for: {badge_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️  Image not found: {image_path}'))
            except Badge.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠️  Badge not found: {badge_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error uploading {badge_name}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Badge images upload complete!'))
