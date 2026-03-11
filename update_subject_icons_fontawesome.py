"""
Fanlar uchun FontAwesome iconlarini qo'yish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from core.models import Subject

# FontAwesome icon mapping - nomiga mos
subject_icons = {
    # Dasturlash tillari
    'Python': 'fab fa-python',
    'JavaScript': 'fab fa-js-square',
    'Java': 'fab fa-java',
    'C++': 'fas fa-code',
    'C#': 'fas fa-code',
    'C': 'fas fa-code',
    'PHP': 'fab fa-php',
    'Rust': 'fab fa-rust',
    'Swift': 'fab fa-swift',
    'SQL': 'fas fa-database',
    'HTML': 'fab fa-html5',
    'CSS': 'fab fa-css3-alt',
    'Go': 'fab fa-golang',
    'Kotlin': 'fab fa-android',
    'Dart': 'fas fa-mobile-alt',
    
    # Tools
    'Docker': 'fab fa-docker',
    'Git': 'fab fa-git-alt',
    'Linux': 'fab fa-linux',
    'CMD': 'fas fa-terminal',
    'NumPy': 'fas fa-square-root-alt',
    'Matplotlib': 'fas fa-chart-line',
    
    # Fanlar
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
    'Geografiya': 'fas fa-globe-americas',
}

def update_icons_to_fontawesome():
    """Barcha fanlar uchun FontAwesome iconlarini qo'yish"""
    
    print("=" * 70)
    print("FANLAR UCHUN FONTAWESOME ICONLARINI QO'YISH")
    print("=" * 70)
    
    updated_count = 0
    not_found = []
    
    for subject in Subject.objects.all():
        icon_found = False
        
        # Icon topish
        for key, icon in subject_icons.items():
            if key.lower() in subject.name.lower():
                if subject.icon != icon:
                    old_icon = subject.icon
                    subject.icon = icon
                    subject.save()
                    print(f"✅ {subject.name}: {old_icon} -> {icon}")
                    updated_count += 1
                else:
                    print(f"✓  {subject.name}: {icon} (o'zgarishsiz)")
                icon_found = True
                break
        
        if not icon_found:
            not_found.append(subject.name)
            # Default icon qo'yish
            if 'fas fa-' not in subject.icon and 'fab fa-' not in subject.icon:
                subject.icon = 'fas fa-book'
                subject.save()
                print(f"⚠️  {subject.name}: Default icon (fas fa-book)")
    
    print(f"\n✅ Jami {updated_count} ta icon yangilandi")
    
    if not_found:
        print(f"\n⚠️  Quyidagi fanlar uchun maxsus icon topilmadi (default icon qo'yildi):")
        for name in not_found:
            print(f"   - {name}")
    
    print("\n💡 Barcha fanlar uchun FontAwesome Icons ishlatildi")
    print("   - fab fa-* : Brand icons (Python, Java, Docker, etc.)")
    print("   - fas fa-* : Solid icons (calculator, atom, flask, etc.)")

if __name__ == '__main__':
    update_icons_to_fontawesome()
