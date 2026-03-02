# Click To'lov Tizimini Test Qilish

## 1. Click Merchant Account

### Test Muhit (Sandbox)
Click test muhitida test qilish uchun:

1. **Click Merchant Panel**: https://my.click.uz/
2. **Test Account** yaratish kerak
3. **Service** yaratish va test kalitlarni olish

### Kerakli Ma'lumotlar

`.env` faylida:
```env
CLICK_MERCHANT_ID=your_test_merchant_id
CLICK_SERVICE_ID=your_test_service_id
CLICK_SECRET_KEY=your_test_secret_key
CLICK_MERCHANT_USER_ID=your_test_merchant_user_id
```

## 2. Callback URL'larni Sozlash

Click merchant panelida:

**Prepare URL:**
```
https://eduself.uz/subscriptions/payment/click/prepare/
```

**Complete URL:**
```
https://eduself.uz/subscriptions/payment/click/complete/
```

⚠️ **Muhim:** URL'lar HTTPS bo'lishi kerak!

## 3. Test Qilish Usullari

### A. Manual Test (Postman/cURL)

#### Prepare Request

```bash
curl -X POST "https://eduself.uz/subscriptions/payment/click/prepare/" \
  -d "click_trans_id=123456789" \
  -d "service_id=YOUR_SERVICE_ID" \
  -d "merchant_trans_id=PAYMENT_ID" \
  -d "amount=79000" \
  -d "action=0" \
  -d "sign_time=2024-01-01 12:00:00" \
  -d "sign_string=CALCULATED_SIGNATURE"
```

