"""
Barcha template'larga translation tags qo'shish
"""
import os
import re

# Template'lar ro'yxati
templates = [
    'templates/core/course_detail.html',
    'templates/core/lesson_detail.html',
    'templates/core/news_detail.html',
    'templates/core/subjects.html',
    'templates/core/subject_detail.html',
    'templates/core/institutions.html',
    'templates/core/institution_detail.html',
    'templates/core/home.html',
]

def add_translation_tags(file_path):
    """Template'ga translation tags qo'shish"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Agar allaqachon translation_tags yuklangan bo'lsa, o'tkazib yuborish
        if '{% load translation_tags %}' in content:
            print(f"✓ {file_path} - allaqachon translation_tags yuklangan")
            return
        
        # {% extends %} dan keyin {% load translation_tags %} qo'shish
        if '{% extends' in content:
            content = re.sub(
                r"({% extends ['\"].*?['\"] %})",
                r"\1\n{% load translation_tags %}",
                content,
                count=1
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ {file_path} - translation_tags qo'shildi")
        else:
            print(f"✗ {file_path} - {{% extends %}} topilmadi")
    
    except FileNotFoundError:
        print(f"✗ {file_path} - fayl topilmadi")
    except Exception as e:
        print(f"✗ {file_path} - xato: {str(e)}")

def main():
    print("=" * 60)
    print("TRANSLATION TAGS QO'SHISH")
    print("=" * 60)
    print()
    
    for template in templates:
        add_translation_tags(template)
    
    print()
    print("=" * 60)
    print("TUGADI!")
    print("=" * 60)
    print()
    print("Keyingi qadam: Har bir template'da dinamik kontentga")
    print("|translate:request.LANGUAGE_CODE filter qo'shing")
    print()
    print("Misol:")
    print("  {{ course.title|translate:request.LANGUAGE_CODE }}")
    print("  {{ news.description|translate:request.LANGUAGE_CODE }}")

if __name__ == '__main__':
    main()
