# 📬 Faol Bo'lmagan Foydalanuvchilarga Eslatma

## Nima Qilindi

3 kun faol bo'lmagan foydalanuvchilarga "Sizni sog'indik" eslatma email yuboriladi.

## ✨ Xususiyatlar

### Qachon Email Yuboriladi?

Email faqat quyidagi shartlar bajarilganda yuboriladi:
- ✅ Foydalanuvchi 3+ kun faol bo'lmagan
- ✅ Email manzili mavjud
- ✅ Email tasdiqlangan
- ✅ Hisob faol (is_active=True)

### Nima Uchun Bu Muhim?

1. **Engagement**: Foydalanuvchilarni qaytarib olish
2. **Retention**: Platformada faol bo'lishni rag'batlantirish
3. **Reminder**: O'qishni davom ettirishni eslatish
4. **Statistics**: Foydalanuvchiga o'z natijalarini ko'rsatish

## 📧 Email Tarkibi

**"Sizni sog'indik" email:**
- 👋 Salom va sog'inish xabari
- 📊 Foydalanuvchi statistikasi:
  - Jami testlar
  - O'tgan testlar
  - Umumiy ball
  - Progress foizi
- 🚀 "Davom etish" tugmasi
- 🎯 Bugungi maqsad
- 🔥 Platformadagi yangiliklar
- 💡 Nima qilish mumkinligi

## 🔧 Texnik Detalllar

### Management Command

```bash
# Dry run (test qilish, email yubormaslik)
python manage.py send_inactive_reminders --dry-run

# Haqiqiy email yuborish
python manage.py send_inactive_reminders

# Boshqa muddat (masalan, 7 kun)
python manage.py send_inactive_reminders --days 7
```

### Command Parametrlari

- `--days N` - Necha kun faol bo'lmagan foydalanuvchilarga yuborish (default: 3)
- `--dry-run` - Faqat ko'rsatish, email yubormaslik (test uchun)

### Code (`accounts/management/commands/send_inactive_reminders.py`)

```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        days = options['days']
        inactive_date = timezone.now() - timedelta(days=days)
        
        # Faol bo'lmagan foydalanuvchilarni topish
        inactive_users = User.objects.filter(
            is_active=True,
            email__isnull=False,
            email_verified=True,
            last_login__lt=inactive_date
        )
        
        # Har biriga email yuborish
        for user in inactive_users:
            send_inactive_reminder_email(user)
```

## 📅 Avtomatik Yuborish (Cron Job)

### Linux/macOS (Crontab)

```bash
# Crontab'ni ochish
crontab -e

# Har kuni soat 10:00 da yuborish
0 10 * * * cd /path/to/eduself && /path/to/python manage.py send_inactive_reminders

# Har 3 kunda bir marta yuborish
0 10 */3 * * cd /path/to/eduself && /path/to/python manage.py send_inactive_reminders
```

### Windows (Task Scheduler)

1. Task Scheduler'ni oching
2. "Create Basic Task" ni tanlang
3. Nom: "EduSelf Inactive Reminders"
4. Trigger: Daily, 10:00 AM
5. Action: Start a program
   - Program: `C:\Python\python.exe`
   - Arguments: `manage.py send_inactive_reminders`
   - Start in: `C:\path\to\eduself`

### Django-Crontab (Python)

```bash
pip install django-crontab
```

`settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'django_crontab',
]

CRONJOBS = [
    # Har kuni soat 10:00 da
    ('0 10 * * *', 'django.core.management.call_command', ['send_inactive_reminders']),
]
```

```bash
# Cron job qo'shish
python manage.py crontab add

# Cron job'larni ko'rish
python manage.py crontab show

# Cron job o'chirish
python manage.py crontab remove
```

### Celery (Advanced)

```python
# tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def send_inactive_reminders():
    call_command('send_inactive_reminders')
```

```python
# celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-inactive-reminders': {
        'task': 'accounts.tasks.send_inactive_reminders',
        'schedule': crontab(hour=10, minute=0),  # Har kuni 10:00
    },
}
```

## 🎯 Foydalanish Stsenariylari

### Stsenariy 1: Yangi Foydalanuvchi
```
1. Foydalanuvchi ro'yxatdan o'tadi
2. 1-2 kun faol bo'ladi
3. 3 kun kirish qilmaydi
4. ✅ Eslatma email keladi
```

### Stsenariy 2: Faol Foydalanuvchi
```
1. Foydalanuvchi har kuni kiradi
2. ❌ Email kelmaydi (faol)
```

### Stsenariy 3: Uzoq Vaqt Kirmaganlar
```
1. Foydalanuvchi 1 oy kirish qilmagan
2. ✅ Eslatma email keladi
3. Qaytib keladi
```

### Stsenariy 4: Email Yo'q
```
1. Foydalanuvchi telefon bilan ro'yxatdan o'tgan
2. Email manzili yo'q
3. ❌ Email kelmaydi
```

## 📊 Statistika

