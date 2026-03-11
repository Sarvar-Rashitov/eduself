"""
Fanlar description'idagi URL'larni olib tashlash va iconlarni yangilash
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Subject

# Yangilangan icon mapping
subject_icons = {
    # Dasturlash tillari
    'Python': 'bi bi-file-code-fill',
    'JavaScript': 'bi bi-filetype-js',
    'Java': 'bi bi-cup-hot-fill',
    'C++': 'bi bi-code-square',
    'C#': 'bi bi-code-square',
    'C': 'bi bi-code-square',
    'PHP': 'bi bi-filetype-php',
    'Rust': 'bi bi-gear-fill',
    'Swift': 'bi bi-apple',
    'SQL': 'bi bi-database-fill',
    'HTML': 'bi bi-filetype-html',
    'CSS': 'bi bi-filetype-css',
    'Go': 'bi bi-code-slash',
    'Kotlin': 'bi bi-code-square',
    'Dart': 'bi bi-code-square',
    
    # Tools
    'Docker': 'bi bi-box-seam',
    'Git': 'bi bi-git',
    'Linux': 'bi bi-terminal-fill',
    'CMD': 'bi bi-terminal',
    'NumPy': 'bi bi-calculator-fill',
    'Matplotlib': 'bi bi-graph-up',
    
    # Fanlar
    'Matematika': 'bi bi-calculator-fill',
    'Fizika': 'bi bi-lightning-fill',
    'Kimyo': 'bi bi-droplet-fill',
    'Biologiya': 'bi bi-flower1',
    'Astronomiya': 'bi bi-moon-stars-fill',
    'Ingliz tili': 'bi bi-translate',
    'Rus tili': 'bi bi-book-fill',
    'Informatika': 'bi bi-laptop-fill',
    'Texnologiya': 'bi bi-gear-wide-connected',
    'Gidrologiya': 'bi bi-droplet-half',
    'Iqtisodiyot': 'bi bi-graph-up-arrow',
    'Geografiya': 'bi bi-globe-americas',
}

def clean_descriptions_and_update_icons():
    """Description'larni tozalash va iconlarni yangilash"""
    
    print("=" * 70)
    print("FANLAR DESCRIPTION'LARINI TOZALASH VA ICONLARNI YANGILASH")
    print("=" * 70)
    
    cleaned_count = 0
    updated_icon_count = 0
    
    for subject in Subject.objects.all():
        updated = False
        
        # Description'dan URL'larni olib tashlash
        if subject.description and 'Logo URL:' in subject.description:
            # URL qismini olib tashlash
            subject.description = subject.description.split('Logo URL:')[0].strip()
            cleaned_count += 1
            updated = True
            print(f"🧹 {subject.name}: Description tozalandi")
        
        # Icon yangilash
        for key, icon in subject_icons.items():
            if key.lower() in subject.name.lower():
                if subject.icon != icon:
                    subject.icon = icon
                    updated_icon_count += 1
                    updated = True
                    print(f"✅ {subject.name}: Icon yangilandi -> {icon}")
                break
        
        if updated:
            subject.save()
    
    print(f"\n✅ Jami {cleaned_count} ta description tozalandi")
    print(f"✅ Jami {updated_icon_count} ta icon yangilandi")
    print("\n💡 Barcha fanlar uchun Bootstrap Icons ishlatildi")

if __name__ == '__main__':
    clean_descriptions_and_update_icons()
