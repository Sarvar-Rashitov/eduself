"""
Loop'lardagi elementlarga translation qo'shish
"""
import os
import re

templates_dir = 'templates/core'
templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

# Loop patterns
patterns = [
    # For loops - subjects
    (r'{{ subject\.name }}', r'{{ subject.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ subject\.description }}', r'{{ subject.description|translate:request.LANGUAGE_CODE }}'),
    
    # For loops - topics
    (r'{{ topic\.name }}', r'{{ topic.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ topic\.description }}', r'{{ topic.description|translate:request.LANGUAGE_CODE }}'),
    
    # For loops - certificates
    (r'{{ certificate\.name }}', r'{{ certificate.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ certificate\.description }}', r'{{ certificate.description|translate:request.LANGUAGE_CODE }}'),
    
    # For loops - tests/exams
    (r'{{ test\.title }}', r'{{ test.title|translate:request.LANGUAGE_CODE }}'),
    (r'{{ exam\.title }}', r'{{ exam.title|translate:request.LANGUAGE_CODE }}'),
    
    # For loops - institutions
    (r'{{ institution\.name }}', r'{{ institution.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ inst\.name }}', r'{{ inst.name|translate:request.LANGUAGE_CODE }}'),
    
    # For loops - directions
    (r'{{ direction\.name }}', r'{{ direction.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ dir\.name }}', r'{{ dir.name|translate:request.LANGUAGE_CODE }}'),
    
    # For loops - categories
    (r'{{ category\.name }}', r'{{ category.name|translate:request.LANGUAGE_CODE }}'),
    (r'{{ cat\.name }}', r'{{ cat.name|translate:request.LANGUAGE_CODE }}'),
    
    # Questions in loops
    (r'{{ q\.text }}', r'{{ q.text|translate:request.LANGUAGE_CODE }}'),
    (r'{{ question\.text }}', r'{{ question.text|translate:request.LANGUAGE_CODE }}'),
    
    # Answers in loops
    (r'{{ answer\.text }}', r'{{ answer.text|translate:request.LANGUAGE_CODE }}'),
    (r'{{ a\.text }}', r'{{ a.text|translate:request.LANGUAGE_CODE }}'),
]

def process_file(file_path):
    """File'ni qayta ishlash"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Patterns'ni qo'llash
        for pattern, replacement in patterns:
            # Agar allaqachon translate filter bo'lmasa
            if pattern in content and '|translate:request.LANGUAGE_CODE' not in content.replace(replacement, ''):
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
    print("LOOP ELEMENTLARIGA TRANSLATION QO'SHISH")
    print("=" * 70)
    print()
    
    updated_count = 0
    
    for template in sorted(templates):
        file_path = os.path.join(templates_dir, template)
        
        if process_file(file_path):
            print(f"✓ {template}")
            updated_count += 1
    
    print()
    print("=" * 70)
    print(f"TUGADI! Yangilandi: {updated_count} ta template")
    print("=" * 70)

if __name__ == '__main__':
    main()
