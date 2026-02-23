"""
Barcha core template'larga translation qo'shish
"""
import os
import re

# Barcha core template'lar
templates_dir = 'templates/core'
templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

# Translation patterns
patterns = [
    # Subject/Topic/Certificate names
    (r'{{ subject\.name }}', r'{{ subject.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ topic\.name }}', r'{{ topic.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ certificate\.name }}', r'{{ certificate.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ test\.title }}', r'{{ test.title|translate:request.LANGUAGE_CODE }}'),
    (r'{{ exam\.title }}', r'{{ exam.title|translate:request.LANGUAGE_CODE }}'),
    
    # Descriptions
    (r'{{ subject\.description }}', r'{{ subject.description|translate:request.LANGUAGE_CODE }}'),
    (r'{{ topic\.description }}', r'{{ topic.description|translate:request.LANGUAGE_CODE }}'),
    (r'{{ certificate\.description }}', r'{{ certificate.description|translate:request.LANGUAGE_CODE }}'),
    (r'{{ test\.description }}', r'{{ test.description|translate:request.LANGUAGE_CODE }}'),
    (r'{{ exam\.description }}', r'{{ exam.description|translate:request.LANGUAGE_CODE }}'),
    
    # Institution
    (r'{{ institution\.name }}', r'{{ institution.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ institution\.description }}', r'{{ institution.description|translate:request.LANGUAGE_CODE }}'),
    (r'{{ institution\.short_description }}', r'{{ institution.short_description|translate:request.LANGUAGE_CODE }}'),
    (r'{{ direction\.name }}', r'{{ direction.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ direction\.description }}', r'{{ direction.description|translate:request.LANGUAGE_CODE }}'),
    
    # Category
    (r'{{ category\.name }}', r'{{ category.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ cat\.name }}', r'{{ cat.name|translate:request.LANGUAGE_CODE }}'),
    
    # Questions (with safe)
    (r'{{ question\.text\|safe }}', r'{{ question.text|translate:request.LANGUAGE_CODE|safe }}'),
    (r'{{ question\.explanation\|safe }}', r'{{ question.explanation|translate:request.LANGUAGE_CODE|safe }}'),
]

def add_translation_tags(file_path):
    """Template'ga translation tags qo'shish"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Agar allaqachon translation_tags yuklangan bo'lsa
        if '{% load translation_tags %}' not in content:
            # {% extends %} dan keyin {% load translation_tags %} qo'shish
            if '{% extends' in content:
                content = re.sub(
                    r"({% extends ['\"].*?['\"] %})",
                    r"\1\n{% load translation_tags %}",
                    content,
                    count=1
                )
        
        # Patterns'ni qo'llash
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Agar o'zgarish bo'lsa, saqlash
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"✗ {file_path} - xato: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("BARCHA CORE TEMPLATE'LARGA TRANSLATION QO'SHISH")
    print("=" * 70)
    print()
    
    updated_count = 0
    skipped_count = 0
    
    for template in sorted(templates):
        file_path = os.path.join(templates_dir, template)
        
        if add_translation_tags(file_path):
            print(f"✓ {template} - yangilandi")
            updated_count += 1
        else:
            print(f"○ {template} - o'zgarish yo'q")
            skipped_count += 1
    
    print()
    print("=" * 70)
    print(f"TUGADI! Yangilandi: {updated_count}, O'zgarish yo'q: {skipped_count}")
    print("=" * 70)

if __name__ == '__main__':
    main()
