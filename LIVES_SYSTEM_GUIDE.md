# Lives/Hearts System - To'liq Qo'llanma

## Umumiy Ma'lumot

Lives/Hearts tizimi - bu foydalanuvchilarning testlarni ishlashini cheklash va gamification qo'shish uchun yaratilgan tizim. Har bir foydalanuvchi kunlik ma'lum miqdorda yurakcha (lives) oladi va testda muvaffaqiyatsiz bo'lsa, yurakcha yo'qotadi.

## Asosiy Xususiyatlar

### 1. Dinamik Sozlamalar (Admin Panel)
Admin panel orqali quyidagilarni sozlash mumkin:
- **Kunlik yurakchalar soni** (daily_lives): Har kuni foydalanuvchi qancha yurakcha oladi
- **Maksimal yurakchalar** (max_lives): Bir vaqtning o'zida maksimal yurakchalar soni
- **Tiklanish vaqti** (refill_time_minutes): Bir yurakcha tiklanish uchun kerak bo'lgan vaqt (daqiqalarda)
- **Yo'qotish miqdori** (lives_cost_on_fail): Muvaffaqiyatsiz testda nechta yurakcha yo'qotiladi
- **O'tish foizi** (passing_score): Test o'tish uchun minimal foiz
- **Tizim holati** (is_active): Lives tizimini yoqish/o'chirish

### 2. Yurakchalar Ko'rinishi

Yurakchalar quyidagi joylarda ko'rsatiladi:
- **Header** (barcha sahifalarda): Yuqori qismda, sahifa nomidan keyin
- **Profil sahifasi**: Gamification bo'limida
- **Test sahifalari**: Test boshlashdan oldin va test jarayonida

### 3. Yurakchalar Logikasi

#### Kunlik Reset
- Har kuni yangi kun boshlanganida, foydalanuvchiga kunlik yurakchalar beriladi
- Agar foydalanuvchi yurakchalarini ishlatmagan bo'lsa ham, yangi kun boshida reset bo'ladi

#### Avtomatik Tiklanish
- Yurakcha yo'qotilgandan keyin, belgilangan vaqtdan so'ng avtomatik tiklanadi
- Masalan: 30 daqiqada 1 yurakcha tiklanadi
- Timer real-time ko'rsatiladi

#### Test Muvaffaqiyatsizligi
- Agar test natijasi passing_score dan past bo'lsa, yurakcha yo'qotiladi
- Yurakchalar tugasa, test ishlash imkoniyati yo'qoladi

## Texnik Implementatsiya

### Models (accounts/models.py)

```python
class LivesSettings(models.Model):
    """Lives tizimi sozlamalari - Singleton"""
    daily_lives = models.PositiveIntegerField(default=5)
    max_lives = models.PositiveIntegerField(default=5)
    refill_time_minutes = models.PositiveIntegerField(default=30)
    lives_cost_on_fail = models.PositiveIntegerField(default=1)
    passing_score = models.PositiveIntegerField(default=70)
    is_active = models.BooleanField(default=True)

class User(AbstractUser):
    # Lives fields
    current_lives = models.PositiveIntegerField(default=5)
    last_life_lost_at = models.DateTimeField(null=True, blank=True)
    last_daily_reset = models.DateField(null=True, blank=True)
```

### User Metodlari

```python
# Lives ma'lumotlarini olish
lives_info = user.get_lives_info()
# Returns: {
#     'current_lives': 3,
#     'max_lives': 5,
#     'next_life_in': timedelta(minutes=15),
#     'is_full': False,
#     'system_active': True
# }

# Yurakcha yo'qotish
user.lose_life()

# Yurakchalar bormi tekshirish
if user.has_lives():
    # Test ishlash mumkin
    pass
```

### API Endpoints

```javascript
// Lives ma'lumotlarini olish
GET /api/lives-info/
Response: {
    "current_lives": 3,
    "max_lives": 5,
    "next_life_in": 900,  // seconds
    "is_full": false,
    "system_active": true,
    "refill_time_minutes": 30
}
```

### Frontend Integration

```javascript
// Lives tizimini ishga tushirish
initLivesSystem();

// Lives displayni yangilash
updateLivesDisplay();

// Yurakcha yo'qotish animatsiyasi
loseLife();
```

## UI/UX Dizayni

### Header Lives Display
- **Joylashuv**: Header'ning o'ng tomonida, sahifa nomidan keyin
- **Dizayn**: Gradient pink background, white hearts
- **Animatsiya**: Heartbeat animation, smooth transitions
- **Timer**: Keyingi yurakcha tiklanish vaqti

### Ranglar
- **Background**: Linear gradient (#FF6B9D → #C06C84)
- **Full Heart**: ❤️ (white with glow)
- **Empty Heart**: 🤍 (30% opacity)
- **Timer**: White text with clock icon

### Animatsiyalar
- **Entrance**: Scale and fade in
- **Heartbeat**: Subtle pulse animation
- **Lost**: Scale up and fade out
- **Refill**: Scale in with bounce

## Test Integration

### Test Boshlashdan Oldin

```python
@login_required
def take_test_view(request, pk):
    # Lives tekshirish
    if not request.user.has_lives():
        messages.error(request, "Yurakchalaringiz tugagan. Keyingi yurakcha uchun kuting.")
        return redirect('core:test_leaderboard', pk=pk)
    
    # Test logic...
```

### Test Tugagandan Keyin

```python
# Natijani tekshirish
if score < settings.passing_score:
    # Yurakcha yo'qotish
    request.user.lose_life()
    messages.warning(request, f"Yurakcha yo'qotdingiz! Qolgan: {request.user.current_lives}")
```

## Admin Panel Sozlash

1. Admin panelga kiring: `/admin/`
2. "Lives sozlamalari" bo'limiga o'ting
3. Sozlamalarni o'zgartiring:
   - Kunlik yurakchalar: 5 (tavsiya etiladi)
   - Maksimal yurakchalar: 5
   - Tiklanish vaqti: 30 daqiqa
   - Yo'qotish: 1 yurakcha
   - O'tish foizi: 70%
4. Saqlang

## Foydalanuvchi Tajribasi

### Scenario 1: Yangi Foydalanuvchi
1. Ro'yxatdan o'tadi
2. 5 ta yurakcha oladi
3. Testlarni ishlaydi
4. Muvaffaqiyatsiz bo'lsa, yurakcha yo'qotadi
5. 30 daqiqadan keyin yurakcha tiklanadi

### Scenario 2: Yurakchalar Tugagan
1. Barcha yurakchalar tugagan
2. Test ishlash imkoniyati yo'q
3. Timer ko'rsatiladi
4. Yurakcha tiklanganidan keyin test ishlash mumkin

### Scenario 3: Kunlik Reset
1. Kecha 2 ta yurakcha qolgan
2. Bugun yangi kun boshlandi
3. Avtomatik 5 ta yurakcha berildi
4. Testlarni ishlashda davom etadi

## Kelajakdagi Yaxshilanishlar

1. **Premium Lives**: Pullik obuna orqali cheksiz yurakchalar
2. **Lives Gifting**: Do'stlarga yurakcha yuborish
3. **Daily Bonus**: Har kuni kirganlar uchun bonus yurakchalar
4. **Streak Bonus**: Uzluksiz kirganlar uchun qo'shimcha yurakchalar
5. **Lives Shop**: XP yoki pul evaziga yurakcha sotib olish

## Xulosa

Lives tizimi foydalanuvchilarni muntazam ravishda platformaga qaytishga undaydi va gamification elementini kuchaytiradi. Tizim to'liq dinamik va admin panel orqali osongina sozlanadi.
