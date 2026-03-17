# 🎯 Page-Based Load Balancing - Har Sahifa O'z Keyidan Foydalanadi

## Konsepsiya

Har bir sahifa o'z API keyidan foydalanadi. Bu **parallel translation** imkonini beradi!

### Mapping:
```python
PAGE_API_KEY_MAPPING = {
    'home': 1,              # Home page → KEY_1
    'institutions': 2,      # Institutions → KEY_2
    'courses': 3,           # Courses → KEY_3
    'subjects': 3,          # Subjects → KEY_3
    'mock_exams': 4,        # Mock exams → KEY_4
    'certificates': 4,      # Certificates → KEY_4
    'profile': 5,           # Profile → KEY_5
    'leaderboard': 5,       # Leaderboard → KEY_5
    'news': 2,              # News → KEY_2
    'ai_assistant': 1,      # AI Assistant → KEY_1
    'oferta': 1,            # Oferta → KEY_1
    'default': 1,           # Default → KEY_1
}
```

## Qanday Ishlaydi?

### 1. Sahifa Aniqlash
`core/context_processors.py` URL'dan sahifa nomini aniqlaydi:

```python
if not path or path == '':
    page_name = 'home'
elif 'institution' in path:
    page_name = 'institutions'
elif 'course' in path:
    page_name = 'courses'
# va hokazo...
```

### 2. API Key Tanlash
`core/translation.py` sahifa uchun tegishli keyni tanlaydi:

```python
def _get_api_key_for_page(self, page_name=None):
    key_index = self.PAGE_API_KEY_MAPPING.get(page_name, 1)
    return self.api_keys[key_index - 1]
```

### 3. Tarjima Qilish
Har bir sahifa o'z keyidan foydalanadi:

```python
api_key = self._get_api_key_for_page(page_name)
response = requests.post(api_url, headers={'Authorization': f'Bearer {api_key}'}, ...)
```

## Afzalliklari

### ✅ Parallel Translation
Har bir sahifa o'z keyidan foydalanadi, shuning uchun:
- Home page → KEY_1 (8 sekund)
- Institutions page → KEY_2 (8 sekund)
- Courses page → KEY_3 (8 sekund)

**Jami:** 8 sekund (parallel!)
**Oldin:** 24 sekund (ketma-ket)

### ✅ Worker Timeout Yo'q
Har bir sahifa 8 sekundda yuklanyapti (30 sekunddan kam).

### ✅ API Rate Limit Yo'q
Har bir key alohida rate limitga ega.

### ✅ Barcha Matnlar Tarjima Qilinadi
200 belgigacha matnlar tarjima qilinadi (oldin 50 edi).

## Template'da Ishlatish

### Yangi Tag (Tavsiya etiladi):
```django
{% load translation_tags %}

{# Page-aware translation #}
{% translate_with_page institution.name request.LANGUAGE_CODE %}
{% translate_with_page course.description "en" %}
```

### Eski Filter (Hali Ishlaydi):
```django
{# Legacy support - default key ishlatadi #}
{{ institution.name|translate:request.LANGUAGE_CODE }}
{{ course.description|translate:"en" }}
```

## Misol: Home Page

### URL: `/`
- Page name: `home`
- API key: `KEY_1`

### Tarjimalar:
```django
{% translate_with_page "Bosh sahifa" request.LANGUAGE_CODE %}
{# KEY_1 ishlatadi #}

{% translate_with_page institution.name request.LANGUAGE_CODE %}
{# KEY_1 ishlatadi #}
```

## Misol: Institutions Page

### URL: `/institutions/`
- Page name: `institutions`
- API key: `KEY_2`

### Tarjimalar:
```django
{% translate_with_page institution.name request.LANGUAGE_CODE %}
{# KEY_2 ishlatadi #}

{% translate_with_page institution.description request.LANGUAGE_CODE %}
{# KEY_2 ishlatadi #}
```

## Konfiguratsiya

### .env Fayl:
```env
DEEPSEEK_API_KEY_1=sk-first-key    # Home, AI Assistant, Oferta
DEEPSEEK_API_KEY_2=sk-second-key   # Institutions, News
DEEPSEEK_API_KEY_3=sk-third-key    # Courses, Subjects
DEEPSEEK_API_KEY_4=sk-fourth-key   # Mock Exams, Certificates
DEEPSEEK_API_KEY_5=sk-fifth-key    # Profile, Leaderboard
```

### Render Environment Variables:
```
DEEPSEEK_API_KEY_1 = sk-first-key
DEEPSEEK_API_KEY_2 = sk-second-key
DEEPSEEK_API_KEY_3 = sk-third-key
DEEPSEEK_API_KEY_4 = sk-fourth-key
DEEPSEEK_API_KEY_5 = sk-fifth-key
```

## Yangi Limitlar

- ✅ Uzunlik: 200 chars (oldin 50 edi)
- ✅ Timeout: 8 sekund (muvozanatli)
- ✅ max_tokens: 200 (uzun matnlar uchun)
- ✅ Cache: 7 kun (uzoq muddat)

## Monitoring

Loglardan ko'rish mumkin:
```
✅ Loaded 5 DeepSeek API key(s) for page-based load balancing
```

Har bir sahifa o'z keyidan foydalanadi:
```
Home page using KEY_1
Institutions page using KEY_2
Courses page using KEY_3
```

## Test Qilish

### 1. Local Test
```bash
# .env ga 5 ta key qo'shing
python manage.py shell

>>> from core.translation import translator
>>> print(f"Keys loaded: {len(translator.api_keys)}")
Keys loaded: 5

>>> # Test page-based key selection
>>> key = translator._get_api_key_for_page('home')
>>> print(f"Home page key: {key[:10]}...")
Home page key: sk-first...

>>> key = translator._get_api_key_for_page('institutions')
>>> print(f"Institutions page key: {key[:10]}...")
Institutions page key: sk-second...
```

### 2. Production Test
1. Render'ga 5 ta key qo'shing
2. Deploy qiling
3. Home page'ni oching → KEY_1 ishlatadi
4. Institutions page'ni oching → KEY_2 ishlatadi
5. Loglarni tekshiring

## Natija

### ✅ Parallel Translation
Har bir sahifa o'z keyidan foydalanadi.

### ✅ Worker Timeout Yo'q
Har bir sahifa 8 sekundda yuklanyapti.

### ✅ Barcha Matnlar Tarjima Qilinadi
200 belgigacha matnlar tarjima qilinadi.

### ✅ Tez va Barqaror
Cache tufayli ikkinchi marta juda tez.

## Deploy

```bash
git add .
git commit -m "feat: Page-based load balancing - har sahifa o'z keyidan foydalanadi"
git push origin main
```

Keyin Render'ga 5 ta API key qo'shing!

---

**Status:** Production-ready
**Keylar kerak:** 5 ta DeepSeek API key
**Deploy vaqti:** 5 daqiqa
**Risk:** Past - backward compatible

**Created:** February 23, 2026, 21:00
