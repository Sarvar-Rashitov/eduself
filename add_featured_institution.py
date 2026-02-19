import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Institution

# Barcha active institutionlarni ko'rish
all_institutions = Institution.objects.filter(is_active=True)
print('All active institutions:')
for i in all_institutions:
    print(f'  {i.id}. {i.name} - Featured: {i.is_featured}')

# Birinchi featured bo'lmagan muassasani featured qilish
non_featured = Institution.objects.filter(is_active=True, is_featured=False).first()
if non_featured:
    non_featured.is_featured = True
    non_featured.save()
    print(f'\n✓ {non_featured.name} featured qilindi!')
else:
    print('\nFeatured bo\'lmagan muassasa topilmadi.')

# Natijani ko'rish
featured = Institution.objects.filter(is_featured=True, is_active=True)
print(f'\nFeatured institutions count: {featured.count()}')
for i in featured:
    print(f'  - {i.name}')
