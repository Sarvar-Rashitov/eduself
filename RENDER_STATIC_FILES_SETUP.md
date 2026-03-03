# Render.com'da Static Files Sozlash

## Muammo

`DEBUG=False` bo'lganda CSS fayllar yuklanmayapti.

## Yechim

### 1. Build Command'ni Yangilash

Render.com dashboard'da:

1. https://dashboard.render.com ga kiring
2. **eduself-bqc5** service'ni tanlang
3. **Settings** → **Build & Deploy** ga o'ting
4. **Build Command** ni quyidagiga o'zgartiring:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

5. **Save Changes** tugmasini bosing

### 2. Environment Variables

**Environment** → **Environment Variables** da:

```env
DEBUG=False
PYTHON_VERSION=3.11.0
```

### 3. Deploy Qilish

**Manual Deploy** → **Deploy latest commit**

### 4. Build Loglarni Kuzatish

Deploy paytida loglarni kuzating:

```
Building...
Installing dependencies...
Collecting static files...
237 static files copied to '/opt/render/project/src/staticfiles'
Running migrations...
Build complete!
```

`Collecting static files...` qatori ko'rinishi kerak!

### 5. Tekshirish

1. https://eduself.uz ga o'ting
2. F12 ni bosing (Developer Tools)
3. **Network** tabiga o'ting
4. Sahifani yangilang
5. CSS fayllarni tekshiring:
   - ✅ `/static/css/style.css` - Status: 200 OK
   - ✅ `/static/css/home.css` - Status: 200 OK

## Agar CSS Hali Ham Yuklanmasa

### Variant 1: WhiteNoise'ni Qayta Sozlash

`settings.py` da:

```python
# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0
```

### Variant 2: Static Root'ni Tekshirish

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Variant 3: STORAGES'ni Tekshirish

```python
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
```

### Variant 4: Middleware Tartibini Tekshirish

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Bu SecurityMiddleware'dan keyin bo'lishi kerak
    # ... boshqa middleware'lar
]
```

## Local Test (DEBUG=False)

Local'da test qilish uchun:

```bash
# 1. .env faylida
DEBUG=False

# 2. Collectstatic
python manage.py collectstatic --noinput

# 3. Server (--insecure faqat test uchun)
python manage.py runserver --insecure

# 4. Brauzerda
http://127.0.0.1:8000/
```

## Production Checklist

- [ ] Build Command'da `collectstatic` bor
- [ ] `DEBUG=False` sozlangan
- [ ] WhiteNoise middleware qo'shilgan
- [ ] STORAGES to'g'ri sozlangan
- [ ] Deploy muvaffaqiyatli
- [ ] CSS fayllar yuklanadi

## Xulosa

Render.com'da static fayllar ishlashi uchun:

1. ✅ Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
2. ✅ DEBUG=False
3. ✅ WhiteNoise middleware
4. ✅ STORAGES sozlangan

Shundan keyin CSS fayllar to'g'ri ishlaydi! 🎨
