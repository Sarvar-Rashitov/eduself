# Badge Rasmlarini Yuklash Yo'riqnomasi

## 1. Gamification Tizimini Sozlash

Barcha levellar va badge'larni yaratish uchun:

```bash
python manage.py setup_gamification
```

Bu command quyidagilarni yaratadi:
- ✅ Level 0 (Beginner) - 0 XP
- ✅ Level 1 - 1,000 XP
- ✅ Level 5 - 5,000 XP
- ✅ Level 10 - 10,000 XP
- ✅ Level 20 - 20,000 XP
- ✅ Level 30 - 30,000 XP
- ✅ Level 40 - 40,000 XP
- ✅ 5 Day Streak Badge
- ✅ 7 Day Streak Badge
- ✅ 15 Day Streak Badge

## 2. Badge Rasmlarini Yuklash

### Avtomatik Yuklash (Local'dan)

Agar badge rasmlari `static/images/bagee/` papkasida bo'lsa:

```bash
python manage.py upload_badge_images
```

Bu command rasmlarni avtomatik Cloudflare R2'ga yuklaydi.

### Qo'lda Yuklash (Admin Panel)

1. Admin panelga kiring: `/admin/`
2. **Badges** bo'limiga o'ting
3. Har bir badge'ni tahrirlang
4. **Image** maydoniga rasm yuklang
5. **Save** tugmasini bosing

Badge rasmlari avtomatik Cloudflare R2'ga yuklanadi va URL avtomatik yaratiladi.

## 3. Badge Rasmlari Joylashuvi

Badge rasmlari quyidagi joyda saqlanadi:
- **Local development**: `media/badges/`
- **Production**: Cloudflare R2 bucket'da `media/badges/`

## 4. Yangi Badge Qo'shish

Admin panelda yangi badge qo'shish:

1. `/admin/accounts/badge/add/` ga o'ting
2. Badge ma'lumotlarini kiriting:
   - **Name**: Badge nomi (masalan: "Level 50")
   - **Description**: Tavsif
   - **Badge type**: Level/Streak/Achievement/Special
   - **Image**: Badge rasmi (PNG/JPG)
   - **Order**: Tartib raqami

3. Badge turiga qarab kerakli maydonlarni to'ldiring:
   - **Level Badge**: Required level tanlang
   - **Streak Badge**: Required streak days kiriting
   - **Achievement Badge**: Required XP yoki tests kiriting

4. **Save** tugmasini bosing

## 5. Yangi Level Qo'shish

Admin panelda yangi level qo'shish:

1. `/admin/accounts/level/add/` ga o'ting
2. Level ma'lumotlarini kiriting:
   - **Name**: Level nomi (masalan: "Level 50")
   - **Level number**: Level raqami (masalan: 50)
   - **Required XP**: Kerakli XP (masalan: 50000)
   - **Icon**: Level ikonkasi (ixtiyoriy)
   - **Color**: Level rangi (hex format, masalan: #6366f1)
   - **Description**: Tavsif

3. **Save** tugmasini bosing

## 6. Foydalanuvchiga Badge Berish

Admin qo'lda badge berishi mumkin:

1. `/admin/accounts/userbadge/add/` ga o'ting
2. **User** va **Badge** tanlang
3. **Save** tugmasini bosing

## 7. Tekshirish

Badge'lar to'g'ri ishlayotganini tekshirish:

1. Profil sahifasiga o'ting
2. Gamification bo'limida badge'lar ko'rinishi kerak
3. Ochilgan badge'lar rangli, qulflangan badge'lar kulrang bo'lishi kerak

## 8. Badge Rasmlari Formatlari

Tavsiya etilgan format:
- **Format**: PNG (shaffof fon bilan)
- **O'lcham**: 256x256 px yoki 512x512 px
- **Fayl hajmi**: 100 KB dan kam
- **Rang**: To'liq rangli (ochilgan badge'lar uchun)

## 9. Muammolarni Hal Qilish

### Badge rasmlari ko'rinmayapti

1. Cloudflare R2 sozlamalarini tekshiring (`.env` fayl)
2. `MEDIA_URL` to'g'ri sozlanganini tekshiring
3. Badge'da rasm yuklanganini admin paneldan tekshiring

### Badge ochilmayapti

1. Badge shartlarini tekshiring (required_xp, required_level, va h.k.)
2. Foydalanuvchining XP va streak'ini tekshiring
3. Badge `is_active=True` ekanligini tekshiring

### Yangi badge ko'rinmayapti

1. Badge `is_active=True` ekanligini tekshiring
2. Badge `order` maydonini to'g'ri sozlang
3. Sahifani yangilang (Ctrl+F5)

## 10. Cloudflare R2 Sozlamalari

`.env` faylida quyidagi sozlamalar bo'lishi kerak:

```env
USE_S3=True
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
AWS_S3_CUSTOM_DOMAIN=your-custom-domain.com
```

## 11. Badge Tizimi Arxitekturasi

```
User (0 XP) → Level 0 (Beginner)
User (1000 XP) → Level 1 Badge ochiladi
User (5000 XP) → Level 5 Badge ochiladi
User (5 kun streak) → 5 Day Streak Badge ochiladi
```

Badge'lar avtomatik ochiladi:
- Foydalanuvchi XP olganida
- Foydalanuvchi streak'ini oshirganida
- Test topshirganida

## 12. Foydali Commandlar

```bash
# Gamification tizimini sozlash
python manage.py setup_gamification

# Badge rasmlarini yuklash
python manage.py upload_badge_images

# Barcha foydalanuvchilarning badge'larini yangilash
python manage.py shell
>>> from accounts.models import User
>>> for user in User.objects.all():
...     user.check_and_unlock_badges()
...     user.update_level()
```

## 13. Xavfsizlik

- Badge rasmlarini faqat admin yuklashi mumkin
- Foydalanuvchilar badge'larni o'zlari qo'sha olmaydi
- Badge shartlari backend'da tekshiriladi
- XP va streak manipulyatsiyasi oldini olish uchun validatsiya bor
