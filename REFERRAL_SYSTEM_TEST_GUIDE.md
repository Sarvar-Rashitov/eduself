# Referal Tizimini Test Qilish

## Referal Tizimi Haqida

Referal tizimi foydalanuvchilarga do'stlarini taklif qilish orqali bepul Pro obunasini olish imkonini beradi.

## Qanday Ishlaydi?

1. **Referal linki olish**: Foydalanuvchi referal sahifasiga kiradi va o'zining maxsus referal linkini oladi
2. **Linkni ulashish**: Foydalanuvchi linkni do'stlari bilan ulashadi
3. **Ro'yxatdan o'tish**: Do'st referal linki orqali ro'yxatdan o'tadi
4. **Avtomatik hisoblash**: Tizim avtomatik ravishda referal hisobini yangilaydi
5. **Mukofot berish**: Shart bajarilganda avtomatik Pro obuna beriladi

## Test Qilish Bosqichlari

### 1. Referal Dasturini Yaratish (Admin Panel)

```bash
python manage.py shell
```

```python
from subscriptions.models import SubscriptionPlan, ReferralProgram
from datetime import timedelta

# Ta'rifni olish
plan = SubscriptionPlan.objects.first()

# Referal dasturini yaratish
program = ReferralProgram.objects.create(
    name="3 Do'st - 30 Kun Pro",
    plan=plan,
    required_referrals=3,  # 3 ta do'st taklif qilish kerak
    referral_deadline_days=30,  # 30 kun ichida
    reward_duration_days=30,  # 30 kunlik obuna beriladi
    is_active=True
)
print(f"✅ Referal dasturi yaratildi: {program}")
```

### 2. Referal Linkini Olish

1. Birinchi foydalanuvchi sifatida tizimga kiring
2. Referal sahifasiga o'ting: `/subscriptions/referral/`
3. Referal linkini ko'ring va nusxalang
4. Link formati: `https://eduself.uz/accounts/register/?ref=USER_ID`

### 3. Yangi Foydalanuvchi Ro'yxatdan O'tkazish

#### Variant 1: Brauzerda Test Qilish

1. Yangi incognito/private oynani oching
2. Referal linkini kiriting
3. Ro'yxatdan o'tish formasini to'ldiring
4. "Ro'yxatdan o'tish" tugmasini bosing

#### Variant 2: Boshqa Brauzerda Test Qilish

1. Boshqa brauzer oching (Chrome, Firefox, Edge)
2. Referal linkini kiriting
3. Ro'yxatdan o'tish formasini to'ldiring

#### Variant 3: Mobil Qurilmada Test Qilish

1. Telefonda brauzer oching
2. Referal linkini kiriting
3. Ro'yxatdan o'tish formasini to'ldiring

### 4. Referal Hisobini Tekshirish

1. Birinchi foydalanuvchi sifatida qaytib kiring
2. Referal sahifasiga o'ting
3. Quyidagilarni tekshiring:
   - ✅ "Taklif qilingan do'stlar" ro'yxatida yangi foydalanuvchi ko'rinadi
   - ✅ "Sizning jarayoningiz" bo'limida hisob yangilangan
   - ✅ Progress bar to'g'ri ko'rsatiladi

### 5. Mukofotni Tekshirish

Agar kerakli miqdorda do'stlar taklif qilingan bo'lsa:

1. Referal sahifasida "Bajarildi" belgisi ko'rinadi
2. Pro sahifasiga o'ting: `/subscriptions/pro/`
3. Faol obuna ko'rinishi kerak
4. Profil sahifasida Pro badge ko'rinadi

## Database Orqali Tekshirish

### Referal Ma'lumotlarini Ko'rish

```bash
python manage.py shell
```

```python
from accounts.models import User
from subscriptions.models import UserReferral, ReferralProgress

# Foydalanuvchini topish
user = User.objects.get(email='test@example.com')

# Referal hisobini ko'rish
referrals = UserReferral.objects.filter(referrer=user)
print(f"Taklif qilingan do'stlar: {referrals.count()}")
for ref in referrals:
    print(f"  - {ref.referred.get_display_name()} ({ref.created_at})")

# Jarayonni ko'rish
progress = ReferralProgress.objects.filter(user=user)
for p in progress:
    print(f"\nDastur: {p.program.name}")
    print(f"Hisob: {p.referral_count}/{p.program.required_referrals}")
    print(f"Bajarilgan: {p.is_completed}")
    print(f"Mukofot berilgan: {p.reward_given}")
```

### Qo'lda Mukofot Berish (Test Uchun)

