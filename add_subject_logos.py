"""
Fanlar uchun logolar qo'shish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Subject

# Fan logolari mapping
subject_logos = {
    'Python': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg',
    'JavaScript': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg',
    'Java': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg',
    'C++': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/cplusplus/cplusplus-original.svg',
    'C#': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/csharp/csharp-original.svg',
    'C': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg',
    'PHP': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg',
    'Rust': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-plain.svg',
    'Swift': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/swift/swift-original.svg',
    'SQL': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg',
    'HTML': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg',
    'CSS': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg',
    'Go': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original.svg',
    'Kotlin': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kotlin/kotlin-original.svg',
    'Dart': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dart/dart-original.svg',
    'Docker': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg',
    'Git': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg',
    'Linux': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg',
    'NumPy': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg',
    'Matplotlib': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/matplotlib/matplotlib-original.svg',
}

# Icon mapping for subjects without logos
subject_icons = {
    'Matematika': 'fas fa-calculator',
    'Fizika': 'fas fa-atom',
    'Kimyo': 'fas fa-flask',
    'Biologiya': 'fas fa-dna',
    'Astronomiya': 'fas fa-moon',
    'Ingliz tili': 'fas fa-language',
    'Rus tili': 'fas fa-book',
    'Informatika': 'fas fa-laptop-code',
    'Texnologiya': 'fas fa-cogs',
    'Gidrologiya': 'fas fa-water',
    'Iqtisodiyot': 'fas fa-chart-line',
    'Geografiya': 'fas fa-globe',
}

def update_subject_icons():
    """Fanlar uchun iconlarni yangilash"""
    
    print("=" * 70)
    print("FANLAR UCHUN ICONLARNI YANGILASH")
    print("=" * 70)
    
    updated_count = 0
    
    for subject in Subject.objects.all():
        # Icon yangilash
        for key, icon in subject_icons.items():
            if key.lower() in subject.name.lower():
                subject.icon = icon
                subject.save()
                print(f"✅ {subject.name}: {icon}")
                updated_count += 1
                break
        
        # Logo URL'larini description'ga qo'shish (kelajakda image field'ga yuklash mumkin)
        for key, logo_url in subject_logos.items():
            if key.lower() in subject.name.lower():
                if not subject.description or logo_url not in subject.description:
                    subject.description = f"{subject.description}\n\nLogo URL: {logo_url}".strip()
                    subject.save()
                    print(f"📷 {subject.name}: Logo URL qo'shildi")
                    updated_count += 1
                break
    
    print(f"\n✅ Jami {updated_count} ta fan yangilandi")
    print("\n💡 Logo URL'larni description'dan olib, image field'ga yuklash uchun:")
    print("   1. Logo URL'larni description'dan ko'chirib oling")
    print("   2. Rasmlarni yuklab oling")
    print("   3. Django admin orqali image field'ga yuklang")

if __name__ == '__main__':
    update_subject_icons()
