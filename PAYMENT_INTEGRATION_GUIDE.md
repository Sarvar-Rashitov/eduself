# Payment Integration Guide - Click va Payme

## Umumiy ma'lumot

EduSelf platformasida Click va Payme to'lov tizimlari integratsiya qilingan.

## Click Integration

### 1. Click Merchant Account

1. Click merchant account yaratish: https://my.click.uz/
2. Merchant ID, Service ID va Secret Key olish
3. Callback URL'larni sozlash

### 2. Environment Variables

`.env` faylida:

```env
CLICK_MERCHANT_ID=your_merchant_id
CLICK_SERVICE_ID=your_service_id
CLICK_SECRET_KEY=your_secret_key
CLICK_MERCHANT_USER_ID=your_merchant_user_id
```

### 3. Callback URL'lar

Click merchant panelida quyidagi URL'larni sozlang:

**Prepare URL:**
```
https://eduself.uz/subscriptions/payment/click/prepare/
```

**Complete URL:**
```
https://eduself.uz/subscriptions/payment/click/complete/
```

### 4. Click API Flow

1. **Prepare** - To'lovni tayyorlash va tekshirish
   - Signature tekshirish
   - Payment ID va summa tekshirish
   - Payment status'ni `processing` ga o'zgartirish

2. **Complete** - To'lovni tasdiqlash
   - Signature tekshirish
   - Payment status'ni `completed` ga o'zgartirish
   - UserSubscription yaratish
   - Promokodni ishlatish

### 5. Click Test

Test muhitida:

```
https://my.click.uz/services/pay?service_id=YOUR_SERVICE_ID&merchant_id=YOUR_MERCHANT_ID&amount=79000&transaction_param=PAYMENT_ID
```

### 6. Click Signature

Signature yaratish:

```python
import hashlib

signature_string = (
    f"{click_trans_id}"
    f"{service_id}"
    f"{secret_key}"
    f"{merchant_trans_id}"
    f"{amount}"
    f"{action}"
    f"{sign_time}"
)

signature = hashlib.md5(signature_string.encode()).hexdigest()
```

## Payme Integration

### 1. Payme Merchant Account

1. Payme merchant account yaratish: https://business.paycom.uz/
2. Merchant ID va Secret Key olish
3. Callback URL sozlash

### 2. Environment Variables

`.env` faylida:

```env
PAYME_MERCHANT_ID=your_merchant_id
PAYME_SECRET_KEY=your_secret_key
PAYME_ENDPOINT=https://checkout.paycom.uz
```

### 3. Callback URL

Payme merchant panelida:

```
https://eduself.uz/subscriptions/payment/payme/callback/
```

### 4. Payme API Flow (JSON-RPC 2.0)

Payme JSON-RPC 2.0 protokolidan foydalanadi.

**Metodlar:**

1. **CheckPerformTransaction** - To'lovni amalga oshirish mumkinligini tekshirish
2. **CreateTransaction** - Tranzaksiya yaratish
3. **PerformTransaction** - To'lovni amalga oshirish
4. **CancelTransaction** - Tranzaksiyani bekor qilish
5. **CheckTransaction** - Tranzaksiya holatini tekshirish

### 5. Payme Authorization

Payme Basic Authentication ishlatadi:

```
Authorization: Basic base64(Paycom:SECRET_KEY)
```

### 6. Payme Request Format

```json
{
    "jsonrpc": "2.0",
    "id": 123,
    "method": "CheckPerformTransaction",
    "params": {
        "amount": 7900000,
        "account": {
            "payment_id": "123"
        }
    }
}
```

### 7. Payme Response Format

```json
{
    "jsonrpc": "2.0",
    "id": 123,
    "result": {
        "allow": true
    }
}
```

### 8. Payme Amount Format

Payme tiyin'da ishlaydi:
- 1 so'm = 100 tiyin
- 79,000 so'm = 7,900,000 tiyin

## Payment Flow

### 1. Foydalanuvchi to'lov qiladi

```
User -> Subscribe page -> Select payment method -> Payment gateway
```

### 2. Payment yaratiladi

```python
payment = Payment.objects.create(
    user=user,
    plan=plan,
    payment_method='click',  # yoki 'payme'
    amount=plan.price,
    discount_amount=discount,
    final_amount=final_amount,
    promo_code=promo,
    status='pending'
)
```

