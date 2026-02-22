# Kunlik Eslatma Tizimi

## Tavsif
Har kuni soat 07:00 va 14:00 da platformaga kirmaganfoydalanuvchilarga avtomatik eslatma yuborish tizimi.

## Xususiyatlar

### 1. Ertalabki Eslatma (07:00)
- Bugun hali platformaga kirmagan foydalanuvchilarga yuboriladi
- Agar foydalanuvchi soat 07:00 gacha kirsa, eslatma yuborilmaydi
- Email, Telegram va platformada bildirishnoma yuboriladi

### 2. Tushdan Keyingi Eslatma (14:00)
- Faqat ertalab eslatma yuborilgan va hali ham kirmagan foydalanuvchilarga yuboriladi
- Agar foydalanuvchi 07:00 dan keyin kirsa, 14:00 da eslatma yuborilmaydi

## Texnik Tafsilotlar

### Management Command
```bash
# Ertalabki eslatma
python manage.py send_daily_reminders --time=morning

# Tushdan keyingi eslatma
python manage.py send_daily_reminders --time=afternoon
```

### Fayl Tuzilmasi
```
accounts/management/commands/
└── send_daily_reminders.py       # Asosiy command

templates/emails/
└── daily_reminder.html            # Email template
```

### Logika

#### Ertalabki Eslatma (07:00)
1. Bugungi kun boshidan (00:00) beri kirmagan foydalanuvchilarni topish
2. Email tasdiqlangan foydalanuvchilarga yuborish
3. Email, Telegram va platformada bildirishnoma yaratish

#### Tushdan Keyingi Eslatma (14:00)
1. Bugun ertalab eslatma yuborilgan foydalanuvchilarni topish
2. Hali ham kirmagan foydalanuvchilarga yuborish
3. Email, Telegram va platformada bildirishnoma yaratish

### Filtrlash
```python
# Bugun kirmagan foydalanuvchilar
today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

inactive_today = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True
).exclude(
    last_login__gte=today_start
).exclude(email='')
```

## Cron Job Sozlamalari

### Render.com
```
Name: Daily Morning Reminder
Command: python manage.py send_daily_reminders --time=morning
Schedule: 0 7 * * *
Description: Har kuni soat 07:00 da ertalabki eslatma yuborish

Name: Daily Afternoon Reminder
Command: python manage.py send_daily_reminders --time=afternoon
Schedule: 0 14 * * *
Description: Har kuni soat 14:00 da tushdan keyingi eslatma yuborish
```

### Cron Syntax
```
0 7 * * *   # Har kuni 07:00
0 14 * * *  # Har kuni 14:00
```

## Email Template

### Ertalabki Eslatma
- **Subject**: EduSelf - Bugun o'qishni boshlaymizmi? 📚
- **Icon**: 🌅
- **Message**: Xayrli tong! Bugun o'qishni boshlaymizmi?

### Tushdan Keyingi Eslatma
- **Subject**: EduSelf - Bugun hali o'qimadingiz 📖
- **Icon**: ☀️
- **Message**: Bugun hali platformaga kirmaganingizni ko'rdik

## Telegram Bildirishnoma

### Ertalabki
```
🌅 Xayrli tong!

Bugun EduSelf platformasida o'qishni boshlaganingiz yo'qmi?

Har kuni 15-20 daqiqa o'qish bilimingizni oshiradi! 📚
```

### Tushdan Keyingi
```
☀️ Bugun hali o'qimadingiz

Faqat 10-15 daqiqa vaqt ajrating va bilimingizni oshiring!

Keling, bugun biror narsa o'rganamiz? 📖
```

## Platformada Bildirishnoma

### Ertalabki
- **Title**: 🌅 Bugun o'qishni boshlaymizmi?
- **Message**: Har kuni 15-20 daqiqa o'qish sizning bilimingizni oshiradi
- **Type**: reminder
- **Icon**: 📚

### Tushdan Keyingi
- **Title**: ☀️ Bugun hali o'qimadingiz
- **Message**: Faqat 10-15 daqiqa vaqt ajrating va bilimingizni oshiring!
- **Type**: reminder
- **Icon**: 📖

## Test Qilish

### Local Test
```bash
# Statistikani ko'rish
python test_daily_reminders.py

# Ertalabki eslatma test
python manage.py send_daily_reminders --time=morning

# Tushdan keyingi eslatma test
python manage.py send_daily_reminders --time=afternoon
```

### Production Test
1. Render.com dashboard'ga kiring
2. Cron Jobs bo'limiga o'ting
3. "Run Now" tugmasini bosing
4. Logs'ni tekshiring

## Monitoring

### Logs
```bash
# Command logs
python manage.py send_daily_reminders --time=morning

# Output:
# ================================================================================
# KUNLIK ESLATMA - MORNING
# ================================================================================
# 📊 Bugun kirmagan foydalanuvchilar: 95
# 🌅 ERTALABKI ESLATMA (07:00)
# --------------------------------------------------------------------------------
# 📊 Natijalar:
#    📧 Email yuborildi: 95
#    💬 Telegram yuborildi: 60
#    🔔 Bildirishnoma yaratildi: 95
```

### Statistika
```python
# Bugun kirmagan foydalanuvchilar
inactive_count = User.objects.filter(
    is_active=True,
    last_login__lt=today_start
).count()

# Bugun kirgan foydalanuvchilar
active_count = User.objects.filter(
    is_active=True,
    last_login__gte=today_start
).count()
```

## Email Backend
- **From**: eduselfuz@gmail.com (avtomatik emaillar)
- **Type**: Avtomatik eslatma
- **Template**: templates/emails/daily_reminder.html

## Xavfsizlik
- Faqat email tasdiqlangan foydalanuvchilarga yuboriladi
- Faqat faol foydalanuvchilarga yuboriladi
- Spam bo'lmasligi uchun kuniga maksimum 2 marta (07:00 va 14:00)

## Kelajakdagi Yaxshilanishlar
1. Foydalanuvchi sozlamalari (eslatmani o'chirish/yoqish)
2. Eslatma vaqtini sozlash
3. Haftalik/oylik statistika
4. A/B testing (turli xabarlar)
5. Personalizatsiya (foydalanuvchi faoliyatiga qarab)

## Muammolarni Hal Qilish

### Email kelmayapti
1. Spam papkasini tekshiring
2. Email backend sozlamalarini tekshiring
3. Gmail App Password to'g'riligini tekshiring

### Telegram kelmayapti
1. Bot token to'g'riligini tekshiring
2. Foydalanuvchi telegram_chat_id borligini tekshiring
3. Bot logs'ni tekshiring

### Cron job ishlamayapti
1. Render.com dashboard'da cron job statusini tekshiring
2. Logs'ni tekshiring
3. Command syntax to'g'riligini tekshiring

## Qo'shimcha Ma'lumot
- Timezone: UTC (Render.com default)
- O'zbekiston vaqti: UTC+5
- 07:00 O'zbekiston = 02:00 UTC
- 14:00 O'zbekiston = 09:00 UTC

**Eslatma**: Cron schedule'ni O'zbekiston vaqtiga moslashtiring!
