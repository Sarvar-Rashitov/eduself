# Gunicorn Worker Timeout Fix

## Muammo

Admin paneldan notification yaratilganda email yuborish juda uzoq vaqt oladi va Gunicorn worker timeout bo'ladi:

```
[CRITICAL] WORKER TIMEOUT (pid:61)
SystemExit: 1
```

## Sabab

- Global notification yaratilganda barcha foydalanuvchilarga email yuboriladi
- Har bir email yuborish 1-2 soniya oladi
- 100+ foydalanuvchi bo'lsa, 100+ soniya ketadi
- Gunicorn default timeout: 30 soniya
- Natija: Worker timeout va 500 error

## Yechim: Async Email Yuborish

Email yuborishni background thread'da bajardik:

### O'zgarishlar

**core/signals.py:**
```python
import threading

def send_emails_async(notification):
    """Email yuborishni background thread'da bajarish"""
    def _send_emails():
        # Email yuborish logikasi
        ...
    
    # Background thread'da ishga tushirish
    thread = threading.Thread(target=_send_emails)
    thread.daemon = True
    thread.start()

@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if not created:
        return
    
    # Async yuborish
    send_emails_async(instance)
```

### Afzalliklari

1. ✅ Admin panel darhol javob qaytaradi (1 soniyadan kam)
2. ✅ Worker timeout bo'lmaydi
3. ✅ Email yuborish background'da davom etadi
4. ✅ Foydalanuvchi tajribasi yaxshilanadi

### Qanday Ishlaydi

```
Admin notification yaratadi
    ↓
Signal ishga tushadi (< 1 soniya)
    ↓
Background thread yaratiladi
    ↓
Admin panel success message ko'rsatadi
    ↓
Background'da email yuboriladi (30+ soniya)
```

## Test Qilish

1. Admin panelga kiring: `/nokia/`
2. Yangi notification yarating
3. Darhol success message ko'rinadi
4. Email yuborish background'da davom etadi
5. Log'larda ko'rish mumkin:

```bash
# Production log'larni ko'rish
tail -f /var/log/gunicorn/error.log

# Yoki Render dashboard'da
```

## Production Deploy

```bash
# Git'ga commit qiling
git add core/signals.py GUNICORN_TIMEOUT_FIX.md
git commit -m "Fix: Async email sending to prevent Gunicorn timeout"
git push origin main

# Render avtomatik deploy qiladi
```

## Monitoring

Log'larda quyidagilarni ko'rasiz:

```
INFO: Email yuborish background thread'da boshlandi
INFO: Global notification: 258 ta foydalanuvchiga yuborilmoqda
INFO: Notification email yuborildi: user1@example.com
INFO: Notification email yuborildi: user2@example.com
...
INFO: Global notification email yuborish tugadi: 258/258
```

## Muqobil Yechimlar

### 1. Celery (Kelajakda)

Agar loyiha katta bo'lsa, Celery ishlatish yaxshiroq:

```python
from celery import shared_task

@shared_task
def send_notification_emails(notification_id):
    notification = Notification.objects.get(id=notification_id)
    # Email yuborish
```

### 2. Django-Q (Yengil alternativa)

```python
from django_q.tasks import async_task

async_task('core.tasks.send_notification_emails', notification.id)
```

### 3. Gunicorn Timeout Oshirish (TAVSIYA ETILMAYDI)

```python
# gunicorn.conf.py
timeout = 120  # 2 daqiqa
```

**Nima uchun yomon:**
- Worker uzoq vaqt band bo'ladi
- Boshqa request'lar kutadi
- Resource'lar behuda ishlatiladi

## Xulosa

✅ Async email yuborish eng yaxshi yechim
✅ Admin panel tez ishlaydi
✅ Email yuborish background'da
✅ Worker timeout muammosi hal qilindi

---

**Sana:** 21 Fevral 2026
**Status:** ✅ Hal qilindi
