# ⏰ Cron Job Sozlash - Avtomatik Email Yuborish

## Nima Uchun Kerak?

Faol bo'lmagan foydalanuvchilarga avtomatik ravishda eslatma email yuborish uchun cron job sozlash kerak.

## 🚀 Tez Boshlash

### 1. Command'ni Test Qilish

```bash
# Dry run (email yubormaslik)
python manage.py send_inactive_reminders --dry-run

# Haqiqiy yuborish
python manage.py send_inactive_reminders
```

### 2. Cron Job Sozlash

#### Linux/macOS

```bash
# Crontab'ni ochish
crontab -e

# Har kuni soat 10:00 da yuborish
0 10 * * * cd /path/to/eduself && /path/to/venv/bin/python manage.py send_inactive_reminders >> /path/to/logs/cron.log 2>&1
```

#### Windows (Task Scheduler)

1. Task Scheduler'ni oching (taskschd.msc)
2. "Create Basic Task" ni tanlang
3. Sozlamalar:
   - **Name**: EduSelf Inactive Reminders
   - **Trigger**: Daily, 10:00 AM
   - **Action**: Start a program
     - **Program**: `C:\path\to\venv\Scripts\python.exe`
     - **Arguments**: `manage.py send_inactive_reminders`
     - **Start in**: `C:\path\to\eduself`

## 📅 Cron Syntax

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Hafta kuni (0-7, 0 va 7 = Yakshanba)
│ │ │ └───── Oy (1-12)
│ │ └─────── Kun (1-31)
│ └───────── Soat (0-23)
└─────────── Daqiqa (0-59)
```

### Misollar

```bash
# Har kuni soat 10:00 da
0 10 * * * command

# Har kuni soat 9:00 va 18:00 da
0 9,18 * * * command

# Har 3 kunda bir marta soat 10:00 da
0 10 */3 * * command

# Dushanbadan Jumagacha soat 10:00 da
0 10 * * 1-5 command

# Har oyning 1-kunida soat 10:00 da
0 10 1 * * command
```

## 🐍 Django-Crontab (Tavsiya Etiladi)

### 1. O'rnatish

```bash
pip install django-crontab
```

### 2. Sozlash

`settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'django_crontab',
]

CRONJOBS = [
    # Har kuni soat 10:00 da faol bo'lmaganlik eslatmasi
    ('0 10 * * *', 'django.core.management.call_command', ['send_inactive_reminders']),
    
    # Har hafta dushanba soat 9:00 da haftalik hisobot (kelajakda)
    # ('0 9 * * 1', 'django.core.management.call_command', ['send_weekly_report']),
]

# Log fayl
CRONTAB_COMMAND_SUFFIX = '2>&1'
```

### 3. Cron Job'larni Boshqarish

```bash
# Cron job qo'shish
python manage.py crontab add

# Cron job'larni ko'rish
python manage.py crontab show

# Cron job o'chirish
python manage.py crontab remove
```

## 🔥 Celery (Advanced)

Agar loyihangizda Celery bo'lsa:

### 1. O'rnatish

```bash
pip install celery redis
```

### 2. Task Yaratish

`accounts/tasks.py`:
```python
from celery import shared_task
from django.core.management import call_command

@shared_task
def send_inactive_reminders():
    """Faol bo'lmagan foydalanuvchilarga eslatma yuborish"""
    call_command('send_inactive_reminders')
    return 'Inactive reminders sent'
```

### 3. Beat Schedule

`eduself/celery.py`:
```python
from celery import Celery
from celery.schedules import crontab

app = Celery('eduself')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-inactive-reminders': {
        'task': 'accounts.tasks.send_inactive_reminders',
        'schedule': crontab(hour=10, minute=0),  # Har kuni 10:00
    },
}
```

### 4. Ishga Tushirish

```bash
# Celery worker
celery -A eduself worker -l info

