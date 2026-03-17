# EduSelf Pro - Test Qilish Qo'llanmasi

## Server ishga tushirish

```bash
python manage.py runserver
```

Server manzili: http://127.0.0.1:8000/

## Test qilish bosqichlari

### 0. Test obuna berish (ixtiyoriy)

Birinchi foydalanuvchiga test uchun Pro obuna berish:

```bash
python manage.py test_subscription
```

Bu buyruq:
- Birinchi foydalanuvchiga Pro obuna beradi
- 30 kunlik muddat bilan
- Admin tomonidan berilgan deb belgilaydi

### 1. Bosh sahifada Pro banner ko'rish

**Oddiy foydalanuvchi uchun:**
1. Brauzerda ochish: http://127.0.0.1:8000/
2. Login qiling (agar login qilmagan bo'lsangiz)
3. Lives system pastida **EduSelf Pro** banner ko'rinishi kerak (ko'k gradient)
4. Banner'ga bosing - Pro sahifasiga o'tishi kerak

**Pro foydalanuvchi uchun:**
1. Test obuna bering: `python manage.py test_subscription`
2. Bosh sahifani yangilang
3. Lives system pastida **EduSelf Pro** banner o'rniga **hozirgi ta'rif** ko'rinishi kerak (yashil gradient)
4. Banner'da ta'rif nomi va muddat ko'rinadi
5. Banner'ga bosing - "Mening obunalarim" sahifasiga o'tishi kerak

### 2. Profil sahifasida Pro section ko'rish

**Oddiy foydalanuvchi uchun:**
1. Profil sahifasiga o'ting: http://127.0.0.1:8000/accounts/profile/
2. Statistika pastida **EduSelf Pro'ga o'ting** section ko'rinishi kerak (ko'k gradient)
3. Section'ga bosing - Pro sahifasiga o'tishi kerak

**Pro foydalanuvchi uchun:**
1. Profil sahifasiga o'ting
2. Statistika pastida **hozirgi ta'rif** ko'rinishi kerak (yashil gradient)
3. Ta'rif nomi va muddat ko'rinadi
4. Section'ga bosing - "Mening obunalarim" sahifasiga o'tishi kerak

### 3. Pro sahifasini ko'rish

URL: http://127.0.0.1:8000/subscriptions/pro/

**Oddiy foydalanuvchi uchun:**
- 3 ta ta'rif: Basic, Pro, Premium
- Har bir ta'rifda:
  - Narx va muddat
  - Xususiyatlar ro'yxati
  - "Sotib olish" tugmasi
- Referal dasturi banner

