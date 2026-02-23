# Ko'p Tillilik Tizimi - Foydalanish Qo'llanmasi

## Qo'llab-quvvatlanadigan Tillar

1. 🇺🇿 O'zbekcha (uz) - Default
2. 🇬🇧 English (en)
3. 🇷🇺 Русский (ru)
4. 🇰🇿 Қазақша (kk)
5. 🏴 Qaraqalpaqsha (kaa)
6. 🇹🇯 Тоҷикӣ (tg)
7. 🇰🇬 Кыргызча (ky)

## Arxitektura

### 1. Statik Matnlar (Django i18n)
Template'lardagi statik matnlar uchun Django'ning o'rnatilgan i18n tizimi ishlatiladi.

### 2. Dinamik Kontent (AI Tarjima)
Database'dagi dinamik kontent (news, courses, etc.) uchun DeepSeek AI API ishlatiladi.

## Foydalanish

### Template'larda Statik Matnlar

```django
{% load i18n %}

<!-- Oddiy matn -->
{% trans "Bosh sahifa" %}

<!-- O'zgaruvchi bilan -->
{% blocktrans %}Salom, {{ user.first_name }}!{% endblocktrans %}
```

### Template'larda Dinamik Kontent

```django
{% load translation_tags %}

<!-- Filter orqali -->
{{ news.title|translate:request.LANGUAGE_CODE }}
{{ course.description|translate:"en" }}

<!-- Tag orqali -->
{% translate_text news.title request.LANGUAGE_CODE %}
{% translate_text course.description "en" "uz" %}

<!-- Source va target tilni ko'rsatish -->
{{ news.title|translate_from:"uz,en" }}
```

### Python Kodda

```python
from core.translation import translate_text, get_translated_field

# Oddiy tarjima
translated = translate_text("Salom", "en", "uz")

# Model field tarjimasi
title = get_translated_field(news, 'title', 'en')
```

### Language Selector

Template'ga language selector qo'shish:

```django
{% load translation_tags %}
{% language_selector %}
```

Bu avtomatik ravishda dropdown yaratadi va foydalanuvchi tilni o'zgartirishi mumkin.

## Til O'zgartirish

### URL Parameter orqali

```
https://eduself.uz/courses/?lang=en
https://eduself.uz/news/?lang=ru
```

### JavaScript orqali

```javascript
// POST request
fetch('/change-language/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        language: 'en',
        next: '/courses/'
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        window.location.href = data.redirect;
    }
});
```

## Til Tanlash Priority

1. URL parameter (`?lang=uz`)
2. User.language (authenticated users)
3. Session language
4. Browser language
5. Default language (uz)

## Cache

AI tarjimalar avtomatik ravishda cache qilinadi:
- Cache vaqti: 24 soat
- Cache key: `translation:{source_lang}:{target_lang}:{text_hash}`

## API Configuration

`.env` faylida:

```env
DEEPSEEK_API_KEY=your-api-key-here
```

## Migration

User modeliga language field qo'shildi:

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

## Testing

Translation tizimini test qilish:

```bash
python test_translation.py
```

## Performance

- Cache hit rate: ~80%+
- Response time: <500ms
- API cost: ~$0.001 per 1K tokens

## Kelajakdagi Yaxshilanishlar

1. ✅ 7 til qo'llab-quvvatlanadi
2. ✅ AI tarjima tizimi
3. ✅ Cache tizimi
4. ✅ User preferences
5. 🔄 Locale files (.po/.mo) yaratish
6. 🔄 Admin panel translation management
7. 🔄 Batch translation
8. 🔄 Translation quality check

## Muammolarni Hal Qilish

### API key ishlamayapti
`.env` faylida `DEEPSEEK_API_KEY` to'g'ri o'rnatilganligini tekshiring.

### Tarjima ko'rinmayapti
1. Cache'ni tozalang: `python manage.py clear_cache`
2. Server'ni qayta ishga tushiring
3. Browser cache'ni tozalang

### Til o'zgarmayapti
1. Middleware to'g'ri o'rnatilganligini tekshiring
2. Session'lar ishlayotganligini tekshiring
3. Browser cookie'lari yoqilganligini tekshiring

## Qo'shimcha Ma'lumot

- Django i18n: https://docs.djangoproject.com/en/5.0/topics/i18n/
- DeepSeek API: https://platform.deepseek.com/docs
- Translation best practices: https://docs.djangoproject.com/en/5.0/topics/i18n/translation/