# Celery beat (scheduler)
celery -A eduself beat -l info
```

## 📊 Monitoring

### Log Fayllar

```bash
# Cron log
tail -f /var/log/cron.log

# Django log
tail -f logs/inactive_reminders.log
```

### Email Hisoboti

Command'dan keyin admin'ga hisobot yuborish:

`accounts/management/commands/send_inactive_reminders.py`:
```python
# Oxirida
if sent_count > 0:
    send_mail(
        subject=f'EduSelf - Inactive Reminders Report',
        message=f'Sent: {sent_count}, Failed: {failed_count}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
    )
```

## 🧪 Test Qilish

### Manual Test

```bash
# Dry run
python manage.py send_inactive_reminders --dry-run

# 1 kun faol bo'lmaganlar (test)
python manage.py send_inactive_reminders --days 1 --dry-run

# Haqiqiy yuborish
python manage.py send_inactive_reminders
```

### Cron Test

```bash
# Cron job'ni darhol ishga tushirish (test)
# Linux/macOS
/path/to/venv/bin/python /path/to/eduself/manage.py send_inactive_reminders

# Windows
C:\path\to\venv\Scripts\python.exe C:\path\to\eduself\manage.py send_inactive_reminders
```

## 🔧 Troubleshooting

### Cron Job Ishlamayapti

1. **Path'larni tekshiring**:
   ```bash
   which python  # Python path
   pwd           # Project path
   ```

2. **Log'larni ko'ring**:
   ```bash
   tail -f /var/log/cron.log
   ```

3. **Manually test qiling**:
   ```bash
   cd /path/to/eduself
   /path/to/venv/bin/python manage.py send_inactive_reminders
   ```

4. **Environment variables**:
   ```bash
   # Crontab'da
   SHELL=/bin/bash
   PATH=/usr/local/bin:/usr/bin:/bin
   DJANGO_SETTINGS_MODULE=eduself.settings
   ```

### Email Yuborilmayapti

1. **Email sozlamalarini tekshiring**:
   ```bash
   python test_email.py
   ```

2. **Gmail App Password**:
   - `.env` faylida to'g'ri kiritilganini tekshiring
   - Bo'sh joylar yo'qligini tekshiring

3. **Dry run test**:
   ```bash
   python manage.py send_inactive_reminders --dry-run
   ```

## 💡 Best Practices

1. **Optimal Vaqt**: Ertalab 9-10 da yuborish (foydalanuvchilar faol vaqt)
2. **Dry Run First**: Avval test qiling
3. **Logging**: Har doim log yozing
4. **Monitoring**: Email yuborilish statistikasini kuzating
5. **Rate Limiting**: Juda ko'p email yubormaslik
6. **Error Handling**: Xatolarni to'g'ri handle qiling

## 📈 Production Sozlamalari

### Render.com

Render.com'da cron job qo'shish:

1. Dashboard → Cron Jobs
2. "New Cron Job" ni bosing
3. Sozlamalar:
   - **Name**: inactive-reminders
   - **Command**: `python manage.py send_inactive_reminders`
   - **Schedule**: `0 10 * * *`

### Heroku

```bash
# Heroku Scheduler add-on
heroku addons:create scheduler:standard

# Scheduler'ni ochish
heroku addons:open scheduler

# Job qo'shish
# Command: python manage.py send_inactive_reminders
# Frequency: Daily at 10:00 AM
```

### AWS (Lambda + CloudWatch)

1. Lambda function yarating
2. CloudWatch Events bilan trigger qo'shing
3. Cron expression: `cron(0 10 * * ? *)`

## 🎯 Xulosa

Cron job sozlash:
1. ✅ Command'ni test qiling
2. ✅ Cron job qo'shing
3. ✅ Log'larni sozlang
4. ✅ Monitoring qo'shing
5. ✅ Production'da test qiling

---

**Eslatma**: Cron job sozlangandan keyin, har kuni avtomatik ravishda faol bo'lmagan foydalanuvchilarga eslatma email yuboriladi.