### Email Yuborilish Shartlari:
- ✅ is_active = True
- ✅ Email mavjud
- ✅ Email tasdiqlangan
- ✅ last_login < 3 kun oldin

### Email Tarkibi:
- Foydalanuvchi ismi
- Faol bo'lmaganlik muddati
- Jami testlar soni
- O'tgan testlar soni
- Umumiy ball
- Progress foizi

## 🧪 Test Qilish

### Manual Test

```bash
# Dry run (email yubormaslik)
python manage.py send_inactive_reminders --dry-run

# Haqiqiy yuborish
python manage.py send_inactive_reminders

# 1 kun faol bo'lmaganlar uchun (test)
python manage.py send_inactive_reminders --days 1 --dry-run
```

### Email Template Test

```bash
python send_test_emails.py
```

## 🎨 Customization

### Email Yuborish Muddatini O'zgartirish

```bash
# 7 kun faol bo'lmaganlar uchun
python manage.py send_inactive_reminders --days 7

# 1 kun faol bo'lmaganlar uchun
python manage.py send_inactive_reminders --days 1
```

### Email Matnini O'zgartirish

`templates/emails/inactive_reminder.html` ni tahrirlang.

### Yuborish Shartlarini O'zgartirish

`accounts/management/commands/send_inactive_reminders.py` da filter'ni o'zgartiring:

```python
inactive_users = User.objects.filter(
    is_active=True,
    email__isnull=False,
    email_verified=True,
    last_login__lt=inactive_date,
    # Qo'shimcha shartlar
    total_points__gt=0,  # Faqat ball to'plaganlar
)
```

## 💡 Best Practices

1. **Dry Run First**: Avval `--dry-run` bilan test qiling
2. **Optimal Time**: Eng yaxshi vaqtda yuboring (ertalab 9-10)
3. **Not Too Often**: Juda tez-tez yubormaslik (3-7 kun optimal)
4. **Personalization**: Foydalanuvchi statistikasini ko'rsating
5. **Unsubscribe**: Unsubscribe imkoniyatini qo'shing
6. **Monitoring**: Email yuborilish statistikasini kuzating

## 📈 Monitoring

### Command Output

```
======================================================================
FAOL BO'LMAGAN FOYDALANUVCHILARGA ESLATMA
======================================================================
📅 Faol bo'lmaganlik muddati: 3 kun
📅 Oxirgi faollik: 18.02.2026 16:04
👥 Jami faol bo'lmagan foydalanuvchilar: 15

📧 user1@example.com (John) - 5 kun faol emas
   ✅ Yuborildi
📧 user2@example.com (Jane) - 7 kun faol emas
   ✅ Yuborildi

======================================================================
✅ YAKUNLANDI
======================================================================
📊 Jami: 15
✅ Yuborildi: 15
❌ Xatolik: 0
```

### Logging

Command'dan keyin log faylini tekshiring:
```bash
tail -f logs/inactive_reminders.log
```

## 🔄 Workflow

```
1. Cron job ishga tushadi (har kuni 10:00)
   ↓
2. Command faol bo'lmagan foydalanuvchilarni topadi
   ↓
3. Har biriga email yuboradi
   ↓
4. Natijani log'ga yozadi
   ↓
5. Admin'ga hisobot yuboradi (opsional)
```

## 🛡️ Xavfsizlik

1. **Email Verification**: Faqat tasdiqlangan email'larga yuborish
2. **Rate Limiting**: Bir vaqtda juda ko'p email yubormaslik
3. **Unsubscribe**: Foydalanuvchi rad etish imkoniyati
4. **Privacy**: Foydalanuvchi ma'lumotlarini himoya qilish

## 💡 Kelajakdagi Yaxshilanishlar

1. **Segmentation**: Turli guruhlar uchun turli email'lar
2. **A/B Testing**: Email variantlarini test qilish
3. **Personalization**: Yanada shaxsiylashtirilgan xabarlar
4. **Multi-channel**: Email + Push + SMS
5. **Smart Timing**: Eng yaxshi vaqtni aniqlash
6. **Unsubscribe Management**: Unsubscribe ro'yxatini boshqarish
7. **Analytics**: Email ochilish va click rate'ni kuzatish

## 📞 Yordam

Muammolar bo'lsa:
- Command'ni `--dry-run` bilan test qiling
- Email sozlamalarini tekshiring (`EMAIL_FIX_GUIDE.md`)
- Log fayllarni ko'ring
- `send_test_emails.py` ni ishga tushiring

## 🎓 Foydalanuvchi Uchun

Agar eslatma email kelsa:

### Qaytib kelish:
1. Email'dagi "Davom etish" tugmasini bosing
2. Login qiling
3. O'qishni davom ettiring

### Email olishni to'xtatish:
1. Profilga kiring
2. Sozlamalar → Email xabarlari
3. "Eslatma email'lar" ni o'chiring

---

**Eslatma**: Bu xususiyat foydalanuvchilarni platformada faol bo'lishga undash uchun qo'shildi. Har kuni avtomatik ravishda ishga tushadi.
