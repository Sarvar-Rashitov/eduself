# Static Files (CSS) Muammosini Hal Qilish

## Muammo

`DEBUG=False` qilinganda CSS fayllar yuklanmayapti.

## Sabab

Django production rejimida static fayllarni avtomatik serve qilmaydi. WhiteNoise middleware ishlatiladi, lekin `collectstatic` ishga tushirilmagan.

## Yechim

### 1. Local Test (DEBUG=False)

```bash
# 1. Static fayllarni to'plash
python manage.py collectstatic --noinput

# 2. Serverni ishga tushiring
python manage.py runserver --insecure
```

`--insecure` flag'i DEBUG=False bo'lganda ham static fayllarni serve qiladi (faqat test uchun).

### 2. Production (Render.com)

#### A. Build Command

Render.com'da **Build Command** ni yangilang:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

#### B. Start Command

```bash
gunicorn eduself.wsgi:application
```

#### C. Environment Variables

```env
DEBUG=False
PYTHON_VERSION=3.11.0
```

### 3. Render.com'da Sozlash

1. https://dashboard.render.com ga kiring
2. Service'ni tanlang (eduself-bqc5)
3. **Settings** ga o'ting
4. **Build & Deploy** bo'limida:

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn eduself.wsgi:application
```

5. **Save Changes** tugmasini bosing
6. **Manual Deploy** → **Deploy latest commit**

### 4. Tekshirish

#### Local

```bash
# 1. DEBUG=False qiling
# .env
DEBUG=False

# 2. Collectstatic
python manage.py collectstatic --noinput

# 3. Server
python manage.py runserver --insecure

# 4. Brauzerda
http://127.0.0.1:8000/
```

#### Production

```bash
# 1. Deploy qiling
git push origin main

# 2. Render.com'da build loglarini kuzating
# "Collecting static files..." ko'rinishi kerak

# 3. Brauzerda
https://eduself.uz/
```

## WhiteNoise Sozlamalari

### settings.py

```python
# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # SecurityMiddleware'dan keyin
    # ... boshqa middleware'lar
]

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Django 4.2+ STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True if DEBUG else False
```

### requirements.txt

```txt
whitenoise==6.6.0
```

## Xatoliklarni Tuzatish

### Xatolik 1: "ValueError: Missing staticfiles manifest entry"

**Sabab:** `collectstatic` ishga tushirilmagan

**Yechim:**
```bash
python manage.py collectstatic --noinput --clear
```

### Xatolik 2: CSS fayllar 404

**Sabab:** STATIC_ROOT noto'g'ri

**Yechim:**
```python
# settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Xatolik 3: Production'da CSS yo'q

**Sabab:** Build command'da collectstatic yo'q

**Yechim:**
```bash
# Render.com Build Command
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Xatolik 4: Local'da CSS yo'q (DEBUG=False)

**Sabab:** Django production rejimida static serve qilmaydi

**Yechim:**
```bash
# Faqat test uchun
python manage.py runserver --insecure
```

## Monitoring

### Static Fayllar Joylashuvi

```bash
# Local
ls -la staticfiles/

# Production (Render.com)
# Build loglarida ko'ring:
# "22 static files copied to '/opt/render/project/src/staticfiles'"
```

### Browser DevTools

1. F12 ni bosing
2. **Network** tabiga o'ting
3. Sahifani yangilang
4. CSS fayllarni tekshiring:
   - ✅ Status: 200 OK
   - ❌ Status: 404 Not Found

### URL'larni Tekshirish

```html
<!-- Template'da -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- Brauzerda -->
<link rel="stylesheet" href="/static/css/style.css">
```

## Best Practices

### 1. .gitignore

```gitignore
# Static files
/staticfiles/
/static/CACHE/

# Media files
/media/
```

### 2. Deployment Checklist

- [ ] `DEBUG=False` sozlangan
- [ ] `collectstatic` build command'da
- [ ] WhiteNoise middleware qo'shilgan
- [ ] STATIC_ROOT to'g'ri
- [ ] STORAGES to'g'ri sozlangan

### 3. Local Development

```env
# .env
DEBUG=True
```

Local'da `DEBUG=True` bo'lganda Django avtomatik static fayllarni serve qiladi.

### 4. Production

```env
# Render.com Environment Variables
DEBUG=False
```

Production'da WhiteNoise static fayllarni serve qiladi.

## Xulosa

### Local (DEBUG=True)
- ✅ Django avtomatik static serve qiladi
- ✅ `collectstatic` kerak emas
- ✅ Tez development

### Production (DEBUG=False)
- ✅ WhiteNoise static serve qiladi
- ✅ `collectstatic` majburiy
- ✅ Xavfsiz va tez

**Keyingi qadam:**
1. Render.com'da Build Command'ni yangilang
2. Deploy qiling
3. CSS ishlashini tekshiring

Muvaffaqiyat! 🎨
