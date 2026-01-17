# EduSelf Telegram Bot - Render Deploy Guide

## 1. Environment Variables (Render Dashboard)

Render dashboard'da quyidagi environment variable'larni qo'shing:

```
DATABASE_URL=postgresql://eduself_db_user:bAdUpCgLl1JmmInlMtpVBMd0JSZ5hlRr@dpg-d4qatlggjchc73b93sbg-a.oregon-postgres.render.com/eduself_db
DEEPSEEK_API_KEY=sk-fbfb83fcb68941bbbf599a4d76461f04
USE_S3=True
AWS_ACCESS_KEY_ID=2b6dbc029d2a370fc8a13c5597d7a556
AWS_SECRET_ACCESS_KEY=aedd1a4db789ff8f04aba7c84e8e73a3abead6a954a4662d4b3588ecfd8bb210
AWS_STORAGE_BUCKET_NAME=eduself-media
AWS_S3_ENDPOINT_URL=https://dcdaade24fb750e52e9f2550daa47a0f.r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto
AWS_DEFAULT_ACL=None
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=EduSelf <noreply@eduself.uz>
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
TELEGRAM_BOT_TOKEN=8468525153:AAEF10F5CDCJ8IkuLJw0WbqTqgkhfI_EdEo
TELEGRAM_BOT_USERNAME=edu_self_bot
TELEGRAM_CHANNEL_USERNAME=@eduselfuz
SITE_URL=https://eduself.uz
DJANGO_SETTINGS_MODULE=eduself.settings
```

## 2. Webhook Setup

Bot Render'da webhook rejimida ishlashi kerak. Polling emas!

### Webhook URL o'rnatish:
```
https://your-render-app.onrender.com/telegram/set-webhook/
```

### Webhook endpoint:
```
https://your-render-app.onrender.com/telegram/webhook/
```

## 3. Build Command (Render)

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

## 4. Start Command (Render)

Web Service uchun:
```bash
gunicorn eduself.wsgi:application
```

Background Worker uchun (agar kerak bo'lsa):
```bash
python run_bot.py
```

## 5. Render Service Types

### Option 1: Web Service Only (Webhook)
- Type: Web Service
- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start Command: `gunicorn eduself.wsgi:application`
- Bot webhook orqali ishlaydi

### Option 2: Web Service + Background Worker
- Web Service: Django app
- Background Worker: Bot polling

## 6. Webhook vs Polling

### Webhook (Render uchun tavsiya etiladi):
- Render'da web service sifatida ishlaydi
- Telegram webhook'larni Django view'ga yuboradi
- Resurs tejaydi

### Polling (Local development):
- Bot doimiy Telegram API'ni so'raydi
- Background process kerak

## 7. Debug Commands

### Webhook holatini tekshirish:
```
https://your-render-app.onrender.com/telegram/webhook-info/
```

### Webhook o'rnatish:
```
https://your-render-app.onrender.com/telegram/set-webhook/
```

### Webhook o'chirish:
```
https://your-render-app.onrender.com/telegram/delete-webhook/
```

## 8. Logs Monitoring

Render dashboard'da logs'ni kuzating:
- Bot xabarlari
- Webhook so'rovlari
- Django errors

## 9. Common Issues

### Bot javob bermaydi:
1. Webhook to'g'ri o'rnatilganmi?
2. Environment variables to'g'rimi?
3. Database ulanishi ishlayaptimi?

### Webhook errors:
1. SITE_URL to'g'ri ko'rsatilganmi?
2. SSL sertifikat ishlayaptimi?
3. Django URL routing to'g'rimi?

## 10. Testing

### Local test:
```bash
python manage.py runserver
ngrok http 8000
# Webhook URL: https://xxx.ngrok.io/telegram/webhook/
```

### Production test:
1. Render'da deploy qiling
2. Webhook o'rnating
3. Bot'ga /start yuboring