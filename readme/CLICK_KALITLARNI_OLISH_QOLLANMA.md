# Click Kalitlarni Olish va Sozlash Qo'llanmasi

## Hozirgi Holat

Sizning `.env` faylingizda:
```env
CLICK_MERCHANT_ID=57452          ✅ To'ldirilgan
CLICK_SERVICE_ID=97245           ✅ To'ldirilgan
CLICK_SECRET_KEY=············    ⚠️  Ko'rsatilmagan (xavfsizlik uchun)
CLICK_MERCHANT_USER_ID=your_click_merchant_user_id  ❌ To'ldirilmagan
```

## Click Kalitlarni Qayerdan Olish Mumkin?

### 1. Click Merchant Paneliga Kirish

**URL:** https://my.click.uz

**Login ma'lumotlari:**
- Login: Sizning Click hisobingiz
- Parol: Sizning parolingiz

### 2. Kalitlarni Topish

#### A. CLICK_MERCHANT_ID va CLICK_SERVICE_ID ✅

Siz allaqachon topgan ekansiz:
```
CLICK_MERCHANT_ID=57452
CLICK_SERVICE_ID=97245
```

#### B. CLICK_SECRET_KEY 🔑

**Qayerdan topish:**

1. Click merchant paneliga kiring: https://my.click.uz
2. **"Xizmatlar"** (Services) bo'limiga o'ting
3. Sizning xizmatingizni tanlang (Service ID: 97245)
4. **"Sozlamalar"** (Settings) yoki **"API"** bo'limiga o'ting
5. **"Secret Key"** yoki **"Maxfiy kalit"** ni toping

**Secret Key formati:**
```
Odatda 32-64 belgidan iborat random string:
Misol: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

**Agar Secret Key topilmasa:**
- Click support bilan bog'laning: support@click.uz
- Telegram: @click_support
- Telefon: +998 71 200 0 200

#### C. CLICK_MERCHANT_USER_ID 👤

Bu qiymat **ixtiyoriy** (optional). Agar Click panelda topilmasa, quyidagilardan birini qiling:

**Variant 1: Merchant ID'ni ishlatish**
```env
CLICK_MERCHANT_USER_ID=57452
```

**Variant 2: Bo'sh qoldirish**
```env
CLICK_MERCHANT_USER_ID=
```

**Variant 3: Click support'dan so'rash**
- Email: support@click.uz
- Telegram: @click_support

## To'liq Sozlash Qo'llanmasi

### Qadam 1: Secret Key'ni Olish

1. https://my.click.uz ga kiring
2. **Xizmatlar** → **Service ID: 97245** ni tanlang
3. **Sozlamalar** → **API** bo'limiga o'ting
4. **Secret Key** ni nusxalang

### Qadam 2: .env Faylini Yangilash

```env
# Payment Integration
# Click Payment
CLICK_MERCHANT_ID=57452
CLICK_SERVICE_ID=97245
CLICK_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6  # Haqiqiy kalitni qo'ying
CLICK_MERCHANT_USER_ID=57452  # Yoki bo'sh qoldiring
```

### Qadam 3: Callback URL'larni Sozlash

Click merchant panelda quyidagi URL'larni qo'shing:

**Prepare URL:**
```
https://eduself.uz/subscriptions/payment/click/prepare/
```

**Complete URL:**
```
https://eduself.uz/subscriptions/payment/click/complete/
```

**Qanday qo'shish:**

1. Click merchant paneliga kiring
2. **Xizmatlar** → **Service ID: 97245**
3. **Sozlamalar** → **Callback URL'lar**
4. Yuqoridagi URL'larni qo'shing
5. **Saqlash** tugmasini bosing

### Qadam 4: Test Qilish

#### A. Test Muhitda (agar mavjud bo'lsa)

```bash
# Test skriptini ishga tushiring
python test_click_payment.py
```

#### B. Haqiqiy To'lov Qilish

1. Saytga kiring: https://eduself.uz
2. **EduSelf Pro** sahifasiga o'ting
3. Ta'rifni tanlang
4. **Click** to'lov usulini tanlang
5. Test kartadan foydalaning:
   ```
   Karta: 8600 0000 0000 0000
   Muddat: 03/99
   CVV: 123
   SMS: 666666
   ```

## Xavfsizlik

### Secret Key'ni Himoya Qilish

1. ✅ `.env` faylini `.gitignore` ga qo'shing
2. ✅ Secret key'ni hech qachon commit qilmang
3. ✅ Secret key'ni hech kimga bermang
4. ✅ Production serverda environment variables ishlatilsin

### .gitignore Tekshirish

```bash
# .gitignore faylida bo'lishi kerak
.env
.env.local
.env.production
*.env
```

## Muammolarni Hal Qilish

### Muammo 1: Secret Key Topilmayapti

**Yechim:**
1. Click support bilan bog'laning
2. Merchant ID va Service ID'ni ayting
3. Secret key'ni so'rang

**Kontaktlar:**
- Email: support@click.uz
- Telegram: @click_support
- Telefon: +998 71 200 0 200

### Muammo 2: Callback URL'lar Ishlamayapti

**Tekshirish:**
```bash
# URL'lar ochiq ekanligini tekshiring
curl -X POST https://eduself.uz/subscriptions/payment/click/prepare/
```

**Yechim:**
1. HTTPS sozlangan bo'lishi kerak
2. URL'lar to'g'ri yozilgan bo'lishi kerak
3. Server ishlab turishi kerak

### Muammo 3: Signature Xatolik

**Sabab:** Secret key noto'g'ri

**Yechim:**
1. Secret key'ni qayta tekshiring
2. Bo'sh joylar yo'qligini tekshiring
3. Copy-paste qilganda qo'shimcha belgilar qo'shilmaganligini tekshiring

## Test Qilish

### 1. Kalitlarni Tekshirish

```bash
python manage.py shell
```

```python
from django.conf import settings

