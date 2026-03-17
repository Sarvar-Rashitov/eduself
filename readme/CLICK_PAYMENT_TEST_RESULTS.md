# Click To'lov Tizimi - Test Natijalari

## ✅ Test Muvaffaqiyatli O'tdi

Test sanasi: 02.03.2026
Test vaqti: 22:16 UTC

## Test Natijalari

### 1. Signature Yaratish va Tekshirish ✅

#### Signature Yaratish
```
Signature string: 12345678912345test_secret_key15000001234567890
MD5 hash: d9e18e4381f64a7e624df041cc763d03
Natija: ✅ To'g'ri
```

#### Signature Tekshirish
```
To'g'ri signature: ✅ Tasdiqlandi
Noto'g'ri signature: ✅ Rad etildi
```

### 2. Click Prepare API ✅

#### So'rov Ma'lumotlari
```json
{
  "click_trans_id": "1772489776829",
  "service_id": "your_click_service_id",
  "merchant_trans_id": "3",
  "amount": "50000.0",
  "action": "0",
  "sign_time": "1772489776",
  "sign_string": "dea813160d5fbb7b34c6..."
}
```

#### Javob
```json
{
  "error": 0,
  "error_note": "Success",
  "click_trans_id": "1772489776829",
  "merchant_trans_id": "3",
  "merchant_prepare_id": 3
}
```

#### Natija
- ✅ Signature to'g'ri tekshirildi
- ✅ To'lov topildi
- ✅ Summa to'g'ri
- ✅ To'lov holati `pending` → `processing` o'zgartirildi
- ✅ Transaction ID saqlandi

### 3. Click Complete API ✅

#### So'rov Ma'lumotlari
```json
{
  "click_trans_id": "1772489776829",
  "service_id": "your_click_service_id",
  "merchant_trans_id": "3",
  "amount": "50000.0",
  "action": "1",
  "sign_time": "1772489777",
  "sign_string": "c05224441f8d45eb025f0c5b38de4635",
  "error": "0",
  "error_note": "Success"
}
```

#### Javob
```json
{
  "error": 0,
  "error_note": "Success",
  "click_trans_id": "1772489776829",
  "merchant_trans_id": "3",
  "merchant_confirm_id": 3
}
```

#### Natija
- ✅ Signature to'g'ri tekshirildi
- ✅ To'lov topildi
- ✅ To'lov holati `processing` → `completed` o'zgartirildi
- ✅ Obuna yaratildi
- ✅ Bajarilgan vaqt saqlandi

### 4. Obuna Yaratish ✅

#### Yaratilgan Obuna
```
ID: 4
Ta'rif: Test Plan
Foydalanuvchi: Click Test
Boshlanish: 02.03.2026
Tugash: 01.04.2026
Holat: active
Faol: ✅ Ha
```

#### Obuna Xususiyatlari
- ✅ Cheksiz yurakchalar
- ✅ Cheksiz AI tahlil
- ✅ Cheksiz AI hamroh
- ✅ Cheksiz universitet imtihonlari
- ✅ Cheksiz mock examlar
- ✅ Cheksiz sertifikat testlar

### 5. Foydalanuvchi Holati ✅

```
Email: click_test@test.com
Ism: Click Test
Pro user: ✅ Ha
Faol obuna: Test Plan
Obunalar soni: 1 ta
```

## Test Qilingan Funksiyalar

### Backend Funksiyalar ✅

1. **ClickPaymentHandler.generate_signature()** ✅
   - MD5 hash yaratish
   - To'g'ri format

2. **ClickPaymentHandler.verify_signature()** ✅
   - Signature tekshirish
   - Xavfsizlik

3. **ClickPaymentHandler.prepare()** ✅
   - To'lovni topish
   - Summa tekshirish
   - Holat yangilash
   - Transaction ID saqlash
   - Xatoliklarni qaytarish

4. **ClickPaymentHandler.complete()** ✅
   - To'lovni tasdiqlash
   - Obuna yaratish
   - Promokod ishlatish
   - Bajarilgan vaqt saqlash

### Database Operatsiyalari ✅

1. **Payment Model** ✅
   - Yaratish
   - Yangilash
   - Holat o'zgartirish
   - Transaction ID saqlash

2. **UserSubscription Model** ✅
   - Yaratish
   - Muddat hisoblash
   - Holat tekshirish
   - is_active() metodi

3. **User Model** ✅
   - is_pro_user() metodi
   - get_active_subscription() metodi

## Xavfsizlik Testlari

### 1. Signature Tekshirish ✅

```python
# To'g'ri signature
✅ Qabul qilindi

# Noto'g'ri signature
❌ Rad etildi (error: -1, SIGN CHECK FAILED)
```

### 2. Summa Tekshirish ✅

```python
# To'g'ri summa
✅ Qabul qilindi

# Noto'g'ri summa
❌ Rad etildi (error: -2, Incorrect parameter amount)
```

### 3. To'lov Topish ✅

