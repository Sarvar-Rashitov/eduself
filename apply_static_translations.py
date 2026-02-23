"""
Barcha template'larga statik tarjimalarni avtomatik qo'llash
"""
import os
import re
import json

# Statik tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    TRANSLATIONS = json.load(f)

templates_dir = 'templates/core'
templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

def apply_translations(file_path):
    """Template'ga statik tarjimalarni qo'llash"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Har bir statik matn uchun
        for uz_text in TRANSLATIONS.keys():
            # Agar matn allaqachon tarjima qilinmagan bo'lsa
            t_tag = '{{% t "{}" request.LANGUAGE_CODE %}}'.format(uz_text)
            if uz_text in content and t_tag not in content:
                # Pattern'lar
                t_replacement = '{{% t "{}" request.LANGUAGE_CODE %}}'.format(uz_text)
                patterns = [
                    # <h1>Matn</h1> -> <h1>{% t "Matn" request.LANGUAGE_CODE %}</h1>
                    (r'(<h[1-6][^>]*>)\s*' + re.escape(uz_text) + r'\s*(</h[1-6]>)',
                     r'\1' + t_replacement + r'\2'),
                    
                    # <button>Matn</button> -> <button>{% t "Matn" request.LANGUAGE_CODE %}</button>
                    (r'(<button[^>]*>)\s*' + re.escape(uz_text) + r'\s*(</button>)',
                     r'\1' + t_replacement + r'\2'),
                    
                    # <a>Matn</a> -> <a>{% t "Matn" request.LANGUAGE_CODE %}</a>
                    (r'(<a[^>]*>)\s*' + re.escape(uz_text) + r'\s*(</a>)',
                     r'\1' + t_replacement + r'\2'),
                    
                    # <span>Matn</span> -> <span>{% t "Matn" request.LANGUAGE_CODE %}</span>
                    (r'(<span[^>]*>)\s*' + re.escape(uz_text) + r'\s*(</span>)',
                     r'\1' + t_replacement + r'\2'),
                    
                    # <p>Matn</p> -> <p>{% t "Matn" request.LANGUAGE_CODE %}</p>
                    (r'(<p[^>]*>)\s*' + re.escape(uz_text) + r'\s*(</p>)',
                     r'\1' + t_replacement + r'\2'),
                    
                    # <label>Matn</label> -> <label>{% t "Matn" request.LANGUAGE_CODE %}</label>
                    (r'(<label[^>]*>)\s*' + re.escape(uz_text) + r'\s*(</label>)',
                     r'\1' + t_replacement + r'\2'),
                    
                    # >Matn< -> >{% t "Matn" request.LANGUAGE_CODE %}<
                    (r'(>)\s*' + re.escape(uz_text) + r'\s*(<)',
                     r'\1' + t_replacement + r'\2'),
                ]
                
                for pattern, replacement in patterns:
                    new_content = re.sub(pattern, replacement, content)
                    if new_content != content:
                        content = new_content
                        changes += 1
                        break
        
        # Agar o'zgarish bo'lsa, saqlash
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        
        return 0
    
    except Exception as e:
        print(f"✗ {file_path} - xato: {str(e)}")
        return 0

def main():
    print("=" * 70)
    print("STATIK TARJIMALARNI BARCHA TEMPLATE'LARGA QO'LLASH")
    print("=" * 70)
    print()
    
    total_changes = 0
    updated_files = 0
    
    for template in sorted(templates):
        file_path = os.path.join(templates_dir, template)
        changes = apply_translations(file_path)
        
        if changes > 0:
            print(f"✓ {template} - {changes} ta o'zgarish")
            total_changes += changes
            updated_files += 1
        else:
            print(f"○ {template}")
    
    print()
    print("=" * 70)
    print(f"TUGADI!")
    print(f"Yangilangan fayllar: {updated_files}")
    print(f"Jami o'zgarishlar: {total_changes}")
    print("=" * 70)

if __name__ == '__main__':
    main()