### 3. To'lov gateway'ga yo'naltiriladi

**Click:**
```
https://my.click.uz/services/pay?service_id=...&merchant_id=...&amount=...&transaction_param=PAYMENT_ID
```

**Payme:**
```
https://checkout.paycom.uz/MERCHANT_ID?amount=...&account[payment_id]=PAYMENT_ID
```

### 4. Callback qabul qilinadi

Payment gateway callback yuboradi:
- Click: Prepare -> Complete
- Payme: CheckPerformTransaction -> CreateTransaction -> PerformTransaction

### 5. Obuna yaratiladi

```python
subscription = UserSubscription.objects.create(
    user=payment.user,
    plan=payment.plan,
    start_date=timezone.now(),
    end_date=timezone.now() + timedelta(days=payment.plan.duration_days),
    status='active',
    acquired_via='payment'
)
```

## Error Handling

### Click Error Codes

- `-1`: SIGN CHECK FAILED
- `-2`: Incorrect parameter amount
- `-4`: Already paid
- `-5`: Transaction not found
- `-8`: Error

### Payme Error Codes

- `-32504`: Insufficient privilege
- `-32700`: Parse error
- `-31001`: Incorrect amount
- `-31003`: Transaction not found
- `-31050`: Payment not found

## Security

### 1. Signature Verification

Har bir so'rovda signature tekshiriladi:

```python
if not ClickPaymentHandler.verify_signature(data):
    return {'error': -1, 'error_note': 'SIGN CHECK FAILED'}
```

### 2. CSRF Exempt

Payment callback'lar CSRF exempt:

```python
@csrf_exempt
def click_prepare(request):
    ...
```

### 3. Authorization

Payme authorization tekshiriladi:

```python
if not PaymePaymentHandler.check_auth(request):
    return {'error': {'code': -32504, 'message': 'Insufficient privilege'}}
```

### 4. Amount Verification

Summa har doim tekshiriladi:

```python
if float(payment.final_amount) != amount:
    return {'error': -2, 'error_note': 'Incorrect parameter amount'}
```

## Testing

### Local Testing

1. ngrok yoki localtunnel ishlatish:
```bash
ngrok http 8000
```

2. Callback URL'ni ngrok URL'ga o'zgartirish:
```
https://your-ngrok-url.ngrok.io/subscriptions/payment/click/prepare/
```

### Production Testing

1. Test merchant account ishlatish
2. Test to'lovlar qilish
3. Callback'lar to'g'ri ishlashini tekshirish

## Monitoring

### Payment Logs

Admin panelda:
- Obunalar > To'lovlar
- Har bir to'lov uchun:
  - Status
  - Transaction ID
  - Payment data (JSON)

### Database Queries

```sql
-- Pending to'lovlar
SELECT * FROM subscriptions_payment WHERE status = 'pending';

-- Completed to'lovlar
SELECT * FROM subscriptions_payment WHERE status = 'completed';

-- Failed to'lovlar
SELECT * FROM subscriptions_payment WHERE status = 'failed';
```

## Troubleshooting

### 1. Callback ishlamayapti

- URL to'g'ri sozlanganligini tekshiring
- HTTPS ishlatilayotganligini tekshiring
- Signature to'g'ri hisoblanyotganligini tekshiring

### 2. Signature xatosi

- Secret key to'g'ri ekanligini tekshiring
- Signature string to'g'ri formatda ekanligini tekshiring

### 3. Amount xatosi

- Payme uchun tiyin'da yuborilayotganligini tekshiring
- Click uchun so'm'da yuborilayotganligini tekshiring

## Production Checklist

- [ ] Merchant account yaratilgan
- [ ] API kalitlar `.env` faylida
- [ ] Callback URL'lar sozlangan
- [ ] HTTPS ishlatilmoqda
- [ ] Signature verification ishlayapti
- [ ] Test to'lovlar muvaffaqiyatli
- [ ] Error handling to'g'ri
- [ ] Monitoring sozlangan

## Support

- Click support: https://click.uz/support
- Payme support: https://paycom.uz/support
- EduSelf support: eduselfuz@gmail.com