```python
# Mavjud to'lov
✅ Topildi

# Mavjud bo'lmagan to'lov
❌ Rad etildi (error: -5, Transaction not found)
```

### 4. Takroriy To'lov ✅

```python
# Birinchi marta
✅ Qabul qilindi

# Ikkinchi marta (allaqachon to'langan)
❌ Rad etildi (error: -4, Already paid)
```

## Callback URL'lar

### Production URL'lar

```
Prepare: https://eduself.uz/subscriptions/payment/click/prepare/
Complete: https://eduself.uz/subscriptions/payment/click/complete/
```

### Test URL'lar (ngrok)

```bash
# ngrok ishga tushirish
ngrok http 8000

# URL'lar
Prepare: https://your-ngrok-url.ngrok.io/subscriptions/payment/click/prepare/
Complete: https://your-ngrok-url.ngrok.io/subscriptions/payment/click/complete/
```

## To'lov URL Formati

### Click to'lov sahifasi

```
https://my.click.uz/services/pay?service_id={SERVICE_ID}&merchant_id={MERCHANT_ID}&amount={AMOUNT}&transaction_param={PAYMENT_ID}
```

### Misol

```
https://my.click.uz/services/pay?service_id=12345&merchant_id=67890&amount=50000&transaction_param=3
```

## cURL Test So'rovlari

### Prepare So'rovi

```bash
curl -X POST "https://eduself.uz/subscriptions/payment/click/prepare/" \
  -d "click_trans_id=1772489776829" \
  -d "service_id=your_click_service_id" \
  -d "merchant_trans_id=3" \
  -d "amount=50000.0" \
  -d "action=0" \
  -d "sign_time=1772489776" \
  -d "sign_string=dea813160d5fbb7b34c6..."
```

### Complete So'rovi

```bash
curl -X POST "https://eduself.uz/subscriptions/payment/click/complete/" \
  -d "click_trans_id=1772489776829" \
  -d "service_id=your_click_service_id" \
  -d "merchant_trans_id=3" \
  -d "amount=50000.0" \
  -d "action=1" \
  -d "sign_time=1772489777" \
  -d "sign_string=c05224441f8d45eb025f0c5b38de4635" \
  -d "error=0" \
  -d "error_note=Success"
```

## Xatoliklar va Ularning Kodlari

| Kod | Xatolik | Tavsif |
|-----|---------|--------|
| 0 | Success | Muvaffaqiyatli |
| -1 | SIGN CHECK FAILED | Signature noto'g'ri |
| -2 | Incorrect parameter amount | Summa noto'g'ri |
| -4 | Already paid | Allaqachon to'langan |
| -5 | Transaction not found | To'lov topilmadi |
| -8 | Error | Umumiy xatolik |

## Monitoring va Logging

### Database Queries

```sql
-- To'lovlarni ko'rish
SELECT * FROM subscriptions_payment WHERE payment_method = 'click';

-- Obunalarni ko'rish
SELECT * FROM subscriptions_usersubscription WHERE acquired_via = 'payment';

-- Pro userlarni ko'rish
SELECT u.* FROM accounts_user u
JOIN subscriptions_usersubscription s ON u.id = s.user_id
WHERE s.status = 'active' AND s.end_date > NOW();
```

### Admin Panel

```
/admin/subscriptions/payment/ - To'lovlar
/admin/subscriptions/usersubscription/ - Obunalar
```

## Keyingi Qadamlar

### 1. Click Merchant Panelida Sozlash

1. Click merchant paneliga kiring
2. Service sozlamalariga o'ting
3. Callback URL'larni qo'shing:
   - Prepare: `https://eduself.uz/subscriptions/payment/click/prepare/`
   - Complete: `https://eduself.uz/subscriptions/payment/click/complete/`
4. Secret key'ni oling va `.env` fayliga qo'shing

### 2. Production Sozlamalari

```env
# .env
CLICK_MERCHANT_ID=your_real_merchant_id
CLICK_SERVICE_ID=your_real_service_id
CLICK_SECRET_KEY=your_real_secret_key
CLICK_MERCHANT_USER_ID=your_real_merchant_user_id
```

### 3. Test Kartalar

Click test muhitida quyidagi kartalardan foydalaning:

```
Karta raqami: 8600 0000 0000 0000
Amal qilish muddati: 03/99
CVV: 123
SMS kod: 666666
```

### 4. Monitoring

- To'lovlar statistikasini kuzatish
- Xatoliklarni logging qilish
- Email bildirishnomalar yuborish
- Telegram bildirishnomalar yuborish

## Xulosa

✅ Click to'lov tizimi to'liq ishlayapti va production uchun tayyor:

1. ✅ Signature yaratish va tekshirish
2. ✅ Prepare API
3. ✅ Complete API
4. ✅ Obuna yaratish
5. ✅ Xavfsizlik tekshiruvlari
6. ✅ Xatoliklarni qaytarish
7. ✅ Database operatsiyalari
8. ✅ Pro user holati

Faqat haqiqiy Click kalitlarini sozlash va merchant panelda callback URL'larni qo'shish qoldi.