**Parametrlar:**
- `click_trans_id`: Click tranzaksiya ID (test: 123456789)
- `service_id`: Sizning service ID
- `merchant_trans_id`: Payment ID (database'dan)
- `amount`: Summa (so'm)
- `action`: 0 (prepare) yoki 1 (complete)
- `sign_time`: Hozirgi vaqt
- `sign_string`: MD5 signature

#### Signature Hisoblash

Python'da:
```python
import hashlib

click_trans_id = "123456789"
service_id = "YOUR_SERVICE_ID"
secret_key = "YOUR_SECRET_KEY"
merchant_trans_id = "PAYMENT_ID"
amount = "79000"
action = "0"
sign_time = "2024-01-01 12:00:00"

signature_string = f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}{amount}{action}{sign_time}"
signature = hashlib.md5(signature_string.encode()).hexdigest()

print(f"Signature: {signature}")
```

### B. Click Test Kartalar

Click test muhitida test kartalar:

**Test Karta 1 (Muvaffaqiyatli):**
- Karta: `8600 4954 7331 6478`
- Amal qilish: `03/99`
- CVV: `666`

**Test Karta 2 (Muvaffaqiyatsiz):**
- Karta: `8600 0691 9540 6311`
- Amal qilish: `03/99`
- CVV: `666`

### C. Click Payment URL

Foydalanuvchini to'lov sahifasiga yo'naltirish:

```
https://my.click.uz/services/pay?service_id=YOUR_SERVICE_ID&merchant_id=YOUR_MERCHANT_ID&amount=79000&transaction_param=PAYMENT_ID&return_url=https://eduself.uz/subscriptions/pro/
```

**Parametrlar:**
- `service_id`: Sizning service ID
- `merchant_id`: Sizning merchant ID
- `amount`: Summa (so'm)
- `transaction_param`: Payment ID
- `return_url`: Qaytish URL'i

## 4. Test Jarayoni

### Qadamma-Qadam Test

#### 1. Payment Yaratish

```bash
# Django shell
python manage.py shell
```

```python
from accounts.models import User
from subscriptions.models import SubscriptionPlan, Payment

user = User.objects.first()
plan = SubscriptionPlan.objects.get(slug='pro')

payment = Payment.objects.create(
    user=user,
    plan=plan,
    payment_method='click',
    amount=plan.price,
    final_amount=plan.price,
    status='pending'
)

print(f"Payment ID: {payment.id}")
print(f"Amount: {payment.final_amount}")
```

#### 2. Click URL Yaratish

```python
payment_id = payment.id
amount = int(payment.final_amount)

click_url = f"https://my.click.uz/services/pay?service_id=YOUR_SERVICE_ID&merchant_id=YOUR_MERCHANT_ID&amount={amount}&transaction_param={payment_id}&return_url=https://eduself.uz/subscriptions/pro/"

print(f"Click URL: {click_url}")
```

#### 3. To'lov Qilish

1. Click URL'ni brauzerda oching
2. Test kartani kiriting
3. To'lovni tasdiqlang

#### 4. Callback Tekshirish

Click avtomatik ravishda callback yuboradi:

**Prepare:**
```
POST /subscriptions/payment/click/prepare/
```

**Complete:**
```
POST /subscriptions/payment/click/complete/
```

#### 5. Natijani Tekshirish

```python
# Django shell
from subscriptions.models import Payment, UserSubscription

payment = Payment.objects.get(id=PAYMENT_ID)
print(f"Status: {payment.status}")
print(f"Transaction ID: {payment.transaction_id}")

if payment.status == 'completed':
    subscription = UserSubscription.objects.filter(user=payment.user).first()
    print(f"Subscription: {subscription}")
    print(f"Plan: {subscription.plan.name}")
    print(f"End Date: {subscription.end_date}")
```

## 5. Xatoliklarni Tekshirish

### Server Logs

```bash
# Terminal'da server log'larini kuzating
python manage.py runserver
```

### Database Tekshirish

```sql
-- Payments
SELECT * FROM subscriptions_payment ORDER BY created_at DESC LIMIT 5;

-- Subscriptions
SELECT * FROM subscriptions_usersubscription ORDER BY created_at DESC LIMIT 5;
```

### Admin Panel

1. http://127.0.0.1:8000/nokia/
2. Obunalar > To'lovlar
3. Oxirgi to'lovni ko'ring

## 6. Keng Tarqalgan Xatoliklar

### 1. Signature Error

**Xato:** `SIGN CHECK FAILED`

**Yechim:**
- Secret key to'g'ri ekanligini tekshiring
- Signature string to'g'ri formatda ekanligini tekshiring
- Barcha parametrlar to'g'ri tartibda ekanligini tekshiring

### 2. Payment Not Found

**Xato:** `Transaction not found`

**Yechim:**
- Payment ID to'g'ri ekanligini tekshiring
- Payment database'da mavjudligini tekshiring
- Payment status `pending` ekanligini tekshiring

### 3. Amount Mismatch

**Xato:** `Incorrect parameter amount`

**Yechim:**
- Click'dan kelgan summa database'dagi summa bilan mos kelishini tekshiring
- Summa so'm'da ekanligini tekshiring (tiyin emas!)

### 4. HTTPS Required

**Xato:** Callback ishlamayapti

**Yechim:**
- Callback URL'lar HTTPS bo'lishi kerak
- Local test uchun ngrok ishlatish:
  ```bash
  ngrok http 8000
  ```
- Ngrok URL'ni Click panelida sozlash

## 7. Local Test (ngrok bilan)

### ngrok O'rnatish

```bash
# Windows
choco install ngrok

# Mac
brew install ngrok

# Linux
snap install ngrok
```

### ngrok Ishga Tushirish

```bash
ngrok http 8000
```

Output:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### Callback URL'larni Yangilash

Click panelida:
```
Prepare: https://abc123.ngrok.io/subscriptions/payment/click/prepare/
Complete: https://abc123.ngrok.io/subscriptions/payment/click/complete/
```

## 8. Production Test

### Production'da Test Qilish

1. **Real Merchant Account** yaratish
2. **Production kalitlar** olish
3. **HTTPS** sozlash (SSL sertifikat)
4. **Callback URL'lar** sozlash
5. **Test to'lov** qilish (real karta bilan)

### Production Checklist

- [ ] Merchant account yaratilgan
- [ ] Production kalitlar `.env` faylida
- [ ] HTTPS ishlayapti
- [ ] Callback URL'lar to'g'ri
- [ ] Signature verification ishlayapti
- [ ] Test to'lov muvaffaqiyatli
- [ ] Obuna yaratildi
- [ ] Email notification yuborildi

## 9. Monitoring

### Real-time Monitoring

```python
# Django shell
from subscriptions.models import Payment

# Pending to'lovlar
pending = Payment.objects.filter(status='pending').count()
print(f"Pending: {pending}")

# Completed to'lovlar
completed = Payment.objects.filter(status='completed').count()
print(f"Completed: {completed}")

# Failed to'lovlar
failed = Payment.objects.filter(status='failed').count()
print(f"Failed: {failed}")
```

### Admin Panel Monitoring

1. Obunalar > To'lovlar
2. Filter by status
3. Check transaction_id
4. View payment_data (JSON)

## 10. Troubleshooting

### Debug Mode

`subscriptions/payment_handlers.py` da:

```python
import logging
logger = logging.getLogger(__name__)

@staticmethod
def prepare(data):
    logger.info(f"Click Prepare: {data}")
    # ... rest of code
```

### Test Script

```python
# test_click_payment.py
import requests
import hashlib

def test_click_prepare():
    url = "https://eduself.uz/subscriptions/payment/click/prepare/"
    
    data = {
        'click_trans_id': '123456789',
        'service_id': 'YOUR_SERVICE_ID',
        'merchant_trans_id': '1',  # Payment ID
        'amount': '79000',
        'action': '0',
        'sign_time': '2024-01-01 12:00:00',
    }
    
    # Calculate signature
    signature_string = f"{data['click_trans_id']}{data['service_id']}YOUR_SECRET_KEY{data['merchant_trans_id']}{data['amount']}{data['action']}{data['sign_time']}"
    data['sign_string'] = hashlib.md5(signature_string.encode()).hexdigest()
    
    response = requests.post(url, data=data)
    print(response.json())

if __name__ == '__main__':
    test_click_prepare()
```

## 11. Success Criteria

To'lov muvaffaqiyatli bo'lishi uchun:

- [ ] Payment status `completed`
- [ ] Transaction ID saqlangan
- [ ] UserSubscription yaratilgan
- [ ] Subscription status `active`
- [ ] End date to'g'ri
- [ ] User'ga email yuborilgan (agar sozlangan bo'lsa)

## 12. Support

Agar muammo bo'lsa:

1. **Server logs** tekshiring
2. **Database** tekshiring
3. **Click merchant panel** tekshiring
4. **Signature** to'g'ri hisoblanyotganini tekshiring
5. **HTTPS** ishlayotganini tekshiring

## Qo'shimcha Resurslar

- Click API dokumentatsiyasi: https://docs.click.uz/
- Click merchant panel: https://my.click.uz/
- EduSelf support: eduselfuz@gmail.com

---

**Muvaffaqiyatli test qilish!** 🎉