**Pro foydalanuvchi uchun:**
- Yuqorida faol obuna haqida ma'lumot (yashil alert)
- Foydalanish statistikasi (progress bar'lar)
- Barcha ta'riflar ko'rinadi
- Hozirgi ta'rifda "Hozirgi ta'rif" badge (yashil)
- Hozirgi ta'rifda "Faol obuna" tugmasi (yashil)
- Boshqa ta'riflarda "Sotib olish" tugmasi

### 4. Obuna sotib olish jarayoni

1. Pro sahifasida biror ta'rifni tanlang
2. "Sotib olish" tugmasini bosing
3. Subscribe sahifasi ochilishi kerak:
   - Ta'rif ma'lumotlari
   - Promokod kiritish maydoni
   - To'lov usuli tanlash (Click/Payme)
   - "To'lovga o'tish" tugmasi

### 5. Promokod test qilish

#### Admin panelda promokod yaratish:

1. Admin panelga kiring: http://127.0.0.1:8000/nokia/
2. "Obunalar" > "Promokodlar" > "Yangi promokod qo'shish"
3. Ma'lumotlarni to'ldiring:
   - Kod: `TEST50`
   - Ta'rif: EduSelf Pro
   - Chegirma: 50%
   - Muddat: Hozirgi sanadan 30 kun
   - Maksimal foydalanish: 10
4. Saqlang

#### Promokodni test qilish:

1. Subscribe sahifasida promokod maydoniga `TEST50` kiriting
2. "Tekshirish" tugmasini bosing
3. Chegirma qo'llanilishi va yangi narx ko'rinishi kerak

### 6. Referal dasturini test qilish

URL: http://127.0.0.1:8000/subscriptions/referral/

Ko'rinishi kerak:
- Faol referal dasturlari
- Har bir dastur uchun:
  - Shart (nechta do'st taklif qilish kerak)
  - Muddat
  - Mukofot
  - "Ulashish" tugmasi

### 7. Admin panelda monitoring

#### Foydalanuvchi obunalari:

1. Admin panel: http://127.0.0.1:8000/nokia/
2. "Obunalar" > "Foydalanuvchi obunalari"
3. Ko'rinishi kerak:
   - Barcha obunalar ro'yxati
   - Holat (Faol/Muddati tugagan)
   - Foydalanish statistikasi

#### To'lovlar:

1. "Obunalar" > "To'lovlar"
2. Ko'rinishi kerak:
   - Barcha to'lovlar
   - Holat (Kutilmoqda/Bajarilgan)
   - To'lov usuli

### 8. Manual Pro belgilash (Admin)

1. Admin panelda "Obunalar" > "Foydalanuvchi obunalari" > "Yangi obuna qo'shish"
2. Ma'lumotlarni to'ldiring:
   - Foydalanuvchi: tanlang
   - Ta'rif: tanlang
   - Boshlanish sanasi: hozirgi sana
   - Tugash sanasi: 30 kun keyin
   - Holat: Faol
   - Qanday olingan: admin
3. Saqlang

### 9. User metodlarini test qilish

Django shell'da:

```bash
python manage.py shell
```

```python
from accounts.models import User

# Foydalanuvchini olish
user = User.objects.first()

# Faol obunani tekshirish
subscription = user.get_active_subscription()
print(subscription)

# Pro foydalanuvchimi?
print(user.is_pro_user())

# Xususiyatdan foydalanish mumkinmi?
print(user.can_use_feature('ai_analysis'))

# Cheksiz yurakchalar bormi?
print(user.has_unlimited_lives())
```

## Payment Integration Test

### Click Test (Development)

Click test muhitida test qilish uchun:

1. Click merchant account yaratish kerak
2. Test kalitlarni `.env` fayliga qo'shish:
```
CLICK_MERCHANT_ID=test_merchant_id
CLICK_SERVICE_ID=test_service_id
CLICK_SECRET_KEY=test_secret_key
CLICK_MERCHANT_USER_ID=test_user_id
```

3. Click test URL: https://my.click.uz/services/pay?service_id=YOUR_SERVICE_ID&merchant_id=YOUR_MERCHANT_ID&amount=79000&transaction_param=PAYMENT_ID

### Payme Test (Development)

Payme test muhitida test qilish uchun:

1. Payme merchant account yaratish kerak
2. Test kalitlarni `.env` fayliga qo'shish:
```
PAYME_MERCHANT_ID=test_merchant_id
PAYME_SECRET_KEY=test_secret_key
```

3. Payme test URL: https://test.paycom.uz/

## Xatoliklarni tekshirish

### Server log'larini ko'rish:

Terminal'da server ishlab turgan joyda log'lar ko'rinadi.

### Database'ni tekshirish:

```bash
python manage.py dbshell
```

```sql
-- Barcha ta'riflarni ko'rish
SELECT * FROM subscriptions_subscriptionplan;

-- Barcha obunalarni ko'rish
SELECT * FROM subscriptions_usersubscription;

-- Barcha to'lovlarni ko'rish
SELECT * FROM subscriptions_payment;
```

## Keng tarqalgan muammolar

### 1. Migration xatoligi

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Static fayllar yuklanmayapti

```bash
python manage.py collectstatic --noinput
```

### 3. Template topilmayapti

`TEMPLATES` sozlamalarini tekshiring `settings.py` da.

### 4. Payment callback ishlamayapti

- CSRF exempt decorator qo'shilganligini tekshiring
- URL'lar to'g'ri sozlanganligini tekshiring
- Payment handler'lar to'g'ri import qilinganligini tekshiring

## Production'ga deploy qilish

### 1. Environment variables

`.env` faylida production kalitlarni sozlang:

```
# Click Production
CLICK_MERCHANT_ID=your_production_merchant_id
CLICK_SERVICE_ID=your_production_service_id
CLICK_SECRET_KEY=your_production_secret_key
CLICK_MERCHANT_USER_ID=your_production_user_id

# Payme Production
PAYME_MERCHANT_ID=your_production_merchant_id
PAYME_SECRET_KEY=your_production_secret_key
PAYME_ENDPOINT=https://checkout.paycom.uz
```

### 2. Callback URL'larni sozlash

Click va Payme merchant panellarida callback URL'larni sozlang:

- Click Prepare: `https://eduself.uz/subscriptions/payment/click/prepare/`
- Click Complete: `https://eduself.uz/subscriptions/payment/click/complete/`
- Payme Callback: `https://eduself.uz/subscriptions/payment/payme/callback/`

### 3. HTTPS

Production'da HTTPS ishlatish majburiy!

### 4. Security

- `DEBUG = False` qiling
- `SECRET_KEY` ni xavfsiz saqlang
- `ALLOWED_HOSTS` ni to'g'ri sozlang

## Qo'shimcha resurslar

- Click API dokumentatsiyasi: https://docs.click.uz/
- Payme API dokumentatsiyasi: https://developer.help.paycom.uz/

## Yordam

Agar muammo yuzaga kelsa:

1. Server log'larini tekshiring
2. Browser console'ni tekshiring
3. Database'ni tekshiring
4. Payment handler'lar to'g'ri ishlayotganini tekshiring

## Muvaffaqiyatli test!

Barcha xususiyatlar ishlashi kerak. Agar muammo bo'lsa, yuqoridagi qadamlarni takrorlang.
