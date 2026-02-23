# Ko'p Tillilik Tizimi - Test Qo'llanmasi

## ✅ Server Ishga Tushirildi

Server manzili: http://127.0.0.1:8000/

## Test Qadamlari

### 1. Mobile Versiya (base.html)

1. Brauzerda http://127.0.0.1:8000/ ochilsin
2. Top bar'da (yuqori qismda) 🌐 globe icon ko'rinishi kerak
3. Globe icon'ga bosing - dropdown ochiladi
4. 7 ta til ko'rinishi kerak:
   - 🇺🇿 O'zbekcha
   - 🇬🇧 English
   - 🇷🇺 Русский
   - 🇰🇿 Қазақша
   - 🏴 Qaraqalpaqsha
   - 🇹🇯 Тоҷикӣ
   - 🇰🇬 Кыргызча
5. Har qanday tilni tanlang - sahifa yangilanadi
6. URL'da `?lang=en` parametri paydo bo'ladi

### 2. Desktop Versiya (base_desktop.html)

1. Brauzer oynasini kengaytiring (desktop mode)
2. Header'da navigation menu'da language selector ko'rinishi kerak
3. Dropdown ochiladi va 7 ta til ko'rinadi
4. Tilni tanlang - sahifa yangilanadi

### 3. Dinamik Kontent Tarjimasi

#### News sahifasida test qilish:

1. http://127.0.0.1:8000/news/ ga o'ting
2. Tilni English'ga o'zgartiring
3. News title va description avtomatik tarjima qilinishi kerak

#### Template'da qo'llash:

```django
{% load translation_tags %}

<!-- News title'ni tarjima qilish -->
{{ news.title|translate:request.LANGUAGE_CODE }}

<!-- Course description'ni tarjima qilish -->
{{ course.description|translate:"en" }}
```

### 4. User Profile'da Til Tanlash

1. Login qiling
2. Profile sahifasiga o'ting: http://127.0.0.1:8000/accounts/profile/
3. "Til" dropdown'da 7 ta til ko'rinishi kerak
4. Tilni tanlang va "Saqlash" bosing
5. Keyingi safar login qilganingizda, tanlangan til avtomatik o'rnatiladi

### 5. API Test

#### Python orqali:

```python
from core.translation import translate_text

# O'zbekchadan inglizchaga
result = translate_text("Salom dunyo", "en", "uz")
print(result)  # Hello world

# Inglizchadan ruschaga
result = translate_text("Hello world", "ru", "en")
print(result)  # Привет мир
```

#### Django shell'da:

```bash
python manage.py shell
```

```python
from core.translation import translator

# Test
text = "Bu test matni"
result = translator.translate(text, 'uz', 'en')
print(result)
```

### 6. Cache Test

1. Birinchi marta tarjima qilish - API'ga so'rov yuboriladi (sekinroq)
2. Ikkinchi marta bir xil matnni tarjima qilish - cache'dan olinadi (tezroq)

```python
import time
from core.translation import translator

text = "Salom, bu test matni"

# Birinchi tarjima
start = time.time()
result1 = translator.translate(text, 'uz', 'en')
time1 = time.time() - start
print(f"Birinchi: {time1:.3f}s")

# Ikkinchi tarjima (cache)
start = time.time()
result2 = translator.translate(text, 'uz', 'en')
time2 = time.time() - start
print(f"Ikkinchi: {time2:.3f}s")

print(f"Cache {time1/time2:.1f}x tezroq")
```

## Kutilgan Natijalar

### ✅ Mobile Versiya
- Language selector top-bar-right'da ko'rinadi
- Dropdown to'g'ri ishlaydi
- Til o'zgarishi URL parameter orqali ishlaydi

### ✅ Desktop Versiya
- Language selector navigation menu'da ko'rinadi
- Dropdown chiroyli ko'rinadi
- Hover effects ishlaydi

### ✅ Dinamik Tarjima
- News, courses, va boshqa dinamik kontent tarjima qilinadi
- Cache tizimi ishlaydi
- API errors gracefully handle qilinadi

### ✅ User Preferences
- User'ning tanlagan tili database'ga saqlanadi
- Keyingi login'da avtomatik o'rnatiladi
- Profile sahifasida o'zgartirish mumkin

## Muammolarni Hal Qilish

### Language selector ko'rinmayapti
1. Browser cache'ni tozalang (Ctrl+Shift+R)
2. Server'ni qayta ishga tushiring
3. Template'da `{% load translation_tags %}` borligini tekshiring

### Tarjima ishlamayapti
1. `.env` faylida `DEEPSEEK_API_KEY` to'g'ri o'rnatilganligini tekshiring
2. Internet connection borligini tekshiring
3. Django logs'ni tekshiring

### Dropdown ochilmayapti
1. Bootstrap JS yuklanganligini tekshiring
2. Browser console'da error borligini tekshiring
3. CSS to'g'ri yuklanganligini tekshiring

## Qo'shimcha Test

### Browser Language Detection
1. Browser tilini o'zgartiring (Settings > Languages)
2. Saytni yangi tab'da oching
3. Browser tili avtomatik aniqlanishi kerak

### Session Persistence
1. Tilni tanlang
2. Boshqa sahifaga o'ting
3. Tanlangan til saqlanishi kerak

### URL Parameter Priority
1. URL'ga `?lang=en` qo'shing
2. Bu session va user preference'dan yuqori priority'ga ega

## Performance Test

```bash
# Test script'ni ishga tushiring
python test_translation.py
```

Kutilgan natija:
- Barcha tillar to'g'ri tarjima qilinadi
- Cache ishlaydi
- Response time < 1s

## Xulosa

Agar barcha testlar muvaffaqiyatli o'tsa:
- ✅ Ko'p tillilik tizimi to'liq ishlaydi
- ✅ 7 ta til qo'llab-quvvatlanadi
- ✅ AI tarjima ishlaydi
- ✅ Cache tizimi faol
- ✅ Mobile va Desktop versiyalar tayyor

Platformangiz endi ko'p tilli! 🎉
