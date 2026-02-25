# Avatar System - Avtomatik Profil Rasmlari

## Qisqacha

Foydalanuvchilar profil rasmini yuklamaganlarida avtomatik ravishda rangli avatarlar ko'rsatiladi. Har bir foydalanuvchi o'zining ID raqamiga asoslangan noyob rangga ega bo'ladi.

## Xususiyatlar

- ✅ Profil rasmini yuklamagan foydalanuvchilar uchun avtomatik avatar
- ✅ Har bir foydalanuvchi uchun noyob rang (8 xil rang)
- ✅ Foydalanuvchi ismi yoki email asosida avatar yaratiladi
- ✅ UI Avatars API dan foydalaniladi
- ✅ Barcha sahifalarda ishlaydi (profil, leaderboard, chat, va h.k.)

## Texnik Tafsilotlar

### User Model - `get_avatar_url()` metodi

```python
def get_avatar_url(self):
    """
    Profil rasmini qaytaradi. Agar foydalanuvchi rasm yuklamagan bo'lsa,
    avtomatik avatar qaytariladi.
    """
    if self.profile_image:
        return self.profile_image.url
    
    # Foydalanuvchi nomi yoki emaildan avatar yaratish
    name = self.get_display_name()
    
    # 8 xil rang
    colors = [
        ('6366f1', 'ffffff'),  # Indigo
        ('8b5cf6', 'ffffff'),  # Purple
        ('ec4899', 'ffffff'),  # Pink
        ('f59e0b', 'ffffff'),  # Amber
        ('10b981', 'ffffff'),  # Emerald
        ('3b82f6', 'ffffff'),  # Blue
        ('ef4444', 'ffffff'),  # Red
        ('14b8a6', 'ffffff'),  # Teal
    ]
    
    # User ID ga asoslangan rang tanlash
    color_index = self.id % len(colors) if self.id else 0
    bg_color, text_color = colors[color_index]
    
    # UI Avatars API
    return f"https://ui-avatars.com/api/?name={name}&background={bg_color}&color={text_color}&size=200&bold=true"
```

### Template'larda Ishlatish

**Eski usul (o'chirildi):**
```django
{% if user.profile_image %}
<img src="{{ user.profile_image.url }}" alt="Profile">
{% else %}
<div class="avatar-placeholder">
    <i class="bi bi-person"></i>
</div>
{% endif %}
```

**Yangi usul:**
```django
<img src="{{ user.get_avatar_url }}" alt="Profile">
```

## Yangilangan Fayllar

### Models
- `accounts/models.py` - `get_avatar_url()` metodi qo'shildi

### Templates
- `templates/accounts/profile.html` - Mobile profil sahifasi
- `templates/accounts/profile_desktop.html` - Desktop profil sahifasi
- `templates/base_desktop.html` - Desktop navigation
- `templates/core/home.html` - Bosh sahifa
- `templates/core/topic_leaderboard.html` - Topic leaderboard (mobile)
- `templates/core/topic_leaderboard_desktop.html` - Topic leaderboard (desktop)
- `templates/core/cert_test_leaderboard.html` - Certificate leaderboard (mobile)
- `templates/core/cert_test_leaderboard_desktop.html` - Certificate leaderboard (desktop)
- `templates/core/mock_exam_leaderboard.html` - Mock exam leaderboard (mobile)
- `templates/core/mock_exam_leaderboard_desktop.html` - Mock exam leaderboard (desktop)
- `templates/core/global_leaderboard_desktop.html` - Global leaderboard
- `templates/ai_assistant/chat.html` - AI chat

## Ranglar

Har bir foydalanuvchi o'zining ID raqamiga asoslangan rangga ega:

1. **Indigo** (#6366f1) - ID % 8 = 0
2. **Purple** (#8b5cf6) - ID % 8 = 1
3. **Pink** (#ec4899) - ID % 8 = 2
4. **Amber** (#f59e0b) - ID % 8 = 3
5. **Emerald** (#10b981) - ID % 8 = 4
6. **Blue** (#3b82f6) - ID % 8 = 5
7. **Red** (#ef4444) - ID % 8 = 6
8. **Teal** (#14b8a6) - ID % 8 = 7

## Afzalliklari

- ✅ Foydalanuvchilar profil rasmini yuklashga majbur emas
- ✅ Har bir foydalanuvchi vizual jihatdan farqlanadi
- ✅ Tizim avtomatik ishlaydi
- ✅ Kod sodda va tushunarli
- ✅ Barcha sahifalarda bir xil ko'rinish

## Kelajakda Qo'shilishi Mumkin

- [ ] Foydalanuvchi o'zi avatar rangini tanlashi
- [ ] Lokal avatar rasmlari (offline ishlash uchun)
- [ ] Avatar generatorni o'zgartirish (boshqa API yoki lokal)
- [ ] Avatar'ga badge yoki status qo'shish

## Test Qilish

```bash
python manage.py shell
```

```python
from accounts.models import User

# Birinchi foydalanuvchini olish
user = User.objects.first()

# Avatar URL ni ko'rish
print(user.get_avatar_url())

# Profil rasmini o'chirish va qayta tekshirish
user.profile_image = None
user.save()
print(user.get_avatar_url())  # Avtomatik avatar ko'rsatiladi
```

## Deployment

Static fayllarni yig'ish:
```bash
python manage.py collectstatic --noinput --clear
```

Server'ni qayta ishga tushirish kerak emas - template o'zgarishlari darhol ko'rinadi.