```python
from subscriptions.models import UserSubscription, ReferralProgram
from django.utils import timezone
from datetime import timedelta

user = User.objects.get(email='test@example.com')
program = ReferralProgram.objects.first()

# Obuna yaratish
subscription = UserSubscription.objects.create(
    user=user,
    plan=program.plan,
    start_date=timezone.now(),
    end_date=timezone.now() + timedelta(days=program.reward_duration_days),
    status='active',
    acquired_via='referral'
)
print(f"✅ Obuna berildi: {subscription}")
```

## Xatoliklarni Tuzatish

### Xatolik 1: Ro'yxatdan o'tish ishlamayapti

**Sabab**: Session ma'lumotlari saqlanmayapti

**Yechim**:
```python
# settings.py da tekshiring
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 soat
```

### Xatolik 2: Referal hisobi yangilanmayapti

**Sabab**: Referal dasturi faol emas

**Yechim**:
```python
from subscriptions.models import ReferralProgram

# Barcha dasturlarni faollashtirish
ReferralProgram.objects.all().update(is_active=True)
```

### Xatolik 3: Mukofot berilmayapti

**Sabab**: Shart bajarilmagan yoki deadline o'tgan

**Yechim**:
```python
from subscriptions.models import ReferralProgress

# Jarayonni tekshirish
progress = ReferralProgress.objects.filter(user=user).first()
print(f"Hisob: {progress.referral_count}/{progress.program.required_referrals}")
print(f"Deadline: {progress.deadline}")
print(f"Bajarilgan: {progress.is_completed}")

# Qo'lda bajarilgan deb belgilash
if progress.referral_count >= progress.program.required_referrals:
    progress.is_completed = True
    progress.save()
    print("✅ Bajarilgan deb belgilandi")
```

## Admin Panelda Monitoring

1. Admin panelga kiring: `/admin/`
2. "Subscriptions" bo'limiga o'ting
3. Quyidagilarni tekshiring:
   - **Referal dasturlari**: Faol dasturlar ro'yxati
   - **Foydalanuvchi referallari**: Barcha referal bog'lanishlar
   - **Referal jarayonlari**: Har bir foydalanuvchining jarayoni

## Test Ssenariysi

### Ssenariy 1: Muvaffaqiyatli Referal

1. ✅ User A referal linkini oladi
2. ✅ User B referal linki orqali ro'yxatdan o'tadi
3. ✅ User A referal sahifasida User B ni ko'radi
4. ✅ User C va User D ham ro'yxatdan o'tadi
5. ✅ User A 3 ta do'st taklif qildi
6. ✅ User A ga avtomatik Pro obuna beriladi

### Ssenariy 2: Deadline O'tishi

1. ✅ User A referal linkini oladi
2. ✅ User B ro'yxatdan o'tadi (1/3)
3. ❌ 30 kun o'tadi
4. ❌ Deadline o'tgani uchun mukofot berilmaydi

### Ssenariy 3: Bir Nechta Dastur

1. ✅ 2 ta referal dasturi mavjud (3 do'st, 5 do'st)
2. ✅ User A 3 ta do'st taklif qiladi
3. ✅ Birinchi dastur bajariladi, obuna beriladi
4. ✅ User A yana 2 ta do'st taklif qiladi
5. ✅ Ikkinchi dastur ham bajariladi, yana obuna beriladi

## Monitoring va Statistika

### Referal Statistikasini Ko'rish

```python
from subscriptions.models import UserReferral, ReferralProgress
from django.db.models import Count

# Eng ko'p referal qilgan foydalanuvchilar
top_referrers = UserReferral.objects.values('referrer__first_name', 'referrer__last_name')\
    .annotate(count=Count('id'))\
    .order_by('-count')[:10]

print("Top 10 Referrers:")
for ref in top_referrers:
    print(f"  {ref['referrer__first_name']} {ref['referrer__last_name']}: {ref['count']} ta")

# Bajarilgan dasturlar
completed = ReferralProgress.objects.filter(is_completed=True, reward_given=True).count()
print(f"\nBajarilgan dasturlar: {completed}")
```

## Xulosa

Referal tizimi to'liq avtomatik ishlaydi:
- ✅ Referal linki avtomatik yaratiladi
- ✅ Ro'yxatdan o'tish avtomatik qayd qilinadi
- ✅ Hisob avtomatik yangilanadi
- ✅ Mukofot avtomatik beriladi

Agar biror narsa ishlamasa, yuqoridagi xatoliklarni tuzatish bo'limiga qarang.
