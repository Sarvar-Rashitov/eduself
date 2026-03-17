# Production Deployment Guide

## Environment Variables

Production serverda quyidagi environment variable'larni sozlang:

### 1. Debug Mode

```env
DEBUG=False
```

**Qayerda sozlash:**
- **Render.com**: Dashboard → Service → Environment → Add Environment Variable
- **Heroku**: Settings → Config Vars → Add
- **DigitalOcean**: App Platform → Settings → Environment Variables

### 2. Barcha Kerakli Variables

```env
# Debug
DEBUG=False

# Database
DATABASE_URL=postgresql://...

# Secret Key
SESSION_SECRET=your-production-secret-key

# Site URL
SITE_URL=https://eduself.uz

# Click Payment
CLICK_MERCHANT_ID=57452
CLICK_SERVICE_ID=97245
CLICK_SECRET_KEY=your_real_secret_key
CLICK_MERCHANT_USER_ID=57452

# Payme Payment
PAYME_MERCHANT_ID=your_payme_merchant_id
PAYME_SECRET_KEY=your_payme_secret_key
PAYME_ENDPOINT=https://checkout.paycom.uz

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=eduselfuz@gmail.com
EMAIL_HOST_PASSWORD=your_password
DEFAULT_FROM_EMAIL=EduSelf <eduselfuz@gmail.com>

# Cloudflare R2
USE_S3=True
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=eduself-media
AWS_S3_ENDPOINT_URL=https://...r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_BOT_USERNAME=edu_self_bot
TELEGRAM_CHANNEL_USERNAME=@eduselfuz

# DeepSeek API
DEEPSEEK_API_KEY_1=sk-...
DEEPSEEK_API_KEY_2=sk-...
DEEPSEEK_API_KEY_3=sk-...
DEEPSEEK_API_KEY_4=sk-...
DEEPSEEK_API_KEY_5=sk-...
```

## Render.com'da Sozlash

### 1. Dashboard'ga Kiring

https://dashboard.render.com

### 2. Service'ni Tanlang

eduself-bqc5 (yoki sizning service nomingiz)

### 3. Environment Variables'ga O'ting

**Settings** → **Environment** → **Environment Variables**

### 4. DEBUG'ni Qo'shing

- **Key**: `DEBUG`
- **Value**: `False`
- **Save Changes** tugmasini bosing

### 5. Service'ni Qayta Ishga Tushiring

**Manual Deploy** → **Deploy latest commit**

## Local vs Production

### Local (DEBUG=True)

```python
# .env
DEBUG=True
```

**Natija:**
- To'lov yaratiladi
- Xabar ko'rsatiladi
- Click sahifasiga yo'naltirilmaydi
- Qo'lda complete qilish kerak

### Production (DEBUG=False)

```env
# Render.com Environment Variables
DEBUG=False
```

**Natija:**
- To'lov yaratiladi
- Click to'lov sahifasiga yo'naltiriladi
- Callback URL'lar avtomatik chaqiriladi
- Obuna avtomatik yaratiladi

## Test Qilish

### Local Test

```bash
# 1. .env faylida
DEBUG=True

# 2. Serverni ishga tushiring
python manage.py runserver

# 3. Brauzerda test qiling
http://127.0.0.1:8000/subscriptions/pro/

# 4. To'lovni complete qiling
python manage.py complete_test_payment PAYMENT_ID
```

### Production Test

```bash
# 1. Render.com'da
DEBUG=False

# 2. Deploy qiling
git push origin main

# 3. Brauzerda test qiling
https://eduself.uz/subscriptions/pro/

# 4. Click to'lov sahifasiga yo'naltiriladi
# 5. Test kartadan foydalaning
# 6. Callback URL'lar avtomatik ishlaydi
```

## Click Callback URL'lar

Production'da Click merchant panelda sozlang:

### Prepare URL
```
https://eduself.uz/subscriptions/payment/click/prepare/
```

### Complete URL
```
https://eduself.uz/subscriptions/payment/click/complete/
```

**Qanday sozlash:**

1. https://my.click.uz ga kiring
2. **Xizmatlar** → **Service ID: 97245**
3. **Sozlamalar** → **Callback URL'lar**
4. Yuqoridagi URL'larni qo'shing
5. **Saqlash**

## HTTPS Sozlash

### Render.com

Render.com avtomatik HTTPS beradi:
- ✅ SSL sertifikat avtomatik
- ✅ HTTPS majburiy
- ✅ Qo'shimcha sozlash kerak emas

### Custom Domain

Agar custom domain (eduself.uz) ishlatayotgan bo'lsangiz:

1. Render.com'da **Settings** → **Custom Domain**
2. `eduself.uz` va `www.eduself.uz` qo'shing
3. DNS sozlamalarini yangilang:
   ```
   Type: CNAME
   Name: @
   Value: eduself-bqc5.onrender.com
   
   Type: CNAME
   Name: www
   Value: eduself-bqc5.onrender.com
   ```

## Monitoring

### Loglarni Ko'rish

**Render.com:**
- Dashboard → Service → Logs

**Local:**
```bash
tail -f logs/django.log
```

### Database Queries

```sql
-- Production to'lovlar
SELECT * FROM subscriptions_payment 
WHERE status = 'completed' 
ORDER BY created_at DESC 
LIMIT 10;

-- Faol obunalar
SELECT COUNT(*) FROM subscriptions_usersubscription 
WHERE status = 'active' AND end_date > NOW();
```

## Xatoliklarni Tuzatish

### Xatolik: Local rejimda ishlayapti

**Sabab:** `DEBUG=True`

**Yechim:**
```env
# Production'da
DEBUG=False
```

### Xatolik: Click sahifasiga yo'naltirilmayapti

**Sabab:** `DEBUG=True` yoki callback URL'lar noto'g'ri

**Yechim:**
1. `DEBUG=False` qiling
2. Callback URL'larni tekshiring
3. HTTPS ishlayotganini tekshiring

### Xatolik: Callback URL'lar ishlamayapti

**Sabab:** URL'lar noto'g'ri yoki server ishlamayapti

**Yechim:**
1. URL'larni tekshiring: `https://eduself.uz/subscriptions/payment/click/prepare/`
2. Server ishlab turganini tekshiring
3. HTTPS sozlanganini tekshiring
4. Click merchant panelda URL'lar to'g'ri ekanligini tekshiring

## Xulosa

### Local Development
```env
DEBUG=True
```
- ✅ Tez test qilish
- ✅ Qo'lda complete qilish
- ✅ Xatoliklarni ko'rish

### Production
```env
DEBUG=False
```
- ✅ Click to'lov ishlaydi
- ✅ Callback URL'lar avtomatik
- ✅ Obuna avtomatik yaratiladi
- ✅ Xavfsiz

**Keyingi qadam:**
1. Render.com'da `DEBUG=False` qiling
2. Service'ni qayta ishga tushiring
3. Production'da test qiling
4. Click merchant panelda callback URL'larni sozlang

Muvaffaqiyat! 🚀
