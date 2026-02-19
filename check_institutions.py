import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Institution

featured = Institution.objects.filter(is_featured=True, is_active=True)
print(f'Featured institutions count: {featured.count()}')
print('\nFeatured institutions:')
for i in featured:
    print(f'  - {i.name}')

print(f'\nTotal active institutions: {Institution.objects.filter(is_active=True).count()}')
