"""
Home sahifasiga tarjimalarni qo'llash
"""
import re

# Home.html faylini o'qish
with open('templates/core/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Tarjima qilish kerak bo'lgan matnlar va ularning joylashuvi
replacements = [
    # Hero section
    ('O\'zbekiston #1 Ta\'lim Platformasi', '{% t "O\'zbekiston #1 Ta\'lim Platformasi" request.LANGUAGE_CODE %}'),
    ('EduSelf bilan o\'z kelajagingizni quring', '{% t "EduSelf bilan o\'z kelajagingizni quring" request.LANGUAGE_CODE %}'),
    ('AI yordamchi, 10,000+ test savollari, sertifikatlar va eng yaxshi ta\'lim muassasalari haqida to\'liq ma\'lumot', 
     '{% t "AI yordamchi, 10,000+ test savollari, sertifikatlar va eng yaxshi ta\'lim muassasalari haqida to\'liq ma\'lumot" request.LANGUAGE_CODE %}'),
    
    # Features
    ('<h4>AI Hamroh</h4>', '<h4>{% t "AI Hamroh" request.LANGUAGE_CODE %}</h4>'),
    ('<p>24/7 shaxsiy yordamchi</p>', '<p>{% t "24/7 shaxsiy yordamchi" request.LANGUAGE_CODE %}</p>'),
    ('<h4>Gamefikatsiya</h4>', '<h4>{% t "Gamefikatsiya" request.LANGUAGE_CODE %}</h4>'),
    ('<p>Ball to\'plang, raqobatlashing</p>', '<p>{% t "Ball to\'plang, raqobatlashing" request.LANGUAGE_CODE %}</p>'),
    ('<h4>Progress Tracking</h4>', '<h4>{% t "Progress Tracking" request.LANGUAGE_CODE %}</h4>'),
    ('<p>Rivojlanishingizni kuzating</p>', '<p>{% t "Rivojlanishingizni kuzating" request.LANGUAGE_CODE %}</p>'),
    ('<p>Bilimingizni tasdiqlang</p>', '<p>{% t "Bilimingizni tasdiqlang" request.LANGUAGE_CODE %}</p>'),
    
    # Buttons
    ('<span>Bepul Boshlash</span>', '<span>{% t "Bepul Boshlash" request.LANGUAGE_CODE %}</span>'),
    
    # Stats
    ('<div class="stat-preview-label">Foydalanuvchilar</div>', 
     '<div class="stat-preview-label">{% t "Foydalanuvchilar" request.LANGUAGE_CODE %}</div>'),
    ('<div class="stat-preview-label">Test Savollari</div>', 
     '<div class="stat-preview-label">{% t "Test Savollari" request.LANGUAGE_CODE %}</div>'),
    ('<div class="stat-preview-label">Sertifikatlar</div>', 
     '<div class="stat-preview-label">{% t "Sertifikatlar" request.LANGUAGE_CODE %}</div>'),
    
    # Dashboard
    ('<h1 class="stats-greeting">Salom,', '<h1 class="stats-greeting">{% t "Salom" request.LANGUAGE_CODE %},'),
    ('<div class="quick-stat-label">Testlar</div>', 
     '<div class="quick-stat-label">{% t "Testlar" request.LANGUAGE_CODE %}</div>'),
    ('<div class="quick-stat-label">Ballar</div>', 
     '<div class="quick-stat-label">{% t "Ballar" request.LANGUAGE_CODE %}</div>'),
    
    # Test results
    ('<h3>Oxirgi Test</h3>', '<h3>{% t "Oxirgi Test" request.LANGUAGE_CODE %}</h3>'),
    ('<i class="bi bi-check-circle-fill text-success"></i> O\'tdingiz', 
     '<i class="bi bi-check-circle-fill text-success"></i> {% t "O\'tdingiz" request.LANGUAGE_CODE %}'),
    ('<i class="bi bi-x-circle-fill text-danger"></i> O\'tmadingiz', 
     '<i class="bi bi-x-circle-fill text-danger"></i> {% t "O\'tmadingiz" request.LANGUAGE_CODE %}'),
    ('<span>Tahlil Ko\'rish</span>', '<span>{% t "Tahlil Ko\'rish" request.LANGUAGE_CODE %}</span>'),
    ('<span>Keyingi Testni Boshlash</span>', '<span>{% t "Keyingi Testni Boshlash" request.LANGUAGE_CODE %}</span>'),
    ('<span>Qayta Urinish</span>', '<span>{% t "Qayta Urinish" request.LANGUAGE_CODE %}</span>'),
    
    # Certificate test
    ('<h3>Oxirgi Sertifikat Testi</h3>', '<h3>{% t "Oxirgi Sertifikat Testi" request.LANGUAGE_CODE %}</h3>'),
    
    # AI Assistant
    ('<h3>AI Hamroh</h3>', '<h3>{% t "AI Hamroh" request.LANGUAGE_CODE %}</h3>'),
    ('<p>Savollaringizga javob oling, tavsiyalar oling</p>', 
     '<p>{% t "Savollaringizga javob oling, tavsiyalar oling" request.LANGUAGE_CODE %}</p>'),
    ('<span>Suhbat Boshlash</span>', '<span>{% t "Suhbat Boshlash" request.LANGUAGE_CODE %}</span>'),
    
    # Platform features
    ('Platformaning Imkoniyatlari', '{% t "Platformaning Imkoniyatlari" request.LANGUAGE_CODE %}'),
    ('<h3>Online Kurslar</h3>', '<h3>{% t "Online Kurslar" request.LANGUAGE_CODE %}</h3>'),
    ('<p>Video darslar</p>', '<p>{% t "Video darslar" request.LANGUAGE_CODE %}</p>'),
    ('<p>Barcha fanlar</p>', '<p>{% t "Barcha fanlar" request.LANGUAGE_CODE %}</p>'),
    ('<h3>Mock Imtihonlar</h3>', '<h3>{% t "Mock Imtihonlar" request.LANGUAGE_CODE %}</h3>'),
    ('<p>Real tajriba</p>', '<p>{% t "Real tajriba" request.LANGUAGE_CODE %}</p>'),
    ('<p>Universitet va maktablar</p>', '<p>{% t "Universitet va maktablar" request.LANGUAGE_CODE %}</p>'),
    ('<p>Top o\'quvchilar</p>', '<p>{% t "Top o\'quvchilar" request.LANGUAGE_CODE %}</p>'),
    
    # Sections
    ('Tavsiya Etamiz', '{% t "Tavsiya Etamiz" request.LANGUAGE_CODE %}'),
    ('Ta\'lim Muassasalari', '{% t "Ta\'lim Muassasalari" request.LANGUAGE_CODE %}'),
    ('Fanlar', '{% t "Fanlar" request.LANGUAGE_CODE %}'),
    ('Top Reyting', '{% t "Top Reyting" request.LANGUAGE_CODE %}'),
    
    # Partners
    ('Bizga Ishonadigan Hamkorlar', '{% t "Bizga Ishonadigan Hamkorlar" request.LANGUAGE_CODE %}'),
    
    # Footer
    ('O\'zbekistonda ta\'limni rivojlantirish platformasi', 
     '{% t "O\'zbekistonda ta\'limni rivojlantirish platformasi" request.LANGUAGE_CODE %}'),
    ('<h4 class="footer-title" style="font-size: 0.8rem;">Platformamiz</h4>', 
     '<h4 class="footer-title" style="font-size: 0.8rem;">{% t "Platformamiz" request.LANGUAGE_CODE %}</h4>'),
    ('<h4 class="footer-title" style="font-size: 0.8rem;">Bog\'lanish</h4>', 
     '<h4 class="footer-title" style="font-size: 0.8rem;">{% t "Bog\'lanish" request.LANGUAGE_CODE %}</h4>'),
    ('<h4 class="footer-title" style="font-size: 0.8rem;">Ijtimoiy tarmoqlar</h4>', 
     '<h4 class="footer-title" style="font-size: 0.8rem;">{% t "Ijtimoiy tarmoqlar" request.LANGUAGE_CODE %}</h4>'),
    ('Barcha huquqlar himoyalangan', '{% t "Barcha huquqlar himoyalangan" request.LANGUAGE_CODE %}'),
    
    # Leaderboard
    ('Sizning o\'rningiz:', '{% t "Sizning o\'rningiz" request.LANGUAGE_CODE %}:'),
    (' ball</span>', ' {% t "ball" request.LANGUAGE_CODE %}</span>'),
    (' test</p>', ' {% t "test" request.LANGUAGE_CODE %}</p>'),
    (' yo\'nalish', ' {% t "yo\'nalish" request.LANGUAGE_CODE %}'),
    (' mavzu • ', ' {% t "mavzu" request.LANGUAGE_CODE %} • '),
    (' savol</p>', ' {% t "savol" request.LANGUAGE_CODE %}</p>'),
]

# Almashtirishlarni qo'llash
changes = 0
for old, new in replacements:
    if old in content and new not in content:
        content = content.replace(old, new)
        changes += 1
        print(f"✓ Almashtirildi: {old[:50]}...")

# Faylni saqlash
with open('templates/core/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✓ Jami {changes} ta o'zgarish amalga oshirildi!")
