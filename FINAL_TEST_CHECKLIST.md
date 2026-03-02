# EduSelf Pro - Yakuniy Test Checklist

## ✅ Test qilish ro'yxati

### 1. Server ishga tushirish
```bash
python manage.py runserver
```
- [ ] Server muvaffaqiyatli ishga tushdi
- [ ] http://127.0.0.1:8000/ ochiladi

### 2. Sample data yaratish
```bash
python manage.py create_sample_plans
```
- [ ] 3 ta ta'rif yaratildi (Basic, Pro, Premium)
- [ ] 2 ta referal dasturi yaratildi

### 3. Oddiy foydalanuvchi test

#### Bosh sahifa
- [ ] Login qiling
- [ ] Lives system pastida "EduSelf Pro" banner ko'rinadi (ko'k gradient)
- [ ] Banner'ga bosing - Pro sahifasiga o'tadi

#### Profil sahifasi
- [ ] Profil sahifasiga o'ting
- [ ] Statistika pastida "EduSelf Pro'ga o'ting" section ko'rinadi (ko'k gradient)
- [ ] Section'ga bosing - Pro sahifasiga o'tadi

#### Pro sahifasi
- [ ] 3 ta ta'rif ko'rinadi
- [ ] Har bir ta'rifda narx, muddat, xususiyatlar ko'rinadi
- [ ] "Sotib olish" tugmalari ishlaydi
- [ ] Referal dasturi banner ko'rinadi

#### Subscribe sahifasi
- [ ] Biror ta'rifni tanlang
- [ ] Subscribe sahifasi ochiladi
- [ ] Promokod maydoni ko'rinadi
- [ ] To'lov usuli tanlash mumkin (Click/Payme)

### 4. Pro foydalanuvchi test

#### Test obuna berish
```bash
python manage.py test_subscription
```
- [ ] Birinchi foydalanuvchiga Pro obuna berildi
- [ ] 30 kunlik muddat ko'rsatildi

#### Bosh sahifa (Pro foydalanuvchi)
- [ ] Sahifani yangilang
- [ ] Lives system pastida hozirgi ta'rif ko'rinadi (yashil gradient)
- [ ] Ta'rif nomi: "EduSelf Pro"
- [ ] Muddat ko'rsatiladi: "30.03.2026 gacha faol"
- [ ] Banner'ga bosing - "Mening obunalarim" sahifasiga o'tadi

#### Profil sahifasi (Pro foydalanuvchi)
- [ ] Profil sahifasiga o'ting
- [ ] Statistika pastida hozirgi ta'rif ko'rinadi (yashil gradient)
- [ ] Ta'rif nomi va muddat ko'rsatiladi
- [ ] Section'ga bosing - "Mening obunalarim" sahifasiga o'tadi

#### Pro sahifasi (Pro foydalanuvchi)
- [ ] Yuqorida faol obuna haqida ma'lumot (yashil alert)
- [ ] Foydalanish statistikasi ko'rinadi (progress bar'lar)
- [ ] Hozirgi ta'rifda "Hozirgi ta'rif" badge (yashil)
- [ ] Hozirgi ta'rifda "Faol obuna" tugmasi (yashil)
- [ ] Boshqa ta'riflarda "Sotib olish" tugmasi

#### Mening obunalarim sahifasi
- [ ] Faol obuna ko'rinadi
- [ ] Ta'rif nomi, muddat ko'rsatiladi
- [ ] Status: "Faol" (yashil badge)

### 5. Admin panel test

#### Ta'riflar
- [ ] Admin panelga kiring: http://127.0.0.1:8000/nokia/
- [ ] "Obunalar" > "Ta'riflar"
- [ ] 3 ta ta'rif ko'rinadi
- [ ] Har birini tahrirlash mumkin

#### Promokod yaratish
- [ ] "Obunalar" > "Promokodlar" > "Yangi promokod qo'shish"
- [ ] Kod: TEST50
- [ ] Ta'rif: EduSelf Pro
- [ ] Chegirma: 50%
- [ ] Muddat: 30 kun
- [ ] Saqlang

#### Promokod test qilish
- [ ] Subscribe sahifasiga o'ting
- [ ] Promokod maydoniga "TEST50" kiriting
- [ ] "Tekshirish" tugmasini bosing
- [ ] Chegirma qo'llaniladi
- [ ] Yangi narx ko'rsatiladi

#### Foydalanuvchi obunalari
- [ ] "Obunalar" > "Foydalanuvchi obunalari"
- [ ] Test obuna ko'rinadi
- [ ] Status: Faol
- [ ] Qanday olingan: admin

### 6. Referal dasturi test

#### Referal sahifasi
- [ ] http://127.0.0.1:8000/subscriptions/referral/
- [ ] Faol dasturlar ko'rinadi
- [ ] Har bir dastur uchun shartlar ko'rsatiladi
- [ ] "Ulashish" tugmasi ishlaydi

### 7. User metodlari test

Django shell'da:
```bash
python manage.py shell
```

```python
from accounts.models import User

user = User.objects.first()

# Faol obunani olish
subscription = user.get_active_subscription()
print(f"Subscription: {subscription}")  # EduSelf Pro

# Pro foydalanuvchimi?
print(f"Is Pro: {user.is_pro_user()}")  # True

# Cheksiz yurakchalar bormi?
print(f"Unlimited lives: {user.has_unlimited_lives()}")  # True

# Xususiyatdan foydalanish mumkinmi?
print(f"Can use AI: {user.can_use_feature('ai_analysis')}")  # True
```

- [ ] Barcha metodlar to'g'ri ishlaydi

### 8. Gradient va dizayn test

#### Ko'k gradient (Oddiy foydalanuvchi)
- [ ] Bosh sahifada banner ko'k gradient
- [ ] Profil sahifasida section ko'k gradient
- [ ] Hover effekt ishlaydi

#### Yashil gradient (Pro foydalanuvchi)
- [ ] Bosh sahifada banner yashil gradient
- [ ] Profil sahifasida section yashil gradient
- [ ] Pro sahifasida alert yashil
- [ ] Hozirgi ta'rif badge yashil
- [ ] Hover effekt ishlaydi

### 9. Mobile responsive test

- [ ] Bosh sahifa mobile'da to'g'ri ko'rinadi
- [ ] Profil sahifasi mobile'da to'g'ri ko'rinadi
- [ ] Pro sahifasi mobile'da to'g'ri ko'rinadi
- [ ] Subscribe sahifasi mobile'da to'g'ri ko'rinadi
- [ ] Barcha tugmalar bosiladi

### 10. Error handling test

#### Noto'g'ri promokod
- [ ] Subscribe sahifasida noto'g'ri promokod kiriting
- [ ] "Promokod topilmadi" xabari ko'rinadi

#### Muddati o'tgan promokod
- [ ] Admin panelda promokod muddatini o'tgan qilib qo'ying
- [ ] "Promokod amal qilmaydi" xabari ko'rinadi

## ✅ Barcha testlar o'tdi!

Agar barcha testlar muvaffaqiyatli o'tsa, tizim production'ga tayyor!

## 🚀 Production'ga deploy qilish

1. Click va Payme merchant account yaratish
2. Production API kalitlarni `.env` fayliga qo'shish
3. Callback URL'larni sozlash
4. HTTPS sozlash
5. Deploy qilish

## 📝 Qo'shimcha

- Barcha dokumentatsiya: EDUSELF_PRO_GUIDE.md
- Test qilish: TESTING_GUIDE.md
- Payment integration: PAYMENT_INTEGRATION_GUIDE.md
- Summary: EDUSELF_PRO_SUMMARY.md