print(f"CLICK_MERCHANT_ID: {settings.CLICK_MERCHANT_ID}")
print(f"CLICK_SERVICE_ID: {settings.CLICK_SERVICE_ID}")
print(f"CLICK_SECRET_KEY: {settings.CLICK_SECRET_KEY[:10]}...")
print(f"CLICK_MERCHANT_USER_ID: {settings.CLICK_MERCHANT_USER_ID}")
```

### 2. To'lov Tizimini Test Qilish

```bash
# Asosiy test
python test_click_payment.py

# Xatolik ssenariylari
python test_click_error_scenarios.py
```

### 3. Haqiqiy To'lov Test

1. Minimal summa bilan test qiling (masalan, 1000 so'm)
2. Test kartadan foydalaning
3. To'lov muvaffaqiyatli bo'lganini tekshiring
4. Admin panelda to'lovni ko'ring

## Click Support Bilan Bog'lanish

### Email Shabloni

```
Mavzu: Secret Key so'rovi - Service ID: 97245

Assalomu alaykum,

Men eduself.uz saytining egasiman. Click to'lov tizimini integratsiya qilmoqdaman.

Merchant ID: 57452
Service ID: 97245

Secret Key'ni olishim kerak. Yordam bera olasizmi?

Rahmat,
[Ismingiz]
[Telefon raqamingiz]
```

### Telegram Xabari

```
Salom! 

eduself.uz uchun Click integratsiyasi qilmoqdaman.
Merchant ID: 57452
Service ID: 97245

Secret Key kerak. Yordam bering iltimos.
```

## Yakuniy Tekshirish

Barcha kalitlar to'ldirilgandan keyin:

```env
# ✅ To'liq to'ldirilgan .env
CLICK_MERCHANT_ID=57452
CLICK_SERVICE_ID=97245
CLICK_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
CLICK_MERCHANT_USER_ID=57452
```

**Keyingi qadamlar:**

1. ✅ Serverni qayta ishga tushiring
2. ✅ Test skriptini ishga tushiring
3. ✅ Haqiqiy to'lov qiling
4. ✅ Admin panelda natijani tekshiring

## Qo'shimcha Ma'lumot

### Click Dokumentatsiyasi

- API Docs: https://docs.click.uz/
- Merchant Panel: https://my.click.uz/
- Support: support@click.uz

### Foydali Linklar

- Test kartalar: https://docs.click.uz/test-cards/
- Xatolik kodlari: https://docs.click.uz/error-codes/
- Integration guide: https://docs.click.uz/integration/

## Xulosa

Sizda allaqachon mavjud:
- ✅ CLICK_MERCHANT_ID=57452
- ✅ CLICK_SERVICE_ID=97245
- ⚠️  CLICK_SECRET_KEY (ko'rsatilmagan, lekin mavjud bo'lishi mumkin)
- ❌ CLICK_MERCHANT_USER_ID (ixtiyoriy)

**Keyingi qadam:**
1. Secret Key'ni Click paneldan oling
2. MERCHANT_USER_ID'ni qo'shing (yoki Merchant ID'ni ishlatilng)
3. Test qiling
4. Production'ga deploy qiling

Agar qiyinchilik bo'lsa, Click support bilan bog'laning! 📞
