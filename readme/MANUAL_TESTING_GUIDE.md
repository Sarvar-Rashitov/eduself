# Lives System - Manual Testing Guide

## Server Ishga Tushirish

Server allaqachon ishlamoqda: http://127.0.0.1:8000/

## Test Qadamlari

### 1. Admin Panel Tekshirish

1. Admin panelga kiring: http://127.0.0.1:8000/admin/
2. "Lives sozlamalari" bo'limiga o'ting
3. Sozlamalarni ko'ring:
   - Kunlik yurakchalar: 5
   - Maksimal yurakchalar: 5
   - Tiklanish vaqti: 30 daqiqa
   - Yo'qotish: 1
   - O'tish foizi: 70%
   - Faol: ✓

### 2. Header Lives Display

1. Bosh sahifaga o'ting: http://127.0.0.1:8000/
2. Header'da yurakchalar ko'rinishini tekshiring:
   - ❤️❤️❤️❤️❤️ (5 ta to'liq yurakcha)
   - Gradient pink background
   - Animated hearts (pulse effect)

### 3. Profil Sahifasi

1. Profil sahifasiga o'ting: http://127.0.0.1:8000/accounts/profile/
2. Lives card'ni tekshiring:
   - "Yurakchalar" sarlavhasi
   - Lives count: 5 / 5
   - Animated hearts
   - "Har kuni yangi yurakchalar beriladi" xabari

### 4. Test Ishlash

#### Test 1: Muvaffaqiyatli Test
1. Biror test sahifasiga o'ting
2. Testni boshlang
3. Barcha savollarga to'g'ri javob bering (70% dan yuqori)
4. Natija: Lives o'zgarmaydi ✅

#### Test 2: Muvaffaqiyatsiz Test
1. Biror test sahifasiga o'ting
2. Testni boshlang
3. Ko'p xato javoblar bering (70% dan past)
4. Natija: 
   - Lives 1 ta kamayadi (5 → 4)
   - Warning message: "Test muvaffaqiyatsiz! Yurakcha yo'qotdingiz. Qolgan: 4 ❤️"
   - Header'da 4 ta yurakcha ko'rsatiladi

#### Test 3: Lives Tugashi
1. Lives'ni 0 ga yetkazish uchun 5 marta muvaffaqiyatsiz test ishlang
2. Lives 0 bo'lganda test boshlashga harakat qiling
3. Natija:
   - Test boshlanmaydi
   - Error message: "Yurakchalaringiz tugagan! Keyingi yurakcha tiklanishini kuting..."
   - Leaderboard sahifasiga redirect

### 5. Lives Tiklanish

#### Manual Test (Admin Panel)
1. Admin panelga o'ting
2. User'ni toping va tahrirlang
3. `current_lives` ni 3 ga o'zgartiring
4. `last_life_lost_at` ni 30 daqiqa oldin qilib qo'ying
5. Saqlang
6. Bosh sahifaga qaytib, lives'ni tekshiring
7. Natija: Lives avtomatik 4 ga ko'tarilishi kerak

#### Automatic Test (Wait)
1. Lives'ni 4 ga kamaytiring (1 marta muvaffaqiyatsiz test)
2. 30 daqiqa kuting
3. Sahifani yangilang
4. Natija: Lives avtomatik 5 ga qaytadi

### 6. Kunlik Reset

1. Admin panelda user'ni tahrirlang
2. `last_daily_reset` ni kechagi sanaga o'zgartiring
3. `current_lives` ni 2 ga o'zgartiring
4. Saqlang
5. Bosh sahifaga o'ting
6. Natija: Lives avtomatik 5 ga qaytadi (kunlik reset)

### 7. Lives Out Modal

1. Lives'ni 0 ga yetkazing
2. Test boshlashga harakat qiling
3. Natija:
   - Modal oyna ochiladi
   - 💔 icon ko'rsatiladi
   - "Yurakchalar tugadi!" xabari
   - Timer ko'rsatiladi
   - "Tushundim" tugmasi

### 8. API Endpoint Test

Browser console'da:
```javascript
fetch('/api/lives-info/')
  .then(r => r.json())
  .then(data => console.log(data));
```

Kutilgan natija:
```json
{
    "current_lives": 5,
    "max_lives": 5,
    "next_life_in": null,
    "is_full": true,
    "system_active": true,
    "refill_time_minutes": 30
}
```

## Expected Results Summary

| Test | Expected Result | Status |
|------|----------------|--------|
| Admin Panel | Lives Settings ko'rinadi | ✅ |
| Header Display | 5 ta yurakcha ko'rsatiladi | ✅ |
| Profile Card | Lives card chiroyli ko'rinadi | ✅ |
| Successful Test | Lives o'zgarmaydi | ✅ |
| Failed Test | Lives 1 ta kamayadi | ✅ |
| No Lives | Test boshlanmaydi | ✅ |
| Auto Refill | 30 daqiqada tiklanadi | ✅ |
| Daily Reset | Har kuni 5 ta beriladi | ✅ |
| Lives Out Modal | Modal ochiladi | ✅ |
| API Endpoint | JSON qaytaradi | ✅ |

## Troubleshooting

### Lives ko'rinmayapti
- Server ishlaganini tekshiring
- Browser console'da xatolarni tekshiring
- `/api/lives-info/` endpoint ishlayotganini tekshiring

### Lives kamaymayd
- LivesSettings.is_active = True ekanini tekshiring
- Test muvaffaqiyatsiz bo'lganini tekshiring (70% dan past)
- Browser console'da xatolarni tekshiring

### Timer ishlamayapti
- JavaScript xatolarini tekshiring
- `last_life_lost_at` to'g'ri o'rnatilganini tekshiring
- Lives to'liq bo'lmasa timer ko'rsatiladi

## Next Steps

Agar barcha testlar muvaffaqiyatli bo'lsa:

1. ✅ Lives system production-ready
2. ✅ Deploy qilish mumkin
3. ✅ Foydalanuvchilarga taqdim etish mumkin

## Support

Agar muammo bo'lsa:
1. Server loglarini tekshiring
2. Browser console'ni tekshiring
3. Database'da Lives Settings mavjudligini tekshiring
4. Migration'lar to'liq o'tganini tekshiring
