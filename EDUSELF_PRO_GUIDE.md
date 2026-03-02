# EduSelf Pro - Premium Subscription Tizimi

## Umumiy ma'lumot

EduSelf Pro - bu platformaning premium obuna tizimi bo'lib, foydalanuvchilarga qo'shimcha imkoniyatlar va cheklovlarni olib tashlash imkonini beradi.

## Asosiy xususiyatlar

### 1. Subscription Plans (Ta'riflar)
- Turli xil ta'riflar yaratish imkoniyati
- Har bir ta'rif uchun:
  - Narx va muddat
  - Cheksiz yurakchalar
  - AI tahlil limiti
  - AI hamroh limiti
  - Universitet imtihoni limiti
  - Mock exam limiti
  - Sertifikat test limiti

### 2. Payment Integration (To'lov integratsiyasi)
- **Click** to'lov tizimi
- **Payme** to'lov tizimi
- To'lov tarixi va monitoring

### 3. Promo Codes (Promokodlar)
- Foiz yoki summa asosida chegirma
- Muddat va foydalanish cheklovi
- Har bir ta'rif uchun alohida promokod

### 4. Referral System (Referal dasturi)
- Do'stlarni taklif qilish orqali bepul obuna
- Har bir dastur uchun:
  - Kerakli taklif soni
  - Taklif muddati
  - Mukofot muddati
- Jarayon monitoring

### 5. Admin Panel
- Barcha ta'riflarni boshqarish
- Promokodlar yaratish va boshqarish
- Referal dasturlarini sozlash
- Foydalanuvchilarni Pro deb belgilash
- To'lovlar va donatlar monitoring

### 6. Frontend (Mobile-first)
- **Bosh sahifa**: Lives system pastida EduSelf Pro banner
- **Profil sahifasi**: Statistika pastida EduSelf Pro section
- **Pro sahifasi**: Barcha ta'riflar va xususiyatlar
- **Referal sahifasi**: Do'stlarni taklif qilish
- **Donat sahifasi**: Loyihani qo'llab-quvvatlash

## Fayllar strukturasi

```
subscriptions/
├── models.py              # Barcha modellar
├── admin.py               # Admin panel sozlamalari
├── views.py               # View'lar
├── urls.py                # URL routing
├── apps.py                # App konfiguratsiyasi
└── migrations/            # Database migrations

templates/subscriptions/
├── pro_page.html          # Asosiy Pro sahifasi
├── subscribe.html         # Obuna sotib olish
├── referral.html          # Referal dasturi
├── donate.html            # Donat sahifasi
└── my_subscriptions.html  # Foydalanuvchi obunalari
```

## Modellar

### SubscriptionPlan
Ta'riflar - narx, muddat, cheklovlar

### UserSubscription
Foydalanuvchi obunalari - holat, muddat, foydalanish statistikasi

### PromoCode
Promokodlar - chegirma, muddat, foydalanish limiti

### ReferralProgram
Referal dasturlari - shartlar, mukofot

### UserReferral
Foydalanuvchi referallari

### ReferralProgress
Referal jarayoni - progress tracking

### Payment
To'lovlar - Click, Payme integratsiyasi

### Donation
Donatlar - loyihani qo'llab-quvvatlash

## Admin panel

Admin panelda quyidagi imkoniyatlar mavjud:

1. **Ta'riflar**: Yangi ta'rif qo'shish, tahrirlash
2. **Promokodlar**: Promokod yaratish, monitoring
3. **Referal dasturlari**: Dastur sozlash
4. **Foydalanuvchi obunalari**: Monitoring, manual aktivatsiya
5. **To'lovlar**: To'lov tarixi, status
6. **Donatlar**: Donat tarixi

## User metodlari

```python
# Faol obunani olish
user.get_active_subscription()

# Pro foydalanuvchimi?
user.is_pro_user()

# Xususiyatdan foydalanish mumkinmi?
user.can_use_feature('ai_analysis')

# Xususiyatdan foydalanish
user.use_feature('ai_analysis')

# Cheksiz yurakchalar bormi?
user.has_unlimited_lives()
```

## URL'lar

```
/subscriptions/pro/                    # EduSelf Pro sahifasi
/subscriptions/subscribe/<slug>/       # Obuna sotib olish
/subscriptions/check-promo/            # Promokod tekshirish (AJAX)
/subscriptions/referral/               # Referal sahifasi
/subscriptions/referral/invite/        # Referal taklif yuborish
/subscriptions/donate/                 # Donat sahifasi
/subscriptions/my-subscriptions/       # Foydalanuvchi obunalari
```

## To'lov integratsiyasi

### Click
- Prepare API: `/subscriptions/payment/click/prepare/`
- Complete API: `/subscriptions/payment/click/complete/`

### Payme
- Callback API: `/subscriptions/payment/payme/callback/`

## Keyingi qadamlar

1. ✅ Modellar yaratildi
2. ✅ Admin panel sozlandi
3. ✅ View'lar va URL'lar yaratildi
4. ✅ Frontend template'lar yaratildi
5. ✅ Bosh sahifa va profil sahifasiga section qo'shildi
6. ⏳ Click va Payme integratsiyasi (API kalitlar kerak)
7. ⏳ Migration qo'llash: `python manage.py migrate`
8. ⏳ Admin panelda ta'riflar yaratish
9. ⏳ Test qilish

## Migration qo'llash

```bash
python manage.py migrate
```

## Admin panelda ta'rif yaratish

1. Admin panelga kiring: `/nokia/`
2. "Obunalar" > "Ta'riflar" > "Yangi ta'rif qo'shish"
3. Ma'lumotlarni to'ldiring:
   - Nomi: "EduSelf Pro Basic"
   - Narx: 50000
   - Muddat: 30 kun
   - Cheklovlarni sozlang
4. Saqlang

## Xavfsizlik

- CSRF protection
- Login required decorators
- Payment verification
- Promo code validation
- Referral fraud prevention

## Kelajakda qo'shilishi mumkin

- Avtomatik obuna yangilash
- Obunani bekor qilish
- Obuna tarixi
- Email bildirishnomalar
- SMS bildirishnomalar
- Telegram bot integratsiyasi
- Analytics va reporting
