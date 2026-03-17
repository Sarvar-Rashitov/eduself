# Donat Tizimini Test Qilish

## Local Test (DEBUG=True)

### 1. Serverni Ishga Tushirish

```bash
python manage.py runserver
```

### 2. Donat Sahifasiga O'tish

http://127.0.0.1:8000/subscriptions/donate/

### 3. Donat Qilish

1. Summani kiriting (minimal 1000 so'm)
2. Xabar yozing (ixtiyoriy)
3. To'lov usulini tanlang (Click yoki Payme)
4. "Donat qilish" tugmasini bosing

**Natija:**
```
✅ Donat yaratildi! Donation ID: 5
ℹ️ Local test rejimi: Click to'lov production'da ishlaydi.
```

### 4. Donatni Complete Qilish

```bash
python manage.py complete_test_donation 5
```

**Natija:**
```
✅ Donat muvaffaqiyatli bajarildi!
   Donation ID: 5
   Foydalanuvchi: John Doe
   Summa: 10000 so'm
   Xabar: Rahmat!
   Bajarilgan: 02.03.2026 22:30
```

### 5. Admin Panelda Ko'rish

http://127.0.0.1:8000/admin/subscriptions/donation/

## Production Test (DEBUG=False)

### 1. Render.com'da DEBUG=False Qilish

1. https://dashboard.render.com ga kiring
2. Service'ni tanlang
3. **Environment** → **Environment Variables**
4. `DEBUG=False` qiling
5. Service'ni qayta ishga tushiring

### 2. Production'da Test Qilish

1. https://eduself.uz/subscriptions/donate/ ga o'ting
2. Summani kiriting
3. To'lov usulini tanlang
4. "Donat qilish" tugmasini bosing

**Natija:**
- ✅ Click to'lov sahifasiga yo'naltirilasiz
- ✅ To'lovni amalga oshiring
- ✅ Donat avtomatik complete bo'ladi

## Donat vs Obuna Farqi

### Donat
- Transaction param: `DONATE_{donation_id}`
- Return URL: `/subscriptions/donate/`
- Obuna yaratilmaydi
- Faqat rahmat xabari

### Obuna
- Transaction param: `{payment_id}`
- Return URL: `/subscriptions/my-subscriptions/`
- Obuna yaratiladi
- Pro user bo'ladi

## Click Callback URL'lar

Donat uchun ham xuddi obuna kabi callback URL'lar ishlaydi:

### Prepare URL
```
https://eduself.uz/subscriptions/payment/click/prepare/
```

### Complete URL
```
https://eduself.uz/subscriptions/payment/click/complete/
```

**Farqi:**
- `merchant_trans_id` parametri `DONATE_` prefixi bilan keladi
- Callback handler donat ekanligini aniqlaydi
- Obuna yaratilmaydi, faqat donat complete bo'ladi

## Donat Callback Handler

Donat uchun alohida callback handler kerak. Keling, qo'shamiz:

### payment_handlers.py ga qo'shish

```python
@staticmethod
def complete(data):
    """
    Click Complete API
    To'lovni tasdiqlash va obuna/donat yaratish
    """
    # ... mavjud kod ...
    
    merchant_trans_id = data.get('merchant_trans_id')
    
    # Donat ekanligini tekshirish
    if merchant_trans_id.startswith('DONATE_'):
        donation_id = merchant_trans_id.replace('DONATE_', '')
        try:
            donation = Donation.objects.get(id=donation_id)
            
            # Donatni tasdiqlash
            donation.status = 'completed'
            donation.completed_at = timezone.now()
            donation.transaction_id = data.get('click_trans_id')
            donation.payment_data = data
            donation.save()
            
            return {
                'error': 0,
                'error_note': 'Success',
                'click_trans_id': data.get('click_trans_id'),
                'merchant_trans_id': merchant_trans_id,
                'merchant_confirm_id': donation.id
            }
        except Donation.DoesNotExist:
            return {
                'error': -5,
                'error_note': 'Donation not found'
            }
    
    # Obuna uchun mavjud kod davom etadi...
```

## Test Ssenariysi

### Ssenariy 1: Minimal Donat

```bash
# 1. Donat qilish
Summa: 1000 so'm
Xabar: (bo'sh)
To'lov: Click

# 2. Complete qilish
python manage.py complete_test_donation 1

# 3. Natija
✅ Donat bajarildi
```

### Ssenariy 2: Katta Donat

```bash
# 1. Donat qilish
Summa: 100000 so'm
Xabar: "Ajoyib platforma! Rahmat!"
To'lov: Click

# 2. Complete qilish
python manage.py complete_test_donation 2

# 3. Natija
✅ Donat bajarildi
Xabar ko'rsatiladi
```

### Ssenariy 3: Minimal Summadan Kam

```bash
# 1. Donat qilish
Summa: 500 so'm

# 2. Natija
❌ Minimal donat summasi 1000 so'm
```

## Database Queries

### Barcha donatlarni ko'rish

```sql
SELECT * FROM subscriptions_donation 
ORDER BY created_at DESC;
```

### Bugungi donatlar

```sql
SELECT * FROM subscriptions_donation 
WHERE DATE(created_at) = CURRENT_DATE;
```

### Jami donat summasi

```sql
SELECT SUM(amount) as total 
FROM subscriptions_donation 
WHERE status = 'completed';
```

### Eng ko'p donat qilganlar

```sql
SELECT 
    u.first_name, 
    u.last_name, 
    COUNT(*) as count,
    SUM(d.amount) as total
FROM subscriptions_donation d
JOIN accounts_user u ON d.user_id = u.id
WHERE d.status = 'completed'
GROUP BY u.id
ORDER BY total DESC
LIMIT 10;
```

## Admin Panel

### Donatlarni Ko'rish

http://127.0.0.1:8000/admin/subscriptions/donation/

### Filtrlash

- Status bo'yicha (pending, completed, failed)
- Sana bo'yicha
- Foydalanuvchi bo'yicha
- To'lov usuli bo'yicha

### Export

Admin panelda "Export to CSV" funksiyasini qo'shish mumkin.

## Xulosa

### Local Test
```bash
# 1. Donat qilish
http://127.0.0.1:8000/subscriptions/donate/

# 2. Complete qilish
python manage.py complete_test_donation DONATION_ID

# 3. Ko'rish
http://127.0.0.1:8000/admin/subscriptions/donation/
```

### Production Test
```bash
# 1. Donat qilish
https://eduself.uz/subscriptions/donate/

# 2. Click to'lov
Avtomatik yo'naltiriladi

# 3. Callback
Avtomatik complete bo'ladi
```

Donat tizimi tayyor! 💰
