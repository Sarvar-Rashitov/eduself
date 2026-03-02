# Local Test Qo'llanmasi

## Local va Production Farqi

### Local (DEBUG=True)
- To'lov faqat yaratiladi
- Click/Payme sahifasiga yo'naltirilmaydi
- Qo'lda to'lovni complete qilish kerak
- Test skriptlar ishlaydi

### Production (DEBUG=False)
- To'lov yaratiladi
- Click/Payme sahifasiga yo'naltiriladi
- Callback URL'lar avtomatik chaqiriladi
- Obuna avtomatik yaratiladi

## Local Test Qilish

### 1. Serverni Ishga Tushirish

```bash
python manage.py runserver
```

### 2. Brauzerda Test Qilish

1. http://127.0.0.1:8000/subscriptions/pro/ ga o'ting
2. Ta'rifni tanlang (masalan, "Basic")
3. To'lov usulini tanlang (Click yoki Payme)
4. "To'lovga o'tish" tugmasini bosing

**Natija:**
```
✅ To'lov yaratildi! Payment ID: 15
ℹ️ Local test rejimi: Click to'lov production'da ishlaydi.
💡 Test uchun: python test_click_payment.py
```

### 3. To'lovni Qo'lda Complete Qilish

#### Variant 1: Management Command

```bash
python manage.py complete_test_payment 15
```

**Natija:**
```
✅ To'lov muvaffaqiyatli bajarildi!
   Payment ID: 15
   Foydalanuvchi: John Doe
   Ta'rif: Basic Plan
   Summa: 50000 so'm
   Obuna ID: 5
   Muddat: 02.03.2026 - 01.04.2026
```

#### Variant 2: Django Shell

```bash
python manage.py shell
```

```python
from subscriptions.models import Payment, UserSubscription
from django.utils import timezone
from datetime import timedelta

# To'lovni topish
payment = Payment.objects.get(id=15)

# To'lovni tasdiqlash
payment.status = 'completed'
payment.completed_at = timezone.now()
payment.transaction_id = f'TEST_{payment.id}'
payment.save()

# Obuna yaratish
subscription = UserSubscription.objects.create(
    user=payment.user,
    plan=payment.plan,
    start_date=timezone.now(),
    end_date=timezone.now() + timedelta(days=payment.plan.duration_days),
    status='active',
    acquired_via='payment'
)

payment.subscription = subscription
payment.save()

print(f"✅ To'lov bajarildi! Obuna ID: {subscription.id}")
```

#### Variant 3: Admin Panel

1. http://127.0.0.1:8000/admin/ ga kiring
2. **Subscriptions** → **Payments** ga o'ting
3. To'lovni tanlang (ID: 15)
4. **Status** ni `completed` ga o'zgartiring
5. **Completed at** ni hozirgi vaqtga o'zgartiring
6. **Save** tugmasini bosing
7. **Subscriptions** → **User subscriptions** ga o'ting
8. **Add user subscription** tugmasini bosing
9. Formani to'ldiring va saqlang

### 4. Natijani Tekshirish

#### Brauzerda

1. http://127.0.0.1:8000/subscriptions/my-subscriptions/ ga o'ting
2. Obunangizni ko'ring

#### Admin Panelda

1. http://127.0.0.1:8000/admin/subscriptions/payment/ - To'lovlar
2. http://127.0.0.1:8000/admin/subscriptions/usersubscription/ - Obunalar

#### Django Shell

```python
from accounts.models import User
from subscriptions.models import UserSubscription

user = User.objects.get(email='your@email.com')

# Pro user ekanligini tekshirish
print(f"Pro user: {user.is_pro_user()}")

# Faol obunani ko'rish
subscription = user.get_active_subscription()
if subscription:
    print(f"Faol obuna: {subscription.plan.name}")
    print(f"Muddat: {subscription.end_date}")
else:
    print("Faol obuna yo'q")
```

## Test Skriptlar

### 1. Click To'lov Tizimini Test Qilish

```bash
python test_click_payment.py
```

Bu skript:
- Test foydalanuvchi yaratadi
- Test ta'rif yaratadi
- To'lov yaratadi
- Prepare API'ni chaqiradi
- Complete API'ni chaqiradi
- Obuna yaratadi
- Natijalarni ko'rsatadi

### 2. Xatolik Ssenariylari

```bash
python test_click_error_scenarios.py
```

Bu skript:
- Noto'g'ri signature
- Noto'g'ri summa
- Mavjud bo'lmagan to'lov
- Allaqachon to'langan to'lov
- Prepare bo'lmagan complete

### 3. Referal Tizimini Test Qilish

```bash
python test_referral_system.py
```

## Production'ga O'tish

### 1. DEBUG'ni O'chirish

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['eduself.uz', 'www.eduself.uz']
```

### 2. HTTPS Sozlash

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name eduself.uz;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### 3. Click Callback URL'larni Sozlash

Click merchant panelda:
- Prepare: `https://eduself.uz/subscriptions/payment/click/prepare/`
- Complete: `https://eduself.uz/subscriptions/payment/click/complete/`

### 4. Test Qilish

1. Production saytga o'ting: https://eduself.uz
2. Pro sahifasiga o'ting
3. Ta'rifni tanlang
4. Click to'lov usulini tanlang
5. Test kartadan foydalaning:
   ```
   Karta: 8600 0000 0000 0000
   Muddat: 03/99
   CVV: 123
   SMS: 666666
   ```

## Monitoring

### Loglarni Ko'rish

```bash
# Django logs
tail -f /var/log/eduself/django.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Database Queries

```sql
-- Bugungi to'lovlar
SELECT * FROM subscriptions_payment 
WHERE DATE(created_at) = CURRENT_DATE;

-- Faol obunalar
SELECT * FROM subscriptions_usersubscription 
WHERE status = 'active' AND end_date > NOW();

-- Pro userlar
SELECT u.* FROM accounts_user u
JOIN subscriptions_usersubscription s ON u.id = s.user_id
WHERE s.status = 'active' AND s.end_date > NOW();
```

## Xatoliklarni Tuzatish

### Xatolik: "name 'settings' is not defined"

**Yechim:**
```python
# subscriptions/views.py
from django.conf import settings  # Bu qator bor ekanligini tekshiring
```

### Xatolik: "NoReverseMatch at /subscriptions/subscribe/"

**Yechim:**
- URL pattern'ni tekshiring
- `payment_id` parametri kerak bo'lmasa, uni o'chiring

### Xatolik: To'lov yaratildi, lekin obuna yo'q

**Yechim:**
```bash
# Qo'lda complete qiling
python manage.py complete_test_payment PAYMENT_ID
```

## Xulosa

Local test uchun:
1. ✅ Serverni ishga tushiring
2. ✅ Brauzerda to'lov yarating
3. ✅ Qo'lda complete qiling
4. ✅ Natijani tekshiring

Production uchun:
1. ✅ DEBUG=False qiling
2. ✅ HTTPS sozlang
3. ✅ Callback URL'larni sozlang
4. ✅ Test qiling

Agar qiyinchilik bo'lsa, test skriptlardan foydalaning! 🚀
