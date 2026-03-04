# Server'ni Qayta Ishga Tushirish

## 1. Server'ni To'xtatish
Agar server ishlab turgan bo'lsa, `Ctrl+C` bosing

## 2. Browser Cache'ni Tozalash
- Chrome: `Ctrl+Shift+Delete` → Clear browsing data
- Yoki: Hard refresh `Ctrl+Shift+R`

## 3. Server'ni Qayta Ishga Tushirish
```bash
python manage.py runserver
```

## 4. Sahifani Yangilash
- Home sahifasiga o'ting: http://localhost:8000/
- Hard refresh: `Ctrl+Shift+R`

## 5. Tekshirish
- Karuselda 20 ta donat ko'rinishi kerak
- Turli foydalanuvchilar ko'rinishi kerak
- Avtomatik scroll ishlashi kerak
- Manual scroll qilish mumkin bo'lishi kerak

## Agar Hali Ham Muammo Bo'lsa

### Debug Mode
Browser console'ni oching (F12) va quyidagilarni tekshiring:
```javascript
// Donations count
document.querySelectorAll('.donation-card').length

// Should show 40 (20 original + 20 duplicate)
```

### Template Debug
View source (Ctrl+U) va quyidagini qidiring:
```html
<div class="donation-card">
```

Nechta topilganini sanang.

## Muammo: Faqat Bitta Foydalanuvchi Ko'rinadi

Agar faqat bitta foydalanuvchi ko'rinsa:
1. Browser cache'ni tozalang
2. Server'ni qayta ishga tushiring
3. Incognito mode'da ochib ko'ring

## Muammo: Donatlar Ko'rinmayapti

Agar donatlar umuman ko'rinmasa:
```bash
python check_donations.py
```

Agar 0 ta completed donat bo'lsa:
```bash
python complete_all_donations.py
```
